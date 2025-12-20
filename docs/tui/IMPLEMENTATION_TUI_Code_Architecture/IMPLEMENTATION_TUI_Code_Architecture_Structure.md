# ngram TUI — Implementation Details: Structure

```
STATUS: IMPLEMENTED
CREATED: 2025-12-18
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:                ../PATTERNS_TUI_Modular_Interface_Design.md
BEHAVIORS:               ../BEHAVIORS_TUI_Interactions.md
ALGORITHM:               ../ALGORITHM_TUI_Widget_Interaction_Flow.md
VALIDATION:              ../VALIDATION_TUI_User_Interface_Invariants.md
HEALTH:                  ../HEALTH_TUI_Component_Test_Coverage.md
SYNC:                    ../SYNC_TUI_Development_Current_State.md
```

---

## CODE STRUCTURE

```
ngram/tui/                           # TUI package root
ngram/tui/__init__.py                # Package exports (11L)
ngram/tui/app.py                     # TUI entry point (24L)
ngram/tui/app_core.py                # Main Textual App (724L)
ngram/tui/app_manager.py             # Manager startup helpers (257L)
ngram/tui/state.py                   # Session state management (198L)
ngram/tui/commands.py                # Slash command handlers (678L)
ngram/tui/commands_agent.py          # Manager agent subprocess helpers (388L)
ngram/tui/manager.py                 # Manager supervisor & Claude PTY (308L)
ngram/tui/widgets/__init__.py        # Widget exports (20L)
ngram/tui/widgets/manager_panel.py   # Left column manager display (246L)
ngram/tui/widgets/agent_panel.py     # Single agent output display (329L)
ngram/tui/widgets/agent_container.py # Columns/tabs container (361L)
ngram/tui/widgets/input_bar.py       # Bottom input widget (222L)
ngram/tui/widgets/status_bar.py      # Top status bar (190L)
ngram/tui/widgets/suggestions.py     # Command suggestions bar (46L)
ngram/tui/styles/theme.tcss          # Paper & Parchment theme CSS (337L)
ngram/tui/styles/theme_light.tcss    # Light theme CSS (383L)
```

Manager startup prefers .ngram/agents/manager/AGENTS.md when present; otherwise it mirrors .ngram/CLAUDE.md into the manager working directory and writes `AGENTS.md` for Codex/Gemini compatibility.
CHANGES tab header includes change/commit rates computed from recent git history (last 60 minutes).

### File Responsibilities

| File | Lines | Status | Purpose | Key Functions/Classes |
|------|-------|--------|---------|----------------------|
| `ngram/tui/app.py` | 24L | OK | TUI entry point | `main()` |
| `ngram/tui/app_core.py` | 724L | OK | Main Textual application | `NgramApp`, `compose()`, `on_mount()` |
| `ngram/tui/app_manager.py` | 257L | OK | Manager startup helpers | `start_manager_with_overview()`, `show_static_overview()` |
| `ngram/tui/widgets/manager_panel.py` | 246L | EXISTS | Manager message display | `ManagerPanel`, `add_message()`, `add_thinking()` |
| `ngram/tui/widgets/agent_panel.py` | 329L | EXISTS | Single agent output | `AgentPanel`, `append_output()` |
| `ngram/tui/widgets/agent_container.py` | 361L | EXISTS | Multi-agent layout | `AgentContainer`, `add_agent()` |
| `ngram/tui/widgets/input_bar.py` | 222L | EXISTS | User input capture | `InputBar`, `on_submit()`, history, tab completion |
| `ngram/tui/widgets/status_bar.py` | 190L | EXISTS | Health score display | `StatusBar`, `update_health()` |
| `ngram/tui/widgets/suggestions.py` | 46L | EXISTS | Command suggestions bar | `SuggestionsBar`, `show_suggestions()` |
| `ngram/tui/state.py` | 198L | EXISTS | Session state | `SessionState`, `AgentHandle`, `ConversationHistory` |
| `ngram/tui/commands.py` | 678L | WATCH | Command routing | `handle_command()`, `handle_repair()`, `handle_doctor()` |
| `ngram/tui/commands_agent.py` | 388L | OK | Manager agent subprocess handling | `_run_agent_message()`, `_detect_commands()` |
| `ngram/tui/styles/theme.tcss` | 337L | EXISTS | CSS styling | Paper & Parchment theme |
| `ngram/tui/styles/theme_light.tcss` | 383L | EXISTS | CSS styling | Light theme variants |

---

## DESIGN PATTERNS

### Architecture Pattern: Component-Based UI

**Pattern:** Textual widget composition

**Why:** Textual provides CSS-like styling, async support, and composable widgets. Matches agent CLI aesthetic.

**Where:** All widget files in `ngram/tui/widgets/` compose into `ngram/tui/app_core.py`.

### Code Patterns

| Pattern | Where Used | Purpose |
|---------|------------|---------|
| Observer | Agent output callbacks | Stream output to panels |
| Factory | `ngram/tui/commands.py` | Route commands to handlers |
| State | `ngram/tui/state.py` | Centralized session state |
| Composition | `ngram/tui/app_core.py` | Build UI from widgets |

