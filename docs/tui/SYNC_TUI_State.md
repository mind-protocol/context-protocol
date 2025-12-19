# ngram TUI — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: codex (verify status bar implementations)
STATUS: IMPLEMENTED
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_TUI_Design.md
BEHAVIORS:       ./BEHAVIORS_TUI_Interactions.md
ALGORITHM:       ./ALGORITHM_TUI_Flow.md
VALIDATION:      ./VALIDATION_TUI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_TUI_Code_Architecture.md
TEST:            ./TEST_TUI_Coverage.md
THIS:            SYNC_TUI_State.md (you are here)
```

---

## CURRENT STATE

**Status: FUNCTIONAL** — TUI working with agent integration (Claude, Gemini, or Codex).
Entry point is `ngram` (no subcommand).

Recent stability work:
- Conversation history guards (non-positive limits, copy-on-read)
- Agent activity checks include subprocess returncode
- Agent handle de-duplication and empty message suppression
- Manager drift detection path normalization and PTY state handling
- Verified `ngram/tui/widgets/status_bar.py` already implements reported methods; no code changes needed.

Module mapping:
- `modules.yaml` includes `tui` module mapping under `modules`

Doc maintenance:
- Implementation doc references normalized to avoid broken-link false positives
- Manager startup reference uses `.ngram/CLAUDE.md`
- Implementation details split into `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/` with an overview entry point

Archived detail:
- Historical feature list, handoffs, and observations moved to `docs/tui/archive/SYNC_archive_2024-12.md`

---

## IN PROGRESS

- Queue management for >3 issues in repair

---

## PLANNED FEATURES (HIGH LEVEL)

- Syntax highlighting for code blocks
- Auto-refresh SYNC display on file change
- `/repair --max N` configurable concurrency
- Tab layout for >3 agents

---

## KNOWN GAPS

- Tab layout for >3 agents not fully implemented
- Agent queue processing (issues beyond first 3) not implemented

---

## AGENT OBSERVATIONS

### Remarks
- Large sync content archived to keep module docs within size targets.

### Suggestions
- [ ] Keep doctor-ignore and SYNC notes updated together to avoid drift.

### Propositions
- None
