import numpy as np

def time_shuffle(x: np.ndarray, block: int=256, seed: int|None=None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = len(x)
    blocks = [x[i:i+block] for i in range(0, n, block)]
    rng.shuffle(blocks)
    return np.concatenate(blocks)[:n]
