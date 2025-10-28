#!/usr/bin/env python
import argparse, pandas as pd, json
from mpfst.spectral.octave_jump import detect_shell_jumps_series

ap = argparse.ArgumentParser()
ap.add_argument("--csv", required=True, help="CSV with column x")
ap.add_argument("--fs", type=float, required=True)
ap.add_argument("--fmin", type=float, required=True)
ap.add_argument("--fmax", type=float, required=True)
args = ap.parse_args()

x = pd.read_csv(args.csv)['x'].values
out = detect_shell_jumps_series(x, args.fs, args.fmin, args.fmax)
print(json.dumps(out))
