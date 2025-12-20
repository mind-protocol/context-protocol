# ngram TUI — Patterns: Agent CLI-Style Interface

```
STATUS: DESIGNING
CREATED: 2025-12-18
UPDATED: 2025-12-19
@ngram:doctor:INCOMPLETE_IMPL:false_positive Short delegating UI actions are complete implementations, not stubs.
```

---

## CHAIN

```
THIS:            PATTERNS_TUI_Modular_Interface_Design.md
BEHAVIORS:       ./BEHAVIORS_TUI_Interactions.md
ALGORITHM:       ./ALGORITHM_TUI_Widget_Interaction_Flow.md
VALIDATION:      ./VALIDATION_TUI_User_Interface_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_TUI_Code_Architecture.md
HEALTH:          ./HEALTH_TUI_Component_Test_Coverage.md
SYNC:            ./SYNC_TUI_Development_Current_State.md
```

---

## THE PROBLEM

The ngram CLI commands (`doctor`, `repair`, `validate`) work well but are fire-and-forget. There's no persistent session where you can:
- See manager and worker agents side by side
- Interact with repairs in progress
- Continue working after one task completes
- Have a conversation with the system about your project

Without a TUI:
- Each command exits after completion
- No visual separation of parallel agent outputs
- No way to provide input during repairs
- Switching between commands requires re-typing

---

## THE PATTERN

**Persistent chat interface with multi-column agent display.**

Inspired by agent CLIs:
- **Entry point**: Just `ngram` (no subcommand)
- **Persistent session**: Runs until user quits
- **Manager + Agents layout**: Manager on left, worker agents in columns on right
- **Input bar at bottom**: Like Claude Code's prompt
- **Commands via `/`**: `/repair`, `/doctor`, `/help`, `/quit`

The TUI wraps existing CLI functionality without replacing it. All subcommands (`ngram doctor`, `ngram repair`, etc.) continue to work.

---

## PRINCIPLES

### Principle 1: Persistent Session, Not One-Shot

The TUI stays open. After a repair completes, you're back at the prompt. You can:
- Run another repair
- Ask questions
- Check health
- Continue the conversation

This mirrors how agent CLIs work — it's a session, not a command. The manager can be backed
by Claude, Gemini, or Codex via `--agents {claude,codex,gemini}`.

### Principle 2: Manager + Workers Visualization

The layout separates concerns:
- **Left column (Manager)**: Orchestration, decisions, status messages
- **Right area (Workers)**: Individual agent outputs, each in its own column
- **Tabs when >3 agents**: Prevents screen crowding

This makes parallel agent work comprehensible instead of interleaved output chaos.

### Principle 3: Commands Over Menu

Use `/commands` rather than menus or keybindings:
- `/repair` — Start repair session
- `/doctor` — Run health check
- `/help` — Show available commands
- `/quit` — Exit

This is familiar to agent CLI users and keeps the interface text-focused.

### Principle 4: White Theme for Readability

Default to light background (white theme) for:
- Better readability in well-lit environments
- Less eye strain for extended sessions
- Professional appearance

Theme is CSS-based (Textual's TCSS) for easy customization.

### Principle 5: Shared Core, Separate Display

The TUI imports from `repair_core.py` — the same logic as the CLI. Only the display layer differs:
- CLI: ANSI codes, print statements
- TUI: Textual widgets, CSS styling

This means:
- No duplicated repair logic
- Bug fixes apply to both
- Tests can target core logic

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| textual | TUI framework (async, CSS-like styling, widgets) |
| repair_core | Shared repair logic (dataclasses, agent spawning) |
| doctor | Health check functionality |

---

## INSPIRATIONS

- **Claude Code** — Chat interface with real-time tool output
- **Codex CLI** — Agent session UX with resumable runs
- **htop/btop** — Multi-column terminal UIs
- **tmux/screen** — Pane-based terminal layouts
- **Lazygit** — TUI that wraps CLI functionality

---

## WHAT THIS DOES NOT SOLVE

- **IDE integration** — Still CLI/terminal only
- **Web interface** — No browser version planned
- **Remote sessions** — Single machine only
- **Custom themes** — White theme only initially

---

## IMPLEMENTATION REFERENCES

| File | Role |
|------|------|
| `ngram/tui/__init__.py` | Package initializer for the TUI bundle and CLI handoff. |
| `ngram/tui/app.py` | Entry point that builds `NgramApp` and bridges to `ngram/cli.py`. |
| `ngram/tui/app_core.py` | Hosts the `NgramApp` lifecycle, event loop, and widget composition. |
| `ngram/tui/manager.py` | Coordinates manager/agent panels and background refresh scheduling. |

```
IMPL: ngram/tui/__init__.py
IMPL: ngram/tui/app.py
IMPL: ngram/tui/app_core.py
IMPL: ngram/tui/manager.py
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Should the ngram manager have memory across sessions?
- [ ] Consider keyboard shortcuts (Ctrl+R for repair, Ctrl+D for doctor)
- [ ] How to handle very long agent outputs? Auto-scroll? Truncation?
- IDEA: Agent history panel showing completed agents
- QUESTION: Should `ngram` without args require textual, or gracefully fall back to CLI help?
