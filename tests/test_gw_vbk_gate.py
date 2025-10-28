from mpfst.domains.gw_superradiance import BHParams, superradiance_overlap, omega_c, mu0
from mpfst.gating.linear_response import evaluate

def test_vbk_overlap_highspin():
    p = BHParams(M=1.0, a=0.9, Q=0.0, m=1, q=0.0, mu=0.05)
    assert omega_c(p) > p.mu
    assert mu0(p) == 0.0
    assert superradiance_overlap(p) is True
    g,w = evaluate('gw_vbk', M=1.0, a=0.9, Q=0.0, m=1, q=0.0, mu=0.05, C=1.0)
    assert g is True and w > 0.0
