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
PATTERNS:        ./PATTERNS_TUI_Design.md
BEHAVIORS:       ./BEHAVIORS_TUI_Interactions.md
ALGORITHM:       ./ALGORITHM_TUI_Flow.md
VALIDATION:      ./VALIDATION_TUI_Invariants.md
THIS:            IMPLEMENTATION_TUI_Code_Architecture.md (overview)
DETAILS:         ./IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md
TEST:            ./TEST_TUI_Coverage.md
SYNC:            ./SYNC_TUI_State.md
```

---

## SUMMARY

Textual-based TUI with a component layout: `NgramApp` composes widgets, `ngram/tui/commands.py` dispatches slash commands, and `ngram/repair_core.py` spawns agents. The UI is a presentation layer over shared CLI logic.

---

## QUICK STRUCTURE (Top-Level)

```
ngram/tui/app.py            # Main Textual app
ngram/tui/commands.py       # Slash command routing
ngram/tui/commands_agent.py # Manager subprocess helpers
ngram/tui/state.py          # Session state
ngram/tui/widgets/*         # UI components
ngram/tui/styles/theme.tcss # Theme
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `main()` | `ngram/tui/app.py:479` | `ngram` (no args) via `ngram/cli.py` |
| `NgramApp.compose()` | `ngram/tui/app.py:74` | Textual mount |
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
