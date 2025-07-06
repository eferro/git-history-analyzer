# 📄 Product Requirements Document (PRD) — Git History Analyzer

## 🎯 Objective

Create a Python CLI tool that allows:
- Clone a Git repository (SSH or HTTPS).
- Move to a previous state (snapshot) by date.
- Analyze code using `scc` (v3.5.0) to obtain line count and complexity by language.
- Export results in JSON and CSV.

## 💡 Problem it solves

- Enables analysis of a project's technical evolution.
- Helps visualize growth and potential technical debt.

## 🧑‍💻 Target users

- Software engineers.
- Tech leads.
- People interested in historical code metrics.

## 🔥 Key features (MVP)

1️⃣ Clone repo from URL.
2️⃣ Checkout to previous commit (by date using `git rev-list`).
3️⃣ Execute `scc` (`-f json`).
4️⃣ Save report in JSON and CSV (minimum: totals by language, lines and approximate complexity).
5️⃣ CLI with:
- `--repo-url`
- `--since-date`
- `--output-dir`

## 🟡 Future improvements (not for MVP)

- Analysis at multiple dates (timeline).
- Charts or visual dashboards.
- Incremental analysis by commits or tags.

## ⚖️ Success criteria

- Works with public and private repos (SSH).
- Exports JSON and CSV correctly.
- Simple installation via PyPI.

## 📊 Success metrics

- Average analysis time < 2 min on medium repos.
- Report manually verified on minimum 3 different repos.

## 🛑 Exclusions (out of MVP scope)

- Graphical visualizations.
- Detailed incremental analysis.
- Direct CI/CD integration.
