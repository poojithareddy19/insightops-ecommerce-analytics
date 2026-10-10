# Author: Gorla Poojitha
"""
Load the Olist CSV files (and the exchange-rate CSV) into the 'raw' schema
of the DuckDB warehouse.

Safe to rerun: every table is fully replaced, never appended,
so running this twice never creates duplicate rows (this is called "idempotent").
"""
from pathlib import Path

import duckdb

# Paths are built from this file's location, so the script works
# no matter which folder you run it from.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
EXTERNAL_DIR = PROJECT_ROOT / "data" / "external"
DB_PATH = PROJECT_ROOT / "warehouse" / "insightops.duckdb"

# table name in the warehouse  ->  CSV file on disk
TABLES = {
    "customers": RAW_DIR / "olist_customers_dataset.csv",
    "geolocation": RAW_DIR / "olist_geolocation_dataset.csv",
    "order_items": RAW_DIR / "olist_order_items_dataset.csv",
    "order_payments": RAW_DIR / "olist_order_payments_dataset.csv",
    "order_reviews": RAW_DIR / "olist_order_reviews_dataset.csv",
    "orders": RAW_DIR / "olist_orders_dataset.csv",
    "products": RAW_DIR / "olist_products_dataset.csv",
    "sellers": RAW_DIR / "olist_sellers_dataset.csv",
    "category_translation": RAW_DIR / "product_category_name_translation.csv",
    "brl_usd_rates": EXTERNAL_DIR / "brl_usd_rates.csv",
}


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")

    for table, path in TABLES.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing file: {path}")

        # all_varchar = true loads every column as text.
        # Raw data should be an untouched copy; we fix types later in dbt.
        # It also protects zip codes like '01310' from losing the leading zero.
        # Our own rates file starts with a '# Author' line; the Olist files are left exactly as downloaded.
        comment = ", comment = '#'" if table == "brl_usd_rates" else ""
        con.execute(f"""
            CREATE OR REPLACE TABLE raw.{table} AS
            SELECT * FROM read_csv('{path.as_posix()}', header = true, all_varchar = true{comment})
        """)
        row_count = con.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]
        print(f"raw.{table:<22} {row_count:>10,} rows")

    con.close()
    print("Done. Warehouse file:", DB_PATH)


if __name__ == "__main__":
    main()
