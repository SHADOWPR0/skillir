#!/usr/bin/env python3
"""Verify that a built wheel contains the usable commons, not metadata alone."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path


def main() -> int:
    wheels = sorted(Path("dist").glob("skillir-*.whl"))
    if len(wheels) != 1:
        print(f"expected one Skill IR wheel in dist, found {len(wheels)}", file=sys.stderr)
        return 1
    with zipfile.ZipFile(wheels[0]) as archive:
        names = set(archive.namelist())
    commons = {name for name in names if name.startswith("skillir/commons/") and name.endswith(".md")}
    required = {
        "skillir/commons/core.pick-and-place.md",
        "skillir/commons/core.component-kitting.md",
        "skillir/commons/core.asset-condition-survey.md",
        "skillir/commons/core.surface-wipe.md",
    }
    if len(commons) < 20 or not required.issubset(commons):
        print(f"wheel commons incomplete: {len(commons)} skill sources", file=sys.stderr)
        return 1
    leaked_builds = {name for name in names if "/build/" in name}
    if leaked_builds:
        print("wheel contains generated build artifacts", file=sys.stderr)
        return 1
    print(f"wheel commons verified: {len(commons)} installable skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
