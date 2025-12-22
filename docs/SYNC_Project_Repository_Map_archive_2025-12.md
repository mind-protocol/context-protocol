# Archived: SYNC_Project_Repository_Map.md

Archived on: 2025-12-20
Original file: SYNC_Project_Repository_Map.md

---

## TODO

### Doc/Impl Drift

<!-- @ngram:todo DOCS: Consider updating the overview generator to preserve or emit SYNC headers instead of manual edits. -->

### Tests to Run

```bash
ngram validate
```

### Immediate

<!-- @ngram:todo Decide whether this file should be regenerated now or after additional repairs land. -->

### Later

<!-- @ngram:todo Capture a lightweight diff summary when regenerating the map, if feasible. -->
<!-- @ngram:proposition Add a note in the generator output about the command used to produce the map. -->

---


## POINTERS

| What | Where |
|------|-------|
| Repository overview generator | `ngram/repo_overview.py` |
| Map output snapshot | `docs/SYNC_Project_Repository_Map.md` |
| Validation command | `ngram/validate.py` |

---

## MATURITY

This archive is **DEPRECATED**; it simply records the repository map snapshot produced on 2025-12-20 so readers can reference that timestamp without disturbing the live map file.

**Canonical (v1):**
- The December 20 map stats and references preserved in this document remain fixed, even as the rest of the repository evolves.

**Designing (v2):**
- None; any new work should target the current `docs/SYNC_Project_Repository_Map.md` and leave this archive untouched unless an explicit archival update is required.

---

## CURRENT STATE

The content below still reflects the 2025-12-20 generation run; no subsequent overview refreshes have been applied, so its file counts, directories, and section refs are historical. This document now serves purely as a timestamped archive of that run.

---

## IN PROGRESS

No work is currently in progress inside this archive; it is intentionally read-only to keep a reproducible trace and only sees edits when an explicit archival event is recorded. Updates belong in the live map until a deliberate archival refresh is scheduled.

---

## RECENT CHANGES

Captured minimal SYNC context for the archived map so the document meets template expectations while leaving the generated body untouched for posterity.

---

## KNOWN ISSUES

