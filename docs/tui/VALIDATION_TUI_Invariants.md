# ngram TUI — Validation: Invariants and Verification

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
ALGORITHM:       ./ALGORITHM_TUI_Flow.md
THIS:            VALIDATION_TUI_Invariants.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_TUI_Code_Architecture.md
HEALTH:          ./HEALTH_TUI_Coverage.md
SYNC:            ./SYNC_TUI_State.md
```

---

## INVARIANTS

These must ALWAYS be true:

### V1: Terminal State Preservation

```
After TUI exits (normal or crash), terminal must be in usable state.
No raw mode artifacts, no broken cursor, no color leaks.
```

**Checked by:** Manual testing, try/finally cleanup in app

### V2: Agent Isolation

```
Each agent process runs independently.
Failure of agent N does not affect agents 1..N-1 or N+1..M.
```

**Checked by:** Kill one agent process, verify others continue

### V3: Output Completeness

```
All agent output lines are captured and displayed.
No silent drops, no truncation without indication.
```

**Checked by:** Compare subprocess output with displayed lines

### V4: Command Atomicity

```
Slash commands either complete fully or show error.
Partial execution states are not user-visible.
```

**Checked by:** Test interrupt during command execution

### V5: Layout Consistency

```
Manager panel always visible on left.
Agent area always visible on right.
Input bar always visible at bottom.
```

**Checked by:** Test with various terminal sizes

---

## PROPERTIES

For property-based testing:

### P1: Health Score Bounds

```
FORALL health_score:
    0 <= health_score <= 100
```

**Tested by:** NOT YET TESTED — awaiting implementation

### P2: Agent Count Consistency

```
FORALL active_agents:
    len(displayed_panels) == min(3, len(active_agents))
    IF len(active_agents) > 3:
        tabs_count == len(active_agents) - 2
```

**Tested by:** NOT YET TESTED — awaiting implementation

### P3: Command Parsing Determinism

```
FORALL input_text:
    parse_input(input_text) == parse_input(input_text)
    (same input always produces same command)
```

**Tested by:** NOT YET TESTED — awaiting implementation

---

## ERROR CONDITIONS

### E1: Textual Import Failure

```
WHEN:    textual package not installed
THEN:    ImportError caught at entry point
SYMPTOM: CLI error message with install instructions
```

**Tested by:** NOT YET TESTED — test without textual installed

### E2: Agent Spawn Failure

```
WHEN:    agent CLI not available or permission denied
THEN:    Agent marked as failed immediately
SYMPTOM: Error message in agent panel, red indicator
```

**Tested by:** NOT YET TESTED — test with missing agent binary

### E3: Terminal Too Small

```
WHEN:    Terminal width < 80 or height < 24
THEN:    Warning displayed, layout may degrade
SYMPTOM: Truncated panels or warning banner
```

**Tested by:** NOT YET TESTED — test with small terminal

### E4: Process Zombie Prevention

```
WHEN:    TUI exits while agents running
THEN:    All agent processes terminated
SYMPTOM: No orphan processes after exit
```

**Tested by:** NOT YET TESTED — check for orphans after force quit

---

## HEALTH COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: Terminal State | — | NOT YET IMPLEMENTED |
| V2: Agent Isolation | — | NOT YET IMPLEMENTED |
| V3: Output Complete | — | NOT YET IMPLEMENTED |
| V4: Command Atomic | — | NOT YET IMPLEMENTED |
| V5: Layout Consist | — | NOT YET IMPLEMENTED |
| E1: Import Failure | — | NOT YET IMPLEMENTED |
| E2: Spawn Failure | — | NOT YET IMPLEMENTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Launch TUI in project directory - shows correctly
[ ] Run /doctor - health check works
[ ] Run /repair - agents spawn and display
[ ] Ctrl+C during repair - exits cleanly
[ ] Terminal usable after exit
[ ] Test with 1, 3, 5 agents - layout adjusts
[ ] Resize terminal - panels reflow
[ ] Force kill TUI - no zombie processes
```

### Automated

```bash
# Once tests exist:
pytest tests/tui/test_app.py

# With coverage:
pytest tests/tui/ --cov=ngram.tui
```

---

## SYNC STATUS

```
LAST_VERIFIED: Not yet
VERIFIED_AGAINST: Implementation pending
VERIFIED_BY: —
RESULT: NOT RUN (no implementation yet)
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Property test for output ordering (messages arrive in order)
- [ ] Invariant for concurrent command handling (what if user types during repair?)
- IDEA: Fuzzing for command parser
- IDEA: Stress test with many rapid commands
- QUESTION: How to test async Textual apps effectively?
