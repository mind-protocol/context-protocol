"""
Doctor command for Context Protocol CLI.

Provides health checks for projects:
- Monolith files (too many lines)
- Undocumented code directories
- Stale SYNC files
- Placeholder documentation
- Missing DOCS: references
- Incomplete doc chains
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

from .utils import IGNORED_EXTENSIONS, HAS_YAML, find_module_directories
from .sync import archive_all_syncs
from .doctor_types import DoctorIssue, DoctorConfig
from .doctor_report import (
    get_issue_guidance,
    get_issue_explanation,
    generate_health_markdown,
    print_doctor_report,
    check_sync_status,
)

if HAS_YAML:
    import yaml


def parse_gitignore(gitignore_path: Path) -> List[str]:
    """Parse .gitignore file and return list of patterns."""
    patterns = []
    if not gitignore_path.exists():
        return patterns

    try:
        with open(gitignore_path) as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                # Normalize pattern for our matching
                if line.endswith('/'):
                    # Directory pattern - add /** suffix
                    patterns.append(line.rstrip('/') + "/**")
                else:
                    patterns.append(line)
    except Exception:
        pass

    return patterns


def load_doctor_config(target_dir: Path) -> DoctorConfig:
    """Load doctor configuration from config.yaml and .gitignore if they exist."""
    config_path = target_dir / ".context-protocol" / "config.yaml"
    gitignore_path = target_dir / ".gitignore"

    config = DoctorConfig()

    # Add patterns from .gitignore
    gitignore_patterns = parse_gitignore(gitignore_path)
    config.ignore.extend(gitignore_patterns)

    if not config_path.exists():
        return config

    if not HAS_YAML:
        return config

    try:
        with open(config_path) as f:
            data = yaml.safe_load(f) or {}

        doctor_config = data.get("doctor", {})

        if "monolith_lines" in doctor_config:
            config.monolith_lines = int(doctor_config["monolith_lines"])
        if "stale_sync_days" in doctor_config:
            config.stale_sync_days = int(doctor_config["stale_sync_days"])
        if "ignore" in doctor_config:
            # Extend defaults, don't replace
            config.ignore.extend(doctor_config["ignore"])
        if "disabled_checks" in doctor_config:
            config.disabled_checks = list(doctor_config["disabled_checks"])

    except Exception:
        pass  # Use defaults on error

    return config


def should_ignore_path(path: Path, ignore_patterns: List[str], target_dir: Path) -> bool:
    """Check if a path should be ignored based on patterns."""
    import fnmatch

    try:
        rel_path = str(path.relative_to(target_dir))
    except ValueError:
        rel_path = str(path)

    # Normalize path separators
    rel_path = rel_path.replace("\\", "/")

    for pattern in ignore_patterns:
        pattern = pattern.replace("\\", "/")

        # Pattern ending with /** means match this directory anywhere
        if pattern.endswith("/**"):
            dir_name = pattern[:-3]
            # Match if dir_name is a component in the path
            if f"/{dir_name}/" in f"/{rel_path}/" or rel_path.startswith(f"{dir_name}/"):
                return True

        # Pattern starting with **/ means match suffix
        elif pattern.startswith("**/"):
            suffix = pattern[3:]
            if rel_path.endswith(suffix) or f"/{suffix}" in f"/{rel_path}":
                return True

        # Simple wildcard patterns
        elif "*" in pattern:
            # Try matching with fnmatch
            if fnmatch.fnmatch(rel_path, pattern):
                return True
            # Also try matching just the filename
            if fnmatch.fnmatch(Path(rel_path).name, pattern):
                return True

        # Exact match or prefix
        else:
            if rel_path == pattern or rel_path.startswith(pattern + "/"):
                return True
            # Also match if pattern appears as a path component
            if f"/{pattern}/" in f"/{rel_path}/" or rel_path.startswith(f"{pattern}/"):
                return True

    return False


def is_binary_file(file_path: Path) -> bool:
    """Check if a file is binary."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(8192)
            return b'\x00' in chunk
    except Exception:
        return True


def find_source_files(target_dir: Path, config: DoctorConfig) -> List[Path]:
    """Find all source code files in the project."""
    files = set()

    # Check all code directories
    for code_dir in find_code_directories(target_dir, config):
        for file_path in code_dir.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() in IGNORED_EXTENSIONS:
                continue
            if should_ignore_path(file_path, config.ignore, target_dir):
                continue
            if is_binary_file(file_path):
                continue
            files.add(file_path)

    return sorted(files)