This snapshot will drift from the live repository as soon as new files land; please regenerate the current map via `ngram overview` before relying on its tree metadata for navigation. The tracked TODOs above flag when a refresh might be due.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Implement_Write_Or_Modify_Code.md`.

**Context:** This file is a historical snapshot; treat `docs/SYNC_Project_Repository_Map.md` as the active SYNC record and only revisit this archive when tracing older releases.

**Next steps:** Rerun `ngram overview` if you need a fresh tree, then update the live sync preface before generating a new archive entry.

**Watch out for:** The generator output will overwrite the tree body, so do not edit the map section directly unless you have rerun the overview with the desired state.

---

## HANDOFF: FOR HUMAN

**Executive summary:** This archive preserves the December 20, 2025 repository map snapshot and now includes a complete SYNC preface describing why it exists and how to interpret it while the generated body remains untouched.

**Decisions made:** Added the canonical SYNC sections instead of editing generated output so doctor checks pass while historical accuracy stays intact.

**Needs your input:** Confirm whether future archive runs should follow the same preface pattern or if the generator should emit these sections automatically.

**Concern:** If the overview generator changes format, this archive may need manual cleanup before being reused as a trusted reference.

---

## CONSCIOUSNESS TRACE

Maintaining this archive required balancing minimal manual narration with the need to satisfy template drift checks; the new sections explain the scope, maturity, known gaps, and handoffs without touching the generated body.

I am confident this preserves the historical snapshot while giving future agents context, though the uncertainty remains whether the generator should automate SYNC prefaces to avoid future drift.

---

---

# Repository Map: 

*Generated: 2025-12-20 01:48*

- **Files:** 99
- **Directories:** 25
- **Total Size:** 847.4K
- **Doc Files:** 73
- **Code Files:** 22
- **Areas:** 4 (docs/ subfolders)
- **Modules:** 6 (subfolders in areas)
- **DOCS Links:** 21 (0.95 avg per code file)

- markdown: 73
- python: 22

```
├── docs/ (270.2K)
│   ├── cli/ (53.1K)
│   │   ├── ALGORITHM_CLI_Logic.md (8.7K)
│   │   ├── BEHAVIORS_CLI_Command_Effects.md (4.8K)
│   │   ├── HEALTH_CLI_Coverage.md (6.2K)
│   │   ├── IMPLEMENTATION_CLI_Code_Architecture.md (15.8K)
│   │   ├── PATTERNS_Why_CLI_Over_Copy.md (4.7K)
│   │   ├── SYNC_CLI_State.md (6.4K)
│   │   ├── SYNC_CLI_State_archive_2025-12.md (1.3K)
│   │   └── VALIDATION_CLI_Invariants.md (5.2K)
│   ├── llm_agents/ (23.6K)
│   │   ├── ALGORITHM_Gemini_Stream_Flow.md (2.7K)
│   │   ├── BEHAVIORS_Gemini_Agent_Output.md (2.0K)
│   │   ├── HEALTH_LLM_Agent_Coverage.md (4.9K)
│   │   ├── IMPLEMENTATION_LLM_Agent_Code_Architecture.md (1.9K)
│   │   ├── PATTERNS_Provider_Specific_LLM_Subprocesses.md (3.7K)
│   │   ├── SYNC_LLM_Agents_State.md (6.4K)
│   │   └── VALIDATION_Gemini_Agent_Invariants.md (2.1K)
│   ├── protocol/ (91.9K)
│   │   ├── ALGORITHM/ (2.5K)
│   │   │   └── ALGORITHM_Overview.md (2.5K)
│   │   ├── IMPLEMENTATION/ (5.4K)
│   │   │   └── IMPLEMENTATION_Overview.md (5.4K)
│   │   ├── archive/ (839)
│   │   │   └── SYNC_archive_2024-12.md (839)
│   │   ├── features/ (53.8K)
│   │   │   ├── doctor/ (44.5K)
│   │   │   │   ├── ALGORITHM_Project_Health_Doctor.md (17.1K)
│   │   │   │   ├── BEHAVIORS_Project_Health_Doctor.md (8.7K)
│   │   │   │   ├── HEALTH_Project_Health_Doctor.md (5.0K)
│   │   │   │   ├── PATTERNS_Project_Health_Doctor.md (4.0K)
│   │   │   │   ├── SYNC_Project_Health_Doctor.md (4.6K)
│   │   │   │   └── VALIDATION_Project_Health_Doctor.md (5.2K)
│   │   │   ├── BEHAVIORS_Agent_Trace_Logging.md (3.7K)
│   │   │   ├── PATTERNS_Agent_Trace_Logging.md (3.6K)
│   │   │   └── SYNC_Agent_Trace_Logging.md (2.0K)
│   │   ├── ALGORITHM_Overview.md (554)
│   │   ├── BEHAVIORS_Observable_Protocol_Effects.md (6.4K)
│   │   ├── HEALTH_Protocol_Verification.md (5.0K)
│   │   ├── IMPLEMENTATION_Overview.md (726)
│   │   ├── PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md (4.8K)
│   │   ├── SYNC_Protocol_Current_State.md (6.2K)
│   │   └── VALIDATION_Protocol_Invariants.md (5.7K)
│   ├── tui/ (52.1K)
│   │   ├── IMPLEMENTATION_TUI_Code_Architecture/ (9.3K)
│   │   │   └── IMPLEMENTATION_TUI_Code_Architecture_Structure.md (9.3K)
│   │   ├── archive/ (4.1K)
│   │   │   ├── IMPLEMENTATION_archive_2024-12.md (2.5K)
│   │   │   └── SYNC_archive_2024-12.md (1.7K)
│   │   ├── ALGORITHM_TUI_Flow.md (6.2K)
│   │   ├── BEHAVIORS_TUI_Interactions.md (6.6K)
│   │   ├── HEALTH_TUI_Coverage.md (6.1K)
│   │   ├── IMPLEMENTATION_TUI_Code_Architecture.md (2.0K)
│   │   ├── PATTERNS_TUI_Design.md (4.5K)
│   │   ├── SYNC_TUI_State.md (5.1K)
│   │   ├── SYNC_TUI_State_archive_2025-12.md (3.6K)
│   │   └── VALIDATION_TUI_Invariants.md (4.7K)
│   └── map.md (49.5K)
├── ngram/ (609.2K)
│   ├── llms/ (10.7K)
│   │   └── gemini_agent.py (10.7K) →
│   ├── tui/ (168.3K)
│   │   ├── styles/ (18.7K)
│   │   │   ├── theme.tcss (9.2K)
│   │   │   └── theme_light.tcss (9.6K)
│   │   ├── widgets/ (44.5K)
│   │   │   ├── agent_container.py (10.5K) →
│   │   │   ├── agent_panel.py (9.5K) →
│   │   │   ├── input_bar.py (7.9K) →
│   │   │   ├── manager_panel.py (8.0K) →
│   │   │   ├── status_bar.py (7.0K) →
│   │   │   ├── suggestions.py (1.2K) →
│   │   │   └── (..1 more files)
│   │   ├── app.py (40.7K) →
│   │   ├── commands.py (29.2K) →
│   │   ├── commands_agent.py (18.4K) →
│   │   ├── manager.py (9.9K) →
│   │   ├── state.py (6.6K) →
│   │   └── (..1 more files)
│   ├── doctor_checks.py (25.8K) →
│   ├── doctor_checks_content.py (20.7K) →
│   ├── doctor_files.py (22.1K) →
│   ├── doctor_report.py (21.4K)
│   ├── repair.py (30.1K) →
│   ├── repair_core.py (27.7K) →
│   ├── repair_instructions.py (27.6K) →
│   ├── repair_instructions_docs.py (18.6K) →
│   ├── repo_overview.py (26.4K) →
│   ├── validate.py (28.3K) →
│   └── (..21 more files)
├── templates/ (132.5K)
│   ├── ngram/ (126.7K)
│   │   ├── agents/ (2.8K)
│   │   │   └── manager/ (2.8K)
│   │   │       └── CLAUDE.md (2.8K)
│   │   ├── state/ (2.1K)
│   │   │   └── SYNC_Project_State.md (2.1K)
│   │   ├── templates/ (38.0K)
│   │   │   ├── ALGORITHM_TEMPLATE.md (2.3K)
│   │   │   ├── BEHAVIORS_TEMPLATE.md (2.1K)
│   │   │   ├── CONCEPT_TEMPLATE.md (1.1K)
│   │   │   ├── HEALTH_TEMPLATE.md (13.8K)
│   │   │   ├── IMPLEMENTATION_TEMPLATE.md (8.7K)
│   │   │   ├── PATTERNS_TEMPLATE.md (2.4K)
│   │   │   ├── SYNC_TEMPLATE.md (3.1K)
│   │   │   ├── TOUCHES_TEMPLATE.md (1.6K)
│   │   │   └── VALIDATION_TEMPLATE.md (2.9K)
│   │   ├── views/ (64.7K)
│   │   │   ├── VIEW_Analyze_Structural_Analysis.md (4.1K)
│   │   │   ├── VIEW_Debug_Investigate_And_Fix_Issues.md (3.7K)
│   │   │   ├── VIEW_Document_Create_Module_Documentation.md (6.1K)
│   │   │   ├── VIEW_Escalation_How_To_Handle_Vague_Tasks_Missing_Information_And_Complex_Non-Obvious_Problems.md (10.5K)
│   │   │   ├── VIEW_Extend_Add_Features_To_Existing.md (4.9K)
│   │   │   ├── VIEW_Health_Define_Health_Checks_And_Verify.md (5.9K)
│   │   │   ├── VIEW_Implement_Write_Or_Modify_Code.md (4.6K)
│   │   │   ├── VIEW_Ingest_Process_Raw_Data_Sources.md (4.5K)
│   │   │   ├── VIEW_Onboard_Understand_Existing_Codebase.md (5.0K)
│   │   │   ├── VIEW_Refactor_Improve_Code_Structure.md (5.1K)
│   │   │   └── (..18 more files)
│   │   ├── PRINCIPLES.md (8.2K)
│   │   └── PROTOCOL.md (10.8K)
│   ├── CODEX_SYSTEM_PROMPT_ADDITION.md (2.1K)
│   ├── GEMINI_SYSTEM_PROMPT_ADDITION.md (2.4K)
│   ├── ngramignore (806)
│   └── (..1 more files)
├── .ngramignore (806)
├── AGENTS.md (23.5K)
└── README.md (4.5K)
```

**Sections:**
- # ngram Framework CLI — Algorithm: Command Processing Logic
- ## CHAIN
- ## OVERVIEW
- ## ALGORITHM: Init Command
- ## DATA STRUCTURES
- ## ALGORITHM: Validate Command
- ## ALGORITHM: Doctor Command
- ## ALGORITHM: Solve Special Markers Command
- ## ALGORITHM: Repair Command
- # AGENTS.md = .ngram/CLAUDE.md + templates/CODEX_SYSTEM_PROMPT_ADDITION.md
- ## KEY DECISIONS
- # Safe fixes that only touch references
- # Also create/update documentation content
- # Also make code changes
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Doc refs:**
- `docs/cli/ALGORITHM_CLI_Logic.md`
- `docs/cli/VALIDATION_CLI_Invariants.md`

**Sections:**
- # ngram Framework CLI — Behaviors: Command Effects and Observable Outcomes
- ## CHAIN
- ## BEHAVIORS
- ## NOTES

**Code refs:**
- `ngram/validate.py`

**Doc refs:**
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- `docs/tui/HEALTH_TUI_Coverage.md`

**Sections:**
- # ngram Framework CLI — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: Init Integrity
- ## HOW TO RUN
- # Run all health checks via validate
- # Run project health via doctor
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/doctor.py`
- `ngram/doctor_checks.py`
- `ngram/doctor_checks_content.py`
- `ngram/doctor_checks_docs.py`
- `ngram/doctor_checks_quality.py`
- `ngram/doctor_checks_sync.py`
- `ngram/doctor_files.py`
- `ngram/doctor_report.py`
- `ngram/doctor_types.py`
- `ngram/github.py`
- `ngram/init_cmd.py`
- `ngram/project_map.py`
- `ngram/project_map_html.py`
- `ngram/prompt.py`
- `ngram/repair.py`
- `ngram/repair_core.py`
- `ngram/repair_escalation_interactive.py`
- `ngram/repair_instructions.py`
- `ngram/repair_instructions_docs.py`
- `ngram/repair_report.py`
- `ngram/repo_overview.py`
- `ngram/repo_overview_formatters.py`
- `ngram/solve_escalations.py`
- `ngram/sync.py`
- `ngram/utils.py`
- `ngram/validate.py`

