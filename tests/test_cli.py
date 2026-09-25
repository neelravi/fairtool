import json
import shutil
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest
import typer
from typer.testing import CliRunner

# Import the main Typer application from your cli.py
from fairtool.cli import _find_calc_files, app

# Initialize the CliRunner
runner = CliRunner()

# --- Fixtures for common test setup ---


@pytest.fixture
def mock_all_runners():
    """
    Mocks all the 'run_...' functions in the logic modules to test
    the CLI layer in isolation.
    """
    with (
        patch("fairtool.cli.parse_module.run_parser") as mock_parse,
        patch("fairtool.cli.analyze_module.run_analysis") as mock_analyze,
        patch("fairtool.cli.summarize_module.run_summarization") as mock_summarize,
        patch("fairtool.cli.export_module.run_export") as mock_export,
    ):
        # Make run_parser return False (not skipped)
        mock_parse.return_value = False
        # Make run_export return True (something was exported)
        mock_export.return_value = True

        yield {
            "parse": mock_parse,
            "analyze": mock_analyze,
            "summarize": mock_summarize,
            "export": mock_export,
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


@pytest.fixture
def nomad_failures(monkeypatch):
    """
    Fakes `nomad parse`. For the files added to the returned set it fails, as it does when the
    system libmagic library is missing; for the others it returns a minimal archive.
    """
    failing_files = set()

    def fake_nomad(command, **kwargs):
        if Path(command[-1]) in failing_files:
            raise subprocess.CalledProcessError(1, command, stderr="ImportError: failed to find libmagic")
        return subprocess.CompletedProcess(command, 0, stdout='{"metadata": {}}', stderr="")

    monkeypatch.setattr("subprocess.run", fake_nomad)
    return failing_files


@pytest.fixture
def analyzed_calc_dir(tmp_path):
    """A calc/ directory holding the analysis_summary.csv that `fair analyze calc` writes."""
    calc_dir = tmp_path / "calc"
    calc_dir.mkdir()
    (calc_dir / "analysis_summary.csv").write_text("identifier,total_energy_eV\ncalc_01,-120.5\n", encoding="utf-8")
    return calc_dir


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
    print("whole stdout", result.stdout)  # For debugging purposes
    assert "Dr. Ravindra Shinde" in result.stdout

    result = runner.invoke(app, ["about"], env={"TERM": "dumb"})
    assert result.exit_code == 0
    assert "r.l.shinde@utwente.nl" in result.stdout


# def test_no_command_shows_help():
#     """
#     Test that invoking with no command shows the help message
#     (due to no_args_is_help=True).
#     """
#     result = runner.invoke(app, env={"TERM": "dumb"})
#     assert result.exit_code == 0
#     assert "Usage: fair [OPTIONS] COMMAND [ARGS]..." in result.stdout
#     assert "Commands" in result.stdout


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

    result = runner.invoke(app, ["parse", str(test_dir), "--recursive", "--force", "--yes", "--output", str(out_dir)])

    assert result.exit_code == 0

    # Check that parse_module.run_parser was called correctly
    mock_parse = mock_all_runners["parse"]

    # It should be called 2 times (once for each file found)
    assert mock_parse.call_count == 2

    # Check the call args.
    # call_args_list[0][0] is the (args,) tuple of the first call.
    # The args are (file_path, output_dir_path, force_flag)
    # Each file's outputs keep its subdirectory, so the two vasprun.xml don't collide
    expected_calls = [
        (test_dir / "vasprun.xml", out_dir, True),
        (test_dir / "subdir" / "vasprun.xml", out_dir / "subdir", True),
    ]

    # Convert mock calls to a simpler, comparable format
    actual_calls = [(call[0][0], call[0][1], call[0][2]) for call in mock_parse.call_args_list]

    # Use sets to be order-agnostic
    assert set(actual_calls) == set(expected_calls)


def test_cli_analyze_command(mock_all_runners, setup_test_files):
    """
    Test the `analyze` command and its options.
    """
    json_file = setup_test_files / "fair_parsed_data.json"
    out_dir = setup_test_files / "analysis_out"
    config_file = setup_test_files / "config.yml"

    result = runner.invoke(app, ["analyze", str(json_file), "--output", str(out_dir), "--config", str(config_file)])

    assert result.exit_code == 0
    mock_analyze = mock_all_runners["analyze"]

    # Check that analyze_module.run_analysis was called with correct args
    mock_analyze.assert_called_once_with(
        json_file,  # Typer resolves this path
        out_dir,
        config_file,
    )


def test_cli_analyze_output_defaults_to_input_location(mock_all_runners, setup_test_files):
    """Without --output, analyze saves into the input directory, or next to a single input file."""
    json_file = setup_test_files / "fair_parsed_data.json"

    assert runner.invoke(app, ["analyze", str(setup_test_files)]).exit_code == 0
    assert runner.invoke(app, ["analyze", str(json_file)]).exit_code == 0

    assert mock_all_runners["analyze"].call_args_list == [
        call(setup_test_files, setup_test_files, None),
        call(json_file, setup_test_files, None),
    ]


def test_cli_analyze_then_export_calculations_with_the_same_file_name(tmp_path):
    """
    Regression: analyzing a tree of calculations gives each one its own identifier, even when
    their parsed files share a name, so `fair export --format json_summary` keeps them all
    instead of failing on a duplicate identifier.
    """
    calc_dir = tmp_path / "calcs"
    for example in ["Advanced/example04", "Expert/example08"]:
        (calc_dir / example).mkdir(parents=True)
        # What `fair parse calcs -r` leaves next to each calcs/<example>/vasprun.xml
        shutil.copy(Path(__file__).parent / "VASP" / example / "fair_parsed_vasprun.json", calc_dir / example)
    analysis_dir = tmp_path / "analysis"

    res_analyze = runner.invoke(app, ["analyze", str(calc_dir), "--output", str(analysis_dir)])
    assert res_analyze.exit_code == 0

    res_export = runner.invoke(
        app, ["export", str(analysis_dir), "--output", str(tmp_path), "--format", "json_summary"]
    )
    assert res_export.exit_code == 0
    summary = json.loads((tmp_path / "exported_summary.json").read_text(encoding="utf-8"))
    assert sorted(summary) == ["Advanced/example04/fair_parsed_vasprun", "Expert/example08/fair_parsed_vasprun"]


def test_cli_analyze_then_export_without_analyze_output(tmp_path, monkeypatch):
    """
    Regression: `fair analyze calc` followed by `fair export calc` exports the analysis.
    Without --output, analyze must save analysis_summary.csv in calc/, where export looks for it,
    rather than in the current directory.
    """
    calc_dir = tmp_path / "calc"
    calc_dir.mkdir()
    # What `fair parse calc` leaves next to calc/dos_si_vasprun.xml
    parsed_json = Path(__file__).parent / "VASP" / "Basic" / "example03" / "fair_parsed_dos_si_vasprun.json"
    shutil.copy(parsed_json, calc_dir)
    export_dir = tmp_path / "exported"
    # Run from calc's parent, like a user typing `fair analyze calc && fair export calc`
    monkeypatch.chdir(tmp_path)

    res_analyze = runner.invoke(app, ["analyze", "calc"])
    assert res_analyze.exit_code == 0
    assert (calc_dir / "analysis_summary.csv").is_file()

    res_export = runner.invoke(app, ["export", "calc", "--output", str(export_dir)])
    assert res_export.exit_code == 0
    exported_csv = export_dir / "exported_data.csv"
    assert exported_csv.is_file()
    assert "fair_parsed_dos_si_vasprun" in exported_csv.read_text(encoding="utf-8")


def test_cli_all_command(mock_all_runners, setup_test_files, caplog):
    """
    Test the `all` command to ensure it orchestrates the
    full workflow and passes options correctly.
    """
    import logging

    caplog.set_level(logging.WARNING)
    test_dir = setup_test_files
    out_dir = setup_test_files / "all_output"

    # We mock the file-finding helpers to isolate the logic
    # of the 'all' command itself.
    with (
        patch("fairtool.cli._find_calc_files") as mock_find_calc,
        patch("fairtool.cli._find_json_files") as mock_find_json,
    ):
        # Setup mock return values
        dummy_calc_file = setup_test_files / "vasprun.xml"
        dummy_json_file = out_dir / "fair_parsed_vasprun.json"
        mock_find_calc.return_value = [dummy_calc_file]
        mock_find_json.return_value = [dummy_json_file]

        result = runner.invoke(
            app, ["all", str(test_dir), "-r", "-f", "-y", "-o", str(out_dir), "--format", "csv", "--embed"]
        )

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

        # The deprecated --embed flag is still accepted, but only warns
        assert "--embed is deprecated" in caplog.text


def test_cli_summarize_command(mock_all_runners, setup_test_files):
    """Test the `summarize` command invoking summarize_module.run_summarization."""
    json_file = setup_test_files / "fair_parsed_data.json"
    out_dir = setup_test_files / "sum_out"

    result = runner.invoke(app, ["summarize", str(json_file), "--output", str(out_dir), "--force"])
    assert result.exit_code == 0
    mock_summarize = mock_all_runners["summarize"]
    mock_summarize.assert_called_once_with(json_file, out_dir, None)


def test_cli_export_command(mock_all_runners, setup_test_files):
    """Test the `export` command with custom format and output directory."""
    input_file = setup_test_files / "fair_parsed_data.json"
    out_dir = setup_test_files / "export_out"

    result = runner.invoke(app, ["export", str(input_file), "--output", str(out_dir), "--format", "yaml"])
    assert result.exit_code == 0
    mock_export = mock_all_runners["export"]
    mock_export.assert_called_once_with(input_file, out_dir, "yaml")


def test_cli_visualize_command(setup_test_files, monkeypatch, caplog):
    """Test that `visualize` still accepts the deprecated --output/--embed flags, warns, and writes nothing."""
    import logging

    import fairtool.cli as fair_cli

    caplog.set_level(logging.WARNING)
    mock_serve_docs = MagicMock()
    monkeypatch.setattr(fair_cli.visualize_module, "serve_docs", mock_serve_docs)
    out_dir = setup_test_files / "viz_out"

    result = runner.invoke(app, ["visualize", str(setup_test_files), "--output", str(out_dir), "--embed", "--no-serve"])
    assert result.exit_code == 0
    assert "--output is deprecated" in caplog.text
    assert "--embed is deprecated" in caplog.text
    assert "Nothing to do" in caplog.text
    assert not out_dir.exists()
    mock_serve_docs.assert_not_called()


def test_cli_help():
    """Test the top-level --help output."""
    result = runner.invoke(app, ["--help"], env={"TERM": "dumb"})
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
    assert "parse" in result.stdout
    assert "summarize" in result.stdout
    assert "analyze" in result.stdout
    assert "export" in result.stdout
    assert "visualize" in result.stdout


def test_cli_invalid_command():
    """Test invoking a non-existent command exits with code 2."""
    result = runner.invoke(app, ["nonexistent_command"], env={"TERM": "dumb"})
    assert result.exit_code != 0


def test_cli_analyze_error_handling(mock_all_runners, setup_test_files):
    """Test analyze command catches backend exceptions and exits with code 1."""
    mock_all_runners["analyze"].side_effect = RuntimeError("Analysis error")
    json_file = setup_test_files / "fair_parsed_data.json"

    result = runner.invoke(app, ["analyze", str(json_file)])
    assert result.exit_code == 1


def test_cli_export_exits_zero_when_exported(analyzed_calc_dir, tmp_path):
    """The real export writes exported_data.csv and exits 0."""
    export_dir = tmp_path / "exported"

    result = runner.invoke(app, ["export", str(analyzed_calc_dir), "--output", str(export_dir)])
    assert result.exit_code == 0
    assert "calc_01" in (export_dir / "exported_data.csv").read_text(encoding="utf-8")


def test_cli_export_no_data_exits_nonzero(tmp_path, caplog):
    """
    Regression: `fair export calc` exits 1 when calc/ has no analysis_summary.csv,
    so that `fair export calc && upload exported_data.csv` stops instead of uploading nothing.
    """
    import logging

    caplog.set_level(logging.INFO)
    calc_dir = tmp_path / "calc"
    calc_dir.mkdir()
    export_dir = tmp_path / "exported"

    result = runner.invoke(app, ["export", str(calc_dir), "--output", str(export_dir)])
    assert result.exit_code == 1
    assert not any(export_dir.iterdir())
    assert "Could not find or load suitable data to export" in caplog.text
    assert "Export finished." not in caplog.text


def test_cli_export_unsupported_format_exits_nonzero(analyzed_calc_dir, tmp_path, caplog):
    """`fair export calc -fmt xml` exits 1 without writing anything."""
    export_dir = tmp_path / "exported"

    result = runner.invoke(app, ["export", str(analyzed_calc_dir), "--output", str(export_dir), "-fmt", "xml"])
    assert result.exit_code == 1
    assert not any(export_dir.iterdir())
    assert "Unsupported export format: 'xml'" in caplog.text


def test_cli_export_error_handling(mock_all_runners, setup_test_files):
    """Test export command catches backend exceptions and exits with code 1."""
    mock_all_runners["export"].side_effect = RuntimeError("Export error")
    json_file = setup_test_files / "fair_parsed_data.json"

    result = runner.invoke(app, ["export", str(json_file)])
    assert result.exit_code == 1


def test_find_calc_files_interactive_abort_single_file(tmp_path, monkeypatch):
    """Test _find_calc_files interactive abortion when user says no for single file."""
    calc_file = tmp_path / "vasprun.xml"
    calc_file.write_text("content", encoding="utf-8")

    import sys

    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(typer, "confirm", lambda prompt: False)

    with pytest.raises(typer.Exit) as exc:
        _find_calc_files(calc_file, assume_yes=False)
    assert exc.value.exit_code == 0


def test_find_calc_files_interactive_abort_dir(tmp_path, monkeypatch):
    """Test _find_calc_files interactive abortion when user says no for directory."""
    calc_file = tmp_path / "vasprun.xml"
    calc_file.write_text("content", encoding="utf-8")

    import sys

    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(typer, "confirm", lambda prompt: False)

    with pytest.raises(typer.Exit) as exc:
        _find_calc_files(tmp_path, assume_yes=False)
    assert exc.value.exit_code == 0


def test_find_calc_files_non_interactive_dir(tmp_path, monkeypatch, caplog):
    """Test _find_calc_files non-interactive environment branch for directory."""
    import logging

    caplog.set_level(logging.INFO)
    calc_file = tmp_path / "vasprun.xml"
    calc_file.write_text("content", encoding="utf-8")

    import sys

    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)

    files = _find_calc_files(tmp_path, assume_yes=False)
    assert len(files) == 1
    assert "Non-interactive environment detected" in caplog.text


