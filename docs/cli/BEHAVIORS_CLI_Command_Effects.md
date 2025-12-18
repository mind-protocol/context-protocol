# ADD Framework CLI — Behaviors: Command Effects and Observable Outcomes

```
STATUS: STABLE
CREATED: 2025-12-18
VERIFIED: 2025-12-18 against commit 6e0062c
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Why_CLI_Over_Copy.md
THIS:            BEHAVIORS_CLI_Command_Effects.md (you are here)
ALGORITHM:       ./ALGORITHM_CLI_Logic.md
VALIDATION:      ./VALIDATION_CLI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Code_Architecture.md
TEST:            ./TEST_CLI_Coverage.md
SYNC:            ./SYNC_CLI_State.md
```

---

## BEHAVIORS

### B1: Init Command

```
GIVEN:  A project directory without ADD Framework
WHEN:   `add-framework init` is executed
THEN:   .add-framework/ directory is created with protocol files
AND:    CLAUDE.md is created or updated with protocol bootstrap
AND:    modules.yaml template is copied to project root
```

### B2: Init with Force

```
GIVEN:  A project with existing .add-framework/
WHEN:   `add-framework init --force` is executed
THEN:   Existing .add-framework/ is removed
AND:    Fresh protocol files are copied
AND:    CLAUDE.md is updated (not duplicated)
```

### B3: Validate Command

```
GIVEN:  A project with ADD Framework installed
WHEN:   `add-framework validate` is executed
THEN:   8 validation checks are run
AND:    Results are printed with pass/fail for each check
AND:    Exit code is 0 if all pass, 1 if any fail
AND:    Fix guidance is printed for failures
```

### B4: Doctor Command

```
GIVEN:  A project with ADD Framework installed
WHEN:   `add-framework doctor` is executed
THEN:   12 health checks are run
AND:    Issues are grouped by severity (critical, warning, info)
AND:    Health score (0-100) is calculated
AND:    Results saved to .add-framework/state/SYNC_Project_Health.md
```

### B5: Repair Command

```
GIVEN:  A project with health issues from doctor
WHEN:   `add-framework repair` is executed
THEN:   Claude Code agents are spawned for each issue
AND:    Agents follow appropriate VIEW for each issue type
AND:    Progress is streamed to terminal
AND:    Report saved to .add-framework/state/REPAIR_REPORT.md
```

### B6: Context Command

```
GIVEN:  A source file path
WHEN:   `add-framework context <file>` is executed
THEN:   Dependency map is printed
AND:    Linked documentation chain is found
AND:    Full doc content is printed
AND:    Access is logged to traces
```

### B7: Sync Command

```
GIVEN:  A project with SYNC files
WHEN:   `add-framework sync` is executed
THEN:   SYNC file status is displayed
AND:    Large files (>200 lines) are auto-archived
```

### B8: Prompt Command

```
GIVEN:  A project with ADD Framework
WHEN:   `add-framework prompt` is executed
THEN:   Bootstrap prompt for LLM is printed to stdout
AND:    Contains PROJECT, SYNC, MODULES sections
```

---

## INPUTS / OUTPUTS

### Primary Function: `main()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| command | str | Subcommand name (init, validate, doctor, etc.) |
| --dir | Path | Target directory (default: cwd) |
| command-specific args | various | See each command |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| exit_code | int | 0 for success, 1 for failure |

**Side Effects:**

- Creates/modifies files in target directory
- Spawns subprocesses (repair command)
- Writes to stdout/stderr

---

## EDGE CASES

### E1: Protocol Not Installed

```
GIVEN:  validate/doctor run on project without .add-framework/
THEN:   Returns failure with clear message
AND:    Suggests running `add-framework init`
```

### E2: No Issues Found

```
GIVEN:  doctor run on healthy project
THEN:   Score is 100/100
AND:    No critical/warning issues listed
AND:    Exit code is 0
```

### E3: Empty Project

```
GIVEN:  init run on empty directory
THEN:   Protocol files are created
AND:    CLAUDE.md is created from scratch
```

### E4: Context for Non-Existent File

```
GIVEN:  context command with non-existent file path
THEN:   Returns failure
AND:    Suggests checking path
```

---

## ANTI-BEHAVIORS

What should NOT happen:

### A1: No Duplicate CLAUDE.md Content

```
GIVEN:   CLAUDE.md already has ADD Framework section
WHEN:    init is run
MUST NOT: Add duplicate protocol section
INSTEAD:  Skip update with message "already has ADD Framework section"
```

### A2: No Silent Failures

```
GIVEN:   Any command encounters an error
WHEN:    Processing fails
MUST NOT: Exit silently with code 0
INSTEAD:  Print error message and exit with code 1
```

### A3: No Destructive Init Without Force

```
GIVEN:   .add-framework/ already exists
WHEN:    init is run without --force
MUST NOT: Overwrite existing files
INSTEAD:  Exit with error suggesting --force
```

### A4: Repair Must Not Skip SYNC Update

```
GIVEN:   Repair agent completes a fix
WHEN:    Changes are made
MUST NOT: Skip SYNC file update
INSTEAD:  Agent must update relevant SYNC with what changed
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Should `init` offer interactive mode to customize what gets installed?
- [ ] Consider adding `add-framework status` combining doctor + sync
- IDEA: Watch mode for continuous health monitoring
- QUESTION: Should doctor auto-run before repair, or stay separate commands?
