# ngram Graph System — Validation: Invariants and Verification

```
@ngram:id: VALIDATION.BUILDING.NGRAM_GRAPH_SYSTEM
STATUS: DESIGNING
CREATED: 2024-12-23
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ngram_Graph_System.md
PATTERNS:        ./PATTERNS_Ngram_Graph_System.md
BEHAVIORS:       ./BEHAVIORS_Ngram_Graph_System.md
ALGORITHM:       ./ALGORITHM_Ngram_Graph_System.md
THIS:            VALIDATION_Ngram_Graph_System.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Ngram_Graph_System.md
HEALTH:          ./HEALTH_Ngram_Graph_System.md
SYNC:            ./SYNC_Ngram_Graph_System.md
```

---

## TESTS VS HEALTH

**Tests gate completion. Health monitors runtime.**

| Concern | Tests (CI) | Health (Runtime) |
|---------|------------|------------------|
| When | Build time | Production |
| Data | Fixtures | Real graph |
| Catches | Code bugs | Emergent drift |
| Blocks | Merge/deploy | Alerts/pages |

### Write Tests For

| Category | Why |
|----------|-----|
| Context assembly rules | Deterministic filtering |
| Link creation | Known triggers |
| Narrative type mapping | Finite enum |
| Ingest correctness | Parseable input |

### Use Health Only For

| Category | Why |
|----------|-----|
| Energy drift | Needs many ticks |
| Agent differentiation | Emergent over time |
| Context quality | Subjective, sampled |
| World liveness | Continuous monitoring |

---

## INVARIANTS

### Context Assembly

#### @ngram:id: V-NGRAM-CONTEXT-HOT-ONLY
**Only hot Narratives appear in context**

```yaml
invariant: V-NGRAM-CONTEXT-HOT-ONLY
priority: HIGH
criteria: |
  For all Narratives in assembled context:
    narrative.energy >= HOT_THRESHOLD
  Cold Narratives never surface regardless of other properties.
verified_by:
  test: tests/building/test_context.py::test_only_hot_narratives_surface
  confidence: untested
evidence:
  - Context assembly query filters by energy
  - Cold Narrative in context = bug
failure_mode: |
  Noise in context. Agent work quality degrades.
  Violates B2: Relevant context surfaces, noise doesn't.
```

---

#### @ngram:id: V-NGRAM-CONTEXT-BOUNDED
**Context size stays manageable**

```yaml
invariant: V-NGRAM-CONTEXT-BOUNDED
priority: HIGH
criteria: |
  len(context.narratives) <= MAX_CONTEXT_NARRATIVES (default: 20)
  Context sorted by energy descending, truncated at limit.
verified_by:
  test: tests/building/test_context.py::test_context_bounded
  confidence: untested
evidence:
  - Context assembly enforces limit
  - Measure context size per trigger
failure_mode: |
  Context overload. Agent confused by too much information.
  Violates B2.
```

---

#### @ngram:id: V-NGRAM-CONTEXT-SPACE-SCOPED
**Context respects Space boundaries**

```yaml
invariant: V-NGRAM-CONTEXT-SPACE-SCOPED
priority: HIGH
criteria: |
  For all Narratives in assembled context:
    Space -[contains]-> Narrative
  where Space is actor's current Space(s).
verified_by:
  test: tests/building/test_context.py::test_context_space_scoped
  confidence: untested
evidence:
  - Context query joins through contains links
  - Narrative from other Space in context = bug
failure_mode: |
  Wrong context loaded. Agent works on irrelevant things.
  Violates B1: Agent produces useful work.
```

---

### Energy Flow

#### @ngram:id: V-NGRAM-ENERGY-BOUNDED
**Energy stays in valid range**

```yaml
invariant: V-NGRAM-ENERGY-BOUNDED
priority: HIGH
criteria: |
  For all nodes: 0 <= node.energy <= 1
  For all links: 0 <= link.energy <= 1
verified_by:
  test: tests/building/test_physics.py::test_energy_bounded
  health: building/health/energy.py::check_bounded
  confidence: untested
evidence:
  - Clamp on every energy update
  - Scan all energies periodically
failure_mode: |
  Negative energy or overflow breaks physics formulas.
```

