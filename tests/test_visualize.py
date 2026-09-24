import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from fairtool.visualize import _copy_resource_tree, _extract_title, _hr_size, _site_template, serve_docs


@pytest.fixture
def fake_template(tmp_path, monkeypatch):
    """Point serve_docs at an empty site template that the test populates."""
    template = tmp_path / "template"
    template.mkdir()
    monkeypatch.setattr("fairtool.visualize._site_template", lambda: template)
    return template


def test_hr_size():
    """Test human readable file size conversion."""
    assert _hr_size(500) == "500.0 B"
    assert _hr_size(1024) == "1.0 KB"
    assert _hr_size(1024 * 1024) == "1.0 MB"
    assert _hr_size(1024 * 1024 * 1024) == "1.0 GB"


def test_extract_title_markdown(tmp_path):
    """Test extracting H1 title from a Markdown file."""
    md_file = tmp_path / "test.md"
    md_file.write_text("# Welcome to FAIRTool\nSome content here.\n", encoding="utf-8")
    assert _extract_title(md_file) == "Welcome to FAIRTool"


def test_extract_title_html(tmp_path):
    """Test extracting title from an HTML file."""
    html_file = tmp_path / "test.html"
    html_file.write_text("<html><head><title>My Calculation</title></head></html>", encoding="utf-8")
    assert _extract_title(html_file) == "My Calculation"


def test_extract_title_missing_file(tmp_path):
    """Test fallback when title cannot be extracted."""
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("", encoding="utf-8")
    assert _extract_title(empty_file) == "—"


def test_site_template_ships_files_referenced_by_mkdocs_yml():
    """Every local file the packaged mkdocs.yml points at is shipped in the site template."""

    class TagTolerantLoader(yaml.SafeLoader):
        """SafeLoader that ignores the !ENV and !!python/* tags used in mkdocs.yml."""

    TagTolerantLoader.add_multi_constructor("", lambda loader, suffix, node: None)

    template = _site_template()
    cfg = yaml.load(template.joinpath("mkdocs.yml").read_text(encoding="utf-8"), Loader=TagTolerantLoader)
    docs = template / "docs"
    # `nav` is not checked: serve_docs always replaces it with one generated from the user's docs

    # Resolved against docs_dir
    for ref in [*cfg["extra_css"], *cfg["extra_javascript"], cfg["theme"]["favicon"], cfg["theme"]["logo"]]:
        assert docs.joinpath(ref).is_file(), ref
    # Resolved against the directory holding mkdocs.yml
    for hook in cfg["hooks"]:
        assert template.joinpath(hook).is_file(), hook
    assert template.joinpath(cfg["theme"]["custom_dir"]).is_dir()
    macros = next(p["macros"] for p in cfg["plugins"] if isinstance(p, dict) and "macros" in p)
    assert template.joinpath(f"{macros['module_name']}.py").is_file()
    # Homepage copied into the generated site
    assert docs.joinpath("README.md").is_file()


def test_copy_resource_tree_skips_pycache(tmp_path):
    """Packaged resource trees are copied recursively, without bytecode caches."""
    src = tmp_path / "src"
    (src / "hooks" / "__pycache__").mkdir(parents=True)
    (src / "hooks" / "shortcodes.py").write_text("x = 1\n", encoding="utf-8")
    (src / "hooks" / "__pycache__" / "shortcodes.cpython-311.pyc").write_bytes(b"\x00")
    (src / "main.html").write_text("<html></html>", encoding="utf-8")

    dest = tmp_path / "dest"
    _copy_resource_tree(src, dest)

    assert (dest / "main.html").read_text(encoding="utf-8") == "<html></html>"
    assert (dest / "hooks" / "shortcodes.py").read_text(encoding="utf-8") == "x = 1\n"
    assert not (dest / "hooks" / "__pycache__").exists()


