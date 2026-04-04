"""Load typed settings from the environment (and optional `.env` file)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from jupyter_base.config.env_lookup import load_env_file_dict, lookup_env
from jupyter_base.config.paths import default_repo_root


@dataclass(frozen=True)
class AppSettings:
    """Application settings derived from environment variables."""

    app_name: str
    environment: str
    debug: bool
    data_dir: Path


def load_settings(*, env_file: Path | None = None, repo_root: Path | None = None) -> AppSettings:
    """Load settings from the process environment and optional dotenv file.

    Dotenv values are merged the same way as ``load_dotenv(override=False)``, but
    keys from the file are **not** written into ``os.environ``. That keeps values
    such as ``OPENAI_API_KEY`` (when stored only in ``.env``) out of the process
    environment so notebooks cannot read them via ``os.environ``.
    """
    root = repo_root or default_repo_root()
    path = env_file if env_file is not None else root / ".env"
    file_values = load_env_file_dict(path)
    data_default = root / "data"
    data_raw = lookup_env(file_values, "JUPYTER_BASE_DATA_DIR", str(data_default))
    data_path = data_raw if data_raw is not None else str(data_default)
    debug_raw = lookup_env(file_values, "JUPYTER_BASE_DEBUG", "") or ""
    return AppSettings(
        app_name=lookup_env(file_values, "JUPYTER_BASE_APP_NAME", "jupyter-base") or "jupyter-base",
        environment=lookup_env(file_values, "JUPYTER_BASE_ENV", "development") or "development",
        debug=debug_raw.lower() in ("1", "true", "yes"),
        data_dir=Path(data_path).expanduser().resolve(),
    )
