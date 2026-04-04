"""Reusable backend library for Jupyter-Base notebooks and services."""

from jupyter_base.config.settings import AppSettings, load_settings
from jupyter_base.core.models import PipelineResult, TaskSummary
from jupyter_base.services.openai_client import OpenAIClient
from jupyter_base.services.workflow import run_example_pipeline
from jupyter_base.utils.text import slugify

__all__ = [
    "AppSettings",
    "OpenAIClient",
    "PipelineResult",
    "TaskSummary",
    "__version__",
    "load_settings",
    "run_example_pipeline",
    "slugify",
]
__version__ = "0.1.0"
