# 📋 Implementation Plan — Git History Analyzer

## 🧭 Approach
- Strict TDD: Red → Green → Refactor for each increment
- "Tidy First": Structural changes before behavioral
- Each task is a single, testable step
- Use Python 3.12, uv, unittest, doublex, expects

---

## 🗂️ Task List

### Layer 1: Repository Operations
- **T1**: [ ] Create project folder structure (src/, tests/, etc.)
- **T2**: [ ] Implement function to clone a git repository (hardcoded URL)
- **T3**: [ ] Add ability to checkout to a hardcoded commit hash
- **T4**: [ ] Add ability to checkout to a commit by date

### Layer 2: Metrics Collection
- **T5**: [ ] Implement function to run scc on the checked-out repo and print JSON to console
- **T6**: [ ] Save scc JSON output to a file
- **T7**: [ ] Parse scc JSON and export a CSV (language, lines, complexity)

### Layer 3: CLI
- **T8**: [ ] Script with hardcoded parameters for repo URL, date, output dir
- **T9**: [ ] Implement CLI with argparse for --repo-url, --since-date, --output-dir
- **T10**: [ ] Ensure output directory is created if it does not exist

### Layer 4: Packaging & Tooling
- **T11**: [ ] Add pyproject.toml for uv and dependencies (doublex, expects, etc.)
- **T12**: [ ] Add README and usage instructions

### Layer 5: Testing & Quality
- **T13**: [ ] Set up unittest with doublex and expects for assertions
- **T14**: [ ] Add tests for each function (clone, checkout, scc, export)
- **T15**: [ ] Add integration test for end-to-end flow

---

## ✅ Conventions
- Each task is a single commit (structural or behavioral)
- All code is covered by tests
- No step proceeds without a failing test first
- Refactor only after green

---

(Tasks will be checked off as completed. Add new tasks as needed for future improvements.) 