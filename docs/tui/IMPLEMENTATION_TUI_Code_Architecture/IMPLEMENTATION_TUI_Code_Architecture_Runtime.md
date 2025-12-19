# ngram TUI — Implementation Details: Runtime

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
THIS:                    IMPLEMENTATION_TUI_Code_Architecture_Runtime.md
TEST:                    ../TEST_TUI_Coverage.md
SYNC:                    ../SYNC_TUI_State.md
```

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