**Doc refs:**
- `docs/cli/ALGORITHM_CLI_Logic.md`
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`

**Sections:**
- # ngram Framework CLI — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Code refs:**
- `agent_cli.py`
- `context.py`
- `doctor.py`
- `github.py`
- `init_cmd.py`
- `project_map.py`
- `prompt.py`
- `repair.py`
- `sync.py`
- `validate.py`

**Doc refs:**
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`

**Sections:**
- # ngram Framework CLI — Patterns: Why CLI Over Copy
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## MARKERS

**Code refs:**
- `doctor_files.py`
- `ngram.py`
- `ngram/project_map_html.py`
- `ngram/repair_core.py`
- `ngram/solve_escalations.py`
- `project_map_html.py`
- `repo_overview.py`

**Doc refs:**
- `docs/cli/ALGORITHM_CLI_Logic.md`
- `docs/cli/SYNC_CLI_State.md`

**Sections:**
- # ngram Framework CLI — Sync: Current State
- ## CHAIN
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## CONFLICTS
- ## HANDOFF
- ## Agent Observations
- ## ARCHIVE

**Code refs:**
- `ngram/doctor_checks.py`

**Sections:**
- # Archived: SYNC_CLI_State.md
- ## MATURITY
- ## RECENT CHANGES (ARCHIVED)
- ## NOTES

**Sections:**
- # ngram Framework CLI — Validation: Invariants and Correctness Checks
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Run CLI commands manually for now
- # No automated test suite yet
- # TODO: Add pytest tests
- ## CHECK REFERENCES
- ## MARKERS

**Sections:**
- # ngram LLM Agents — Algorithm: Gemini Stream Flow
- ## CHAIN
- ## OVERVIEW
- ## ALGORITHM: Gemini Adapter Execution
- ## DATA FLOW
- ## COMPLEXITY
- ## MARKERS

**Sections:**
- # ngram LLM Agents — Behaviors: Gemini Agent Output
- ## CHAIN
- ## BEHAVIORS
- ## NOTES

**Code refs:**
- `gemini_agent.py`
- `ngram/llms/gemini_agent.py`

**Doc refs:**
- `docs/cli/HEALTH_CLI_Coverage.md`

**Sections:**
- # ngram LLM Agents — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: Stream Validity
- ## HOW TO RUN
- # Manual verification of stream JSON
- # Manual verification of plain text
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `ngram/agent_cli.py`
- `ngram/llms/gemini_agent.py`

**Sections:**
- # ngram LLM Agents — Implementation: Code Architecture
- ## CHAIN
- ## MODULE LAYOUT
- ## ENTRY POINTS
- ## KEY FUNCTIONS
- ## DATA FLOW
- ## EXTERNAL DEPENDENCIES
- ## CONFIGURATION
- ## INTEGRATION POINTS

**Code refs:**
- `agent_cli.py`
- `ngram/llms/gemini_agent.py`

**Sections:**
- # ngram LLM Agents — Patterns: Provider-Specific LLM Subprocesses
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## MARKERS

**Code refs:**
- `gemini_agent.py`
- `ngram/agent_cli.py`
- `ngram/llms/gemini_agent.py`

**Doc refs:**
- `docs/llm_agents/ALGORITHM_Gemini_Stream_Flow.md`
- `docs/llm_agents/BEHAVIORS_Gemini_Agent_Output.md`
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md`
- `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`
- `docs/llm_agents/SYNC_LLM_Agents_State.md`
- `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md`

**Sections:**
- # LLM Agents — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- # No module-specific tests documented yet.
- ## CONSCIOUSNESS TRACE
- ## Agent Observations
- ## POINTERS

**Sections:**
- # ngram LLM Agents — Validation: Gemini Agent Invariants
- ## CHAIN
- ## INVARIANTS
- ## EDGE CASES
- ## VERIFICATION METHODS
- ## FAILURE MODES

**Doc refs:**
- `templates/CLAUDE_ADDITION.md`
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`
- `templates/ngram/agents/manager/CLAUDE.md`

**Sections:**
- # ngram Framework — Algorithm: Overview
- ## CHAIN
- ## OVERVIEW
- ## CONTENTS
- ## ALGORITHM: Install Protocol in Project
- ## ALGORITHM: Agent Starts Task
- ## ALGORITHM: Create New Module
- ## ALGORITHM: Modify Existing Module
- ## ALGORITHM: Document Cross-Cutting Concept
- ## NOTES

