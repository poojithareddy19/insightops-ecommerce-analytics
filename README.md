# InsightOps: End-to-End E-commerce Analytics

**By Gorla Poojitha** ([@poojithareddy19](https://github.com/poojithareddy19))

I built the analytics function for a real Brazilian e-commerce marketplace
(Olist, ~100k orders): from raw data to a tested warehouse, SQL analyses, an A/B
test, dashboards and business recommendations.

**Capstone memo:** [docs/capstone-memo.md](docs/capstone-memo.md)  |  **Deck:** [docs/capstone-deck.pdf](docs/capstone-deck.pdf)  |  **Dashboards:** [dashboards/](dashboards/README.md)

![Executive dashboard](dashboards/executive_overview.png)

## Key findings
- Only **2.2%** of customers ever come back on a later day (2,065 of 94,990). A naive
  "2+ orders" count says 3.0%, but 250 of those are one checkout split into two orders.
- The top 10% of customers generate **38.3%** of revenue, through single large orders,
  not loyalty.
- Orders delivered 7+ days late average **1.70 stars** vs 4.17 on time; 79% of them get 1 or 2 stars.
- A late first delivery cuts the chance of returning by a third (1.74% vs 2.57%).
- A first-month win-back program could add an estimated **R$55k to R$110k a year**;
  fixing late first deliveries alone adds only R$4k to R$7k in repeat sales.
- A simulated free-shipping A/B test lifts conversion by +0.86 pp but loses about R$59k
  once shipping cost is counted against commission. Recommendation: don't ship.

## Architecture
```text
Kaggle CSVs + Frankfurter API (GitHub Actions, weekly)
        -> Python loaders -> DuckDB (raw)
        -> dbt (staging -> marts, 17 models, 49 data tests)
        -> SQL analyses + Python stats -> dashboards, Excel report, memos
```
![dbt lineage](dashboards/dbt_lineage.png)

## What's inside
| Folder | Contents |
|---|---|
| ingestion/ | Raw loader and API ingestion |
| dbt/ | Staging and mart models with tests |
| analyses/ | 17 SQL queries, each answering a business question, plus data quality checks |
| notebooks/ | Statistics and simulated A/B test |
| docs/ | Data audit, metric catalog, insight memo, A/B memo, capstone memo and deck, devlog |
| dashboards/ | Executive and operations dashboards, Excel report, lineage graph |
| scripts/ | Download, profiling, SQL runner, exports, dashboard/deck/report builders |

Start with [docs/data-audit.md](docs/data-audit.md) (15 data issues and what I did about
each), [docs/metric-catalog.md](docs/metric-catalog.md) and
[docs/insights-part1.md](docs/insights-part1.md).

## Run it yourself
Python 3.12. From the project root:

1. `python -m venv .venv`, activate it, `pip install -r requirements.txt`
2. `python scripts/download_olist.py` (or download the dataset from Kaggle into data/raw/)
3. `python ingestion/fetch_rates.py`
4. `python ingestion/load_raw.py`
5. `cd dbt && dbt build && cd ..` (expect PASS=65 WARN=1 ERROR=0; the warning is explained in the data audit)
6. `python scripts/run_sql.py analyses/03_never_reordered.sql` (any query in analyses/)
7. `python scripts/build_dashboards.py`, `python scripts/build_deck.py`
8. `python scripts/export_marts.py` (add `--plain` for Looker Studio uploads), then `python scripts/build_excel_report.py`

On Windows, if `jupyter nbconvert` fails with a pyzmq DLL error, run it as
`python -m nbconvert` so it uses the venv instead of another Python install.
