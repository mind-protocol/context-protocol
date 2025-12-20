# ngram Framework CLI — Behaviors: Command Effects and Observable Outcomes

```
STATUS: STABLE
CREATED: 2025-12-18
VERIFIED: 2025-12-18 against commit 6e0062c
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Why_CLI_Over_Copy.md
THIS:            BEHAVIORS_CLI_Command_Effects.md
ALGORITHM:       ./ALGORITHM_CLI_Command_Execution_Logic.md
VALIDATION:      ./VALIDATION_CLI_Instruction_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Code_Architecture.md
HEALTH:          ./HEALTH_CLI_Command_Test_Coverage.md
SYNC:            ./SYNC_CLI_Development_State.md
```

---

## BEHAVIORS

### B1: Init Command

```
GIVEN:  A project directory without ngram Framework
WHEN:   `ngram init` is executed
THEN:   .ngram/ directory is created with protocol files
AND:    .ngram/CLAUDE.md is created or updated with protocol bootstrap
AND:    AGENTS.md is created or updated with the bootstrap plus Codex guidance
AND:    modules.yaml template is copied to project root
AND:    Repository map is generated at map.md
```

### B2: Init with Force

```
GIVEN:  A project with existing .ngram/
WHEN:   `ngram init --force` is executed
THEN:   Existing .ngram/ is removed
AND:    Fresh protocol files are copied
AND:    .ngram/CLAUDE.md and AGENTS.md are updated (not duplicated)
AND:    If removal fails due to permissions, init falls back to a partial refresh with warnings
```

### B3: Validate Command

```
GIVEN:  A project with ngram Framework installed
WHEN:   `ngram validate` is executed
THEN:   8 validation checks are run
AND:    Results are printed with pass/fail for each check
AND:    Exit code is 0 if all pass, 1 if any fail
AND:    Fix guidance is printed for failures
```

### B4: Doctor Command

```
GIVEN:  A project with ngram Framework installed
WHEN:   `ngram doctor` is executed
THEN:   13 health checks are run
AND:    Issues are grouped by severity (critical, warning, info)
AND:    Health score (0-100) is calculated
AND:    Results saved to .ngram/state/SYNC_Project_Health.md
AND:    Exit code is 0 even when issues are found
AND:    GitHub issues are created only when `--github` is provided
```

### B5: Repair Command

```
GIVEN:  A project with health issues from doctor
WHEN:   `ngram repair` is executed
THEN:   Repair agents are spawned for each issue
AND:    `--agents {claude,codex,gemini}` selects the agent provider
AND:    Agents follow appropriate VIEW for each issue type
AND:    Progress is streamed to terminal
AND:    Report saved to .ngram/state/REPAIR_REPORT.md
```

### B6: Context Command

```
GIVEN:  A source file path
WHEN:   `ngram context <file>` is executed
THEN:   Dependency map is printed
AND:    Linked documentation chain is found
AND:    Full doc content is printed
AND:    Access is logged to traces
```

### B7: Sync Command

```
GIVEN:  A project with SYNC files
WHEN:   `ngram sync` is executed
THEN:   SYNC file status is displayed
AND:    Large files (>200 lines) are auto-archived
```

### B8: Prompt Command

```
GIVEN:  A project with ngram Framework
WHEN:   `ngram prompt` is executed
THEN:   Bootstrap prompt for LLM is printed to stdout
AND:    Contains PROJECT, SYNC, MODULES sections
```

### B9: Overview Command

```
GIVEN:  A project directory
WHEN:   `ngram overview` is executed
THEN:   File tree is generated (respecting .gitignore/.ngramignore)
AND:    Timestamp added (YYYY-MM-DD HH:MM format)
AND:    Character counts shown for files and directories
AND:    Bidirectional links extracted (code→docs via DOCS:, docs→code via refs)
AND:    Cross-folder doc refs extracted
AND:    Section headers extracted from markdown files
AND:    Function/class definitions extracted from code files
AND:    Local imports extracted (stdlib/npm filtered out)
AND:    Module dependencies from modules.yaml included
AND:    Main map is saved to map.{md|yaml|json} in project root
AND:    Copy of main map is saved to docs/map.{md|yaml|json} (if docs/ exists)
AND:    Specific maps (map_{folder}.md) are generated for core folders (src, app, backend, etc)
```

**Options:**
- `--dir, -d PATH` — Target directory (default: cwd)
- `--folder, -p NAME` — Subfolder to map only (relative to project root). If provided, only this map is generated in root.
- `--format, -f {md,yaml,json}` — Output format (default: md)

### B10: Solve Escalations Command

```
GIVEN:  A project with files containing `@ngram&#58;escalation` or `@ngram&#58;proposition` markers
WHEN:   `ngram solve-markers` is executed
THEN:   The CLI identifies all files containing these markers
AND:    The CLI prints a numbered list of these files in priority order
AND:    The CLI prompts the human to review and resolve them
```

### B11: Agents Command

```
GIVEN:  A project with ngram Framework
WHEN:   `ngram agents <agent_name>` is executed
THEN:   The specified agent is invoked with the given prompt and context
AND:    The agent's output is streamed to the terminal
```

**Agents:**
- `gemini`, `claude`, `codex` (provider options)

---

## NOTES

Inputs/outputs, edge cases, and anti-behaviors are captured in `docs/cli/VALIDATION_CLI_Invariants.md` and `docs/cli/ALGORITHM_CLI_Logic.md` to avoid duplication.
