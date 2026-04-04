"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest

from jupyter_base.config.settings import AppSettings, load_settings


@pytest.fixture
def repo_root() -> Path:
    """Repository root (contains `pyproject.toml`)."""
    here = Path(__file__).resolve().parent
    for parent in (here, *here.parents):
        if (parent / "pyproject.toml").is_file():
            return parent
    raise RuntimeError("Could not locate repository root")


@pytest.fixture
def sample_settings(repo_root: Path, tmp_path: Path) -> AppSettings:
    """Isolated settings with a temp data directory."""
    env = tmp_path / ".env"
    env.write_text(
        "JUPYTER_BASE_APP_NAME=test-app\n"
        f"JUPYTER_BASE_DATA_DIR={tmp_path / 'data'}\n"
        "JUPYTER_BASE_ENV=testing\n",
        encoding="utf-8",
    )
    return load_settings(env_file=env, repo_root=repo_root)
