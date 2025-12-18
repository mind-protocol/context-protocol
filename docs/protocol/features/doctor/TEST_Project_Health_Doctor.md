# TEST: Project Health Doctor

**Test cases and coverage for the doctor command.**

---

## TEST STRUCTURE

```
tests/
└── doctor/
    ├── test_checks.py          # Individual check tests
    ├── test_aggregation.py     # Result aggregation
    ├── test_scoring.py         # Score calculation
    ├── test_output.py          # Output formatting
    ├── test_config.py          # Configuration loading
    └── fixtures/               # Test project structures
        ├── clean_project/
        ├── monolith_project/
        ├── undocumented_project/
        └── stale_project/
```

---

## UNIT TESTS

### Check: Monolith Files

```python
class TestMonolithCheck:

    def test_under_threshold_passes(self, tmp_path):
        """Files under threshold produce no issues."""
        create_file(tmp_path / "src/small.py", lines=499)
        config = {"monolith_lines": 500}

        issues = check_monolith(discover_project(tmp_path), config)

        assert len(issues) == 0

    def test_at_threshold_passes(self, tmp_path):
        """Files exactly at threshold pass."""
        create_file(tmp_path / "src/exact.py", lines=500)
        config = {"monolith_lines": 500}

        issues = check_monolith(discover_project(tmp_path), config)

        assert len(issues) == 0

    def test_over_threshold_fails(self, tmp_path):
        """Files over threshold produce critical issue."""
        create_file(tmp_path / "src/big.py", lines=501)
        config = {"monolith_lines": 500}

        issues = check_monolith(discover_project(tmp_path), config)

        assert len(issues) == 1
        assert issues[0].type == "MONOLITH"
        assert issues[0].severity == "critical"
        assert issues[0].details["lines"] == 501

    def test_ignored_files_skipped(self, tmp_path):
        """Ignored patterns are not checked."""
        create_file(tmp_path / "src/generated/big.py", lines=1000)
        config = {"monolith_lines": 500, "ignore": ["**/generated/**"]}

        issues = check_monolith(discover_project(tmp_path), config)

        assert len(issues) == 0

    def test_binary_files_skipped(self, tmp_path):
        """Binary files are not counted."""
        create_binary_file(tmp_path / "src/image.png", size=100000)
        config = {"monolith_lines": 500}

        issues = check_monolith(discover_project(tmp_path), config)

        assert len(issues) == 0
```

### Check: Stale SYNC

```python
class TestStaleSyncCheck:

    def test_recent_sync_passes(self, tmp_path):
        """SYNC updated recently produces no issue."""
        create_sync_file(tmp_path, days_ago=0)
        config = {"stale_sync_days": 14}

        issues = check_stale_sync(discover_project(tmp_path), config)

        assert len(issues) == 0

    def test_old_sync_warns(self, tmp_path):
        """SYNC older than threshold produces warning."""
        create_sync_file(tmp_path, days_ago=15)
        config = {"stale_sync_days": 14}

        issues = check_stale_sync(discover_project(tmp_path), config)

        assert len(issues) == 1
        assert issues[0].severity == "warning"

    def test_sync_without_date_warns(self, tmp_path):
        """SYNC with no LAST_UPDATED produces warning."""
        create_sync_file(tmp_path, no_date=True)
        config = {"stale_sync_days": 14}

        issues = check_stale_sync(discover_project(tmp_path), config)

        assert len(issues) == 1
```

### Check: Undocumented Code

