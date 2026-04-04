"""Tests for example workflow."""

from jupyter_base.services.workflow import run_example_pipeline


def test_run_example_pipeline(sample_settings) -> None:
    result = run_example_pipeline(sample_settings, "My Topic!")
    assert result.label == "demo:my-topic"
    assert result.success is True
