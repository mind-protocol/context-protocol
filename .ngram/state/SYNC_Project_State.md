# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: codex (tui doctor-ignore sync)
```

---

## CURRENT STATE

TUI implementations are complete, but doctor was flagging short delegating methods as incomplete. This update aligns doctor-ignore with actual TUI behavior and records the change in TUI sync.

---

## ACTIVE WORK

### TUI doctor alignment

- **Area:** `ngram/tui/`
- **Status:** complete
- **Owner:** agent
- **Context:** Suppressed false-positive INCOMPLETE_IMPL findings for TUI app/input/manager panels.

---

## RECENT CHANGES

### 2025-12-19: Suppressed false-positive TUI INCOMPLETE_IMPL

- **What:** Added doctor-ignore entries for `ngram/tui/app.py`, `ngram/tui/widgets/input_bar.py`, and `ngram/tui/widgets/manager_panel.py`.
- **Why:** Doctor flagged short delegating methods that are already fully implemented.
- **Impact:** Doctor no longer reports these false positives.

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| Broken CHAIN links in doctor feature docs | medium | `docs/protocol/features/doctor/` | `ngram validate` reports missing IMPLEMENTATION_Project_Health_Doctor.md links. |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** `VIEW_Implement_Write_Or_Modify_Code.md`

**Current focus:** Keep doctor-ignore aligned with actual TUI implementation and update SYNCs when suppressing findings.

**Key context:**
TUI false positives are now suppressed in `.ngram/doctor-ignore.yaml`.

**Watch out for:**
Doctor flags functions with <=2 body lines as incomplete.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Doctor false positives for TUI short methods are now suppressed, and the TUI sync reflects that change.

**Decisions made recently:**
Marked `ngram/tui/app.py` and related widgets as intentional minimal implementations in doctor-ignore.

**Needs your input:**
None.

**Concerns:**
None.

---

## TODO

### High Priority

- [ ] None.

### Backlog

- [ ] None.

---

## CONSCIOUSNESS TRACE

**Project momentum:**
Steady, small maintenance fixes.

**Architectural concerns:**
None noted for this change.

**Opportunities noticed:**
Consider auto-syncing doctor-ignore additions into module SYNC entries.

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `tui/` | implemented | `docs/tui/SYNC_TUI_State.md` |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Mapped modules:**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| tui | `ngram/tui/**` | `docs/tui/` | DESIGNING |

**Unmapped code:** (run `ngram validate` to check)
- `ngram/` is currently unmapped in `modules.yaml`.

**Coverage notes:**

---

## Agent Observations

### Remarks
- doctor-ignore now reflects TUI false positives that were already documented in TUI sync.
- `ngram validate` fails due to missing `IMPLEMENTATION_Project_Health_Doctor.md` references.

### Suggestions
- [ ] Add module mappings in `modules.yaml` for `ngram/tui/**` to avoid unmapped warnings.

### Propositions
- Consider a helper that syncs doctor-ignore entries into module SYNC entries automatically.
The module manifest is still in template form; mapping work is pending.
