```

# runtime_engine — Validation: Invariants for Stepper Gating and Realtime Playback

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Runtime_Engine_Stepper_And_Realtime_Traversal_Control_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Runtime_Engine_User_Controlled_Traversal_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Runtime_Engine_Step_Release_And_Realtime_Scheduling.md
THIS:            VALIDATION_Connectome_Runtime_Engine_Invariants_For_Stepper_And_Realtime.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md
HEALTH:          ./HEALTH_Connectome_Runtime_Engine_Runtime_Verification_Of_Pacing_And_Order.md
SYNC:            ./SYNC_Connectome_Runtime_Engine_Sync_Current_State.md
```

---

## BEHAVIORS GUARANTEED

| Behavior ID | Behavior | Why This Validation Matters |
|-------------|----------|-----------------------------|
| B1 | Stepper Next clicks gate the runtime so a single FlowEvent release occurs, then the gate stays closed until the user explicitly advances again. | Guarantees researchers can trace every ledger entry back to an intentional click, preserving determinism and preventing ghost steps from polluting playback logs. |
| B2 | Speed selection only adjusts animation duration and presentation pacing, never the count or timing of released events when the runtime is in stepper mode. | Ensures temporal fidelity stays separate from authorization decisions, keeping approvals narrowly scoped to Next commands while still letting the UI feel responsive. |
| B3 | Minimum duration clamping forces each acknowledged release into a visible 200ms+ animation window even when upstream telemetry reports near-zero delays. | Keeps the runtime feeling “real” for observers, so rapid telemetry cannot collapse animations into imperceptible flashes that undermine trust in scenario playback. |

## OBJECTIVES COVERED

| Objective | Validations | Rationale |
|-----------|-------------|-----------|
| Keep each Next-driven step deterministic by tying ledger updates to a single click and preserving the replay sequence before the loop continues. | V1, V2, P1 | Prevents analysts from chasing multiple concurrent releases and makes regression tests reliable by ensuring the same script always yields the same FlowEvent ordering. |
| Block autoplay leaks and unauthorized releases so stepper mode never advances without explicit user consent even when speed controls are touched. | V2, E1, E2 | Forces the runtime to catch all boundary violations, so downstream dashboards and health probes can sound the alarm before autoplay undermines debug storytelling. |
| Keep perceived playback durations trustworthy by enforcing the minimum animation window regardless of how fast inputs or telemetry arrive. | V3 | Maintains human-scale timing, giving observers a stable pacing window for annotations and explanations even when the engine could render infinitely fast otherwise. |

---

## INVARIANTS

### V1: One Next click releases exactly one event (stepper mode)

```
IF mode==stepper AND command==next_step AND not end_of_script:
ledger_length increases by exactly 1
cursor increases by exactly 1
```

### V2: Speed does not change authorization (stepper mode)

```
IF mode==stepper:
changing speed must not change ledger_length or cursor
only affects computed animation duration defaults
```

### V3: Minimum duration clamp

```
FOR every released event:
animation_duration_ms >= 200ms
```

---

## PROPERTIES

### P1: Deterministic replay (stepper)

```
Given same step_script and same starting state:
sequence of released FlowEvents is identical (ignoring timestamps)
```

### P2: End-of-script is stable

```
After reaching end_of_script:
further next_step commands do not append events
```

---

## ERROR CONDITIONS

### E1: Double release per click

```
SYMPTOM: ledger_length increases by >1 for a single Next command
SEVERITY: ERROR
```

### E2: Autoplay leak in stepper mode

```
SYMPTOM: events released without a Next command when mode==stepper
SEVERITY: ERROR
```

---

## HEALTH COVERAGE

| Validation | Health Indicator                                 |
| ---------- | ------------------------------------------------ |
| V1         | runtime_stepper_single_step_integrity            |
| V2         | runtime_speed_authorization_separation           |
| V3         | runtime_min_duration_enforced                    |
| P1         | runtime_stepper_replay_determinism (optional v1) |
| E1/E2      | runtime_autoplay_leak_detector                   |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Click Next once → exactly one new log entry
[ ] Switch speed to 3x → click Next once → still exactly one entry
[ ] Run to end → click Next → no new entry; UI says end reached
[ ] Set a step duration to 10ms → animation still takes >=200ms
```

### Automated

```
pnpm connectome:health runtime_engine
```

---

# Run tests

```
pnpm connectome:health runtime_engine
```

# Run with coverage

```
pnpm connectome:health runtime_engine --coverage
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-20
VERIFIED_AGAINST:
impl: ?
health: ?
RESULT:
V1: NOT RUN
V2: NOT RUN
V3: NOT RUN
```

---

## GAPS / IDEAS / QUESTIONS

* QUESTION: Do we treat “Restart” as a new session boundary in determinism checks?
* IDEA: Add a “command ledger” (Next/Restart/Mode changes) for auditability (v2)

---

---
