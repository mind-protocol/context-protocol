# ALGORITHM: Project Health Doctor

**Step-by-step procedures for health checks.**

---

## MAIN FLOW

```
doctor(project_dir, options):
    1. Load configuration
    2. Discover project structure
    3. Run enabled checks
    4. Aggregate results
    5. Calculate score
    6. Generate output
    7. Return exit code
```

---

## 1. LOAD CONFIGURATION

```python
def load_config(project_dir: Path) -> DoctorConfig:
    config_path = project_dir / ".add-framework" / "config.yaml"

    defaults = {
        "monolith_lines": 500,
        "god_function_lines": 100,
        "stale_sync_days": 14,
        "designing_stuck_days": 21,
        "nesting_depth": 4,
        "ignore": [],
        "disabled_checks": [],
        "severity_overrides": {}
    }

    if config_path.exists():
        user_config = yaml.load(config_path)
        return merge(defaults, user_config.get("doctor", {}))

    return defaults
```

---

## 2. DISCOVER PROJECT STRUCTURE

```python
def discover_project(project_dir: Path) -> ProjectStructure:
    return ProjectStructure(
        code_dirs = find_code_directories(project_dir),
        doc_dirs = find_doc_directories(project_dir),
        modules = load_modules_yaml(project_dir),
        sync_files = find_sync_files(project_dir),
        source_files = find_source_files(project_dir)
    )
```

### Find Code Directories

```python
def find_code_directories(project_dir: Path) -> List[Path]:
    """Find directories likely containing source code."""
    candidates = ["src", "lib", "app", "pkg", "components", "modules"]
    found = []

    for candidate in candidates:
        path = project_dir / candidate
        if path.exists() and path.is_dir():
            found.append(path)
            # Also find subdirectories
            for subdir in path.iterdir():
                if subdir.is_dir() and not subdir.name.startswith('.'):
                    found.append(subdir)

    return found
```

---

## 3. RUN CHECKS

Each check returns a list of issues:

```python
@dataclass
class Issue:
    type: str           # MONOLITH, STALE_SYNC, etc.
    severity: str       # critical, warning, info
    path: str           # Affected file/directory
    message: str        # Human description
    details: dict       # Type-specific data
    suggestion: str     # How to fix
```

### Check: Monolith Files

```python
def check_monolith(project: ProjectStructure, config: DoctorConfig) -> List[Issue]:
    issues = []
    threshold = config["monolith_lines"]

    for source_file in project.source_files:
        if should_ignore(source_file, config["ignore"]):
            continue

        line_count = count_lines(source_file)

        if line_count > threshold:
            issues.append(Issue(
                type="MONOLITH",
                severity="critical",
                path=str(source_file),
                message=f"{line_count} lines (threshold: {threshold})",
                details={"lines": line_count, "threshold": threshold},
                suggestion=suggest_split(source_file)
            ))

    return issues
```

### Check: Undocumented Code

```python
def check_undocumented(project: ProjectStructure, config: DoctorConfig) -> List[Issue]:
    issues = []

    for code_dir in project.code_dirs:
        # Check if mapped in modules.yaml
        mapping = find_mapping(code_dir, project.modules)

        if mapping is None:
            issues.append(Issue(
                type="UNDOCUMENTED",
                severity="critical",
                path=str(code_dir),
                message="No documentation exists",
                details={"files": count_files(code_dir)},
                suggestion=f"Create docs and add to modules.yaml"
            ))
        elif not Path(mapping["docs"]).exists():
            issues.append(Issue(
                type="MISSING_DOCS",
                severity="critical",
                path=str(code_dir),
                message=f"Mapped to {mapping['docs']} but path doesn't exist",
                details={"mapped_to": mapping["docs"]},
                suggestion=f"Create {mapping['docs']} or fix mapping"
            ))

    return issues
```

### Check: Stale SYNC

```python
def check_stale_sync(project: ProjectStructure, config: DoctorConfig) -> List[Issue]:
    issues = []
    threshold_days = config["stale_sync_days"]
    threshold = datetime.now() - timedelta(days=threshold_days)

    for sync_file in project.sync_files:
        last_updated = parse_sync_date(sync_file)

        if last_updated and last_updated < threshold:
            days_old = (datetime.now() - last_updated).days
            commits_since = count_commits_since(sync_file.parent, last_updated)

            issues.append(Issue(
                type="STALE_SYNC",
                severity="warning",
                path=str(sync_file),
                message=f"Last updated {days_old} days ago, {commits_since} commits since",
                details={"days": days_old, "commits": commits_since},
                suggestion="Review and update SYNC with current state"
            ))

    return issues
```

