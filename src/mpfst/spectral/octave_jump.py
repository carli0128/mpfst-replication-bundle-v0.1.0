import argparse, json, numpy as np
from .utils import octave_band_edges, filterbank_energy
from .ssm import dominant_shell_indices, detect_shell_jumps

def detect_shell_jumps_series(x, fs, fmin, fmax, n_bands=8, energy_min=None, min_gap=1):
    edges = octave_band_edges(fmin, fmax, n_bands)
    E = filterbank_energy(np.asarray(x), fs, edges)
    dom = dominant_shell_indices(E, energy_min=energy_min)
    jumps = detect_shell_jumps(dom, edges, min_gap=min_gap)
    return {"edges": edges.tolist(), "jumps": jumps}

def detect_shell_jumps_cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="CSV with 1D signal column 'x'")
    ap.add_argument("--fs", type=float, required=True)
    ap.add_argument("--fmin", type=float, required=True)
    ap.add_argument("--fmax", type=float, required=True)
    ap.add_argument("--bands", type=int, default=8)
    ap.add_argument("--energy-min", type=float, default=None)
    ap.add_argument("--min-gap", type=int, default=1)
    args = ap.parse_args()
    import pandas as pd
    df = pd.read_csv(args.csv)
    x = df["x"].values
    out = detect_shell_jumps_series(x, args.fs, args.fmin, args.fmax,
                                    n_bands=args.bands, energy_min=args.energy_min,
                                    min_gap=args.min_gap)
    print(json.dumps(out))