---

#### @ngram:id: V-NGRAM-ENERGY-DECAYS
**Energy decays when not reinforced**

```yaml
invariant: V-NGRAM-ENERGY-DECAYS
priority: HIGH
criteria: |
  If node receives no energy for N ticks:
    node.energy decreases toward 0
  Decay rate configurable per node type.
verified_by:
  health: building/health/energy.py::check_decay
  confidence: needs-health
evidence:
  - Monitor nodes over time
  - Node stays hot forever without input = bug
failure_mode: |
  Goals never complete. Context never clears.
  Violates B3: Goals complete naturally.
```

---

#### @ngram:id: V-NGRAM-STRENGTH-ACCUMULATES
**Strength grows with energy flow**

```yaml
invariant: V-NGRAM-STRENGTH-ACCUMULATES
priority: HIGH
criteria: |
  When energy flows through link:
    link.strength += growth_amount
  Growth formula: (energy × emotion × origin.weight) / ((1 + strength) × target.weight)
verified_by:
  test: tests/building/test_physics.py::test_strength_growth_formula
  confidence: untested
evidence:
  - Sample link traversals
  - Compare expected vs actual growth
failure_mode: |
  No memory formation. Old work never resurfaces.
  Violates B4: Old work resurfaces.
```

---

#### @ngram:id: V-NGRAM-STRENGTH-PERSISTS
**Strength does not decay**

```yaml
invariant: V-NGRAM-STRENGTH-PERSISTS
priority: HIGH
criteria: |
  link.strength never decreases except by explicit action.
  Cold links retain strength indefinitely.
verified_by:
  health: building/health/strength.py::check_no_decay
  confidence: needs-health
evidence:
  - Monitor strength values over long periods
  - Strength decrease without cause = bug
failure_mode: |
  Memory loss. Past decisions forgotten.
  Violates B4.
```

---

### Graph Structure

#### @ngram:id: V-NGRAM-ACTOR-IN-SPACE
**Every Actor is in at least one Space**

```yaml
invariant: V-NGRAM-ACTOR-IN-SPACE
priority: HIGH
criteria: |
  For all actors:
    EXISTS (Space)-[contains]->(Actor)
verified_by:
  test: tests/building/test_structure.py::test_actor_has_space
  health: building/health/structure.py::check_orphan_actors
  confidence: untested
evidence:
  - Query actors without contains link
  - Orphan actor = never triggers
failure_mode: |
  Agent never activates. Invisible to system.
  Violates B8: World stays alive.
```

---

#### @ngram:id: V-NGRAM-MOMENT-EXPRESSES
**Every Moment has expresses link from Actor**

```yaml
invariant: V-NGRAM-MOMENT-EXPRESSES
priority: HIGH
criteria: |
  For all moments:
    EXISTS (Actor)-[expresses]->(Moment)
verified_by:
  test: tests/building/test_structure.py::test_moment_has_author
  health: building/health/structure.py::check_orphan_moments
  confidence: untested
evidence:
  - Query moments without expresses link
  - Orphan moment = unknown origin
failure_mode: |
  Can't trace who said what. Attribution lost.
```

---

#### @ngram:id: V-NGRAM-MOMENT-IN-SPACE
**Every Moment is contained by a Space**

```yaml
invariant: V-NGRAM-MOMENT-IN-SPACE
priority: MED
criteria: |
  For all moments:
    EXISTS (Space)-[contains]->(Moment)
verified_by:
  test: tests/building/test_structure.py::test_moment_has_space
  confidence: untested
evidence:
  - Query moments without contains link
failure_mode: |
  Moment doesn't appear in any context.
  Energy flows but nothing surfaces.
```

---

#### @ngram:id: V-NGRAM-NARRATIVE-VALID-TYPE
**Narratives have valid type from doc chain**

