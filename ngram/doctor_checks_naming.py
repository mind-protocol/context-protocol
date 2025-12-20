"""
Doctor check functions for naming conventions.

Health checks that verify:
- Documentation files use PREFIX_PascalCase_With_Underscores.md
- Code files use snake_case.py
- Directories use snake_case

DOCS: docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md
"""

import re
from pathlib import Path
from typing import List

from .doctor_types import DoctorIssue, DoctorConfig
from .doctor_files import should_ignore_path, find_source_files, find_code_directories

# Standard doc prefixes
STANDARD_DOC_PREFIXES = [
    "PATTERNS", "BEHAVIORS", "ALGORITHM", "VALIDATION",
    "IMPLEMENTATION", "TEST", "SYNC", "HEALTH", "CONCEPT", "TOUCHES"
]

def is_snake_case(name: str) -> bool:
    """Check if a name is snake_case, allowing for dunder files."""
    if name.startswith('__') and name.endswith('__'):
        inner = name[2:-2]
        return bool(re.match(r'^[a-z0-9]+(_[a-z0-9]+)*$', inner))
    return bool(re.match(r'^[a-z0-9]+(_[a-z0-9]+)*$', name))

def is_pascal_case_with_underscores(name: str) -> bool:
    """Check if a name is PascalCase (allowing acronyms) with underscores."""
    # Each part separated by underscore must start with uppercase
    parts = name.split('_')
    for part in parts:
        if not part:
            return False
        # Part must start with uppercase letter or number (e.g. 2D)
        if not (part[0].isupper() or part[0].isdigit()):
            return False
    return True

def doctor_check_naming_conventions(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for files and folders that violate naming conventions."""
    if "naming_conventions" in config.disabled_checks:
        return []

    violations = []

    # Check directories
    for code_dir in find_code_directories(target_dir, config):
        if should_ignore_path(code_dir, config.ignore, target_dir):
            continue

        if not is_snake_case(code_dir.name):
            try:
                rel_path = str(code_dir.relative_to(target_dir))
            except ValueError:
                rel_path = str(code_dir)
            violations.append({"path": rel_path, "type": "directory", "expected": "snake_case"})

    # Check source files (code)
    for source_file in find_source_files(target_dir, config):
        # Skip doc files (checked separately)
        if source_file.suffix.lower() == '.md':
            continue

        if not is_snake_case(source_file.stem):
            try:
                rel_path = str(source_file.relative_to(target_dir))
            except ValueError:
                rel_path = str(source_file)
            violations.append({"path": rel_path, "type": "code file", "expected": "snake_case"})

    # Check documentation files
    docs_dir = target_dir / "docs"
    if docs_dir.exists():
        for md_file in docs_dir.rglob("*.md"):
            if should_ignore_path(md_file, config.ignore, target_dir):
                continue

            name = md_file.stem
            if '_' not in name:
                try:
                    rel_path = str(md_file.relative_to(target_dir))
                except ValueError:
                    rel_path = str(md_file)
                violations.append({"path": rel_path, "type": "doc file", "expected": "PREFIX_Name.md"})
                continue

            prefix, rest = name.split('_', 1)
            # Prefix might be part of STANDARD_DOC_PREFIXES or just a generic prefix
            # The rule is PREFIX_PascalCase
            if not is_pascal_case_with_underscores(rest):
                try:
                    rel_path = str(md_file.relative_to(target_dir))
                except ValueError:
                    rel_path = str(md_file)
                violations.append({"path": rel_path, "type": "doc file", "expected": f"{prefix}_PascalCase_Name.md"})

    # Group violations into "tasks" of 10
    issues = []
    for i in range(0, len(violations), 10):
        group = violations[i:i+10]
        group_paths = [v["path"] for v in group]

        # Use the first path as the primary path for the issue
        primary_path = group[0]["path"]

        issues.append(DoctorIssue(
            issue_type="NAMING_CONVENTION",
            severity="warning",
            path=primary_path,
            message=f"Naming convention violations task ({i//10 + 1}): {len(group)} items",
            details={"violations": group},
            suggestion=f"Rename these files/folders to follow {group[0]['expected']}: {', '.join(group_paths[:3])}"
        ))

    return issues
