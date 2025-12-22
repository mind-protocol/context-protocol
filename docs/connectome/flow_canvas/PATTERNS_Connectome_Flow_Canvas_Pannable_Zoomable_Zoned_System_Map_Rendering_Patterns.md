```

# flow_canvas — Patterns: Pannable/Zoomable Zoned Map with Stable Edge Readability

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
THIS:            PATTERNS_Connectome_Flow_Canvas_Pannable_Zoomable_Zoned_System_Map_Rendering_Patterns.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Flow_Canvas_Layout_Zones_And_Edge_Label_Decluttering.md
VALIDATION:      ./VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md
HEALTH:          ./HEALTH_Connectome_Flow_Canvas_Runtime_Verification_Of_Render_Stability_And_Perf_Budgets.md
SYNC:            ./SYNC_Connectome_Flow_Canvas_Sync_Current_State.md
```

The following behavior statements describe what the canvas must reliably do and what hazards it must prevent so the zoomable system map stays legible as complexity grows.

## BEHAVIORS SUPPORTED

* Interactive pan, zoom, fit-to-view, and reset controls keep camera motion responsive so analysts can zoom into dense clusters without losing the context of the current step in the runtime engine.
* Deterministic zone placement and label decluttering keep the FE/BE/GRAPH/AGENTS backdrops visible so focus transitions highlight the right region without hiding adjacent lanes.
* Stable edge glow, hover persistence, and node click hooks surface the current focus so the canvas reinforces runtime intent rather than merely showing a static projection.
* Camera transforms are limited to explicit UI actions so the navigation experience always matches the user's recent input and never drifts to an unexpected orientation.

## BEHAVIORS PREVENTED

* Prevents edges from disappearing by keying each connector to a stable identifier and factoring camera transforms out of the render loop so step transitions never drop or flicker lines.
* Prevents label overcrowding by decluttering noisy text until users zoom in, avoiding bold reflows that would overwhelm the tracing narrative when thousands of nodes spill into view.
* Prevents inadvertent layout jumps by only updating camera state via the dedicated controls, so stepper advances never trigger abrupt pan/zoom resets that would tear the spatial memory.

These behavior statements connect back to the health and validation narratives so the monitoring systems know what guarantees to verify when rendering large graphs.

### Bidirectional Contract

```
Before modifying this doc or the code:

1. Read ALL docs in this chain
2. Read event_model + state_store (canvas is a projection)

After modifying this doc:

* Update implementation OR record mismatch in SYNC

After modifying the code:

* Update docs OR record mismatch in SYNC

Never degrade:

* pan/zoom correctness
* edge label readability
* stable rendering (no disappearing edges)
  ```

---

## THE PROBLEM

The connectome diagram must function as a **debugging instrument**, not a poster.

The current failure modes (already observed):

* edges become unreadable (over-bold, overlapping labels)
* edges “disappear” during step transitions (resize/viewBox race)
* nodes are too close and visually ungrouped
* player vs UI vs hook nodes are not distinguishable
* no pan/zoom means you choose between “readable” and “fits on screen”

We need a canvas pattern that stays readable as complexity increases and can scale to thousands of nodes.

---

## THE PATTERN

**Force-directed projection with interactive camera (zones as optional context).**

* “Zones” are explicit containers:

  * FRONTEND
  * BACKEND
  * GRAPH
  * AGENTS
* Nodes are placed by a force-directed layout that scales to large graphs
* Zones remain as optional, low-contrast contextual backdrops
* Camera supports:

  * pan
  * zoom
  * fit-to-view
  * reset view

Key insight:

> If the diagram is a projection of a ledger, the layout must remain legible as the graph grows.
> We accept force layout to preserve scalability, then rely on zoom + hover for precision.

---

## PRINCIPLES

### Principle 1: Camera-first (pan/zoom) before layout cleverness

A readable diagram needs:

* space between nodes (no tight packing)
* pan/zoom to inspect without shrinking labels into noise
* “reset camera” to recover orientation

