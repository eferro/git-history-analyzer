import datetime
import json
import subprocess
import sys
from typing import List, Dict


def run(cmd, cwd=None, capture_output=False, check=True):
    return subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.PIPE if capture_output else None,
        check=check,
        text=True,
    )


def get_commit_date(repo_dir, args):
    out = run(["git", "log"] + args, cwd=repo_dir, capture_output=True)
    lines = out.stdout.strip().splitlines()
    return lines[0] if lines else None


def list_month_starts(start: datetime.date, end: datetime.date) -> List[datetime.date]:
    dates = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        dates.append(datetime.date(y, m, 1))
        if m == 12:
            y += 1
            m = 1
        else:
            m += 1
    return dates


def list_week_starts(start: datetime.date, end: datetime.date) -> List[datetime.date]:
    # start from the Monday of the first week
    cur = start - datetime.timedelta(days=start.weekday())
    dates = []
    while cur <= end:
        dates.append(cur)
        cur += datetime.timedelta(days=7)
    return dates


def list_day_starts(start: datetime.date, end: datetime.date) -> List[datetime.date]:
    cur = start
    dates = []
    while cur <= end:
        dates.append(cur)
        cur += datetime.timedelta(days=1)
    return dates


def list_period_starts(start: datetime.date, end: datetime.date, period: str) -> List[datetime.date]:
    if period == "daily":
        return list_day_starts(start, end)
    if period == "weekly":
        return list_week_starts(start, end)
    return list_month_starts(start, end)


def collect_metrics(repo_dir: str, dates: List[datetime.date], branch_ref: str, debug: bool) -> Dict[str, Dict[str, Dict[str, int]]]:
    results = {}
    for dt in dates:
        ds = dt.strftime("%Y-%m-%d")
        commit = run([
            "git",
            "rev-list",
            "-1",
            "--before",
            f"{ds} 23:59:59",
            branch_ref,
        ], cwd=repo_dir, capture_output=True).stdout.strip()
        if not commit:
            continue
        run(["git", "checkout", commit], cwd=repo_dir)
        if debug:
            print(f"=== {ds} commit {commit} ===", file=sys.stderr)
        out = run(["scc", "-f", "json"], cwd=repo_dir, capture_output=True)
        if debug:
            print(out.stdout, file=sys.stderr)
        try:
            stats = json.loads(out.stdout)
        except json.JSONDecodeError:
            print(f"Error parsing scc JSON at {ds}", file=sys.stderr)
            continue
        per_lang = {}
        for ent in stats:
            name = ent.get("Name") or ent.get("language") or ent.get("Language") or ent.get("name")
            lines = ent.get("Code") or ent.get("code") or ent.get("Lines") or ent.get("lines")
            complexity = ent.get("Complexity") or ent.get("complexity")
            if not name:
                continue
            per_lang[name] = {"lines": lines, "complexity": complexity}
        results[ds] = per_lang
    return results
