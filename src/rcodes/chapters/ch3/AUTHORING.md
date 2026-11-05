# Chapter 3 rule authoring guide

Read `../ch2/AUTHORING.md` first. Everything in it applies here with the changes below.
Chapter 3 (grouped dwellings) is the twin of Chapter 2 (single houses): the same four
parts, the same 24 elements, and most provisions word for word. The engine keeps the two
packages independent but a pairing lint (`core/lint.py`, check `pairing`) compares every
rule that exists under the same clause ID in both and warns when their evaluator, inputs,
exceptions, conditions, coding or kind differ, unless the rule's `notes` begin with
`diverges:`.

## Sources

1. Draft text: `Working/text/draft/Residential Design Codes Chapter 3 - Grouped Dwellings.txt`
   (page markers `===== PAGE n =====`; use the Chapter 3 PDF page in `source.page`).
2. Register: `Working/register/ch3-grouped-dwellings.csv` (same columns as the ch2 register;
   `id` values `ch3-001` to `ch3-100`).
3. The Chapter 2 package: `src/rcodes/chapters/ch2/` (rules, fallbacks, tables, cases). This is
   your starting point, not a source of truth: every value must still be checked against the
   Chapter 3 text, because the registers found differences the Table of Changes does not list.

## Method: start from the twin

For each provision in your slice:

1. Find the Chapter 2 rule file for the same clause (same element and clause number). If the
   Chapter 3 text is the same provision, copy the file and change only:
   - `id`: `/ch2/` to `/ch3/` (keep the clause, suffix and `#fragment` exactly)
   - `chapter`: `ch3`
   - `applies_to`: `["grouped_dwelling"]` (plus `"ancillary_dwelling"` where the clause says so)
   - `fallback`: `rcodes:draft-2026-10-24/ch3/M<element>`
   - `source.page`: the Chapter 3 page
   - `register_ref`: the ch3 row id
   - `replaces`: from the ch3 register's `current_source` and `change_type`
   - `notes`: Chapter 3 register notes, short
   Leave `evaluator`, `inputs`, `exceptions`, `conditions`, `coding`, `kind` untouched so the
   pairing lint passes.
2. If the Chapter 3 text differs (a value, a condition, an extra sub-clause), change what differs
   and start `notes` with `diverges: <what and why, citing the ch3 page>`.
3. If the provision exists only in Chapter 3 (communal streets, visitor parking, C3.4.6, C3.7.5
   to C3.7.6, C3.7.10 to C3.7.15, C1.2.3, C1.2.5, C1.2.8, C2.4.2 to C2.4.3, C2.7.1, Table 3B),
   write it fresh following the ch2 guide. Its ID will have no twin and the lint ignores it.
4. If a Chapter 2 provision has no Chapter 3 equivalent, do not copy it. Say so in your reply.

Clause numbers can shift between the chapters (Chapter 3's 3.7 has fifteen clauses to
Chapter 2's ten; Chapter 3's 1.2 has eight to Chapter 2's five). Match provisions by content
first and number second; the ID always follows the Chapter 3 number.

## Tables

Copy the Chapter 2 table files you need into `ch3/tables/` with the same short `id` (the
registry resolves a table in the chapter's own package first), update `source` to the
Chapter 3 page, and check every value against the Chapter 3 text. Table 3B (site area per
dwelling) replaces Table 2B and is keyed on coding like it; it carries minimum, average,
and battleaxe values per dwelling.

## Facts

Use `ch3/FACTS.md`. It is the Chapter 2 vocabulary plus a grouped-dwelling section. Propose
new facts in `tests/cases/FACTS-PROPOSED-<part>.md` as before.

## Files you write

```
src/rcodes/chapters/ch3/
  rules/<element>/<clause>.json
  fallbacks/M<element>.json
  tables/table-<ref>.json
  tests/cases/<part>.json
  tests/cases/FACTS-PROPOSED-<part>.md   (only if needed)
```

Do not write meta.json, AUTHORING.md, FACTS.md or table-3A.json. Do not touch another slice's
directories or anything under ch2/. No session, hand-off, messaging or scheduling tools. Do not
run pytest or install packages.
