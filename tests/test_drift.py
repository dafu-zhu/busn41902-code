"""Source-equality check between the inline `# @save` function definitions
in the L1 demos and their package mirrors in busn41902/.

The d2l.ai pattern has each method's canonical body live inline in the
demo where it first appears (visually marked `# @save`); the `busn41902/`
package mirrors the body verbatim so later demos can import the helper.
This test catches drift between the two.
"""

import ast
import inspect
import re
from pathlib import Path

import busn41902.regression


def _extract_function_source(file_path: Path, name: str) -> str:
    text = file_path.read_text()
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(text, node)
    raise AssertionError(f"function {name!r} not found in {file_path}")


_SAVE_MARKER = re.compile(r"\s*#\s*@save\s*$")


def _normalize(src: str) -> str:
    """Strip the `# @save` marker (any whitespace before/around it) so that
    demo and package versions compare equal regardless of formatter changes
    to the inline-comment spacing."""
    return "\n".join(_SAVE_MARKER.sub("", line).rstrip() for line in src.splitlines()).strip()


def test_ols_inline_matches_package_mirror():
    repo_root = Path(__file__).resolve().parent.parent
    demo_path = repo_root / "L1" / "demo_ols.py"

    inline_src = _extract_function_source(demo_path, "ols")
    package_src = inspect.getsource(busn41902.regression.ols)

    assert _normalize(inline_src) == _normalize(package_src), (
        "demo_ols.py's inline `ols` has drifted from busn41902.regression.ols. "
        "Update both to the same body."
    )
