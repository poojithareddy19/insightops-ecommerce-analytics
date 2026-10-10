# Author: Gorla Poojitha
"""
Download daily BRL -> USD exchange rates from the free Frankfurter API
(no API key needed) and save them to data/external/brl_usd_rates.csv.

Safe to rerun: the CSV is rebuilt from scratch every time.
"""
import csv
from datetime import date, timedelta
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = PROJECT_ROOT / "data" / "external" / "brl_usd_rates.csv"
BASE_URL = "https://api.frankfurter.app"
START_DATE = date(2016, 8, 1)  # a little before the first Olist order


def fetch_window(start: date, end: date) -> dict:
    """Return {'2016-08-01': 0.31, ...} for one date window."""
    url = f"{BASE_URL}/{start.isoformat()}..{end.isoformat()}"
    response = requests.get(url, params={"from": "BRL", "to": "USD"}, timeout=30)
    response.raise_for_status()  # stop with an error if the API call failed
    rates = response.json().get("rates", {})
    return {day: values["USD"] for day, values in rates.items()}


def main() -> None:
    all_rates = {}
    window_start = START_DATE
    today = date.today()

    # Ask for 90 days at a time to keep each request small.
    while window_start <= today:
        window_end = min(window_start + timedelta(days=89), today)
        all_rates.update(fetch_window(window_start, window_end))
        window_start = window_end + timedelta(days=1)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="") as f:
        # Always "\n": the csv default is "\r\n", which made each run on Linux rewrite every line
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["rate_date", "brl_to_usd"])
        for day in sorted(all_rates):
            writer.writerow([day, all_rates[day]])

    print(f"Saved {len(all_rates):,} daily rates to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
