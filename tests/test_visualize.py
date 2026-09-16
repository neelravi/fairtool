import json
from pathlib import Path

import pytest

from fairtool.visualize import (
    _extract_title,
    _hr_size,
    generate_markdown_embedding,
    get_band_structure_data,
    get_dos_data,
    get_structure_data,
    run_visualization,
    serve_docs,
)


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


def test_serve_docs_dry_run(tmp_path):
    """Test serve_docs with dry_run=True creates and normalizes temporary mkdocs configuration."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Test Docs\nHello world.", encoding="utf-8")

    temp_dir = serve_docs(docs_dir, port=9999, dry_run=True)
    assert temp_dir is not None
    assert Path(temp_dir).exists()
    assert (Path(temp_dir) / "mkdocs.yml").exists()

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
