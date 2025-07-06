# 🛠️ Implementation Plan — Git History Analyzer

## 💥 Philosophy

"If we had to deliver it tomorrow, what would we do?"

👉 Reduce to minimum viable. Each step must be functional and reversible.

---

## 🍔 Initial Slicing (Hamburger Method)

### Layer 1: Repo checkout

- **1.1:** Clone repo without historical checkout.
- **1.2:** Add checkout by hardcoded hash.
- **1.3:** Checkout by date (`git rev-list -n 1 --before`).

✅ Start with 1.1, then 1.2 and finally 1.3.

### Layer 2: Metrics with scc

- **2.1:** Execute `scc` and display in console.
- **2.2:** Save JSON output.
- **2.3:** Parse and export CSV.

✅ Start with 2.1 and then advance.

### Layer 3: CLI

- **3.1:** Script with hardcoded parameters.
- **3.2:** CLI with `argparse` and flags (`--repo-url`, `--since-date`, `--output-dir`).

✅ Start with 3.1.

### Layer 4: Packaging

- **4.1:** Standalone script.
- **4.2:** Packaging with `pyproject.toml` and `uv`.
- **4.3:** Publication on PyPI.

✅ Start with 4.1.

---

## ✅ Initial micro-steps (1–3 hours each)

1️⃣ Clone repo and print "repo cloned!".
2️⃣ Checkout to hardcoded commit.
3️⃣ Execute `scc` and display JSON in console.
4️⃣ Save JSON to file.
5️⃣ Generate basic CSV (one line per language: language, lines, complexity).
6️⃣ Replace hardcoded values with arguments (`argparse`).
7️⃣ Configure `pyproject.toml` with `uv`, package.
8️⃣ Prepare README and publish on PyPI.

---

## 🟢 First deliverable slice

- Python script that:
  - Clones repo.
  - Hardcoded checkout.
  - Executes `scc` and saves JSON.
  - Without complete CLI or CSV yet.

---

## ⚖️ Anti-patterns to avoid

- Don't generalize or create internal libraries yet.
- Don't add incremental analysis in MVP.
- Don't optimize for multiple dates before validating.