```python
class TestUndocumentedCheck:

    def test_mapped_code_passes(self, tmp_path):
        """Code with modules.yaml mapping passes."""
        create_code_dir(tmp_path / "src/api")
        create_docs_dir(tmp_path / "docs/api")
        create_modules_yaml(tmp_path, {"api": {"code": "src/api/**", "docs": "docs/api/"}})

        issues = check_undocumented(discover_project(tmp_path), {})

        assert len(issues) == 0

    def test_unmapped_code_fails(self, tmp_path):
        """Code without mapping produces critical issue."""
        create_code_dir(tmp_path / "src/api")
        create_modules_yaml(tmp_path, {})

        issues = check_undocumented(discover_project(tmp_path), {})

        assert len(issues) == 1
        assert issues[0].type == "UNDOCUMENTED"
        assert issues[0].severity == "critical"

    def test_mapped_but_missing_docs_fails(self, tmp_path):
        """Code mapped to non-existent docs produces critical issue."""
        create_code_dir(tmp_path / "src/api")
        create_modules_yaml(tmp_path, {"api": {"code": "src/api/**", "docs": "docs/api/"}})
        # Note: docs/api/ not created

        issues = check_undocumented(discover_project(tmp_path), {})

        assert len(issues) == 1
        assert issues[0].type == "MISSING_DOCS"
```

---

## INTEGRATION TESTS

```python
class TestDoctorIntegration:

    def test_clean_project_scores_100(self, clean_project_fixture):
        """Clean project with all conventions followed scores 100."""
        result = run_doctor(clean_project_fixture)

        assert result.score == 100
        assert len(result.issues["critical"]) == 0
        assert len(result.issues["warning"]) == 0

    def test_exit_code_on_critical(self, monolith_project_fixture):
        """Projects with critical issues exit with code 1."""
        result = run_doctor(monolith_project_fixture)

        assert result.exit_code == 1

    def test_json_output_is_valid(self, any_project_fixture):
        """JSON output is parseable."""
        output = run_doctor_raw(any_project_fixture, format="json")

        parsed = json.loads(output)
        assert "score" in parsed
        assert "issues" in parsed

    def test_deterministic_output(self, any_project_fixture):
        """Running doctor twice produces same output."""
        output1 = run_doctor_raw(any_project_fixture)
        output2 = run_doctor_raw(any_project_fixture)

        assert output1 == output2
```

---

## FIXTURE PROJECTS

### clean_project/

```
clean_project/
├── .context-protocol/
│   ├── modules.yaml        # All code mapped
│   └── state/
│       └── SYNC_Project_State.md  # Recently updated
├── src/
│   └── api/
│       └── index.ts        # Small file, has DOCS: ref
└── docs/
    └── api/
        ├── PATTERNS_*.md
        ├── BEHAVIORS_*.md
        ├── ALGORITHM_*.md
        ├── VALIDATION_*.md
        ├── TEST_*.md
        └── SYNC_*.md
```

### monolith_project/

```
monolith_project/
├── .context-protocol/
└── src/
    └── everything.ts       # 1000+ lines
```

### undocumented_project/

```
undocumented_project/
├── .context-protocol/
│   └── modules.yaml        # Empty mappings
└── src/
    ├── api/
    ├── auth/
    └── utils/              # None documented
```

### stale_project/

```
stale_project/
├── .context-protocol/
│   └── state/
│       └── SYNC_Project_State.md  # LAST_UPDATED: 60 days ago
└── src/
    └── ...
```

---

## COVERAGE TARGETS

| Area | Target | Rationale |
|------|--------|-----------|
| Check functions | 100% | Core logic must be fully tested |
| Configuration | 90% | Edge cases in config parsing |
| Output formatting | 80% | Visual output harder to test |
| CLI interface | 70% | Integration tests cover most |

---

## RUNNING TESTS

```bash
# All doctor tests
pytest tests/doctor/

# With coverage
pytest tests/doctor/ --cov=context_protocol.doctor

# Specific check
pytest tests/doctor/test_checks.py::TestMonolithCheck

# Integration only
pytest tests/doctor/ -m integration
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Project_Health_Doctor.md
BEHAVIORS:       ./BEHAVIORS_Project_Health_Doctor.md
ALGORITHM:       ./ALGORITHM_Project_Health_Doctor.md
VALIDATION:      ./VALIDATION_Project_Health_Doctor.md
IMPLEMENTATION:  ./IMPLEMENTATION_Project_Health_Doctor.md
TEST:            THIS
SYNC:            ./SYNC_Project_Health_Doctor.md
```
