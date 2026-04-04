"""Tests for OpenAI API key resolution."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from jupyter_base.config.openai_key import resolve_openai_api_key


def test_resolve_from_key_file(repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    key_file = tmp_path / "k.txt"
    key_file.write_text("sk-from-file\n", encoding="utf-8")
    env = tmp_path / ".env"
    env.write_text(f"JUPYTER_BASE_OPENAI_KEY_FILE={key_file}\n", encoding="utf-8")
    assert resolve_openai_api_key(repo_root=repo_root, env_file=env) == "sk-from-file"


def test_resolve_key_file_relative_to_repo(repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    secrets = tmp_path / ".secrets"
    secrets.mkdir()
    (secrets / "k").write_text("sk-rel\n", encoding="utf-8")
    env = tmp_path / ".env"
    env.write_text("JUPYTER_BASE_OPENAI_KEY_FILE=.secrets/k\n", encoding="utf-8")
    assert resolve_openai_api_key(repo_root=tmp_path, env_file=env) == "sk-rel"


def test_resolve_openai_from_env_var(repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    env = tmp_path / ".env"
    env.write_text("OPENAI_API_KEY=should-not-use-when-env-set\n", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-from-environ")
    assert resolve_openai_api_key(repo_root=repo_root, env_file=env) == "sk-from-environ"


def test_resolve_openai_from_dotenv_only(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    env = tmp_path / ".env"
    env.write_text("OPENAI_API_KEY=sk-from-dotenv\n", encoding="utf-8")
    assert resolve_openai_api_key(repo_root=repo_root, env_file=env) == "sk-from-dotenv"
    assert os.environ.get("OPENAI_API_KEY") is None
