#!/usr/bin/env python3
"""Fail a trusted release build when externally supplied prohibited terms appear.

Keep the terms themselves out of the public repository. Set SKILLIR_NEUTRALITY_TERMS
to a comma-separated private release list in trusted CI or before publication.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> int:
    terms = [item.strip().lower() for item in os.environ.get("SKILLIR_NEUTRALITY_TERMS", "").split(",") if item.strip()]
    if not terms:
        print("neutrality scan skipped: SKILLIR_NEUTRALITY_TERMS is unset")
        return 0
    root = Path(__file__).resolve().parents[1]
    ignored = {".git", ".venv", "build", "dist", "__pycache__"}
    violations: list[str] = []
    for path in root.rglob("*"):
        if any(part in ignored for part in path.parts) or not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8").lower()
        except UnicodeDecodeError:
            continue
        if any(term in content for term in terms):
            violations.append(str(path.relative_to(root)))
    if violations:
        print("neutrality scan failed: prohibited private term found in " + ", ".join(violations), file=sys.stderr)
        return 1
    print("neutrality scan passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
