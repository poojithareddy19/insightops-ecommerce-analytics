# Devlog

## 2026-10-10 (Phase 0)
- Did: created the repo, folder layout, .gitignore and requirements, set up a Python 3.12 venv, downloaded the Olist data.
- Problem: the default `python` on this machine is 3.13 from miniconda, and the guide targets 3.12.
- Fix: created the venv with the `py` launcher pointing at 3.12 so the project doesn't depend on whatever conda has active.
- Problem: downloading from Kaggle by hand is a manual step nobody can repeat from the repo.
- Fix: added `scripts/download_olist.py`, which pulls the public dataset with kagglehub and copies the 9 CSVs into data/raw.
- Learned: the raw folder is about 125 MB, mostly geolocation (61 MB). Good reason to keep it out of Git.
- Next: exchange rates API, raw loader, profiling.

## 2026-10-10 (Phase 1)
- Did: exchange-rate ingestion (2,610 daily rates), raw loader into DuckDB, weekly GitHub Actions refresh, profiling, quality checks, data audit.
- Checked: ran load_raw.py twice, counts identical both times (idempotent).
- Problem: `run_sql.py` crashed with UnicodeEncodeError on Windows. DuckDB draws result tables with box characters and the console was cp1252.
- Fix: `sys.stdout.reconfigure(encoding="utf-8")` at the top of the script.
- Most surprising: 99,441 customer_ids but only 96,096 real people. Counting customer_id would make almost every customer look like a one-time buyer by construction. Also 789 review_ids are shared by 2+ orders, so review_id can't be a key either.
- Also: November 2016 has zero orders, and Sep/Oct 2018 have 20 between them. Any trend chart has to be cut to Jan 2017 to Aug 2018.
- Next: dbt staging and marts.
