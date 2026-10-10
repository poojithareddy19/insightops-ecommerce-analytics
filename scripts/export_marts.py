# Author: Gorla Poojitha
"""
Export the mart tables to CSV files in data/exports/
so you can upload them to Looker Studio, Google Sheets, Excel or BigQuery.

Also runs scripts/export_cohort_retention.sql, so one command writes all 9 files.
Every file starts with a '# Author' line. Looker Studio can't skip that line,
so for Looker uploads run:  python scripts/export_marts.py --plain
"""
import argparse
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "warehouse" / "insightops.duckdb"
EXPORT_DIR = PROJECT_ROOT / "data" / "exports"
COHORT_SQL = PROJECT_ROOT / "scripts" / "export_cohort_retention.sql"
AUTHOR_LINE = b"# Author: Gorla Poojitha\n"

MARTS = ["fct_orders", "fct_order_items", "fct_payments",
         "dim_customers", "dim_products", "dim_sellers", "dim_dates"]


def add_author_line(path: Path) -> None:
    """COPY rewrites each file from scratch, so the line is never added twice."""
    path.write_bytes(AUTHOR_LINE + path.read_bytes())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--plain", action="store_true",
                        help="leave out the '# Author' line (use this for Looker Studio uploads)")
    args = parser.parse_args()

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH), read_only=True)
    written = []
    for table in MARTS:
        out = EXPORT_DIR / f"{table}.csv"
        con.execute(f"COPY marts.{table} TO '{out.as_posix()}' (HEADER, DELIMITER ',')")
        written.append(out)

    # A pre-joined, dashboard-friendly table: one row per order item with category and seller state
    out = EXPORT_DIR / "dashboard_order_items.csv"
    con.execute(f"""
        COPY (
            select
                i.order_id, i.order_date, i.price, i.freight_value, i.item_total,
                p.category_name, s.seller_state,
                o.customer_state, o.customer_state_iso, o.is_late, o.review_score, o.delivery_days
            from marts.fct_order_items i
            join marts.fct_orders  o on i.order_id = o.order_id
            join marts.dim_products p on i.product_id = p.product_id
            join marts.dim_sellers  s on i.seller_id = s.seller_id
            where i.is_valid_order
        ) TO '{out.as_posix()}' (HEADER, DELIMITER ',')
    """)
    written.append(out)

    # The cohort query writes to a path relative to the project root; make it absolute
    out = EXPORT_DIR / "cohort_retention.csv"
    con.execute(COHORT_SQL.read_text(encoding="utf-8").replace("data/exports/cohort_retention.csv", out.as_posix()))
    written.append(out)

    for path in written:
        if not args.plain:
            add_author_line(path)
        print("Exported", path)


if __name__ == "__main__":
    main()
