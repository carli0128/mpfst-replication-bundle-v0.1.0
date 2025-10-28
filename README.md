# MPFST Replication Bundle

[![CI](https://github.com/carli0128/mpfst-replication-bundle-v0.1.0/actions/workflows/ci.yml/badge.svg)](https://github.com/carli0128/mpfst-replication-bundle-v0.1.0/actions/workflows/ci.yml)

This package ships the analysis tools for the MPFST empirical tests:
coherence triangle (μ, γ, H), mℓ meter, Spectral Shell Monitor (SSM) with octave shell‑jumps,
nulls/controls, collapse, densification, and the fractional (α, β) prediction loop.

## New: GW ringdowns — VBK superradiance specialization
- `src/mpfst/domains/gw_superradiance.py` — evaluate the Kerr/Kerr–Newman
  superradiance conditions as a *linear‑response* gate (does not change MPFST core).
- Unified API in `src/mpfst/gating/linear_response.py` (domain registry).
- CLI example:
  ```bash
  python scripts/vbk_gate.py --M 60 --a 0.8 --mu 0.05
  ```

## How to install
```bash
conda env create -f environment.yml
conda activate mpfst-replication
pip install -e .
pytest -q
```