**Doc refs:**
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`

**Sections:**
- # ngram Framework — Implementation: Overview
- ## CHAIN
- ## OVERVIEW
- ## FILE STRUCTURE
- ## SCHEMAS AND CONFIG
- ## FLOWS AND LINKS
- # DOCS: docs/{area}/{module}/PATTERNS_*.md

**Sections:**
- # Archived: Protocol SYNC Notes (2024-12)
- ## SUMMARY OF 2024-12 CHANGES
- ## ARCHIVED NOTES

**Sections:**
- # ALGORITHM: Project Health Doctor
- ## MAIN FLOW
- ## 1. LOAD CONFIGURATION
- ## 2. DISCOVER PROJECT STRUCTURE
- # Also find subdirectories
- ## 3. RUN CHECKS
- # Check if mapped in modules.yaml
- # Check for template placeholders
- # Look for DOCS: comment
- # Find most recent SYNC update across all SYNC files
- # 1. Folders must be snake_case
- # 2. Code files must be snake_case.py
- # 3. Doc files must be PREFIX_PascalCase_With_Underscores.md
- # Group into tasks of 10
- # Skip if no docs at all (that's UNDOCUMENTED, not ABANDONED)
- # Check if only has PATTERNS or SYNC (started but not continued)
- # Started (has 1-2 docs) but incomplete (missing 3+ docs)
- # Check if stale
- # Check directories
- # Check files
- ## 4. AGGREGATE RESULTS
- # Apply severity overrides
- # Group by severity
- ## 5. CALCULATE SCORE
- ## 6. GENERATE OUTPUT
- ## 7. EXIT CODE
- ## CHAIN

**Sections:**
- # BEHAVIORS: Project Health Doctor
- ## COMMAND INTERFACE
- # Basic health check
- # With specific directory
- # Output formats
- # Filter by severity
- # Specific checks
- ## HEALTH CHECKS
- ## SPECIAL MARKERS
- ## OUTPUT BEHAVIOR
- ## Critical (2 issues)
- ## Warnings (3 issues)
- ## Info (3 issues)
- ## Suggested Actions
- ## GUIDED REMEDIATION
- ## Current State
- ## Recommended Steps
- # DOCS: docs/api/PATTERNS_Api_Design.md
- ## Template Commands
- # Generate PATTERNS from template
- ## Reference
- ## EXIT CODES
- ## CONFIGURATION
- # Thresholds
- # Ignore patterns
- # Disable specific checks
- # Custom severity overrides
- ## FALSE POSITIVE SUPPRESSION
- ## DOC TEMPLATE DRIFT DEFERMENTS
- ## NON-STANDARD DOC TYPE DEFERMENTS
- ## RESOLVED ESCALATION MARKERS
- ## CHAIN

**Code refs:**
- `doctor_checks.py`
- `doctor_report.py`
- `ngram/doctor.py`

**Doc refs:**
- `docs/tui/HEALTH_TUI_Coverage.md`

**Sections:**
- # Project Health Doctor — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: Score Sanity
- ## HOW TO RUN
- # Run all doctor checks on the current project
- # Run with JSON output for machine parsing
- ## KNOWN GAPS
- ## MARKERS

**Sections:**
- # PATTERNS: Project Health Doctor
- ## THE PROBLEM
- ## THE INSIGHT
- ## DESIGN DECISIONS
- ## WHAT WE CHECK
- ## WHAT WE DON'T CHECK
- ## ALTERNATIVES CONSIDERED
- ## CHAIN

**Code refs:**
- `doctor.py`

**Sections:**
- # SYNC: Project Health Doctor
- ## MATURITY
- ## CURRENT STATE
- ## IMPLEMENTATION ORDER
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CHAIN

**Sections:**
- # VALIDATION: Project Health Doctor
- ## INVARIANTS
- ## CHECK CORRECTNESS
- ## OUTPUT FORMAT CORRECTNESS
- ## EDGE CASES
- ## PERFORMANCE BOUNDS
- ## VERIFICATION COMMANDS
- # Verify determinism
- # Verify exit codes
- # Verify JSON validity
- # Verify ignore patterns
- ## CHAIN

**Sections:**
- # Agent Trace Logging — Behaviors: Observable Effects
- ## CHAIN
- ## COMMANDS
- ## AUTOMATIC TRACING
- ## TRACE FILE FORMAT
- ## INTEGRATION POINTS
- ## Usage (auto-generated)
- ## WHAT GETS TRACED
- ## WHAT DOESN'T GET TRACED

**Sections:**
- # Agent Trace Logging — Patterns: Why This Design
- ## CHAIN
- ## THE PROBLEM
- ## THE INSIGHT
- ## DESIGN DECISIONS
- ## WHAT THIS ENABLES
- ## TRADEOFFS
- ## ALTERNATIVES CONSIDERED
- ## OPEN QUESTIONS

**Code refs:**
- `ngram/cli.py`

**Sections:**
- # Agent Trace Logging — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IMPLEMENTATION PLAN
- ## HANDOFF: FOR AGENTS
- ## TODO
- ## OPEN QUESTIONS

**Sections:**
- # ngram Framework — Algorithm: Overview
- ## CHAIN
- ## ENTRY POINT

**Sections:**
- # ngram Framework — Behaviors: Observable Protocol Effects
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Code refs:**
- `ngram/validate.py`

**Doc refs:**
- `docs/cli/HEALTH_CLI_Coverage.md`

**Sections:**
- # ngram Framework — Health: Protocol Verification and Mechanics
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: Chain Completeness
- ## HOW TO RUN
- # Verify protocol health for the current project
- # Verify a specific module
- ## KNOWN GAPS
- ## MARKERS

**Doc refs:**
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_Overview.md`

**Sections:**
- # ngram Framework — Implementation: Overview
- ## CHAIN
- ## ENTRY POINT

**Sections:**
- # ngram Framework — Patterns: Bidirectional Documentation Chain for AI Agent Workflows
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- # Descriptive names
- # Not
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## MARKERS

**Code refs:**
- `ngram/cli.py`

**Doc refs:**
- `archive/SYNC_archive_2024-12.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_File_Structure.md`
- `templates/CLAUDE_ADDITION.md`
- `templates/ngram/PRINCIPLES.md`
- `templates/ngram/PROTOCOL.md`

**Sections:**
- # ngram Framework — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## STRUCTURE
- ## POINTERS
- ## ARCHIVE
- ## Agent Observations

**Code refs:**
- `scripts/check_chain_links.py`
- `scripts/check_doc_completeness.py`
- `scripts/check_doc_refs.py`
- `scripts/check_orphans.py`

**Sections:**
- # ngram Framework — Validation: Protocol Invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Check all invariants
- # Check specific invariant
- # Check specific module
- ## SYNC STATUS
- ## MARKERS

**Code refs:**
- `ngram/cli.py`
- `ngram/doctor.py`
- `ngram/repair_core.py`
- `ngram/tui/app.py`
- `ngram/tui/commands.py`
- `ngram/tui/commands_agent.py`
- `ngram/tui/manager.py`
- `ngram/tui/state.py`
- `ngram/tui/widgets/agent_container.py`
- `ngram/tui/widgets/agent_panel.py`
- `ngram/tui/widgets/input_bar.py`
- `ngram/tui/widgets/manager_panel.py`
- `ngram/tui/widgets/status_bar.py`
- `ngram/tui/widgets/suggestions.py`

