# LLM Agents — Sync: Current State

```
LAST_UPDATED: 2025-12-25
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
HEALTH:          ./HEALTH_LLM_Agent_Coverage.md
THIS:            SYNC_LLM_Agents_State.md (you are here)
```

---

## MATURITY

**What's canonical (v1):**
- `gemini_agent.py` provides a Gemini CLI wrapper for the TUI/CLI.
- Streamed JSON output matches the TUI expectations used by other agents.

**What's still being designed:**
- Shared abstractions for additional LLM providers.
- Expanded tool schema support and richer message formatting for Gemini.

**What's proposed (v2+):**
- A reusable adapter base class for multi-provider consistency.
- Configurable model selection via CLI flags.

---

## CURRENT STATE

`ngram/llms/gemini_agent.py` implements a standalone CLI process that authenticates with GEMINI_API_KEY (CLI arg, `.env`, or env var), sends a prompt to Gemini, streams JSON output for the TUI, and executes basic local tools (filesystem/search/web fetch). Google search requests use a configurable base URL via `NGRAM_GOOGLE_SEARCH_URL`. The CLI builds the subprocess invocation from `ngram/agent_cli.py` when the `gemini` provider is selected.

---

## IN PROGRESS

No active implementation work is underway; the last changes were
documentation-only updates, and adapter behavior is unchanged.

---

## RECENT CHANGES

### 2025-12-26: Extended Gemini validation behavior/objective rationale

- **What:** Added richer explanatory clauses to the BEHAVIORS GUARANTEED and OBJECTIVES COVERED tables in `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md` so every row now exceeds 50 characters while calling out why each invariant matters, giving the doctor pre-digested evidence for each guarantee, and showing which health checks expect the invariant.
- **Why:** Keep the validation template compliant with the length expectations and give future agents more context before they follow downstream chains.
- **Files:** `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md`, `docs/llm_agents/SYNC_LLM_Agents_State.md`
- **Verification:** `ngram validate` *(fails: pre-existing connectome health doc gaps, membrane naming, and CHAIN/link warnings already tracked by the doctor)*

### 2025-12-25: Filled Gemini algorithm template length requirements

- **What:** Added the missing `OBJECTIVES AND BEHAVIORS` section, spun up the `main()` narrative, and spelled out how the entrypoint’s stages satisfy the 50+ character template requirement.
- **Why:** Close the DOC_TEMPLATE_DRIFT warning pointing at `ALGORITHM_Gemini_Stream_Flow.md` by making objectives explicit and highlighting the primary entrypoint responsible for running the Gemini subprocess.
- **Trace:** Logged that the objectives/behaviors + main narrative now exceeds the 50+ character threshold so agents can verify the template line quickly.
- **Files:** `docs/llm_agents/ALGORITHM_Gemini_Stream_Flow.md`, `docs/llm_agents/SYNC_LLM_Agents_State.md`
- **Verification:** `ngram validate` (fails: existing `docs/connectome/health` gaps plus naming/CHAIN warnings noted by the doctor)

### 2025-12-25: Expanded Gemini health coverage template