### Principle 2: Force layout for scale, stepper for semantics

The connectome “main data flow” is a system diagram, but the graph must scale to thousands of nodes:

* force layout preserves legibility under growth
* stepper semantics remain deterministic (one step per click)
* spatial memory is supported by consistent force parameters

### Principle 3: Label readability over style bravado

* link titles are NOT bold
* labels must remain readable at 100% zoom and not overwhelm nodes
* label background or halo should ensure contrast against edges

### Principle 4: Rendering stability is a correctness requirement

Edges must not disappear:

* no manual SVG viewBox recompute races
* stable edge objects keyed by id
* camera transforms must not detach edges from nodes

---

## DATA

| Data           | Description                                                              |
| -------------- | ------------------------------------------------------------------------ |
| `nodes[]`      | UI nodes with force-directed positions and zone membership               |
| `edges[]`      | Flow edges derived from FlowEvents (or a base map + active highlighting) |
| `active_focus` | which node/edge is active; glow persists                                 |
| `camera`       | x,y,zoom (view state)                                                    |
| `zones`        | FE/BE/GRAPH/AGENTS rectangles and labels                                 |

---

## DEPENDENCIES

| Module           | Why We Depend On It                                  |
| ---------------- | ---------------------------------------------------- |
| `state_store`    | provides nodes/edges list + active_focus             |
| `runtime_engine` | drives step releases that change active focus        |
| `edge_kit`       | provides edge types and visual components            |
| `node_kit`       | provides node renderers                              |
| `event_model`    | provides callType/trigger semantics used for styling |

---

## INSPIRATIONS

* React Flow / node editor UIs
* trace viewers with stable timelines
* “systems maps” with swimlanes (zones)

---

## SCOPE

### In Scope

* pannable/zoomable canvas camera behavior
* zone containers (visual grouping)
* deterministic layout strategy for v1
* label decluttering strategy (minimal but stable)
* fit-to-view + reset view controls

### Out of Scope

* node and edge styling details (owned by node_kit / edge_kit)
* log/explain panel (owned by log_panel)
* telemetry ingestion (owned by telemetry_adapter)
* health invariants for backend truth (not owned here)

---

## PATTERNS USED (SUB-PATTERNS)

### P1: Zoned containers as “semantic declutter”

Zones reduce cognitive load:

* users can instantly locate FE vs BE vs GRAPH vs AGENTS
* edges crossing zones become meaningful and easier to read

### P2: Stable keying and memoization of graph elements

Nodes and edges must be keyed by stable ids:

* node id: stable module/entity id
* edge id: stable link id (from FlowEvent or base map)

### P3: Layering: edges above nodes (but interaction-friendly)

* edges visually on top (as requested)
* but must still allow node interaction
* solution: edges in a higher visual layer with pointer events carefully controlled

---

## ENTRY POINTS

| Entry                                                         | Purpose                                                  |
| ------------------------------------------------------------- | -------------------------------------------------------- |
| `render_connectome_canvas(nodes, edges, zones, active_focus)` | projection render                                        |
| `set_camera_pan_zoom(new_state)`                              | camera updates                                           |
| `fit_view_to_zones()`                                         | reset/fit                                                |
| `on_node_click(node_id)`                                      | interacts with runtime (player message, pin focus, etc.) |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### canvas_renders_store_projection

```
flow:
name: canvas_renders_store_projection
purpose: Render stable map from store state.
steps:
- read nodes/edges/zones/active_focus from store selectors
- render zones first
- render nodes and edges with stable keys
- apply active_focus glow persistence
- apply camera transform
docking_points:
- dock_canvas_render_commit (event): used by HEALTH for “no disappearing edges”
```

---

## MARKERS

* [ ] Tune force parameters for very large graphs (nodes > 1k).
* IDEA: optional “declutter toggle” hides secondary labels until zoom > threshold.
* QUESTION: do we need minimap in v1? (nice-to-have)

---

---
