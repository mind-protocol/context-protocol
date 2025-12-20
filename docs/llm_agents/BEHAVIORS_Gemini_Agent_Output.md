# ngram LLM Agents — Behaviors: Gemini Agent Output

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against commit ad538f8
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Provider_Specific_LLM_Subprocesses.md
THIS:            BEHAVIORS_Gemini_Agent_Output.md (you are here)
ALGORITHM:       ./ALGORITHM_Gemini_Stream_Flow.md
VALIDATION:      ./VALIDATION_Gemini_Agent_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_LLM_Agent_Code_Architecture.md
HEALTH:          ./HEALTH_LLM_Agent_Coverage.md
SYNC:            ./SYNC_LLM_Agents_State.md
```

---

## BEHAVIORS

### B1: Missing API Key

```
GIVEN:  The process is started without --api-key, GEMINI_API_KEY in .env, or GEMINI_API_KEY env var
WHEN:   The adapter initializes
THEN:   A JSON error message is printed to stdout
AND:    The process exits with code 1
```

### B2: Streaming JSON Output

```
GIVEN:  --output-format stream-json (default)
WHEN:   A Gemini response is streamed
THEN:   Each text chunk emits a JSON message with type=assistant
AND:    Each message includes content[{type: "text", text: <chunk>}]
AND:    A final JSON message with type=result includes the full response
```

### B3: Plain Text Output

```
GIVEN:  --output-format text
WHEN:   The adapter receives a Gemini response
THEN:   The response text is printed to stdout as plain text
```

### B4: Model Listing Debug Output

```
GIVEN:  The adapter starts successfully
WHEN:   The model list is requested
THEN:   Available model IDs are printed to stderr
AND:    Errors in listing models are printed to stderr
```

### B5: Tool Execution Output

```
GIVEN:  The Gemini response includes tool calls
WHEN:   The adapter processes tool calls
THEN:   A tool_code JSON message is emitted for each tool invocation
AND:    A tool_result JSON message is emitted with either data or an error
```

---

## NOTES

Input shaping for system prompts and tool use is documented in the ALGORITHM/VALIDATION docs to avoid duplication here.
