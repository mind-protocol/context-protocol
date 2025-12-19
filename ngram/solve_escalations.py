# DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md
"""
Scan the repo for escalation markers and report them.
"""

from pathlib import Path
from typing import List, Tuple

from .doctor_files import load_doctor_config, should_ignore_path, is_binary_file

ESCALATION_TAGS = (
    "@ngram:doctor:escalation",
    "@ngram:escalation",
)

PROPOSITION_TAGS = (
    "@ngram:doctor:proposition",
    "@ngram:proposition",
)
IGNORED_FILES = {
    "ngram/solve_escalations.py",
    "docs/cli/ALGORITHM_CLI_Logic.md",
}


def _is_log_file(path: Path) -> bool:
    return path.suffix == ".log" or path.name.endswith(".log")


def _find_markers_in_files(target_dir: Path, marker_tags: Tuple[str, ...], issue_type: str) -> List[Tuple[int, int, str, str]]:
    """Return file paths with given markers, ordered by priority and importance."""
    config = load_doctor_config(target_dir)
    matches: List[Tuple[int, int, str, str]] = []

    # Directories to ignore (examples, internal docs)
    ignore_dirs = {
        "templates/ngram/views",
        ".ngram/views",
    }

    for path in target_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            rel_path = str(path.relative_to(target_dir))
        except ValueError:
            continue
        
        # Skip ignore dirs
        if any(rel_path.startswith(d) for d in ignore_dirs):
            continue

        if rel_path in IGNORED_FILES:
            continue
        if should_ignore_path(path, config.ignore, target_dir):
            continue
        if _is_log_file(path):
            continue
        if is_binary_file(path):
            continue

        try:
            content = path.read_text(errors="ignore")
        except Exception:
            continue

        if not any(tag in content for tag in marker_tags):
            continue

        # Higher priority for explicit @ngram:doctor tags
        doc_priority = 0 if any(f"@ngram:doctor:{issue_type.lower()}" in content for issue_type in marker_tags) else 1
        occurrences = sum(content.count(tag) for tag in marker_tags)
        matches.append((doc_priority, -occurrences, rel_path, issue_type))

    matches.sort()
    return matches


def solve_special_markers_command(target_dir: Path) -> int:
    """CLI entrypoint for `ngram solve-markers` to find and report special markers."""
    escalation_matches = _find_markers_in_files(target_dir, ESCALATION_TAGS, "ESCALATION")
    proposition_matches = _find_markers_in_files(target_dir, PROPOSITION_TAGS, "PROPOSITION")

    all_matches = sorted(escalation_matches + proposition_matches)

    if not all_matches:
        print("No special markers found.")
        return 0

    print("Special markers (priority order):")
    for idx, (doc_prio, occ, path, issue_type) in enumerate(all_matches, 1):
        print(f"  {idx}. [{issue_type}] {path}")

    print("\nPlease review these markers and provide decisions or consider implementing propositions.")
    print("After resolving, fill the `response` field in the existing escalation/proposition YAML.")
    return 0
