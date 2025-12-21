```

# runtime_engine — Sync: Current State

LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**Canonical (v1 intent):**

* stepper: Next releases exactly one event
* speed modifies duration only, never authorization
* min duration clamp 200ms

**In design:**

* restart policy (boundary vs clear) now set to boundary event
* realtime buffering (deferred)

**Deferred:**

* realtime adapter wiring
* buffering policy and retention

---

## CURRENT STATE

Stepper runtime engine is implemented with a fixed step script. Next dispatches exactly one event through FlowEvent normalization and an atomic store commit. Speed affects animation duration but does not release additional events.

---

## RECENT CHANGES

### 2025-12-20: Implemented stepper runtime engine

* **What:** Added runtime command dispatch, step release logic, and initialization that sets script total.
* **Why:** Enforce stepper gating semantics and connect UI controls to a single release path.
* **Files:**
  * `app/connectome/lib/next_step_gate_and_realtime_playback_runtime_engine.ts`
  * `app/connectome/lib/minimum_duration_clamp_and_speed_based_default_policy.ts`
  * `app/connectome/lib/step_script_cursor_and_replay_determinism_helpers.ts`
  * `app/connectome/lib/connectome_step_script_sample_sequence.ts`

---

### 2026-04-17: Complete runtime engine health template narratives (Closes #11)

* **What:** Added a full OBJECTIVES COVERAGE table plus individual indicator stories for the pacing, speed, duration, and autoplay checks so the health doc now describes every required metric, dock, and threat with ≥50-character prose.
* **Why:** DOC_TEMPLATE_DRIFT #11 flagged missing objectives and indicator sections; the new narratives clarify what each signal defends and the guardrails downstream agents must audit.
* **Files:** `docs/connectome/runtime_engine/HEALTH_Connectome_Runtime_Engine_Runtime_Verification_Of_Pacing_And_Order.md`, `docs/connectome/runtime_engine/SYNC_Connectome_Runtime_Engine_Sync_Current_State.md`, `.ngram/state/SYNC_Project_State.md`
* **Validation:** Pending the next `ngram validate` run; the change is purely documentation.

### 2026-04-18: Refine runtime_engine health coverage (#11)

* **What:** Reworked the OBJECTIVES COVERAGE table and added detailed indicator sections for speed, duration, and autoplay so every health signal now documents validation targets, docking points, and forwardings.
* **Why:** The doctor still flagged DOC_TEMPLATE_DRIFT for missing indicator details and objective coverage; adding the narratives keeps the runtime_engine health doc canonical for downstream agents.
* **Files:**
  * `docs/connectome/runtime_engine/HEALTH_Connectome_Runtime_Engine_Runtime_Verification_Of_Pacing_And_Order.md`
  * `docs/connectome/runtime_engine/SYNC_Connectome_Runtime_Engine_Sync_Current_State.md`
* **Verification:** `ngram validate`

---

## TODO

* [ ] Define realtime mode behavior once telemetry_adapter exists
* [ ] Decide whether restart should clear ledger vs boundary (currently boundary event)

Run:

```
pnpm connectome:health runtime_engine
```

---
