"""
Download the Olist dataset from Kaggle and copy the 9 CSV files into data/raw/.

Uses kagglehub, which can fetch public datasets. If Kaggle asks for a login,
download the ZIP by hand from kaggle.com/datasets/olistbr/brazilian-ecommerce
and unzip it into data/raw/ instead.
"""
import shutil
from pathlib import Path

import kagglehub

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATASET = "olistbr/brazilian-ecommerce"


def main() -> None:
    download_dir = Path(kagglehub.dataset_download(DATASET))
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(download_dir.glob("*.csv"))
    for path in csv_files:
        shutil.copy2(path, RAW_DIR / path.name)
        print("Copied", path.name)

    print(f"{len(csv_files)} files in {RAW_DIR}")


if __name__ == "__main__":
    main()
