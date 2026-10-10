"""
Run a .sql file against the warehouse and print every result.
Usage:  python scripts/run_sql.py analyses/01_monthly_revenue_growth.sql
"""
import sys
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "warehouse" / "insightops.duckdb"

# DuckDB draws tables with box characters; the Windows console defaults to cp1252,
# which can't print them, so force UTF-8 output.
sys.stdout.reconfigure(encoding="utf-8")

if len(sys.argv) != 2:
    sys.exit("Usage: python scripts/run_sql.py path/to/query.sql")

query_text = Path(sys.argv[1]).read_text(encoding="utf-8")
con = duckdb.connect(str(DB_PATH), read_only=True)

# A file can hold several queries separated by ';'. Run and print each one.
for number, statement in enumerate(con.extract_statements(query_text), start=1):
    print(f"\n--- Result {number} ---")
    result = con.sql(statement.query)
    if result is None:          # statements like COPY return no table
        print("Done (no result table).")
    else:
        result.show(max_rows=50, max_width=250)
