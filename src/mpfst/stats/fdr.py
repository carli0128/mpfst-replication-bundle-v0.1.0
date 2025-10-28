import numpy as np

def bh_fdr(pvals, alpha=0.05):
    p = np.sort(np.asarray(pvals))
    m = len(p)
    thresh = alpha * np.arange(1, m+1)/m
    k = np.where(p<=thresh)[0]
    return int(k.max()+1) if len(k)>0 else 0
