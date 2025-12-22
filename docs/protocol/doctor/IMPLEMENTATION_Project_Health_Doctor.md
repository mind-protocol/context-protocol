# Project Health Doctor — Implementation: Code architecture and docking

@ngram:id: PROTOCOL.DOCTOR.IMPLEMENTATION

```
STATUS: CANONICAL
CREATED: 2025-12-21
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Project_Health_Doctor.md
BEHAVIORS:       ./BEHAVIORS_Project_Health_Doctor.md
ALGORITHM:       ./ALGORITHM_Project_Health_Doctor.md
VALIDATION:      ./VALIDATION_Project_Health_Doctor.md
THIS:            IMPLEMENTATION_Project_Health_Doctor.md
HEALTH:          ./HEALTH_Project_Health_Doctor.md
SYNC:            ./SYNC_Project_Health_Doctor.md
```

---

## CODE STRUCTURE

| File | Purpose | Key functions | Notes |
|------|---------|---------------|-------|
| `ngram/doctor.py` | CLI entry point and runner orchestration | `DoctorRunner`, `main`, `collect_checks` | Parses args, wires config, and emits text/JSON output. |
| `ngram/doctor_checks_core.py` | Structural checks | `doctor_check_monolith`, `doctor_check_undocumented`, `doctor_check_stale_sync` | Ensures file size and code coverage remain manageable and mapped. |
| `ngram/doctor_checks_reference.py` | DOCS/IMPLEMENTATION linkage | `doctor_check_no_docs_ref`, `doctor_check_broken_impl_links` | Confirms every source and implementation doc references each other. |
| `ngram/doctor_checks_stub.py` | Placeholder detection | `doctor_check_stub_impl`, `doctor_check_incomplete_impl`, `doctor_check_undoc_impl` | Finds stub impls, empty functions, and undocumented files. |
| `ngram/doctor_checks_metadata.py` | modules.yaml coverage | `doctor_check_yaml_drift`, `doctor_check_missing_tests` | Validates metadata against actual code/docs/tests. |
| `ngram/doctor_checks_prompt_integrity.py` | Prompt + coupling checks | `doctor_check_prompt_doc_reference`, `doctor_check_doc_link_integrity`, `doctor_check_code_doc_delta_coupling` | Drives the prompt health checks and tracks doc/SYNC coupling. |
| `ngram/doctor_checks_content.py` | Content-specific validations | `doctor_check_doc_duplication`, `doctor_check_long_strings`, `doctor_check_recent_log_errors`, `doctor_check_special_markers`, `doctor_check_new_undoc_code` | Drives documentation hygiene signals. |
| `ngram/doctor_checks_docs.py` | Documentation health rules | `doctor_check_incomplete_chain`, `doctor_check_doc_template_drift`, `doctor_check_large_doc_module`, `doctor_check_nonstandard_doc_type`, `doctor_check_placeholder_docs`, `doctor_check_orphan_docs`, `doctor_check_stale_impl` | Ensures PATTERNS→SYNC chains stay intact. |
| `ngram/doctor_checks_naming.py` | Naming/style heuristics | `doctor_check_vague_names` | Detects low-information filenames. |
| `ngram/doctor_checks_quality.py` | Quality heuristics | `doctor_check_magic_values`, `doctor_check_hardcoded_secrets` | Tracks magic numbers and secrets. |
| `ngram/doctor_checks_sync.py` | Sync and state checks | `doctor_check_doc_gaps`, `doctor_check_conflicts`, `doctor_check_suggestions` | Validates the maintenance cadence of SYNC files and proposals. |
| `ngram/doctor_files.py` | Discovery helpers | `discover_docs`, `load_doctor_false_positives`, `find_code_directories` | Enumerates sources, respects ignores, and feeds the check runner. |

```
IMPL: ngram/doctor.py
IMPL: ngram/doctor_checks.py
IMPL: ngram/doctor_checks_content.py
IMPL: ngram/doctor_checks_docs.py
IMPL: ngram/doctor_checks_naming.py
IMPL: ngram/doctor_checks_quality.py
IMPL: ngram/doctor_checks_sync.py
IMPL: ngram/doctor_files.py
```

---

## DATA FLOW

- CLI → `ngram/doctor.py` → `DoctorRunner.run()`  
  - loads config + SW/h threshold  
  - collects doc root via `ngram/doctor_files.py`
  - dispatches to each `doctor_check_*` function
- Each `doctor_check_*` returns `DoctorIssue` records  
  - aggregated in `ngram/doctor_checks.py`  
  - output formatted and scored before exiting

Docking points for health clients:
- `DOCS` metadata (`docs/*` tags) consumed by `doctor_check_doc_link_integrity`.
- `SYNC` metadata inspected by `doctor_check_code_doc_delta_coupling`.

---

## DOC-LINK COMPLIANCE

 The doctor implementation is the bi-directional anchor for every health-related doc. The CLI/doctor doc chain now names every code path referenced by the health indicators listed in `...ngram/state/SYNC_Project_Health.md` (also available at `..ngram/state/SYNC_Project_Health.md`):

- `ngram/doctor.py` serves as the CLI entry glue.
- `ngram/doctor_checks.py` orchestrates the check catalog.
- `ngram/doctor_checks_content.py` contains the doc-link & code-doc checks.
- `ngram/doctor_checks_docs.py`, `ngram/doctor_checks_quality.py`, `ngram/doctor_checks_naming.py`, and `ngram/doctor_checks_sync.py` embody the validation suite.
- `ngram/doctor_files.py` hosts discovery helpers used by every check.

Each code file above also appears in the prompt health doc chain via `DOCS:` pointers so `ngram doctor` can assert the linkage remains intact.

---

## LOCATIONS

| Area | Description |
|------|-------------|
| `ngram/doctor.py` | CLI command wiring (`docs/cli/core/...` references this doc). |
| `ngram/doctor_checks.py` | Contains `doctor_check_doc_link_integrity`, `doctor_check_code_doc_delta_coupling`, `doctor_check_monolith`, etc. |
| `ngram/doctor_checks_*` | Each module represents a badge of health coverage (content, docs, naming, quality, sync). |
| `ngram/doctor_files.py` | Shared discovery logic, false-positive suppression, and config watchers. |

---

## GAPS / IDEAS

<!-- @ngram:todo The `doctor_check_*` functions could expose metadata describing which IMPLEMENTATION docs they reference for richer doc linking automation. -->
<!-- @ngram:proposition Emit structured events from `DoctorRunner` so `ngram doctor` health results can feed dashboards. -->
