"""Small, dependency-free frontmatter parser for the Skill IR authoring contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip('"\'') for item in value[1:-1].split(",") if item.strip()]
    return value.strip('"\'')


def parse(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Unterminated YAML frontmatter; close it with a standalone '---'.")
    raw, body = text[4:end], text[end + 5 :]
    data: dict[str, Any] = {}
    active_list: str | None = None
    for number, line in enumerate(raw.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            if active_list is None:
                raise ValueError(f"Frontmatter line {number}: list item has no key.")
            data.setdefault(active_list, []).append(_scalar(stripped[2:]))
            continue
        if ":" not in line:
            raise ValueError(f"Frontmatter line {number}: expected key: value.")
        key, value = line.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Frontmatter line {number}: key is empty.")
        value = value.strip()
        if value:
            data[key] = _scalar(value)
            active_list = None
        else:
            data[key] = []
            active_list = key
    return data, body.lstrip("\n")


def load(path: Path) -> tuple[dict[str, Any], str]:
    return parse(path.read_text(encoding="utf-8"))
