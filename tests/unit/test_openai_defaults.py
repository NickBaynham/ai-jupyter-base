"""Tests for OpenAI default model resolution."""

from __future__ import annotations

from pathlib import Path

import pytest

from jupyter_base.config.openai_defaults import (
    DEFAULT_OPENAI_CHAT_MODEL,
    resolve_default_openai_chat_model,
)


def test_resolve_default_model_from_dotenv(repo_root: Path, tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("JUPYTER_BASE_OPENAI_MODEL=gpt-4o\n", encoding="utf-8")
    assert (
        resolve_default_openai_chat_model(repo_root=repo_root, env_file=env) == "gpt-4o"
    )


def test_resolve_default_model_env_overrides_dotenv(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    env = tmp_path / ".env"
    env.write_text("JUPYTER_BASE_OPENAI_MODEL=gpt-4o\n", encoding="utf-8")
    monkeypatch.setenv("JUPYTER_BASE_OPENAI_MODEL", "gpt-4o-mini")
    assert (
        resolve_default_openai_chat_model(repo_root=repo_root, env_file=env)
        == "gpt-4o-mini"
    )


def test_resolve_default_model_fallback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("JUPYTER_BASE_OPENAI_MODEL", raising=False)
    env = tmp_path / ".env"
    env.write_text("OPENAI_API_KEY=x\n", encoding="utf-8")
    assert (
        resolve_default_openai_chat_model(repo_root=tmp_path, env_file=env)
        == DEFAULT_OPENAI_CHAT_MODEL
    )
