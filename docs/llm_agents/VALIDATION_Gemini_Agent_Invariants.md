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
HEALTH:          ./HEALTH_LLM_Agent_Coverage.md
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

---

## PROPERTIES

- `GeminiAdapter` enforces stream shape and error isolation, so downstream consumers never see mixing of JSON/state text.
- The invariants are agnostic to model selection; a new provider must still satisfy these behaviors before being considered safe.

---

## ERROR CONDITIONS

- `MissingCredential`: raised when GEMINI_API_KEY is not found in env, config, or CLI.
- `StreamShapeViolation`: when `stream-json` output omits `type: "assistant"`.
- `ToolCallFailure`: emitted as the `tool_result` message when tool execution errors occur.

---

## HEALTH COVERAGE

- `prompt_doc_reference_check` now depends on the Gemini adapter referencing `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`.
- `doctor_check_code_doc_delta_coupling` ensures doc/SYNC/implementation updates stay in sync with adapter changes.
- `doctor_check_yaml_drift` now monitors `modules.yaml` entries so additional providers self-document.

---

## VERIFICATION PROCEDURE

1. Run `NG_ENV=dev ngram repair --provider gemini` and assert the output structure rules hold.
2. Validate error detection by unsetting `GEMINI_API_KEY` and confirming the CLI exits with a JSON error.
3. Add a new provider and verify these invariants via the same tests before marking the change canonical.

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-21
VERIFIED_AGAINST:
    impl: ngram/llms/gemini_agent.py @ HEAD
VERIFIED_BY: codex
RESULT:
    V1: PASS
    V2: PASS
    V3: PASS
    V4: PASS
    V5: PASS
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Should we define explicit severity weighting for stream errors vs. tool failures?
- IDEA: Add JSON schema validation for `tool_result` payloads so downstream parsers can rely on a rigid contract.
