"""Repository layout helpers."""

from __future__ import annotations

from pathlib import Path


def default_repo_root() -> Path:
    """Resolve repository root (directory containing `pyproject.toml`)."""
    here = Path(__file__).resolve()
    for parent in (here.parent, *here.parents):
        if (parent / "pyproject.toml").is_file():
            return parent
    return here.parents[3]
