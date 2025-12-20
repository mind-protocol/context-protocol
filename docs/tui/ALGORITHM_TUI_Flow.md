# ngram TUI — Algorithm: Application Flow and Event Handling

```
STATUS: DRAFT
CREATED: 2025-12-18
VERIFIED: Not yet — implementation pending
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_TUI_Design.md
BEHAVIORS:       ./BEHAVIORS_TUI_Interactions.md
THIS:            ALGORITHM_TUI_Flow.md (you are here)
VALIDATION:      ./VALIDATION_TUI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_TUI_Code_Architecture.md
HEALTH:          ./HEALTH_TUI_Coverage.md
SYNC:            ./SYNC_TUI_State.md
```

---

## OVERVIEW

The TUI is a Textual-based async application that manages a persistent session with multiple concurrent agent panels. It processes user input via slash commands, orchestrates repair agents, and streams their output to dedicated display columns.

The core loop: receive input -> parse command -> dispatch to handler -> update display -> await next input.

---

## DATA STRUCTURES

### SessionState

```
SessionState:
  health_score: int (0-100)
  active_agents: List[AgentHandle]
  manager_messages: List[str]
  last_command: str | None
  running: bool
```

### AgentHandle

```
AgentHandle:
  id: str
  issue_type: str
  target_path: str
  process: asyncio.Process
  output_buffer: List[str]
  status: "running" | "completed" | "failed" | "timeout"
```

### SlashCommand

```
SlashCommand:
  name: str (e.g., "repair", "doctor", "quit", "help")
  args: List[str]
```

---

## ALGORITHM: Main Event Loop

### Step 1: Initialize Application

Launch Textual app, set up layout, run initial health check.

```
app = NgramApp()
await app.compose()  # Build widget tree
health = await run_doctor_check()
update_status_bar(health)
focus_input_bar()
```

### Step 2: Await User Input

Input bar captures text. On Enter, parse and dispatch.

```
while running:
    text = await input_bar.get_input()
    command = parse_input(text)
    await dispatch_command(command)
```

### Step 3: Parse Input

```
IF text starts with "/":
    Split into command name and args
    Return SlashCommand(name, args)
ELSE:
    Return natural language input (for future ngram manager)
```

### Step 4: Dispatch Command

```
MATCH command.name:
    "/repair" -> handle_repair(args)
    "/doctor" -> handle_doctor()
    "/help"   -> handle_help()
    "/quit"   -> handle_quit()
    _         -> show_unknown_command_error()
```

---

## KEY DECISIONS

### D0: Agent Provider

```
IF --agents=codex:
    Use codex exec resume --last for manager prompts
    Parse plain text output
ELIF --agents=gemini:
    Use gemini --resume latest for manager prompts
    Parse plain text output
ELSE:
    Use claude --continue with stream-json output
```

### D1: Handle /repair Command

```
IF repair already running:
    Show "Repair in progress" message
    Return
ELSE:
    issues = await run_doctor()
    IF no issues:
        Show "No issues found"
    ELSE:
        spawn_agents(issues)
        update_agent_panels()
```

### D2: Agent Panel Layout

```
IF active_agents.count <= 3:
    Show all as columns (equal width)
ELSE:
    Show first 3 as columns
    Add tab bar for remaining agents
    Tabs switch which agent is in column 3
```

### D3: Agent Completion

```
WHEN agent process exits:
    IF exit_code == 0 AND "REPAIR COMPLETE" in output:
        Mark agent as completed (green indicator)
    ELSE:
        Mark agent as failed (red indicator)

    Update health score (re-run quick check)
    IF all agents done:
        Show summary in manager panel
```

---

## DATA FLOW

```
User Input
    │
    ▼
┌──────────────────┐
│   Input Bar      │ ← Textual Input widget
└────────┬─────────┘
         │ text string
         ▼
┌──────────────────┐
│  Command Parser  │ ← parse_input()
└────────┬─────────┘
         │ SlashCommand
         ▼
┌──────────────────┐
│ Command Handler  │ ← handle_repair(), etc.
└────────┬─────────┘
         │ spawns agents
         ▼
┌──────────────────┐
│  repair_core.py  │ ← spawn_repair_agent_async()
└────────┬─────────┘
         │ asyncio.Process per agent
         ▼
┌──────────────────┐
│  Agent Panels    │ ← Real-time output streaming
└──────────────────┘
```

---

## COMPLEXITY

**Time:** O(n) per repair cycle — where n is number of issues

**Space:** O(n * m) — n agents * m output lines buffered

**Bottlenecks:**
- Agent spawn time (subprocess creation)
- Output buffering for very verbose agents
- Tab switching with many agents

---

## HELPER FUNCTIONS

### `parse_input(text: str) -> SlashCommand | str`

**Purpose:** Convert raw input to structured command

**Logic:** Check for leading `/`, split on whitespace, return command or raw text

### `spawn_agents(issues: List[DoctorIssue])`

**Purpose:** Start repair agent processes for each issue

**Logic:** For each issue, call `spawn_repair_agent_async()` with output callback that updates corresponding panel

### `update_agent_panel(agent_id: str, line: str)`

**Purpose:** Append output line to agent's panel

**Logic:** Find panel by ID, append line, scroll if at bottom

### `run_doctor_check() -> int`

**Purpose:** Get current health score

**Logic:** Run `ngram doctor --json`, extract score

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| `repair_core.py` | `spawn_repair_agent_async()` | RepairResult |
| `doctor.py` | `run_doctor_checks()` | List[DoctorIssue], score |
| `textual` | Widget composition | UI layout |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Algorithm for resizing panels on terminal resize
- [ ] How to handle agent output parsing for progress indicators
- IDEA: Progress bars for agents based on output patterns
- IDEA: Pause/resume agent execution
- QUESTION: Should ngram manager run continuously in background?