**Doc refs:**
- `docs/tui/PATTERNS_TUI_Design.md`

**Sections:**
- # ngram TUI — Implementation Details: Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## BOUNDARIES
- ## SCHEMA
- ## MODULE DEPENDENCIES
- ## CONFIGURATION
- ## DATA FLOW
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## BIDIRECTIONAL LINKS

**Code refs:**
- `ngram/cli.py`
- `ngram/repair_core.py`
- `ngram/tui/app.py`
- `ngram/tui/commands.py`
- `ngram/tui/state.py`

**Sections:**
- # Archive: TUI Implementation Details (2024-12)
- ## Design Patterns (Historical Detail)
- ## Runtime Behavior (Historical Detail)
- ## Concurrency Model (Historical Detail)
- ## Configuration (Historical Detail)
- ## Bidirectional Links (Historical Detail)
- ## Remaining Work (Historical Detail)
- ## Decisions Made (Historical Detail)

**Code refs:**
- `app.py`
- `commands.py`
- `state.py`

**Doc refs:**
- `docs/tui/SYNC_TUI_State.md`

**Sections:**
- # Archived: SYNC_TUI_State.md (Condensed)
- ## Completed Features (Condensed)
- ## Planned Features (Condensed)
- ## Known Gaps
- ## Known Issues (Historical)
- ## Handoff Notes (Historical)
- ## Agent Observations (Historical)

**Code refs:**
- `doctor.py`
- `repair_core.py`

**Sections:**
- # ngram TUI — Algorithm: Application Flow and Event Handling
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: Main Event Loop
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Sections:**
- # ngram TUI — Behaviors: User Interactions and Observable Effects
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Code refs:**
- `manager.py`
- `ngram/tui/app.py`

**Doc refs:**
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`

**Sections:**
- # ngram TUI — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: Input Responsiveness
- ## HOW TO RUN
- # Manual verification of slash commands
- # Type /help, /doctor, /repair in the TUI input bar.
- # Manual verification of agent panels
- # Run /repair and verify that agent panels appear and stream output.
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `ngram/cli.py`
- `ngram/repair_core.py`
- `ngram/tui/commands.py`
- `ngram/tui/commands_agent.py`

**Doc refs:**
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md`

**Sections:**
- # ngram TUI — Implementation: Code Architecture (Overview)
- ## CHAIN
- ## SUMMARY
- ## QUICK STRUCTURE (Top-Level)
- ## ENTRY POINTS
- ## WHAT TO READ NEXT
- ## REMAINING WORK
- ## DECISIONS MADE

**Code refs:**
- `repair_core.py`

**Sections:**
- # ngram TUI — Patterns: Agent CLI-Style Interface
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## MARKERS

**Code refs:**
- `ngram/repair_core.py`
- `ngram/tui/app.py`
- `ngram/tui/commands.py`
- `ngram/tui/state.py`
- `ngram/tui/widgets/status_bar.py`

**Doc refs:**
- `docs/tui/PATTERNS_TUI_Design.md`
- `docs/tui/archive/SYNC_archive_2024-12.md`

**Sections:**
- # ngram TUI — Sync: Current State
- ## CHAIN
- ## CURRENT STATE
- ## IN PROGRESS
- ## PLANNED FEATURES (HIGH LEVEL)
- ## KNOWN GAPS
- ## AGENT OBSERVATIONS

**Code refs:**
- `repair.py`
- `repair_core.py`

**Sections:**
- # Archived: SYNC_TUI_State.md
- ## DESIGN DECISIONS
- ## FILE STRUCTURE (Planned)

**Sections:**
- # ngram TUI — Validation: Invariants and Verification
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Once tests exist:
- # With coverage:
- ## SYNC STATUS
- ## MARKERS

