# ---
# title: "L? demo: <method name>"
# format:
#   html:
#     code-fold: false
#     code-tools: true
# ---

# %% [markdown]
# # <method name>
#
# **Lecture reference:** §X.Y of `lecNN.tex`.
#
# This page is the implementation companion to the derivation in the lecture
# note. The lecture proves *why* the method works; here we show *how* it is
# computed and *how it behaves* on a concrete dataset.

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from busn41902._io import save_figure
# from busn41902.<module> import <fn>     # uncomment per-demo

HERE = Path(__file__).parent
np.random.seed(0)

# %% [markdown]
# ## §1 — Methodology recap
#
# *(Terse statement of the result the lecture proved. No derivation.
# Link back to the lecture's section.)*

# %% [markdown]
# ## §2 — Implementation walkthrough
#
# *(Step-by-step exposition of the code. When a primitive library function
# is introduced for the first time, hyperlink it to its canonical doc.)*

# %%
# (code chunks, alternating with markdown cells)

# %% [markdown]
# ## §3 — Numerical demonstration
#
# *(Concrete worked example. Figures saved with ``save_figure(fig, name, HERE)``
# to ``./figures/<name>.pdf``; Quarto captures the inline render automatically.)*

# %%
# (demo code that produces figures + tables)
