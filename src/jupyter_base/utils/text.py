"""Text utilities."""

from __future__ import annotations

import re


def slugify(value: str) -> str:
    """Lowercase alphanumeric slug with hyphens (empty string if no alnum)."""
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip()).strip("-").lower()
    return cleaned
