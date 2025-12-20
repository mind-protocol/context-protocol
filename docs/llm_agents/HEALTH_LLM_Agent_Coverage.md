# ngram LLM Agents — Health: Verification Mechanics and Coverage

```
STATUS: STABLE
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This file defines the health verification mechanics for the ngram LLM Agents (primarily the Gemini adapter). It ensures that the communication between the ngram core and the underlying LLM provider is robust, correctly formatted, and resilient to failures.

It safeguards:
- **Output Correctness:** Ensuring streaming JSON or plain text formats match expectations.
- **Error Handling:** Ensuring API failures or missing credentials are surfaced correctly.
- **Performance:** Monitoring for excessive latency or token consumption issues.

Boundaries:
- This file covers the provider-specific subprocess behavior.
- It does not verify the quality of the LLM responses (subjective).
- It does not verify the CLI logic that calls these agents (covered in `docs/cli/HEALTH_CLI_Coverage.md`).

---

## WHY THIS PATTERN

HEALTH is separate from tests because it verifies real system health without changing implementation files. For LLM agents, this allows monitoring real-world interactions and detecting provider-side drift or API changes without modifying the core adapter code.

- **Failure mode avoided:** Provider API updates that change the JSON schema, leading to silent failures in the TUI.
- **Docking-based checks:** Uses the subprocess stdout/stderr and exit codes as docking points.
- **Throttling:** Prevents excessive API costs by running heavy verification checks at a low cadence.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Provider_Specific_LLM_Subprocesses.md
BEHAVIORS:       ./BEHAVIORS_Gemini_Agent_Output.md
ALGORITHM:       ./ALGORITHM_Gemini_Stream_Flow.md
VALIDATION:      ./VALIDATION_Gemini_Agent_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_LLM_Agent_Code_Architecture.md
THIS:            HEALTH_LLM_Agent_Coverage.md
SYNC:            ./SYNC_LLM_Agents_State.md

IMPL:            ngram/llms/gemini_agent.py
```

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: gemini_stream_flow
    purpose: Main interaction loop with the LLM. Failure breaks all AI functionality.
    triggers:
      - type: event
        source: cli:ngram repair or tui:manager
    frequency:
      expected_rate: 5/min
      peak_rate: 50/min
      burst_behavior: throttled by provider rate limits
    risks:
      - V-GEMINI-JSON: Invalid JSON streaming format
    notes: Heavily dependent on GEMINI_API_KEY being set.
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: stream_validity
    flow_id: gemini_stream_flow
    priority: high
    rationale: TUI depends on parsing every JSON chunk correctly.
  - name: api_connectivity
    flow_id: gemini_stream_flow
    priority: high
    rationale: Detects missing credentials or network issues immediately.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: .ngram/state/SYNC_Project_Health.md
  result:
    representation: binary
    value: 1
    updated_at: 2025-12-20T00:00:00Z
    source: gemini_stream_flow
```

---

## DOCK TYPES (COMPLETE LIST)

- `process` (gemini_agent.py subprocess)
- `stream` (stdout JSON chunks)
- `auth` (GEMINI_API_KEY environment variable)

---

## CHECKER INDEX

```yaml
checkers:
  - name: json_format_checker
    purpose: Validates that every chunk is a valid JSON object of the correct type.
    status: active
    priority: high
  - name: auth_credential_checker
    purpose: Verifies that required API keys are available and valid.
    status: active
    priority: high
```

---

## INDICATOR: Stream Validity

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: stream_validity
  client_value: The TUI and CLI can reliably parse agent outputs in real-time.
  validation:
    - validation_id: V-GEMINI-JSON
      criteria: Chunks must be valid newline-delimited JSON with 'type' and 'content' fields.
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed:
    - float_0_1
  selected:
    - float_0_1
  semantics:
    float_0_1: Percentage of successfully parsed chunks in the last session.
```

### DOCKS SELECTED

```yaml
docks:
  output:
    id: assistant_chunks
    method: main
    location: ngram/llms/gemini_agent.py:400
```

---

## HOW TO RUN

```bash
# Manual verification of stream JSON
python3 -m ngram.llms.gemini_agent -p "ping" --output-format stream-json

# Manual verification of plain text
python3 -m ngram.llms.gemini_agent -p "ping" --output-format text
```

---

## KNOWN GAPS

- [ ] No automated check for response latency.
- [ ] No check for provider-side rate limit errors (429).
- [ ] No automated unit tests for `gemini_agent.py` internals.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add a "health probe" prompt to quickly verify API connectivity.
- QUESTION: Should we monitor token usage per-session in HEALTH?
