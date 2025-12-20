"""
ngram CLI - Memory for AI agents

DOCS: docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md

Protocol for context, state, and handoffs across sessions.

What `ngram init` does:
1. Copies the protocol files to .ngram/ in your project
2. Appends the protocol bootstrap to .ngram/CLAUDE.md (creates it if missing)

What `ngram validate` does:
1. Checks protocol invariants (from VALIDATION_Protocol_Invariants.md)
2. Reports gaps and issues
3. Helps maintain protocol health

WHY A CLI INSTEAD OF "JUST COPY THE FOLDER":
- Versioning: `pip install --upgrade ngram` gets you updates
- Discoverability: easier to remember than a git URL
- Future: can add `validate`, `new-module`, etc. without changing workflow

TEMPLATES LOCATION:
- When installed: ngram/templates/ (bundled with package)
- When developing: templates/ at repo root
- CLI checks both locations
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Import from submodules
from .agent_cli import AGENT_CHOICES, DEFAULT_AGENT
from .init_cmd import init_protocol
from .validate import validate_protocol
from .prompt import print_bootstrap_prompt
from .context import print_module_context
from .doctor import doctor_command
from .doctor_files import add_doctor_ignore, load_doctor_ignore
from .project_map import print_project_map
from .sync import sync_command
from .solve_escalations import solve_special_markers_command
from .repair import repair_command
from .refactor import refactor_command
from .repo_overview import generate_and_save as generate_overview


from .agent_cli import build_agent_command


def _add_module_translation_args(parser):
    parser.add_argument("--module-old", type=str, help="Existing module key in modules.yaml")
    parser.add_argument("--module-new", type=str, help="New module key name in modules.yaml")


def _validate_module_translation(args):
    if args.module_old or args.module_new:
        if not (args.module_old and args.module_new):
            raise ValueError("--module-old and --module-new must be supplied together")



def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="ngram",
        description="ngram - Memory for AI agents. Protocol for context, state, and handoffs."
    )
    parser.add_argument(
        "--agents",
        choices=AGENT_CHOICES,
        default="claude",
        help="Agent provider for repair and TUI (default: claude)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize ngram in the current directory"
    )
    init_parser.add_argument(
        "--no-force",
        action="store_true",
        dest="no_force",
        help="Don't overwrite existing .ngram/ directory (default: overwrite)"
    )
    init_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Directory to initialize (default: current directory)"
    )

    # ... (the rest of the original subparsers)


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
        "--github",
        action="store_true",
        help="Create GitHub issues for findings (default: disabled)"
    )
    doctor_parser.add_argument(
        "--no-github",
        action="store_true",
        help="Don't create GitHub issues for findings (default: disabled)"
    )
    doctor_parser.add_argument(
        "--github-max",
        type=int,
        default=10,
        help="Max GitHub issues to create (default: 10)"
    )

    # solve-markers command
    markers_parser = subparsers.add_parser(
        "solve-markers",
        help="List @ngram special markers (escalations, propositions) for human review"
    )
    markers_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory)"
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

    # overview command
    overview_parser = subparsers.add_parser(
        "overview",
        help="Generate repository overview with file tree, sections, functions, and dependencies"
    )
    overview_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory)"
    )
    overview_parser.add_argument(
        "--folder", "-p",
        type=str,
        default=None,
        help="Subfolder to map only (relative to project root)"
    )
    overview_parser.add_argument(
        "--format", "-f",
        choices=["md", "yaml", "json"],
        default="md",
        help="Output format (default: md)"
    )
    overview_parser.add_argument(
        "--min-size",
        type=int,
        default=500,
        help="Minimum file size in chars to include (default: 500, 0 = no limit)"
    )
    overview_parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Max files per directory, largest first (default: 10, 0 = no limit)"
    )
    overview_parser.add_argument(
        "--all",
        action="store_true",
        help="Include all files (equivalent to --min-size 0 --top 0)"
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
        help="Automatically fix project health issues using repair agents"
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
    repair_parser.add_argument(
        "--agents",
        choices=AGENT_CHOICES,
        default="claude",
        help="Agent provider for repair runs (default: claude)",
    )

    # refactor command
    refactor_parser = subparsers.add_parser(
        "refactor",
        help="Adjust module/doc names and keep references in sync"
    )
    refactor_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory)"
    )
    refactor_subparsers = refactor_parser.add_subparsers(dest="action")

    rename_parser = refactor_subparsers.add_parser(
        "rename",
        help="Rename a doc/module path and update references"
    )
    rename_parser.add_argument("old", type=str, help="Existing path to rename (relative to project root)")
    rename_parser.add_argument("new", type=str, help="New target path (relative to project root)")
    _add_module_translation_args(rename_parser)
    rename_parser.set_defaults(action="rename")

    move_parser = refactor_subparsers.add_parser(
        "move",
        help="Move a doc/module path elsewhere (alias for rename)"
    )
    move_parser.add_argument("old", type=str, help="Existing path to move (relative to project root)")
    move_parser.add_argument("new", type=str, help="Destination path (relative to project root)")
    _add_module_translation_args(move_parser)
    move_parser.set_defaults(action="move")

    promote_parser = refactor_subparsers.add_parser(
        "promote",
        help="Promote a docs area/module into the root docs folder"
    )
    promote_parser.add_argument("source", type=str, help="Existing docs path (docs/<area>/<module>)")
    promote_parser.add_argument(
        "--target", "-t",
        type=str,
        default=None,
        help="Optional explicit target path (defaults to docs/<module>)"
    )
    _add_module_translation_args(promote_parser)
    promote_parser.set_defaults(action="promote")

    demote_parser = refactor_subparsers.add_parser(
        "demote",
        help="Demote a docs module into an area (docs/<area>/<module>)"
    )
    demote_parser.add_argument("module", type=str, help="Existing module path (usually docs/<module>)")
    demote_parser.add_argument(
        "--target-area", "-a",
        type=str,
        required=True,
        help="Area name under docs/ to move into"
    )
    _add_module_translation_args(demote_parser)
    demote_parser.set_defaults(action="demote")

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
        success = init_protocol(args.dir, not args.no_force)
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
            github=args.github and not args.no_github, github_max=args.github_max
        )
        sys.exit(exit_code)
    elif args.command == "solve-markers":
        exit_code = solve_special_markers_command(args.dir)
        sys.exit(exit_code)
    elif args.command == "map":
        print_project_map(args.dir, args.output)
        sys.exit(0)
    elif args.command == "overview":
        # Handle --all flag
        min_size = 0 if args.all else args.min_size
        top_files = 0 if args.all else args.top
        output_path = generate_overview(
            args.dir, args.format,
            subfolder=args.folder,
            min_size=min_size,
            top_files=top_files,
        )
        print(f"Generated: {output_path}")
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
            agent_provider=args.agents,
        )
        sys.exit(exit_code)
    elif args.command == "refactor":
        if not args.action:
            refactor_parser.print_help()
            sys.exit(1)
        try:
            _validate_module_translation(args)
        except ValueError as exc:
            print(exc)
            sys.exit(1)
        exit_code = refactor_command(args)
        sys.exit(exit_code)
    elif args.command == "ignore":
        if args.list:
            # List current ignores
            ignores = load_doctor_ignore(args.dir)
            if not ignores:
                print("No ignores configured.")
                print(f"Add ignores with: ngram ignore --type TYPE --path PATH --reason REASON")
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
            print("  List ignores: ngram ignore --list")
            print("  Add ignore:   ngram ignore --type TYPE --path PATH [--reason REASON]")
            print()
            print("Examples:")
            print("  ngram ignore --type MONOLITH --path src/legacy.py --reason 'Legacy code, too risky to split'")
            print("  ngram ignore --type MAGIC_VALUES --path tests/** --reason 'Test fixtures'")
            sys.exit(1)
    elif args.command is None:
        # Launch TUI when no subcommand is given (similar to agent CLIs)
        try:
            from .tui import NgramApp
            app = NgramApp(target_dir=Path.cwd(), agent_provider=args.agents)
            app.run()
            sys.exit(0)
        except ImportError as e:
            if "textual" in str(e).lower():
                print("TUI requires textual. Install with: pip install ngram[tui]")
                print()
                parser.print_help()
                sys.exit(1)
            else:
                raise
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
