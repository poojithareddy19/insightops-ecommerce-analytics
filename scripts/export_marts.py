"""
Export the mart tables to CSV files in data/exports/
so you can upload them to Looker Studio, Google Sheets, Excel or BigQuery.
"""
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "warehouse" / "insightops.duckdb"
EXPORT_DIR = PROJECT_ROOT / "data" / "exports"

MARTS = ["fct_orders", "fct_order_items", "fct_payments",
         "dim_customers", "dim_products", "dim_sellers", "dim_dates"]


def main() -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH), read_only=True)
    for table in MARTS:
        out = EXPORT_DIR / f"{table}.csv"
        con.execute(f"COPY marts.{table} TO '{out.as_posix()}' (HEADER, DELIMITER ',')")
        print("Exported", out)

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
    print("Exported", out)


if __name__ == "__main__":
    main()
