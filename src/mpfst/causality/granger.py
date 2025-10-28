import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests

def granger_pair(x, y, maxlag=5):
    import warnings
    warnings.filterwarnings("ignore")
    data = np.column_stack([y, x])  # test x->y
    res = grangercausalitytests(data, maxlag=maxlag, verbose=False)
    pvals = [res[lag][0]['ssr_ftest'][1] for lag in range(1, maxlag+1)]
    return float(min(pvals))
