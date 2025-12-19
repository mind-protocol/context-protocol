# BEHAVIORS: Project Health Doctor

**Observable effects of the doctor command.**

---

## COMMAND INTERFACE

```bash
# Basic health check
ngram doctor

# With specific directory
ngram doctor --dir /path/to/project

# Output formats
ngram doctor --format text     # Human readable (default)
ngram doctor --format json     # Machine readable
ngram doctor --format markdown # For reports

# Filter by severity
ngram doctor --level critical  # Only critical issues
ngram doctor --level warning   # Critical + warnings
ngram doctor --level all       # Everything (default)

# Specific checks
ngram doctor --check monolith
ngram doctor --check stale
ngram doctor --check undocumented
```

---

## OUTPUT BEHAVIOR

### Text Format (Default)

```
🏥 Project Health Report: my-project
=====================================

## Critical (2 issues)

  ✗ MONOLITH: src/game/combat.ts
    847 lines (threshold: 500)
    → Consider splitting into combat/attack.ts, combat/defense.ts, combat/damage.ts

  ✗ UNDOCUMENTED: src/api/
    No documentation exists for this code directory
    → Run: ngram doctor --guide src/api/
    → See: VIEW_Document_Create_Module_Documentation.md

## Warnings (3 issues)

  ⚠ STALE_SYNC: docs/vision/SYNC_Vision_State.md
    Last updated 23 days ago, 47 commits since
    → Review and update SYNC with current state

  ⚠ NO_DOCS_REF: src/types/game.ts
    Code file has no DOCS: reference comment
    → Add: # DOCS: docs/types/PATTERNS_*.md

  ⚠ INCOMPLETE_CHAIN: docs/auth/
    Missing: TEST_*.md
    → Create TEST doc or mark as intentionally skipped

## Info (3 issues)

  ℹ ACTIVITY_GAP: .ngram/
    No SYNC updates in 18 days
    → Review project state and update relevant SYNC files

  ℹ ABANDONED: docs/auth/
    Started 45 days ago, only has PATTERNS, SYNC
    → Either complete documentation or remove if no longer relevant

  ℹ VAGUE_NAME: src/utils.ts
    File named 'utils.ts' is non-descriptive
    → Consider naming by what it actually does (e.g., string_helpers, date_formatters)

─────────────────────────────────────
Health Score: 64/100
Critical: 2 | Warnings: 3 | Info: 3
─────────────────────────────────────

## Suggested Actions

1. [ ] Split src/game/combat.ts (Critical)
2. [ ] Document src/api/ (Critical)
3. [ ] Update docs/vision/SYNC_Vision_State.md (Warning)
4. [ ] Add DOCS: ref to src/types/game.ts (Warning)

Run `ngram doctor --guide <path>` for detailed remediation.
```

### JSON Format

```json
{
  "project": "/path/to/project",
  "timestamp": "2025-12-16T10:30:00Z",
  "score": 67,
  "issues": {
    "critical": [
      {
        "type": "MONOLITH",
        "path": "src/game/combat.ts",
        "details": {
          "lines": 847,
          "threshold": 500
        },
        "suggestion": "Split into smaller modules"
      }
    ],
    "warning": [...],
    "info": [...]
  },
  "summary": {
    "critical": 2,
    "warning": 3,
    "info": 1
  }
}
```

---

## GUIDED REMEDIATION

```bash
ngram doctor --guide src/api/
```

Outputs detailed steps for fixing a specific issue:

```
🔧 Remediation Guide: src/api/
==============================

Issue: UNDOCUMENTED
This code directory has no documentation.

## Current State
- 5 files in src/api/
- 423 total lines
- Main entry: index.ts

## Recommended Steps

1. Create documentation directory:
   mkdir -p docs/api/

2. Create minimum viable docs:
   - PATTERNS_Api_Design.md (why this API shape)
   - SYNC_Api_State.md (current status)

3. Add DOCS reference to main file:
   # DOCS: docs/api/PATTERNS_Api_Design.md

4. Update modules.yaml:
   api:
     code: "src/api/**"
     docs: "docs/api/"
     maturity: DESIGNING

5. Run validation:
   ngram validate

## Template Commands

# Generate PATTERNS from template
ngram doctor --scaffold PATTERNS docs/api/

## Reference
- VIEW: .ngram/views/VIEW_Document_Create_Module_Documentation.md
```

---

## EXIT CODES

| Code | Meaning |
|------|---------|
| 0 | No critical issues |
| 1 | Critical issues found |
| 2 | Error running doctor |

Allows CI integration:
```bash
ngram doctor --level critical || exit 1
```

---

## CONFIGURATION

`.ngram/config.yaml`:

```yaml
doctor:
  # Thresholds
  monolith_lines: 500
  god_function_lines: 100
  stale_sync_days: 14
  designing_stuck_days: 21
  nesting_depth: 4

  # Ignore patterns
  ignore:
    - "src/generated/**"
    - "vendor/**"
    - "**/*.test.ts"

  # Disable specific checks
  disabled_checks:
    - circular_deps  # Too slow for large projects

  # Custom severity overrides
  severity_overrides:
    incomplete_chain: info  # Downgrade from warning
```

---

## FALSE POSITIVE SUPPRESSION

If a check is a false positive, the doctor ignores it when a linked doc declares it.

Add a line directly under the doc's `UPDATED: YYYY-MM-DD` metadata line:

`@ngram:doctor:CHECK_TYPE_NAME:false_positive Explanation message`

The suppression applies when the issue's file references that doc via a `DOCS:` header, or when the issue targets that doc file directly.

---

## DOC TEMPLATE DRIFT DEFERMENTS

For the doc template drift check (`DOC_TEMPLATE_DRIFT`), you can defer or mark as non-required in the same metadata block:

`@ngram:doctor:DOC_TEMPLATE_DRIFT:postponed YYYY-MM-DD Short explanation`
`@ngram:doctor:DOC_TEMPLATE_DRIFT:non-required Short explanation`
`@ngram:doctor:DOC_TEMPLATE_DRIFT:escalation Detailed choice/question/context for human`

If a postponed date is in the past, the issue is still reported.

---

## NON-STANDARD DOC TYPE DEFERMENTS

For the non-standard doc type check (`NON_STANDARD_DOC_TYPE`), you can defer or mark as exception:

`@ngram:doctor:NON_STANDARD_DOC_TYPE:postponed YYYY-MM-DD Short explanation`
`@ngram:doctor:NON_STANDARD_DOC_TYPE:exception Short explanation`

If a postponed date is in the past, the issue is still reported.

---

## RESOLVED ESCALATION MARKERS

Doctor flags any file containing `@ngram:solved-escalations` (or `@ngram:solved-escalation`) as `RESOLVE_ESCALATION` so resolved markers get applied and cleaned up.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Project_Health_Doctor.md
BEHAVIORS:       THIS
ALGORITHM:       ./ALGORITHM_Project_Health_Doctor.md
VALIDATION:      ./VALIDATION_Project_Health_Doctor.md
IMPLEMENTATION:  ./IMPLEMENTATION_Project_Health_Doctor.md
TEST:            ./TEST_Project_Health_Doctor.md
SYNC:            ./SYNC_Project_Health_Doctor.md
```
