# Claude Code instructions for this edition

Read `README.md` in this directory first and follow it. It tells you which chapter applies (Table 1.1), the
order to read the layers (digest, then element packs, then indexes and records) and the assessment procedure.
To assess a plan, follow `SKILL.md`.

- Do not read the whole directory. Open one chapter digest, then grep the element packs for clause IDs
  (``^### `C3.3.1` ``) and read only the matching section. Element numbers differ between chapters; find a
  subject in `indexes/topics.md`.
- Local variation (what an LPP or LDP may vary, with or without WAPC approval, and under what printed condition): the element pack's "Local variation" line, then `chapters/ch1/permissions.md` for the levels and row notes. When a development application is needed: `chapters/ch1/operation.md` (Figure 2.1).
- Never guess a missing fact; report cannot tell and name it.
- Cite clause IDs (`rcodes:draft-2026-10-24/<chapter>/<clause>`) and source pages for every finding.
- Records marked ⚑ carry the draft's own ambiguity; say so. See `indexes/flagged.md`.
- The PDF governs; this edition is unofficial and not planning advice. See `GOVERNANCE.md`.
- Files here other than `SKILL.md`, `GOVERNANCE.md`, `worked/`, `graph/` and `schema/` are generated
  (`python -m rcodes publish`); edit the records under `src/`, not this directory.