```yaml
invariant: V-NGRAM-NARRATIVE-VALID-TYPE
priority: MED
criteria: |
  For all narratives:
    narrative.type IN [objectives, pattern, behavior, algorithm,
                       validation, implementation, health, sync,
                       goal, rationale, memory, escalation, proposition]
verified_by:
  test: tests/building/test_structure.py::test_narrative_type_valid
  confidence: untested
evidence:
  - Validate on creation
  - Query for unknown types
failure_mode: |
  Unknown type = can't determine handling.
  Physics defaults may be wrong.
```

---

### Actor Behavior

#### @ngram:id: V-NGRAM-AGENT-TRIGGERS-ON-HOT
**Agents trigger when Moment in their Space activates**

```yaml
invariant: V-NGRAM-AGENT-TRIGGERS-ON-HOT
priority: HIGH
criteria: |
  When Moment.energy >= ACTIVATION_THRESHOLD
  AND (Space)-[contains]->(Moment)
  AND (Space)-[contains]->(Agent)
  THEN Agent.trigger() called with context
verified_by:
  test: tests/building/test_agent.py::test_agent_triggers_on_activation
  confidence: untested
evidence:
  - Log trigger events
  - Hot moment + agent in space + no trigger = bug
failure_mode: |
  Work doesn't happen. World appears dead.
  Violates B1, B8.
```

---

#### @ngram:id: V-NGRAM-AGENT-CREATES-MOMENTS
**Agent work creates Moments**

```yaml
invariant: V-NGRAM-AGENT-CREATES-MOMENTS
priority: HIGH
criteria: |
  When agent.respond() completes:
    At least one Moment created
    Moment links to triggering context via about
    Moment links from Agent via expresses
verified_by:
  test: tests/building/test_agent.py::test_agent_creates_moments
  confidence: untested
evidence:
  - Count moments before/after agent work
  - Zero new moments = broken agent
failure_mode: |
  Agent works but nothing recorded.
  No energy flow from completion.
```

---

### Ingest

#### @ngram:id: V-NGRAM-INGEST-CREATES-NARRATIVES
**Doc ingest creates Narratives**

```yaml
invariant: V-NGRAM-INGEST-CREATES-NARRATIVES
priority: HIGH
criteria: |
  For each doc file matching pattern:
    At least one Narrative created
    Narrative.type matches doc type (OBJECTIVES_ -> objectives, etc.)
    Narrative linked to containing Space
verified_by:
  test: tests/building/test_ingest.py::test_doc_creates_narrative
  confidence: untested
evidence:
  - Count narratives before/after ingest
  - Missing narrative for known doc = bug
failure_mode: |
  Docs not queryable. Knowledge not in graph.
  Violates B6: Docs become queryable.
```

---

#### @ngram:id: V-NGRAM-INGEST-EXTRACTS-MARKERS
**Markers become goal/escalation Narratives**

```yaml
invariant: V-NGRAM-INGEST-EXTRACTS-MARKERS
priority: MED
criteria: |
  For each @ngram:todo marker:
    Narrative created with type=goal, status=pending
  For each @ngram:escalation marker:
    Narrative created with type=escalation, status=pending
verified_by:
  test: tests/building/test_ingest.py::test_markers_extracted
  confidence: untested
evidence:
  - Count marker narratives vs markers in source
failure_mode: |
  TODOs not tracked. Escalations invisible.
```

---

### World Runner

#### @ngram:id: V-NGRAM-WORLD-TICKS
**World advances when runner active**

```yaml
invariant: V-NGRAM-WORLD-TICKS
priority: HIGH
criteria: |
  When runner.running == True:
    tick() called at configured rate (x1/x2/x3)
    All actors generate energy per tick
    Physics flows
verified_by:
  health: building/health/runner.py::check_ticking
  confidence: needs-health
evidence:
  - Monitor tick count over time
  - Tick rate matches config
failure_mode: |
  World frozen. No agents trigger.
  Violates B8: World stays alive.
```

---

#### @ngram:id: V-NGRAM-ALL-ACTORS-GENERATE
**All actors generate energy each tick**