def test_find_calc_files_neither_file_nor_dir(tmp_path, monkeypatch):
    """Test _find_calc_files error when path is neither file nor directory."""
    test_path = tmp_path / "special"
    test_path.touch()

    monkeypatch.setattr(Path, "is_file", lambda self: False)
    monkeypatch.setattr(Path, "is_dir", lambda self: False)

    with pytest.raises(typer.Exit) as exc:
        _find_calc_files(test_path, assume_yes=True)
    assert exc.value.exit_code == 1


def test_find_json_files_edge_cases(tmp_path):
    """Test _find_json_files non-existent, non-matching file, and empty dir."""
    from fairtool.cli import _find_json_files

    # Non-existent
    with pytest.raises(typer.Exit):
        _find_json_files(Path("non_existent_path_999"))

    # Non-matching file
    other_file = tmp_path / "other.json"
    other_file.write_text("{}", encoding="utf-8")
    assert _find_json_files(other_file) == []

    # Empty directory
    empty_dir = tmp_path / "empty_dir"
    empty_dir.mkdir()
    assert _find_json_files(empty_dir) == []


def test_cli_parse_no_files_and_failure(mock_all_runners, tmp_path, caplog):
    """Test parse command when no files found or run_parser raises error."""
    import logging

    caplog.set_level(logging.INFO)
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    # No files found
    res = runner.invoke(app, ["parse", str(empty_dir), "--yes"])
    assert res.exit_code == 0

    # Parse failure
    calc_file = tmp_path / "vasprun.xml"
    calc_file.write_text("dummy", encoding="utf-8")
    mock_all_runners["parse"].side_effect = RuntimeError("Parser crashed")

    res2 = runner.invoke(app, ["parse", str(calc_file), "--yes"])
    assert res2.exit_code == 1
    assert "Failed:  1" in caplog.text


