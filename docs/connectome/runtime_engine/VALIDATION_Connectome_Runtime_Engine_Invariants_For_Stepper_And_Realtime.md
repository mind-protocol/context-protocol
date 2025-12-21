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
| B1 | Each Next command in stepper mode releases exactly one FlowEvent and then holds the gate closed until an explicit follow-up click occurs. | Validating this keeps every ledger entry tied to an intentional action, preserving deterministic replay and auditability even when UI jitter or retries happen. |
| B2 | Adjusting the speed slider only tunes animation duration and presentation pacing, never the ledger length, cursor, or count of FlowEvents released in stepper mode. | This keeps authorization decisions separate from animation feel, so auditors and automations can trust that the speed control never secretly advances the script. |
| B3 | Every release obeys the runtime’s 200ms minimum animation window so realtime playback cannot collapse into imperceptible bursts that disguise rapid autoplayer pulses. | The pacing guard ensures observers, telemetry, and downstream health probes see the same perceptible cadence, preventing autoplayer bursts from undermining trust. |

## OBJECTIVES COVERED

| Objective | Validations | Rationale |
|-----------|-------------|-----------|
| Keep the Next button bounded to a single deterministic release so ledger updates, cursors, and log entries stay predictable before the loop continues. | V1, P1 | This objective prevents the runtime from producing multiple FlowEvents per command, making replay tests reproducible and analyses confident in the script ordering. |
| Keep speed adjustments purely as duration knobs and block unauthorized autoplay so the runtime never advances without explicit user consent. | V2, E1, E2 | Verifying V2 plus the error conditions ensures downstream tooling can detect any boundary violation that would let autoplay leak past the gate when speed or telemetry shifts. |
| Maintain human-scale pacing by enforcing the 200ms minimum duration clamp so viewers always perceive each release before the next command. | V3 | The clamp keeps pacing aligned with telemetry and narrative expectations, ensuring autoplayer bursts remain obvious and do not masquerade as legitimate rehearsals. |

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
