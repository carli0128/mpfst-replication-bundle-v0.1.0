import argparse, numpy as np

def hazard_curve(m_l: np.ndarray, events: np.ndarray, bins=20):
    m_l = np.asarray(m_l, dtype=float); events = np.asarray(events, dtype=bool)
    edges = np.linspace(0,1,bins+1)
    idx = np.digitize(m_l, edges)-1
    hazard = []
    centers = 0.5*(edges[:-1]+edges[1:])
    for b in range(bins):
        mask = idx==b
        if mask.sum()<5:
            hazard.append(np.nan); continue
        hazard.append(events[mask].mean())
    return centers, np.array(hazard)

def hazard_cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ml_csv", required=True, help="CSV with columns m_l,event")
    args = ap.parse_args()
    import pandas as pd
    df = pd.read_csv(args.ml_csv)
    c, h = hazard_curve(df["m_l"].values, df["event"].values.astype(bool))
    for ci, hi in zip(c, h):
        print(f"{ci:.3f},{hi if np.isfinite(hi) else 'nan'}")
