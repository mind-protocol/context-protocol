# ngram LLM Agents — Validation: Gemini Agent Invariants

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against commit ad538f8
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Provider_Specific_LLM_Subprocesses.md
BEHAVIORS:       ./BEHAVIORS_Gemini_Agent_Output.md
ALGORITHM:       ./ALGORITHM_Gemini_Stream_Flow.md
THIS:            VALIDATION_Gemini_Agent_Invariants.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_LLM_Agent_Code_Architecture.md
TEST:            ./TEST_LLM_Agent_Coverage.md
SYNC:            ./SYNC_LLM_Agents_State.md
```

---

## INVARIANTS

### V1: Missing Credentials Fail Fast

- If GEMINI_API_KEY is absent from all sources, the adapter emits a JSON error and exits with code 1.

### V2: Streaming Output Shape

- For `stream-json`, each streamed chunk must be wrapped in a JSON object with `type: "assistant"` and a `message.content` list containing text parts.
- A final JSON object with `type: "result"` must include the full concatenated response text.

### V3: Text Output Is Plain

- For `text`, the adapter prints only the response text with no JSON wrapper.

### V4: Debug Output Is Isolated

- Model listing and related errors are written to stderr only, so stdout remains parseable for the TUI.

### V5: Tool Calls Return Structured Results

- Tool calls emit a `tool_code` message and a corresponding `tool_result` message on stdout.
- Tool execution errors return a JSON object with an `error` key instead of raising.

---

## EDGE CASES

- Gemini returns empty chunks: only non-empty chunk.text should be emitted.
- Gemini SDK throws during model listing: the adapter still proceeds after logging to stderr.

---

## VERIFICATION METHODS

- Manual run with/without GEMINI_API_KEY to verify error handling.
- Manual run with `--output-format stream-json` to confirm JSON structure.
- Manual run with `--output-format text` to confirm plain output.

---

## FAILURE MODES

- Missing `GEMINI_API_KEY` produces a JSON error and exit 1.
- Unexpected SDK exceptions are returned as JSON error objects on stdout.