@pytest.mark.parametrize(
    ("unchanged", "failing", "exit_code", "counts"),
    [
        # nomad cannot run, e.g. without libmagic
        ([], ["vasprun.xml", "subdir/vasprun.xml"], 1, (0, 0, 2)),
        ([], ["subdir/vasprun.xml"], 1, (1, 0, 1)),
        # A file unchanged since its last parse is skipped, which is not a failure
        (["vasprun.xml"], [], 0, (1, 1, 0)),
    ],
    ids=["all-fail", "partly-fail", "no-fail"],
)
def test_cli_parse_exits_nonzero_when_a_file_fails(
    setup_test_files, nomad_failures, caplog, unchanged, failing, exit_code, counts
):
    """
    Regression: `fair parse` exited 0 even when nomad could not parse any file, so scripts and CI
    could not tell that the run failed. It still reports the counts, then exits 1 if any file failed.
    """
    caplog.set_level("INFO", logger="fairtool")
    for name in unchanged:
        assert runner.invoke(app, ["parse", str(setup_test_files / name), "-y"]).exit_code == 0
    caplog.clear()
    nomad_failures.update(setup_test_files / name for name in failing)

    result = runner.invoke(app, ["parse", str(setup_test_files), "-r", "-y"])

    assert result.exit_code == exit_code
    success, skipped, failed = counts
    assert [record.getMessage() for record in caplog.records[-4:]] == [
        "--- Parsing Finished ---",
        f"[green]Success: {success}[/green]",
        f"[yellow]Skipped: {skipped}[/yellow]",
        f"[red]Failed:  {failed}[/red]",
    ]


