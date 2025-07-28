import datetime
from types import SimpleNamespace
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from git_history_analyzer import collector


def test_collect_metrics_parses_json(tmp_path, monkeypatch):
    def fake_run(cmd, cwd=None, capture_output=False, check=True):
        if cmd[:2] == ["git", "rev-list"]:
            return SimpleNamespace(stdout="deadbeef\n")
        if cmd[:2] == ["git", "checkout"]:
            return SimpleNamespace(stdout="")
        if cmd[0] == "scc":
            data = "[{\"Name\": \"Python\", \"Lines\": 10, \"Complexity\": 2}]"
            return SimpleNamespace(stdout=data)
        raise AssertionError(f"unexpected command {cmd}")

    monkeypatch.setattr(collector, "run", fake_run)
    dates = [datetime.date(2024, 1, 1)]
    results = collector.collect_metrics(str(tmp_path), dates, "main", False)
    assert results == {
        "2024-01-01": {"Python": {"lines": 10, "complexity": 2}}
    }


def test_list_week_starts_aligns_to_monday():
    start = datetime.date(2024, 1, 3)  # Wednesday
    end = datetime.date(2024, 1, 20)
    weeks = collector.list_week_starts(start, end)
    assert weeks[0] == datetime.date(2024, 1, 1)
    assert weeks[0].weekday() == 0
    assert weeks[-1] == datetime.date(2024, 1, 15)
