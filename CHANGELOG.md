# Changelog

## Unreleased

- Expanded the executable commons from one example to twenty-four compilable,
  vendor-neutral skills covering inspection, pick/place, fixture handling,
  material movement, replenishment, counting, sorting, order picking, workspace
  checks, and operator-confirmed handoff.
- Added a regression test requiring every checked-in commons skill to compile
  without blocking gaps.
- Bundled the complete skill Markdown in the wheel and added `skillir show` and
  `skillir pull` so installed users can inspect and customize commons skills.
- Replaced the flat starter list with a validated taxonomy spanning ten
  verticals and eleven reusable skill groups.
- Removed the unused OCR extra; PDF extraction remains explicit and advanced
  scanned-document OCR provenance stays gated in the roadmap.

## 0.1.0 — 2026-07-09

- Shipped the initial Skill IR CLI and `urn:skill-ir:v1alpha1` contract.
- Added Markdown ingestion, optional PDF ingestion contract, capability-aware compilation, gap reports, deterministic mock simulation, bundles, digest attestations, and local registry publishing.
- Added neutral robot profiles, a starter physical-skill catalog, safety boundaries, public governance files, and cross-platform CI.

### Deliberate limits

- PDF extraction requires the optional local `pdf` extra.
- Release-grade cryptographic OCI attestations, richer OCR provenance, target adapters, and hardware qualification are planned follow-on work.
- No bundle in this release claims target-platform deployment or universal safety.
