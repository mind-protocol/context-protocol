```

# node_kit — Implementation: Component Map and Styling Tokens

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Node_Kit_Typed_Language_Coded_Energy_Aware_Node_Rendering_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Node_Kit_Visible_Clarity_And_Trust_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Node_Kit_Node_Rendering_Spec_And_Energy_Glow_Mapping.md
VALIDATION:      ./VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md
THIS:            IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md
HEALTH:          ./HEALTH_Connectome_Node_Kit_Runtime_Verification_Of_Node_State_And_Visual_Signal_Truth.md
SYNC:            ./SYNC_Connectome_Node_Kit_Sync_Current_State.md

IMPL:            app/connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting (planned) (PROPOSED)
```

---

## CODE STRUCTURE

```
app/
└── connectome/
├── components/
│   └── node_kit/
│       ├── typed_connectome_node_components_with_energy_and_step_highlighting (planned)
│       ├── connectome_node_frame_with_title_path_and_tooltip_shell (planned)
│       ├── connectome_energy_badge_bucketed_glow_and_value_formatter (planned)
│       ├── connectome_player_wait_progress_bar_with_four_second_cap (planned)
│       ├── connectome_tick_cron_circular_progress_ring_with_speed_label (planned)
│       ├── connectome_node_background_theme_tokens_by_type_and_language (planned)
│       └── connectome_node_step_list_and_active_step_highlighter (planned)
```

### File Responsibilities

| File                                                                     | Responsibility                                         | Key Exports                                                                                         |
| ------------------------------------------------------------------------ | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| `typed_connectome_node_components_with_energy_and_step_highlighting (planned)` | exports node variants used by flow_canvas              | `PlayerNode`, `UiNode`, `ModuleNode`, `GraphQueriesNode`, `MomentNode`, `AgentNode`, `TickCronNode` |
| `connectome_node_frame_with_title_path_and_tooltip_shell (planned)`            | shared rounded frame (“more circled”) + tooltip anchor | `NodeFrame`                                                                                         |
| `connectome_energy_badge_bucketed_glow_and_value_formatter (planned)`          | energy value display + deterministic glow mapping      | `EnergyBadge`                                                                                       |
| `connectome_player_wait_progress_bar_with_four_second_cap (planned)`           | wait progress bar widget                               | `PlayerWaitProgressBar`                                                                             |
| `connectome_tick_cron_circular_progress_ring_with_speed_label (planned)`       | tick cron ring widget                                  | `TickCronRing`                                                                                      |
| `connectome_node_background_theme_tokens_by_type_and_language (planned)`        | token tables for background + title colors             | `themeForNodeTypeAndLanguage`                                                                       |
| `connectome_node_step_list_and_active_step_highlighter (planned)`              | renders steps list + active highlight                  | `StepList`                                                                                          |

---

## STYLING TOKENS (V1)

### Node background categories

* Player: distinct warm tint (not yellow moment tint)
* UI: cool neutral tint
* Module TS: blue tint
* Module PY: purple tint
* GraphQueries: purple tint (distinct from PY by accent ?)
* Moment: yellow tint
* Agent: green tint
* TickCron: speed-coded tint

### Energy mapping tokens

* grey bucket: low energy
* blue bucket: medium-low
* orange bucket: medium-high
* yellow bucket: high energy

---

## ENTRY POINTS

| Entry Point                           | Used By               |
| ------------------------------------- | --------------------- |
| `PlayerNode`                          | flow_canvas           |
| `ModuleNode`                          | flow_canvas           |
| `AgentNode` (Narrator, World Builder) | flow_canvas           |
| `EnergyBadge`                         | all nodes with energy |
| `StepList`                            | nodes with steps list |

---

## DATA FLOW AND DOCKING

node_kit consumes store selectors only; no writes.

```
flow:
name: node_kit_renders_store_projection
steps:
- flow_canvas passes view model + active focus
- node_kit renders deterministic visuals and widgets
docking_points:
- none required (HEALTH probes DOM/test harness)
```

---

## CONFIGURATION

| Config                     | Default                  |
| -------------------------- | ------------------------ |
| `ENERGY_BUCKET_THRESHOLDS` | [0.10, 0.30, 0.60]       |
| `WAIT_MAX_SECONDS`         | 4.0                      |
| `TITLE_PROMINENCE`         | enforced by style tokens |

---

## BIDIRECTIONAL LINKS

* each node_kit TSX should reference docs/connectome/node_kit/*
* update SYNC when energy threshold tokens change

---

## GAPS / IDEAS / QUESTIONS

* [ ] Decide whether GraphQueries node should be a ModuleNode with call_type=graphQuery styling, or a separate node type (currently separate for clarity).
* QUESTION: Do we display both “language” and “call_type” badges, or only one?
