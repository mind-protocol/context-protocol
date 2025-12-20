```

# edge_kit — Implementation: Component Map and Render Tokens

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Edge_Kit_Color_Coded_Trigger_Typed_Directional_Link_Styling_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Edge_Kit_Readable_Directional_And_Truthful_Link_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Edge_Kit_Edge_Rendering_Pulse_Shine_And_Label_Placement_Rules.md
VALIDATION:      ./VALIDATION_Connectome_Edge_Kit_Invariants_For_Color_Dash_And_Pulse_Truth.md
THIS:            IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md
HEALTH:          ./HEALTH_Connectome_Edge_Kit_Runtime_Verification_Of_Link_Visibility_And_Semantic_Styling.md
SYNC:            ./SYNC_Connectome_Edge_Kit_Sync_Current_State.md

IMPL:            app/connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses (planned) (PROPOSED)
```

---

## CODE STRUCTURE

```
app/
└── connectome/
├── components/
│   └── edge_kit/
│       ├── semantic_edge_components_with_directional_shine_and_pulses (planned)
│       ├── connectome_edge_style_tokens_for_trigger_and_calltype_mapping (planned)
│       ├── connectome_edge_label_renderer_with_halo_and_zoom_policy (planned)
│       ├── connectome_edge_directional_shine_animation_helpers (planned)
│       ├── connectome_edge_pulse_particle_animation_and_boundary_clamp_helpers (planned)
│       └── connectome_node_boundary_intersection_geometry_helpers (planned)
```

### File Responsibilities

| File                                                                     | Responsibility                      | Key Exports                             |
| ------------------------------------------------------------------------ | ----------------------------------- | --------------------------------------- |
| `semantic_edge_components_with_directional_shine_and_pulses (planned)`         | Edge components used by flow_canvas | `DirectEdge`, `StreamEdge`, `AsyncEdge` |
| `connectome_edge_style_tokens_for_trigger_and_calltype_mapping (planned)`       | strict mappings                     | `styleForTrigger`, `colorForCallType`   |
| `connectome_edge_label_renderer_with_halo_and_zoom_policy (planned)`           | label rendering (not bold)          | `EdgeLabel`                             |
| `connectome_edge_directional_shine_animation_helpers (planned)`                 | shine animation definitions         | `makeShineStroke`                       |
| `connectome_edge_pulse_particle_animation_and_boundary_clamp_helpers (planned)` | pulses, magnitude scaling           | `renderPulse`, `computePulseDuration`   |
| `connectome_node_boundary_intersection_geometry_helpers (planned)`              | clamp endpoints at node edges       | `intersectWithRoundedRect`              |

---

## RENDER TOKENS (V1)

### Base widths (less bold)

* base: 2.5
* active: 3.5

### Call type colors

* graphLink: yellow/orange
* graphQuery: purple
* code: blue
* llm: green

### Label

* font weight normal
* halo/stroke always on
* color matches edge

---

## ENTRY POINTS

| Entry                             | Used By             |
| --------------------------------- | ------------------- |
| `DirectEdge/StreamEdge/AsyncEdge` | flow_canvas         |
| `EdgeLabel`                       | edge components     |
| `intersectWithRoundedRect`        | pulse clamp helpers |

---

## DATA FLOW AND DOCKING

Edges consume edge view models produced by flow_canvas (which reads store).

```
flow:
name: edge_kit_renders_edge_view_models
steps:
- flow_canvas passes edge view model
- edge_kit maps trigger/call_type to style tokens
- edge_kit renders label + shine + pulses
docking_points:
- none in code; HEALTH reads styles via probes
```

---

## CONFIGURATION

| Config                 | Default |
| ---------------------- | ------- |
| MIN_PULSE_MS           | 200     |
| SHINE_AMPLITUDE_STREAM | higher  |
| SHINE_AMPLITUDE_DIRECT | subtle  |

---

## GAPS / IDEAS / QUESTIONS

* [ ] Decide whether hook/timer triggers need unique visuals beyond dotted/dashed.
* QUESTION: do we allow graphLink subtypes to shift yellow/orange?
