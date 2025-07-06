#!/usr/bin/env python3
"""
Clone a git repository, sample its codebase on the first of each month,
run 'scc -f json' at each point, and accumulate per-language LOC and complexity.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile


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
    # args: git log parameters to fetch date, e.g.
    # ['--reverse', '--format=%cd', '--date=format:%Y-%m-%d', 'branch']
    out = run(['git', 'log'] + args, cwd=repo_dir, capture_output=True)
    lines = out.stdout.strip().splitlines()
    return lines[0] if lines else None


def list_month_starts(start_date, end_date):
    # inclusive on both ends
    dates = []
    y, m = start_date.year, start_date.month
    while (y, m) <= (end_date.year, end_date.month):
        dates.append(datetime.date(y, m, 1))
        # increment month
        if m == 12:
            y += 1
            m = 1
        else:
            m += 1
    return dates


def main():
    p = argparse.ArgumentParser(
        description="Sample a git repo each month and collect scc metrics"
    )
    p.add_argument('repo_url', help='URL of the git repository')
    p.add_argument('--branch', default='HEAD', help='Branch or ref to sample (default HEAD)')
    p.add_argument('--dates', nargs='+', metavar='YYYY-MM-DD',
                   help='Specific dates to sample instead of entire history')
    p.add_argument('--debug', action='store_true',
                   help='Enable debug output of commits and raw scc JSON')
    p.add_argument('--csv', action='store_true',
                   help='Output results in CSV wide format (one column per language metrics)')
    args = p.parse_args()

    tmp = tempfile.mkdtemp(prefix='scc_monthly_')
    try:
        # Ensure scc is available
        try:
            run(['scc', '--version'], capture_output=True)
        except Exception:
            print("Error: 'scc' command not found or failed", file=sys.stderr)
            sys.exit(1)
        # Clone repository
        print(f"Cloning {args.repo_url} into {tmp}...", file=sys.stderr)
        try:
            run(['git', 'clone', args.repo_url, tmp], capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e.stderr}", file=sys.stderr)
            sys.exit(1)
        # Checkout branch if specified
        if args.branch and args.branch != 'HEAD':
            print(f"Checking out branch {args.branch}...", file=sys.stderr)
            try:
                run(['git', 'checkout', args.branch], cwd=tmp, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"Error checking out branch {args.branch}: {e.stderr}", file=sys.stderr)
                sys.exit(1)
        # Determine the branch name (resolve HEAD if needed)
        branch_ref = args.branch
        if args.branch == 'HEAD':
            try:
                out = run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=tmp, capture_output=True)
                branch_ref = out.stdout.strip()
            except subprocess.CalledProcessError as e:
                print(f"Error resolving HEAD branch: {e.stderr}", file=sys.stderr)
                sys.exit(1)
        # Determine first and last commit dates on branch_ref
        first = get_commit_date(
            tmp,
            args=['--reverse', '--format=%cd', '--date=format:%Y-%m-%d', branch_ref]
        )
        last = get_commit_date(
            tmp,
            args=['-1', '--format=%cd', '--date=format:%Y-%m-%d', branch_ref]
        )
        if not first or not last:
            print(f"Could not determine commit dates: first={first}, last={last}", file=sys.stderr)
            sys.exit(1)
        print(f"Sampling from {first} to {last} on {branch_ref}", file=sys.stderr)
        if args.dates:
            months = []
            for ds in args.dates:
                try:
                    months.append(datetime.datetime.strptime(ds, '%Y-%m-%d').date())
                except ValueError:
                    print(f"Invalid date format: {ds}", file=sys.stderr)
                    sys.exit(1)
        else:
            d0 = datetime.datetime.strptime(first, '%Y-%m-%d').date()
            d1 = datetime.datetime.strptime(last, '%Y-%m-%d').date()
            months = list_month_starts(d0, d1)

        results = {}
        # sample each month
        for dt in months:
            ds = dt.strftime('%Y-%m-%d')
            # find the last commit on or before this date on the target branch
            commit = run(
                ['git', 'rev-list', '-1', '--before', f'{ds} 23:59:59', branch_ref],
                cwd=tmp,
                capture_output=True
            ).stdout.strip()
            if not commit:
                continue
            # checkout
            run(['git', 'checkout', commit], cwd=tmp)
            if args.debug:
                print(f"=== {ds} commit {commit} ===", file=sys.stderr)
            # run scc
            out = run(['scc', '-f', 'json'], cwd=tmp, capture_output=True)
            if args.debug:
                print(out.stdout, file=sys.stderr)
            try:
                stats = json.loads(out.stdout)
            except json.JSONDecodeError:
                print(f'Error parsing scc JSON at {ds}', file=sys.stderr)
                continue
            per_lang = {}
            for ent in stats:
                # support various JSON key casings from scc
                name = ent.get('Name') or ent.get('language') or ent.get('Language') or ent.get('name')
                lines = ent.get('Code') or ent.get('code') or ent.get('Lines') or ent.get('lines')
                complexity = ent.get('Complexity') or ent.get('complexity')
                if not name:
                    continue
                per_lang[name] = {'lines': lines, 'complexity': complexity}
            results[ds] = per_lang

        # output JSON or CSV
        if args.csv:
            # wide CSV: date, <lang>_lines, <lang>_complexity...
            import csv
            # collect all languages
            langs = set()
            for per in results.values():
                langs.update(per.keys())
            langs = sorted(langs)
            # build header
            header = ['date']
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
                    row.append(vals.get('lines', ''))
                    row.append(vals.get('complexity', ''))
                writer.writerow(row)
        else:
            json.dump(results, sys.stdout, indent=2)
            sys.stdout.write('\n')
    finally:
        # cleanup
        shutil.rmtree(tmp)


if __name__ == '__main__':
    main()