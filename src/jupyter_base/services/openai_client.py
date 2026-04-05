"""OpenAI access for notebooks without exposing credentials."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from openai import OpenAI
from openai.types.chat import ChatCompletion

from jupyter_base.config.openai_key import resolve_openai_api_key


class OpenAIClient:
    """Resolve the API key internally and delegate to the OpenAI SDK.

    Prefer this over constructing ``openai.OpenAI`` in notebooks so the key can
    live in ``.env`` or a key file without being copied into cells or left in
    ``os.environ`` (when you use a key file and start Jupyter with
    ``OPENAI_API_KEY`` unset).

    Use :attr:`responses` for the `Responses API <https://platform.openai.com/docs/api-reference/responses>`_
    (``client.responses.create(...)``), or :meth:`chat_completion` / :meth:`complete_text`
    for chat completions.
    """

    __slots__ = ("_client",)

    def __init__(
        self,
        *,
        repo_root: Path | None = None,
        env_file: Path | None = None,
        api_key: str | None = None,
    ) -> None:
        key = api_key or resolve_openai_api_key(repo_root=repo_root, env_file=env_file)
        if not key:
            msg = (
                "OpenAI API key not configured. Use one of: OPENAI_API_KEY in the "
                "environment; OPENAI_API_KEY in .env (read by this package without "
                "exporting to os.environ); or JUPYTER_BASE_OPENAI_KEY_FILE pointing "
                "to a file whose first line is the key. For kernels without "
                "OPENAI_API_KEY in the environment, use a key file and "
                "`make run-jupyter JUPYTER_STRIP_OPENAI_ENV=1`."
            )
            raise ValueError(msg)
        self._client = OpenAI(api_key=key)

    @property
    def responses(self) -> Any:
        """Same as ``OpenAI(...).responses`` — create calls via ``.create()``."""
        return self._client.responses

    @property
    def chat(self) -> Any:
        """Underlying ``chat`` namespace (e.g. ``client.chat.completions.create``)."""
        return self._client.chat

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def chat_completion(
        self,
        *,
        messages: Sequence[Mapping[str, Any]],
        model: str = "gpt-4o-mini",
        **kwargs: Any,
    ) -> ChatCompletion:
        """Call ``chat.completions.create``; returns the SDK response object."""
        return self._client.chat.completions.create(
            model=model,
            messages=[dict(m) for m in messages],  # type: ignore[misc]
            **kwargs,
        )

    def complete_text(
        self,
        *,
        user: str,
        model: str = "gpt-4o-mini",
        system: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Single-turn chat; returns assistant message text (empty string if none)."""
        msgs: list[dict[str, str]] = []
        if system is not None:
            msgs.append({"role": "system", "content": system})
        msgs.append({"role": "user", "content": user})
        resp = self.chat_completion(messages=msgs, model=model, **kwargs)
        content = resp.choices[0].message.content
        return content or ""
