import numpy as np

def dominant_shell_indices(E: np.ndarray, energy_min=None):
    """Given energy matrix E [bands x time], return dominant band index per time.
    Optionally ignore frames where max energy < energy_min (returns -1).
    """
    if E.ndim!=2: raise ValueError("E must be (bands,time)")
    dom = E.argmax(axis=0)
    if energy_min is not None:
        mx = E.max(axis=0)
        dom = np.where(mx>=energy_min, dom, -1)
    return dom

def detect_shell_jumps(dom_idx: np.ndarray, freqs: np.ndarray, min_gap: int=1):
    """Return list of (t, old_idx, new_idx, delta_log2) for changes in dominant shell.
    delta_log2 = log2(f_new/f_old) using representative band center frequencies.
    """
    centers = np.sqrt(freqs[:-1]*freqs[1:])
    jumps = []
    last = dom_idx[0]
    last_t = 0
    for t, k in enumerate(dom_idx[1:], start=1):
        if k != last and k>=0 and last>=0 and (t-last_t)>=min_gap:
            d = np.log2(centers[k] / centers[last])
            jumps.append((t, int(last), int(k), float(np.round(d, 3))))
            last_t = t
        if k>=0:
            last = k
    return jumps
