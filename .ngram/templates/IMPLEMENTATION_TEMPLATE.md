# {Module} — Implementation: Code Architecture and Structure

```
STATUS: {DRAFT | STABLE | DEPRECATED}
CREATED: {DATE}
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_{name}.md
BEHAVIORS:      ./BEHAVIORS_{name}.md
ALGORITHM:      ./ALGORITHM_{name}.md
VALIDATION:     ./VALIDATION_{name}.md
THIS:           IMPLEMENTATION_{name}.md
TEST:           ./TEST_{name}.md
SYNC:           ./SYNC_{name}.md
```

---

## CODE STRUCTURE

```
{area}/
├── {module}/
│   ├── __init__.py          # {what this exports}
│   ├── {file}.py             # {responsibility}
│   ├── {file}.py             # {responsibility}
│   └── {submodule}/
│       └── {file}.py         # {responsibility}
```

### File Responsibilities

| File | Purpose | Key Functions/Classes |
|------|---------|----------------------|
| `{path}` | {what it does} | `{func}`, `{class}` |
| `{path}` | {what it does} | `{func}`, `{class}` |

---

## SCHEMA

### {Data Structure Name}

```yaml
{StructureName}:
  required:
    - {field}: {type}          # {description}
    - {field}: {type}          # {description}
  optional:
    - {field}: {type}          # {description}
  constraints:
    - {constraint description}
```

### {Data Structure Name}

```yaml
{StructureName}:
  required:
    - {field}: {type}
  relationships:
    - {relation}: {target structure}
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| {name} | `{file}:{line}` | {what triggers this} |
| {name} | `{file}:{line}` | {what triggers this} |

---

## DATA FLOW

### {Flow Name}: {Brief Description}

```
┌─────────────────┐
│  {Input Source} │
└────────┬────────┘
         │ {data type}
         ▼
┌─────────────────┐
│   {Module A}    │ ← {what happens here}
│   {file.py}     │
└────────┬────────┘
         │ {transformed data}
         ▼
┌─────────────────┐
│   {Module B}    │ ← {what happens here}
│   {file.py}     │
└────────┬────────┘
         │ {output type}
         ▼
┌─────────────────┐
│  {Output/Sink}  │
└─────────────────┘
```

### {Flow Name}: {Brief Description}

```
{Another flow diagram}
```

---

## LOGIC CHAINS

### LC1: {Chain Name}

**Purpose:** {what this chain accomplishes}

```
{input}
  → {module_a}.{function}()     # {what it does}
    → {module_b}.{function}()   # {transformation}
      → {module_c}.{function}() # {final step}
        → {output}
```

**Data transformation:**
- Input: `{type}` — {description}
- After step 1: `{type}` — {what changed}
- After step 2: `{type}` — {what changed}
- Output: `{type}` — {final form}

### LC2: {Chain Name}

**Purpose:** {what this chain accomplishes}

```
{flow description}
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
{module_a}
    └── imports → {module_b}
    └── imports → {module_c}
        └── imports → {module_d}
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `{package}` | {purpose} | `{file}` |
| `{package}` | {purpose} | `{file}` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| {state name} | `{file}:{var}` | {global/module/instance} | {when created/destroyed} |

### State Transitions

```
{state_a} ──{event}──▶ {state_b} ──{event}──▶ {state_c}
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. {what happens first}
2. {what happens next}
3. {system ready}
```

### Main Loop / Request Cycle

```
1. {trigger}
2. {processing}
3. {response}
```

### Shutdown

```
1. {cleanup step}
2. {final step}
```

---

## CONCURRENCY MODEL

{If applicable: threads, async, processes}

| Component | Model | Notes |
|-----------|-------|-------|
| {component} | {sync/async/threaded} | {considerations} |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `{key}` | `{file}` | `{value}` | {what it controls} |

---

## BIDIRECTIONAL LINKS

### Code → Docs

Files that reference this documentation:

| File | Line | Reference |
|------|------|-----------|
| `{file}` | {line} | `# DOCS: {path}` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM step 1 | `{file}:{function}` |
| ALGORITHM step 2 | `{file}:{function}` |
| BEHAVIOR B1 | `{file}:{function}` |
| VALIDATION V1 | `{test_file}:{test}` |

---

## GAPS / IDEAS / QUESTIONS

- [ ] {Missing implementation}
- [ ] {Technical debt}
- IDEA: {Architecture improvement}
- QUESTION: {Design uncertainty}
