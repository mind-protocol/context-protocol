# flow_canvas — Sync: Current State

LAST_UPDATED: 2026-04-08
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**Canonical (v1 intent):**

* pannable/zoomable system map
* zones FE/BE/GRAPH/AGENTS
* deterministic layout
* stable edge rendering (no disappearance)

**In design:**

* label declutter thresholds
* minimap and drag behavior (deferred)

---

## CURRENT STATE

Implemented a React Flow-based FlowCanvas with force-directed node layout seeded by zones, stable edge rendering, and pannable/zoomable camera. Zones render as background nodes, and edges are keyed and stable. Fit-to-view is available via a small overlay button.

---

## RECENT CHANGES

### 2025-12-20: Switched node layout to force-directed for scale

* **What:** Added force-directed layout (d3-force) seeded by zone positions and linked by edges.
* **Why:** Support thousands of nodes without manual layout while preserving readability.
* **Files:** `app/connectome/components/deterministic_zone_and_node_layout_computation_helpers.ts`, `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`.

### 2025-12-20: Implemented FlowCanvas with zones + deterministic layout

* **What:** Added React Flow renderer, zone nodes, deterministic node positions, and stable edge list.
* **Why:** Provide a readable, stable canvas as a debugging instrument in v1.
* **Files:** `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`, `app/connectome/components/deterministic_zone_and_node_layout_computation_helpers.ts`.

### 2025-12-21: Filtered search edges without endpoints

* **What:** Filtered search edges to only render links with both endpoints present.
* **Why:** Avoid React Flow edge warnings and invalid edge entries when graph data is incomplete.
* **Files:** `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`.

### 2025-12-21: Added LOD throttling for large graphs

* **What:** Reduced node/edge rendering detail based on zoom and graph size (hide labels, steps, motion).
* **Why:** Prevent 1fps when rendering large graphs.
* **Files:** `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`, `app/connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.tsx`, `app/connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.tsx`, `app/connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`, `app/connectome/connectome.css`.

### 2025-12-21: Switched canvas renderer to WebGL

* **What:** Replaced React Flow rendering with a custom WebGL canvas + label overlay.
* **Why:** Maintain interactive performance on large graphs (WebGL points/lines).
* **Files:** `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`, `app/connectome/connectome.css`.

### 2026-04-08: Fill validation template drift sections for flow_canvas (#11)

* **What:** Added the missing BEHAVIORS GUARANTEED, OBJECTIVES COVERED, PROPERTIES, and SYNC STATUS sections to `VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md` and expanded each narrative so the template now exceeds fifty characters per block.
* **Why:** Completes DOC_TEMPLATE_DRIFT #11 for the validation doc and gives downstream agents a document that explicitly links behaviors, objectives, invariants, and syncing evidence.
* **Files:** `docs/connectome/flow_canvas/VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md`

### 2026-04-07: Add flow canvas behavior objectives and I/O (#11)

* **What:** Documented OBJECTIVES SERVED plus INPUTS/OUTPUTS details in `BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md` so the template now describes the goals and data contracts for the canvas.
* **Why:** DOC_TEMPLATE_DRIFT #11 highlighted the missing sections, and the new narrative keeps the canonical behavior doc aligned with the rest of the chain.
* **Files:** `docs/connectome/flow_canvas/BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md`

---

## TODO

* [ ] Implement label declutter hooks in edge rendering (optional v1)
* [ ] Add a minimap only if navigation becomes painful

Run:

```
pnpm connectome:health flow_canvas
```

---

## HANDOFF

**For agents:**

* Keep deterministic layout; do not introduce force layout in v1.
* Ensure edges keep stable ids and do not disappear on step transitions.

**For human:**

* Fit-to-view is implemented; node dragging remains disabled for determinism.

---
