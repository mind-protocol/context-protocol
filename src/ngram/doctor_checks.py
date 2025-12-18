"""
Doctor check functions for ngram CLI.

All health check functions that examine the codebase for issues.
Each function returns a List[DoctorIssue].

DOCS: docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md
"""

import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Set

from .utils import IGNORED_EXTENSIONS, HAS_YAML, find_module_directories
from .doctor_types import DoctorIssue, DoctorConfig
from .doctor_files import (
    should_ignore_path,
    find_source_files,
    find_code_directories,
    count_lines,
    find_long_sections,
)

if HAS_YAML:
    import yaml

# Re-export functions from split modules for backwards compatibility
from .doctor_checks_quality import (
    doctor_check_magic_values,
    doctor_check_hardcoded_secrets,
)
from .doctor_checks_docs import (
    doctor_check_placeholder_docs,
    doctor_check_orphan_docs,
    doctor_check_stale_impl,
    doctor_check_large_doc_module,
    doctor_check_incomplete_chain,
)


def doctor_check_monolith(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for monolith files (too many lines)."""
    if "monolith" in config.disabled_checks:
        return []

    issues = []
    threshold = config.monolith_lines

    # Documentation files get a higher threshold (2x)
    doc_extensions = {'.md', '.txt', '.rst'}

    for source_file in find_source_files(target_dir, config):
        line_count = count_lines(source_file)

        # Use higher threshold for docs
        if source_file.suffix.lower() in doc_extensions:
            effective_threshold = threshold * 2
        else:
            effective_threshold = threshold

        if line_count > effective_threshold:
            try:
                rel_path = str(source_file.relative_to(target_dir))
            except ValueError:
                rel_path = str(source_file)

            # Find long sections for specific recommendations
            long_sections = find_long_sections(source_file, min_lines=50)

            # Build suggestion with specific targets
            if long_sections:
                top_sections = long_sections[:3]
                section_strs = [f"{s['kind']} {s['name']}() ({s['length']}L, :{s['line']})" for s in top_sections]
                suggestion = f"Split: {', '.join(section_strs)}"
            else:
                suggestion = "Consider splitting into smaller modules"

            issues.append(DoctorIssue(
                issue_type="MONOLITH",
                severity="critical",
                path=rel_path,
                message=f"{line_count} lines (threshold: {effective_threshold})",
                details={
                    "lines": line_count,
                    "threshold": effective_threshold,
                    "long_sections": long_sections,
                },
                suggestion=suggestion
            ))

    return issues


def doctor_check_undocumented(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for code directories without documentation."""
    if "undocumented" in config.disabled_checks:
        return []

    issues = []

    # Load modules.yaml if it exists
    manifest_path = target_dir / "modules.yaml"
    mapped_paths = set()

    if manifest_path.exists() and HAS_YAML:
        try:
            with open(manifest_path) as f:
                data = yaml.safe_load(f) or {}
            modules = data.get("modules", {})
            for module_data in modules.values():
                if isinstance(module_data, dict) and "code" in module_data:
                    # Extract base path from glob pattern
                    code_path = module_data["code"].replace("/**", "").replace("/*", "")
                    mapped_paths.add(code_path)
        except Exception:
            pass

    # Check each code directory
    for code_dir in find_code_directories(target_dir, config):
        if should_ignore_path(code_dir, config.ignore, target_dir):
            continue

        try:
            rel_path = str(code_dir.relative_to(target_dir))
        except ValueError:
            rel_path = str(code_dir)

        # Check if mapped
        is_mapped = False
        for mapped in mapped_paths:
            if rel_path.startswith(mapped) or mapped.startswith(rel_path):
                is_mapped = True
                break

        if not is_mapped:
            # Count files (excluding ignored dirs and junk files)
            file_count = sum(
                1 for f in code_dir.rglob("*")
                if f.is_file()
                and f.suffix.lower() not in IGNORED_EXTENSIONS
                and not should_ignore_path(f, config.ignore, target_dir)
            )

            issues.append(DoctorIssue(
                issue_type="UNDOCUMENTED",
                severity="critical",
                path=rel_path,
                message=f"No documentation mapping ({file_count} files)",
                details={"file_count": file_count},
                suggestion="Add mapping to modules.yaml"
            ))

    return issues


def doctor_check_stale_sync(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for stale SYNC files."""
    if "stale_sync" in config.disabled_checks:
        return []

    issues = []
    threshold_days = config.stale_sync_days
    threshold_date = datetime.now() - timedelta(days=threshold_days)

    # Find all SYNC files
    sync_files = []
    protocol_dir = target_dir / ".ngram"
    docs_dir = target_dir / "docs"

    if protocol_dir.exists():
        sync_files.extend(protocol_dir.rglob("SYNC_*.md"))
    if docs_dir.exists():
        sync_files.extend(docs_dir.rglob("SYNC_*.md"))

    for sync_file in sync_files:
        if should_ignore_path(sync_file, config.ignore, target_dir):
            continue

        try:
            content = sync_file.read_text()
        except Exception:
            continue

        # Parse LAST_UPDATED date
        last_updated = None
        for line in content.split('\n'):
            if 'LAST_UPDATED:' in line:
                date_str = line.split('LAST_UPDATED:')[1].strip()
                try:
                    last_updated = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    try:
                        last_updated = datetime.strptime(date_str[:10], "%Y-%m-%d")
                    except ValueError:
                        pass
                break

        if last_updated and last_updated < threshold_date:
            days_old = (datetime.now() - last_updated).days

            try:
                rel_path = str(sync_file.relative_to(target_dir))
            except ValueError:
                rel_path = str(sync_file)

            issues.append(DoctorIssue(
                issue_type="STALE_SYNC",
                severity="warning",
                path=rel_path,
                message=f"Last updated {days_old} days ago",
                details={"days_old": days_old, "last_updated": str(last_updated.date())},
                suggestion="Review and update SYNC with current state"
            ))

    return issues


# doctor_check_placeholder_docs moved to doctor_checks_docs.py


def doctor_check_no_docs_ref(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for source files without DOCS: reference."""
    if "no_docs_ref" in config.disabled_checks:
        return []

    issues = []
    # Match DOCS: in comments or docstrings
    docs_pattern = re.compile(r'#\s*DOCS:|//\s*DOCS:|/\*\s*DOCS:|^\s*DOCS:', re.MULTILINE)

    # Skip documentation files - DOCS: references only make sense in code
    doc_extensions = {'.md', '.txt', '.rst', '.html', '.css'}

    for source_file in find_source_files(target_dir, config):
        # Skip documentation files
        if source_file.suffix.lower() in doc_extensions:
            continue
        try:
            content = source_file.read_text()
        except Exception:
            continue

        # Only check files with substantial content
        if count_lines(source_file) < 50:
            continue

        if not docs_pattern.search(content[:config.docs_ref_search_chars]):
            try:
                rel_path = str(source_file.relative_to(target_dir))
            except ValueError:
                rel_path = str(source_file)

            issues.append(DoctorIssue(
                issue_type="NO_DOCS_REF",
                severity="info",
                path=rel_path,
                message="No DOCS: reference in file header",
                details={},
                suggestion="Add: # DOCS: path/to/PATTERNS.md"
            ))

    return issues


def extract_impl_file_refs(impl_path: Path) -> List[str]:
    """Extract file references from an IMPLEMENTATION doc."""
    try:
        content = impl_path.read_text()
    except Exception:
        return []

    refs = []
    # Match patterns like `path/to/file.py` or path/to/file.py in code blocks
    # Common patterns in IMPLEMENTATION docs

    # Match file paths in backticks or code blocks
    patterns = [
        r'`([^`]+\.\w+)`',  # `file.py`
        r'- `([^`]+)`',  # - `path/to/file`
        r'│\s+[├└]──\s+(\S+\.\w+)',  # Tree structure
        r'^\s*(\S+\.(?:py|ts|js|tsx|jsx|go|rs|java|rb))\s*[-—#]',  # file.py - description
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content, re.MULTILINE)
        refs.extend(matches)

    # Filter to likely file paths (contain extension, not too long)
    valid_refs = []
    for ref in refs:
        ref = ref.strip()
        if '.' in ref and len(ref) < 200 and not ref.startswith('http'):
            # Clean up common prefixes
            ref = ref.lstrip('./')
            valid_refs.append(ref)

    return list(set(valid_refs))


def doctor_check_broken_impl_links(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for IMPLEMENTATION docs that reference non-existent files."""
    if "broken_impl_links" in config.disabled_checks:
        return []

    issues = []
    docs_dir = target_dir / "docs"

    if not docs_dir.exists():
        return issues

    # Find all IMPLEMENTATION docs
    for impl_file in docs_dir.rglob("IMPLEMENTATION_*.md"):
        if should_ignore_path(impl_file, config.ignore, target_dir):
            continue

        file_refs = extract_impl_file_refs(impl_file)
        missing_files = []

        for ref in file_refs:
            # Try to find the file
            possible_paths = [
                target_dir / ref,
                target_dir / "src" / ref,
                target_dir / "engine" / ref,
                target_dir / "frontend" / ref,
            ]

            found = any(p.exists() for p in possible_paths)
            if not found:
                missing_files.append(ref)

        if missing_files:
            try:
                rel_path = str(impl_file.relative_to(target_dir))
            except ValueError:
                rel_path = str(impl_file)

            issues.append(DoctorIssue(
                issue_type="BROKEN_IMPL_LINK",
                severity="critical",
                path=rel_path,
                message=f"References {len(missing_files)} non-existent file(s)",
                details={"missing_files": missing_files[:10]},
                suggestion=f"Update or remove references: {', '.join(missing_files[:3])}"
            ))

    return issues


def detect_stub_patterns(content: str, suffix: str) -> List[Dict[str, Any]]:
    """Detect stub/placeholder patterns in code."""
    stubs = []

    if suffix in ['.py']:
        # Python: pass, NotImplementedError, ...
        patterns = [
            (r'def \w+\([^)]*\):\s*\n\s+pass\s*$', 'empty function with pass'),
            (r'def \w+\([^)]*\):\s*\n\s+\.\.\.', 'function with ellipsis'),
            (r'raise NotImplementedError', 'NotImplementedError'),
            (r'#\s*TODO[:\s]', 'TODO comment'),
            (r'#\s*FIXME[:\s]', 'FIXME comment'),
            (r'#\s*XXX[:\s]', 'XXX comment'),
            (r'#\s*STUB[:\s]', 'STUB comment'),
            (r'#\s*HACK[:\s]', 'HACK comment'),
        ]
    elif suffix in ['.js', '.ts', '.jsx', '.tsx']:
        # JS/TS
        patterns = [
            (r'function \w+\([^)]*\)\s*\{\s*\}', 'empty function'),
            (r'=>\s*\{\s*\}', 'empty arrow function'),
            (r'throw new Error\([\'"]not implemented', 'not implemented error'),
            (r'//\s*TODO[:\s]', 'TODO comment'),
            (r'//\s*FIXME[:\s]', 'FIXME comment'),
            (r'//\s*XXX[:\s]', 'XXX comment'),
        ]
    elif suffix in ['.go']:
        # Go
        patterns = [
            (r'func \w+\([^)]*\)\s*\{\s*\}', 'empty function'),
            (r'panic\([\'"]not implemented', 'not implemented panic'),
            (r'//\s*TODO[:\s]', 'TODO comment'),
        ]
    else:
        patterns = [
            (r'TODO[:\s]', 'TODO'),
            (r'FIXME[:\s]', 'FIXME'),
            (r'not implemented', 'not implemented'),
        ]

    for pattern, description in patterns:
        matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
        if matches:
            stubs.append({"pattern": description, "count": len(matches)})

    return stubs


def doctor_check_stub_impl(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for implementation files that are stubs (placeholder implementations)."""
    if "stub_impl" in config.disabled_checks:
        return []

    issues = []

    # Only check files that are referenced in IMPLEMENTATION docs or mapped in modules.yaml
    for source_file in find_source_files(target_dir, config):
        # Skip test files
        if 'test' in source_file.name.lower():
            continue

        try:
            content = source_file.read_text()
        except Exception:
            continue

        # Skip small files (likely config or simple modules)
        if len(content) < 100:
            continue

        stubs = detect_stub_patterns(content, source_file.suffix.lower())

        # Only report if significant stub presence
        total_stubs = sum(s["count"] for s in stubs)
        if total_stubs >= 3:  # At least 3 stub indicators
            try:
                rel_path = str(source_file.relative_to(target_dir))
            except ValueError:
                rel_path = str(source_file)

            stub_summary = ", ".join(f"{s['pattern']} ({s['count']})" for s in stubs[:3])

            issues.append(DoctorIssue(
                issue_type="STUB_IMPL",
                severity="warning",
                path=rel_path,
                message=f"Contains {total_stubs} stub indicators",
                details={"stubs": stubs, "total": total_stubs},
                suggestion=f"Implement: {stub_summary}"
            ))

    return issues


def find_empty_functions(file_path: Path) -> List[Dict[str, Any]]:
    """Find empty or incomplete functions in a file."""
    try:
        content = file_path.read_text()
        lines = content.split('\n')
    except Exception:
        return []

    empty_funcs = []
    suffix = file_path.suffix.lower()

    if suffix in ['.py']:
        # Find Python functions that only have pass, docstring, or are very short
        in_func = False
        func_name = ""
        func_start = 0
        func_indent = 0
        func_lines = []

        for i, line in enumerate(lines):
            # Detect function start
            match = re.match(r'^(\s*)(async\s+)?def\s+(\w+)', line)
            if match:
                # Check previous function
                if in_func and func_lines:
                    # Analyze function body
                    body = '\n'.join(func_lines)
                    body_stripped = re.sub(r'""".*?"""', '', body, flags=re.DOTALL)
                    body_stripped = re.sub(r"'''.*?'''", '', body_stripped, flags=re.DOTALL)
                    body_stripped = re.sub(r'#.*$', '', body_stripped, flags=re.MULTILINE)
                    body_lines = [l for l in body_stripped.split('\n') if l.strip()]

                    if len(body_lines) <= 2:  # Only pass/return/ellipsis
                        empty_funcs.append({
                            "name": func_name,
                            "line": func_start,
                            "reason": "empty or trivial body"
                        })

                in_func = True
                func_indent = len(match.group(1))
                func_name = match.group(3)
                func_start = i + 1
                func_lines = []
            elif in_func:
                # Check if we're still in the function
                if line.strip() and not line.startswith(' ' * (func_indent + 1)):
                    # Left function
                    # Check previous function
                    body = '\n'.join(func_lines)
                    body_stripped = re.sub(r'""".*?"""', '', body, flags=re.DOTALL)
                    body_stripped = re.sub(r"'''.*?'''", '', body_stripped, flags=re.DOTALL)
                    body_stripped = re.sub(r'#.*$', '', body_stripped, flags=re.MULTILINE)
                    body_lines = [l for l in body_stripped.split('\n') if l.strip()]

                    if len(body_lines) <= 2:
                        empty_funcs.append({
                            "name": func_name,
                            "line": func_start,
                            "reason": "empty or trivial body"
                        })
                    in_func = False
                else:
                    func_lines.append(line)

    return empty_funcs[:10]  # Limit to 10


def doctor_check_incomplete_impl(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for incomplete implementation files (empty functions, TODOs)."""
    if "incomplete_impl" in config.disabled_checks:
        return []

    issues = []

    for source_file in find_source_files(target_dir, config):
        # Skip test files
        if 'test' in source_file.name.lower():
            continue

        empty_funcs = find_empty_functions(source_file)

        if len(empty_funcs) >= 2:  # At least 2 empty functions
            try:
                rel_path = str(source_file.relative_to(target_dir))
            except ValueError:
                rel_path = str(source_file)

            func_names = [f["name"] for f in empty_funcs[:5]]

            issues.append(DoctorIssue(
                issue_type="INCOMPLETE_IMPL",
                severity="warning",
                path=rel_path,
                message=f"Contains {len(empty_funcs)} empty/incomplete function(s)",
                details={"empty_functions": empty_funcs},
                suggestion=f"Implement: {', '.join(func_names)}"
            ))

    return issues


def doctor_check_undoc_impl(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for implementation files not documented in any IMPLEMENTATION doc."""
    if "undoc_impl" in config.disabled_checks:
        return []

    issues = []
    docs_dir = target_dir / "docs"

    if not docs_dir.exists():
        return issues

    # Collect all file references from IMPLEMENTATION docs
    documented_files = set()
    for impl_file in docs_dir.rglob("IMPLEMENTATION_*.md"):
        refs = extract_impl_file_refs(impl_file)
        for ref in refs:
            # Normalize path
            documented_files.add(ref.lower())
            # Also add just the filename
            documented_files.add(Path(ref).name.lower())

    # Check source files
    for source_file in find_source_files(target_dir, config):
        # Skip test files
        if 'test' in source_file.name.lower():
            continue

        # Skip small files
        if count_lines(source_file) < 50:
            continue

        try:
            rel_path = str(source_file.relative_to(target_dir))
        except ValueError:
            rel_path = str(source_file)

        # Check if documented
        is_documented = (
            rel_path.lower() in documented_files or
            source_file.name.lower() in documented_files
        )

        if not is_documented:
            issues.append(DoctorIssue(
                issue_type="UNDOC_IMPL",
                severity="info",
                path=rel_path,
                message="Not referenced in any IMPLEMENTATION doc",
                details={},
                suggestion="Add to relevant IMPLEMENTATION_*.md"
            ))

    return issues


# doctor_check_new_undoc_code moved to doctor_checks_content.py


def doctor_check_yaml_drift(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    if "yaml_drift" in config.disabled_checks:
        return []

    issues = []
    manifest_path = target_dir / "modules.yaml"

    if not manifest_path.exists() or not HAS_YAML:
        return issues

    try:
        with open(manifest_path) as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        return issues

    modules = data.get("modules") or {}
    module_names = set(modules.keys())

    for module_name, module_data in modules.items():
        if not isinstance(module_data, dict):
            continue

        drift_issues = []

        # Check code path exists
        code_path = module_data.get("code", "")
        if code_path:
            # Remove glob patterns
            base_path = code_path.replace("/**", "").replace("/*", "").rstrip("/")
            if base_path and not (target_dir / base_path).exists():
                drift_issues.append(f"code path '{base_path}' not found")

        # Check docs path exists
        docs_path = module_data.get("docs", "")
        if docs_path:
            docs_path = docs_path.rstrip("/")
            if docs_path and not (target_dir / docs_path).exists():
                drift_issues.append(f"docs path '{docs_path}' not found")

        # Check tests path exists (if specified)
        tests_path = module_data.get("tests", "")
        if tests_path:
            base_tests = tests_path.replace("/**", "").replace("/*", "").rstrip("/")
            if base_tests and not (target_dir / base_tests).exists():
                drift_issues.append(f"tests path '{base_tests}' not found")

        # Check dependencies exist as modules
        depends_on = module_data.get("depends_on", [])
        if isinstance(depends_on, list):
            for dep in depends_on:
                if dep not in module_names:
                    drift_issues.append(f"dependency '{dep}' not defined")

        if drift_issues:
            issues.append(DoctorIssue(
                issue_type="YAML_DRIFT",
                severity="critical",
                path=f"modules.yaml#{module_name}",
                message=f"Module '{module_name}' has {len(drift_issues)} drift issue(s)",
                details={"module": module_name, "issues": drift_issues},
                suggestion="; ".join(drift_issues[:3])
            ))

    return issues


# doctor_check_large_doc_module moved to doctor_checks_docs.py
# doctor_check_incomplete_chain moved to doctor_checks_docs.py


def doctor_check_missing_tests(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for modules without tests."""
    issues = []

    if "MISSING_TESTS" in config.disabled_checks:
        return issues

    # Check modules.yaml for modules without tests
    modules_yaml = target_dir / "modules.yaml"
    if not modules_yaml.exists() or not HAS_YAML:
        return issues

    try:
        with open(modules_yaml) as f:
            data = yaml.safe_load(f) or {}

        for module_name, module_data in data.get("modules", {}).items():
            if not isinstance(module_data, dict):
                continue

            tests_path = module_data.get("tests")
            code_path = module_data.get("code")

            if not code_path:
                continue

            # Check if tests path exists
            if tests_path:
                test_dir = target_dir / tests_path.rstrip("/*")
                if test_dir.exists():
                    continue  # Has tests

            # No tests defined or path doesn't exist
            issues.append(DoctorIssue(
                issue_type="MISSING_TESTS",
                severity="info",
                path=module_name,
                message=f"No tests for module",
                details={"module": module_name, "code": code_path},
                suggestion="Add tests and update modules.yaml"
            ))

    except Exception:
        pass

    return issues


# doctor_check_orphan_docs moved to doctor_checks_docs.py

# doctor_check_conflicts, doctor_check_doc_gaps, doctor_check_suggestions
# moved to doctor_checks_sync.py

# doctor_check_doc_duplication moved to doctor_checks_content.py

# doctor_check_stale_impl moved to doctor_checks_docs.py
# doctor_check_magic_values moved to doctor_checks_quality.py
# doctor_check_hardcoded_secrets moved to doctor_checks_quality.py
# doctor_check_long_strings moved to doctor_checks_content.py
