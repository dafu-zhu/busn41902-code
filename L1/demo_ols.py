# ---
# title: "L1 demo: OLS on the AK wage data"
# format:
#   html:
#     code-fold: false
#     code-tools: true
# ---

# %% [markdown]
# # OLS on the AK wage data
#
# **Lecture reference:** §3 of `lec01.tex`, Slides L1.14–L1.15
# (*Ordinary Least Squares: Algebra*).
#
# This page is the implementation companion to the OLS algebra derived in
# the lecture. The lecture proves *why* the BLP coefficient solves the
# normal equations; here we show *how* it is computed and *how it behaves*
# on the AK census wage data.

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from busn41902._io import save_figure
from busn41902.data import load_big2

HERE = Path(__file__).resolve().parent
np.random.seed(0)

# %% [markdown]
# ## §1. Methodology recap {#sec-recap}
#
# The lecture derives the OLS estimator as the sample analog of the
# population moment condition $\E[x_i \varepsilon_i] = 0$:
#
# $$\widehat{\beta}_n = \widehat{\E}[x_i x_i']^{-1}\,\widehat{\E}[x_i y_i]
# = (X'X)^{-1} X'y.$$
#
# Equivalently, $\widehat{\beta}_n = \arg\min_b \lVert y - Xb \rVert_2^2$.
# The closed form requires only that $X'X$ be invertible — no
# distributional assumption on the error.

# %% [markdown]
# ## §2. Implementation walkthrough {#sec-impl}
#
# Below is the canonical OLS solver used throughout this companion code.
# It is marked `# @save` in the [d2l.ai](https://zh.d2l.ai/) convention:
# this is the function's first appearance in the lecture-companion, and
# from L2 onward demos will `from busn41902.regression import ols` rather
# than redefine it. The body shown here is byte-identical to
# `busn41902.regression.ols` (enforced by `tests/test_drift.py`).


# %%
def ols(X, y):  # @save
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


# %% [markdown]
# Why
# [`np.linalg.solve`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html)
# rather than
# [`np.linalg.inv`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.inv.html)?
# `solve(A, b)` factors $A$ via LU decomposition once and back-substitutes
# to recover $A^{-1}b$, which is numerically more stable than forming
# $A^{-1}$ explicitly and then multiplying. The MATLAB source uses
# `inv(X'*X)*(X'*y)`; we standardize on `solve` repo-wide and log the
# choice as `INC-001` (`cosmetic`).

# %% [markdown]
# ## §3. Numerical demonstration {#sec-demo}
#
# Fit $\log\text{wage} = \beta_0 + \beta_1 \cdot \text{educ} + \varepsilon$
# on the AK census wage data and overlay the OLS line on the scatter.

# %%
y, d = load_big2()
X = np.column_stack([np.ones(len(d)), d])
beta = ols(X, y)
print(f"n = {len(d):,}")
print(f"β̂ = ({beta[0]:.6f}, {beta[1]:.6f})")

# %%
#| label: fig-ols-line
#| fig-cap: "OLS BLP line over the AK wage scatter (5 000-point subsample for legibility)."

rng = np.random.default_rng(0)
idx = rng.choice(len(d), size=5_000, replace=False)

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(d[idx], y[idx], s=4, alpha=0.15, color="gray", label="AK data (5k subsample)")
dd = np.arange(int(d.min()), int(d.max()) + 1)
ax.plot(
    dd,
    beta[0] + beta[1] * dd,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"OLS line: β̂ = ({beta[0]:.3f}, {beta[1]:.3f})",
)
ax.set_xlabel("Years of education")
ax.set_ylabel("Log(wage)")
ax.legend()
save_figure(fig, "ols_line", HERE)
plt.show()
