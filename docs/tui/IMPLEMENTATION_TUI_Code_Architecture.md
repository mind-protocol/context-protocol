# ngram TUI — Implementation: Code Architecture

```
STATUS: IMPLEMENTED
CREATED: 2025-12-18
UPDATED: 2025-12-18
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_TUI_Design.md
BEHAVIORS:       ./BEHAVIORS_TUI_Interactions.md
ALGORITHM:       ./ALGORITHM_TUI_Flow.md
VALIDATION:      ./VALIDATION_TUI_Invariants.md
THIS:            IMPLEMENTATION_TUI_Code_Architecture.md (you are here)
TEST:            ./TEST_TUI_Coverage.md
SYNC:            ./SYNC_TUI_State.md
```

---

## CODE STRUCTURE

```
ngram/tui/                           # TUI package root
ngram/tui/__init__.py                # Package exports (11L)
ngram/tui/app.py                     # Main Textual App (491L)
ngram/tui/state.py                   # Session state management (169L)
ngram/tui/commands.py                # Slash command handlers (443L)
ngram/tui/manager.py                 # Manager supervisor & Claude PTY (Claude only) (275L)
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

Manager startup mirrors `../../.ngram/CLAUDE.md` into the manager working directory and writes `AGENTS.md` with the same content for Codex/Gemini compatibility.

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
| `ngram/tui/commands.py` | 443L | EXISTS | Command routing | `handle_command()`, `handle_repair()`, `handle_doctor()` |
| `ngram/tui/styles/theme.tcss` | 244L | EXISTS | CSS styling | Paper & Parchment theme |
| `ngram/tui/manager.py` | 275L | EXISTS | Manager supervisor | `ManagerSupervisor`, `ClaudePTY`, `DriftWarning` |
| `ngram/cli.py` | - | EXISTS | CLI entry point | TUI launched via `ngram` (no subcommand) |
| `ngram/repair_core.py` | 497L | EXISTS | Shared logic | `spawn_repair_agent_async()` |

### Manager Supervisor Details

- Drift detection parses agent output for change verbs and categorizes code updates vs markdown docs.
- ClaudePTY running state reflects subprocess exit to avoid stale "running" flags.

---

## DESIGN PATTERNS

### Architecture Pattern: Component-Based UI

**Pattern:** Textual widget composition

**Why:** Textual provides CSS-like styling, async support, and composable widgets. Matches agent CLI aesthetic.

**Where:** All widget files in ngram/tui/widgets/ compose into ngram/tui/app.py

### Code Patterns

| Pattern | Where Used | Purpose |
|---------|------------|---------|
| Observer | Agent output callbacks | Stream output to panels |
| Factory | `ngram/tui/commands.py` | Route commands to handlers |
| State | `ngram/tui/state.py` | Centralized session state |
| Composition | `ngram/tui/app.py` | Build UI from widgets |

### Anti-Patterns to Avoid

- **Monolithic app.py** — Keep under 200 lines, delegate to widgets
- **Sync blocking** — Never block event loop, use async throughout
- **Global state** — Use SessionState class, not module globals
- **Hardcoded colors** — All styling in `ngram/tui/styles/theme.tcss`

### Boundary Definitions

**Inside TUI module:**
- Widget rendering
- User input handling
- Layout management
- Command parsing

**Outside TUI module (use via imports):**
- Repair logic (`ngram/repair_core.py`)
- Doctor checks (`ngram/doctor.py`)
- File operations (agents handle this)

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

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `main()` | `ngram/tui/app.py:479` | `ngram` (no args) via `ngram/cli.py` |
| `NgramApp.compose()` | `ngram/tui/app.py:74` | Textual mount |
| `InputBar.action_submit()` | `ngram/tui/widgets/input_bar.py:60` | User Enter |

---

## DATA FLOW

### User Command Flow

```
┌─────────────────┐
│   User Input    │
│   "/repair"     │
└────────┬────────┘
         │ string
         ▼
┌─────────────────────────┐
│       InputBar          │ ← captures input, emits event
│ ngram/tui/widgets/  │
│       input_bar.py      │
└───────────┬─────────────┘
            │ SlashCommand
            ▼
┌─────────────────────────┐
│       NgramApp          │ ← routes to handler
│   ngram/tui/app.py  │
└───────────┬─────────────┘
            │ dispatch
            ▼
