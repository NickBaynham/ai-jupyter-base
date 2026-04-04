"""Load typed settings from the environment (and optional `.env` file)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _default_repo_root() -> Path:
    """Resolve repository root (directory containing `pyproject.toml`)."""
    here = Path(__file__).resolve()
    for parent in (here.parent, *here.parents):
        if (parent / "pyproject.toml").is_file():
            return parent
    return here.parents[3]


@dataclass(frozen=True)
class AppSettings:
    """Application settings derived from environment variables."""

    app_name: str
    environment: str
    debug: bool
    data_dir: Path


def load_settings(*, env_file: Path | None = None, repo_root: Path | None = None) -> AppSettings:
    """Load settings, optionally reading `env_file` into the process environment."""
    root = repo_root or _default_repo_root()
    path = env_file if env_file is not None else root / ".env"
    if path.is_file():
        load_dotenv(path)
    data_default = root / "data"
    data_raw = os.getenv("JUPYTER_BASE_DATA_DIR", str(data_default))
    return AppSettings(
        app_name=os.getenv("JUPYTER_BASE_APP_NAME", "jupyter-base"),
        environment=os.getenv("JUPYTER_BASE_ENV", "development"),
        debug=os.getenv("JUPYTER_BASE_DEBUG", "").lower() in ("1", "true", "yes"),
        data_dir=Path(data_raw).expanduser().resolve(),
    )
