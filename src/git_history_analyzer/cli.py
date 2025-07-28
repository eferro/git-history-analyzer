import argparse
import datetime
import json
import shutil
import sys
import tempfile
import subprocess
from .collector import (
    run,
    get_commit_date,
    list_period_starts,
    collect_metrics,
)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Sample a git repo and collect scc metrics",
    )
    p.add_argument("repo_url", help="URL of the git repository")
    p.add_argument(
        "--branch",
        default="HEAD",
        help="Branch or ref to sample (default HEAD)",
    )
    p.add_argument(
        "--dates",
        nargs="+",
        metavar="YYYY-MM-DD",
        help="Specific dates to sample instead of entire history",
    )
    p.add_argument(
        "--period",
        choices=["daily", "weekly", "monthly"],
        default="monthly",
        help="Sampling period if --dates not provided",
    )
    p.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output of commits and raw scc JSON",
    )
    p.add_argument(
        "--csv",
        action="store_true",
        help="Output results in CSV wide format",
    )
    args = p.parse_args(argv)

    tmp = tempfile.mkdtemp(prefix="scc_metrics_")
    try:
        try:
            run(["scc", "--version"], capture_output=True)
        except Exception:
            print("Error: 'scc' command not found or failed", file=sys.stderr)
            return 1

        print(f"Cloning {args.repo_url} into {tmp}...", file=sys.stderr)
        try:
            run(["git", "clone", args.repo_url, tmp], capture_output=True)
        except subprocess.CalledProcessError as e:  # type: ignore[name-defined]
            print(f"Error cloning repository: {e.stderr}", file=sys.stderr)
            return 1

        if args.branch and args.branch != "HEAD":
            print(f"Checking out branch {args.branch}...", file=sys.stderr)
            try:
                run(["git", "checkout", args.branch], cwd=tmp, capture_output=True)
            except subprocess.CalledProcessError as e:  # type: ignore[name-defined]
                print(f"Error checking out branch {args.branch}: {e.stderr}", file=sys.stderr)
                return 1

        branch_ref = args.branch
        if args.branch == "HEAD":
            try:
                out = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=tmp, capture_output=True)
                branch_ref = out.stdout.strip()
            except subprocess.CalledProcessError as e:  # type: ignore[name-defined]
                print(f"Error resolving HEAD branch: {e.stderr}", file=sys.stderr)
                return 1

        first = get_commit_date(
            tmp,
            args=["--reverse", "--format=%cd", "--date=format:%Y-%m-%d", branch_ref],
        )
        last = get_commit_date(
            tmp,
            args=["-1", "--format=%cd", "--date=format:%Y-%m-%d", branch_ref],
        )
        if not first or not last:
            print(f"Could not determine commit dates: first={first}, last={last}", file=sys.stderr)
            return 1

        print(f"Sampling from {first} to {last} on {branch_ref}", file=sys.stderr)
        if args.dates:
            dates = []
            for ds in args.dates:
                try:
                    dates.append(datetime.datetime.strptime(ds, "%Y-%m-%d").date())
                except ValueError:
                    print(f"Invalid date format: {ds}", file=sys.stderr)
                    return 1
        else:
            d0 = datetime.datetime.strptime(first, "%Y-%m-%d").date()
            d1 = datetime.datetime.strptime(last, "%Y-%m-%d").date()
            dates = list_period_starts(d0, d1, args.period)

        results = collect_metrics(tmp, dates, branch_ref, args.debug)

        if args.csv:
            import csv

            langs = set()
            for per in results.values():
                langs.update(per.keys())
            langs = sorted(langs)
            header = ["date"]
            for lang in langs:
                header.append(f"{lang}_lines")
                header.append(f"{lang}_complexity")
            writer = csv.writer(sys.stdout)
            writer.writerow(header)
            for ds in sorted(results.keys()):
                row = [ds]
                per = results.get(ds, {})
                for lang in langs:
                    vals = per.get(lang, {})
                    row.append(vals.get("lines", ""))
                    row.append(vals.get("complexity", ""))
                writer.writerow(row)
        else:
            json.dump(results, sys.stdout, indent=2)
            sys.stdout.write("\n")
        return 0
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    raise SystemExit(main())
