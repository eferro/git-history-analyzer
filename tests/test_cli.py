import datetime
from types import SimpleNamespace
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from git_history_analyzer import cli


def test_main_generates_csv_output(monkeypatch, tmp_path, capsys):
    tmp_repo = tmp_path / "repo"
    tmp_repo.mkdir()

    def fake_mkdtemp(*, prefix="tmp", suffix=None, dir=None):
        return str(tmp_repo)

    removed = []

    def fake_rmtree(path):
        removed.append(path)

    def fake_run(cmd, cwd=None, capture_output=False, check=True):
        if cmd == ["scc", "--version"]:
            return SimpleNamespace(stdout="scc 1.0\n", stderr="")
        if cmd[:2] == ["git", "clone"]:
            assert cmd[2] == "https://example.com/repo.git"
            assert cmd[3] == str(tmp_repo)
            return SimpleNamespace(stdout="", stderr="")
        if cmd[:4] == ["git", "rev-parse", "--abbrev-ref", "HEAD"]:
            assert cwd == str(tmp_repo)
            return SimpleNamespace(stdout="main\n", stderr="")
        raise AssertionError(f"unexpected command {cmd}")

    commit_dates = iter(["2024-01-01", "2024-02-15"])

    def fake_get_commit_date(repo_dir, args):
        return next(commit_dates)

    def fake_collect_metrics(repo_dir, dates, branch_ref, debug):
        assert repo_dir == str(tmp_repo)
        assert branch_ref == "main"
        assert dates == [
            datetime.date(2024, 1, 1),
            datetime.date(2024, 2, 1),
        ]
        assert debug is False
        return {
            "2024-01-01": {"Python": {"lines": 10, "complexity": 3}},
            "2024-02-01": {"Rust": {"lines": 5, "complexity": 1}},
        }

    monkeypatch.setattr(cli.tempfile, "mkdtemp", fake_mkdtemp)
    monkeypatch.setattr(cli.shutil, "rmtree", fake_rmtree)
    monkeypatch.setattr(cli, "run", fake_run)
    monkeypatch.setattr(cli, "get_commit_date", fake_get_commit_date)
    monkeypatch.setattr(cli, "collect_metrics", fake_collect_metrics)

    exit_code = cli.main(
        [
            "https://example.com/repo.git",
            "--dates",
            "2024-01-01",
            "2024-02-01",
            "--csv",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.splitlines() == [
        "date,Python_lines,Python_complexity,Rust_lines,Rust_complexity",
        "2024-01-01,10,3,,",
        "2024-02-01,,,5,1",
    ]
    assert "Cloning https://example.com/repo.git into" in captured.err
    assert "Sampling from 2024-01-01 to 2024-02-15 on main" in captured.err
    assert removed == [str(tmp_repo)]


def test_main_reports_error_when_scc_missing(monkeypatch, tmp_path, capsys):
    tmp_repo = tmp_path / "repo"
    tmp_repo.mkdir()

    def fake_mkdtemp(*, prefix="tmp", suffix=None, dir=None):
        return str(tmp_repo)

    removed = []

    def fake_rmtree(path):
        removed.append(path)

    def fake_run(cmd, cwd=None, capture_output=False, check=True):
        raise FileNotFoundError("scc not found")

    monkeypatch.setattr(cli.tempfile, "mkdtemp", fake_mkdtemp)
    monkeypatch.setattr(cli.shutil, "rmtree", fake_rmtree)
    monkeypatch.setattr(cli, "run", fake_run)

    exit_code = cli.main(["https://example.com/repo.git"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: 'scc' command not found or failed" in captured.err
    assert captured.out == ""
    assert removed == [str(tmp_repo)]
