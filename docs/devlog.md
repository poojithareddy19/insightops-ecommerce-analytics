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

## 2026-10-10 (Phase 4)
- Did: statistics notebook (skew, Mann-Whitney on late vs on-time reviews, full simulated A/B test) and the decision memo.
- Problem: `jupyter nbconvert` crashed with "DLL load failed while importing _zmq". The venv's `jupyter` launcher was picking up miniconda's broken pyzmq.
- Fix: run it as `python -m nbconvert` with the venv's Python, so everything comes from the venv.
- Problem: the log10 histogram of order value broke on orders worth 0 (valid orders with no items). Filtered to positive values for that plot.
- Added: a within-state check on the review gap. Late orders score 1.6 to 2.3 stars lower inside each of the 10 biggest states, so geography doesn't explain it away.
- Result: the free shipping test "wins" on significance (+0.86 pp, p < 0.0001) and loses on money (about -R$59k net). Breaking even needs a 12.5 pp lift.
- Learned: daily peeking turned a 5% false positive rate into 24% in simulation. Fix the sample size first.
- Next: dashboards.

## 2026-10-10 (Phase 5)
- Did: CSV exports for Looker Studio, two dashboard pages rendered from the marts, Excel category report.
- Decision: built the dashboards as a script (matplotlib) instead of Looker Studio for now, so they rebuild from the warehouse with one command. The exports are ready for Looker later.
- Redesign: the guide's operations page puts median delivery days and late rate on one time series. Different units, so I split them into two charts instead of a dual axis. That split is what made Feb-Mar 2018 obvious: the late rate hit 19%.
- Correction: I first wrote that delivery barely slowed and the estimates were simply too tight. Looking at the chart again, Feb 2018 is the slowest month (median 14 days). Checked promised vs actual by month: deliveries slowed to 13-14 days AND the promised window shrank from 26 to 22 days. Both at once.
- Problem: the "Nov 2017 peak" label sat on top of the chart subtitle, then on top of the line. Moved it to the left of the point.
- Problem: openpyxl can't create a real PivotTable. Built the pivot as a sorted summary table and kept XLOOKUP and actual vs target as live formulas. Opened it in Excel to confirm the formulas actually calculate.
- Next: capstone on repeat purchases.

## 2026-10-10 (Phase 6)
- Did: capstone analysis (query 12), memo and a 5-slide deck generated from the warehouse.
- Choice: only first orders from Jan 2017 to May 2018 in the capstone, so every customer had 3+ months to come back. Without that, mid-2018 customers drag the return rate down just because the data ends.
- Result: a late first delivery cuts the return rate by a third (1.74% vs 2.57%, CI 0.47 to 1.19 pp). Not "half", which is what I expected going in.
- Surprise: when I did the impact maths, fixing late first deliveries is worth only R$4k to R$7k a year in repeat sales. 5,250 late first orders x 0.83 pp x R$167 is just small. The bigger lever is a first-month win-back for all 65.7k new customers (R$55k to R$110k), and it has to be A/B tested.
- How I estimated impact: customers a year x (target rate - current rate) x R$167 of later orders per returning customer. Target rates come from groups already in the data (on-time first orders; high-return categories at 3.1-4.3%), and every number is given as a range.
- Problem: deck slide showed "R55ktoR110k" in italics. Two dollar signs in one string turn on matplotlib's math mode. Fixed with text.parse_math = False.
- Next: README landing page.

## 2026-10-10 (Phase 7)
- Did: README landing page with the real findings, resume bullets with real numbers.
- Still to do by hand: Looker Studio version of the dashboards, blog posts, demo video, LinkedIn posts, pinning the repo.
