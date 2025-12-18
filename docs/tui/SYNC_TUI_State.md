# ngram TUI — Sync: Current State

```
LAST_UPDATED: 2025-12-18
UPDATED_BY: repair-agent (INCOMPLETE_CHAIN fix)
STATUS: DESIGNING
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

**Status: DESIGNING** — Documentation exists, implementation beginning.

The TUI will provide a Claude Code-style persistent chat interface for ngram. Entry point is `ngram` (no subcommand).

### Completed
- PATTERNS documentation
- Core extraction (`repair_core.py`) for shared repair logic
- Full documentation chain (BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST)

### In Progress
- Package structure creation

### Planned
- Textual-based app with multi-column layout
- Manager panel (left) + Agent panels (right columns/tabs)
- Input bar with /command support
- White theme CSS
- Integration with existing repair/doctor functionality

---

## DESIGN DECISIONS

### Entry Point: `ngram`

Running `ngram` with no subcommand launches the TUI. All other subcommands (`ngram doctor`, `ngram repair`, etc.) continue to work as CLI tools.

**Rationale**: Mirrors Claude Code where just typing `claude` launches the interface.

### Layout: Manager + Agents

```
┌─────────────────────────────────────────────────────────────────────┐
│  ngram                                               Health: 32/100 │
├───────────────────────┬─────────────────────────────────────────────┤
│      MANAGER          │           AGENTS (columns or tabs)          │
│                       │  ┌─────────────┬─────────────┬───────────┐  │
│  > Status messages    │  │  Agent 1    │  Agent 2    │  Agent 3  │  │
│  > Decisions          │  │             │             │           │  │
│                       │  └─────────────┴─────────────┴───────────┘  │
├───────────────────────┴─────────────────────────────────────────────┤
│ > input field                                                    ⏎  │
└─────────────────────────────────────────────────────────────────────┘
```

- Manager (left, fixed ~30% width): Orchestration output
- Agents (right, dynamic): One column per agent, tabs if >3
- Input (bottom): Claude Code-style prompt

### Theme: White

Light background for readability. CSS-based via Textual's TCSS.

### Shared Core: repair_core.py

Extracted shared logic from `repair.py`:
- Dataclasses: `RepairResult`, `ArbitrageDecision`
- Constants: `ISSUE_SYMBOLS`, `ISSUE_PRIORITY`, `DEPTH_*`
- Functions: `build_agent_prompt()`, `parse_decisions_from_output()`
- Async spawn: `spawn_repair_agent_async()` for TUI integration

Both CLI (`repair.py`) and TUI import from `repair_core.py`.

---

## FILE STRUCTURE (Planned)

```
src/ngram/
├── tui/                         # TUI package
│   ├── __init__.py
│   ├── app.py                   # Main Textual App
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── manager_panel.py     # Left column
│   │   ├── agent_panel.py       # Single agent display
│   │   ├── agent_container.py   # Columns/tabs switcher
│   │   ├── input_bar.py         # Bottom input
│   │   └── status_bar.py        # Top status bar
│   ├── styles/
│   │   └── theme.tcss           # White theme
│   ├── state.py                 # Session state
│   ├── commands.py              # /command handlers
│   └── manager.py               # Manager agent logic
├── tui_command.py               # Entry point
└── repair_core.py               # Shared repair logic (created)
```

---

## KNOWN ISSUES

| Issue | Notes |
|-------|-------|
| BROKEN_IMPL_LINK | IMPLEMENTATION doc references planned files that don't exist yet. This is expected for DESIGNING status - will resolve when code is implemented. |

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Documentation created. Need to implement:
1. Add TUI module to `modules.yaml`
2. Create package structure
3. Update `cli.py` for TUI launch
4. Add textual dependency
5. Implement widgets

**What you need to understand:**
- TUI uses Textual framework (async, CSS styling)
- Must integrate with `repair_core.py` for agent spawning
- White theme is required (CSS in `theme.tcss`)

**Watch out for:**
- Textual is optional dependency — CLI must work without it
- Async integration: Textual is async, repair_core provides async spawn

---

## HANDOFF: FOR HUMAN

**Executive summary:**
TUI design documented. Core extraction done. Ready for implementation.

**Decisions made:**
- Entry point: `ngram` (no subcommand)
- Layout: Manager left, agents right (columns/tabs)
- Theme: White
- Shared core: `repair_core.py`

**Needs your input:**
- None currently

---

## POINTERS

| What | Where |
|------|-------|
| Design rationale | `docs/tui/PATTERNS_TUI_Design.md` |
| Shared repair logic | `src/ngram/repair_core.py` |
| CLI integration point | `src/ngram/cli.py` |
| Implementation plan | `/home/mind-protocol/.claude/plans/structured-cooking-alpaca.md` |
