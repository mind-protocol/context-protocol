# ngram TUI — Implementation: Code Architecture (Overview)

```
STATUS: IMPLEMENTED
CREATED: 2025-12-18
UPDATED: 2025-12-19
@ngram:doctor:INCOMPLETE_IMPL:false_positive Short widget helpers and accessors are intentionally minimal but complete.
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_TUI_Modular_Interface_Design.md
BEHAVIORS:       ./BEHAVIORS_TUI_Interactions.md
ALGORITHM:       ./ALGORITHM_TUI_Widget_Interaction_Flow.md
VALIDATION:      ./VALIDATION_TUI_User_Interface_Invariants.md
THIS:            IMPLEMENTATION_TUI_Code_Architecture.md
HEALTH:          ./HEALTH_TUI_Component_Test_Coverage.md
SYNC:            ./SYNC_TUI_Development_Current_State.md
```

---

## SUMMARY

Textual-based TUI with a component layout: `NgramApp` composes widgets, `ngram/tui/commands.py` dispatches slash commands, and `ngram/repair_core.py` spawns agents. The UI is a presentation layer over shared CLI logic.

---

## QUICK STRUCTURE (Top-Level)

```
ngram/tui/app.py            # TUI entry point
ngram/tui/app_core.py       # Main Textual app implementation
ngram/tui/app_manager.py    # Manager startup helpers
ngram/tui/commands.py       # Slash command routing
ngram/tui/commands_agent.py # Manager subprocess helpers
ngram/tui/state.py          # Session state
ngram/tui/widgets/*         # UI components
ngram/tui/styles/theme.tcss # Theme
```

---

## COMPONENT REFERENCES

- `ngram/tui/__init__.py` — Package initializer for the TUI bundle.
- `ngram/tui/app.py` — Entry point invoked by `ngram/cli`.
- `ngram/tui/app_core.py` — Hosts `NgramApp` and the widget lifecycle.
- `ngram/tui/app_manager.py` — Manages startup sequences and event loops.
- `ngram/tui/commands.py` — Slash command routing for textual commands.
- `ngram/tui/commands_agent.py` — Spawns agent subprocesses and handles their I/O.
- `ngram/tui/manager.py` — Coordinates multi-agent panels and refresh cycles.
- `ngram/tui/state.py` — Shared session state for the UI.
- `ngram/tui/widgets/__init__.py` — Widget exports.
- `ngram/tui/widgets/agent_container.py` — Hosts agent cards.
- `ngram/tui/widgets/agent_panel.py` — Displays individual agent outputs.
- `ngram/tui/widgets/manager_panel.py` — Controls manager interactions.
- `ngram/tui/widgets/status_bar.py` — Renders connection and health indicators.
- `ngram/tui/widgets/suggestions.py` — Shows suggestion chips and hints.

```
IMPL: ngram/tui/__init__.py
IMPL: ngram/tui/app.py
IMPL: ngram/tui/app_core.py
IMPL: ngram/tui/app_manager.py
IMPL: ngram/tui/commands.py
IMPL: ngram/tui/commands_agent.py
IMPL: ngram/tui/manager.py
IMPL: ngram/tui/state.py
IMPL: ngram/tui/widgets/__init__.py
IMPL: ngram/tui/widgets/agent_container.py
IMPL: ngram/tui/widgets/agent_panel.py
IMPL: ngram/tui/widgets/manager_panel.py
IMPL: ngram/tui/widgets/status_bar.py
IMPL: ngram/tui/widgets/suggestions.py
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `main()` | `ngram/tui/app.py:12` | `ngram` (no args) via `ngram/cli.py` |
| `NgramApp.compose()` | `ngram/tui/app_core.py:107` | Textual mount |
| `InputBar.action_submit()` | `ngram/tui/widgets/input_bar.py:60` | User Enter |

---

## WHAT TO READ NEXT

- Implementation structure and responsibilities: `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md`

---

## REMAINING WORK

- Tab layout for >3 agents (columns exist; tabs not implemented).
- `/sync` auto-refresh for SYNC panel.
- Syntax highlighting for code blocks.

---

## DECISIONS MADE

- Single `ngram/tui/commands.py` for command handlers, with subprocess logic extracted to `ngram/tui/commands_agent.py`.
- Paper & Parchment theme defined in `ngram/tui/styles/theme.tcss`.
