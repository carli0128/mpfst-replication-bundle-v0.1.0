#!/usr/bin/env bash
set -euo pipefail

# Fetch a small, open-access set of data for the notebooks and examples.
# - IRIS seismic (MiniSEED + CSV)
# - GWOSC event JSON (no large strain files)
# - PhysioNet EEG (CSV) if MNE is available in this shell env

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# IRIS (1–10 minutes)
python3 data/fetch_iris.py \
  --network "${IRIS_NETWORK:-IU}" \
  --station "${IRIS_STATION:-ANMO}" \
  --location "${IRIS_LOCATION:-*}" \
  --channel "${IRIS_CHANNEL:-BHZ}" \
  --start   "${IRIS_START:-2020-01-01T00:00:00}" \
  --duration "${IRIS_DURATION:-600}" \
  --csv

# GWOSC event JSON
python3 data/fetch_gwosc.py \
  --catalog "${GWOSC_CATALOG:-GWTC-1-confident}" \
  --event   "${GWOSC_EVENT:-GW150914}"

# EEG via PhysioNet (optional; requires MNE in this shell environment)
if python3 - <<'PY'
try:
  import mne  # just a probe
  import sys
  print('OK')
  sys.exit(0)
except Exception:
  import sys
  print('NO')
  sys.exit(1)
PY
then
  python3 data/fetch_openneuro.py --provider physionet --channel "${EEG_CHANNEL:-Cz}" --export-csv
else
  echo "[info] MNE not installed in this terminal environment; skipping EEG fetch." >&2
  echo "       Tip: pip install mne  # then re-run this script" >&2
fi

echo "All fetches attempted. Cached under data/cache/."