def test_cli_summarize_options_and_skip(mock_all_runners, setup_test_files, caplog):
    """Test summarize command template, skip existing, and failure."""
    import logging

    caplog.set_level(logging.INFO)
    json_file = setup_test_files / "fair_parsed_data.json"

    # Template option
    res = runner.invoke(app, ["summarize", str(json_file), "--template", "mytemplate.j2", "--force"])
    assert res.exit_code == 0

    # Output already exists and not force -> skip
    existing_md = setup_test_files / "fair_summarized_data.md"
    existing_md.write_text("existing", encoding="utf-8")
    res_skip = runner.invoke(app, ["summarize", str(json_file)])
    assert res_skip.exit_code == 0
    assert "Skipped: 1" in caplog.text

    # Summarize raises exception
    mock_all_runners["summarize"].side_effect = RuntimeError("Summarize failed")
    res_err = runner.invoke(app, ["summarize", str(json_file), "--force"])
    assert res_err.exit_code == 1
    assert "Failed:  1" in caplog.text


def test_cli_summarize_no_json_files(tmp_path, caplog):
    """Test summarize command when no JSON files are found."""
    import logging

    caplog.set_level(logging.WARNING)
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    res = runner.invoke(app, ["summarize", str(empty_dir)])
    assert res.exit_code == 0
    assert "No 'fair_parsed_*.json' files found" in caplog.text


