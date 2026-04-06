"""Tests for OpenAIClient."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from jupyter_base.services.openai_client import OpenAIClient


def test_openai_client_uses_default_model_from_env(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text(
        "OPENAI_API_KEY=sk-test\nJUPYTER_BASE_OPENAI_MODEL=gpt-4o\n",
        encoding="utf-8",
    )
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock()]
    mock_resp.choices[0].message.content = "ok"
    with patch("jupyter_base.services.openai_client.OpenAI") as mock_openai_cls:
        instance = MagicMock()
        instance.chat.completions.create.return_value = mock_resp
        mock_openai_cls.return_value = instance
        client = OpenAIClient(repo_root=tmp_path, env_file=env)
        assert client.complete_text(user="hi") == "ok"
        instance.chat.completions.create.assert_called_once()
        assert instance.chat.completions.create.call_args.kwargs["model"] == "gpt-4o"


def test_openai_client_complete_text(repo_root: Path, tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("OPENAI_API_KEY=sk-test\n", encoding="utf-8")
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock()]
    mock_resp.choices[0].message.content = "hello"
    with patch("jupyter_base.services.openai_client.OpenAI") as mock_openai_cls:
        instance = MagicMock()
        instance.chat.completions.create.return_value = mock_resp
        mock_openai_cls.return_value = instance
        client = OpenAIClient(repo_root=tmp_path, env_file=env)
        assert client.complete_text(user="hi", model="gpt-4o-mini") == "hello"
    mock_openai_cls.assert_called_once_with(api_key="sk-test")


def test_openai_client_exposes_sdk_namespaces(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("OPENAI_API_KEY=sk-test\n", encoding="utf-8")
    with patch("jupyter_base.services.openai_client.OpenAI") as mock_cls:
        inner = MagicMock()
        mock_cls.return_value = inner
        client = OpenAIClient(repo_root=tmp_path, env_file=env)
        assert client.responses is inner.responses
        assert client.chat is inner.chat


def test_openai_client_missing_key(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("JUPYTER_BASE_APP_NAME=x\n", encoding="utf-8")
    try:
        OpenAIClient(repo_root=tmp_path, env_file=env)
    except ValueError as e:
        assert "OpenAI API key not configured" in str(e)
    else:
        raise AssertionError("expected ValueError")
