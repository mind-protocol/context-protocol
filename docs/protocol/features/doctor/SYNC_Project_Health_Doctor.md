# SYNC: Project Health Doctor

```
LAST_UPDATED: 2025-12-16
UPDATED_BY: Claude (Opus 4.5)
STATUS: CANONICAL
```

---

## MATURITY

**What's canonical (v1):**
- CLI command: `add-framework doctor`
- Output formats: text, JSON
- Level filtering: --level critical/warning/all
- Configuration via config.yaml
- .gitignore pattern support
- Checks: monolith, undocumented, stale_sync, placeholder, no_docs_ref, incomplete_chain
- Default ignores: node_modules, .next, dist, build, vendor, __pycache__, etc.
- Health score: 0-100

**What's documented but not implemented (v2):**
- check_activity_gaps - No SYNC updates in N days
- check_abandoned - Docs started but never completed
- check_vague_names - Files named utils, helpers, misc, etc.
- `--guide` remediation mode
- Markdown output format

---

## CURRENT STATE

Doctor command implemented and working.

The command provides holistic project health analysis beyond pass/fail validation. Checks for:
- Monolith files (>500 lines by default)
- Undocumented code directories
- Stale SYNC files (>14 days by default)
- Placeholder docs (template markers)
- Missing DOCS: references (info only)
- Incomplete doc chains

Features:
- Text and JSON output
- Severity filtering (--level)
- .gitignore pattern support
- Configurable thresholds via config.yaml
- Smart default ignores (node_modules, .next, etc.)

---

## IMPLEMENTATION ORDER

Suggested order based on dependencies:

1. **Configuration loader** — Other checks need thresholds
2. **Project discovery** — Finds files to check
3. **Individual checks** — Start with monolith, undocumented
4. **Aggregation & scoring** — Combine results
5. **Output formatters** — Text first, then JSON
6. **CLI integration** — Wire into click
7. **Guided remediation** — `--guide` flag

---

## HANDOFF: FOR AGENTS

**Likely VIEW:** VIEW_Implement

**To implement:**
1. Read ALGORITHM doc for pseudocode
2. Add `doctor` command to cli.py
3. Create `doctor.py` module for checks
4. Follow existing CLI patterns (click decorators, Path handling)

**Key decisions already made:**
- Monolith threshold: 500 lines default
- Stale SYNC threshold: 14 days default
- Score deductions: critical=-10, warning=-3, info=-1

**Watch out for:**
- Don't count lines in binary files
- Handle permission errors gracefully
- Sort file traversal for determinism

---

## HANDOFF: FOR HUMAN

**Summary:** Doctor command fully designed. Docs specify checks, output format, configuration, and testing approach. Ready for implementation.

**Decisions to review:**
- Threshold defaults (500 lines, 14 days) — adjust?
- Severity assignments — anything miscategorized?
- Missing checks — anything else worth detecting?

---

## TODO

### Implemented (v1)

- [x] Configuration loader (config.yaml support)
- [x] Project discovery functions
- [x] check_monolith
- [x] check_undocumented
- [x] check_stale_sync
- [x] check_placeholder_docs
- [x] check_no_docs_ref
- [x] check_incomplete_chain
- [x] Result aggregation
- [x] Score calculation
- [x] Text output formatter
- [x] JSON output formatter
- [x] CLI command integration
- [x] Auto-save to HEALTH.md

### To Implement (v2)

- [ ] check_activity_gaps - No SYNC updates in N days across project
- [ ] check_abandoned - Docs started but never completed
- [ ] check_vague_names - Files named utils, helpers, misc, etc.
- [ ] `--guide` remediation mode

### Future Ideas

- IDEA: `--fix` mode that auto-creates missing docs
- IDEA: `--watch` mode for continuous health monitoring
- IDEA: Health score badge for README
- IDEA: Integration with CI (GitHub Actions template)
- IDEA: Trend tracking (score over time)

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Project_Health_Doctor.md
BEHAVIORS:       ./BEHAVIORS_Project_Health_Doctor.md
ALGORITHM:       ./ALGORITHM_Project_Health_Doctor.md
VALIDATION:      ./VALIDATION_Project_Health_Doctor.md
IMPLEMENTATION:  ./IMPLEMENTATION_Project_Health_Doctor.md
TEST:            ./TEST_Project_Health_Doctor.md
SYNC:            THIS
```