@pytest.mark.parametrize(
    ("existing_summaries", "failing", "exit_code", "counts"),
    [
        ([], ["fair_parsed_data.json", "subdir/fair_parsed_data.json"], 1, (0, 0, 2)),
        ([], ["subdir/fair_parsed_data.json"], 1, (1, 0, 1)),
        # A file whose summary already exists is skipped, which is not a failure
        (["fair_summarized_data.md"], [], 0, (1, 1, 0)),
    ],
    ids=["all-fail", "partly-fail", "no-fail"],
)
def test_cli_summarize_exits_nonzero_when_a_file_fails(
    mock_all_runners, setup_test_files, caplog, existing_summaries, failing, exit_code, counts
):
    """
    Regression: `fair summarize` exited 0 even when files failed to summarize.
    It still reports the counts, then exits 1 if any file failed.
    """
    caplog.set_level("INFO", logger="fairtool")
    (setup_test_files / "subdir" / "fair_parsed_data.json").write_text("{}", encoding="utf-8")
    for name in existing_summaries:
        (setup_test_files / name).write_text("existing", encoding="utf-8")
    failing_files = {setup_test_files / name for name in failing}

    def fake_summarization(json_file, output_dir, template):
        if json_file in failing_files:
            raise RuntimeError("Summarize failed")

    mock_all_runners["summarize"].side_effect = fake_summarization

    result = runner.invoke(app, ["summarize", str(setup_test_files)])

    assert result.exit_code == exit_code
    success, skipped, failed = counts
    assert [record.getMessage() for record in caplog.records[-4:]] == [
        "--- Summarization Finished ---",
        f"[green]Success: {success}[/green]",
        f"[yellow]Skipped: {skipped}[/yellow]",
        f"[red]Failed:  {failed}[/red]",
    ]


