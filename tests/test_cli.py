import pytest
from typer.testing import CliRunner
from pathlib import Path
from unittest.mock import patch, MagicMock
import typer

# Import the main Typer application from your cli.py
from fairtool.cli import app, _find_calc_files

# Initialize the CliRunner
runner = CliRunner()

# --- Fixtures for common test setup ---

@pytest.fixture
def mock_all_runners():
    """
    Mocks all the 'run_...' functions in the logic modules to test
    the CLI layer in isolation.
    """
    with patch('fairtool.cli.parse_module.run_parser') as mock_parse, \
         patch('fairtool.cli.analyze_module.run_analysis') as mock_analyze, \
         patch('fairtool.cli.summarize_module.run_summarization') as mock_summarize, \
         patch('fairtool.cli.export_module.run_export') as mock_export, \
         patch('fairtool.cli.visualize_module.run_visualization') as mock_visualize:
        
        # Make run_parser return False (not skipped)
        mock_parse.return_value = False 
        
        yield {
            "parse": mock_parse,
            "analyze": mock_analyze,
            "summarize": mock_summarize,
            "export": mock_export,
            "visualize": mock_visualize
        }

@pytest.fixture
def setup_test_files(tmp_path):
    """
    Create a standard file structure for testing file finding.
    
    Structure:
    tmp_path/
    ├── vasprun.xml
    ├── other.txt
    ├── fair_parsed_data.json
    ├── config.yml
    └── subdir/
        └── vasprun.xml
    """
    (tmp_path / "vasprun.xml").write_text("dummy vasp 1")
    (tmp_path / "subdir").mkdir(parents=True)
    (tmp_path / "subdir" / "vasprun.xml").write_text("dummy vasp 2")
    (tmp_path / "other.txt").write_text("not a calc file")
    (tmp_path / "fair_parsed_data.json").write_text("{}")
    (tmp_path / "config.yml").write_text("config: true")
    return tmp_path


# --- Existing Tests ---

def test_version_command():
    """
    Test the --version/-v flag.
    """
    result = runner.invoke(app, ["--version"], env={"TERM": "dumb"})
    assert result.exit_code == 0
    assert "FAIR Tool Version:" in result.stdout

    result = runner.invoke(app, ["-v"], env={"TERM": "dumb"})
    assert result.exit_code == 0
    assert "FAIR Tool Version:" in result.stdout


def test_author(capsys):
    """
    Test if the author information is displayed correctly in 'about'.
    """
    result = runner.invoke(app, ["about"], env={"TERM": "dumb"})
    assert result.exit_code == 0
    print ("whole stdout", result.stdout)  # For debugging purposes
    assert "Dr. Ravindra Shinde" in result.stdout

    result = runner.invoke(app, ["about"], env={"TERM": "dumb"})
    assert result.exit_code == 0
    assert "r.l.shinde@utwente.nl" in result.stdout


def test_no_command_shows_help():
    """
    Test that invoking with no command shows the help message
    (due to no_args_is_help=True).
    """
    result = runner.invoke(app, env={"TERM": "dumb"})
    assert result.exit_code == 0
    assert "Usage: fair [OPTIONS] COMMAND [ARGS]..." in result.stdout
    assert "Commands" in result.stdout


# --- [NEW] Unit Tests for _find_calc_files Helper ---

def test_find_calc_files_non_recursive(setup_test_files):
    """Test finding files only in the root directory."""
    files = _find_calc_files(setup_test_files, recursive=False, assume_yes=True)
    assert len(files) == 1
    assert files[0].name == "vasprun.xml"
    assert files[0].parent.name == setup_test_files.name

def test_find_calc_files_recursive(setup_test_files):
    """Test finding files recursively."""
    files = _find_calc_files(setup_test_files, recursive=True, assume_yes=True)
    assert len(files) == 2
    # Check that we found both vasprun.xml files
    assert {f.parent.name for f in files} == {setup_test_files.name, "subdir"}

def test_find_calc_files_on_file_input(setup_test_files):
    """Test giving a direct file path instead of a directory."""
    file_path = setup_test_files / "vasprun.xml"
    files = _find_calc_files(file_path, recursive=False, assume_yes=True)
    assert len(files) == 1
    assert files[0] == file_path

