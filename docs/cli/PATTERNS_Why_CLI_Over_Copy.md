# ADD Framework CLI — Patterns: Why CLI Over Copy

```
STATUS: STABLE
CREATED: 2025-12-18
VERIFIED: 2025-12-18 against commit 1440b4c
```

---

## CHAIN

```
THIS:            PATTERNS_Why_CLI_Over_Copy.md (you are here)
BEHAVIORS:       ./BEHAVIORS_CLI_Command_Effects.md
ALGORITHM:       ./ALGORITHM_CLI_Logic.md
VALIDATION:      ./VALIDATION_CLI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Code_Architecture.md
TEST:            ./TEST_CLI_Coverage.md
SYNC:            ./SYNC_CLI_State.md
```

---

## THE PROBLEM

The ADD Framework is fundamentally just markdown files. You could copy them manually. So why have a CLI at all?

Without tooling:
- Version discovery is manual (which version of the protocol?)
- Updates require re-copying entire directories
- No way to check protocol health
- Repair operations require manual agent coordination
- Discoverability is poor (harder to remember git URL than `pip install`)

---

## THE PATTERN

**Minimal CLI wrapping file operations + automated health management.**

The CLI does NOT add complex logic. It provides:
1. **Installation** — Copy protocol files to target project
2. **Validation** — Check protocol invariants are satisfied
3. **Health Checks** — Identify documentation gaps, stale syncs, code monoliths
4. **Automated Repair** — Spawn Claude Code agents to fix issues
5. **Navigation** — Find docs from code paths, generate context

The protocol itself remains file-based. The CLI is orchestration, not logic.

---

## PRINCIPLES

### Principle 1: Files First, CLI Second

The protocol is markdown files. Period. An agent working on a project should be able to navigate and use the protocol by reading files directly.

The CLI exists for convenience: installation, updates, health checks. But everything the CLI does could be done manually with file operations.

This matters because:
- No vendor lock-in
- Protocol works even if CLI breaks
- Agents don't need the CLI to follow the protocol

### Principle 2: Modular Subcommands

Each CLI command lives in its own module:
- `init_cmd.py` — Initialize protocol in a project
- `validate.py` — Check protocol invariants
- `doctor.py` — Health checks and diagnostics
- `repair.py` — Spawn agents to fix issues
- `sync.py` — SYNC file management
- `context.py` — Code-to-docs navigation
- `prompt.py` — Generate LLM bootstrap prompts
- `project_map.py` — Visual project mapping
- `github.py` — GitHub integration

New commands can be added without touching existing ones. Each module is self-contained.

### Principle 3: Agent-Driven Repair

The `repair` command is the most sophisticated part of the CLI. It:
1. Runs `doctor` to identify issues
2. For each issue, builds a task-specific prompt
3. Spawns Claude Code subprocess with the prompt
4. Streams agent output in real-time
5. Tracks success/failure and generates report

This is not "AI magic" — it's structured task delegation. Each agent gets:
- Specific VIEW to follow
- Docs to read first
- Clear success criteria
- Instructions to update SYNC when done

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| subprocess | Spawn Claude Code agents for repair |
| yaml (optional) | Parse modules.yaml for module mappings |
| pathlib | File system operations throughout |
| argparse | CLI argument parsing |

---

## INSPIRATIONS

- **Git** — Subcommand pattern (`git status`, `git commit`, etc.)
- **npm/pip** — Package-based distribution for versioning
- **Terraform** — `init`, `validate`, `plan`, `apply` workflow
- **Claude Code itself** — Agent-as-subprocess pattern for repairs

---

## WHAT THIS DOES NOT SOLVE

- **Protocol design** — The CLI doesn't define what good documentation looks like
- **Project-specific customization** — config.yaml exists but is minimal
- **IDE integration** — This is CLI-only, no editor plugins
- **Multi-project orchestration** — Operates on one project at a time

---

## GAPS / IDEAS / QUESTIONS

- [ ] Consider adding `add-framework watch` for continuous health monitoring
- [ ] The `repair --parallel` flag is useful but output can be messy
- IDEA: MCP server integration for richer tool access during repairs
- QUESTION: Should `doctor` auto-run before `repair`, or stay separate?
