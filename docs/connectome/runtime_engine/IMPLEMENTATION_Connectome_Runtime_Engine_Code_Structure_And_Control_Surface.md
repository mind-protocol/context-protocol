```

# runtime_engine — Implementation: Code Architecture and Structure

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Runtime_Engine_Stepper_And_Realtime_Traversal_Control_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Runtime_Engine_User_Controlled_Traversal_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Runtime_Engine_Step_Release_And_Realtime_Scheduling.md
VALIDATION:      ./VALIDATION_Connectome_Runtime_Engine_Invariants_For_Stepper_And_Realtime.md
THIS:            IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md
HEALTH:          ./HEALTH_Connectome_Runtime_Engine_Runtime_Verification_Of_Pacing_And_Order.md
SYNC:            ./SYNC_Connectome_Runtime_Engine_Sync_Current_State.md

IMPL:            app/connectome/lib/next_step_gate_and_realtime_playback_runtime_engine (planned) (PROPOSED)
```

---

## CODE STRUCTURE

```
app/
└── connectome/
├── lib/
│   ├── next_step_gate_and_realtime_playback_runtime_engine (planned)
│   ├── minimum_duration_clamp_and_speed_based_default_policy (planned)
│   └── step_script_cursor_and_replay_determinism_helpers (planned)
```

### File Responsibilities

| File                                                       | Responsibility                                                    | Key Exports                                     |
| ---------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------- |
| `next_step_gate_and_realtime_playback_runtime_engine (planned)`   | command dispatch + step release gate + realtime attach (deferred) | `dispatch_runtime_command`, `release_next_step` |
| `minimum_duration_clamp_and_speed_based_default_policy (planned)` | duration policy + thresholds                                      | `compute_animation_duration_ms`                 |
| `step_script_cursor_and_replay_determinism_helpers (planned)`     | cursor movement + stable ids for stepper                          | `make_stepper_event_id`, `advance_cursor`       |

---

## DESIGN PATTERNS

### Architecture Pattern

* Gate + scheduler split by mode (stepper vs realtime)

### Code Patterns in Use

* pure helpers for deterministic outputs
* table-driven speed → default duration mapping

### Anti-Patterns to Avoid

* timers that release events in stepper mode
* direct store mutation from UI components
* duplicating event_model normalization

### Boundaries

| Boundary                 | Inside              | Outside                                 |
| ------------------------ | ------------------- | --------------------------------------- |
| Runtime control boundary | gating + scheduling | rendering, storage, telemetry transport |

---

## SCHEMA

### RuntimeCommand

(see PATTERNS)

### RuntimeReleaseResult

(see PATTERNS)

---

## ENTRY POINTS

| Entry Point                           | Trigger                                                |
| ------------------------------------- | ------------------------------------------------------ |
| `dispatch_runtime_command(cmd)`       | UI actions                                             |
| `release_next_step()`                 | called only from `dispatch_runtime_command(next_step)` |
| `attach_realtime_stream()` (deferred) | telemetry adapter                                      |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### stepper_next_step_release: Next click → one event

```
flow:
name: stepper_next_step_release
steps:
- id: cmd_received
file: app/connectome/lib/next_step_gate_and_realtime_playback_runtime_engine (planned)
function: dispatch_runtime_command
trigger: direct
output: RuntimeReleaseResult (released/blocked/end_of_script)
- id: normalize
file: app/connectome/lib/next_step_gate_and_realtime_playback_runtime_engine (planned)
function: release_next_step
trigger: direct
output: FlowEvent
notes: "calls event_model.normalize_flow_event"
- id: store_commit
file: app/connectome/state_store (?)
function: commit_release (?)
trigger: direct
output: state updated
docking_points:
- id: dock_runtime_release_result
type: event
direction: output
file: app/connectome/lib/next_step_gate_and_realtime_playback_runtime_engine (planned)
function: release_next_step
payload: RuntimeReleaseResult
notes: "HEALTH observes one-click-one-event"
```

---

## STATE MANAGEMENT

### Where State Lives

* cursor, mode, speed, pause in `state_store`

### State Transitions

(see runtime_engine PATTERNS)

---

## RUNTIME BEHAVIOR

### Initialization

* bind step script
* set defaults (mode=stepper, speed=pause)

### Main Loop / Request Cycle

* command-driven, synchronous per click

### Shutdown

* detach realtime subscription (deferred)

---

## CONCURRENCY MODEL

* serialize commands
* realtime queue drain policy deferred

---

## CONFIGURATION

| Config           | Default |
| ---------------- | ------- |
| MIN_ANIMATION_MS | 200     |
| DEFAULT_SPEED    | pause   |
| DEFAULT_MODE     | stepper |

---

## BIDIRECTIONAL LINKS

### Code → Docs

* add doc pointer headers to the TS files

### Docs → Code

* V1 invariants enforced by release_next_step

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

* if realtime introduces buffering complexity → extract buffer policy to a separate helper

### Missing Implementation

* [ ] implement runtime engine TS files
* [ ] add health runner (scripts/connectome/health/runtime_engine_health_check_runner (planned))

### Ideas

* IDEA: session boundaries for restart, preserve previous logs

### Questions

* QUESTION: Should restart clear ledger or mark boundary? (pending human decision)
