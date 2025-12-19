# ngram TUI — Implementation Details: Structure

```
STATUS: IMPLEMENTED
CREATED: 2025-12-18
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:                ../PATTERNS_TUI_Design.md
BEHAVIORS:               ../BEHAVIORS_TUI_Interactions.md
ALGORITHM:               ../ALGORITHM_TUI_Flow.md
VALIDATION:              ../VALIDATION_TUI_Invariants.md
IMPLEMENTATION_OVERVIEW: ../IMPLEMENTATION_TUI_Code_Architecture.md
THIS:                    IMPLEMENTATION_TUI_Code_Architecture_Structure.md
TEST:                    ../TEST_TUI_Coverage.md
SYNC:                    ../SYNC_TUI_State.md
```

---

## CODE STRUCTURE

```
ngram/tui/                           # TUI package root
ngram/tui/__init__.py                # Package exports (11L)
ngram/tui/app.py                     # Main Textual App (491L)
ngram/tui/state.py                   # Session state management (169L)
ngram/tui/commands.py                # Slash command handlers (637L)
ngram/tui/commands_agent.py          # Manager agent subprocess helpers (349L)
ngram/tui/manager.py                 # Manager supervisor & Claude PTY (275L)
ngram/tui/widgets/__init__.py        # Widget exports (20L)
ngram/tui/widgets/manager_panel.py   # Left column manager display (138L)
ngram/tui/widgets/agent_panel.py     # Single agent output display (97L)
ngram/tui/widgets/agent_container.py # Columns/tabs container (120L)
ngram/tui/widgets/input_bar.py       # Bottom input widget (133L)
ngram/tui/widgets/status_bar.py      # Top status bar (74L)
ngram/tui/styles/theme.tcss          # Paper & Parchment theme CSS (244L)
ngram/cli.py                         # CLI entry point (TUI launched via `ngram`)
ngram/repair_core.py                 # Shared repair logic (497L)
```

Manager startup prefers `.ngram/agents/manager/AGENTS.md` when present; otherwise it mirrors `.ngram/CLAUDE.md` into the manager working directory and writes `AGENTS.md` for Codex/Gemini compatibility.

### File Responsibilities

| File | Lines | Status | Purpose | Key Functions/Classes |
|------|-------|--------|---------|----------------------|
| `ngram/tui/app.py` | 491L | EXISTS | Main Textual application | `NgramApp`, `compose()`, `on_mount()`, `main()` |
| `ngram/tui/widgets/manager_panel.py` | 138L | EXISTS | Manager message display | `ManagerPanel`, `add_message()`, `add_thinking()` |
| `ngram/tui/widgets/agent_panel.py` | 97L | EXISTS | Single agent output | `AgentPanel`, `append_output()` |
| `ngram/tui/widgets/agent_container.py` | 120L | EXISTS | Multi-agent layout | `AgentContainer`, `add_agent()` |
| `ngram/tui/widgets/input_bar.py` | 133L | EXISTS | User input capture | `InputBar`, `on_submit()`, history, tab completion |
| `ngram/tui/widgets/status_bar.py` | 74L | EXISTS | Health score display | `StatusBar`, `update_health()` |
| `ngram/tui/state.py` | 169L | EXISTS | Session state | `SessionState`, `AgentHandle`, `ConversationHistory` |
| `ngram/tui/commands.py` | 637L | WATCH | Command routing | `handle_command()`, `handle_repair()`, `handle_doctor()` |
| `ngram/tui/commands_agent.py` | 349L | OK | Manager agent subprocess handling | `_run_agent_message()`, `_detect_commands()` |
| `ngram/tui/styles/theme.tcss` | 244L | EXISTS | CSS styling | Paper & Parchment theme |
| `ngram/tui/manager.py` | 275L | EXISTS | Manager supervisor | `ManagerSupervisor`, `ClaudePTY`, `DriftWarning` |
| `ngram/cli.py` | - | EXISTS | CLI entry point | TUI launched via `ngram` (no subcommand) |
| `ngram/repair_core.py` | 497L | EXISTS | Shared logic | `spawn_repair_agent_async()` |

---

## DESIGN PATTERNS

### Architecture Pattern: Component-Based UI

**Pattern:** Textual widget composition

**Why:** Textual provides CSS-like styling, async support, and composable widgets. Matches agent CLI aesthetic.

**Where:** All widget files in `ngram/tui/widgets/` compose into `ngram/tui/app.py`.

### Code Patterns

| Pattern | Where Used | Purpose |
|---------|------------|---------|
| Observer | Agent output callbacks | Stream output to panels |
| Factory | `ngram/tui/commands.py` | Route commands to handlers |
| State | `ngram/tui/state.py` | Centralized session state |
| Composition | `ngram/tui/app.py` | Build UI from widgets |

### Anti-Patterns to Avoid

- Monolithic `app.py` — keep logic delegated to widgets/helpers.
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
    └── imports → widget modules
    └── imports → ngram/tui/state.py
    └── imports → ngram/tui/commands.py
    └── imports → ngram/tui/manager.py

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
| `textual` | TUI framework | `ngram/tui/app.py` and widget files |
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
User Input -> InputBar -> NgramApp -> commands.py -> repair_core.py -> AgentContainer
```

### Agent Output Flow

```
Subprocess stdout -> repair_core output callback -> AgentPanel.append_output() -> render
```

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
| `ngram/tui/app.py` | 1 | DOCS reference to `PATTERNS_TUI_Design.md` |
| `ngram/tui/state.py` | 1 | DOCS reference to implementation docs |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM main loop | `ngram/tui/app.py:NgramApp.run()` |
| BEHAVIOR B1 launch | `ngram/tui/app.py:main()`, `ngram/cli.py` |
| BEHAVIOR B2 repair | `ngram/tui/commands.py:handle_repair()` |
