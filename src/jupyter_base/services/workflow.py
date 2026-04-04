"""Example workflow callable from notebooks or services."""

from __future__ import annotations

from jupyter_base.config.settings import AppSettings
from jupyter_base.core.models import PipelineResult, TaskSummary
from jupyter_base.utils.text import slugify


def run_example_pipeline(settings: AppSettings, topic: str) -> PipelineResult:
    """Demonstrate structured outputs and use of config + utilities."""
    slug = slugify(topic)
    tasks = [
        TaskSummary(name="load_settings", ok=True, detail=f"app={settings.app_name}"),
        TaskSummary(name="normalize_topic", ok=bool(slug), detail=slug),
        TaskSummary(
            name="environment",
            ok=settings.environment != "",
            detail=settings.environment,
        ),
    ]
    return PipelineResult(label=f"demo:{slug}", tasks=tasks)
