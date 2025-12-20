#!/usr/bin/env python3
"""
Blood Ledger Terminology Linter

Fixes terminology issues in the codebase:
1. Replaces "player" in node attributes with actual player character name
2. Replaces "NPC/npc" with "character/s" in code and docs

Usage:
    python lint_terminology.py [--fix] [--player-name NAME] [--graph NAME]

    --fix           Apply fixes (default: dry-run, just report)
    --player-name   Override player character name (default: fetch from graph)
    --graph         Graph name to query (default: blood_ledger)
"""

# DOCS: docs/schema/graph-health/PATTERNS_Graph_Health_Validation.md

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


def get_player_name_from_graph(graph_name: str = "blood_ledger") -> Optional[str]:
    """Fetch the player character name from FalkorDB."""
    try:
        from falkordb import FalkorDB
        db = FalkorDB(host='localhost', port=6379)
        graph = db.select_graph(graph_name)
        result = graph.query('''
            MATCH (c:Character {type: "player"})
            RETURN c.name
        ''')
        if result.result_set and result.result_set[0]:
            return result.result_set[0][0]
    except Exception as e:
        print(f"  Warning: Could not fetch player name from graph: {e}")
    return None


def get_player_name_from_yaml() -> Optional[str]:
    """Fetch the player character name from characters.yaml."""
    try:
        import yaml
        chars_file = PROJECT_ROOT / "data" / "world" / "characters.yaml"
        if chars_file.exists():
            with open(chars_file) as f:
                chars = yaml.safe_load(f)
            for char in chars:
                if char.get('type') == 'player':
                    return char.get('name')
    except Exception as e:
        print(f"  Warning: Could not fetch player name from YAML: {e}")
    return None

# Directories to scan
SCAN_DIRS = [
    "engine",
    "data",
    "docs",
    "agents",
    "frontend/src",
]

# File extensions to check
CODE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx"}
DOC_EXTENSIONS = {".md", ".yaml", ".yml", ".json"}
ALL_EXTENSIONS = CODE_EXTENSIONS | DOC_EXTENSIONS

# Files/dirs to skip
SKIP_PATTERNS = [
    "node_modules",
    "__pycache__",
    ".git",
    "venv",
    ".venv",
    "dist",
    "build",
    ".next",
    "lint_terminology.py",  # Don't lint self
]


@dataclass
class LintIssue:
    file: Path
    line_num: int
    line: str
    issue_type: str
    match: str
    suggestion: str


@dataclass
class LintResult:
    issues: List[LintIssue] = field(default_factory=list)
    files_scanned: int = 0
    files_with_issues: int = 0
    fixes_applied: int = 0


