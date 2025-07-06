# Monthly SCC Metrics Collector

This script clones a Git repository, samples its codebase at the first of each month (or specified dates),
runs [scc](https://github.com/boyter/scc) to collect per-language metrics (lines of code and complexity),
and outputs the results as JSON or CSV for easy analysis and charting.

## Requirements
- Python 3.6+ (tested on Python 3.12)
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
2. Clone or download this script into your working directory.

## Usage
```sh
python3 monthly_scc_metrics.py [OPTIONS] <repo_url>
``` 

### Positional Argument
- `<repo_url>`: Git clone URL (SSH or HTTPS) of the repository to analyze.

### Options
- `--branch BRANCH` : Branch or ref to sample (default: `HEAD`).
- `--dates YYYY-MM-DD [YYYY-MM-DD ...]` : Specific dates to sample instead of the full history.
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

- Sample every month for the default branch, output JSON:
  ```sh
  python3 monthly_scc_metrics.py https://github.com/user/project.git > metrics.json
  ```

- Sample specific dates, output CSV:
  ```sh
  python3 monthly_scc_metrics.py \
    git@github.com:user/project.git \
    --dates 2023-01-01 2023-06-01 2023-12-01 \
    --csv > metrics.csv
  ```

## Cleanup
The script uses a temporary folder to clone and automatically removes it when done.

## License
This script is provided under the MIT License. See LICENSE for details.