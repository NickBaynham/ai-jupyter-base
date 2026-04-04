"""Tests for text helpers."""

from jupyter_base.utils.text import slugify


def test_slugify_basic() -> None:
    assert slugify("Hello World") == "hello-world"


def test_slugify_strips_noise() -> None:
    assert slugify("  Foo!!! Bar  ") == "foo-bar"
