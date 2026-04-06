"""Defaults for OpenAI usage (non-secret)."""

from __future__ import annotations

from pathlib import Path

from jupyter_base.config.env_lookup import load_env_file_dict, lookup_env
from jupyter_base.config.paths import default_repo_root

DEFAULT_OPENAI_CHAT_MODEL = "gpt-4o-mini"


def resolve_default_openai_chat_model(
    *,
    repo_root: Path | None = None,
    env_file: Path | None = None,
) -> str:
    """Return the default chat model from env / dotenv, or ``DEFAULT_OPENAI_CHAT_MODEL``.

    Reads ``JUPYTER_BASE_OPENAI_MODEL`` using the same merge rules as
    ``lookup_env`` (process environment overrides dotenv file). Empty values are
    ignored.
    """
    root = repo_root or default_repo_root()
    path = env_file if env_file is not None else root / ".env"
    file_values = load_env_file_dict(path)
    raw = lookup_env(file_values, "JUPYTER_BASE_OPENAI_MODEL")
    if raw and str(raw).strip():
        return str(raw).strip()
    return DEFAULT_OPENAI_CHAT_MODEL