**Code refs:**
- `agent_cli.py`
- `app.py`
- `commands.py`
- `context.py`
- `doctor.py`
- `doctor_checks.py`
- `doctor_files.py`
- `doctor_report.py`
- `file_utils.py`
- `gemini_agent.py`
- `github.py`
- `init_cmd.py`
- `manager.py`
- `ngram.py`
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/doctor.py`
- `ngram/doctor_checks.py`
- `ngram/doctor_checks_content.py`
- `ngram/doctor_checks_docs.py`
- `ngram/doctor_checks_quality.py`
- `ngram/doctor_checks_sync.py`
- `ngram/doctor_files.py`
- `ngram/doctor_report.py`
- `ngram/doctor_types.py`
- `ngram/github.py`
- `ngram/init_cmd.py`
- `ngram/llms/gemini_agent.py`
- `ngram/project_map.py`
- `ngram/project_map_html.py`
- `ngram/prompt.py`
- `ngram/repair.py`
- `ngram/repair_core.py`
- `ngram/repair_escalation_interactive.py`
- `ngram/repair_instructions.py`
- `ngram/repair_instructions_docs.py`
- `ngram/repair_report.py`
- `ngram/repo_overview.py`
- `ngram/repo_overview_formatters.py`
- `ngram/solve_escalations.py`
- `ngram/sync.py`
- `ngram/tui/app.py`
- `ngram/tui/commands.py`
- `ngram/tui/commands_agent.py`
- `ngram/tui/manager.py`
- `ngram/tui/state.py`
- `ngram/tui/widgets/agent_container.py`
- `ngram/tui/widgets/agent_panel.py`
- `ngram/tui/widgets/input_bar.py`
- `ngram/tui/widgets/manager_panel.py`
- `ngram/tui/widgets/status_bar.py`
- `ngram/tui/widgets/suggestions.py`
- `ngram/utils.py`
- `ngram/utils/file_utils.py`
- `ngram/utils/string_utils.py`
- `ngram/utils/validation_utils.py`
- `ngram/validate.py`
- `project_map.py`
- `project_map_html.py`
- `prompt.py`
- `repair.py`
- `repair_core.py`
- `repo_overview.py`
- `scripts/check_chain_links.py`
- `scripts/check_doc_completeness.py`
- `scripts/check_doc_refs.py`
- `scripts/check_orphans.py`
- `src/analytics/batch_ingest.py`
- `src/analytics/storage/event_store.py`
- `src/analytics/stream_ingest.py`
- `src/analytics/validation/schema_rules.py`
- `src/dashboard/op_metrics.py`
- `src/dashboard/product_metrics.py`
- `state.py`
- `string_utils.py`
- `sync.py`
- `utils.py`
- `validate.py`

**Doc refs:**
- `archive/SYNC_archive_2024-12.md`
- `docs/cli/ALGORITHM_CLI_Logic.md`
- `docs/cli/HEALTH_CLI_Coverage.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture.md`
- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`
- `docs/cli/SYNC_CLI_State.md`
- `docs/cli/VALIDATION_CLI_Invariants.md`
- `docs/llm_agents/ALGORITHM_Gemini_Stream_Flow.md`
- `docs/llm_agents/BEHAVIORS_Gemini_Agent_Output.md`
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md`
- `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`
- `docs/llm_agents/SYNC_LLM_Agents_State.md`
- `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_File_Structure.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_Overview.md`
- `docs/tui/BEHAVIORS_TUI_Interactions.md`
- `docs/tui/HEALTH_TUI_Coverage.md`
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md`
- `docs/tui/PATTERNS_TUI_Design.md`
- `docs/tui/SYNC_TUI_State.md`
- `docs/tui/archive/SYNC_archive_2024-12.md`
- `templates/CLAUDE_ADDITION.md`
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`
- `templates/ngram/PRINCIPLES.md`
- `templates/ngram/PROTOCOL.md`
- `templates/ngram/agents/manager/CLAUDE.md`
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # Repository Map:

**Docs:** `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`

**Definitions:**
- `def main()`
- `def run_shell_command()`
- `def read_file()`
- `def list_directory()`
- `def search_file_content()`
- `def glob_files()`
- `def replace_text()`
- `def write_file()`
- `def google_web_search()`
- `def web_fetch()`
- `def codebase_investigator()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class ClickableStatic`
- `def __init__()`
- `def on_click()`
- `class AgentContainer`
- `def __init__()`
- `def _prepare_markdown()`
- `def _set_markdown_content()`
- `def compose()`
- `def on_mount()`
- `def add_agent()`
- `def update_agent()`
- `def remove_agent()`
- `def set_agent_status()`
- `def update_sync_content()`
- `def update_doctor_content()`
- `def get_path()`
- `def update_map_content()`
- `def update_changes_content()`
- `def switch_to_tab()`
- `def add_summary()`
- `def clear_summary()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class AgentPanel`
- `def __init__()`
- `def on_mount()`
- `def on_scroll()`
- `def toggle_collapse()`
- `def collapse()`
- `def expand()`
- `def _update_header_text()`
- `def set_output()`
- `def append_output()`
- `def _maybe_render()`
- `def _flush_render()`
- `def _do_render()`
- `def set_status()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class InputBar`
- `class CommandSubmitted`
- `def __init__()`
- `class InputChanged`
- `class ShowSuggestions`
- `def __init__()`
- `def __init__()`
- `def on_mount()`
- `def _update_height()`
- `def on_text_area_changed()`
- `def value()`
- `def value()`
- `def _submit()`
- `def on_key()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class ClickableStatic`
- `def __init__()`
- `def on_click()`
- `async def update()`
- `class ClickableMarkdown`
- `def __init__()`
- `def on_click()`
- `async def update()`
- `class ManagerPanel`
- `def __init__()`
- `def on_mount()`
- `def _is_at_bottom()`
- `def _auto_scroll()`
- `def add_message()`
- `def add_thinking()`
- `def add_tool_call()`
- `def escape_markup()`
- `def clear()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class StatusBar`
- `def __init__()`
- `def set_folder()`
- `def update_health()`
- `def set_repair_progress()`
- `def clear_repair_progress()`
- `def _start_animation()`
- `def _stop_animation()`
- `def _animate()`
- `def _format_progress_bar()`
- `def _format_bar()`
- `def _refresh_display()`
- `def _get_health_color()`
- `def on_resize()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class SuggestionsBar`
- `def __init__()`
- `def show_suggestions()`

**Docs:** `docs/tui/PATTERNS_TUI_Design.md`

**Definitions:**
- `def check_textual()`
- `class NgramApp`
- `def __init__()`
- `def compose()`
- `async def on_mount()`
- `async def _startup_sequence()`
- `async def _start_claude_pty()`
- `async def on_claude_output()`
- `async def _start_manager_with_overview()`
- `def _build_manager_overview_prompt()`
- `async def _show_static_overview()`
- `async def _animate_loading()`
- `def on_click()`
- `async def on_input_bar_command_submitted()`
- `def on_input_bar_input_changed()`
- `def on_input_bar_show_suggestions()`
- `async def _run_doctor()`
- `async def _run_doctor_with_display()`
- `async def _load_doctor_data()`
- `async def _load_sync_data()`
- `async def _load_map_data()`
- `async def _load_git_data()`
- `async def get_status()`
- `async def get_log()`
- `async def get_recent_commit_rate()`
- `async def get_recent_change_rate()`
- `async def _refresh_changes_tab()`
- `async def _refresh_sync_tab()`
- `async def _refresh_map_tab()`
- `async def _refresh_doctor_tab()`
- `async def _run_doctor_async()`
- `async def _handle_drift_warning()`
- `async def handle_command()`
- `def log_error()`
- `def on_exception()`
- `def notify_manager_response()`
- `def reset_manager_session()`
- `async def action_interrupt_or_quit()`
- `def _reset_ctrl_c()`
- `async def action_quit()`
- `async def action_doctor()`
- `async def action_repair()`
- `def action_tab_agents()`
- `def action_tab_sync()`
- `def action_tab_doctor()`
- `def action_tab_map()`
- `def action_tab_changes()`
- `def action_next_tab()`
- `def action_prev_tab()`
- `def _switch_tab()`
- `def _cycle_tab()`
- `def main()`

**Docs:** `docs/tui/BEHAVIORS_TUI_Interactions.md`

**Definitions:**
- `def _truncate_thinking()`
- `def _output_indicates_rate_limit()`
- `async def handle_command()`
- `async def handle_message()`
- `async def _animate_loading()`
- `async def handle_help()`
- `async def handle_run()`
- `async def _run_shell_command()`
- `async def handle_repair()`
- `def _get_last_messages()`
- `async def _periodic_agent_summary()`
- `async def _run_git_command()`
- `async def _spawn_agent()`
- `async def on_output()`
- `async def _run_agent()`
- `async def _spawn_next_from_queue()`
- `async def _manager_review_agent()`
- `async def handle_doctor()`
- `async def handle_quit()`
- `async def handle_clear()`
- `async def handle_issues()`
- `async def handle_logs()`
- `async def handle_reset_manager()`
- `async def _refresh_map()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `def _detect_commands()`
- `def _build_codex_history_prompt()`
- `async def _run_agent_message()`
- `async def run_agent()`
- `def throttled_update()`
- `async def drain_stderr()`
- `def _build_review_prompt()`
- `async def _run_manager_review()`

**Docs:** `docs/tui/PATTERNS_TUI_Design.md`

