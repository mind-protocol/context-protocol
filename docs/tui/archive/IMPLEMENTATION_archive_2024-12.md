# Archive: TUI Implementation Details (2024-12)

Archived on: 2025-12-19
Source: ../IMPLEMENTATION_TUI_Code_Architecture.md (overview now; details split into folder)

---

## Design Patterns (Historical Detail)

### Architecture Pattern: Component-Based UI
- Textual widget composition, async support, composable widgets

### Code Patterns
- Observer: agent output callbacks
- Factory: command routing
- State: centralized session state
- Composition: app builds UI from widgets

### Anti-Patterns to Avoid
- Monolithic app.py
- Sync blocking in event loop
- Global state
- Hardcoded colors (use TCSS theme)

### Boundary Definitions
- Inside TUI: widgets, input handling, layout, command parsing
- Outside: repair logic, doctor checks, file operations

---

## Runtime Behavior (Historical Detail)

### Initialization
1. Import textual (fail gracefully if missing)
2. Create NgramApp instance
3. Mount widgets (compose)
4. Run initial doctor check
5. Focus input bar
6. Enter event loop

### Main Loop
1. Await input event
2. Parse command
3. Dispatch to handler
4. Update UI
5. Repeat

### Shutdown
1. Signal agent processes to terminate
2. Wait for graceful shutdown (timeout 5s)
3. Force kill remaining
4. Restore terminal
5. Exit

---

## Concurrency Model (Historical Detail)

- Textual app is async and event-driven
- Agent processes are independent subprocesses
- Output streaming uses async callbacks

---

## Configuration (Historical Detail)

- `AGENT_TIMEOUT` in `ngram/repair_core.py` (default 600s)
- Theme in `ngram/tui/styles/theme.tcss` (Paper & Parchment)

---

## Bidirectional Links (Historical Detail)

### Code → Docs
- `ngram/tui/app.py` references PATTERNS_TUI_Design.md
- `ngram/tui/state.py` references IMPLEMENTATION_TUI_Code_Architecture.md (overview)

### Docs → Code
- ALGORITHM main loop → `ngram/tui/app.py:NgramApp.run()`
- BEHAVIOR B1 launch → `ngram/tui/app.py:main()`, `ngram/cli.py`
- BEHAVIOR B2 repair → `ngram/tui/commands.py:handle_repair()`

---

## Remaining Work (Historical Detail)

- Tab layout for >3 agents
- Markdown rendering for responses
- Syntax highlighting for code blocks
- `/issues` command to switch right panel to issues list
- Auto-refresh SYNC display on file change

---

## Decisions Made (Historical Detail)

- Single `ngram/tui/commands.py` for command handlers (implemented)
- Widget classes follow standard Textual pattern
- Paper & Parchment theme in `ngram/tui/styles/theme.tcss`