class TerminologyLinter:
    def __init__(self, player_name: str = "Rolf"):
        self.player_name = player_name
        self.result = LintResult()

        # Patterns for NPC replacement
        self.npc_patterns = [
            # NPC/NPCs -> character/characters
            (r'\bNPCs\b', 'characters'),
            (r'\bNPC\b', 'character'),
            (r'\bnpcs\b', 'characters'),
            (r'\bnpc\b', 'character'),
            # non-player character -> character (redundant)
            (r'\bnon-player characters?\b', 'character'),
            (r'\bNon-player characters?\b', 'character'),
            (r'\bNon-Player Characters?\b', 'Character'),
        ]

        # Patterns for "player" in node attributes (YAML/code)
        # These are cases where "player" is used as a value, not a type
        self.player_value_patterns = [
            # In YAML: name: "player" or name: player
            (r'(name:\s*["\']?)player(["\']?)', rf'\1{player_name}\2'),
            # In YAML: id: player or id: "player"
            (r'(id:\s*["\']?)player(["\']?)', rf'\1char_{player_name.lower()}\2'),
            # In code: name="player" or name='player'
            (r'(name\s*=\s*["\'])player(["\'])', rf'\1{player_name}\2'),
            # In code: "the player" when referring to character (but not type)
            # Skip this - too ambiguous
        ]

        # Patterns that are OK (don't flag these)
        self.ok_patterns = [
            r'type:\s*["\']?player',  # type: player is correct
            r'type\s*=\s*["\']player',  # type="player" is correct
            r'player_id',  # variable names are fine
            r'player_name',
            r'player_context',
            r'player_connection',
            r'PlayerContext',
            r'for_player',
            r'get_player',
            r'is_player',
            r'\.player',  # attribute access
            r'player\.',
            r'\[.player.\]',  # dict access
            r'# .*player',  # comments mentioning player concept
            r'Player character',  # documentation
            r'player character',
            r'the player',  # referring to human
            r'Player\'s',
            r'player\'s',
        ]

    def should_skip(self, path: Path) -> bool:
        """Check if path should be skipped."""
        path_str = str(path)
        for pattern in SKIP_PATTERNS:
            if pattern in path_str:
                return True
        return False

    def get_files(self) -> List[Path]:
        """Get all files to scan."""
        files = []
        for scan_dir in SCAN_DIRS:
            dir_path = PROJECT_ROOT / scan_dir
            if not dir_path.exists():
                continue
            for ext in ALL_EXTENSIONS:
                for file in dir_path.rglob(f"*{ext}"):
                    if not self.should_skip(file):
                        files.append(file)
        return files

    def is_ok_context(self, line: str, match: str) -> bool:
        """Check if match is in an OK context."""
        for pattern in self.ok_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                # Check if the OK pattern covers our match
                ok_match = re.search(pattern, line, re.IGNORECASE)
                if ok_match and match.lower() in ok_match.group().lower():
                    return True
        return False

    def check_npc_usage(self, file: Path, content: str) -> List[LintIssue]:
        """Check for NPC terminology that should be 'character'."""
        issues = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for pattern, replacement in self.npc_patterns:
                matches = list(re.finditer(pattern, line))
                for match in matches:
                    matched_text = match.group()
                    # Skip if in OK context
                    if self.is_ok_context(line, matched_text):
                        continue
                    issues.append(LintIssue(
                        file=file,
                        line_num=line_num,
                        line=line.strip(),
                        issue_type="npc_terminology",
                        match=matched_text,
                        suggestion=replacement
                    ))
        return issues

    def check_player_as_name(self, file: Path, content: str) -> List[LintIssue]:
        """Check for 'player' used as character name instead of actual name."""
        issues = []
        lines = content.split('\n')

        # Only check YAML files for this
        if file.suffix not in {'.yaml', '.yml'}:
            return issues

        for line_num, line in enumerate(lines, 1):
            # Check for name: player (but not type: player)
            if re.search(r'^\s*name:\s*["\']?player["\']?\s*$', line, re.IGNORECASE):
                if not re.search(r'type:', line):
                    issues.append(LintIssue(
                        file=file,
                        line_num=line_num,
                        line=line.strip(),
                        issue_type="player_as_name",
                        match="player",
                        suggestion=self.player_name
                    ))
        return issues

    def lint_file(self, file: Path) -> List[LintIssue]:
        """Lint a single file."""
        try:
            content = file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  Warning: Could not read {file}: {e}")
            return []

        issues = []
        issues.extend(self.check_npc_usage(file, content))
        issues.extend(self.check_player_as_name(file, content))
        return issues

    def fix_file(self, file: Path, issues: List[LintIssue]) -> int:
        """Apply fixes to a file. Returns number of fixes applied."""
        if not issues:
            return 0

        try:
            content = file.read_text(encoding='utf-8')
        except Exception:
            return 0

        fixes = 0

        # Apply NPC replacements
        for pattern, replacement in self.npc_patterns:
            new_content, count = re.subn(pattern, replacement, content)
            if count > 0:
                content = new_content
                fixes += count

        # Apply player name replacements (careful with these)
        if file.suffix in {'.yaml', '.yml'}:
            # name: player -> name: Rolf (but not type: player)
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if re.search(r'^\s*name:\s*["\']?player["\']?\s*$', line, re.IGNORECASE):
                    new_line = re.sub(
                        r'(name:\s*["\']?)player(["\']?)',
                        rf'\1{self.player_name}\2',
                        line,
                        flags=re.IGNORECASE
                    )
                    if new_line != line:
                        fixes += 1
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            content = '\n'.join(new_lines)

        if fixes > 0:
            file.write_text(content, encoding='utf-8')

        return fixes

    def run(self, fix: bool = False) -> LintResult:
        """Run the linter."""
        files = self.get_files()
        self.result.files_scanned = len(files)

        files_with_issues = set()

        print(f"Scanning {len(files)} files...")
        print()

        for file in files:
            issues = self.lint_file(file)
            if issues:
                files_with_issues.add(file)
                self.result.issues.extend(issues)

                if fix:
                    fixes = self.fix_file(file, issues)
                    self.result.fixes_applied += fixes

        self.result.files_with_issues = len(files_with_issues)
        return self.result

    def report(self, fix: bool = False):
        """Print report of issues found."""
        if not self.result.issues:
            print("✓ No terminology issues found!")
            return

        # Group by file
        by_file: Dict[Path, List[LintIssue]] = {}
        for issue in self.result.issues:
            if issue.file not in by_file:
                by_file[issue.file] = []
            by_file[issue.file].append(issue)

        # Group by type
        npc_issues = [i for i in self.result.issues if i.issue_type == "npc_terminology"]
        player_issues = [i for i in self.result.issues if i.issue_type == "player_as_name"]

        print("=" * 70)
        print("TERMINOLOGY LINT REPORT")
        print("=" * 70)
        print()

        if npc_issues:
            print(f"## NPC → character ({len(npc_issues)} issues)")
            print()
            shown = 0
            for issue in npc_issues[:20]:
                rel_path = issue.file.relative_to(PROJECT_ROOT)
                print(f"  {rel_path}:{issue.line_num}")
                print(f"    {issue.line[:70]}...")
                print(f"    '{issue.match}' → '{issue.suggestion}'")
                print()
                shown += 1
            if len(npc_issues) > 20:
                print(f"  ... and {len(npc_issues) - 20} more")
            print()

        if player_issues:
            print(f"## 'player' as name → '{self.player_name}' ({len(player_issues)} issues)")
            print()
            for issue in player_issues[:10]:
                rel_path = issue.file.relative_to(PROJECT_ROOT)
                print(f"  {rel_path}:{issue.line_num}")
                print(f"    {issue.line}")
                print(f"    '{issue.match}' → '{issue.suggestion}'")
                print()

        print("=" * 70)
        print(f"Files scanned:     {self.result.files_scanned}")
        print(f"Files with issues: {self.result.files_with_issues}")
        print(f"Total issues:      {len(self.result.issues)}")
        if fix:
            print(f"Fixes applied:     {self.result.fixes_applied}")
        else:
            print()
            print("Run with --fix to apply changes")
        print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Lint Blood Ledger codebase for terminology issues"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply fixes (default: dry-run)"
    )
    parser.add_argument(
        "--player-name",
        default=None,
        help="Override player character name (default: fetch from graph/YAML)"
    )
    parser.add_argument(
        "--graph",
        default="blood_ledger",
        help="Graph name to query for player (default: blood_ledger)"
    )
    args = parser.parse_args()

    # Resolve player name: CLI override > graph > YAML > error
    player_name = args.player_name
    if not player_name:
        print("Fetching player name from graph...")
        player_name = get_player_name_from_graph(args.graph)
    if not player_name:
        print("Fetching player name from characters.yaml...")
        player_name = get_player_name_from_yaml()
    if not player_name:
        print("ERROR: Could not determine player name.")
        print("  - No Character with type='player' found in graph")
        print("  - No Character with type='player' found in characters.yaml")
        print("  - Use --player-name to specify manually")
        sys.exit(1)

    print(f"Player character: {player_name}")
    print()

    linter = TerminologyLinter(player_name=player_name)
    linter.run(fix=args.fix)
    linter.report(fix=args.fix)

    # Exit with error code if issues found (for CI)
    if linter.result.issues and not args.fix:
        sys.exit(1)


if __name__ == "__main__":
    main()
