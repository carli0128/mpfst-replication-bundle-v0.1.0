import numpy as np
from sklearn.decomposition import PCA

def participation_ratio(singular_values: np.ndarray) -> float:
    s2 = (singular_values**2)
    return float((s2.sum()**2) / ( (s2**2).sum() + 1e-12))

def low_rank_collapse(X: np.ndarray, k: int|None=None):
    pca = PCA(n_components=min(X.shape))
    pca.fit(X)
    pr = participation_ratio(pca.singular_values_)
    return {"pr": pr, "singular_values": pca.singular_values_}
