# Narrator — Implementation: Code Architecture and Structure

```
STATUS: STABLE
CREATED: 2024-12-19
UPDATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
VALIDATION:      ./VALIDATION_Narrator.md
THIS:            IMPLEMENTATION_Narrator.md (you are here)
HEALTH:          ./HEALTH_Narrator.md
SYNC:            ./SYNC_Narrator.md

IMPL:            engine/infrastructure/orchestration/narrator.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
agents/narrator/
├── CLAUDE.md             # Core agent instructions (System Prompt)
├── .claude/              # Agent CLI state
└── ...
engine/infrastructure/orchestration/narrator.py  # Python entry point and prompt builder
engine/infrastructure/orchestration/agent_cli.py # CLI wrapper for agent invocation
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `agents/narrator/CLAUDE.md` | Authorial intelligence rules | N/A | ~400 | OK |
| `engine/infrastructure/orchestration/narrator.py` | Prompt construction and IO | `run_narrator` | ~300 | OK |
| `engine/infrastructure/orchestration/agent_cli.py` | Subprocess management | `run_agent` | ~200 | OK |

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Agent-as-a-Service with CLI integration.

**Why this pattern:** Decouples the authorial logic (prompt-driven) from the game engine (Python-driven). The CLI interface allows for thread persistence and easy testing.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Prompt Builder | `engine/infrastructure/orchestration/narrator.py` | Dynamically assembles context for the LLM. |
| Streaming | `tools/stream_dialogue.py` | Delivers incremental output to the frontend via SSE. |

---

## SCHEMA

### Narrator Output (JSON)

```yaml
NarratorOutput:
  required:
    - scene: object            # New scene tree or updates
    - time_elapsed: int        # Game minutes passed
  optional:
    - mutations: list          # Graph updates to apply
    - voice_lines: list        # Audio assets to trigger
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| Narrator Call | `engine/infrastructure/orchestration/narrator.py:50` | Orchestrator.process_action |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Scene Generation: Action → Narrator → Graph

This flow handles the transition from a player action to a newly authored scene, including any world-state changes (mutations).

```yaml
flow:
  name: scene_generation
  purpose: Author new story beats based on current graph state.
  scope: Action -> LLM -> Graph Mutations -> Scene Response
  steps:
    - id: step_1_context
      description: Orchestrator gathers graph context and world state.
      file: engine/infrastructure/orchestration/narrator.py
      function: build_prompt
      input: playthrough_id, player_action
      output: full_prompt_string
      trigger: run_narrator call
      side_effects: none
    - id: step_2_author
      description: Agent authors response using CLAUDE.md rules.
      file: agents/narrator/CLAUDE.md
      function: N/A (Agent Intelligence)
      input: prompt
      output: JSON payload
      trigger: subprocess call
      side_effects: none
    - id: step_3_apply
      description: Extract and apply graph mutations from output.
      file: engine/physics/graph/graph_ops.py
      function: apply_mutation
      input: mutation_list
      output: success_boolean
      trigger: engine/infrastructure/orchestration/narrator.py parsing
      side_effects: graph state changed
  docking_points:
    guidance:
      include_when: narrative intent becomes concrete data
    available:
      - id: narrator_input
        type: custom
        direction: input
        file: engine/infrastructure/orchestration/narrator.py
        function: run_narrator
        trigger: Orchestrator
        payload: PromptContext
        async_hook: optional
        needs: none
        notes: Context fed to the authorial intelligence
      - id: narrator_output
        type: custom
        direction: output
        file: engine/infrastructure/orchestration/narrator.py
        function: run_narrator
        trigger: return response
        payload: NarratorOutput
        async_hook: required
        needs: none
        notes: Raw output before filtering
    health_recommended:
      - dock_id: narrator_output
        reason: Verification of authorial coherence and schema adherence.
```

---

## LOGIC CHAINS

### LC1: Invention to Canon

**Purpose:** Ensure LLM inventions are persisted correctly.

