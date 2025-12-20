```

# state_store — Implementation: Code Architecture and Structure

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_State_Store_Single_Source_Of_Truth_For_Events_Focus_And_Timers.md
BEHAVIORS:       ./BEHAVIORS_Connectome_State_Store_Observable_State_Consistency_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_State_Store_Atomic_Commits_For_Step_Releases_And_Realtime.md
VALIDATION:      ./VALIDATION_Connectome_State_Store_Invariants_For_Ledger_Ordering_And_Focus.md
THIS:            IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md
HEALTH:          ./HEALTH_Connectome_State_Store_Runtime_Verification_Of_Ledger_And_Timer_Correctness.md
SYNC:            ./SYNC_Connectome_State_Store_Sync_Current_State.md

IMPL:            app/connectome/lib/zustand_connectome_state_store_with_atomic_commit_actions (planned) (PROPOSED)
```

---

## CODE STRUCTURE

```
app/
└── connectome/
├── lib/
│   ├── zustand_connectome_state_store_with_atomic_commit_actions (planned)
│   ├── connectome_session_boundary_and_restart_policy_controller (planned)
│   ├── connectome_wait_timer_progress_and_tick_display_signal_selectors (planned)
│   └── connectome_export_jsonl_and_text_log_serializer (planned)
```

### File Responsibilities

| File                                                                  | Responsibility                   | Key Exports                                       |
| --------------------------------------------------------------------- | -------------------------------- | ------------------------------------------------- |
| `zustand_connectome_state_store_with_atomic_commit_actions (planned)`        | store state + long-named actions | `useConnectomeStore`                              |
| `connectome_session_boundary_and_restart_policy_controller (planned)`        | implements restart policy A/B    | `restart_session_*`                               |
| `connectome_wait_timer_progress_and_tick_display_signal_selectors (planned)` | selectors for wait/tick widgets  | `selectWaitProgress`, `selectTickDisplay`         |
| `connectome_export_jsonl_and_text_log_serializer (planned)`                  | stable copy/export               | `serializeLedgerToJsonl`, `serializeLedgerToText` |

---

## DESIGN PATTERNS

* Single store authority (Zustand)
* atomic commit action for each release
* pure selectors for derived time values (avoid scattered timers)

---

## ENTRY POINTS

| Entry Point                                                        | Trigger                     |
| ------------------------------------------------------------------ | --------------------------- |
| `commit_step_release_append_event_and_set_focus_and_explanation()` | runtime_engine step release |
| `restart_session_clear_or_boundary()`                              | user Restart                |
| `serializeLedgerToJsonl()`                                         | Copy/export button          |

---

## DATA FLOW AND DOCKING

### store_atomic_commit: runtime release → store update

```
flow:
name: store_atomic_commit
steps:
- runtime_engine calls commit action with {event, focus, explanation, timer actions}
- store mutates ledger + focus + explanation in one transaction
docking_points:
- dock_store_commit_action_invoked (event): for HEALTH
```

---

## STATE MANAGEMENT

State is the product here.

* keep ledger immutable by copying array on append
* keep focus singular
* keep explanation as one sentence

---

## CONFIGURATION

| Config                 | Default | Notes                             |
| ---------------------- | ------- | --------------------------------- |
| `MAX_WAIT_SECONDS`     | 4.0     | progress cap                      |
| `RETENTION_MAX_EVENTS` | ?       | realtime retention cap (deferred) |
| `RESTART_POLICY`       | ?       | clear vs boundary                 |

---

## BIDIRECTIONAL LINKS

### Code → Docs

* store file header references docs/connectome/state_store/*

### Docs → Code

* validation invariants are implemented as store health checks

---

## GAPS / IDEAS / QUESTIONS

* [ ] Decide RESTART_POLICY and lock it (docs + code)
* [ ] Decide retention cap for realtime mode
