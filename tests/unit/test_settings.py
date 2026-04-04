"""Tests for environment-backed settings."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from jupyter_base.config.settings import load_settings


def test_load_settings_reads_env_file(repo_root: Path, tmp_path: Path) -> None:
    env = tmp_path / "custom.env"
    env.write_text(
        "JUPYTER_BASE_APP_NAME=from-file\n"
        "JUPYTER_BASE_DEBUG=true\n"
        f"JUPYTER_BASE_DATA_DIR={tmp_path / 'd'}\n",
        encoding="utf-8",
    )
    s = load_settings(env_file=env, repo_root=repo_root)
    assert s.app_name == "from-file"
    assert s.debug is True
    assert s.data_dir == (tmp_path / "d").resolve()


def test_load_settings_does_not_inject_openai_into_environ(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    env = tmp_path / "custom.env"
    env.write_text(
        "JUPYTER_BASE_APP_NAME=app\n"
        f"JUPYTER_BASE_DATA_DIR={tmp_path / 'd'}\n"
        "OPENAI_API_KEY=secret-from-dotenv\n",
        encoding="utf-8",
    )
    load_settings(env_file=env, repo_root=repo_root)
    assert os.environ.get("OPENAI_API_KEY") is None
