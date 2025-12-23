# ngram Graph System — Sync: Current State

```
STATUS: DESIGNING → PHASE 1
UPDATED: 2025-12-23
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ngram_Graph_System.md
PATTERNS:        ./PATTERNS_Ngram_Graph_System.md
BEHAVIORS:       ./BEHAVIORS_Ngram_Graph_System.md
ALGORITHM:       ./ALGORITHM_Ngram_Graph_System.md
VALIDATION:      ./VALIDATION_Ngram_Graph_System.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ngram_Graph_System.md
HEALTH:          ./HEALTH_Ngram_Graph_System.md (not yet)
THIS:            SYNC_Ngram_Graph_System.md (you are here)
```

---

## CURRENT STATE

**Phase:** Design complete. Starting Phase 1 implementation.

---

## IMPLEMENTATION PHASES

| Phase | Goal | Value Delivered | Status |
|-------|------|-----------------|--------|
| 1. See Graph | Ingest docs → nodes | Docs queryable in graph | **NEXT** |
| 2. Active Context | Query active Narratives | Physics-driven relevance | — |
| 3. One Agent | Agent responds to Moment | Agent produces output | — |
| 4. Lasting Work | Agent creates Narratives | Knowledge growth | — |
| 5. Multi-Agent | 6 agents differentiate | Parallel work | — |
| 6. Continuous | World runs autonomously | Full vision | — |

### Phase 1 Scope

**Input:** `docs/building/*.md` + `mapping.yaml`
**Output:** Graph with Spaces, Narratives, Things
**Verify:** Query graph, see docs as nodes

Deliverables:
- `building/ingest/discover.py` — find files matching patterns
- `building/ingest/parse.py` — extract content, sections, markers
- `building/ingest/create.py` — call engine.create_* APIs
- `building/config/mapping.py` — load mapping.yaml

---

### What Exists

| Doc | Status | Content |
|-----|--------|---------|
| OBJECTIVES | Complete | 8 ranked objectives, non-objectives, tradeoffs |
| PATTERNS | Complete | 8 key decisions, invariants, open patterns |
| BEHAVIORS | Complete | 11 observable value behaviors, anti-behaviors |
| ALGORITHM | Complete | 4 client procedures (ingest, query, handler, create) |
| VALIDATION | Complete | 17 invariants across 6 categories |
| mapping.yaml | Complete | v2.0 repo-to-graph mapping |
| IMPLEMENTATION | Complete | Code structure, 3 flows with docking points |
| HEALTH | Not started | — |

### What's Designed

- **Graph structure:** 5 node types (Space, Actor, Narrative, Moment, Thing)
- **Link types:** 9 types per schema v1.2 (contains, expresses, about, relates, attached_to, leads_to, sequence, primes, can_become)
- **Physics:** Energy/weight/strength/conductivity fields defined
- **Client boundary:** Clear separation between client (us) and engine
- **Ingest pipeline:** mapping.yaml defines all transformations

### What's NOT Designed

- Agent prompts (base prompts, response format)
- Bootstrap sequence (first run procedure)
- Incremental ingest (file changes after bootstrap)
- Health checkers for this module
- Actual implementation code

---

## RECENT CHANGES

| Date | Change |
|------|--------|
| 2025-12-23 | Defined 6-phase implementation plan |
| 2025-12-23 | Analyzed engine reuse (40% reuse, 60% new) |
| 2025-12-23 | Reviewed all escalations with recommendations |
| 2024-12-23 | Created full doc chain (OBJECTIVES → VALIDATION) |
| 2024-12-23 | Created mapping.yaml v2.0 with 9 link types |
| 2024-12-23 | Added escalations/propositions to all docs |

---

## OPEN DECISIONS

| Decision | Options | Leaning |
|----------|---------|---------|
| Space granularity | per module / per objective / per feature | Start with module |
| Agent count | fixed 6 / dynamic | Start fixed |
| Goal completion | physics decay / explicit close | Physics decay |
| Ingest trigger | manual / file watcher / git hook | Manual first |
| Type inference | heuristics / LLM | Heuristics first |

---

## BLOCKERS

None currently. Ready for implementation.

---

## NEXT STEPS (Phase 1)

1. **Resolve Phase 1 escalations** — Engine API verification, mapping parser
2. **Create building/ package** — `__init__.py`, directory structure
3. **Implement mapping loader** — `config/mapping.py` with pydantic models
4. **Implement discover** — `ingest/discover.py` file pattern matching
5. **Implement parse** — `ingest/parse.py` doc parsing, marker extraction
6. **Implement create** — `ingest/create.py` engine API calls
7. **Test with docs/building/** — verify 8 docs become Narratives

---

## HANDOFFS

### For Phase 1 Implementation

**Blocking escalations to resolve first:**
1. Verify engine API — do `engine.create_space()`, `engine.create_narrative()` exist?
2. Choose mapping parser approach — pydantic recommended

**Then build:**
- `building/config/mapping.py` — load + validate mapping.yaml
- `building/ingest/discover.py` — glob patterns from mapping
- `building/ingest/parse.py` — markdown parsing, marker extraction
- `building/ingest/create.py` — engine API calls

### For Human

Phase 1 escalations need decisions (see below).

---

## MARKERS

### Phase 1 TODOs

<!-- @ngram:todo Verify engine.create_space() API exists and signature -->
<!-- @ngram:todo Verify engine.create_narrative() API exists and signature -->
<!-- @ngram:todo Create building/ package directory structure -->
<!-- @ngram:todo Implement mapping.py with pydantic models -->
<!-- @ngram:todo Implement discover.py file pattern matching -->
<!-- @ngram:todo Implement parse.py markdown + marker extraction -->
<!-- @ngram:todo Implement create.py engine API calls -->
<!-- @ngram:todo Test ingest with docs/building/ -->

### Phase 1 Escalations

<!-- @ngram:escalation Engine API not verified — need to check actual signatures for create_space, create_narrative, create_thing, create_link -->
<!-- @ngram:escalation Mapping parser choice — pydantic vs raw dict. Recommendation: pydantic for validation -->
<!-- @ngram:escalation Section extraction granularity — one Narrative per file or per ## heading? Recommendation: start with file level -->
<!-- @ngram:escalation Link creation during ingest — when to create contains/relates links? Same pass or separate? -->

### Future Phase TODOs

<!-- @ngram:todo Create agents.yaml with initial agents (Phase 3) -->
<!-- @ngram:todo Define physics constants (Phase 2) -->
<!-- @ngram:todo Create HEALTH doc with runtime checkers (Phase 6) -->

### Propositions

<!-- @ngram:proposition Create a "dry run" mode that logs what would be created without touching graph -->
<!-- @ngram:proposition Start ingest with docs/building/ only, expand after verified -->
