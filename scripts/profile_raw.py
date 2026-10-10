"""
Profile every raw table: row count, and the null percentage of every column.
Writes the result to docs/profile_raw.md so you can read it and use it in your data audit.
"""
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "warehouse" / "insightops.duckdb"
OUTPUT_FILE = PROJECT_ROOT / "docs" / "profile_raw.md"


def main() -> None:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    tables = [row[0] for row in con.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'raw' ORDER BY 1"
    ).fetchall()]

    lines = ["# Raw data profile", "", "*Gorla Poojitha*", ""]
    for table in tables:
        total = con.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]
        lines += [f"## raw.{table} ({total:,} rows)", "", "| column | nulls | null % | distinct values |", "|---|---|---|---|"]
        columns = [row[0] for row in con.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema = 'raw' AND table_name = ? ORDER BY ordinal_position", [table]
        ).fetchall()]
        for col in columns:
            nulls, distinct = con.execute(
                f'SELECT COUNT(*) - COUNT("{col}"), COUNT(DISTINCT "{col}") FROM raw.{table}'
            ).fetchone()
            pct = 100 * nulls / total if total else 0
            lines.append(f"| {col} | {nulls:,} | {pct:.2f}% | {distinct:,} |")
        lines.append("")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print("Profile written to", OUTPUT_FILE)


if __name__ == "__main__":
    main()