**Definitions:**
- `class DriftWarning`
- `class ClaudePTY`
- `def __init__()`
- `async def start()`
- `async def _read_output()`
- `def _clean_output()`
- `async def send()`
- `async def stop()`
- `def is_running()`
- `class ManagerSupervisor`
- `def __init__()`
- `def _normalize_path()`
- `def extract_changed_files()`
- `def extract_doc_updates()`
- `async def check_agent_output()`
- `async def monitor_agent()`
- `async def on_agent_complete()`
- `def write_guidance()`
- `def clear_guidance()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class ConversationMessage`
- `def to_dict()`
- `def from_dict()`
- `class ConversationHistory`
- `def __init__()`
- `def _load()`
- `def _save()`
- `def add_message()`
- `def get_recent()`
- `def clear()`
- `def start_new_session()`
- `class AgentHandle`
- `def duration()`
- `def is_active()`
- `def append_output()`
- `def get_output()`
- `class SessionState`
- `def add_agent()`
- `def remove_agent()`
- `def get_agent()`
- `def add_manager_message()`
- `def active_count()`
- `def clear_completed()`

**Docs:** `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture.md`

**Definitions:**
- `def doctor_check_monolith()`
- `def doctor_check_undocumented()`
- `def doctor_check_stale_sync()`
- `def doctor_check_no_docs_ref()`
- `def extract_impl_file_refs()`
- `def doctor_check_broken_impl_links()`
- `def detect_stub_patterns()`
- `def doctor_check_stub_impl()`
- `def find_empty_functions()`
- `def doctor_check_incomplete_impl()`
- `def doctor_check_undoc_impl()`
- `def doctor_check_yaml_drift()`
- `def doctor_check_missing_tests()`

**Docs:** `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture.md`

