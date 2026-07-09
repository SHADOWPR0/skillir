"""Parse the deliberately small Markdown authoring surface into deterministic steps."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


STEP = re.compile(r"^\s*(\d+)\.\s+(.+?)\s*$")
FIELD = re.compile(r"^\s*-\s*(action|observe|verify|on_failure|evidence):\s*(.+?)\s*$", re.I)


@dataclass
class Step:
    id: str
    instruction: str
    action: str = "unresolved"
    observe: str = ""
    verify: str = ""
    on_failure: str = "escalate.human"
    evidence: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "instruction": self.instruction,
            "action": self.action,
            "observe": self.observe,
            "verify": self.verify,
            "on_failure": self.on_failure,
            "evidence_refs": self.evidence,
        }


def parse_steps(body: str) -> list[Step]:
    in_steps = False
    steps: list[Step] = []
    current: Step | None = None
    for line in body.splitlines():
        if line.strip().lower() == "## steps":
            in_steps = True
            continue
        if in_steps and line.startswith("## "):
            break
        if not in_steps:
            continue
        match = STEP.match(line)
        if match:
            current = Step(id=f"step-{int(match.group(1)):02d}", instruction=match.group(2))
            steps.append(current)
            continue
        match = FIELD.match(line)
        if match and current:
            key, value = match.group(1).lower(), match.group(2)
            if key == "evidence":
                current.evidence.append(value)
            else:
                setattr(current, key, value)
    return steps


def section_text(body: str, heading: str) -> str:
    marker = f"## {heading}".lower()
    lines = body.splitlines()
    collected: list[str] = []
    active = False
    for line in lines:
        if line.strip().lower() == marker:
            active = True
            continue
        if active and line.startswith("## "):
            break
        if active and line.strip():
            collected.append(line.strip())
    return " ".join(collected)
