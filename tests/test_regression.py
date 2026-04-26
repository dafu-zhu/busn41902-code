"""Tests for busn41902.regression.ols.

The reference β for big2 is captured once via np.linalg.inv on the
data and frozen as _REFERENCE_BETA_LINEAR. The frozen value pins
reproducibility — any future change to ols, load_big2, or the data
will break the test.
"""

import numpy as np

from busn41902.data import load_big2
from busn41902.regression import ols

# Captured 2026-04-25 via np.linalg.inv(X.T @ X) @ X.T @ y on big2.mat;
# pins reproducibility against future ols / load_big2 changes.
_REFERENCE_BETA_LINEAR = np.array([4.99509707, 0.07085730])


def test_ols_recovers_synthetic_beta():
    rng = np.random.default_rng(0)
    n, k = 500, 3
    X = np.column_stack([np.ones(n), rng.standard_normal((n, k - 1))])
    true_beta = np.array([1.5, -2.0, 0.7])
    y = X @ true_beta + 0.01 * rng.standard_normal(n)

    beta = ols(X, y)

    assert beta.shape == (k,)
    assert np.allclose(beta, true_beta, rtol=1e-2)


def test_ols_matches_reference_on_big2():
    y, d = load_big2()
    X = np.column_stack([np.ones(len(d)), d])

    beta = ols(X, y)

    assert np.allclose(beta, _REFERENCE_BETA_LINEAR, rtol=1e-6)
