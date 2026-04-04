"""Resolve the OpenAI API key without requiring it to appear in `os.environ`."""

from __future__ import annotations

import os
from pathlib import Path

from jupyter_base.config.env_lookup import load_env_file_dict, lookup_env
from jupyter_base.config.paths import default_repo_root


def resolve_openai_api_key(
    *,
    repo_root: Path | None = None,
    env_file: Path | None = None,
) -> str | None:
    """Return the API key, or None if not configured.

    Resolution order:

    1. File at ``JUPYTER_BASE_OPENAI_KEY_FILE`` (from the environment or the
       dotenv file), with paths relative to the repo root resolved under that root.
    2. ``OPENAI_API_KEY`` in the process environment (typical for CI or shells).
    3. ``OPENAI_API_KEY`` in the dotenv file only (never injected into ``os.environ``).
    """
    root = repo_root or default_repo_root()
    path = env_file if env_file is not None else root / ".env"
    file_values = load_env_file_dict(path)

    key_file_raw = lookup_env(file_values, "JUPYTER_BASE_OPENAI_KEY_FILE")
    if key_file_raw:
        key_path = Path(key_file_raw).expanduser()
        if not key_path.is_absolute():
            key_path = (root / key_path).resolve()
        if key_path.is_file():
            line = key_path.read_text(encoding="utf-8").strip().splitlines()
            if line and line[0].strip():
                return line[0].strip()

    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    file_key = file_values.get("OPENAI_API_KEY")
    if file_key and str(file_key).strip():
        return str(file_key).strip()

    return None