### Anti-Patterns to Avoid

- Monolithic `ngram/tui/app_core.py` — keep logic delegated to widgets/helpers.
- Sync blocking — use async throughout.
- Global state — use SessionState class, not module globals.
- Hardcoded colors — all styling in `ngram/tui/styles/theme.tcss`.

---

## BOUNDARIES

**Inside TUI module:** rendering, input handling, layout management, command parsing.

**Outside TUI module:** repair logic (`ngram/repair_core.py`), doctor checks (`ngram/doctor.py`), file operations (agents handle this).

---

## SCHEMA

### SessionState

```yaml
SessionState:
  required:
    - health_score: int           # Current health 0-100
    - active_agents: List[AgentHandle]
    - running: bool               # App running state
  optional:
    - manager_messages: List[str] # Message history
    - last_command: str           # Most recent command
```

### AgentHandle

```yaml
AgentHandle:
  required:
    - id: str                     # Unique identifier
    - issue_type: str             # e.g., "INCOMPLETE_CHAIN"
    - target_path: str            # Issue target
    - process: asyncio.Process    # Subprocess handle
    - status: str                 # running/completed/failed/timeout
  optional:
    - output_buffer: List[str]    # Captured output lines
    - start_time: float           # For duration tracking
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
ngram/tui/app.py
    └── imports → ngram/tui/app_core.py

ngram/tui/app_core.py
    └── imports → widget modules
    └── imports → ngram/tui/state.py
    └── imports → ngram/tui/commands.py
    └── imports → ngram/tui/manager.py
    └── imports → ngram/tui/app_manager.py

ngram/tui/app_manager.py
    └── imports → ngram/tui/commands_agent.py

ngram/tui/commands.py
    └── imports → ngram/tui/commands_agent.py
    └── imports → ngram/repair_core.py
    └── imports → ngram/doctor.py
    └── imports → ngram/tui/app.py (type hint)

ngram/cli.py
    └── imports → ngram/tui/app.py (NgramApp)
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `textual` | TUI framework | `ngram/tui/app_core.py` and widget files |
| `asyncio` | Async subprocess | `ngram/tui/commands.py` |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `AGENT_TIMEOUT` | `ngram/repair_core.py` | 600s | Max agent runtime |
| Theme | `ngram/tui/styles/theme.tcss` | Paper & Parchment | Visual theme |

---

## DATA FLOW

### User Command Flow

```
User Input -> InputBar -> NgramApp -> ngram/tui/commands.py -> ngram/repair_core.py -> AgentContainer
```

### Agent Output Flow

```
Subprocess stdout -> repair_core output callback -> AgentPanel.append_output() -> render
```

`ngram/tui/commands.py` wires the output callback to buffer chunks in `AgentHandle` and forward them to the active `AgentPanel` for streaming.

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Session state | `ngram/tui/state.py:SessionState` | App instance | App lifetime |
| Agent handles | SessionState active_agents | Session | Per repair run |
| Widget state | Individual widgets | Widget instance | Widget lifetime |

### SessionState Helpers

- `add_agent()` replaces an existing agent with the same id to avoid duplicates.
- `active_count` uses AgentHandle.is_active, which checks subprocess returncode.
- Conversation history returns copies and handles non-positive limits.

### State Transitions

```
IDLE -> RUNNING -> IDLE (complete/error/timeout)
```

---

## RUNTIME BEHAVIOR

### Initialization

1. Import `textual` (fail gracefully if missing).
2. Create `NgramApp` instance.
3. Compose widgets.
4. Run initial doctor check.
5. Focus input bar.
6. Enter event loop.

### Main Loop

1. Await input event.
2. Parse command.
3. Dispatch handler.
4. Update UI.
5. Return to step 1.

### Shutdown

1. Signal all agent processes to terminate.
2. Wait for graceful shutdown (timeout 5s).
3. Force-kill remaining.
4. Restore terminal.
5. Exit.

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Textual App | async | Event-driven, single thread |
| Agent processes | subprocess | Independent processes |
| Output streaming | async callback | Non-blocking |

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Line | Reference |
|------|------|-----------|
| `ngram/tui/app_core.py` | 1 | DOCS reference to `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md` |
| `ngram/tui/app.py` | 1 | DOCS reference to `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md` |
| `ngram/tui/manager.py` | 1 | DOCS reference to `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md` |
| `ngram/tui/__init__.py` | 1 | DOCS reference to `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md` |
| `ngram/tui/app_manager.py` | 1 | DOCS reference to `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md` |
| `ngram/tui/state.py` | 1 | DOCS reference to implementation docs |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM main loop | `ngram/tui/app_core.py:NgramApp.run()` |
| BEHAVIOR B1 launch | `ngram/tui/app.py:main()`, `ngram/cli.py` |
| BEHAVIOR B2 repair | `ngram/tui/commands.py:handle_repair()` |
