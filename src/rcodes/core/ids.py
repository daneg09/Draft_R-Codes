"""Clause ID scheme.

    rcodes:<version>/<chapter>/<clause>[#fragment]

Examples
    rcodes:draft-2026-10-24/ch2/C3.1.1
    rcodes:draft-2026-10-24/ch2/C3.1.1#table-3.1a
    rcodes:draft-2026-10-24/ch4p2/T2.1#row-R80
    rcodes:vol1-v3-2026-04-10/partB/5.1.3-C3.1

IDs are immutable within a version. Clause may be a C/M/A/O/DG/T (table) reference or
a current-code clause path. Element is derived from the clause where it has the form
<letter(s)><part>.<element>.<n>.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_ID_RE = re.compile(
    r"^rcodes:(?P<version>[a-z0-9][a-z0-9.-]*)/(?P<chapter>[a-z0-9-]+)/(?P<clause>[A-Za-z0-9.()-]+)"
    r"(?:#(?P<fragment>[A-Za-z0-9.-]+))?$"
)
_CLAUSE_RE = re.compile(r"^(?P<column>C|M|A|O|DG|T)?(?P<part>\d+)\.(?P<element>\d+)(?:\.(?P<n>\d+))?(?P<suffix>.*)$")


@dataclass(frozen=True)
class ClauseId:
    version: str
    chapter: str
    clause: str
    fragment: str | None = None

    @classmethod
    def parse(cls, text: str) -> "ClauseId":
        m = _ID_RE.match(text.strip())
        if not m:
            raise ValueError(f"not a clause id: {text!r}")
        return cls(m["version"], m["chapter"], m["clause"], m["fragment"])

    def __str__(self) -> str:
        base = f"rcodes:{self.version}/{self.chapter}/{self.clause}"
        return f"{base}#{self.fragment}" if self.fragment else base

    @property
    def column(self) -> str | None:
        m = _CLAUSE_RE.match(self.clause)
        return m["column"] if m else None

    @property
    def element(self) -> str | None:
        """'3.1' for C3.1.1; None for clauses that do not follow part.element.n."""
        m = _CLAUSE_RE.match(self.clause)
        if not m:
            return None
        return f"{m['part']}.{m['element']}"

    def with_fragment(self, fragment: str) -> "ClauseId":
        return ClauseId(self.version, self.chapter, self.clause, fragment)


def make(version: str, chapter: str, clause: str, fragment: str | None = None) -> str:
    return str(ClauseId(version, chapter, clause, fragment))


def is_valid(text: str) -> bool:
    return _ID_RE.match(text.strip()) is not None
