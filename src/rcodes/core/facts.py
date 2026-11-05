"""Facts: the inputs a rule reads.

A FactSet is a flat map of dotted names (site.r_code, dwelling.garage.setback_primary_m)
to values, plus per-fact metadata (source, method, confidence). A fact that is absent,
null, or below the confidence threshold is UNKNOWN. Rules never see a default.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

DEFAULT_CONFIDENCE_THRESHOLD = 0.8
METHODS = ("stated", "measured", "computed", "inferred", "assumed")


class _Unknown:
    __slots__ = ()

    def __repr__(self) -> str:
        return "UNKNOWN"

    def __bool__(self) -> bool:
        return False


UNKNOWN = _Unknown()


@dataclass
class FactMeta:
    source: dict[str, Any] = field(default_factory=dict)
    method: str = "stated"
    confidence: float = 1.0


@dataclass
class FactSet:
    values: dict[str, Any] = field(default_factory=dict)
    meta: dict[str, FactMeta] = field(default_factory=dict)
    threshold: float = DEFAULT_CONFIDENCE_THRESHOLD
    missing_log: list[str] = field(default_factory=list)

    @classmethod
    def from_application(cls, doc: dict[str, Any], threshold: float = DEFAULT_CONFIDENCE_THRESHOLD) -> "FactSet":
        """Flatten an application-data document into dotted fact names.

        Lists of objects (dwellings[]) are flattened with an index: dwellings.0.bedrooms.
        Lists of scalars and GeoJSON geometry objects are kept whole.
        facts_meta is keyed by the same dotted names.
        """
        values: dict[str, Any] = {}

        def walk(prefix: str, node: Any) -> None:
            if isinstance(node, dict):
                if node.get("type") in ("Polygon", "MultiPolygon", "Point", "LineString") and "coordinates" in node:
                    values[prefix] = node
                    return
                for k, v in node.items():
                    if prefix == "" and k == "facts_meta":
                        continue
                    walk(f"{prefix}.{k}" if prefix else k, v)
            elif isinstance(node, list) and node and all(isinstance(x, dict) for x in node):
                values[prefix + ".count"] = len(node)
                for i, item in enumerate(node):
                    walk(f"{prefix}.{i}", item)
            else:
                values[prefix] = node

        walk("", doc)
        meta: dict[str, FactMeta] = {}
        for name, m in (doc.get("facts_meta") or {}).items():
            meta[name] = FactMeta(source=m.get("source", {}), method=m.get("method", "stated"),
                                  confidence=float(m.get("confidence", 1.0)))
        return cls(values=values, meta=meta, threshold=threshold)

    def get(self, name: str) -> Any:
        """Value or UNKNOWN. Unknowns are logged with the reason."""
        if name not in self.values or self.values[name] is None:
            self._log(f"{name}: not supplied")
            return UNKNOWN
        m = self.meta.get(name)
        if m is not None and m.confidence < self.threshold:
            self._log(f"{name}: confidence {m.confidence:.2f} below {self.threshold:.2f}")
            return UNKNOWN
        return self.values[name]

    def has(self, name: str) -> bool:
        return self.get(name) is not UNKNOWN

    def provenance(self, name: str) -> FactMeta | None:
        return self.meta.get(name)

    def _log(self, reason: str) -> None:
        if reason not in self.missing_log:
            self.missing_log.append(reason)

    def with_overrides(self, **kw: Any) -> "FactSet":
        v = dict(self.values)
        v.update(kw)
        return FactSet(values=v, meta=dict(self.meta), threshold=self.threshold)
