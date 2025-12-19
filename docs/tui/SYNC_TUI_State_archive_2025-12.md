# Archived: SYNC_TUI_State.md

Archived on: 2025-12-18
Original file: SYNC_TUI_State.md

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
- Dataclasses: `RepairResult`, `EscalationDecision`
- Constants: `ISSUE_SYMBOLS`, `ISSUE_PRIORITY`, `DEPTH_*`
- Functions: `build_agent_prompt()`, `parse_decisions_from_output()`
- Async spawn: `spawn_repair_agent_async()` for TUI integration

Both CLI (`repair.py`) and TUI import from `repair_core.py`.

---


## FILE STRUCTURE (Planned)

```
ngram/
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

