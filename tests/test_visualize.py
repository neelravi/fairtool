import json
import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from fairtool.visualize import (
    _copy_resource_tree,
    _extract_title,
    _hr_size,
    _site_template,
    generate_markdown_embedding,
    get_band_structure_data,
    get_dos_data,
    get_structure_data,
    run_visualization,
    serve_docs,
)


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


def test_get_structure_data_valid():
    """Test extracting valid structure data from lattice, species, and coordinates."""
    data = {
        "results": {
            "properties": {
                "structure": {
                    "lattice_vectors": [[5.43, 0, 0], [0, 5.43, 0], [0, 0, 5.43]],
                    "species_at_sites": ["Si", "Si"],
                    "cartesian_site_positions": [[0.0, 0.0, 0.0], [1.35, 1.35, 1.35]],
                }
            }
        }
    }
    struct = get_structure_data(data)
    assert struct is not None
    assert "@class" in struct or "lattice" in struct or "sites" in struct


def test_get_structure_data_none():
    """Test structure data extraction returns None when missing."""
    assert get_structure_data({}) is None
    assert get_structure_data({"results": {}}) is None


def test_get_band_structure_data():
    """Test extracting band structure data."""
    data_with_bs = {
        "results": {"properties": {"electronic": {"band_structure": {"pymatgen_bandstructure": {"bands": [1, 2, 3]}}}}}
    }
    assert get_band_structure_data(data_with_bs) == {"bands": [1, 2, 3]}
    assert get_band_structure_data({}) is None


def test_get_dos_data():
    """Test extracting DOS data."""
    data_with_dos = {"results": {"properties": {"electronic": {"dos": {"pymatgen_dos": {"energies": [0.1, 0.2]}}}}}}
    assert get_dos_data(data_with_dos) == {"energies": [0.1, 0.2]}
    assert get_dos_data({}) is None


def test_generate_markdown_embedding():
    """Test generating React visualization Markdown embedding snippets."""
    snippet = generate_markdown_embedding(Path("output/calc_structure.json"), "structure", "viz-calc-1")
    assert 'id="viz-calc-1"' in snippet
    assert 'data-viz-type="structure"' in snippet
    assert 'data-src="calc_structure.json"' in snippet


def test_run_visualization_single_file(tmp_path):
    """Test run_visualization on a single parsed JSON file."""
    parsed_content = {
        "results": {
            "properties": {
                "structure": {
                    "lattice_vectors": [[3.0, 0, 0], [0, 3.0, 0], [0, 0, 3.0]],
                    "species_at_sites": ["Fe"],
                    "cartesian_site_positions": [[0.0, 0.0, 0.0]],
                },
                "electronic": {
                    "band_structure": {"pymatgen_bandstructure": {"dummy": "bands"}},
                    "dos": {"pymatgen_dos": {"dummy": "dos"}},
                },
            }
        }
    }
    json_file = tmp_path / "sample_parsed.json"
    json_file.write_text(json.dumps(parsed_content), encoding="utf-8")
    out_dir = tmp_path / "viz_out"
    out_dir.mkdir()

    run_visualization(json_file, out_dir, embed=True)

    assert (out_dir / "sample_structure.json").exists()
    assert (out_dir / "sample_bands.json").exists()
    assert (out_dir / "sample_dos.json").exists()
    assert (out_dir / "visualization_embeds.md").exists()


