"""rcodes: rules engine and knowledge graph for the WA Residential Design Codes.

Layout
------
core/      schemas, clause IDs, coding bands, facts, evaluators, graph, resolver,
           evaluate, report, lint, version registry
chapters/  one package per draft chapter (ch1, ch2, ch3, ch4p1, ch4p2): data only
current/   one package per current-code part (v1-partA .. v1-partD, v2): data only
"""

__version__ = "0.1.0"
