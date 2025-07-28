#!/usr/bin/env python3
"""Backward compatibility wrapper for the git-history-analyzer package."""
from git_history_analyzer.cli import main

if __name__ == "__main__":
    raise SystemExit(main())