def find_code_directories(target_dir: Path, config: DoctorConfig) -> List[Path]:
    """Find leaf directories that contain source code files directly.

    Only returns directories that have code files DIRECTLY in them,
    not just subdirectories with code. This means:
    - src/context_protocol/ is returned (has .py files directly)
    - src/ is NOT returned (only has subdirectories)
    """
    skip_dirs = {'.git', '.context-protocol', 'docs', '__pycache__', '.venv', 'venv', 'templates', 'data'}
    found = []

    def has_direct_code_files(directory: Path) -> bool:
        """Check if directory has code files DIRECTLY in it (not in subdirs)."""
        for f in directory.iterdir():  # iterdir, not rglob
            if not f.is_file():
                continue
            if f.suffix.lower() in IGNORED_EXTENSIONS:
                continue
            if should_ignore_path(f, config.ignore, target_dir):
                continue
            # Check if it's a code file (not just any file)
            if f.suffix.lower() in {'.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.java', '.c', '.cpp', '.h', '.rb', '.php'}:
                return True
        return False

    def find_leaf_code_dirs(directory: Path, depth: int = 0) -> List[Path]:
        """Recursively find leaf directories with code files."""
        if depth > 5:  # Prevent infinite recursion
            return []

        results = []
        has_direct_code = has_direct_code_files(directory)

        # Check subdirectories
        subdirs_with_code = []
        for subdir in directory.iterdir():
            if not subdir.is_dir():
                continue
            if subdir.name.startswith('.'):
                continue
            if subdir.name in skip_dirs:
                continue
            if should_ignore_path(subdir, config.ignore, target_dir):
                continue

            # Recursively find code dirs in subdirectory
            sub_results = find_leaf_code_dirs(subdir, depth + 1)
            if sub_results:
                subdirs_with_code.extend(sub_results)

        # If this dir has direct code files AND no subdirs with code, it's a leaf
        # If this dir has direct code AND subdirs with code, include both
        if has_direct_code:
            results.append(directory)

        results.extend(subdirs_with_code)
        return results

    # Check all top-level directories
    for item in target_dir.iterdir():
        if not item.is_dir():
            continue
        if item.name.startswith('.'):
            continue
        if item.name in skip_dirs:
            continue
        if should_ignore_path(item, config.ignore, target_dir):
            continue

        found.extend(find_leaf_code_dirs(item))

    return found


def count_lines(file_path: Path) -> int:
    """Count non-empty lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for line in f if line.strip())
    except Exception:
        return 0


def find_long_sections(file_path: Path, min_lines: int = 50) -> List[Dict[str, Any]]:
    """Find long functions, classes, or sections in a file."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
    except Exception:
        return []

    sections = []
    suffix = file_path.suffix.lower()

    # Language-specific patterns
    if suffix in ['.py']:
        # Python: def, class, async def
        pattern = re.compile(r'^(\s*)(def |async def |class )(\w+)')
    elif suffix in ['.js', '.ts', '.jsx', '.tsx']:
        # JS/TS: function, class, const/let with arrow or function
        pattern = re.compile(r'^(\s*)(function |class |(?:const|let|var)\s+)(\w+)')
    elif suffix in ['.go']:
        # Go: func
        pattern = re.compile(r'^()(func\s+(?:\([^)]+\)\s+)?)(\w+)')
    elif suffix in ['.rs']:
        # Rust: fn, impl, struct
        pattern = re.compile(r'^(\s*)(fn |impl |struct )(\w+)')
    elif suffix in ['.java', '.kt']:
        # Java/Kotlin: class, interface, method patterns
        pattern = re.compile(r'^(\s*)(public |private |protected |class |interface |fun ).*?(\w+)\s*[({]')
    elif suffix in ['.rb']:
        # Ruby: def, class, module
        pattern = re.compile(r'^(\s*)(def |class |module )(\w+)')
    elif suffix in ['.md']:
        # Markdown: ## headers
        pattern = re.compile(r'^()(#{1,3}\s+)(.+)')
    else:
        return []  # Unsupported language

    # Find all section starts
    section_starts = []
    for i, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            indent = len(match.group(1))
            kind = match.group(2).strip()
            name = match.group(3)
            section_starts.append({
                "line": i + 1,
                "indent": indent,
                "kind": kind,
                "name": name,
            })

    # Calculate section lengths (until next section at same or lower indent)
    for i, section in enumerate(section_starts):
        start_line = section["line"]
        end_line = len(lines)

        # Find end: next section at same or lower indent level
        for j in range(i + 1, len(section_starts)):
            next_section = section_starts[j]
            if next_section["indent"] <= section["indent"]:
                end_line = next_section["line"] - 1
                break

        section["length"] = end_line - start_line + 1
        section["end_line"] = end_line

    # Filter to long sections and sort by length
    long_sections = [s for s in section_starts if s["length"] >= min_lines]
    long_sections.sort(key=lambda x: x["length"], reverse=True)

    return long_sections[:5]  # Top 5 longest


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
    protocol_dir = target_dir / ".context-protocol"
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


