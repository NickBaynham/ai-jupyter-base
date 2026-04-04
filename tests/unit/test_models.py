"""Tests for core models."""

from jupyter_base.core.models import PipelineResult, TaskSummary


def test_pipeline_success() -> None:
    r = PipelineResult(
        label="x",
        tasks=[TaskSummary(name="a", ok=True), TaskSummary(name="b", ok=True)],
    )
    assert r.success is True
    d = r.to_dict()
    assert d["label"] == "x"
    assert d["success"] is True
    assert len(d["tasks"]) == 2


def test_pipeline_failure() -> None:
    r = PipelineResult(label="x", tasks=[TaskSummary(name="a", ok=False)])
    assert r.success is False
