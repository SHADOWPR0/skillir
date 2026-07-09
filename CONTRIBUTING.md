# Contributing

Contribute source-backed, vendor-neutral physical skills, adapters, test cases,
or documentation.

## Contribution contract

- Include a declared SPDX license and rights to distribute every contributed source or derivative.
- Use `skill.md` plus evidence references; do not submit loose prompt text as a skill.
- Preserve uncertainty. Missing physical facts belong in a gap report, never invented fields.
- Keep target-platform names, private customer information, credentials, and proprietary manuals out of public packs.
- Add deterministic tests and run `python3 -m unittest discover -s tests` before opening a pull request.

## Maturity claims

Use only the defined labels: `reference`, `reviewed`, `robot_ir`,
`sim_qualified`, `cell_qualified`, and `production_approved`. Do not claim a
skill is universally safe, certified, or compatible with a target system unless
the submitted evidence proves that precise configuration.

## Pack layout

```text
packs/<domain>/skills/<skill-id>/
  skill.md
  tests/
  assets/
```

Generated build output stays untracked. Large datasets and videos belong in a
content-addressed registry, not Git.