def test_serve_docs_dry_run(tmp_path):
    """Test serve_docs with dry_run=True creates and normalizes temporary mkdocs configuration."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Test Docs\nHello world.", encoding="utf-8")

    temp_dir = serve_docs(docs_dir, port=9999, dry_run=True)
    assert temp_dir is not None
    assert Path(temp_dir).exists()
    assert (Path(temp_dir) / "mkdocs.yml").exists()

    # The files the generated config relies on are copied out of the packaged template
    assert (Path(temp_dir) / "macros.py").is_file()
    assert (Path(temp_dir) / "material" / "overrides" / "hooks" / "shortcodes.py").is_file()
    for asset in ("js/3Dmol-min.js", "js/structure.js", "stylesheets/extra.css", "assets/logo.png"):
        assert (Path(temp_dir) / "docs" / asset).is_file(), asset
    assert "custom_dir: material\n" in (Path(temp_dir) / "mkdocs.yml").read_text(encoding="utf-8")

    # Clean up temp dir
    import shutil

    shutil.rmtree(temp_dir, ignore_errors=True)


def test_serve_docs_dry_run_with_nested_dirs(tmp_path):
    """Test serve_docs handles nested directories, nav generation, and summaries in dry_run mode."""
    docs_dir = tmp_path / "docs_complex"
    docs_dir.mkdir()
    (docs_dir / "README.md").write_text("# Complex Project\nOverview", encoding="utf-8")

    sub1 = docs_dir / "sub1"
    sub1.mkdir()
    (sub1 / "page1.md").write_text("# Page 1\nDetails", encoding="utf-8")

    sub2 = docs_dir / "sub2"
    sub2.mkdir()
    (sub2 / "page2a.md").write_text("# Page 2A\nDetails", encoding="utf-8")
    (sub2 / "page2b.md").write_text("# Page 2B\nDetails", encoding="utf-8")

    temp_dir = serve_docs(docs_dir, port=9998, dry_run=True)
    assert temp_dir is not None
    assert (Path(temp_dir) / "mkdocs.yml").exists()

    import shutil

    shutil.rmtree(temp_dir, ignore_errors=True)


def test_serve_docs_nonexistent_path():
    """Test serve_docs with non-existent directory raises SystemExit."""
    with pytest.raises(SystemExit):
        serve_docs(Path("non_existent_folder_98765"), port=8000)


def test_hr_size_tb_pb():
    """Test human readable file size conversion for TB and PB."""
    tb = 1024 * 1024 * 1024 * 1024
    assert "TB" in _hr_size(tb * 2)
    pb = tb * 1024
    assert "PB" in _hr_size(pb * 2)


def test_extract_title_read_error(monkeypatch):
    """Test _extract_title gracefully returns fallback on read error."""

    def mock_open(*args, **kwargs):
        raise OSError("Read failed")

    monkeypatch.setattr("builtins.open", mock_open)
    assert _extract_title(Path("some_file.md")) == "—"


def test_serve_docs_missing_packaged_mkdocs(tmp_path, fake_template, caplog):
    """Test serve_docs raises SystemExit if packaged mkdocs.yml is missing."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    with pytest.raises(SystemExit) as excinfo:
        serve_docs(docs_dir)

    assert excinfo.value.code == 1
    assert "Packaged mkdocs.yml not found" in caplog.text


def test_serve_docs_smart_index_generation(tmp_path):
    """Test serve_docs generating smart index.md covering summary, structure, data, and graphics files."""
    docs_dir = tmp_path / "docs_rich"
    docs_dir.mkdir()

    # Subdirectory with multiple files to trigger smart index table generation
    sub = docs_dir / "calculation_folder"
    sub.mkdir()

    # Summary pages
    (sub / "report1.md").write_text("# Report 1\nSome markdown", encoding="utf-8")
    (sub / "report2.md").write_text("# Report 2\nSome markdown", encoding="utf-8")
    (sub / "page.html").write_text("<title>HTML Page</title>", encoding="utf-8")

    # Structure data files
    (sub / "fair-structure.json").write_text("{}", encoding="utf-8")

    # Other data files with heuristic categories
    (sub / "fair_parsed_vasprun.json").write_text("{}", encoding="utf-8")
    (sub / "fair_summarized_calc.json").write_text("{}", encoding="utf-8")
    (sub / "calc_metadata.json").write_text("{}", encoding="utf-8")
    (sub / "other_generic.json").write_text("{}", encoding="utf-8")

    # Graphics files
    (sub / "plot.png").write_bytes(b"dummy png")
    (sub / "diagram.svg").write_text("<svg></svg>", encoding="utf-8")

    # Empty subfolder
    (docs_dir / "empty_folder").mkdir()
    (docs_dir / "empty_folder" / "dummy.md").write_text("# Empty Folder", encoding="utf-8")
    (docs_dir / "empty_folder" / "dummy2.md").write_text("# Empty Folder 2", encoding="utf-8")

    temp_dir = serve_docs(docs_dir, port=9997, dry_run=True)
    assert temp_dir is not None

    generated_index = Path(temp_dir) / "docs" / "calculation_folder" / "index.md"
    assert generated_index.exists()
    content = generated_index.read_text(encoding="utf-8")
    assert "Summary Pages" in content
    assert "Structure Data Files" in content
    assert "Data Files" in content
    assert "Graphics Files" in content
    assert "VASP Parsed JSON" in content
    assert "Summary JSON" in content
    assert "Metadata JSON" in content
    assert "PNG Image" in content

    import shutil

    shutil.rmtree(temp_dir, ignore_errors=True)


