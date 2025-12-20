# SYNC: Project Health

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: ngram doctor
STATUS: CRITICAL
```

---

## CURRENT STATE

**Health Score:** 0/100

The project has critical issues that will significantly impact agent effectiveness. Address these before starting new work.

| Severity | Count |
|----------|-------|
| Critical | 7 |
| Warning | 52 |
| Info | 38 |

---

## ISSUES

### MONOLITH (1 files)

**What's wrong:** Large files are hard to navigate, test, and maintain. They slow down agents who need to load context, and changes become risky because side effects are hard to predict.

**How to fix:** Extract cohesive functionality into separate modules. Start with the largest functions/classes listed above.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `ngram/tui/app.py` - 829 lines (threshold: 800)
  - Split: class NgramApp() (915L, :42), async def _start_manager_with_overview() (192L, :239), async def on_mount() (69L, :125)

### UNDOCUMENTED (4 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `ngram` - No documentation mapping (47 files)
  - Add mapping to modules.yaml
- `ngram/llms` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `ngram/tui` - No documentation mapping (15 files)
  - Add mapping to modules.yaml
- `ngram/tui/widgets` - No documentation mapping (7 files)
  - Add mapping to modules.yaml

### PLACEHOLDER (1 files)

**What's wrong:** Template placeholders mean the documentation was started but never completed. Agents loading these docs get no useful information.

**How to fix:** Fill in the placeholders with actual content, or delete the file if it's not needed yet.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `.ngram/state/SYNC_Project_State.md` - Contains 1 template placeholder(s)
  - Fill in actual content

### BROKEN_IMPL_LINK (1 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_Overview.md` - References 2 non-existent file(s)
  - Update or remove references: ngram/state/SYNC_Project_Health.md, ngram/state/SYNC_Project_State.md

### INCOMPLETE_IMPL (2 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `ngram/doctor_files.py` - Contains 2 empty/incomplete function(s)
- `ngram/repair_core.py` - Contains 2 empty/incomplete function(s)

### LARGE_DOC_MODULE (1 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/cli` - Total 52K chars (threshold: 50K)

### DOC_TEMPLATE_DRIFT (42 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md` - Missing: SCOPE
- `docs/llm_agents/SYNC_LLM_Agents_State.md` - Too short: IN PROGRESS, KNOWN ISSUES
- `docs/llm_agents/BEHAVIORS_Gemini_Agent_Output.md` - Missing: INPUTS / OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, GAPS / IDEAS / QUESTIONS
- `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md` - Missing: PROPERTIES, ERROR CONDITIONS, TEST COVERAGE, VERIFICATION PROCEDURE, SYNC STATUS, GAPS / IDEAS / QUESTIONS
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md` - Missing: HOW TO USE THIS TEMPLATE, INDICATOR: {Indicator Name}
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - Missing: CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, DATA FLOW AND DOCKING (FLOW-BY-FLOW), LOGIC CHAINS, MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, BIDIRECTIONAL LINKS, GAPS / IDEAS / QUESTIONS
- `docs/llm_agents/ALGORITHM_Gemini_Stream_Flow.md` - Missing: DATA STRUCTURES, ALGORITHM: {Primary Function Name}, KEY DECISIONS, HELPER FUNCTIONS, INTERACTIONS
- `docs/cli/SYNC_CLI_State.md` - Missing: MATURITY, HANDOFF: FOR AGENTS, HANDOFF: FOR HUMAN, TODO, CONSCIOUSNESS TRACE, POINTERS; Too short: IN PROGRESS
- `docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md` - Missing: DATA FLOW AND DOCKING (FLOW-BY-FLOW), LOGIC CHAINS
- `docs/cli/PATTERNS_Why_CLI_Over_Copy.md` - Missing: SCOPE
- ... and 32 more

### NON_STANDARD_DOC_TYPE (1 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/map.md` - Doc filename does not use a standard prefix

### NAMING_CONVENTION (1 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/map.md` - Naming convention violations task (1): 6 items

### ESCALATION (4 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `templates/ngram/views/VIEW_Escalation_How_To_Handle_Vague_Tasks_Missing_Information_And_Complex_Non-Obvious_Problems.md` - Escalation marker needs decision
- `docs/cli/SYNC_CLI_State.md` - Escalation marker needs decision
- `docs/cli/BEHAVIORS_CLI_Command_Effects.md` - Escalation marker needs decision
- `.ngram/views/VIEW_Escalation_How_To_Handle_Vague_Tasks_Missing_Information_And_Complex_Non-Obvious_Problems.md` - Escalation marker needs decision

### HARDCODED_CONFIG (1 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `ngram/llms/gemini_agent.py` - Contains hardcoded configuration values

---

## LATER

These are minor issues that don't block work but would improve project health:

- [ ] `ngram/agent_cli.py` - No DOCS: reference in file header
- [ ] `ngram/doctor_types.py` - No DOCS: reference in file header
- [ ] `ngram/tui/styles/theme.tcss` - No DOCS: reference in file header
- [ ] `ngram/tui/styles/theme_light.tcss` - No DOCS: reference in file header
- [ ] `ngram/doctor_checks_naming.py` - Not referenced in any IMPLEMENTATION doc
- [ ] `docs/cli/ALGORITHM_CLI_Logic.md` - Doc not linked from code or modules.yaml
- [ ] `docs/cli/BEHAVIORS_CLI_Command_Effects.md` - Doc not linked from code or modules.yaml
- [ ] `docs/cli/HEALTH_CLI_Coverage.md` - Doc not linked from code or modules.yaml
- [ ] `docs/cli/SYNC_CLI_State.md` - Doc not linked from code or modules.yaml
- [ ] `docs/cli/SYNC_CLI_State_archive_2025-12.md` - Doc not linked from code or modules.yaml
- ... and 28 more

---

## HANDOFF

**For the next agent:**

Before starting your task, consider addressing critical issues - especially if your work touches affected files. Monoliths and undocumented code will slow you down.

**Recommended first action:** Pick one MONOLITH file you'll be working in and split its largest function into a separate module.

---

*Generated by `ngram doctor`*