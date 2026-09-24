# fairtool/visualize.py

"""Builds and serves the local mkdocs site for browsing processed calculation data."""

import logging
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Optional

log = logging.getLogger("fairtool")

# --- Helper Functions ---


def _hr_size(num_bytes: int) -> str:
    """Human readable file size."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num_bytes < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"


def _extract_title(file_path):
    """Return title from markdown (# Heading) or HTML (<title>) file."""
    try:
        with open(file_path, encoding="utf-8") as fh:
            text = fh.read(4096)  # Read only the first 4KB for speed
            # Markdown H1 title
            match = re.search(r"^\s*#\s+(.+)", text, re.MULTILINE)
            if match:
                return match.group(1).strip()
            # HTML <title>...</title>
            match = re.search(r"<title>(.*?)</title>", text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
    except Exception:
        pass
    return "—"


# The mkdocs site template (mkdocs.yml, macros.py, theme overrides, hooks and
# static assets) ships as package data inside `fairtool`, so `serve_docs` works
# the same from a wheel install as from a source checkout.
SITE_TEMPLATE = "site_template"


def _site_template() -> Traversable:
    """Return the packaged mkdocs site template directory."""
    return resources.files("fairtool") / SITE_TEMPLATE


def _copy_resource_tree(src: Traversable, dest: Path) -> None:
    """Recursively copy a packaged resource directory to `dest` on disk, skipping bytecode caches."""
    dest.mkdir(parents=True, exist_ok=True)
    for entry in src.iterdir():
        if entry.name == "__pycache__":
            continue
        if entry.is_dir():
            _copy_resource_tree(entry, dest / entry.name)
        else:
            (dest / entry.name).write_bytes(entry.read_bytes())


# --- Main Execution Logic ---


def serve_docs(
    docs_path: Path, port: int = 8000, dry_run: bool = False, build: bool = False, build_dir: Optional[Path] = None
):
    """
    Launch an mkdocs server that uses the packaged site template (mkdocs.yml,
    macros.py, theme overrides) while scanning `docs_path` for the markdown files.

    This function creates a temporary mkdocs config that points `docs_dir` to the
    provided `docs_path` while keeping the rest of the packaged `mkdocs.yml` and
    ensuring `macros.py` is placed next to the config file as required by the
    macros plugin.
    """
    docs_path = Path(docs_path).resolve()
    if not docs_path.exists():
        log.error(f"Docs path does not exist: {docs_path}")
        raise SystemExit(1)

    # Locate the site template shipped as package data inside `fairtool`
    template = _site_template()
    packaged_docs = template / "docs"
    packaged_mkdocs = template / "mkdocs.yml"
    packaged_macros = template / "macros.py"

    if not packaged_mkdocs.is_file():
        log.error(f"Packaged mkdocs.yml not found at expected location: {packaged_mkdocs}")
        raise SystemExit(1)

    # Create a temporary directory to host the modified mkdocs config (and macros)
    temp_dir = Path(tempfile.mkdtemp(prefix="fairtool-mkdocs-"))
    try:
        temp_mkdocs = temp_dir / "mkdocs.yml"

        # Read packaged mkdocs.yml and ensure docs_dir is set to the user-provided path.
        content = packaged_mkdocs.read_text(encoding="utf-8")

        # Create a temporary docs directory that merges user docs and packaged static assets.
        temp_docs = temp_dir / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        # Copy user-provided docs into temp_docs (do not modify original)
        try:
            if docs_path.is_dir():
                for src in docs_path.rglob("*"):
                    rel = src.relative_to(docs_path)
                    dest = temp_docs / rel
                    if src.is_dir():
                        dest.mkdir(parents=True, exist_ok=True)
                    else:
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src, dest)
            else:
                # single file -> copy into temp_docs
                shutil.copy2(docs_path, temp_docs / docs_path.name)
        except Exception:
            log.warning("Failed to copy user docs into temporary docs directory; continuing with limited content.")

        # Copy packaged static assets (stylesheets, js, assets) and any `includes/`
        # used by snippets into temp_docs, so files like stylesheets/extra.css,
        # js/structure.js and assets/logo.png are available to the dev server and avoid 404s.
        for static_name in ("stylesheets", "js", "assets", "includes"):
            src = packaged_docs / static_name
            if not src.is_dir():
                log.debug(f"No packaged static folder found for '{static_name}' in {packaged_docs}")
                continue
            try:
                _copy_resource_tree(src, temp_docs / static_name)
                log.debug(f"Copied static folder {src} -> {temp_docs / static_name}")
            except Exception as e:
                log.debug(f"Could not copy packaged static folder {src}: {e}")

        # If the packaged docs include a homepage (README.md or index.md), copy
        # that into the temporary docs root so the packaged theme overrides
        # (which often target the site homepage) are applied. Do not overwrite
        # any user-provided file.
        for candidate in ("README.md", "index.md"):
            src_home = packaged_docs / candidate
            if src_home.is_file() and not (temp_docs / candidate).exists():
                try:
                    (temp_docs / candidate).write_bytes(src_home.read_bytes())
                    log.debug(f"Copied packaged homepage {src_home} -> {temp_docs / candidate}")
                    # Stop after copying the first available candidate
                    break
                except Exception:
                    log.debug(f"Failed to copy packaged homepage {src_home}")

        # Ensure there's an index.md so the site root renders instead of 404
        try:
            # MkDocs expects an `index.md` at the site root when a nav entry
            # references 'index.md'. Older projects sometimes use README.md;
            # prefer index.md and copy README.md -> index.md when present so
            # the nav and files stay in sync and mkdocs doesn't warn.
            index_file = temp_docs / "index.md"
            readme_file = temp_docs / "README.md"

            # Only create a generated index.md if neither README.md nor
            # index.md already exist. If README.md is present, prefer it as
            # the site homepage so packaged theme overrides targeting the
            # homepage can be applied.
            if not index_file.exists() and not readme_file.exists():
                # Build an index that shows the output of `tree` in a bash code block
                all_md = sorted([p for p in temp_docs.rglob("*.md")])

                def tree_lines_for_dir(root: Path) -> list[str]:
                    lines = []

                    def _walk(dirpath: Path, prefix: str = ""):
                        entries = sorted([p for p in dirpath.iterdir() if not p.name.startswith("__")])
                        dirs = [
                            e
                            for e in entries
                            if e.is_dir() and any(f.suffix.lower() in (".md", ".markdown") for f in e.rglob("*.md"))
                        ]
                        # files not shown at folder level per user request
                        for i, d in enumerate(dirs):
                            last = i == len(dirs) - 1
                            connector = "└── " if last else "├── "
                            lines.append(f"{prefix}{connector}{d.name}")
                            _walk(d, prefix + ("    " if last else "│   "))

                    # include root label
                    lines.append(str(root.name) + "/")
                    _walk(root)
                    return lines

                total_dirs = len([d for d in temp_docs.rglob("*") if d.is_dir() and d != temp_docs])
                total_md = len(all_md)

                tree_lines = tree_lines_for_dir(temp_docs)

                with open(index_file, "w", encoding="utf-8") as idx:
                    idx.write("# FAIR Tool - Local Preview\n\n")
                    idx.write("This is a local preview generated by `fair visualize`.\n\n")

                    # Stats
                    idx.write("## Summary\n\n")
                    idx.write(f"- Total folders: **{total_dirs}**\n")
                    idx.write(f"- Markdown pages: **{total_md}**\n\n")

                    # Tree (as output of `tree` inside a bash code block)
                    idx.write("## Pages and Folders (tree)\n\n")
                    idx.write("```bash\n")
                    for tree_line in tree_lines:
                        idx.write(tree_line + "\n")
                    idx.write("```\n")
        except Exception:
            log.debug("Failed to create temporary index.md")

        # Try to replace an existing docs_dir entry in the packaged config; point to temp_docs instead.
        if re.search(r"^\s*docs_dir\s*:\s*.+$", content, flags=re.MULTILINE):
            content = re.sub(r"^\s*docs_dir\s*:\s*.+$", f"docs_dir: '{str(temp_docs)}'", content, flags=re.MULTILINE)
        else:
            # Insert at top
            content = f"docs_dir: '{str(temp_docs)}'\n" + content

        # Override site_url and directory URL handling to ensure dev server serves assets from root
        # and doesn't prepend the packaged site_url (which was set to /fairtool/).
        # Insert or replace site_url and use_directory_urls settings.
        if re.search(r"^\s*site_url\s*:\s*.+$", content, flags=re.MULTILINE):
            content = re.sub(
                r"^\s*site_url\s*:\s*.+$", f"site_url: 'http://127.0.0.1:{int(port)}'", content, flags=re.MULTILINE
            )
        else:
            # insert after docs_dir line
            content = content.replace(
                f"docs_dir: '{str(temp_docs)}'\n",
                f"docs_dir: '{str(temp_docs)}'\nsite_url: 'http://127.0.0.1:{int(port)}'\n",
            )

        if re.search(r"^\s*use_directory_urls\s*:\s*.+$", content, flags=re.MULTILINE):
            content = re.sub(
                r"^\s*use_directory_urls\s*:\s*.+$", "use_directory_urls: false", content, flags=re.MULTILINE
            )
        else:
            content = content.replace(
                f"site_url: 'http://127.0.0.1:{int(port)}'\n",
                f"site_url: 'http://127.0.0.1:{int(port)}'\nuse_directory_urls: false\n",
            )

        # Some mkdocs plugins referenced in the packaged mkdocs.yml may not be
        # installed in the user's environment (for example: include_dir_to_nav).
        # If 'include_dir_to_nav' is referenced we try to import it — if it's
        # available we keep it so mkdocs can auto-generate directory-based nav;
        # otherwise we remove it to avoid a hard failure.
        if "include_dir_to_nav" in content:
            try:
                import importlib

                importlib.import_module("include_dir_to_nav")
                log.info(
                    "'include_dir_to_nav' plugin is available in the environment; keeping it in temporary mkdocs config."
                )
            except Exception:
                log.warning(
                    "Detected 'include_dir_to_nav' plugin in packaged mkdocs.yml; plugin not importable in this environment — removing it for live serve. Consider installing the plugin if you need its behavior."
                )
                # Remove lines like '- include_dir_to_nav' or '  include_dir_to_nav: ...'
                content = re.sub(r"(?m)^[ \t]*-?[ \t]*include_dir_to_nav(?::.*)?$\n(?:^[ \t]+[^\n]*$\n)*", "", content)

        # Build a nav that keeps the top-level horizontal navigation small while
        # exposing directory names in the vertical sidebar. We create a single
        # parent -> root grouping (so horizontal nav shows only Home + parent)
        # and then list directories under that root. For page labels we try to
        # extract the first H1 heading from the markdown; fall back to a
        # humanized filename if none is found. This avoids showing raw filenames
        # like 'vasprun' in the nav.

        def humanize(stem: str) -> str:
            stem = re.sub(r"^(fair_summarized_|fair_parsed_|fair-)", "", stem)
            stem = stem.replace("_", " ").replace("-", " ")
            return stem.strip().replace(".md", "").title()

        def first_h1_title(p: Path) -> str:
            try:
                with open(p, "r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if line.startswith("#"):
                            # remove leading hashes and whitespace
                            title = line.lstrip("#").strip()
                            if title.lower() in ("home", "index"):
                                return humanize(p.stem)
                            return title
            except Exception:
                pass
            return humanize(p.stem)

        def has_markdown(dirpath: Path) -> bool:
            for _ in dirpath.rglob("*.md"):
                return True
            return False

        def build_nav_object_for_dir(dirpath: Path):
            # Only directories (and their index pages) should appear in the
            # navigation. Individual filenames are not shown. If a directory
            # contains exactly one markdown file and no subdirectories we link
            # directly to that page. Otherwise we ensure an `index.md` exists
            # for the directory (creating one if necessary) and use that as the
            # directory's entry; child directories are nested underneath.
            pages = sorted([p for p in dirpath.glob("*.md") if p.name != "index.md"])
            children = sorted([d for d in dirpath.iterdir() if d.is_dir() and has_markdown(d)])

            # Single-file directory -> link directly to the file
            if len(pages) == 1 and not children:
                return pages[0].relative_to(temp_docs).as_posix()

            # Ensure an index.md exists for the directory so the nav links to
            # the directory rather than to individual pages.
            idx = dirpath / "index.md"
            if not idx.exists():
                try:
                    with open(idx, "w", encoding="utf-8") as fh:
                        title = dirpath.name.replace("_", " ").replace("-", " ").title()
                        fh.write(f"# {title}\n\n")
                        fh.write(f"This page provides an overview of the **`{dirpath.name}`** directory.\n\n")

                        # Discover recursively
                        all_md_files = [p for p in dirpath.rglob("*.md") if p.name != "index.md"]
                        all_html_files = [p for p in dirpath.rglob("*.html") if p.name != "index.html"]
                        structure_files = [p for p in dirpath.rglob("fair-structure.json")]
                        other_data_files = [p for p in dirpath.rglob("*.json") if p.name != "fair-structure.json"]
                        graphics_files = [
                            p for p in dirpath.rglob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".svg")
                        ]

                        # --- Markdown/HTML Summary Files ---
                        if all_md_files or all_html_files:
                            fh.write("## Summary Pages\n\n")
                            fh.write("_Markdown or HTML pages found recursively._\n\n")
                            fh.write("| Path | Type | Size | Modified | Title |\n")
                            fh.write("|------|------|------|-----------|--------|\n")

                            for f in sorted(
                                all_md_files + all_html_files, key=lambda p: p.relative_to(dirpath).as_posix()
                            ):
                                rel = f.relative_to(dirpath).as_posix()
                                size = _hr_size(f.stat().st_size)
                                mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                                ftype = "Markdown" if f.suffix.lower() == ".md" else "HTML"
                                title = _extract_title(f)
                                fh.write(f"| `{rel}` | {ftype} | {size} | {mtime} | {title} |\n")
                            fh.write("\n")

                        # --- Structure Data Files ---
                        if structure_files:
                            fh.write("## Structure Data Files\n\n")
                            fh.write("_FAIR structure files (`fair-structure.json`) found recursively._\n\n")
                            fh.write("| Path | Type | Size | Modified |\n")
                            fh.write("|------|------|------|-----------|\n")
                            for sf in sorted(structure_files, key=lambda p: p.relative_to(dirpath).as_posix()):
                                rel = sf.relative_to(dirpath).as_posix()
                                size = _hr_size(sf.stat().st_size)
                                mtime = datetime.fromtimestamp(sf.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                                fh.write(f"| `{rel}` | Structure JSON | {size} | {mtime} |\n")
                            fh.write("\n")

                        # --- Other Data Files ---
                        if other_data_files:
                            fh.write("## Data Files\n\n")
                            fh.write("_Other JSON data files found recursively (excluding structure JSON)._  \n\n")
                            fh.write("| Path | Type | Size | Modified |\n")
                            fh.write("|------|------|------|-----------|\n")

                            for df in sorted(other_data_files, key=lambda p: p.relative_to(dirpath).as_posix()):
                                rel = df.relative_to(dirpath).as_posix()
                                size = _hr_size(df.stat().st_size)
                                mtime = datetime.fromtimestamp(df.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")

                                # Heuristic: infer type
                                name = df.name.lower()
                                if "vasprun" in name:
                                    ftype = "VASP Parsed JSON"
                                elif "summarized" in name:
                                    ftype = "Summary JSON"
                                elif "metadata" in name:
                                    ftype = "Metadata JSON"
                                else:
                                    ftype = "Generic JSON"

                                fh.write(f"| `{rel}` | {ftype} | {size} | {mtime} |\n")
                            fh.write("\n")

                        # --- Graphics / Visualization Files ---
                        if graphics_files:
                            fh.write("## Graphics Files\n\n")
                            fh.write("_Visualization and figure files found recursively._\n\n")
                            fh.write("| Path | Type | Size | Modified |\n")
                            fh.write("|------|------|------|-----------|\n")
                            for img in sorted(graphics_files, key=lambda p: p.relative_to(dirpath).as_posix()):
                                rel = img.relative_to(dirpath).as_posix()
                                size = _hr_size(img.stat().st_size)
                                mtime = datetime.fromtimestamp(img.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")

                                ext = img.suffix.lower().replace(".", "").upper()
                                ftype = f"{ext} Image"

                                fh.write(f"| `{rel}` | {ftype} | {size} | {mtime} |\n")
                            fh.write("\n")

                        if not (all_md_files or all_html_files or structure_files or other_data_files):
                            fh.write("_This folder currently has no recognized Markdown, HTML, or data files._\n\n")

                        fh.write("\n---\n")
                        fh.write("*(AI generated summary coming soon)*\n")

                except Exception:
                    log.debug(f"Could not create smart index.md for {dirpath}", exc_info=True)

            # Build nav entries: the first entry for a directory is an explicit
            # mapping label -> index page so MkDocs will use the provided label
            # rather than extracting the H1 from the page (which can be 'Home').
            entries = []
            if dirpath != temp_docs:
                # Use a neutral 'Overview' label so the sidebar shows a clear
                # label under the directory without duplicating the directory
                # name itself.
                entries.append({"Overview": idx.relative_to(temp_docs).as_posix()})

            for d in children:
                entries.append({d.name: build_nav_object_for_dir(d)})

            return entries

        # Pick a sensible top-level home file: prefer index.md, fall back to README.md
        if (temp_docs / "index.md").exists():
            home_entry = "index.md"
        elif (temp_docs / "README.md").exists():
            home_entry = "README.md"
        else:
            home_entry = "index.md"

        final_nav = [{"Home": home_entry}]
        docs_label = docs_path.name

        # Build docs nav object. We do NOT include individual file names in the
        # navigation; only folder names (which link to their index pages) and
        # single-file folders linking directly to the file.
        docs_nav_obj = []
        for d in sorted([d for d in temp_docs.iterdir() if d.is_dir() and has_markdown(d)]):
            if d.name in ("assets", "stylesheets", "js", "includes", "material"):
                continue
            docs_nav_obj.append({d.name: build_nav_object_for_dir(d)})

        final_nav.append({docs_label: docs_nav_obj})

        # Inject nav into packaged config safely
        try:
            import yaml

            try:
                cfg = yaml.safe_load(content)
            except Exception:
                cfg = None

            if cfg is not None:
                cfg["docs_dir"] = str(temp_docs)
                cfg["site_url"] = f"http://127.0.0.1:{int(port)}"
                cfg["use_directory_urls"] = False

                plugins = cfg.get("plugins")
                if isinstance(plugins, list):
                    new_plugins = []
                    for p in plugins:
                        if p == "include_dir_to_nav":
                            continue
                        if isinstance(p, dict) and "include_dir_to_nav" in p:
                            continue
                        new_plugins.append(p)
                    cfg["plugins"] = new_plugins

                    # Ensure theme custom_dir points to the material theme root
                    # (the packaged layout uses material/overrides as a subfolder
                    #  containing the Jinja2 overrides). MkDocs expects
                    #  custom_dir to point to the theme root directory; the
                    #  overrides are located under <custom_dir>/overrides.
                    theme = cfg.get("theme") or {}
                    if isinstance(theme, dict):
                        cd = theme.get("custom_dir")
                        if isinstance(cd, str) and cd.endswith("overrides"):
                            # move up one level so MkDocs sees custom_dir as 'material'
                            cfg["theme"]["custom_dir"] = cd.rsplit("/", 1)[0]

                    cfg["nav"] = final_nav
                content = yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True, width=10000)
            else:
                nav_yaml = yaml.dump(final_nav, allow_unicode=True, sort_keys=False, width=10000)
                lines = content.splitlines(True)
                nav_start = None
                for i, line in enumerate(lines):
                    if re.match(r"^\s*nav\s*:", line):
                        nav_start = i
                        break

                if nav_start is not None:
                    end = None
                    for j in range(nav_start + 1, len(lines)):
                        if re.match(r"^[^ \t].+?:", lines[j]):
                            end = j
                            break

                    new_nav_block = ["nav:\n", nav_yaml]
                    if end is None:
                        new_lines = lines[:nav_start] + new_nav_block
                    else:
                        new_lines = lines[:nav_start] + new_nav_block + lines[end:]
                    content = "".join(new_lines)
                else:
                    content = content + "\nnav:\n" + nav_yaml
                    # If the packaged config used a 'custom_dir' that pointed
                    # directly at an 'overrides' subfolder (e.g. 'material/overrides')
                    # many projects expect the theme root to be the parent
                    # directory. When we copy the entire `material` folder into
                    # the temp site, adjust the textual config so MkDocs will
                    # find the overrides under <custom_dir>/overrides.
                    try:
                        content = re.sub(r"(?m)^(\s*custom_dir\s*:\s*)(.+?/)?overrides\s*$", r"\1material", content)
                    except Exception:
                        pass
        except Exception:
            log.debug("Failed to auto-generate per-directory nav block; continuing without it.")

        # Final textual normalization: ensure custom_dir does not point
        # directly at an 'overrides' subfolder (e.g. 'material/overrides').
        # MkDocs expects custom_dir to be the theme root; the Jinja2
        # overrides live under <custom_dir>/overrides. Normalize to
        # 'material' so our copied theme folder is discovered.
        try:
            content = re.sub(r"(?m)^(\s*custom_dir\s*:\s*)(.+?/)?overrides\s*$", r"\1material", content)
        except Exception:
            pass

        temp_mkdocs.write_text(content, encoding="utf-8")

        # Copy macros.py next to temp mkdocs.yml if it exists in the packaged template
        if packaged_macros.is_file():
            try:
                (temp_dir / "macros.py").write_bytes(packaged_macros.read_bytes())
            except Exception:
                log.debug("Failed to copy macros.py to temporary dir", exc_info=True)
        else:
            log.debug("No packaged macros.py found; continuing without copying macros.")

        # Also copy the `material` theme folder that the config references
        # relatively (custom_dir and the hooks under `material/overrides`).
        packaged_material = template / "material"
        if packaged_material.is_dir():
            dst_material = temp_dir / "material"
            try:
                _copy_resource_tree(packaged_material, dst_material)
            except Exception:
                # Don't fail if copying fails; warn instead
                log.warning("Failed to copy packaged material overrides; theme customization may be missing.")

        # If build=True, run mkdocs build using the temporary mkdocs config.
        # The caller can optionally provide `build_dir` to control the
        # output location; by default the site is written under the temp dir
        # as '<temp_dir>/site'. We do not change cleanup semantics here: the
        # temporary directory is removed at the end of this function unless
        # `dry_run` is True.
        if build:
            # Resolve build target to an absolute path. If the caller provided
            # a relative path (e.g. 'site'), resolve it against the current
            # working directory so MkDocs doesn't treat it relative to the
            # temporary mkdocs.yml location and accidentally write into the
            # temp dir.
            if build_dir is not None:
                bd = Path(build_dir)
                if bd.is_absolute():
                    target = bd
                else:
                    target = Path.cwd() / bd
            else:
                target = temp_dir / "site"

            target = target.resolve()
            cmd = [sys.executable, "-m", "mkdocs", "build", "-f", str(temp_mkdocs), "-d", str(target)]
            log.info(f"Running mkdocs build -> {target}")
            try:
                proc = subprocess.run(cmd, check=False)
                if proc.returncode != 0:
                    log.error(f"mkdocs build exited with return code {proc.returncode}")
                    # Do not raise SystemExit here; allow caller to inspect temp dir
                else:
                    log.info(f"mkdocs build completed; site available at: {target}")
            except FileNotFoundError:
                log.error(
                    "`mkdocs` command not found. Is mkdocs installed in the active Python environment? Try `pip install mkdocs mkdocs-material mkdocs-macros-plugin`."
                )
            except Exception as e:
                log.error(f"Error running mkdocs build: {e}", exc_info=True)
            # If build was requested and this is not a dry_run, do not start
            # the interactive dev server afterwards. Return so callers (CI
            # scripts or users) can continue without hanging on a serve.
            if not dry_run:
                return

        # If dry_run is requested, return temp_dir so caller can inspect files
        if dry_run:
            log.info(f"Wrote temporary mkdocs config to: {temp_mkdocs}")
            log.info(f"Temporary docs tree at: {temp_docs}")
            return temp_dir

        # Build the mkdocs serve command
        cmd = [sys.executable, "-m", "mkdocs", "serve", "-f", str(temp_mkdocs), "--dev-addr", f"127.0.0.1:{int(port)}"]

        log.info(f"Starting mkdocs server on http://127.0.0.1:{port}")
        log.info(f"Using packaged mkdocs config from {packaged_mkdocs} with docs_dir={docs_path}")
        log.info("Press Ctrl+C to stop the server.")

        # Launch mkdocs serve. This will block until the server is stopped.
        try:
            process = subprocess.run(cmd, check=False)
            if process.returncode != 0:
                log.error(f"mkdocs exited with return code {process.returncode}")
                raise SystemExit(process.returncode)
        except FileNotFoundError:
            log.error(
                "`mkdocs` command not found. Is mkdocs installed in the active Python environment? Try `pip install mkdocs mkdocs-material mkdocs-macros-plugin`."
            )
            raise SystemExit(1)
        except KeyboardInterrupt:
            log.info("mkdocs server stopped by user.")
    finally:
        # Clean up the temporary directory unless dry_run requested
        try:
            if dry_run:
                log.info(f"dry_run requested; leaving temporary directory in place: {temp_dir}")
            else:
                shutil.rmtree(temp_dir)
        except Exception:
            pass
