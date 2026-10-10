# Author: Gorla Poojitha
"""
Download the Olist dataset from Kaggle and copy the 9 CSV files into data/raw/.

Uses kagglehub, which can fetch public datasets. If Kaggle asks for a login,
download the ZIP by hand from kaggle.com/datasets/olistbr/brazilian-ecommerce
and unzip it into data/raw/ instead.
"""
from pathlib import Path

import kagglehub

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATASET = "olistbr/brazilian-ecommerce"
AUTHOR_LINE = b"# Author: Gorla Poojitha"
BOM = b"\xef\xbb\xbf"


def main() -> None:
    download_dir = Path(kagglehub.dataset_download(DATASET))
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(download_dir.glob("*.csv"))
    for path in csv_files:
        # Add an author line on top; the data below it is copied byte for byte,
        # and the original download stays untouched in the kagglehub cache.
        # The Kaggle files use "\r\n"; the author line must match, or DuckDB's
        # format detection fails on files with mixed line endings.
        # One file also starts with a UTF-8 byte order mark, which has to stay first.
        data = path.read_bytes()
        bom = BOM if data.startswith(BOM) else b""
        data = data[len(bom):]
        newline = b"\r\n" if b"\r\n" in data[:data.find(b"\n") + 1] else b"\n"
        (RAW_DIR / path.name).write_bytes(bom + AUTHOR_LINE + newline + data)
        print("Copied", path.name)

    print(f"{len(csv_files)} files in {RAW_DIR}")


if __name__ == "__main__":
    main()
