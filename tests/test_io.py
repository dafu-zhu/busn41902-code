"""Tests for busn41902._io.save_figure."""

from pathlib import Path

import matplotlib.pyplot as plt

from busn41902._io import save_figure


def test_save_figure_creates_pdf_under_base_dir(tmp_path: Path) -> None:
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])

    out = save_figure(fig, "smoke", tmp_path)

    assert out == tmp_path / "figures" / "smoke.pdf"
    assert out.is_file()
    assert out.stat().st_size > 0
    plt.close(fig)


def test_save_figure_creates_figures_dir_if_missing(tmp_path: Path) -> None:
    fig, _ = plt.subplots()
    target_dir = tmp_path / "L7"
    target_dir.mkdir()

    out = save_figure(fig, "x", target_dir)

    assert out.parent.name == "figures"
    assert out.parent.is_dir()
    assert out.is_file()
    assert out.stat().st_size > 0
    plt.close(fig)
