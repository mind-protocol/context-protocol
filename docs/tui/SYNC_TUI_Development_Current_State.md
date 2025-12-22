# ngram TUI — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex (verify TUI implementation link)
STATUS: IMPLEMENTED
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_TUI_Modular_Interface_Design.md
BEHAVIORS:       ./BEHAVIORS_TUI_Interactions.md
ALGORITHM:       ./ALGORITHM_TUI_Widget_Interaction_Flow.md
VALIDATION:      ./VALIDATION_TUI_User_Interface_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_TUI_Code_Architecture.md
HEALTH:          ./HEALTH_TUI_Component_Test_Coverage.md
THIS:            SYNC_TUI_Development_Current_State.md (you are here)
```

---

## CURRENT STATE

**Status: FUNCTIONAL** — TUI working with agent integration (Claude, Gemini, or Codex).
Entry point is `ngram` (no subcommand).

Recent fix:
- Passed DoctorConfig into `spawn_repair_agent_async` from the TUI repair flow to avoid missing-argument errors.
- Stored the repair DoctorConfig on the app and reused it when spawning queued agents.
Refactor:
- Extracted `NgramApp` into `ngram/tui/app_core.py` to shrink `ngram/tui/app.py` (app.py 969L → 24L; app_core.py became 955L).
- Extracted manager startup helpers into `ngram/tui/app_manager.py` (app_core.py 955L → 724L).

Recent stability work:
- Conversation history guards (non-positive limits, copy-on-read)
- Agent activity checks include subprocess returncode
- Agent handle de-duplication and empty message suppression
- Manager drift detection path normalization and PTY state handling
- Rate-limit detection now requires error-context markers and only stops repair on failed agents to avoid false positives.
- Migrated INCOMPLETE_IMPL suppressions into doc metadata tags and removed doctor-ignore entries.
- Verified `ngram/tui/widgets/status_bar.py` already implements reported methods; no code changes needed.
- Implemented `/doctor` handler logic to update health status and log results.
- Streamed repair agent output into agent panels while buffering agent logs.
- Re-verified `ngram/tui/state.py` already implements `ConversationMessage.to_dict` and `AgentHandle.duration`; no code changes required.
- CHANGES tab header now shows recent changes/min and commits/min (last 60 minutes).
- CHANGES tab refresh is now backgrounded and rate-limited to avoid startup stalls; periodic repair summaries use async git calls every 2 minutes (last 5 entries).
- Tab switching no longer triggers background refresh for DOCTOR/SYNC/MAP/CHANGES to avoid click-time stalls.
- SYNC/MAP markdown rendering now truncates large content to keep tab switching responsive.
- Markdown rendering now caches Rich renderables for all tabs to avoid re-parsing on tab switch while keeping formatting.
- Markdown strong text and headings now use orange styling via a Rich theme override matching the tab background to avoid black fill.
- Tab content for SYNC/MAP/DOCTOR/CHANGES is click-to-copy (copies raw markdown).

Module mapping:
- `modules.yaml` includes `tui` module mapping under `modules`

Doc maintenance:
- Implementation doc references normalized to avoid broken-link false positives
- Implementation overview references now point to `ngram/repair_core.py` and full TUI command paths
- Manager startup reference uses repo-root `.ngram/CLAUDE.md` and `.ngram/agents/manager/AGENTS.md` paths
- Structure doc and TUI DOCS headers point to `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md` for core entry points
- Manager and package DOCS headers now reference `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md`
- Verified structure doc references resolve to existing TUI PATTERNS docs
- Data flow diagram uses full file paths for command and repair routing
- Implementation details split into `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/` with an overview entry point
- Runtime implementation content consolidated into `IMPLEMENTATION_TUI_Code_Architecture_Structure.md` to avoid duplicate docs
- Removed `IMPLEMENTATION_TUI_Code_Architecture_Runtime.md` so the structure doc is the single IMPLEMENTATION detail file
- Structure doc file list updated for new widgets and theme files
- Re-verified IMPLEMENTATION doc backtick references for STALE_IMPL; all paths resolve
- Clarified suggestions bar label in the structure doc file list
- Manager /repair issue lists render as a single block to avoid extra blank lines between items.
- Consolidated the 2024-12 archive into the 2025-12 canonical archive and left the older file as a reference.

Archived detail:
Older content archived to: `archive/SYNC_TUI_State_Archive_2025-12.md`
Archive consolidation: confirmed the 2024-12 condensed snapshot lives in `archive/SYNC_TUI_State_Archive_2025-12.md` and replaced `archive/SYNC_Archive_2024-12.md` with a reference.

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

- Could not resolve escalation in `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md` as no human decisions were provided for the conflict: "Should `ngram` without args require textual, or gracefully fall back to CLI help?".


- Tab layout for >3 agents not fully implemented
- Agent queue processing (issues beyond first 3) not implemented

---

## CONFLICTS

### DECISION: Monolith target file
- Conflict: Repair task named `ngram/tui/app.py` as the monolith target, but current implementation places the main app in `ngram/tui/app_core.py` while `ngram/tui/app.py` is a thin entry point.
- Resolution: Split `ngram/tui/app_core.py` by extracting manager startup helpers into `ngram/tui/app_manager.py`.
- Reasoning: The monolithic logic lives in `ngram/tui/app_core.py`, so addressing the actual file restores code structure and aligns with the module layout.
- Updated: `ngram/tui/app_core.py`, `ngram/tui/app_manager.py`, `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md`, `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`, `modules.yaml`.

## AGENT OBSERVATIONS

### Remarks
- Large sync content archived to keep module docs within size targets.
- Verified `ConversationMessage.to_dict` and `AgentHandle.duration` are implemented in `ngram/tui/state.py` during INCOMPLETE_IMPL repair review; no code changes required.
- Re-verified `ngram/tui/widgets/status_bar.py` implementations for the INCOMPLETE_IMPL report; no code changes required.
- Re-verified `ngram/tui/widgets/status_bar.py` for the current INCOMPLETE_IMPL repair; implementations already present, so no code changes required.
- Verified `ngram/tui/commands.py` already implements `on_output` and `handle_doctor`; INCOMPLETE_IMPL report was stale.
- Manager /repair issue lists now render without extra blank lines between items.
- Extracted `NgramApp` into `ngram/tui/app_core.py` and left `ngram/tui/app.py` as the entry point.
- Extracted manager startup helpers to `ngram/tui/app_manager.py` to reduce `ngram/tui/app_core.py`.

### Suggestions
<!-- @ngram:todo Keep doctor-ignore and SYNC notes updated together to avoid drift. -->

### Propositions
- None