def test_cli_visualize_build_and_serve_modes(setup_test_files, monkeypatch):
    """Test visualize command with --build and --serve."""
    import fairtool.cli as fair_cli

    mock_serve_docs = MagicMock()
    monkeypatch.setattr(fair_cli.visualize_module, "serve_docs", mock_serve_docs)

    # Build mode
    res_build = runner.invoke(app, ["visualize", str(setup_test_files), "--build"])
    assert res_build.exit_code == 0
    assert mock_serve_docs.called

    # Build mode failure
    mock_serve_docs.side_effect = RuntimeError("Build failure")
    res_build_err = runner.invoke(app, ["visualize", str(setup_test_files), "--build"])
    assert res_build_err.exit_code == 1

    # Serve mode
    mock_serve_docs.side_effect = None
    mock_serve_docs.reset_mock()
    res_serve = runner.invoke(app, ["visualize", str(setup_test_files), "--serve"])
    assert res_serve.exit_code == 0
    assert mock_serve_docs.called

    # Serve mode failure
    mock_serve_docs.side_effect = RuntimeError("Server failure")
    res_serve_err = runner.invoke(app, ["visualize", str(setup_test_files), "--serve"])
    assert res_serve_err.exit_code == 1


def test_cli_visualize_build_failure_exits_nonzero(tmp_path, monkeypatch, caplog):
    """A failed mkdocs build makes `visualize --build` exit non-zero instead of reporting success."""
    docs_dir = tmp_path / "calcs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Calculations", encoding="utf-8")
    # --build writes the site to ./site
    monkeypatch.chdir(tmp_path)
    caplog.set_level("INFO", logger="fairtool")

    # serve_docs runs for real; only the mkdocs subprocess is mocked, and it fails
    with patch("subprocess.run", return_value=MagicMock(returncode=3)):
        result = runner.invoke(app, ["visualize", str(docs_dir), "--build"])

    assert result.exit_code == 3
    assert "Build finished" not in caplog.text


def test_cli_all_command_workflow_and_errors(setup_test_files, mock_all_runners, tmp_path):
    """Test all command happy path and all error conditions."""
    out_dir = tmp_path / "all_out"
    out_dir.mkdir()

    # 1. No files found to parse
    empty_dir = tmp_path / "empty_dir_all"
    empty_dir.mkdir()
    res = runner.invoke(app, ["all", str(empty_dir), "--output", str(out_dir), "--yes"])
    assert res.exit_code == 0

    # 2. All files fail to parse (parse_success == 0)
    mock_all_runners["parse"].side_effect = RuntimeError("Parse failed")
    res_fail = runner.invoke(app, ["all", str(setup_test_files / "vasprun.xml"), "--output", str(out_dir), "--yes"])
    assert res_fail.exit_code == 1

    # Reset parse
    mock_all_runners["parse"].side_effect = None

    # 3. Analyze step fails
    mock_all_runners["analyze"].side_effect = RuntimeError("Analyze failed")
    res_ana_err = runner.invoke(app, ["all", str(setup_test_files / "vasprun.xml"), "--output", str(out_dir), "--yes"])
    assert res_ana_err.exit_code == 1
    mock_all_runners["analyze"].side_effect = None

    # 4. Summarize step outer error
    with patch("fairtool.cli._find_json_files", side_effect=RuntimeError("Find json error")):
        res_sum_err = runner.invoke(
            app, ["all", str(setup_test_files / "vasprun.xml"), "--output", str(out_dir), "--yes"]
        )
        assert res_sum_err.exit_code == 1

    # 5. Export step fails
    mock_all_runners["export"].side_effect = RuntimeError("Export error")
    res_exp_err = runner.invoke(app, ["all", str(setup_test_files / "vasprun.xml"), "--output", str(out_dir), "--yes"])
    assert res_exp_err.exit_code == 1
    mock_all_runners["export"].side_effect = None

    # 6. Happy path full workflow
    (out_dir / "fair_parsed_test.json").write_text("{}", encoding="utf-8")
    res_happy = runner.invoke(app, ["all", str(setup_test_files / "vasprun.xml"), "--output", str(out_dir), "--yes"])
    assert res_happy.exit_code == 0


def test_cli_all_aborts_when_nothing_exported(setup_test_files, mock_all_runners, tmp_path, caplog):
    """`fair all` exits 1 and stops at the export step when it exports nothing (e.g., -fmt xml)."""
    import logging

    caplog.set_level(logging.INFO)
    out_dir = tmp_path / "all_out"
    mock_all_runners["export"].return_value = False

    res = runner.invoke(
        app, ["all", str(setup_test_files / "vasprun.xml"), "--output", str(out_dir), "--yes", "-fmt", "xml"]
    )
    assert res.exit_code == 1
    mock_all_runners["export"].assert_called_once_with(out_dir, out_dir, "xml")
    # No later step runs, and the workflow doesn't report success
    assert caplog.records[-1].getMessage() == "Nothing was exported. Aborting workflow."
