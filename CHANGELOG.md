# Changelog

## 0.1.0 — 2026-07-09

- Shipped the initial Skill IR CLI and `urn:skill-ir:v1alpha1` contract.
- Added Markdown ingestion, optional PDF ingestion contract, capability-aware compilation, gap reports, deterministic mock simulation, bundles, digest attestations, and local registry publishing.
- Added neutral robot profiles, a starter physical-skill catalog, safety boundaries, public governance files, and cross-platform CI.

### Deliberate limits

- PDF extraction requires the optional local `pdf` extra.
- Release-grade cryptographic OCI attestations, richer OCR provenance, target adapters, and hardware qualification are planned follow-on work.
- No bundle in this release claims target-platform deployment or universal safety.
