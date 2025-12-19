# LLM Agents — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Provider_Specific_LLM_Subprocesses.md
BEHAVIORS:       ./BEHAVIORS_Gemini_Agent_Output.md
ALGORITHM:       ./ALGORITHM_Gemini_Stream_Flow.md
VALIDATION:      ./VALIDATION_Gemini_Agent_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_LLM_Agent_Code_Architecture.md
TEST:            ./TEST_LLM_Agent_Coverage.md
THIS:            SYNC_LLM_Agents_State.md (you are here)
```

---

## MATURITY

**What's canonical (v1):**
- `gemini_agent.py` provides a Gemini CLI wrapper for the TUI/CLI.
- Streamed JSON output matches the TUI expectations used by other agents.

**What's still being designed:**
- Shared abstractions for additional LLM providers.
- Tool support and richer message formatting for Gemini.

**What's proposed (v2+):**
- A reusable adapter base class for multi-provider consistency.
- Configurable model selection via CLI flags.

---

## CURRENT STATE

`ngram/llms/gemini_agent.py` implements a standalone CLI process that authenticates with GEMINI_API_KEY (CLI arg, `.env`, or env var), sends a prompt to Gemini, and streams JSON output for the TUI. The CLI builds the subprocess invocation from `ngram/agent_cli.py` when the `gemini` provider is selected.

---

## IN PROGRESS

None.

---

## RECENT CHANGES

### 2025-12-19: Documented LLM agent module

- **What:** Added full doc chain + module mapping for `ngram/llms`.
- **Why:** The module was previously undocumented, causing unmapped code warnings and incomplete chain validation failures.
- **Files:** `docs/llm_agents/BEHAVIORS_Gemini_Agent_Output.md`, `docs/llm_agents/ALGORITHM_Gemini_Stream_Flow.md`, `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md`, `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md`, `docs/llm_agents/TEST_LLM_Agent_Coverage.md`, `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`, `docs/llm_agents/SYNC_LLM_Agents_State.md`, `modules.yaml`, `ngram/llms/gemini_agent.py`
- **Struggles/Insights:** Needed the full chain to satisfy `ngram validate`.

---

## KNOWN ISSUES

None noted.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Documentation only; no behavior changes.

**What you need to understand:**
The Gemini adapter is a thin wrapper intended to isolate provider SDK usage. It streams JSON chunks for the TUI but does not support tool use or model selection.

**Watch out for:**
The adapter prints model listings to stderr unconditionally; consider gating if that output is noisy.

**Open questions I had:**
Should we standardize adapter helpers for streaming JSON and error handling?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
LLM agent docs now exist for the Gemini adapter, with module mapping and a DOCS pointer added.

**Decisions made:**
Documented the module as DESIGNING and kept the chain minimal (PATTERNS + SYNC).

**Needs your input:**
None.

---

## TODO

### Doc/Impl Drift

- [ ] IMPL→DOCS: If a shared adapter helper is introduced, expand the doc chain.

### Tests to Run

```bash
# No module-specific tests documented yet.
```

### Immediate

- [ ] None.

### Later

- [ ] Add BEHAVIORS/ALGORITHM/IMPLEMENTATION docs once multiple providers exist.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Calm, focused on minimal documentation to satisfy mapping requirements.

**Threads I was holding:**
Whether to document the stderr model listing as a known issue and whether to add more doc chain files.

**Intuitions:**
A shared adapter helper will likely appear once a second provider is added.

**What I wish I'd known at the start:**
That only the Gemini adapter exists, so the docs should stay lean.

---

## POINTERS

| What | Where |
|------|-------|
| Gemini adapter | `ngram/llms/gemini_agent.py` |
| CLI integration | `ngram/agent_cli.py` |
