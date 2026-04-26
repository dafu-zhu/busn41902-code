# ---
# title: "L1 demo: Conditional mean by education category"
# format:
#   html:
#     code-fold: false
#     code-tools: true
# ---

# %% [markdown]
# # Conditional mean of log-wage by education category
#
# **Lecture reference:** §3 of `lec01.tex`, Slide L1.10 (*Conditional Mean*).
#
# The lecture defines $\E[y \mid w] = g(w)$ as the squared-error-optimal
# predictor. With *discrete* $w$, the population conditional expectation
# function reduces to within-group means. This page builds the empirical
# version on the AK census wage data: the mean of log-wage at each year
# of education, computed via OLS on a one-hot dummy design matrix.

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
# For a discrete control $w \in \{0, 1, \ldots, 20\}$, the population CEF
# $\E[y \mid w = k]$ is just the mean of $y$ within the subpopulation with
# $w = k$. The sample analog is
# $$\widehat{m}_k = \frac{1}{n_k} \sum_{i: d_i = k} y_i,$$
# which can be written equivalently as the OLS coefficient vector when $X$
# is the $n \times 21$ matrix of one-hot dummies for $d \in \{0, \ldots, 20\}$.

# %% [markdown]
# ## §2. Implementation walkthrough {#sec-impl}
#
# Build the dummy matrix $D \in \{0, 1\}^{n \times 21}$ where
# $D_{i,k} = \mathbf{1}[d_i = k]$, then solve the normal equations
# $D'D \widehat{m} = D' y$.
#
# Note that $D'D$ is diagonal — its $(k, k)$ entry is the count
# $n_k$ of observations with $d = k$ — and $D'y$ has entries
# $\sum_{i: d_i = k} y_i$. So the OLS solution recovers exactly the
# group-mean formula above.

# %%
def conditional_mean_by_bin(d, y, K):
    """Per-bin sample mean of *y* over integer bins of *d*, computed via OLS.

    Equivalent to ``[y[d == k].mean() for k in range(K)]`` but expressed as
    a single ``np.linalg.solve`` to make the algebraic equivalence with
    OLS explicit.
    """
    n = len(d)
    D = np.zeros((n, K))
    D[np.arange(n), d.astype(int)] = 1.0
    # D'D is diagonal with entries n_k; D'y has entries sum_{i: d_i=k} y_i.
    # solve(D'D, D'y) recovers the group means n_k^{-1} sum y_i.
    return np.linalg.solve(D.T @ D, D.T @ y)


# %% [markdown]
# ## §3. Numerical demonstration {#sec-demo}

# %%
y, d = load_big2()
K = int(d.max()) + 1
print(f"n = {len(d):,}; education bins = 0..{K - 1}")
meanw = conditional_mean_by_bin(d, y, K)
for k in range(K):
    print(f"  d = {k:2d}: mean log-wage = {meanw[k]:.4f} (n_k = {(d == k).sum():,})")

# %%
#| label: fig-cond-mean-boxplot
#| fig-cap: "Distribution of log-wage by education year on the AK data."

fig, ax = plt.subplots(figsize=(10, 4))
ax.boxplot(
    [y[d == k] for k in range(K)],
    positions=range(K),
    showfliers=False,
    widths=0.6,
    patch_artist=True,
    boxprops=dict(facecolor="lightblue", color="steelblue"),
    medianprops=dict(color="firebrick", linewidth=1.5),
)
ax.set_xlabel("Years of education")
ax.set_ylabel("Log(wage)")
ax.set_title("Boxplot of log-wage by education")
save_figure(fig, "cond_mean_boxplot", HERE)
plt.show()

# %%
#| label: fig-cond-mean
#| fig-cap: "Per-year conditional mean of log-wage on the AK data."

rng = np.random.default_rng(0)
idx = rng.choice(len(d), size=5_000, replace=False)

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(d[idx], y[idx], s=4, alpha=0.15, color="gray", label="AK data (5k subsample)")
ax.plot(np.arange(K), meanw, "o-", color="steelblue", linewidth=2, markersize=6,
        label="Conditional mean by education")
ax.set_xlabel("Years of education")
ax.set_ylabel("Log(wage)")
ax.legend()
save_figure(fig, "cond_mean", HERE)
plt.show()
