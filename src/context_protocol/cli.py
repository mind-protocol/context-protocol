"""
Context Protocol CLI

DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md

This is intentionally minimal. The protocol is just files — this CLI copies them.

What `context-protocol init` does:
1. Copies the protocol files to .context-protocol/ in your project
2. Appends the protocol bootstrap to your CLAUDE.md (creates it if missing)

What `context-protocol validate` does:
1. Checks protocol invariants (from VALIDATION_Protocol_Invariants.md)
2. Reports gaps and issues
3. Helps maintain protocol health

WHY A CLI INSTEAD OF "JUST COPY THE FOLDER":
- Versioning: `pip install --upgrade context-protocol` gets you updates
- Discoverability: easier to remember than a git URL
- Future: can add `validate`, `new-module`, etc. without changing workflow

TEMPLATES LOCATION:
- When installed: src/context_protocol/templates/ (bundled with package)
- When developing: templates/ at repo root
- CLI checks both locations
"""

import argparse
import sys
from pathlib import Path

# Import from submodules
from .init_cmd import init_protocol
from .validate import validate_protocol
from .prompt import print_bootstrap_prompt
from .context import print_module_context
from .doctor import doctor_command
from .doctor_files import add_doctor_ignore, load_doctor_ignore
from .project_map import print_project_map
from .sync import sync_command
from .repair import repair_command


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="context-protocol",
        description="Context Protocol - A context management system for AI agents"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize Context Protocol in the current directory"
    )
    init_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite existing .context-protocol/ directory"
    )
    init_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Directory to initialize (default: current directory)"
    )
    init_parser.add_argument(
        "--claude-md-dir",
        type=Path,
        default=None,
        help="Directory for CLAUDE.md (default: same as --dir)"
    )

    # validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Check protocol invariants and find gaps"
    )
    validate_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Directory to validate (default: current directory)"
    )
    validate_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show details for all checks, not just failures"
    )

    # prompt command
    prompt_parser = subparsers.add_parser(
        "prompt",
        help="Generate bootstrap prompt for LLM"
    )
    prompt_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory)"
    )

    # context command
    context_parser = subparsers.add_parser(
        "context",
        help="Get full documentation context for a file"
    )
    context_parser.add_argument(
        "file",
        type=Path,
        help="File path to get context for"
    )
    context_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory)"
    )

    # doctor command
    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Check project health (monoliths, stale docs, undocumented code)"
    )
    doctor_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory)"
    )
    doctor_parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    doctor_parser.add_argument(
        "--level", "-l",
        choices=["critical", "warning", "all"],
        default="all",
        help="Filter by severity level (default: all)"
    )
    doctor_parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save to HEALTH.md"
    )
    doctor_parser.add_argument(
        "--no-github",
        action="store_true",
        help="Don't create GitHub issues for findings (default: creates issues)"
    )
    doctor_parser.add_argument(
        "--github-max",
        type=int,
        default=10,
        help="Max GitHub issues to create (default: 10)"
    )

    # map command
    map_parser = subparsers.add_parser(
        "map",
        help="Show visual project map of modules and dependencies"
    )
    map_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory)"
    )
    map_parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output HTML file path (default: open in browser)"
    )

    # sync command
    sync_parser = subparsers.add_parser(
        "sync",
        help="Show SYNC file status (auto-archives large files)"
    )
    sync_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory)"
    )

    # repair command
    repair_parser = subparsers.add_parser(
        "repair",
        help="Automatically fix project health issues using Claude Code agents"
    )
    repair_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory)"
    )
    repair_parser.add_argument(
        "--max", "-m",
        type=int,
        default=None,
        help="Maximum issues to fix (default: all)"
    )
    repair_parser.add_argument(
        "--type", "-t",
        action="append",
        dest="types",
        choices=[
            "MONOLITH", "UNDOCUMENTED", "STALE_SYNC", "PLACEHOLDER",
            "INCOMPLETE_CHAIN", "NO_DOCS_REF", "BROKEN_IMPL_LINK",
            "STUB_IMPL", "INCOMPLETE_IMPL", "UNDOC_IMPL", "LARGE_DOC_MODULE",
            "YAML_DRIFT"
        ],
        help="Only fix specific issue types (can be repeated)"
    )
    repair_parser.add_argument(
        "--depth",
        choices=["links", "docs", "full"],
        default="docs",
        help="Repair depth: links (refs only), docs (+ content), full (+ code changes). Default: docs"
    )
    repair_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without spawning agents"
    )
    repair_parser.add_argument(
        "--parallel", "-p",
        type=int,
        default=5,
        help="Number of parallel agents (default: 5, use 1 for sequential)"
    )

    # ignore command
    ignore_parser = subparsers.add_parser(
        "ignore",
        help="Add or list suppressed doctor issues"
    )
    ignore_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory)"
    )
    ignore_parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List current ignores"
    )
    ignore_parser.add_argument(
        "--type", "-t",
        type=str,
        help="Issue type to ignore (e.g., MONOLITH, HARDCODED_SECRET)"
    )
    ignore_parser.add_argument(
        "--path", "-p",
        type=str,
        help="Path or glob pattern to ignore (e.g., src/legacy/*, tests/**)"
    )
    ignore_parser.add_argument(
        "--reason", "-r",
        type=str,
        default="",
        help="Reason for ignoring (for audit trail)"
    )

    # version
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    args = parser.parse_args()

    if args.command == "init":
        success = init_protocol(args.dir, args.force, args.claude_md_dir)
        sys.exit(0 if success else 1)
    elif args.command == "validate":
        success = validate_protocol(args.dir, args.verbose)
        sys.exit(0 if success else 1)
    elif args.command == "prompt":
        print_bootstrap_prompt(args.dir)
        sys.exit(0)
    elif args.command == "context":
        success = print_module_context(args.dir, args.file)
        sys.exit(0 if success else 1)
    elif args.command == "doctor":
        exit_code = doctor_command(
            args.dir, args.format, args.level, args.no_save,
            github=not args.no_github, github_max=args.github_max
        )
        sys.exit(exit_code)
    elif args.command == "map":
        print_project_map(args.dir, args.output)
        sys.exit(0)
    elif args.command == "sync":
        exit_code = sync_command(args.dir)
        sys.exit(exit_code)
    elif args.command == "repair":
        exit_code = repair_command(
            args.dir,
            max_issues=args.max,
            issue_types=args.types,
            depth=args.depth,
            dry_run=args.dry_run,
            parallel=args.parallel,
        )
        sys.exit(exit_code)
    elif args.command == "ignore":
        if args.list:
            # List current ignores
            ignores = load_doctor_ignore(args.dir)
            if not ignores:
                print("No ignores configured.")
                print(f"Add ignores with: context-protocol ignore --type TYPE --path PATH --reason REASON")
            else:
                print(f"Doctor Ignores ({len(ignores)} entries):")
                print("-" * 50)
                for ig in ignores:
                    print(f"  {ig.issue_type}: {ig.path}")
                    if ig.reason:
                        print(f"    Reason: {ig.reason}")
                    if ig.added_by or ig.added_date:
                        print(f"    Added: {ig.added_by or 'unknown'} on {ig.added_date or 'unknown'}")
                    print()
            sys.exit(0)
        elif args.type and args.path:
            # Add new ignore
            success = add_doctor_ignore(
                args.dir,
                issue_type=args.type.upper(),
                path=args.path,
                reason=args.reason,
                added_by="human"
            )
            if success:
                print(f"Added ignore: {args.type.upper()} on {args.path}")
            else:
                print("Failed to add ignore (check PyYAML is installed)")
                sys.exit(1)
            sys.exit(0)
        else:
            print("Usage:")
            print("  List ignores: context-protocol ignore --list")
            print("  Add ignore:   context-protocol ignore --type TYPE --path PATH [--reason REASON]")
            print()
            print("Examples:")
            print("  context-protocol ignore --type MONOLITH --path src/legacy.py --reason 'Legacy code, too risky to split'")
            print("  context-protocol ignore --type MAGIC_VALUES --path tests/** --reason 'Test fixtures'")
            sys.exit(1)
    elif args.command is None:
        parser.print_help()
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