def doctor_check_placeholder_docs(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for docs with template placeholders."""
    if "placeholder" in config.disabled_checks:
        return []

    issues = []
    placeholder_pattern = re.compile(r'\{[A-Z][A-Z_]+\}')

    docs_dir = target_dir / "docs"
    protocol_dir = target_dir / ".context-protocol"

    search_dirs = []
    if docs_dir.exists():
        search_dirs.append(docs_dir)
    if protocol_dir.exists():
        search_dirs.append(protocol_dir)

    for search_dir in search_dirs:
        for md_file in search_dir.rglob("*.md"):
            if should_ignore_path(md_file, config.ignore, target_dir):
                continue

            # Skip template files - they're supposed to have placeholders
            if "template" in md_file.name.lower() or "/templates/" in str(md_file).lower():
                continue

            try:
                content = md_file.read_text()
            except Exception:
                continue

            # Skip code blocks and inline code when searching for placeholders
            lines = content.split('\n')
            in_code_block = False
            placeholders_found = []

            for line in lines:
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue

                if not in_code_block:
                    # Also skip inline code (text between backticks)
                    line_without_inline_code = re.sub(r'`[^`]+`', '', line)
                    matches = placeholder_pattern.findall(line_without_inline_code)
                    placeholders_found.extend(matches)

            if placeholders_found:
                try:
                    rel_path = str(md_file.relative_to(target_dir))
                except ValueError:
                    rel_path = str(md_file)

                # Filter common false positives
                real_placeholders = [p for p in placeholders_found
                                    if p not in ['{JSON}', '{XML}', '{HTML}', '{CSS}', '{TEMPLATE}', '{PLACEHOLDER}']]

                if real_placeholders:
                    issues.append(DoctorIssue(
                        issue_type="PLACEHOLDER",
                        severity="critical",
                        path=rel_path,
                        message=f"Contains {len(real_placeholders)} template placeholder(s)",
                        details={"placeholders": list(set(real_placeholders))[:5]},
                        suggestion="Fill in actual content"
                    ))

    return issues


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

        if not docs_pattern.search(content[:2000]):  # Check first 2000 chars
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
    import re

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


def doctor_check_yaml_drift(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for modules.yaml mappings that don't match reality."""
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


def doctor_check_large_doc_module(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for doc modules with too much content (hard to load in context)."""
    if "large_doc_module" in config.disabled_checks:
        return []

    issues = []
    docs_dir = target_dir / "docs"

    if not docs_dir.exists():
        return issues

    # Threshold: 50K chars is roughly 12K tokens, which is a lot for one module
    char_threshold = 50000

    modules = find_module_directories(docs_dir)

    for module_dir in modules:
        if should_ignore_path(module_dir, config.ignore, target_dir):
            continue

        total_chars = 0
        file_sizes = []

        for md_file in module_dir.glob("*.md"):
            try:
                content = md_file.read_text()
                size = len(content)
                total_chars += size
                file_sizes.append({"file": md_file.name, "chars": size})
            except Exception:
                continue

        if total_chars > char_threshold:
            try:
                rel_path = str(module_dir.relative_to(target_dir))
            except ValueError:
                rel_path = str(module_dir)

            # Sort by size to show largest files
            file_sizes.sort(key=lambda x: x["chars"], reverse=True)
            largest = [f"{f['file']} ({f['chars']//1000}K)" for f in file_sizes[:3]]

            issues.append(DoctorIssue(
                issue_type="LARGE_DOC_MODULE",
                severity="warning",
                path=rel_path,
                message=f"Total {total_chars//1000}K chars (threshold: {char_threshold//1000}K)",
                details={"total_chars": total_chars, "file_sizes": file_sizes},
                suggestion=f"Consider splitting. Largest: {', '.join(largest)}"
            ))

    return issues


def doctor_check_incomplete_chain(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for modules with incomplete doc chains."""
    if "incomplete_chain" in config.disabled_checks:
        return []

    issues = []
    docs_dir = target_dir / "docs"

    if not docs_dir.exists():
        return issues

    full_chain = ["PATTERNS_", "BEHAVIORS_", "ALGORITHM_", "VALIDATION_", "IMPLEMENTATION_", "TEST_", "SYNC_"]
    modules = find_module_directories(docs_dir)

    for module_dir in modules:
        if should_ignore_path(module_dir, config.ignore, target_dir):
            continue

        md_files = list(module_dir.glob("*.md"))

        missing = []
        for doc_type in full_chain:
            if not any(doc_type in f.name for f in md_files):
                missing.append(doc_type.rstrip('_'))

        if missing and len(missing) < 6:  # Not completely empty
            try:
                rel_path = str(module_dir.relative_to(target_dir))
            except ValueError:
                rel_path = str(module_dir)

            issues.append(DoctorIssue(
                issue_type="INCOMPLETE_CHAIN",
                severity="warning",
                path=rel_path,
                message=f"Missing: {', '.join(missing)}",
                details={"missing": missing, "present": [d.rstrip('_') for d in full_chain if d not in missing]},
                suggestion="Complete the doc chain for full coverage"
            ))

    return issues


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


def doctor_check_orphan_docs(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for docs not linked from code or modules.yaml."""
    issues = []

    if "ORPHAN_DOCS" in config.disabled_checks:
        return issues

    docs_dir = target_dir / "docs"
    if not docs_dir.exists():
        return issues

    # Get all doc files
    doc_files = set()
    for pattern in ["**/*.md"]:
        for f in docs_dir.glob(pattern):
            if f.is_file():
                doc_files.add(f.relative_to(target_dir))

    # Get docs referenced in modules.yaml
    referenced_docs = set()
    modules_yaml = target_dir / "modules.yaml"
    if modules_yaml.exists() and HAS_YAML:
        try:
            with open(modules_yaml) as f:
                data = yaml.safe_load(f) or {}
            for module_data in data.get("modules", {}).values():
                if isinstance(module_data, dict) and module_data.get("docs"):
                    docs_path = module_data["docs"].rstrip("/*")
                    # Add all files under this docs path
                    docs_subdir = target_dir / docs_path
                    if docs_subdir.exists():
                        for f in docs_subdir.glob("**/*.md"):
                            referenced_docs.add(f.relative_to(target_dir))
        except Exception:
            pass

    # Get docs referenced via DOCS: comments in code
    for code_ext in [".py", ".js", ".ts", ".tsx", ".go", ".rs"]:
        for code_file in target_dir.rglob(f"*{code_ext}"):
            if should_ignore_path(code_file, config.ignore, target_dir):
                continue
            try:
                content = code_file.read_text(errors="ignore")
                for line in content.split("\n")[:20]:  # Check first 20 lines
                    if "DOCS:" in line:
                        # Extract path after DOCS:
                        path_match = line.split("DOCS:")[-1].strip()
                        if path_match:
                            referenced_docs.add(Path(path_match))
            except Exception:
                pass

    # Find orphans
    orphan_docs = doc_files - referenced_docs
    for orphan in sorted(orphan_docs)[:10]:  # Limit to 10
        issues.append(DoctorIssue(
            issue_type="ORPHAN_DOCS",
            severity="info",
            path=str(orphan),
            message="Doc not linked from code or modules.yaml",
            details={},
            suggestion="Link from code, add to modules.yaml, or delete"
        ))

    return issues


def doctor_check_conflicts(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for CONFLICTS sections with ARBITRAGE items needing human decision."""
    issues = []

    if "ARBITRAGE" in config.disabled_checks:
        return issues

    # Search SYNC files for ## CONFLICTS sections
    search_paths = [
        target_dir / ".context-protocol" / "state",
        target_dir / "docs",
    ]

    for search_dir in search_paths:
        if not search_dir.exists():
            continue

        for sync_file in search_dir.rglob("SYNC_*.md"):
            if should_ignore_path(sync_file, config.ignore, target_dir):
                continue

            try:
                content = sync_file.read_text()

                # Look for ## CONFLICTS section
                if "## CONFLICTS" not in content and "## Conflicts" not in content:
                    continue

                # Extract ARBITRAGE items (unresolved conflicts needing human input)
                arbitrage_items = []
                in_conflicts_section = False
                current_item = None

                for line in content.split("\n"):
                    if line.strip().startswith("## CONFLICTS") or line.strip().startswith("## Conflicts"):
                        in_conflicts_section = True
                        continue
                    elif line.strip().startswith("## ") and in_conflicts_section:
                        # Left CONFLICTS section
                        break
                    elif in_conflicts_section:
                        # Look for ARBITRAGE headers
                        if "### ARBITRAGE:" in line or "### Arbitrage:" in line:
                            if current_item:
                                arbitrage_items.append(current_item)
                            current_item = {"title": line.split(":", 1)[-1].strip(), "details": []}
                        elif current_item and line.strip().startswith("-"):
                            current_item["details"].append(line.strip().lstrip("- "))
                        elif line.strip().startswith("### DECISION") or line.strip().startswith("### Decision"):
                            # DECISION items are resolved, skip
                            if current_item:
                                arbitrage_items.append(current_item)
                            current_item = None

                if current_item:
                    arbitrage_items.append(current_item)

                if arbitrage_items:
                    rel_path = str(sync_file.relative_to(target_dir))
                    issues.append(DoctorIssue(
                        issue_type="ARBITRAGE",
                        severity="critical",  # Needs human decision
                        path=rel_path,
                        message=f"{len(arbitrage_items)} conflict(s) need human decision",
                        details={
                            "conflicts": [item["title"] for item in arbitrage_items],
                            "items": arbitrage_items[:5],
                        },
                        suggestion=f"Decide: {arbitrage_items[0]['title']}" if arbitrage_items else ""
                    ))

            except Exception:
                pass

    return issues


def doctor_check_doc_gaps(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for GAPS sections left by previous agents in SYNC files."""
    issues = []

    if "DOC_GAPS" in config.disabled_checks:
        return issues

    # Search SYNC files for ## GAPS sections
    search_paths = [
        target_dir / ".context-protocol" / "state",
        target_dir / "docs",
    ]

    for search_dir in search_paths:
        if not search_dir.exists():
            continue

        for sync_file in search_dir.rglob("SYNC_*.md"):
            if should_ignore_path(sync_file, config.ignore, target_dir):
                continue

            try:
                content = sync_file.read_text()

                # Look for ## GAPS section
                if "## GAPS" not in content and "## Gaps" not in content:
                    continue

                # Extract uncompleted items ([ ] not [x])
                uncompleted = []
                in_gaps_section = False

                for line in content.split("\n"):
                    if line.strip().startswith("## GAPS") or line.strip().startswith("## Gaps"):
                        in_gaps_section = True
                        continue
                    elif line.strip().startswith("## ") and in_gaps_section:
                        # Left GAPS section
                        break
                    elif in_gaps_section:
                        # Look for uncompleted checkboxes
                        if "[ ]" in line:
                            # Extract the task text
                            task = line.split("[ ]")[-1].strip().lstrip("- ")
                            if task:
                                uncompleted.append(task)

                if uncompleted:
                    rel_path = str(sync_file.relative_to(target_dir))
                    issues.append(DoctorIssue(
                        issue_type="DOC_GAPS",
                        severity="warning",
                        path=rel_path,
                        message=f"{len(uncompleted)} incomplete task(s) from previous session",
                        details={"gaps": uncompleted[:10], "total": len(uncompleted)},
                        suggestion=f"Complete: {uncompleted[0][:50]}..." if uncompleted else ""
                    ))

            except Exception:
                pass

    return issues


def doctor_check_suggestions(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for agent suggestions in SYNC files that user can act on."""
    issues = []

    if "SUGGESTION" in config.disabled_checks:
        return issues

    # Search SYNC files for ### Suggestions sections
    search_paths = [
        target_dir / ".context-protocol" / "state",
        target_dir / "docs",
    ]

    for search_dir in search_paths:
        if not search_dir.exists():
            continue

        for sync_file in search_dir.rglob("SYNC_*.md"):
            if should_ignore_path(sync_file, config.ignore, target_dir):
                continue

            try:
                content = sync_file.read_text()

                # Look for ### Suggestions section
                if "### Suggestions" not in content and "### suggestions" not in content:
                    continue

                # Extract uncompleted suggestions ([ ] not [x])
                suggestions = []
                in_suggestions_section = False

                for line in content.split("\n"):
                    if line.strip().startswith("### Suggestions") or line.strip().startswith("### suggestions"):
                        in_suggestions_section = True
                        continue
                    elif line.strip().startswith("### ") and in_suggestions_section:
                        # Left Suggestions section
                        break
                    elif line.strip().startswith("## ") and in_suggestions_section:
                        # Left to new major section
                        break
                    elif in_suggestions_section:
                        # Look for uncompleted checkboxes
                        if "[ ]" in line:
                            # Extract the suggestion text
                            suggestion_text = line.split("[ ]")[-1].strip().lstrip("- ")
                            # Remove HTML comments
                            if "<!--" in suggestion_text:
                                suggestion_text = suggestion_text.split("<!--")[0].strip()
                            if suggestion_text:
                                suggestions.append(suggestion_text)

                if suggestions:
                    rel_path = str(sync_file.relative_to(target_dir))
                    for suggestion in suggestions:
                        issues.append(DoctorIssue(
                            issue_type="SUGGESTION",
                            severity="info",
                            path=rel_path,
                            message=f"Agent suggestion: {suggestion[:60]}{'...' if len(suggestion) > 60 else ''}",
                            details={"suggestion": suggestion, "source_file": rel_path},
                            suggestion=suggestion
                        ))

            except Exception:
                pass

    return issues


def doctor_check_stale_impl(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for IMPLEMENTATION docs that don't match actual files."""
    issues = []

    if "STALE_IMPL" in config.disabled_checks:
        return issues

    # Find all IMPLEMENTATION docs
    docs_dir = target_dir / "docs"
    if not docs_dir.exists():
        return issues

    for impl_doc in docs_dir.rglob("IMPLEMENTATION*.md"):
        if should_ignore_path(impl_doc, config.ignore, target_dir):
            continue

        try:
            content = impl_doc.read_text(errors="ignore")

            # Extract file references from the doc
            referenced_files = set()
            for line in content.split("\n"):
                # Look for file paths in backticks or table cells
                import re
                matches = re.findall(r'`([^`]+\.(?:py|js|ts|tsx|go|rs|java))`', line)
                for match in matches:
                    referenced_files.add(match)

            if not referenced_files:
                continue

            # Check which files exist
            missing_files = []
            for ref_file in referenced_files:
                # Try relative to target_dir
                full_path = target_dir / ref_file
                if not full_path.exists():
                    missing_files.append(ref_file)

            if missing_files and len(missing_files) < len(referenced_files):
                # Some files missing but not all (if all missing, doc might be for different project)
                rel_path = str(impl_doc.relative_to(target_dir))
                issues.append(DoctorIssue(
                    issue_type="STALE_IMPL",
                    severity="warning",
                    path=rel_path,
                    message=f"{len(missing_files)} referenced files not found",
                    details={"missing_files": missing_files[:5]},
                    suggestion="Update doc to match actual file structure"
                ))

        except Exception:
            pass

    return issues


def calculate_health_score(issues: Dict[str, List[DoctorIssue]]) -> int:
    """Calculate health score from issues."""
    score = 100

    score -= len(issues.get("critical", [])) * 10
    score -= len(issues.get("warning", [])) * 3
    score -= len(issues.get("info", [])) * 1

    return max(0, score)


def run_doctor(target_dir: Path, config: DoctorConfig) -> Dict[str, Any]:
    """Run all doctor checks and return results."""
    all_issues = []

    # Run checks
    all_issues.extend(doctor_check_monolith(target_dir, config))
    all_issues.extend(doctor_check_undocumented(target_dir, config))
    all_issues.extend(doctor_check_stale_sync(target_dir, config))
    all_issues.extend(doctor_check_placeholder_docs(target_dir, config))
    all_issues.extend(doctor_check_no_docs_ref(target_dir, config))
    all_issues.extend(doctor_check_incomplete_chain(target_dir, config))
    # Implementation checks
    all_issues.extend(doctor_check_broken_impl_links(target_dir, config))
    all_issues.extend(doctor_check_stub_impl(target_dir, config))
    all_issues.extend(doctor_check_incomplete_impl(target_dir, config))
    all_issues.extend(doctor_check_undoc_impl(target_dir, config))
    all_issues.extend(doctor_check_large_doc_module(target_dir, config))
    all_issues.extend(doctor_check_yaml_drift(target_dir, config))
    # New checks
    all_issues.extend(doctor_check_missing_tests(target_dir, config))
    all_issues.extend(doctor_check_orphan_docs(target_dir, config))
    all_issues.extend(doctor_check_stale_impl(target_dir, config))
    all_issues.extend(doctor_check_doc_gaps(target_dir, config))
    all_issues.extend(doctor_check_conflicts(target_dir, config))
    all_issues.extend(doctor_check_suggestions(target_dir, config))

    # Group by severity
    grouped = {
        "critical": [i for i in all_issues if i.severity == "critical"],
        "warning": [i for i in all_issues if i.severity == "warning"],
        "info": [i for i in all_issues if i.severity == "info"],
    }

    score = calculate_health_score(grouped)

    return {
        "project": str(target_dir),
        "score": score,
        "issues": grouped,
        "summary": {
            "critical": len(grouped["critical"]),
            "warning": len(grouped["warning"]),
            "info": len(grouped["info"]),
        }
    }


def doctor_command(
    target_dir: Path,
    output_format: str = "text",
    level: str = "all",
    no_save: bool = False,
    github: bool = False,
    github_max: int = 10,
) -> int:
    """Run the doctor command and return exit code."""
    # Auto-archive large SYNC files first (silent)
    archived = archive_all_syncs(target_dir, max_lines=200)

    config = load_doctor_config(target_dir)
    results = run_doctor(target_dir, config)

    # Filter by level if specified
    if level == "critical":
        results["issues"]["warning"] = []
        results["issues"]["info"] = []
        results["summary"]["warning"] = 0
        results["summary"]["info"] = 0
    elif level == "warning":
        results["issues"]["info"] = []
        results["summary"]["info"] = 0

    print_doctor_report(results, output_format)

    # Check SYNC status and recommend if needed (text format only)
    if output_format == "text":
        # Show archived files if any
        if archived:
            print()
            print(f"Auto-archived {len(archived)} large SYNC file(s)")

        sync_status = check_sync_status(target_dir)
        if sync_status["stale"] > 0 or sync_status["large"] > 0:
            print()
            print("SYNC Status:")
            if sync_status["stale"] > 0:
                print(f"  {sync_status['stale']} stale SYNC file(s)")
            if sync_status["large"] > 0:
                print(f"  {sync_status['large']} large SYNC file(s) (>200 lines)")
            print()
            print("  Run: context-protocol sync")

    # Create GitHub issues if requested
    github_issues = []
    if github and output_format == "text":
        print()
        print("Creating GitHub issues...")
        try:
            from .github import create_issues_for_findings
            all_issues = results["issues"]["critical"] + results["issues"]["warning"]
            github_issues = create_issues_for_findings(all_issues, target_dir, max_issues=github_max)
            if github_issues:
                print(f"  Created {len(github_issues)} issue(s)")
                # Store mapping for repair command
                results["github_issues"] = {
                    issue.path: {"number": issue.number, "url": issue.url}
                    for issue in github_issues
                }
        except Exception as e:
            print(f"  Failed to create issues: {e}")

    # Save GitHub issue mapping for repair command
    if github_issues:
        mapping_path = target_dir / ".context-protocol" / "state" / "github_issues.json"
        if mapping_path.parent.exists():
            mapping_data = {
                issue.path: {"number": issue.number, "url": issue.url, "type": issue.issue_type}
                for issue in github_issues
            }
            mapping_path.write_text(json.dumps(mapping_data, indent=2))

    # Save to SYNC_Project_Health.md by default (unless --no-save or json output)
    if not no_save and output_format != "json":
        health_path = target_dir / ".context-protocol" / "state" / "SYNC_Project_Health.md"
        if health_path.parent.exists():
            health_content = generate_health_markdown(results, github_issues)
            health_path.write_text(health_content)
            print()
            print(f"Saved to {health_path.relative_to(target_dir)}")

    # Exit code: 1 if critical issues
    return 1 if results["issues"]["critical"] else 0