```
Agent authored "fact"
  → engine/infrastructure/orchestration/narrator.py extracts mutations
    → graph_ops.py applies to FalkorDB
      → fact is now queryable by physics/other agents
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/orchestration/narrator.py
    ├── imports → engine/physics/graph
    └── imports → engine/moment_graph
```

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Thread History | `.claude/` | thread | per-playthrough session |

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Narrator CLI | Sync/Subprocess | Blocks worker thread during generation |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `AGENTS_MODEL` | env | `claude` | Model provider for narrator |

---

## RUNTIME BEHAVIOR

### Initialization

```
1. NarratorService instantiates with a working directory over the agents/narrator prompt bundle, sets the timeout, and flags that no session has started yet so CLI continuation only kicks in after the first call.
2. Logging, env reads (e.g., `AGENTS_MODEL`), and helper imports complete before the manager hands over the first scene context so the agent is ready when RunNarrator begins.
3. When the engine bootstraps, any CLI invocation or server endpoint that needs narration constructs NarratorService and acknowledges that the fallback path is available before attempting to stream text.
```

### Main Loop / Request Cycle

```
1. A caller (playthrough loop or manual CLI) invokes `NarratorService.generate`, supplying scene context, optional world injections, and any specific instruction string, which immediately triggers `_build_prompt` to serialize the data into the YAML-backed prompt.
2. `_call_claude` runs `run_agent` inside `agent_cli`, optionally continuing an existing session, enforces the JSON output contract, and falls back to the minimal scene when the subprocess fails, times out, or the response cannot be parsed.
3. Parsed outputs (scene tree, time_elapsed, optional mutations/seeds) are returned, while `NarratorService` keeps the `session_started` flag true so future calls will resume the ongoing session instead of restarting each time.
```

### Shutdown

```
1. When the playthrough ends or the CLI is told to stop, the orchestrator calls `NarratorService.reset_session` to drop the continuation flag and allow the next run to start fresh.
2. There is no background thread to tear down; simply resetting the flag and logging the reset is sufficient because the CLI is synchronous and short-lived per scene.
3. After reset, the next generate call rebuilds the prompt from scratch, reinitializes logging context if needed, and reuses the working directory path without lingering state.
```

---

## BIDIRECTIONAL LINKS

### Code → Docs

Files that reference this documentation:

| File | Line | Reference |
|------|------|-----------|
| `engine/infrastructure/orchestration/narrator.py` | 7 | `DOCS: docs/agents/narrator/IMPLEMENTATION_Narrator.md` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| DATA FLOW AND DOCKING (step 1: prompt build) | `engine/infrastructure/orchestration/narrator.py:build_prompt` |
| DATA FLOW AND DOCKING (step 2: agent call) | `engine/infrastructure/orchestration/narrator.py:_call_claude` |
| DATA FLOW AND DOCKING (step 3: mutation apply) | `engine/physics/graph/graph_ops.py:apply_mutation` |
| LOGIC CHAINS (Invention to Canon) | `engine/physics/graph/graph_ops.py:apply_mutation` |
| CONCURRENCY MODEL | `engine/infrastructure/orchestration/agent_cli.py:run_agent` |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

Files approaching WATCH/SPLIT status - identify what can be extracted:

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `engine/infrastructure/orchestration/narrator.py` | ~200L | <400L | n/a | Already lean; no extract candidate yet |

### Missing Implementation

- [ ] Capture narrator health metrics (prompt timing, CLI latency, JSON parsing success) and feed them into the existing health tooling so runtime regressions surface automatically.
- [ ] Document how the narrator fallback scene mutations should be reconciled into the world graph instead of silently returning empty mutation lists.

### Ideas

- IDEA: Surface a table-driven prompt template so new injection fields can be added without editing `_build_prompt`.
- IDEA: Extend NarratorService with an opt-in instrumentation hook that posts raw JSON responses to the health dashboard for easier debugging.

### Questions

- QUESTION: Should NarratorService expose a hook that validates mutation lists against the schema before returning, or is the downstream caller responsible for schema enforcement?
- QUESTION: When fallback scenes fire repeatedly, should the orchestrator halt play-throughs to block potential sandbox loops instead of returning minimal scenes forever?
