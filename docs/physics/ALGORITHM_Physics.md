# Physics — Algorithm: System Overview

```
CREATED: 2024-12-18
UPDATED: 2025-12-20
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Physics.md
BEHAVIORS:      ./BEHAVIORS_Physics.md
THIS:           ALGORITHM_Physics.md (you are here)
SCHEMA:         ../schema/SCHEMA_Moments.md
VALIDATION:     ./VALIDATION_Physics.md
IMPLEMENTATION: ./IMPLEMENTATION_Physics.md
HEALTH:         ./HEALTH_Physics.md
SYNC:           ./SYNC_Physics.md
```

---

## Consolidation Note

This algorithm is now split into focused documents to reduce size and make
review more targeted. The overview stays here; deep dives live in the
linked algorithm docs below.

## OVERVIEW

This algorithm describes the physics engine that moves energy through the
graph, detects flips, and hands off work to handlers, canon, and display
control. The intent is to keep all authoritative state in the graph while
the tick cycle applies deterministic propagation rules.

---

## DETAILED ALGORITHMS

- `algorithms/ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md`
  — canonical physics algorithm covering energy mechanics, flow sources/sinks, tick cycle, handler/input processing, and speed control behaviors.
- `algorithms/ALGORITHM_Physics_Mechanisms.md` (function-level mapping to code)

## LEGACY ALGORITHM REDIRECTS

- `algorithms/ALGORITHM_Physics_Energy_Flow_Sources_Sinks_And_Moment_Dynamics.md`
- `algorithms/ALGORITHM_Physics_Tick_Cycle_Gating_Flips_And_Dispatch.md`
- `algorithms/ALGORITHM_Physics_Handler_And_Input_Processing_Flows.md`
- `algorithms/ALGORITHM_Physics_Speed_Control_And_Display_Filtering.md`
  — stubs that point readers to the canonical algorithm above.

## DATA STRUCTURES

- Graph nodes for Characters, Narratives, Moments with `weight` and `energy`.
- Graph links for BELIEVES/ABOUT/SUPPORTS/etc. with `strength` and optional
  routing attributes like `presence_required` and `require_words`.
- Tick context: current tick index, decay constants, and pending flip results.
- Queues: handler outputs (potential moments) and canon records (actualized).

---

## ALGORITHM: Physics Tick Cycle

Primary function: `run_physics_tick()` (conceptual name for the per-tick loop).

1. Load active characters and their BELIEVES/ORIGINATED links.
2. Pump character energy into narratives using link strengths.
3. Route narrative energy across narrative-to-narrative links (zero-sum).
4. Push energy to moments via ATTACHED_TO and CAN_SPEAK links.
5. Apply decay and clamp weights/energy to minimum thresholds.
6. Compute salience and detect flips for moments and narratives.
7. Emit flip results to handlers and canon recording pipeline.
8. Persist updated weights/energy to the graph and return tick summary.

---

## KEY DECISIONS

- Energy is the proximity signal; no separate proximity layer exists.
- Links only route energy; creation happens via character pumps or input.
- The graph is the only source of truth; ticks never cache authoritative state.
- Zero-sum transfers preserve energy while decay and actualization drain it.

---

## DATA FLOW

Graph queries load current node/link state → tick computes injections and
transfers → updates are written back to the graph → flip events are surfaced
to handlers and canon holder → display layer filters by speed settings.

---

## COMPLEXITY

Per tick cost is proportional to the number of active characters, their
adjacent BELIEVES/ABOUT links, and reachable narrative edges. Worst case is
O(V+E) over the active subgraph; practical runs are bounded by salience
filters and query limits in graph ops.

---

## HELPER FUNCTIONS

- `salience(node)` multiplies weight and energy to rank surfacing.
- `reinforce_link()` and `challenge_link()` adjust strengths with clamps.
- `apply_decay()` reduces energy/weight based on real-time elapsed.
- `is_interrupt()` classifies moments for 3x snap-to-1x transitions.

---

## INTERACTIONS

- Handlers read flip outputs to generate new potential moments.
- Canon holder records actualized moments and THEN links.
- Speed controller adjusts tick interval and display filtering rules.
- GraphOps/GraphQueries provide the mutation and read API used by ticks.

---

## MARKERS

- Handler runtime and canon holder code are planned but not fully implemented.
- Energy constants (pump rates, thresholds) still need playtesting.
- Question Answerer async integration depends on infrastructure readiness.

---
