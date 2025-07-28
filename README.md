# Git History Metrics Collector

This utility clones a Git repository and samples its codebase at configurable intervals
(daily, weekly, or monthly, or at specific dates).
It runs [scc](https://github.com/boyter/scc) to collect per-language metrics (lines of code and complexity)
and outputs the results as JSON or CSV for easy analysis and charting.

## Requirements
- Python 3.8+ (tested on Python 3.12)
- [git](https://git-scm.com/) installed and in your `PATH`
- [scc](https://github.com/boyter/scc) installed (tested with scc v3.5.0)
- Access to the target repository (SSH or HTTPS clone URL); authentication must be preconfigured.

## Installation
1. Ensure Git and scc are installed:
   ```sh
   # Ubuntu/Debian example
   sudo apt-get update && sudo apt-get install git
   sudo snap install scc --classic
   ```
2. Install the package from PyPI:
   ```sh
   pip install git-history-analyzer
   ```
   You can also clone this repository and install it locally with `pip install .`.

## Usage
```sh
git-history-metrics [OPTIONS] <repo_url>
```

### Positional Argument
- `<repo_url>`: Git clone URL (SSH or HTTPS) of the repository to analyze.

### Options
- `--branch BRANCH` : Branch or ref to sample (default: `HEAD`).
- `--dates YYYY-MM-DD [YYYY-MM-DD ...]` : Specific dates to sample instead of the full history.
- `--period {daily,weekly,monthly}` : Sampling period when `--dates` is not provided.
- `--csv`          : Output a wide CSV (one row per date, one column per language metric).
- `--debug`        : Print debug information (commit SHA, raw scc JSON) to stderr.
- `-h, --help`     : Show help message and exit.

## Output Formats

- **JSON** (default):
  ```json
  {
    "2024-06-01": {
      "Python": { "lines": 43768, "complexity": 2479 },
      "YAML":   { "lines": 24432, "complexity": null },
      ...
    },
    ...
  }
  ```

- **CSV** (`--csv`): Wide format for multi-series line charts.
  ```csv
  date,Python_lines,Python_complexity,YAML_lines,YAML_complexity,...
  2024-06-01,43768,2479,24432,,...
  2024-07-01,44210,2503,24500,,...
  ```

## Examples

- Sample monthly (the default period) for the default branch, output JSON:
  ```sh
  git-history-metrics https://github.com/user/project.git > metrics.json
  ```

- Sample specific dates, output CSV:
  ```sh
  git-history-metrics \
    git@github.com:user/project.git \
    --dates 2023-01-01 2023-06-01 2023-12-01 \
    --csv > metrics.csv
  ```

- Sample full history monthly on the default branch, output CSV:
  ```sh
  git-history-metrics https://github.com/user/project.git --csv > metrics_full_history.csv
  ```

## Cleanup
The script uses a temporary folder to clone and automatically removes it when done.

## License
This script is provided under the MIT License. See LICENSE for details.