### Check: Placeholder Docs

```python
def check_placeholder_docs(project: ProjectStructure, config: DoctorConfig) -> List[Issue]:
    issues = []
    placeholder_patterns = ["{", "TODO:", "FIXME:", "XXX:"]

    for doc_file in project.doc_dirs.glob("**/*.md"):
        content = doc_file.read_text()

        # Check for template placeholders
        if re.search(r'\{[A-Z_]+\}', content):
            issues.append(Issue(
                type="PLACEHOLDER",
                severity="critical",
                path=str(doc_file),
                message="Contains template placeholders",
                details={"placeholders": find_placeholders(content)},
                suggestion="Fill in actual content"
            ))

    return issues
```

### Check: No DOCS Reference

```python
def check_no_docs_ref(project: ProjectStructure, config: DoctorConfig) -> List[Issue]:
    issues = []

    for source_file in project.source_files:
        if should_ignore(source_file, config["ignore"]):
            continue

        content = source_file.read_text()

        # Look for DOCS: comment
        if not re.search(r'#\s*DOCS:', content) and \
           not re.search(r'//\s*DOCS:', content):
            issues.append(Issue(
                type="NO_DOCS_REF",
                severity="warning",
                path=str(source_file),
                message="No DOCS: reference comment",
                details={},
                suggestion="Add: # DOCS: path/to/PATTERNS.md"
            ))

    return issues
```

### Check: Incomplete Chain

```python
def check_incomplete_chain(project: ProjectStructure, config: DoctorConfig) -> List[Issue]:
    issues = []
    required_types = ["PATTERNS", "BEHAVIORS", "ALGORITHM", "VALIDATION", "TEST", "SYNC"]

    for doc_dir in find_module_doc_dirs(project):
        present = set()
        for doc_file in doc_dir.glob("*.md"):
            for doc_type in required_types:
                if doc_file.name.startswith(doc_type):
                    present.add(doc_type)

        missing = set(required_types) - present

        if missing:
            issues.append(Issue(
                type="INCOMPLETE_CHAIN",
                severity="warning",
                path=str(doc_dir),
                message=f"Missing: {', '.join(sorted(missing))}",
                details={"missing": list(missing), "present": list(present)},
                suggestion="Create missing docs or mark as intentionally skipped"
            ))

    return issues
```

### Check: Activity Gaps

```python
def check_activity_gaps(project: ProjectStructure, config: DoctorConfig) -> List[Issue]:
    """Detect periods of no SYNC updates across the project."""
    issues = []
    threshold_days = config.get("activity_gap_days", 14)
    threshold = datetime.now() - timedelta(days=threshold_days)

    # Find most recent SYNC update across all SYNC files
    most_recent = None
    for sync_file in project.sync_files:
        last_updated = parse_sync_date(sync_file)
        if last_updated and (most_recent is None or last_updated > most_recent):
            most_recent = last_updated

    if most_recent and most_recent < threshold:
        days_silent = (datetime.now() - most_recent).days
        issues.append(Issue(
            type="ACTIVITY_GAP",
            severity="warning",
            path=".add-framework/",
            message=f"No SYNC updates in {days_silent} days",
            details={"days_silent": days_silent, "last_activity": str(most_recent.date())},
            suggestion="Review project state and update relevant SYNC files"
        ))

    return issues
```

### Check: Abandoned Areas

