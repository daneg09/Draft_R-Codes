"""Render a RunResult as JSON or Markdown."""

from __future__ import annotations

import json
from typing import Any

from .evaluate import RunResult

STATUS_LABEL = {
    "MEETS": "Meets",
    "DOES_NOT_MEET": "Does not meet",
    "CANNOT_TELL": "Cannot tell",
    "NOT_APPLICABLE": "Not applicable",
    "NOT_EVALUATED": "Not evaluated",
}


def to_json(result: RunResult, indent: int = 2) -> str:
    return json.dumps(result.to_dict(), indent=indent, ensure_ascii=False)


def to_markdown(result: RunResult) -> str:
    d = result.to_dict()
    lines: list[str] = []
    lines.append(f"# R-Codes check: {d['version']}")
    lines.append("")
    a = d["applicability"]
    lines.append(f"Chapter: {d['chapter'] or 'none'}. Dwelling type: {a.get('dwelling_type')}. "
                 f"Coding: {a.get('r_code')}. Pathway: {d['pathway']}.")
    da = d["development_application"]
    lines.append(f"Development application: {da.get('required_label', da.get('required'))}. {da.get('basis', '')}".strip())
    if a.get("reasons"):
        lines.append("")
        for r in a["reasons"]:
            lines.append(f"- {r}")
    counts = d["counts"]
    if counts:
        lines.append("")
        lines.append("| Outcome | Count |")
        lines.append("|---|---|")
        for k, v in sorted(counts.items()):
            lines.append(f"| {STATUS_LABEL.get(k, k)} | {v} |")
    lines.append("")
    lines.append("## Provisions")
    lines.append("")
    lines.append("| Element | Clause | Outcome | Tested | Threshold | Exception / variation | Fallback |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in d["results"]:
        o = r.get("outcome", {})
        tested = _fmt(o.get("tested"))
        thr = f"{_fmt(o.get('op'))} {_fmt(o.get('threshold'))}".strip()
        extra = []
        if r.get("exception_used"):
            extra.append(f"exception: {r['exception_used']}")
        if r.get("variation"):
            v = r["variation"]
            extra.append(f"{v['instrument']} {v['clause']} ({v['status']})")
        if r.get("missing"):
            extra.append("missing: " + ", ".join(r["missing"]))
        clause = r["rule_id"].split("/")[-1]
        lines.append(f"| {r['element']} {r.get('element_title', '')} | {clause} | {STATUS_LABEL.get(r['status'], r['status'])} "
                     f"| {tested} | {thr} | {'; '.join(extra)} | {(r.get('fallback') or '').split('/')[-1]} |")
    if d["elements_on_merit"]:
        lines.append("")
        lines.append("## Merit assessment required")
        lines.append("")
        for e in d["elements_on_merit"]:
            lines.append(f"- Element {e}")
        if d["consultation"]:
            lines.append("")
            lines.append("Recommended consultation (Chapter 1 Table 2.4):")
            for c in d["consultation"]:
                lines.append(f"- {c['element']} {c.get('element_title', '')}: {c['parties']}")
    if d["variations"]:
        lines.append("")
        lines.append("## Local instrument variations")
        lines.append("")
        for v in d["variations"]:
            lines.append(f"- {v['instrument']} {v['clause']}: {v['status']}. {v['reason']}")
    if d["missing"]:
        lines.append("")
        lines.append("## Missing facts")
        lines.append("")
        for src, names in d["missing"].items():
            lines.append(f"- {src}: " + ", ".join(names))
    if d["warnings"]:
        lines.append("")
        lines.append("## Warnings")
        lines.append("")
        for w in d["warnings"]:
            lines.append(f"- {w}")
    return "\n".join(lines) + "\n"


def _fmt(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)
