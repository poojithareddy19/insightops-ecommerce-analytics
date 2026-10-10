# Devlog

## 2026-10-10 (Phase 0)
- Did: created the repo, folder layout, .gitignore and requirements, set up a Python 3.12 venv, downloaded the Olist data.
- Problem: the default `python` on this machine is 3.13 from miniconda, and the guide targets 3.12.
- Fix: created the venv with the `py` launcher pointing at 3.12 so the project doesn't depend on whatever conda has active.
- Problem: downloading from Kaggle by hand is a manual step nobody can repeat from the repo.
- Fix: added `scripts/download_olist.py`, which pulls the public dataset with kagglehub and copies the 9 CSVs into data/raw.
- Learned: the raw folder is about 125 MB, mostly geolocation (61 MB). Good reason to keep it out of Git.
- Next: exchange rates API, raw loader, profiling.
