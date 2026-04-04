"""Structured results for notebook-friendly APIs."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class TaskSummary:
    """Single step in a pipeline."""

    name: str
    ok: bool
    detail: str = ""


@dataclass
class PipelineResult:
    """Aggregate outcome with metadata notebooks can display or log."""

    label: str
    tasks: list[TaskSummary] = field(default_factory=list)
    finished_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))

    @property
    def success(self) -> bool:
        return all(t.ok for t in self.tasks)

    def to_dict(self) -> dict[str, object]:
        return {
            "label": self.label,
            "success": self.success,
            "finished_at": self.finished_at.isoformat(),
            "tasks": [{"name": t.name, "ok": t.ok, "detail": t.detail} for t in self.tasks],
        }
