# ngram TUI — Health: Verification Mechanics and Coverage

```
STATUS: STABLE
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This file defines the health verification mechanics for the ngram TUI. It ensures the interactive experience remains functional, responsive, and accurately reflects the state of the underlying system.

It safeguards:
- **Interaction Integrity:** Ensuring user inputs (natural language and slash commands) are correctly processed.
- **Visual Feedback:** Ensuring that agent status, project health, and repair progress are correctly displayed.
- **Async Robustness:** Ensuring the app handles multiple parallel agent streams without crashing or freezing.

Boundaries:
- This file covers the TUI application logic and widget coordination.
- It does not verify the deep internal logic of LLM agents (covered in `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`).
- It does not verify the core CLI commands when run outside the TUI.

---

## WHY THIS PATTERN

HEALTH is separate from tests because it verifies real system health without changing implementation files. For a TUI, this is especially valuable as it can monitor for rendering lag, deadlocks, or misaligned state between the UI and the backend.

- **Failure mode avoided:** The TUI showing a "Repairing..." status indefinitely because a subprocess died silently.
- **Docking-based checks:** Uses the `SessionState` and widget mount events as docking points.
- **Throttling:** Ensures UI-intensive checks (like refreshing the project map) don't degrade the user experience.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_TUI_Design.md
BEHAVIORS:       ./BEHAVIORS_TUI_Interactions.md
ALGORITHM:       ./ALGORITHM_TUI_Flow.md
VALIDATION:      ./VALIDATION_TUI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_TUI_Code_Architecture.md
THIS:            HEALTH_TUI_Coverage.md
SYNC:            ./SYNC_TUI_State.md

IMPL:            ngram/tui/app.py
```

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: tui_main_event_loop
    purpose: Manages the lifecycle of the TUI. Failure makes the tool unusable.
    triggers:
      - type: manual
        source: cli:ngram (no args)
    frequency:
      expected_rate: 1/session
      peak_rate: 1/sec (restart cycle)
      burst_behavior: stable
    risks:
      - V-TUI-MOUNT: App fails to mount widgets
    notes: Heavily relies on Textual's async engine.

  - flow_id: command_execution_flow
    purpose: Processes user commands. Failure breaks the core interaction loop.
    triggers:
      - type: event
        source: tui:input_bar
    frequency:
      expected_rate: 5/min
      peak_rate: 20/min
      burst_behavior: bursts during interactive repair
    risks:
      - V-TUI-CMD: Slash commands fail to parse
    notes: Handles both natural language and /commands.

  - flow_id: agent_stream_coordination
    purpose: Renders parallel agent outputs. Failure leads to UI jitter or data loss.
    triggers:
      - type: event
        source: ngram/llms/gemini_agent.py
    frequency:
      expected_rate: 10/sec (streaming chunks)
      peak_rate: 100/sec (multi-agent)
      burst_behavior: highly bursty
    risks:
      - V-TUI-ASYNC: UI lockups during heavy streaming
    notes: Critical for multi-agent "swarming" behavior.
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: input_responsiveness
    flow_id: command_execution_flow
    priority: high
    rationale: Laggy input feels broken to users.
  - name: state_synchronization
    flow_id: agent_stream_coordination
    priority: high
    rationale: The UI must match the actual status of background agents.
  - name: layout_integrity
    flow_id: tui_main_event_loop
    priority: med
    rationale: Ensures tabs and panels remain visible and correctly sized.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: .ngram/state/SYNC_Project_Health.md
  result:
    representation: enum
    value: OK
    updated_at: 2025-12-20T00:00:00Z
    source: tui_main_event_loop
```

---

## DOCK TYPES (COMPLETE LIST)

- `event` (Textual message bus)
- `process` (Agent subprocess handles)
- `cli` (TUI launch command)

---

## CHECKER INDEX

```yaml
checkers:
  - name: widget_mount_check
    purpose: Verifies that all critical panels (Manager, Agents, Status) mount successfully.
    status: active
    priority: high
  - name: command_parse_check
    purpose: Verifies that common slash commands parse to the correct objects.
    status: active
    priority: high
  - name: agent_handle_leak_check
    purpose: Monitors for abandoned agent subprocesses or handles.
    status: active
    priority: med
```

---

## INDICATOR: Input Responsiveness

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: input_responsiveness
  client_value: Users can type and execute commands without perceived delay.
  validation:
    - validation_id: V-TUI-LATENCY
      criteria: Command processing latency must be < 100ms for UI-only actions.
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed:
    - float_0_1
  selected:
    - float_0_1
  semantics:
    float_0_1: Inverse of latency (1.0 = immediate, 0.0 = > 500ms delay).
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: input_submitted
    method: on_input_bar_command_submitted
    location: ngram/tui/app.py:300
```

---

## HOW TO RUN

```bash
# Manual verification of slash commands
# Type /help, /doctor, /repair in the TUI input bar.

# Manual verification of agent panels
# Run /repair and verify that agent panels appear and stream output.
```

---

## KNOWN GAPS

- [ ] No automated visual regression tests for layout.
- [ ] No automated check for terminal color compatibility.
- [ ] No automated unit tests for `manager.py` logic.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Use Textual's `App.run_test()` for automated health verification in CI.
- IDEA: Add a "TUI Health" overlay for developers to see internal latency and event counts.
- QUESTION: How should we handle terminal resizing failures in HEALTH?
