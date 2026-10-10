# Resume bullets

Filled in with the project's real numbers. Each one is backed by a file in this repo.

- Modeled a 100k-order e-commerce dataset into a star schema with dbt (17 models, 49 data tests), reducing typical analysis queries from multi-table joins to single-table reads
- Found that customer_id identified orders rather than people (99,441 ids vs 96,096 real customers) and that 250 "repeat customers" were split checkouts; corrected the repeat rate from 3.0% to 2.2% and enforced the right keys with dbt tests
- Built cohort retention and revenue-concentration analyses showing 38% of revenue came from the top 10% of customers; showed a late first delivery cuts the return rate by a third and proposed a first-month win-back program worth an estimated R$55k to R$110k per year
- Designed and analyzed a simulated A/B test (power analysis, SRM and A/A checks, significance testing) and recommended against shipping a statistically significant result after costing it (about -R$59k net)
- Built executive and operations dashboards tracking 8 KPIs from dbt marts, plus an Excel category report with XLOOKUP targets