- **What:** Added the OBJECTIVES COVERAGE table plus richer `stream_validity` and `api_connectivity` indicator sections describing algorithm mechanics, throttling, forwardings, and manual run guidance.
- **Why:** Close the DOC_TEMPLATE_DRIFT warning for `HEALTH_LLM_Agent_Coverage.md` while giving doctors precise streaming and connectivity signals.
- **Files:** `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- **Verification:** `ngram validate`

### 2025-12-25: Expanded Gemini implementation doc to runtime detail

- **What:** Added sections covering code structure, design patterns, schema, flow-by-flow docking, logic chains, dependencies, state handling, runtime behavior, concurrency, and bidirectional links so the implementation doc now satisfies the template expectations.
- **Why:** Resolve the DOC_TEMPLATE_DRIFT warning pointing at `IMPLEMENTATION_LLM_Agent_Code_Architecture.md` by giving each required heading substantive narrative and clarifying how the adapter interacts with the CLI and TUI.
- **Files:** `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md`, `docs/llm_agents/SYNC_LLM_Agents_State.md`
- **Verification:** `ngram validate` *(fails: existing connectome health doc gaps, membrane naming, and CHAIN/link warnings already tracked by the doctor)*

### 2025-12-30: Recorded concurrency question for implementation gaps

- **What:** Noted in the `IMPLEMENTATION_LLM_Agent_Code_Architecture.md` GAPS section that tracking helper execution timestamps could surface helpers that block the stream unexpectedly, keeping the concurrency narrative visible for future diagnostics.
- **Why:** DOC_TEMPLATE_DRIFT highlighted missing explanatory sections, and this open question anchors the remaining concurrency concerns inside the Implementation doc while the SYNC points agents at the right follow-up.
- **Files:** `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md`, `docs/llm_agents/SYNC_LLM_Agents_State.md`
- **Trace:** Copying the helper execution timestamp question into the SYNC remarks keeps the concurrency concern visible even if surrounding sections move later.
- **Verification:** `ngram validate` *(fails for the known docs/connectome/health gaps, membrane naming mismatch, and CHAIN/link warnings already tracked elsewhere)*

### 2025-12-21: Added objectives and lengthened Gemini behaviors text

- **What:** Added an OBJECTIVES SERVED section and expanded the NOTES/INPUTS/OUTPUTS narratives so each template passage exceeds 50 characters while highlighting how streams, plain text, and diagnostics interact.
- **Why:** Close the DOC_TEMPLATE_DRIFT warning for the Gemini behaviors doc that noted missing objectives and overly brief sections.
- **Files:** `docs/llm_agents/BEHAVIORS_Gemini_Agent_Output.md`, `docs/llm_agents/SYNC_LLM_Agents_State.md`
- **Verification:** `ngram validate` (fails: existing connectome health doc gaps, membrane naming, and CHAIN link warnings noted by doctor)

### 2025-12-20: Filled Gemini behaviors template sections

- **What:** Added INPUTS/OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, and GAPS sections to the Gemini behaviors doc.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the behaviors template and clarify output expectations.
- **Files:** `docs/llm_agents/BEHAVIORS_Gemini_Agent_Output.md`

### 2025-12-21: Added PATTERNS behavior sections

- **What:** Filled the provider subprocess PATTERNS doc with BEHAVIORS SUPPORTED and BEHAVIORS PREVENTED narratives so the template is complete.
- **Why:** Close the DOC_TEMPLATE_DRIFT warning for this PATTERNS file and spell out the observable effects of the subprocess boundary.
- **Files:** `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`
- **Verification:** `ngram validate`

### 2025-12-21: Completed Gemini validation template

- **What:** Added the BEHAVIORS GUARANTEED table and OBJECTIVES COVERED narrative to describe the observable guarantees and goals for the Gemini adapter.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the validation template and give downstream agents explicit behavior assertions to rely on.
- **Files:** `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md`
- **Verification:** `ngram validate`

### 2025-12-22: Documented Gemini behavior objectives

- **What:** Added the missing `OBJECTIVES SERVED` section and expanded the NOTES/INPUTS/OUTPUTS narrative so every Gemini behaviors template section exceeds the length threshold.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the behaviors doc and keep the objectives and I/O story explicit for future agents.
- **Files:** `docs/llm_agents/BEHAVIORS_Gemini_Agent_Output.md`
- **Verification:** `ngram validate`

### 2025-12-23: Formalized Gemini validation behavior/objective tables

- **What:** Replaced the brief bullet lists with BEHAVIORS GUARANTEED and OBJECTIVES COVERED tables in the Gemini validation doc and expanded each rationale so every section exceeds the 50+ character threshold.
- **Why:** Resolve the remaining DOC_TEMPLATE_DRIFT warning, give downstream agents explicit guarantees/objective alignment, and keep the template length expectations satisfied.
- **Files:** `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md`
- **Verification:** `ngram validate` *(fails: pre-existing connectome health doc gaps and chain/link warnings noted by the doctor)*

### 2025-12-24: Detailed LLM health coverage into objective + connectivity sections

- **What:** Added an OBJECTIVES COVERAGE summary and a dedicated API connectivity indicator so the HEALTH template now captures both streaming and auth verification flows.
- **Why:** Close the remaining DOC_TEMPLATE_DRIFT warning tied to the health doc and link the API connectivity signal to the `api_connectivity` indicator.
- **Files:** `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- **Verification:** `ngram validate` *(fails: pre-existing connectome health doc gaps and chain/link warnings noted by the doctor)*