```yaml
invariant: V-NGRAM-ALL-ACTORS-GENERATE
priority: HIGH
criteria: |
  Each tick:
    For all actors in a Space:
      actor generates energy based on proximity
  No actor excluded from generation.
verified_by:
  test: tests/building/test_physics.py::test_all_actors_generate
  health: building/health/energy.py::check_generation
  confidence: untested
evidence:
  - Log generation per actor per tick
  - Actor with zero generation = bug
failure_mode: |
  Some actors starve. Uneven participation.
  Violates objective: same rules for all.
```

---

## CONFIDENCE LEVELS

| Level | Meaning | Action |
|-------|---------|--------|
| `high` | Test + health cover completely | None |
| `partial` | Test exists but edge cases remain | Track gaps |
| `needs-health` | Runtime behavior matters more than test | Write health check |
| `untested` | Gap, tracked for completion | Write test or justify |

---

## PRIORITY LEVELS

| Priority | Meaning | Requirement |
|----------|---------|-------------|
| `HIGH` | System breaks without this | MUST have verified_by |
| `MED` | Degraded behavior | SHOULD have test |
| `LOW` | Nice to have | MAY defer |

---

## VALIDATION ID INDEX

| ID | Category | Priority | Confidence |
|----|----------|----------|------------|
| V-NGRAM-CONTEXT-HOT-ONLY | Context | HIGH | untested |
| V-NGRAM-CONTEXT-BOUNDED | Context | HIGH | untested |
| V-NGRAM-CONTEXT-SPACE-SCOPED | Context | HIGH | untested |
| V-NGRAM-ENERGY-BOUNDED | Energy | HIGH | untested |
| V-NGRAM-ENERGY-DECAYS | Energy | HIGH | needs-health |
| V-NGRAM-STRENGTH-ACCUMULATES | Energy | HIGH | untested |
| V-NGRAM-STRENGTH-PERSISTS | Energy | HIGH | needs-health |
| V-NGRAM-ACTOR-IN-SPACE | Structure | HIGH | untested |
| V-NGRAM-MOMENT-EXPRESSES | Structure | HIGH | untested |
| V-NGRAM-MOMENT-IN-SPACE | Structure | MED | untested |
| V-NGRAM-NARRATIVE-VALID-TYPE | Structure | MED | untested |
| V-NGRAM-AGENT-TRIGGERS-ON-HOT | Actor | HIGH | untested |
| V-NGRAM-AGENT-CREATES-MOMENTS | Actor | HIGH | untested |
| V-NGRAM-INGEST-CREATES-NARRATIVES | Ingest | HIGH | untested |
| V-NGRAM-INGEST-EXTRACTS-MARKERS | Ingest | MED | untested |
| V-NGRAM-WORLD-TICKS | Runner | HIGH | needs-health |
| V-NGRAM-ALL-ACTORS-GENERATE | Runner | HIGH | untested |

---

## MARKERS

<!-- @ngram:todo Write test suite for context assembly invariants -->
<!-- @ngram:todo Write health checkers for energy/strength monitoring -->
<!-- @ngram:todo Define HOT_THRESHOLD, ACTIVATION_THRESHOLD constants -->
<!-- @ngram:todo Define MAX_CONTEXT_NARRATIVES constant -->

<!-- @ngram:escalation V-NGRAM-ENERGY-DECAYS vs goals that stay active — need to distinguish "ongoing goal" from "stuck goal". How? -->
<!-- @ngram:escalation V-NGRAM-STRENGTH-PERSISTS may cause unbounded growth — need to define max strength or soft cap? -->
<!-- @ngram:escalation V-NGRAM-AGENT-TRIGGERS-ON-HOT doesn't specify priority — if 3 Moments are hot, which one? Highest energy? Random? -->

<!-- @ngram:proposition Add invariant V-NGRAM-NO-ORPHAN-NARRATIVES — every Narrative should be in at least one Space -->
<!-- @ngram:proposition Add invariant V-NGRAM-HUMAN-GENERATES-MOST — human energy generation should be measurably higher than agents to ensure steering -->
<!-- @ngram:proposition Add health check for "agent diversity" — alert if all agents converge to same beliefs/spaces -->
