# ngram TUI — Behaviors: User Interactions and Observable Effects

```
STATUS: IMPLEMENTED
CREATED: 2025-12-18
VERIFIED: 2025-12-18 — core behaviors working (B6, B8, B10, B12 implemented 2025-12-18)
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_TUI_Modular_Interface_Design.md
THIS:            BEHAVIORS_TUI_Interactions.md
ALGORITHM:       ./ALGORITHM_TUI_Widget_Interaction_Flow.md
VALIDATION:      ./VALIDATION_TUI_User_Interface_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_TUI_Code_Architecture.md
HEALTH:          ./HEALTH_TUI_Component_Test_Coverage.md
SYNC:            ./SYNC_TUI_Development_Current_State.md
```

---

## BEHAVIORS

### B1: Launch TUI

```
GIVEN:  User is in project with .ngram directory
WHEN:   User runs `ngram` (no subcommand)
THEN:   TUI launches with multi-column layout
AND:    Manager panel appears on left (~30% width)
AND:    Agent panel area appears on right
AND:    Input bar appears at bottom with prompt
AND:    Health score displays in status bar
```

### B2: Execute Slash Command

```
GIVEN:  TUI is running with input focus
WHEN:   User types `/repair` and presses Enter
THEN:   Repair session starts
AND:    Manager panel shows orchestration status
AND:    Agent panels show individual agent outputs
AND:    Input returns to prompt when complete
```

### B3: Run Doctor Command

```
GIVEN:  TUI is running
WHEN:   User types `/doctor` and presses Enter
THEN:   Health check runs
AND:    Health score updates in status bar
```

### B3.1: Chat with Manager

```
GIVEN:  TUI is running with input focus
WHEN:   User types non-command text and presses Enter
THEN:   User input displays in blue with blank line before
AND:    Animated "..." appears while waiting
AND:    Agent thinking displays in dim italic (Claude only)
AND:    Agent response displays in manager panel
AND:    Conversation resumes on each turn (Claude, Gemini, or Codex)
```

### B3.2: Display SYNC on Launch

```
GIVEN:  TUI launches successfully
WHEN:   Doctor check completes
THEN:   Right panel shows contents of ...ngram/state/SYNC_Project_State.md
AND:    If SYNC file missing, shows issues list instead
AND:    CHANGES tab header shows recent changes/commits per minute
```

### B4: Quit TUI

```
GIVEN:  TUI is running
WHEN:   User types `/quit` or presses Ctrl+C
THEN:   TUI exits gracefully
AND:    Control returns to terminal
```

### B5: Display Multiple Agents

```
GIVEN:  Repair session with multiple issues
WHEN:   Agents spawn for each issue
THEN:   Each agent gets its own column (up to 3)
AND:    If >3 agents, tabs appear for switching
AND:    Agent outputs stream in real-time
AND:    Repository map (map.md) refreshes after each successful agent
```

### B6: Streaming Responses

```
GIVEN:  User sends message to manager
WHEN:   Agent generates response
THEN:   Text streams to manager panel as it arrives
AND:    "..." indicator replaced progressively with text
AND:    Thinking blocks appear in dim italic as they arrive
```

### B7: Issues Command

```
GIVEN:  TUI is running with SYNC displayed
WHEN:   User types `/issues`
THEN:   Right panel switches to issues list
AND:    Issues colored by severity (red/orange/dim)
```

### B8: Input History

```
GIVEN:  User has sent previous messages
WHEN:   User presses Up arrow
THEN:   Previous input appears in input bar
AND:    Down arrow navigates forward through history
AND:    Current draft is preserved when navigating history
```

### B10: Auto-Scroll

```
GIVEN:  Manager panel has messages
WHEN:   New message added
THEN:   Panel scrolls to show latest message
AND:    AgentPanel scrolls when output appended
AND:    Static content (SYNC/issues) wrapped in VerticalScroll for scrollability
```

### B12: Resize Handling

```
GIVEN:  TUI is running
WHEN:   Terminal window resizes
THEN:   Status bar health repositions to right
AND:    Panels adjust proportionally
```

---

## INPUTS / OUTPUTS

### Primary Interface: Input Bar

**Inputs:**

| Input | Type | Description |
|-------|------|-------------|
| User text | string | Commands starting with `/` or natural language |
| Enter key | keypress | Submit input |
| Ctrl+C | keypress | Quit TUI |

**Outputs:**

| Output | Location | Description |
|--------|----------|-------------|
| Manager messages | Left panel | Orchestration status, decisions |
| Agent outputs | Right columns | Individual agent work streams |
| Health score | Status bar | Current project health 0-100 |
| Command feedback | Manager panel | Response to slash commands |

**Side Effects:**

- File system changes (repairs, doc updates)
- Project state changes (via repair agents)
- SYNC file updates

---

## EDGE CASES

### E1: No Issues Found

```
GIVEN:  User runs `/repair` but doctor finds no issues
THEN:   Manager panel shows "No issues to repair"
AND:    Input returns to prompt
```

### E2: Textual Not Installed

```
GIVEN:  User runs `ngram` but textual is not installed
THEN:   Helpful error message shows
AND:    Suggests: `pip install ngram[tui]`
```

### E3: Agent Timeout

```
GIVEN:  Agent runs for >10 minutes
THEN:   Agent is terminated
AND:    Manager panel shows timeout message
AND:    Other agents continue
```

### E4: Very Long Output

```
GIVEN:  Agent produces very long output
THEN:   Panel scrolls automatically
AND:    User can scroll back to review
```

---

## ANTI-BEHAVIORS

### A1: Never Block on Single Agent

```
GIVEN:   Multiple repair agents running
WHEN:    One agent takes long or fails
MUST NOT: Block other agents from running
INSTEAD:  Other agents continue independently
```

### A2: Never Lose Output

```
GIVEN:   Agent produces output
WHEN:    Output is longer than visible area
MUST NOT: Discard output or truncate silently
INSTEAD:  Buffer output, allow scrolling
```

### A3: Never Corrupt Terminal

```
GIVEN:   TUI exits (normal or crash)
WHEN:    Control returns to terminal
MUST NOT: Leave terminal in broken state
INSTEAD:  Reset terminal modes properly
```

### A4: Never Run Without Context

```
GIVEN:   User is outside project directory
WHEN:    User runs `ngram`
MUST NOT: Launch TUI in wrong context
INSTEAD:  Show error about missing .ngram directory
```

---

## IMPLEMENTATION REFERENCES

- `ngram/tui/commands.py` — Slash command router used by the TUI input bar to map `/repair`, `/doctor`, and other commands to handlers.

```
IMPL: ngram/tui/commands.py
```

---

## MARKERS

- [x] RESOLVED: Natural language input goes to manager agent via subprocess

### Planned Behaviors

#### B9: Tab Completion
```
GIVEN:  User types `/` in input bar
WHEN:   User presses Tab
THEN:   Command autocompletes or shows options
```

#### B11: Markdown Rendering
```
GIVEN:  SYNC file displayed in right panel
WHEN:   File contains markdown formatting
THEN:   Markdown renders with proper styling
AND:    Code blocks have syntax highlighting
```

### Open Questions
<!-- @ngram:todo Behavior when agent produces binary/non-text output -->
