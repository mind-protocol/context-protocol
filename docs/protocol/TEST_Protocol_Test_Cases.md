# ADD Framework — Test: Test Cases and Coverage

```
STATUS: STABLE
CREATED: 2024-12-16
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md
BEHAVIORS:       ./BEHAVIORS_Observable_Protocol_Effects.md
ALGORITHM:       ./ALGORITHM_Workflows_And_Procedures.md
VALIDATION:      ./VALIDATION_Protocol_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Protocol_Code_Architecture.md
THIS:            TEST_Protocol_Test_Cases.md
SYNC:            ./SYNC_Protocol_Current_State.md
```

---

## TEST STRATEGY

The protocol is tested through:
1. **CLI validation** — `add-framework validate` checks invariants
2. **Dogfooding** — The protocol uses itself
3. **Real-world usage** — Testing on actual projects (blood-ledger)

---

## CLI TESTS

### `add-framework init`

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| Fresh install | Empty directory | Creates .add-framework/, CLAUDE.md | pass |
| Already exists | Directory with .add-framework/ | Error unless --force | pass |
| Force overwrite | --force flag | Overwrites existing | pass |

### `add-framework validate`

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| No protocol | Directory without .add-framework/ | Fails V6 | pass |
| Uninitialized SYNC | Template placeholders | Fails V6 | pass |
| Missing VIEWs | Incomplete views/ | Fails V7 | pass |
| Broken CHAIN links | Dead references | Fails V3 | pass |
| Naming violations | PATTERN.md (not PATTERNS_) | Fails NC | pass |
| Incomplete chain | Missing doc types | Fails FC | pass |
| All valid | Complete protocol | All pass | pass |

### `add-framework prompt`

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| Generate prompt | Valid directory | Bootstrap prompt with paths | pass |

### `add-framework context`

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| File with DOCS: ref | cli.py | Returns full chain | pass |
| File without DOCS: | Random file | "No linked documentation" | pass |

---

## INTEGRATION TESTS

### Dogfooding

```
GIVEN:  Protocol repo exists
WHEN:   Run `add-framework init` on itself
THEN:   .add-framework/ created
AND:    `add-framework validate` passes
STATUS: pass
```

### Blood Ledger Installation

```
GIVEN:  blood-ledger project exists
WHEN:   Run `add-framework init --dir ~/the-blood-ledger`
THEN:   Protocol installed
AND:    CLAUDE.md updated
AND:    Validate shows gaps to fix
STATUS: pass
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Empty docs/ directory | Validate should pass (nothing to check) | pass |
| Module at root level | docs/module/ (not docs/area/module/) | pass |
| Nested modules | docs/area/module/ pattern | pass |
| Multiple CHAIN links | File with many refs | pass |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| CLI init | High | All flags tested |
| CLI validate | High | All checks tested |
| CLI prompt | Medium | Basic output tested |
| CLI context | Medium | DOCS: ref tested |
| Module detection | High | Both nesting levels |

---

## HOW TO RUN

```bash
# Manual testing via CLI
add-framework validate --dir /path/to/project
add-framework context file.py --dir /path/to/project

# Dogfood test
add-framework init --dir /home/mind-protocol/add-framework --force
add-framework validate --dir /home/mind-protocol/add-framework
```

---

## KNOWN TEST GAPS

- [ ] Automated test suite (pytest)
- [ ] CI integration
- [ ] Edge case: very deep nesting (docs/a/b/c/module/)
- [ ] Edge case: symlinks in docs/

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add pytest test suite
- [ ] Add GitHub Actions CI
- IDEA: `add-framework test` command to run self-tests
- QUESTION: Should validate be strict (fail) or lenient (warn)?
