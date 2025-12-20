# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
```

---

## CURRENT STATE

The CLI is in active use while fixes continue to land in the repair subsystem. A SyntaxError in `ngram/repair_core.py` was blocking `ngram --agents` from importing; the function was repaired and retry state initialized. Verification of the CLI run is still pending.

---

## ACTIVE WORK

### Repair CLI import failure

- **Area:** `cli/`
- **Status:** completed (needs verification)
- **Owner:** codex
- **Context:** Fixed SyntaxError and missing retry state in `spawn_repair_agent_async` that prevented CLI startup.

---

## RECENT CHANGES

### 2025-12-20: Escalation resolution for AGENTS.md deferred

- **What:** Reviewed escalation task for `AGENTS.md` and confirmed no human decisions were provided.
- **Why:** The issue requires explicit decisions before conflicts can be resolved.
- **Impact:** No doc changes made for this escalation; awaiting human input.

### 2025-12-20: Fix repair_core async SyntaxError

- **What:** Wrapped `spawn_repair_agent_async` in a proper try/except, initialized retry counters, recorded Gemini fallback state, and imported `DoctorConfig` in `ngram/repair.py`.
- **Why:** `ngram --agents codex` failed to import due to a mismatched `except` and missing variables.
- **Impact:** CLI import path should be restored; agent spawning retry state is now defined.

### 2025-12-20: Fix TUI repair agent config wiring

- **What:** Passed DoctorConfig into the TUI `spawn_repair_agent_async` call.
- **Why:** TUI repair runs failed with "missing 1 required positional argument: config".
- **Impact:** TUI repair flow should run without the config argument error.
- **Follow-up:** Stored and reused DoctorConfig for queued agent spawns to avoid NameError in later steps.

### 2025-12-20: Resolved BROKEN_IMPL_LINK and STALE_IMPL issues

- **What:** Corrected all `BROKEN_IMPL_LINK` references in `docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md`, `docs/protocol/IMPLEMENTATION_Protocol_System_Architecture.md`, `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_Protocol_File_Structure.md`, and `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md`.
- **Why:** To resolve broken links caused by the `ngram/utils.py` to `ngram/core_utils.py` rename and the documentation renames, and to prevent `STALE_IMPL` warnings.
- **Impact:** The codebase documentation now accurately reflects the file structure and dependencies, improving agent navigation and project health scores.

### 2025-12-20: Fix ModuleNotFoundError and acknowledge documentation renames

- **What:** Pending detail from prior work (not updated here).
- **Why:** Pending detail from prior work (not updated here).
- **Impact:** Pending detail from prior work (not updated here).

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| CLI fix not verified | warning | `cli/` | `ngram --agents codex` should be rerun to confirm import now succeeds |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** `VIEW_Debug_Investigate_And_Fix_Issues.md`

**Current focus:** Verify CLI import (`ngram --agents codex`) and ensure repair agent flow still runs.

**Key context:**
`spawn_repair_agent_async` had a mismatched `except` and undefined retry variables; these were repaired.

**Watch out for:**
`spawn_repair_agent` in `ngram/repair.py` returns a coroutine; double-check sync call sites if issues persist.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Fixed a SyntaxError in `ngram/repair_core.py` that prevented `ngram --agents codex` from starting. The code now initializes retry counters and aligns exception handling, but the CLI run still needs verification.

**Decisions made recently:**
Added a single retry/fallback path for Gemini model selection when agent command setup fails.

**Needs your input:**
Confirm whether you want me to run `ngram --agents codex` now for verification.

**Concerns:**
`spawn_repair_agent` returns the async coroutine directly; if any callers assume sync behavior, it may require follow-up.

---

## TODO

### High Priority

- [ ] Verify `ngram --agents codex` now runs without import errors.

### Backlog

- [ ] Reconcile remaining placeholder entries in this SYNC file.
- IDEA: Add a quick CLI smoke test for agent command imports.

---

## CONSCIOUSNESS TRACE

**Project momentum:**
Moving; recent fixes were focused on unblocking CLI usage.

**Architectural concerns:**
Mixed sync/async repair agent paths could be confusing if not documented.

**Opportunities noticed:**
Add a lightweight smoke test for CLI imports to prevent regressions.

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `cli/` | active | `docs/cli/SYNC_CLI_Development_State.md` |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Mapped modules:**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| cli | `ngram/` | `docs/cli/` | CANONICAL |

**Unmapped code:** (run `ngram validate` to check)
- Not reviewed in this change set.

**Coverage notes:**
`modules.yaml` may still be template-only; reconcile in a dedicated task.
