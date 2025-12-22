# Physics — Implementation: Code Architecture & Runtime

```
STATUS: STABLE
UPDATED: 2025-12-21
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Physics.md
BEHAVIORS:      ./BEHAVIORS_Physics.md
ALGORITHMS:     ./ALGORITHM_Physics.md
VALIDATION:     ./VALIDATION_Physics.md
THIS:           ./IMPLEMENTATION_Physics.md (you are here)
HEALTH:         ./HEALTH_Physics.md
SYNC:           ./SYNC_Physics.md
ARCHIVE:        ./archive/IMPLEMENTATION_Physics_archive_2025-12.md
```

---

## SUMMARY

The physics implementation ensures graph-first orchestration where all state lives in FalkorDB. The system uses a tick-based metabolism (GraphTick) to propagate energy and detect salience flips. This document covers code structure, design patterns, state management, runtime behavior, and module dependencies.

---

## CODE STRUCTURE & RESPONSIBILITIES

### Code Structure Snapshot

- `engine/physics/tick.py`: GraphTick pump/propagate/decay loop, flip detection, energy clamps.
- `engine/physics/graph/graph_queries.py`: Read façade used by the tick and traversal layers.
- `engine/physics/graph/graph_ops.py`: Mutation façade plus mixins (attention split, PRIMES decay, contradiction pressure).
- `engine/physics/graph/graph_ops_read_only_interface.py`: Connectome-friendly read helpers (GraphReadOps) pulled into separate module.
- `engine/moment_graph/*`: Queries + traversal helpers for click/wait interactions.
- `engine/models/*`: Pydantic base models for moments, links, narratives, etc.

The tick is the orchestrator; it does not store state beyond an ephemeral context.

### File Responsibilities (Highlight)

| Artifact | Purpose | Owner | Status |
|----------|---------|-------|--------|
| `engine/physics/tick.py` | Tick metabolism and flip detection | GraphTick | WATCH (430+ lines) |
| `graph_queries.py` | Read queries | GraphQueries | SPLIT (under 700 lines) |
| `graph_ops.py` | Write commands | GraphOps + mixins | SPLIT (under 700 lines) |
| `graph_ops_read_only_interface.py` | Search/seed reader | GraphReadOps | OK |
| `moment_graph/traversal.py` | Interaction handling | Click traversal | OK |

### Schema & Entrypoints

- **Moment node:** `id`, `text`, `type`, `status`, `weight`, `energy`.
- **Links:** BELIEVES, ATTACHED_TO, CAN_SPEAK, THEN, etc.

**Entry points:**
- Physics tick: `engine/physics/tick.py:run()` invoked by the orchestrator.
- Click traversal: `engine/moment_graph/traversal.py:handle_click()`.
- Player input: `engine/infrastructure/api/moments.py`.

---

## DESIGN & RUNTIME PATTERNS

### Design Patterns

- **Graph-first orchestration:** GraphTick reads/writes the graph; all state lives there.
- **Query/Command separation:** `graph_queries` vs `graph_ops` keeps reads and writes distinct.
- **Facades + mixins:** GraphOps composes command mixins (attention split, PRIMES, contradictions) so plumbing stays composable.
- **Observer/Events:** `graph_ops_events.py` emits hooks for downstream listeners without inlining the logic.

### Runtime Patterns

- **Scene as query:** Scenes are query results, not objects.
- **Time passage:** `advance_time(minutes)` called on spoken moments to drive ticks.
- **Character movement:** Travel moments update `AT` links and spawn consequence moments.

### Anti-patterns to avoid

- Hidden writes in query helpers.
- Stateful orchestrators that cache moment state instead of always querying the graph.

---

## STATE MANAGEMENT

- **Graph state:** Lives in FalkorDB (`Moment`, `Link`, `Narrative` nodes). No cached state outside the graph.
- **Active tensions:** Derived from contradictions/demands; persist as relationships, not dedicated nodes.
- **Energy:** Stored on node properties; decays each tick.

---

## TICK METABOLISM (FLOWS)

### physics_tick Flow

1. Characters pump energy into narratives via BELIEVES/ABOUT links (`_flow_energy_to_narratives`).
2. Narrative energy transfers across RELATES_TO/SUPPORTS links (`_propagate_energy`).
3. Energy flows into moments (`ATTACHED_TO`, `CAN_SPEAK`), then clamps/decays (`_decay_energy`).
4. Salience is computed (weight × energy); `_detect_flips` surfaces events when thresholds cross.
5. Flip metadata returns to orchestrator to trigger handlers and canon.
6. Updates are persisted through `graph_ops` and reported to observers (events, health, display).

### Logic Chains

- **Flip detection:** Tension/energy crosses threshold → `TickResult.flips` → orchestrator dispatch → handler output.
- **Action queue:** Action moment actualizes → queued by `process_actions` → updates graph (AT, possession, tension) → cascade occurs.
- **Drama cascade:** One actualization energizes witnesses → new flips follow (B8 behavior).

---

## CONCURRENCY, CONFIG & DEPENDENCIES

### Concurrency & Config

- Physics tick runs synchronously; energy math is linear.
- Handlers execute asynchronously (LLM calls) but writing occurs sequentially through graph ops.
- Configs: `DECAY_RATE`, `BELIEF_FLOW_RATE` stored in `engine/physics/constants.py`.

### Module Dependencies

- `engine/infrastructure/orchestration/orchestrator.py` → imports `engine/physics/tick.py` and `engine/moment_graph/queries.py`.
- `engine/physics/tick.py` → reads via `graph_queries.py`, writes via `graph_ops.py`, coordinates `graph_ops_events.py` for listeners.
- `engine/physics/graph/graph_ops.py` → composes mixins for attention split, PRIMES decay, contradiction pressure.
- `engine/physics/graph/graph_ops_read_only_interface.py` → consumed by Connectome search + GraphReadOps for seed queries.

**External packages:**
- `falkordb` for graph database access.
- `pydantic` for node/link models.

---

## OBSERVABILITY & LINKS

### Bidirectional Links

- **Code → Docs:** tick, display snaps, cluster monitors point to `docs/physics/PATTERNS_Physics.md` and `algorithms/ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md`.
- **Docs → Code:** ALGORITHM steps map to `_flow_energy_to_narratives`, `_decay_energy`, `_detect_flips`.

### Docking & Observability

- **start:** orchestrator calls GraphTick with elapsed time.
- **flip_output:** returns flip list for handler/canon scheduling.
- **health anchor:** `docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md` references the per-mechanism functions for monitoring.

---

## GAPS / PROPOSITIONS

- Handler runtime wiring still pending (captured in SYNC).
- Speed controller and canon holder integrations remain future work increments.
