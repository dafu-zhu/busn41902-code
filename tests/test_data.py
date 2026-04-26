"""Smoke tests for busn41902.data loaders."""

import numpy as np

from busn41902.data import load_big2


def test_load_big2_returns_two_1d_arrays_with_d_nonnegative():
    y, d = load_big2()

    assert y.ndim == 1
    assert d.ndim == 1
    assert y.shape == d.shape
    assert y.shape[0] > 0
    assert (d >= 0).all()
    assert np.issubdtype(y.dtype, np.floating)
    # d is integer-valued years of education; may be stored as int or float.
    # Verify it round-trips to integer.
    assert np.allclose(d, np.round(d))
