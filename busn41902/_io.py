"""I/O helpers for demos."""

from pathlib import Path

from matplotlib.figure import Figure


def save_figure(fig: Figure, name: str, base_dir: Path) -> Path:
    """Save a matplotlib figure as PDF under ``{base_dir}/figures/{name}.pdf``.

    Demos pass ``base_dir = Path(__file__).parent`` so the path is bound
    to the demo file's own location, independent of the CWD that ``python``
    or ``quarto render`` happens to run from.

    Parameters
    ----------
    fig
        Matplotlib figure to save.
    name
        Base filename (no extension); ``.pdf`` is appended.
    base_dir
        Directory whose ``figures/`` subdirectory receives the file.
        Created if it does not exist.

    Returns
    -------
    Path
        The path the file was written to.
    """
    out = base_dir / "figures" / f"{name}.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight")
    return out
