# ngram Framework — Algorithm: Installation and Bootstrap

```
STATUS: STABLE
CREATED: 2024-12-15
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md
BEHAVIORS:       ../BEHAVIORS_Observable_Protocol_Effects.md
ALGORITHM:       ../ALGORITHM_Overview.md
THIS:            ./ALGORITHM_Installation_And_Bootstrap.md
VALIDATION:      ../VALIDATION_Protocol_Invariants.md
IMPLEMENTATION:  ../IMPLEMENTATION_Overview.md
TEST:            ../TEST_Protocol_Test_Cases.md
SYNC:            ../SYNC_Protocol_Current_State.md
```

---

## ALGORITHM: Install Protocol in Project

1. Copy templates into `.ngram/`.
   - Source: `templates/ngram/`
   - Target: `{project}/.ngram/`
2. Update bootstrap files.
   - Append `templates/CLAUDE_ADDITION.md` to `.ngram/CLAUDE.md` (create if missing).
   - Mirror the same content to root `AGENTS.md` and append `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`.
   - For manager role, write `.ngram/agents/manager/AGENTS.md` using `templates/ngram/agents/manager/CLAUDE.md` plus the Codex addition.
3. Initialize `.ngram/state/SYNC_Project_State.md` with current state.
4. (Optional) Create `docs/` and add module docs as needed.

---

## ALGORITHM: Agent Starts Task

1. Read bootstrap: `.ngram/CLAUDE.md` (or root `AGENTS.md`), then `.ngram/PROTOCOL.md`.
2. Identify task type and select the matching VIEW.
3. Read the VIEW and load required context (SYNC, module docs).
4. Execute work.
5. Update SYNC files and any affected docs.