def test_run_visualization_empty_dir(tmp_path):
    """Test run_visualization with no parsed files found."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    out_dir = tmp_path / "viz_out"
    out_dir.mkdir()

    run_visualization(empty_dir, out_dir, embed=False)
    assert len(list(out_dir.iterdir())) == 0


def test_run_visualization_invalid_input(tmp_path):
    """Test run_visualization with non-JSON file."""
    txt_file = tmp_path / "bad.txt"
    txt_file.write_text("hello", encoding="utf-8")
    out_dir = tmp_path / "viz_out"
    out_dir.mkdir()

    run_visualization(txt_file, out_dir, embed=False)
    assert len(list(out_dir.iterdir())) == 0


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


def test_get_structure_data_branches(monkeypatch):
    """Test get_structure_data with pymatgen_structure, missing Structure, incomplete, and exception."""
    import fairtool.visualize as viz

    # Case 1: Structure is None
    monkeypatch.setattr(viz, "Structure", None)
    assert viz.get_structure_data({}) is None

    # Case 2: Pymatgen Structure available with pymatgen_structure dict
    from pymatgen.core import Structure

    monkeypatch.setattr(viz, "Structure", Structure)

    pmg_dict = {
        "@module": "pymatgen.core.structure",
        "@class": "Structure",
        "charge": 0,
        "lattice": {
            "matrix": [[3.0, 0, 0], [0, 3.0, 0], [0, 0, 3.0]],
            "a": 3.0,
            "b": 3.0,
            "c": 3.0,
            "alpha": 90.0,
            "beta": 90.0,
            "gamma": 90.0,
            "volume": 27.0,
        },
        "sites": [
            {
                "species": [{"element": "Fe", "occu": 1}],
                "abc": [0.0, 0.0, 0.0],
                "xyz": [0.0, 0.0, 0.0],
                "label": "Fe",
            }
        ],
    }
    data_with_pmg = {"results": {"properties": {"structure": {"pymatgen_structure": pmg_dict}}}}
    struct_out = viz.get_structure_data(data_with_pmg)
    assert struct_out is not None

    # Case 3: Incomplete data (missing coords/species)
    incomplete_data = {"results": {"properties": {"structure": {"lattice_vectors": [[1, 0, 0]]}}}}
    assert viz.get_structure_data(incomplete_data) is None

    # Case 4: Exception in processing
    error_data = {"results": {"properties": {"structure": {"pymatgen_structure": "bad-type"}}}}
    assert viz.get_structure_data(error_data) is None


def test_get_band_and_dos_exception(monkeypatch):
    """Test get_band_structure_data and get_dos_data exception handling."""
    from unittest.mock import MagicMock

    mock_bad_dict = MagicMock()
    mock_bad_dict.get.side_effect = RuntimeError("Bad structure")

    assert get_band_structure_data(mock_bad_dict) is None
    assert get_dos_data(mock_bad_dict) is None


def test_run_visualization_corrupted_json_and_exception(tmp_path):
    """Test run_visualization handles corrupted JSON and file exceptions."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # Corrupted JSON
    bad_json = tmp_path / "calc_parsed.json"
    bad_json.write_text("{ unclosed", encoding="utf-8")
    run_visualization(bad_json, out_dir, embed=False)

    # File that causes an exception
    good_json = tmp_path / "calc2_parsed.json"
    good_json.write_text(json.dumps({"results": {}}), encoding="utf-8")

    with patch("fairtool.visualize.get_structure_data", side_effect=RuntimeError("Failure")):
        run_visualization(good_json, out_dir, embed=False)


def test_run_visualization_embed_save_failure(tmp_path, monkeypatch):
    """Test run_visualization handles failure when saving visualization_embeds.md."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    json_file = tmp_path / "calc_parsed.json"
    json_file.write_text(
        json.dumps(
            {
                "results": {
                    "properties": {
                        "structure": {
                            "lattice_vectors": [[3.0, 0, 0], [0, 3.0, 0], [0, 0, 3.0]],
                            "species_at_sites": ["Fe"],
                            "cartesian_site_positions": [[0.0, 0.0, 0.0]],
                        }
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    orig_open = open

    def mock_open(path, mode="r", *args, **kwargs):
        if "visualization_embeds.md" in str(path) and "w" in mode:
            raise OSError("Write error on embeds")
        return orig_open(path, mode, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)
    # Should not raise exception
    run_visualization(json_file, out_dir, embed=True)


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
    (sub / "vasprun_parsed.json").write_text("{}", encoding="utf-8")
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