**Definitions:**
- `def doctor_check_new_undoc_code()`
- `def doctor_check_doc_duplication()`
- `def doctor_check_recent_log_errors()`
- `def doctor_check_long_strings()`
- `def doctor_check_special_markers()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `def parse_gitignore()`
- `def load_doctor_config()`
- `def load_doctor_ignore()`
- `def is_issue_ignored()`
- `def filter_ignored_issues()`
- `def extract_docs_references_from_file()`
- `def _parse_doc_false_positives()`
- `def parse_doctor_doc_tags()`
- `def load_doctor_false_positives()`
- `def filter_false_positive_issues()`
- `def add_doctor_ignore()`
- `def should_ignore_path()`
- `def is_binary_file()`
- `def find_code_directories()`
- `def has_direct_code_files()`
- `def find_leaf_code_dirs()`
- `def find_source_files()`
- `def count_lines()`
- `def find_long_sections()`

**Definitions:**
- `def get_issue_guidance()`
- `def get_issue_explanation()`
- `def generate_health_markdown()`
- `def print_doctor_report()`
- `def check_sync_status()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `def get_severity_color()`
- `def get_agent_color()`
- `def get_agent_symbol()`
- `def load_github_issue_mapping()`
- `def save_github_issue_mapping()`
- `def spawn_repair_agent()`
- `def repair_command()`
- `def run_repair()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `def get_symbol_name()`
- `def get_issue_folder_name()`
- `class RepairResult`
- `class EscalationDecision`
- `def get_learnings_content()`
- `def _get_git_head()`
- `def get_issue_symbol()`
- `def get_issue_action_parts()`
- `def get_issue_action()`
- `def get_depth_types()`
- `def split_docs_to_read()`
- `def _detect_recent_issue_number()`
- `def build_agent_prompt()`
- `def parse_decisions_from_output()`
- `def parse_stream_json_line()`
- `async def spawn_repair_agent_async()`
- `def run_agent_sync()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `def get_issue_instructions()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `def get_doc_instructions()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `class FileInfo`
- `class DependencyInfo`
- `class RepoOverview`
- `def get_language()`
- `def extract_docs_ref()`
- `def extract_markdown_sections()`
- `def extract_markdown_code_refs()`
- `def extract_markdown_doc_refs()`
- `def extract_code_definitions()`
- `def count_chars()`
- `def _filter_local_imports()`
- `def build_file_tree()`
- `def get_dependency_info()`
- `def count_tree_stats()`
- `def traverse()`
- `def count_docs_structure()`
- `def generate_repo_overview()`
- `def generate_and_save()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `class ValidationResult`
- `def check_protocol_installed()`
- `def check_project_sync_exists()`
- `def check_module_docs_minimum()`
- `def check_full_chain()`
- `def check_chain_links()`
- `def check_naming_conventions()`
- `def check_views_exist()`
- `def check_module_manifest()`
- `def generate_fix_prompt()`
- `def validate_protocol()`

**Sections:**
- # ngram Manager
- ## Your Role
- ## Context You Have
- ## What You Can Do
- ## What You Output
- ## Guidelines
- ## Special Marker Check
- ## Files to Check
- ## Updating LEARNINGS Files
- ## After Your Response

**Sections:**
- # Project — Sync: Current State
- ## CURRENT STATE
- ## ACTIVE WORK
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## AREAS
- ## MODULE COVERAGE

**Code refs:**
- `{path/to/main/source/file.py`

**Sections:**
- # {Module Name} — Algorithm: {Brief Description of Procedures and Logic}
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: {Primary Function Name}
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Code refs:**
- `{path/to/main/source/file.py`

**Sections:**
- # {Module Name} — Behaviors: {Brief Description of Observable Effects}
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Sections:**
- # CONCEPT: {Concept Name} — {What This Concept Is}
- ## WHAT IT IS
- ## WHY IT EXISTS
- ## KEY PROPERTIES
- ## RELATIONSHIPS TO OTHER CONCEPTS
- ## THE CORE INSIGHT
- ## COMMON MISUNDERSTANDINGS
- ## SEE ALSO

**Code refs:**
- `{path/to/health/checker_script.py`

**Sections:**
- # {Module} — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: {Indicator Name}
- ## HOW TO RUN
- # Run all health checks for this module
- # Run a specific checker
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `{path/to/main/source/file.py`

**Sections:**
- # {Module} — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Code refs:**
- `{path/to/main/source/file.py`

**Sections:**
- # {Module Name} — Patterns: {Brief Design Philosophy Description}
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Sections:**
- # {Module/Area/Project} — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Sections:**
- # TOUCHES: Where {Concept Name} Appears in the System
- ## MODULES THAT IMPLEMENT
- ## INTERFACES
- ## DEPENDENCIES
- ## INVARIANTS ACROSS MODULES
- ## CONFLICTS / TENSIONS
- ## SYNC
- ## WHEN TO UPDATE THIS FILE

**Code refs:**
- `{path/to/main/source/file.py`

**Sections:**
- # {Module Name} — Validation: {Brief Description of Invariants and Tests}
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Run tests
- # Run with coverage
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # VIEW: Analyze — Structural Analysis and Recommendations
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## ANALYSIS CHECKLIST
- ## OUTPUT FORMAT
- ## Current Structure
- ## Recommendations
- ## Proposed Structure
- ## AFTER ANALYSIS
- ## Structural Analysis — [DATE]
- ## HANDOFF
- ## VERIFICATION

**Sections:**
- # VIEW: Debug
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## THE WORK
- ## WHEN YOU FIND IT
- ## HANDOFFS
- ## OBSERVATIONS (Living Documentation)
- ## Agent Observations
- ## VERIFICATION

**Sections:**
- # VIEW: Document New Module
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## THE WORK
- ## CHAIN
- # DOCS: docs/backend/auth/PATTERNS_Why_JWT_With_Refresh_Tokens.md
- ## MINIMUM VIABLE DOCUMENTATION
- ## AFTER DOCUMENTATION
- ## VERIFICATION

**Code refs:**
- `file_utils.py`
- `ngram/utils/file_utils.py`
- `ngram/utils/string_utils.py`
- `ngram/utils/validation_utils.py`
- `src/analytics/batch_ingest.py`
- `src/analytics/storage/event_store.py`
- `src/analytics/stream_ingest.py`
- `src/analytics/validation/schema_rules.py`
- `src/dashboard/op_metrics.py`
- `src/dashboard/product_metrics.py`
- `string_utils.py`
- `utils.py`

**Sections:**
- # VIEW: Escalation & Proposition
- ## VISION
- ## THE PATTERN
- ## HOW ESCALATION WORKS
- ## HOW PROPOSITION WORKS
- ## WHEN TO ESCALATE (PRECISE)
- ## WHEN NOT TO ESCALATE
- ## ESCALATION TYPES
- ## ESCALATION MARKER FORMAT (YAML)
- ## PROPOSITION MARKER FORMAT (YAML)
- ## PRIORITY SCALE (HOW TO SET)
- ## HOOKS (WHEN TO INCLUDE)

**Sections:**
- # VIEW: Extend
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## PLANNING
- ## THE WORK
- ## BEFORE VERIFICATION: DOC VERIFICATION
- ## AFTER EXTENDING
- # modules.yaml (project root)
- ## HANDOFFS
- ## OBSERVATIONS (Living Documentation)
- ## Agent Observations
- ## VERIFICATION

**Sections:**
- # VIEW: Health — Define Health Checks and Verify System Health
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## WHAT TO DEFINE
- ## WRITING GOOD HEALTH
- ## AFTER DEFINING HEALTH
- ## OBSERVATIONS (Living Documentation)
- ## Agent Observations
- ## HANDOFF
- ## VERIFICATION
- ## DOCTOR FALSE POSITIVES

**Sections:**
- # VIEW: Implement
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## THE WORK
- ## BEFORE VERIFICATION: DOC VERIFICATION
- ## AFTER IMPLEMENTATION
- # modules.yaml (project root)
- # ... other fields as relevant
- ## OBSERVATIONS (Living Documentation)
- ## Agent Observations
- ## VERIFICATION

**Sections:**
- # VIEW: Ingest — Process Raw Data Sources
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## THE WORK
- ## OUTPUT
- ## HANDOFF
- ## VERIFICATION
- ## TIPS

**Sections:**
- # VIEW: Onboard — Understand Existing Codebase
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## WHAT TO BUILD
- ## QUESTIONS TO ANSWER
- ## CODE RESTRUCTURE ANALYSIS
- ## Proposed Structure Changes
- ## OUTPUT
- ## HANDOFF

**Sections:**
- # VIEW: Refactor — Improve Code Structure Without Changing Behavior
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## BEFORE REFACTORING
- ## WHILE REFACTORING
- ## AFTER REFACTORING
- ## OBSERVATIONS (Living Documentation)
- ## Agent Observations
- ## HANDOFF
- ## VERIFICATION

**Sections:**
- # Working Principles
- ## Architecture: One Solution Per Problem
- ## Verification: Test Before Claiming Built
- ## Communication: Depth Over Brevity
- ## Quality: Never Degrade
- ## Experience: User Before Infrastructure
- ## Feedback Loop: Human-Agent Collaboration
- ## How These Principles Integrate

**Doc refs:**
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # ngram Framework
- ## WHY THIS PROTOCOL EXISTS
- ## COMPANION: PRINCIPLES.md
- ## THE CORE INSIGHT
- ## HOW TO USE THIS
- ## FILE TYPES AND THEIR PURPOSE
- ## KEY PRINCIPLES (from PRINCIPLES.md)
- ## STRUCTURING YOUR DOCS
- ## WHEN DOCS DON'T EXIST
- ## THE DOCUMENTATION PROCESS
- ## Maturity
- ## THE PROTOCOL IS A TOOL

**Sections:**
- ## 4. Protocol-First Reading
- ## 5. Parallel Work Awareness
- ## 6. Operational Proactivity
- ## 5. Communication Principles

**Sections:**
- ## GEMINI Agent Operating Principles (Derived from ngram Protocol)
- ## Operational Directives

**Doc refs:**
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # ngram
- # Working Principles
- ## Architecture: One Solution Per Problem
- ## Verification: Test Before Claiming Built
- ## Communication: Depth Over Brevity
- ## Quality: Never Degrade
- ## Experience: User Before Infrastructure
- ## Feedback Loop: Human-Agent Collaboration
- ## How These Principles Integrate
- # ngram Framework
- ## WHY THIS PROTOCOL EXISTS
- ## COMPANION: PRINCIPLES.md
- ## THE CORE INSIGHT
- ## HOW TO USE THIS
- ## FILE TYPES AND THEIR PURPOSE
- ## KEY PRINCIPLES (from PRINCIPLES.md)
- ## STRUCTURING YOUR DOCS
- ## WHEN DOCS DON'T EXIST
- ## THE DOCUMENTATION PROCESS
- ## Maturity
- ## THE PROTOCOL IS A TOOL
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change
- ## CLI Commands
- ## 4. Protocol-First Reading
- ## 5. Parallel Work Awareness
- ## 6. Operational Proactivity
- ## 5. Communication Principles

**Sections:**
- # ngram
- ## The Problem
- ## The Solution
- ## Quick Start
- # Install
- # Initialize in your project
- # Check protocol health
- # Check project health (monoliths, stale docs, etc.)
- # Auto-fix issues with agents
- # Get documentation context for a file
- # Generate bootstrap prompt for LLM
- ## CLI Commands
- ## How It Works
- # ngram
- # VIEW: Implement
- ## LOAD FIRST
- ## AFTER CHANGES
- ## Documentation Chain
- ## Key Concepts
- ## Design Principles
- ## License
- ## Contributing
