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
IGNORED_FILES = {
    "ngram/solve_escalations.py",
    "docs/cli/ALGORITHM_CLI_Logic.md",
}


def _is_log_file(path: Path) -> bool:
    return path.suffix == ".log" or path.name.endswith(".log")


def find_escalation_markers(target_dir: Path) -> List[str]:
    """Return escalation file paths ordered by priority and importance."""
    config = load_doctor_config(target_dir)
    matches: List[Tuple[int, int, str]] = []

    for path in target_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            rel_path = str(path.relative_to(target_dir))
        except ValueError:
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

        if not any(tag in content for tag in ESCALATION_TAGS):
            continue

        doc_priority = 0 if "@ngram:doctor:escalation" in content else 1
        occurrences = sum(content.count(tag) for tag in ESCALATION_TAGS)
        matches.append((doc_priority, -occurrences, rel_path))

    matches.sort()
    return [path for _, _, path in matches]


def solve_escalations_command(target_dir: Path) -> int:
    """CLI entrypoint for `ngram solve-escalations`."""
    escalation_files = find_escalation_markers(target_dir)

    if not escalation_files:
        print("No escalation markers found.")
        return 0

    print("Escalation markers (priority order):")
    for idx, path in enumerate(escalation_files, 1):
        print(f"  {idx}. {path}")

    print("\nPlease review these escalation markers and provide decisions.")
    print("After resolving, fill the `response` field in the existing escalation YAML.")
    return 0