┌─────────────────────────┐
│ ngram/tui/commands  │ ← handle_repair()
│       handle_*()        │
└───────────┬─────────────┘
            │ spawns agents
            ▼
┌─────────────────────────┐
│ ngram/repair_core   │ ← spawn_repair_agent_async()
└───────────┬─────────────┘
            │ asyncio.Process per issue
            ▼
┌─────────────────────────┐
│     AgentContainer      │ ← displays in columns
│ ngram/tui/widgets/  │
│   agent_container.py    │
└─────────────────────────┘
```

### Agent Output Flow

```
┌─────────────────────────┐
│      Manager Agent      │ ← subprocess (Claude, Gemini, or Codex)
│       (external)        │
└───────────┬─────────────┘
            │ stdout lines
            ▼
┌─────────────────────────┐
│ ngram/repair_core   │ ← on_output callback
│   spawn_async()         │
└───────────┬─────────────┘
            │ parsed text
            ▼
┌─────────────────────────┐
│      AgentPanel         │ ← append_output()
│ ngram/tui/widgets/  │
│    agent_panel.py       │
└───────────┬─────────────┘
            │ render
            ▼
┌─────────────────────────┐
│     User Display        │
└─────────────────────────┘
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
    └── imports → ngram/repair_core.py
    └── imports → ngram/doctor.py
    └── imports → ngram/tui/app.py (type hint)

ngram/cli.py
    └── imports → ngram/tui/app.py (NgramApp)
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `textual` | TUI framework | ngram/tui/app.py and widget files |
| `asyncio` | Async subprocess | `ngram/tui/commands.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Session state | `ngram/tui/state.py:SessionState` | App instance | App lifetime |
| Agent handles | SessionState active_agents | Session | Per repair run |
| Widget state | Individual widgets | Widget instance | Widget lifetime |

### SessionState Helpers

- `add_agent()` replaces an existing agent with the same id to avoid duplicate handles.
- `active_count` relies on `AgentHandle.is_active`, which also checks subprocess returncode.
- `ConversationHistory.get_recent()` returns a copy and handles non-positive limits.

### State Transitions

```
IDLE ──/repair──▶ RUNNING ──complete──▶ IDLE
                     │
                     ├──error──▶ IDLE (with error message)
                     │
                     └──timeout──▶ IDLE (with timeout message)
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Import textual (fail gracefully if missing)
2. Create NgramApp instance
3. Mount widgets (compose)
4. Run initial doctor check
5. Focus input bar
6. Enter event loop
```

### Main Loop

```
1. Await input event
2. Parse command
3. Dispatch to handler
4. Update UI
5. Back to step 1
```

### Shutdown

```
1. Signal all agent processes to terminate
2. Wait for graceful shutdown (timeout 5s)
3. Force kill remaining
4. Restore terminal
5. Exit
```

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Textual App | async | Event-driven, single thread |
| Agent processes | subprocess | Independent processes |
| Output streaming | async callback | Non-blocking |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `AGENT_TIMEOUT` | `ngram/repair_core.py` | 600s | Max agent runtime |
| Theme | `ngram/tui/styles/theme.tcss` | Paper & Parchment | Visual theme |

---

## BIDIRECTIONAL LINKS

### Code → Docs

Files reference this documentation:

| File | Line | Reference |
|------|------|-----------|
| ngram/tui/app.py | 1 | DOCS reference to PATTERNS_TUI_Design.md |
| ngram/tui/state.py | 1 | DOCS reference to this file |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM main loop | `ngram/tui/app.py:NgramApp.run()` |
| BEHAVIOR B1 launch | `ngram/tui/app.py:main()`, `ngram/cli.py` |
| BEHAVIOR B2 repair | `ngram/tui/commands.py:handle_repair()` |

---

## REMAINING WORK

- [ ] Tab layout for >3 agents (columns work, tabs not implemented)
- [ ] Markdown rendering for responses
- [ ] Syntax highlighting for code blocks
- [ ] `/issues` command to switch right panel to issues list
- [ ] Auto-refresh SYNC display on file change

## DECISIONS MADE

- [x] Single `ngram/tui/commands.py` for all command handlers (implemented)
- [x] Widgets are classes (standard Textual pattern)
- [x] Paper & Parchment theme in `ngram/tui/styles/theme.tcss`
