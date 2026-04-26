# ---
# title: "L1 demo: Cubic-spline basis on the AK wage data"
# format:
#   html:
#     code-fold: false
#     code-tools: true
# ---

# %% [markdown]
# # Cubic-spline basis for nonparametric regression on the AK data
#
# **Lecture reference:** §3 of `lec01.tex`, Slide L1.13 answer (3)
# (*Nonparametric Regression*).
#
# The lecture's third answer to "why OLS?" is that with a rich enough
# basis, the linear predictor $x_i^{K\prime}\beta$ approximates the true
# CEF arbitrarily well as $K \to \infty$ (Newey 1997). This page
# instantiates that idea: a cubic spline with knots at $\{12, 16\}$ on
# the AK wage data, fit by OLS on a $K = 6$-column basis matrix.

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from busn41902._io import save_figure
from busn41902.data import load_big2
from busn41902.regression import ols

HERE = Path(__file__).resolve().parent
np.random.seed(0)

# %% [markdown]
# ## §1. Methodology recap {#sec-recap}
#
# The linear predictor's basis is
# $x_i^K = (1, d_i, d_i^2, d_i^3, b_{12}(d_i), b_{16}(d_i))$
# where $b_k(d)$ is a cubic-spline basis function with knot at $k$.
# OLS recovers the projection of $\E[y \mid d]$ onto this $K = 6$-dim
# linear span.

# %% [markdown]
# ## §2. Implementation walkthrough {#sec-impl}
#
# We build the basis matrix inline — basis construction is the lesson of
# this demo, not an abstraction to hide. The OLS solve is then a single
# call to `busn41902.regression.ols`, defined inline in `demo_ols.py`.
#
# **Truncation direction.** The MATLAB source
# (`AKMeanExample.m:32`) uses
# $b_k(d) = ((d - k) \cdot \mathbf{1}[d \le k])^3$ — non-zero *below* the
# knot, zero above. The standard textbook truncated-power form is
# $b_k(d) = (d - k)_+^3 = \max(d - k, 0)^3$ — non-zero *above* the knot.
# Both span the same $C^2$ cubic-spline space with breakpoints at
# $\{12, 16\}$; fitted curves are identical, only the coefficients differ.
# We mirror MATLAB so the verification test compares β coefficient-by-
# coefficient against the reference. Logged as `INC-002` (`cosmetic`).

# %%
def cubic_spline_basis_matrix(d, knots=(12, 16)):
    """Build the $n \\times 6$ truncated-power basis matrix matching MATLAB.

    Inline construction (rather than a package helper) because the basis
    construction *is* the lesson of this demo. See the §2 markdown for
    the truncation-direction note.
    """
    cols = [np.ones_like(d, dtype=float), d.astype(float),
            d.astype(float) ** 2, d.astype(float) ** 3]
    for k in knots:
        cols.append(((d - k) * (d <= k)) ** 3)
    return np.column_stack(cols)


# %% [markdown]
# ## §3. Numerical demonstration {#sec-demo}

# %%
y, d = load_big2()
K = int(d.max()) + 1
Xs = cubic_spline_basis_matrix(d, knots=(12, 16))
bb = ols(Xs, y)
print(f"n = {len(d):,}; basis columns = {Xs.shape[1]}")
print("β̂ (spline) =", np.array2string(bb, precision=6))

# Evaluate the spline curve on the integer education grid.
dd = np.arange(K)
xs_grid = cubic_spline_basis_matrix(dd, knots=(12, 16))
spline_curve = xs_grid @ bb

# %%
#| label: fig-spline
#| fig-cap: "Cubic-spline curve (knots at 12, 16) over the AK wage scatter."

rng = np.random.default_rng(0)
idx = rng.choice(len(d), size=5_000, replace=False)

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(d[idx], y[idx], s=4, alpha=0.15, color="gray", label="AK data (5k subsample)")
ax.plot(dd, spline_curve, color="seagreen", linewidth=2, label="Cubic spline (knots 12, 16)")
ax.set_xlabel("Years of education")
ax.set_ylabel("Log(wage)")
ax.legend()
save_figure(fig, "spline_curve", HERE)
plt.show()

# %% [markdown]
# ### Comparison: conditional mean vs. OLS line vs. spline
#
# All three predictors of $\E[\log\text{wage} \mid \text{educ}]$ overlaid
# on the same scatter. Each curve is recomputed inline below so this
# demo is self-contained for Quarto rendering.

# %%
# Conditional means (one-hot dummy OLS).
n = len(d)
D = np.zeros((n, K))
D[np.arange(n), d.astype(int)] = 1.0
meanw = np.linalg.solve(D.T @ D, D.T @ y)

# OLS line.
X1 = np.column_stack([np.ones(n), d])
beta_linear = ols(X1, y)
ols_line = beta_linear[0] + beta_linear[1] * dd

# Spline curve already computed above as `spline_curve`.

# %%
#| label: fig-comparison
#| fig-cap: "Three predictors of $\\E[\\log\\text{wage} \\mid \\text{educ}]$ overlaid on the AK data: per-year conditional means (blue), OLS BLP line (red dashed), cubic spline with knots 12, 16 (green)."

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(d[idx], y[idx], s=4, alpha=0.12, color="gray", label="AK data (5k subsample)")
ax.plot(dd, meanw, "o-", color="steelblue", linewidth=2, markersize=6,
        label="Conditional mean by education")
ax.plot(dd, ols_line, color="firebrick", linestyle="--", linewidth=2,
        label="OLS line")
ax.plot(dd, spline_curve, color="seagreen", linewidth=2,
        label="Cubic spline (knots 12, 16)")
ax.set_xlabel("Years of education")
ax.set_ylabel("Log(wage)")
ax.legend(loc="upper left", fontsize=10)
save_figure(fig, "comparison_overlay", HERE)
plt.show()
