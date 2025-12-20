```

# flow_canvas — Implementation: Code Architecture and Structure

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Flow_Canvas_Pannable_Zoomable_Zoned_System_Map_Rendering_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Flow_Canvas_Layout_Zones_And_Edge_Label_Decluttering.md
VALIDATION:      ./VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md
THIS:            IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md
HEALTH:          ./HEALTH_Connectome_Flow_Canvas_Runtime_Verification_Of_Render_Stability_And_Perf_Budgets.md
SYNC:            ./SYNC_Connectome_Flow_Canvas_Sync_Current_State.md

IMPL:            app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer (planned) (PROPOSED)
```

---

## CODE STRUCTURE

```
app/
└── connectome/
├── components/
│   ├── pannable_zoomable_zoned_flow_canvas_renderer (planned)
│   ├── deterministic_zone_and_node_layout_computation_helpers (planned)
│   └── edge_label_declutter_and_visibility_policy_helpers (planned)
```

### File Responsibilities

| File                                                        | Responsibility                              | Key Components/Exports                   |
| ----------------------------------------------------------- | ------------------------------------------- | ---------------------------------------- |
| `pannable_zoomable_zoned_flow_canvas_renderer (planned)`          | renders zones + nodes + edges with pan/zoom | `FlowCanvas`                             |
| `deterministic_zone_and_node_layout_computation_helpers (planned)` | compute positions from node list            | `computeZones`, `computeNodePositions`   |
| `edge_label_declutter_and_visibility_policy_helpers (planned)`     | label placement offsets and zoom policy     | `computeLabelAnchors`, `shouldShowLabel` |

---

## DESIGN PATTERNS

* stable keyed elements (ids never change)
* deterministic layout (no force)
* camera controls: fit/reset/pan/zoom

---

## ENTRY POINTS

| Entry Point                                 | Trigger                                   |
| ------------------------------------------- | ----------------------------------------- |
| `FlowCanvas()`                              | /connectome page render                   |
| `computeZones(viewport)`                    | on init and on resize                     |
| `computeNodePositions(nodes, zones)`        | on node list change (not on focus change) |
| `computeLabelAnchors(edges, nodePositions)` | on edge list change                       |

---

## DATA FLOW AND DOCKING

### store_projection_to_canvas

```
flow:
name: store_projection_to_canvas
steps:
- read node list + edge list + active focus from store
- compute positions (only when topology changes)
- render FlowCanvas with edge_kit and node_kit components
docking_points:
- dock_canvas_rendered_edge_ids (metric): used by HEALTH to detect missing edges
```

---

## CONFIGURATION

| Config            | Default    |
| ----------------- | ---------- |
| `NODE_SPACING_X`  | 260        |
| `NODE_SPACING_Y`  | 180        |
| `LABEL_MIN_ZOOM`  | 0.8 (?)    |
| `ALLOW_NODE_DRAG` | false (v1) |

---

## BIDIRECTIONAL LINKS

* canvas TSX should reference this doc chain
* health harness should reference VALIDATION invariants

---

## GAPS / IDEAS / QUESTIONS

* QUESTION: adopt React Flow as dependency (recommended) or implement custom canvas? (v1: React Flow)
* IDEA: minimap toggle in top-right for navigation
