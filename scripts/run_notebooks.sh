#!/usr/bin/env bash
set -euo pipefail

# Execute notebooks headlessly using nbconvert.
# By default, executes photonics and seismic notebooks.
# Set RUN_EEG=true to also execute the EEG notebook (may download data via MNE).

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Prefer project virtualenv Python if present
if [[ -x ".venv/bin/python" ]]; then
  PY=".venv/bin/python"
else
  PY="python3"
fi

# Ensure nbconvert is available
if ! "$PY" - <<'PY'
try:
  import nbconvert  # noqa: F401
  print('nbconvert: OK')
except Exception:
  raise SystemExit(1)
PY
then
  "$PY" -m pip install --upgrade pip >/dev/null 2>&1 || true
  "$PY" -m pip install nbconvert >/dev/null 2>&1
fi

# Photonics (uses synthetic if CSV missing)
"$PY" -m nbconvert --to notebook --execute notebooks/03_photonics_octave_jumps.ipynb --inplace

# Seismic (ObsPy fetches a short window)
"$PY" -m nbconvert --to notebook --execute notebooks/04_seismic_hazard_surrogates.ipynb --inplace

# EEG (optional; may download datasets via MNE)
if [[ "${RUN_EEG:-false}" == "true" ]]; then
  "$PY" -m nbconvert --to notebook --execute notebooks/02_eeg_hazard_tiering.ipynb --inplace
else
  echo "[info] Skipping EEG notebook (set RUN_EEG=true to include)."
fi

echo "Notebooks executed successfully."