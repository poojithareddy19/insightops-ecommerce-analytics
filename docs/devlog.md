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

## 2026-10-10 (Phase 2)
- Did: dbt project with 10 staging views and 7 mart tables, 47 schema tests + 2 singular tests, docs, lineage graph, metric catalog.
- Result: `dbt build` gives PASS=65 WARN=1 ERROR=0.
- Problem: the warning (1,021 orders where payments != items + freight) was supposed to be installment interest. When I split it, 772 of them were paid orders with no items at all, mostly unavailable/canceled. Interest only explains about 230.
- Learned: check an explanation before writing it into the audit. The "obvious" cause was the minority.
- Decisions: a customer is a customer_unique_id, never customer_id. Revenue is items + freight on valid orders (not payment_value, which includes interest and money taken for orders that never shipped).
- Problem: I wanted the lineage image to be reproducible instead of a manual screenshot of `dbt docs serve`.
- Fix: `scripts/plot_lineage.py` draws it from dbt/target/manifest.json. First version showed one box because matplotlib doesn't autoscale for text; had to set the axis limits by hand.
- Next: SQL analysis portfolio.

## 2026-10-10 (Phase 3)
- Did: 16 analysis queries (01-11 from the plan, 13-17 my own), insights memo.
- Problem: query 03 said 2,638 customers ordered again, dim_customers said 2,888 repeat customers. Same data, two answers.
- Cause: 250 customers have two orders with the exact same purchase timestamp. That's one checkout split into two orders (probably different sellers), not someone coming back. Query 03 compares timestamps with `>`, so it skips them; dim_customers counts orders.
- Fix: added `is_returning_customer` (valid orders on 2+ different days) to dim_customers and made it the headline metric: 2,065 of 94,990 customers, 2.2%.
- Surprise: the 20 worst sellers by late rate only cause 3% of late orders. The plan assumed seller SLAs on those sellers would fix a lot. Volume is in the big sellers.
- Learned: always reconcile a number against a second query before writing it down.
- Next: statistics notebook and the A/B test.