```python
def check_abandoned_areas(project: ProjectStructure, config: DoctorConfig) -> List[Issue]:
    """Find documentation that was started but never completed."""
    issues = []
    threshold_days = config.get("abandoned_days", 30)
    threshold = datetime.now() - timedelta(days=threshold_days)

    for doc_dir in find_module_doc_dirs(project):
        docs = list(doc_dir.glob("*.md"))

        # Skip if no docs at all (that's UNDOCUMENTED, not ABANDONED)
        if not docs:
            continue

        # Check if only has PATTERNS or SYNC (started but not continued)
        doc_types = set()
        for doc in docs:
            for prefix in ["PATTERNS_", "BEHAVIORS_", "ALGORITHM_", "VALIDATION_", "TEST_", "SYNC_"]:
                if doc.name.startswith(prefix):
                    doc_types.add(prefix.rstrip("_"))

        # Started (has 1-2 docs) but incomplete (missing 3+ docs)
        if 1 <= len(doc_types) <= 2:
            # Check if stale
            newest_mod = max(doc.stat().st_mtime for doc in docs)
            newest_date = datetime.fromtimestamp(newest_mod)

            if newest_date < threshold:
                days_stale = (datetime.now() - newest_date).days
                issues.append(Issue(
                    type="ABANDONED",
                    severity="warning",
                    path=str(doc_dir),
                    message=f"Started {days_stale} days ago, only has {', '.join(doc_types)}",
                    details={
                        "present": list(doc_types),
                        "days_stale": days_stale
                    },
                    suggestion="Either complete documentation or remove if no longer relevant"
                ))

    return issues
```

### Check: Vague Names

```python
def check_vague_names(project: ProjectStructure, config: DoctorConfig) -> List[Issue]:
    """Flag files/directories with non-descriptive names."""
    issues = []

    vague_patterns = {
        "utils": "Consider naming by what it actually does (e.g., string_helpers, date_formatters)",
        "helpers": "Consider naming by domain (e.g., auth_helpers, payment_utils)",
        "misc": "Split into specific, named modules",
        "stuff": "Rename to describe actual contents",
        "common": "Consider naming by what's common (e.g., shared_types, base_classes)",
        "lib": "Consider more specific names for subdirectories",
        "core": "Consider what 'core' means in this context",
        "base": "Consider naming by what it's a base for",
        "general": "Split into specific concerns",
        "other": "Categorize contents properly",
    }

    # Check directories
    for code_dir in project.code_dirs:
        dir_name = code_dir.name.lower()
        if dir_name in vague_patterns:
            issues.append(Issue(
                type="VAGUE_NAME",
                severity="info",
                path=str(code_dir),
                message=f"Directory named '{code_dir.name}' is non-descriptive",
                details={"name": code_dir.name, "type": "directory"},
                suggestion=vague_patterns[dir_name]
            ))

    # Check files
    for source_file in project.source_files:
        file_stem = source_file.stem.lower()
        if file_stem in vague_patterns:
            issues.append(Issue(
                type="VAGUE_NAME",
                severity="info",
                path=str(source_file),
                message=f"File named '{source_file.name}' is non-descriptive",
                details={"name": source_file.name, "type": "file"},
                suggestion=vague_patterns[file_stem]
            ))

    return issues
```

---

## 4. AGGREGATE RESULTS

```python
def aggregate_results(all_issues: List[Issue], config: DoctorConfig) -> Dict:
    # Apply severity overrides
    for issue in all_issues:
        if issue.type in config["severity_overrides"]:
            issue.severity = config["severity_overrides"][issue.type]

    # Group by severity
    return {
        "critical": [i for i in all_issues if i.severity == "critical"],
        "warning": [i for i in all_issues if i.severity == "warning"],
        "info": [i for i in all_issues if i.severity == "info"]
    }
```

---

## 5. CALCULATE SCORE

```python
def calculate_score(results: Dict) -> int:
    score = 100

    score -= len(results["critical"]) * 10
    score -= len(results["warning"]) * 3
    score -= len(results["info"]) * 1

    return max(0, score)
```

---

## 6. GENERATE OUTPUT

```python
def generate_output(results: Dict, score: int, format: str) -> str:
    if format == "json":
        return json.dumps({
            "score": score,
            "issues": results,
            "summary": {k: len(v) for k, v in results.items()}
        })
    elif format == "markdown":
        return render_markdown_report(results, score)
    else:  # text
        return render_text_report(results, score)
```

---

## 7. EXIT CODE

```python
def get_exit_code(results: Dict) -> int:
    if results["critical"]:
        return 1
    return 0
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Project_Health_Doctor.md
BEHAVIORS:       ./BEHAVIORS_Project_Health_Doctor.md
ALGORITHM:       THIS
VALIDATION:      ./VALIDATION_Project_Health_Doctor.md
IMPLEMENTATION:  ./IMPLEMENTATION_Project_Health_Doctor.md
TEST:            ./TEST_Project_Health_Doctor.md
SYNC:            ./SYNC_Project_Health_Doctor.md
```