def test_serve_docs_build_modes(tmp_path):
    """Test serve_docs with build=True, relative and absolute build_dir, success and failure."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Docs Home", encoding="utf-8")

    # Case 1: Successful build with custom relative build_dir
    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        serve_docs(docs_dir, build=True, build_dir=Path("custom_site"), dry_run=False)
        assert mock_run.called
        cmd = mock_run.call_args[0][0]
        assert "build" in cmd

    # Case 2: Build with absolute build_dir
    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        abs_site = tmp_path / "abs_site"
        serve_docs(docs_dir, build=True, build_dir=abs_site, dry_run=False)

    # Case 3: Build failure (non-zero exit code) exits with mkdocs' return code
    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.returncode = 3
        mock_run.return_value = mock_proc

        with pytest.raises(SystemExit) as excinfo:
            serve_docs(docs_dir, build=True, dry_run=False)
        assert excinfo.value.code == 3
        # The temporary directory holding the generated mkdocs.yml is still removed
        cmd = mock_run.call_args[0][0]
        assert not Path(cmd[cmd.index("-f") + 1]).parent.exists()

    # Case 4: FileNotFoundError for mkdocs
    with patch("subprocess.run", side_effect=FileNotFoundError("mkdocs missing")):
        with pytest.raises(SystemExit) as excinfo:
            serve_docs(docs_dir, build=True, dry_run=False)
        assert excinfo.value.code == 1

    # Case 5: General exception during build
    with patch("subprocess.run", side_effect=RuntimeError("Build crashed")):
        with pytest.raises(SystemExit) as excinfo:
            serve_docs(docs_dir, build=True, dry_run=False)
        assert excinfo.value.code == 1


def test_serve_docs_serve_interactive(tmp_path):
    """Test serve_docs launching server, handling returncode != 0, FileNotFoundError, and KeyboardInterrupt."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Docs Home", encoding="utf-8")

    # Non-zero exit code
    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_run.return_value = mock_proc
        with pytest.raises(SystemExit):
            serve_docs(docs_dir, port=8001, dry_run=False)

    # FileNotFoundError
    with patch("subprocess.run", side_effect=FileNotFoundError("mkdocs not installed")):
        with pytest.raises(SystemExit):
            serve_docs(docs_dir, port=8001, dry_run=False)

    # KeyboardInterrupt
    with patch("subprocess.run", side_effect=KeyboardInterrupt):
        serve_docs(docs_dir, port=8001, dry_run=False)


def test_serve_docs_generated_index_tree(tmp_path, fake_template):
    """Test auto-generating index.md with directory tree when no homepage exists."""
    docs_dir = tmp_path / "docs_tree"
    docs_dir.mkdir()
    sub = docs_dir / "subfolder"
    sub.mkdir()
    (sub / "nested.md").write_text("# Nested Page", encoding="utf-8")

    # A template without a packaged homepage, so the generated index runs
    (fake_template / "mkdocs.yml").write_text("site_name: Tree Docs\n", encoding="utf-8")

    temp_dir = serve_docs(docs_dir, port=9996, dry_run=True)
    assert temp_dir is not None
    generated_index = Path(temp_dir) / "docs" / "index.md"
    assert generated_index.exists()
    content = generated_index.read_text(encoding="utf-8")
    assert "FAIR Tool - Local Preview" in content
    assert "Pages and Folders (tree)" in content
    assert "subfolder" in content

    import shutil

    shutil.rmtree(temp_dir, ignore_errors=True)


