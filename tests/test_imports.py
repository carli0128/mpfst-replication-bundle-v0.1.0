def test_imports():
    import mpfst
    from mpfst.coherence import metrics, meter
    from mpfst.spectral import ssm, octave_jump
    from mpfst.fractional import inversion, response
    assert hasattr(mpfst, "__version__")
