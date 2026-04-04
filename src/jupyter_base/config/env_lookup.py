"""Read `.env` files without mutating `os.environ` (keeps secrets out of the process environment)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import dotenv_values


def load_env_file_dict(path: Path) -> dict[str, str | None]:
    """Parse a dotenv file into a dict; missing file yields an empty dict."""
    if not path.is_file():
        return {}
    return dict(dotenv_values(path))


def lookup_env(file_values: dict[str, str | None], key: str, default: str | None = None) -> str | None:
    """Match `load_dotenv(override=False)` semantics: process env wins, then file."""
    if key in os.environ:
        return os.environ[key]
    raw = file_values.get(key)
    if raw is not None and str(raw).strip() != "":
        return str(raw)
    return default
