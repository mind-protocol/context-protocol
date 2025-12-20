"""
Doctor check functions for documentation analysis.

Health checks that analyze documentation quality:
- Placeholder docs with template markers
- Orphan docs not linked from code
- Stale IMPLEMENTATION docs
- Large doc modules
- Incomplete doc chains

DOCS: docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md
"""

import re
from datetime import date
from pathlib import Path
from typing import List

from .utils import find_module_directories
from .doctor_types import DoctorIssue, DoctorConfig
from .doctor_files import should_ignore_path, parse_doctor_doc_tags

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def doctor_check_placeholder_docs(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for docs with template placeholders."""
    if "placeholder" in config.disabled_checks:
        return []

    issues = []
    placeholder_pattern = re.compile(r'\{[A-Z][A-Z_]+\}')

    docs_dir = target_dir / "docs"
    protocol_dir = target_dir / ".ngram"

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

    full_chain = ["PATTERNS_", "BEHAVIORS_", "ALGORITHM_", "VALIDATION_", "IMPLEMENTATION_", "HEALTH_", "SYNC_"]
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


DOC_TYPE_TEMPLATES = {
    "PATTERNS": ".ngram/templates/PATTERNS_TEMPLATE.md",
    "BEHAVIORS": ".ngram/templates/BEHAVIORS_TEMPLATE.md",
    "ALGORITHM": ".ngram/templates/ALGORITHM_TEMPLATE.md",
    "VALIDATION": ".ngram/templates/VALIDATION_TEMPLATE.md",
    "IMPLEMENTATION": ".ngram/templates/IMPLEMENTATION_TEMPLATE.md",
    "HEALTH": ".ngram/templates/HEALTH_TEMPLATE.md",
    "SYNC": ".ngram/templates/SYNC_TEMPLATE.md",
    "CONCEPT": ".ngram/templates/CONCEPT_TEMPLATE.md",
    "TOUCHES": ".ngram/templates/TOUCHES_TEMPLATE.md",
}

STANDARD_DOC_PREFIXES = tuple(f"{prefix}_" for prefix in DOC_TYPE_TEMPLATES.keys())


def _iter_doc_files(target_dir: Path, config: DoctorConfig) -> List[Path]:
    """Collect doc files from standard documentation roots."""
    doc_files: List[Path] = []
    search_dirs = [target_dir / "docs", target_dir / ".ngram" / "state"]

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for md_file in search_dir.rglob("*.md"):
            if should_ignore_path(md_file, config.ignore, target_dir):
                continue
            doc_files.append(md_file)

    return doc_files


def _extract_h2_sections(content: str) -> dict:
    """Extract H2 sections and their content."""
    sections = {}
    current = None
    buffer: List[str] = []

    for line in content.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = line[3:].strip()
            buffer = []
        elif current is not None:
            buffer.append(line)

    if current is not None:
        sections[current] = "\n".join(buffer).strip()

    return sections


def _doc_tag_allows_suppression(
    doc_path: Path,
    issue_type: str,
    allowed_statuses: set,
) -> bool:
    """Check if a doc tag suppresses an issue for now."""
    tags = parse_doctor_doc_tags(doc_path).get(issue_type, [])
    today = date.today()

    for tag in tags:
        status = tag.get("status", "")
        if status not in allowed_statuses:
            continue

        if status == "postponed":
            date_str = tag.get("date", "")
            if not date_str:
                continue
            try:
                postpone_until = date.fromisoformat(date_str)
            except ValueError:
                continue
            if postpone_until >= today:
                return True
            continue

        return True

    return False


def _doc_tag_message(doc_path: Path, issue_type: str, status: str) -> str:
    """Return the first matching tag message for an issue type/status."""
    tags = parse_doctor_doc_tags(doc_path).get(issue_type, [])
    for tag in tags:
        if tag.get("status") == status:
            return tag.get("message", "")
    return ""


def doctor_check_doc_template_drift(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check docs against their templates for missing or too-short sections."""
    if "DOC_TEMPLATE_DRIFT" in config.disabled_checks:
        return []

    issues = []
    template_sections_cache = {}

    for doc_path in _iter_doc_files(target_dir, config):
        prefix = doc_path.name.split("_", 1)[0]
        template_path = DOC_TYPE_TEMPLATES.get(prefix)
        if not template_path:
            continue

        if _doc_tag_allows_suppression(doc_path, "DOC_TEMPLATE_DRIFT", {"postponed", "non-required"}):
            continue

        if prefix not in template_sections_cache:
            template_file = target_dir / template_path
            if not template_file.exists():
                template_sections_cache[prefix] = []
            else:
                template_content = template_file.read_text(errors="ignore")
                template_sections_cache[prefix] = list(_extract_h2_sections(template_content).keys())

        required_sections = template_sections_cache[prefix]
        if not required_sections:
            continue

        doc_content = doc_path.read_text(errors="ignore")
        doc_sections = _extract_h2_sections(doc_content)

        missing = [section for section in required_sections if section not in doc_sections]
        short = [
            section for section in required_sections
            if section in doc_sections and len(doc_sections[section].strip()) < 50
        ]

        escalation_note = ""
        if missing:
            escalation_note = _doc_tag_message(doc_path, "DOC_TEMPLATE_DRIFT", "escalation")

        if missing or short:
            rel_path = str(doc_path.relative_to(target_dir))
            message_parts = []
            if missing:
                message_parts.append(f"Missing: {', '.join(missing)}")
            if short:
                message_parts.append(f"Too short: {', '.join(short)}")
            if escalation_note:
                message_parts.append(f"Escalation: {escalation_note}")

            issues.append(DoctorIssue(
                issue_type="DOC_TEMPLATE_DRIFT",
                severity="warning",
                path=rel_path,
                message="; ".join(message_parts),
                details={"missing": missing, "short": short},
                suggestion="Fill missing sections and expand short ones to 50+ characters"
            ))

    return issues


def doctor_check_nonstandard_doc_type(target_dir: Path, config: DoctorConfig) -> List[DoctorIssue]:
    """Check for docs that don't use standard doc type prefixes."""
    if "NON_STANDARD_DOC_TYPE" in config.disabled_checks:
        return []

    issues = []

    for doc_path in _iter_doc_files(target_dir, config):
        if doc_path.name.startswith(STANDARD_DOC_PREFIXES):
            continue

        if _doc_tag_allows_suppression(doc_path, "NON_STANDARD_DOC_TYPE", {"postponed", "exception"}):
            continue

        rel_path = str(doc_path.relative_to(target_dir))
        issues.append(DoctorIssue(
            issue_type="NON_STANDARD_DOC_TYPE",
            severity="warning",
            path=rel_path,
            message="Doc filename does not use a standard prefix",
            details={"prefixes": list(STANDARD_DOC_PREFIXES)},
            suggestion="Rename to PATTERNS_/BEHAVIORS_/ALGORITHM_/VALIDATION_/IMPLEMENTATION_/HEALTH_/SYNC_"
        ))

    return issues
