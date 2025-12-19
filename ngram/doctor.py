"""
Doctor command for ngram CLI.

Provides health checks for projects:
- Monolith files (too many lines)
- Undocumented code directories
- Stale SYNC files
- Placeholder documentation
- Missing DOCS: references
- Incomplete doc chains

DOCS: docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md
"""

import json
from pathlib import Path
from typing import List, Dict, Any

from .sync import archive_all_syncs
from .doctor_types import DoctorIssue, DoctorConfig
from .doctor_report import (
    generate_health_markdown,
    print_doctor_report,
    check_sync_status,
)
from .doctor_files import (
    load_doctor_config,
    load_doctor_ignore,
    filter_ignored_issues,
)
from .doctor_checks import (
    doctor_check_monolith,
    doctor_check_undocumented,
    doctor_check_stale_sync,
    doctor_check_placeholder_docs,
    doctor_check_no_docs_ref,
    doctor_check_broken_impl_links,
    doctor_check_stub_impl,
    doctor_check_incomplete_impl,
    doctor_check_undoc_impl,
    doctor_check_yaml_drift,
    doctor_check_large_doc_module,
    doctor_check_incomplete_chain,
    doctor_check_missing_tests,
    doctor_check_orphan_docs,
    doctor_check_stale_impl,
    doctor_check_magic_values,
    doctor_check_hardcoded_secrets,
)
from .doctor_checks_sync import (
    doctor_check_conflicts,
    doctor_check_doc_gaps,
    doctor_check_suggestions,
)
from .doctor_checks_content import (
    doctor_check_new_undoc_code,
    doctor_check_doc_duplication,
    doctor_check_long_strings,
    doctor_check_recent_log_errors,
)


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
    all_issues.extend(doctor_check_new_undoc_code(target_dir, config))
    all_issues.extend(doctor_check_large_doc_module(target_dir, config))
    all_issues.extend(doctor_check_yaml_drift(target_dir, config))
    # New checks
    all_issues.extend(doctor_check_missing_tests(target_dir, config))
    all_issues.extend(doctor_check_orphan_docs(target_dir, config))
    all_issues.extend(doctor_check_stale_impl(target_dir, config))
    all_issues.extend(doctor_check_doc_gaps(target_dir, config))
    all_issues.extend(doctor_check_conflicts(target_dir, config))
    all_issues.extend(doctor_check_suggestions(target_dir, config))
    all_issues.extend(doctor_check_doc_duplication(target_dir, config))
    all_issues.extend(doctor_check_recent_log_errors(target_dir, config))
    # Code quality checks
    all_issues.extend(doctor_check_magic_values(target_dir, config))
    all_issues.extend(doctor_check_hardcoded_secrets(target_dir, config))
    all_issues.extend(doctor_check_long_strings(target_dir, config))

    # Filter out suppressed issues from doctor-ignore.yaml
    ignores = load_doctor_ignore(target_dir)
    all_issues, ignored_count = filter_ignored_issues(all_issues, ignores)

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
        },
        "ignored_count": ignored_count,
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
            print("  Run: ngram sync")

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
        mapping_path = target_dir / ".ngram" / "state" / "github_issues.json"
        if mapping_path.parent.exists():
            mapping_data = {
                issue.path: {"number": issue.number, "url": issue.url, "type": issue.issue_type}
                for issue in github_issues
            }
            mapping_path.write_text(json.dumps(mapping_data, indent=2))

    # Save to SYNC_Project_Health.md by default (unless --no-save or json output)
    if not no_save and output_format != "json":
        health_path = target_dir / ".ngram" / "state" / "SYNC_Project_Health.md"
        if health_path.parent.exists():
            health_content = generate_health_markdown(results, github_issues)
            health_path.write_text(health_content)
            print()
            print(f"Saved to {health_path.relative_to(target_dir)}")

    # Always exit 0; issues are reported in output and SYNC file
    return 0