def test_serve_docs_clean_yaml_config(tmp_path, fake_template, monkeypatch, caplog):
    """Test serve_docs when packaged mkdocs.yml is valid standard YAML with plugins and overrides."""
    docs_dir = tmp_path / "docs_clean"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Clean Docs", encoding="utf-8")

    (fake_template / "mkdocs.yml").write_text(
        """
site_name: Clean Docs
site_url: https://localhost/fairtool
theme:
  name: material
  custom_dir: material/overrides
plugins:
  - search
  - include_dir_to_nav
  - include_dir_to_nav:
      some: option
""",
        encoding="utf-8",
    )

    # Also test that the template has no macros.py and that copying the material folder fails
    (fake_template / "material" / "overrides").mkdir(parents=True)
    monkeypatch.setattr(
        "fairtool.visualize._copy_resource_tree", MagicMock(side_effect=OSError("Copy material failed"))
    )

    temp_dir = serve_docs(docs_dir, port=9995, dry_run=True)
    assert temp_dir is not None
    temp_yaml = Path(temp_dir) / "mkdocs.yml"
    assert temp_yaml.exists()
    content = temp_yaml.read_text(encoding="utf-8")
    assert "include_dir_to_nav" not in content
    assert yaml.safe_load(content)["theme"]["custom_dir"] == "material"
    assert not (Path(temp_dir) / "macros.py").exists()
    assert "Failed to copy packaged material overrides" in caplog.text

    import shutil

    shutil.rmtree(temp_dir, ignore_errors=True)


def test_serve_docs_plugin_importable(tmp_path, fake_template, monkeypatch, caplog):
    """Test serve_docs when include_dir_to_nav is importable in the environment."""
    docs_dir = tmp_path / "docs_importable"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Importable Docs", encoding="utf-8")

    (fake_template / "mkdocs.yml").write_text(
        """
site_name: Importable Docs
site_url: https://localhost/fairtool
plugins:
  - include_dir_to_nav
""",
        encoding="utf-8",
    )

    import importlib

    caplog.set_level(logging.INFO, logger="fairtool")
    real_import_module = importlib.import_module
    monkeypatch.setattr(
        importlib,
        "import_module",
        lambda name, *args: MagicMock() if name == "include_dir_to_nav" else real_import_module(name, *args),
    )

    temp_dir = serve_docs(docs_dir, port=9993, dry_run=True)
    assert temp_dir is not None
    assert "'include_dir_to_nav' plugin is available" in caplog.text
    import shutil

    shutil.rmtree(temp_dir, ignore_errors=True)


def test_serve_docs_no_nav_fallback(tmp_path, fake_template, monkeypatch):
    """Test serve_docs nav injection fallback when content has no nav entry."""
    docs_dir = tmp_path / "docs_nonav"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# No Nav Docs", encoding="utf-8")

    (fake_template / "mkdocs.yml").write_text(
        """
site_name: No Nav Docs
site_url: https://localhost/fairtool
custom_dir: material/overrides
""",
        encoding="utf-8",
    )

    # Force yaml.safe_load to fail so it takes fallback textual branch
    monkeypatch.setattr(yaml, "safe_load", MagicMock(side_effect=Exception("YAML load fail")))

    temp_dir = serve_docs(docs_dir, port=9994, dry_run=True)
    assert temp_dir is not None
    temp_yaml = Path(temp_dir) / "mkdocs.yml"
    assert temp_yaml.exists()
    content = temp_yaml.read_text(encoding="utf-8")
    assert "nav:" in content
    assert "custom_dir: material\n" in content

    import shutil

    shutil.rmtree(temp_dir, ignore_errors=True)


def test_serve_docs_build_with_packaged_template(tmp_path):
    """A real mkdocs build with the packaged template renders pages, macros and static assets."""
    docs_dir = tmp_path / "calcs"
    (docs_dir / "example01").mkdir(parents=True)
    (docs_dir / "example01" / "summary.md").write_text(
        "# Example 01\n\n{{ structure_viewer('fair-structure.json') }}\n", encoding="utf-8"
    )
    site_dir = tmp_path / "site"

    serve_docs(docs_dir, build=True, build_dir=site_dir)

    assert (site_dir / "index.html").is_file()
    for asset in ("js/3Dmol-min.js", "js/structure.js", "stylesheets/extra.css", "assets/logo.png"):
        assert (site_dir / asset).is_file(), asset
    # structure_viewer comes from the packaged macros.py
    assert 'class="structure-viewer"' in (site_dir / "example01" / "summary.html").read_text(encoding="utf-8")