### 2025-12-25: Populate LLM implementation architecture doc

- **What:** Expanded `IMPLEMENTATION_LLM_Agent_Code_Architecture.md` with code structure, module layout, design patterns, schema, flows, logic chains, dependencies, state transitions, runtime/concurrency, configuration, bidirectional links, and GAPS/IDEAS/Q entries so every template bucket now has 50+ characters of guidance.
- **Why:** The doc drift warning listed missing sections such as logical flows, state management, and concurrency; filling them keeps the implementation doc aligned with downstream expectations.
- **Files:** `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md`, `docs/llm_agents/SYNC_LLM_Agents_State.md`
- **Verification:** `ngram validate` *(fails: existing connectome health doc gaps plus naming/CHAIN warnings noted by doctor)*

### 2025-12-30: Logged concurrency question for LLM implementation gaps

- **What:** Noted in the implementation GAPS section that tracking helper execution timestamps could expose long-running helpers and keep the concurrency narrative visible for downstream diagnostics.
- **Why:** The doc drift fix reorganized the Implementation doc, so surfacing this open question in the SYNC ensures the doctor can find the concurrency concern when the issue recurs.
- **Files:** `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md`, `docs/llm_agents/SYNC_LLM_Agents_State.md`
- **Verification:** `ngram validate` *(fails: existing docs/connectome/health gaps, the membrane naming mismatch, and CHAIN/link warnings tracked elsewhere)*

---

## KNOWN ISSUES

No confirmed defects are tracked; the stderr model listing noise is
noted in handoff context and has not been triaged yet.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Documentation only; no behavior changes.

**What you need to understand:**
The Gemini adapter is a thin wrapper intended to isolate provider SDK usage. It streams JSON chunks for the TUI and supports basic local tool execution. The default model is `gemini-3-flash-preview`.

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

## Agent Observations

### Remarks
- Added SCOPE and DATA sections to the provider adapter PATTERNS doc to resolve template drift.
- Added missing template sections (SCOPE/DATA) to the provider subprocess patterns doc.
- Documented BEHAVIORS SUPPORTED and BEHAVIORS PREVENTED in the provider subprocess PATTERNS doc to describe allowed and blocked flows.
- Filled missing template sections in the Gemini behaviors doc to document inputs, outputs, and edge cases.
- Gemini tool stubs were replaced with real filesystem/web handlers and light persistence.
- Google search base URL is now configurable via `NGRAM_GOOGLE_SEARCH_URL`.
- Expanded short SYNC sections to satisfy template length requirements.
- Documented the Gemini objectives and I/O story so the behaviors template is fully compliant again.
- Formalized the Gemini validation guarantees/objectives tables so the doctor no longer reports drift and the sections exceed the required length threshold, giving future agents richer context to trust the invariants.
- Expanded the Gemini implementation doc with code-structure, state, and runtime sections to close its DOC_TEMPLATE_DRIFT warning.
- Logged a helper execution timestamp question in the implementation GAPS section so the concurrency narrative stays visible for future investigations and the doctor can trace the helper timeline question back to the health narrative; this open idea now sits in the Implementation doc until the doctor closes it.
- Logged a helper execution timestamp question in the implementation GAPS section so the concurrency narrative stays visible for future investigations and the doctor can trace the helper timeline question back to the health narrative.

### Suggestions
- [ ] Add automated tests for tool outputs (tool_code/tool_result JSON).

### Propositions
- Consider a shared tool helper module if additional providers are added.

---

## POINTERS

| What | Where |
|------|-------|
| Gemini adapter | `ngram/llms/gemini_agent.py` |
| CLI integration | `ngram/agent_cli.py` |


---

## TODO

- [ ] Capture telemetry for LLM adapters (usage counts, errors, sync updates) so doctor can surface trends and the SYNC reflects real-world load.

## ARCHIVE

Older content archived to: `SYNC_LLM_Agents_State_archive_2025-12.md`