def test_find_calc_files_no_files_found(setup_test_files):
    """Test searching a directory that contains no matching files."""
    (setup_test_files / "empty_dir").mkdir()
    files = _find_calc_files(setup_test_files / "empty_dir", recursive=True, assume_yes=True)
    assert len(files) == 0

def test_find_calc_files_non_existent_path():
    """Test that a non-existent path raises a typer.Exit."""
    with pytest.raises(typer.Exit):
        _find_calc_files(Path("non_existent_path_12345"), recursive=True, assume_yes=True)


# --- [NEW] CLI Integration Tests ---

def test_cli_parse_command_options(mock_all_runners, setup_test_files):
    """
    Test the `parse` command's options: -r, -f, -y, -o.
    This test checks that the CLI layer correctly interprets these
    options and passes them to the backend parser.
    """
    test_dir = setup_test_files
    out_dir = setup_test_files / "output"
    
    result = runner.invoke(app, [
        "parse",
        str(test_dir),
        "--recursive",
        "--force",
        "--yes",
        "--output", str(out_dir)
    ])
    
    assert result.exit_code == 0
    
    # Check that parse_module.run_parser was called correctly
    mock_parse = mock_all_runners["parse"]
    
    # It should be called 2 times (once for each file found)
    assert mock_parse.call_count == 2
    
    # Check the call args.
    # call_args_list[0][0] is the (args,) tuple of the first call.
    # The args are (file_path, output_dir_path, force_flag)
    expected_calls = [
        (test_dir / "vasprun.xml", out_dir, True),
        (test_dir / "subdir" / "vasprun.xml", out_dir, True)
    ]
    
    # Convert mock calls to a simpler, comparable format
    actual_calls = [
        (call[0][0], call[0][1], call[0][2]) for call in mock_parse.call_args_list
    ]
    
    # Use sets to be order-agnostic
    assert set(actual_calls) == set(expected_calls)


def test_cli_analyze_command(mock_all_runners, setup_test_files):
    """
    Test the `analyze` command and its options.
    """
    json_file = setup_test_files / "fair_parsed_data.json"
    out_dir = setup_test_files / "analysis_out"
    config_file = setup_test_files / "config.yml"

    result = runner.invoke(app, [
        "analyze",
        str(json_file),
        "--output", str(out_dir),
        "--config", str(config_file)
    ])
    
    assert result.exit_code == 0
    mock_analyze = mock_all_runners["analyze"]
    
    # Check that analyze_module.run_analysis was called with correct args
    mock_analyze.assert_called_once_with(
        json_file, # Typer resolves this path
        out_dir,
        config_file
    )

def test_cli_all_command(mock_all_runners, setup_test_files):
    """
    Test the `all` command to ensure it orchestrates the
    full workflow and passes options correctly.
    """
    test_dir = setup_test_files
    out_dir = setup_test_files / "all_output"
    
    # We mock the file-finding helpers to isolate the logic
    # of the 'all' command itself.
    with patch('fairtool.cli._find_calc_files') as mock_find_calc, \
         patch('fairtool.cli._find_json_files') as mock_find_json:
        
        # Setup mock return values
        dummy_calc_file = setup_test_files / "vasprun.xml"
        dummy_json_file = out_dir / "fair_parsed_vasprun.json"
        mock_find_calc.return_value = [dummy_calc_file]
        mock_find_json.return_value = [dummy_json_file]
        
        result = runner.invoke(app, [
            "all",
            str(test_dir),
            "-r", "-f", "-y",
            "-o", str(out_dir),
            "--format", "csv",
            "--embed"
        ])
        
        assert result.exit_code == 0
        
        # Check that the 'all' command called all the backend
        # modules in the correct order with the correct arguments.
        
        # 1. Parse
        mock_find_calc.assert_called_once_with(test_dir, recursive=True, assume_yes=True)
        mock_all_runners["parse"].assert_called_once_with(dummy_calc_file, out_dir, True)
        
        # 2. Analyze
        mock_all_runners["analyze"].assert_called_once_with(out_dir, out_dir, None)
        
        # 3. Summarize
        mock_find_json.assert_called_once_with(out_dir, recursive=True)
        mock_all_runners["summarize"].assert_called_once_with(dummy_json_file, out_dir, None)

        # 4. Export
        mock_all_runners["export"].assert_called_once_with(out_dir, out_dir, "csv")

        # 5. Visualize
        mock_all_runners["visualize"].assert_called_once_with(out_dir, out_dir, True)
