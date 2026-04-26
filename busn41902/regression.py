"""Regression estimators for BUSN 41902."""

import numpy as np


def ols(X, y):
    """β̂ = (X'X)⁻¹ X'y, computed via np.linalg.solve.

    Parameters
    ----------
    X : ndarray, shape (n, k)
        Design matrix.
    y : ndarray, shape (n,)
        Response.

    Returns
    -------
    beta : ndarray, shape (k,)

    Notes
    -----
    Implemented as ``np.linalg.solve(X.T @ X, X.T @ y)`` rather than
    ``np.linalg.inv(X.T @ X) @ X.T @ y`` — ``solve`` factors X'X once
    via LU decomposition, which is numerically more stable and ~2× faster
    than computing the inverse explicitly. See INCONSISTENCIES INC-001.

    MATLAB origin: ``inv(X'*X)*(X'*y)`` (e.g. AKMeanExample.m:25).
    """
    return np.linalg.solve(X.T @ X, X.T @ y)
