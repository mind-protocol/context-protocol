"""
ngram status - Show module implementation progress and health

DOCS: docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture.md

Provides:
- Global status: overview of all modules with maturity and health
- Module status: detailed view of a specific module's implementation progress
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

# Try to import yaml, fall back gracefully
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class DocChainStatus:
    """Status of a module's documentation chain."""
    objectifs: Optional[Path] = None
    patterns: Optional[Path] = None
    behaviors: Optional[Path] = None
    algorithm: Optional[Path] = None
    validation: Optional[Path] = None
    implementation: Optional[Path] = None
    health: Optional[Path] = None
    sync: Optional[Path] = None

    def completeness_score(self) -> Tuple[int, int]:
        """Return (present, total) for doc chain completeness."""
        docs = [
            self.patterns, self.behaviors, self.algorithm,
            self.validation, self.implementation, self.health, self.sync
        ]
        present = sum(1 for d in docs if d is not None)
        return present, len(docs)

    def to_bar(self) -> str:
        """Return a visual bar showing completeness."""
        present, total = self.completeness_score()
        filled = "█" * present
        empty = "░" * (total - present)
        return f"[{filled}{empty}] {present}/{total}"


@dataclass
class ModuleStatus:
    """Complete status of a module."""
    name: str
    maturity: str = "UNKNOWN"
    code_pattern: str = ""
    docs_path: str = ""
    doc_chain: DocChainStatus = field(default_factory=DocChainStatus)
    sync_status: str = "NO_SYNC"
    sync_summary: str = ""
    health_issues: List[Dict] = field(default_factory=list)
    exists_in_yaml: bool = False
    code_exists: bool = False
    docs_exist: bool = False


def load_modules_yaml(project_dir: Path) -> Dict[str, Any]:
    """Load modules.yaml from project directory."""
    if not HAS_YAML:
        return {}

    yaml_path = project_dir / "modules.yaml"
    if not yaml_path.exists():
        return {}

    try:
        with open(yaml_path) as f:
            data = yaml.safe_load(f) or {}

        # Modules can be under 'modules:' key or at root level
        # Collect all dict entries that look like module configs (have 'code' or 'docs' keys)
        modules = {}

        # Check under 'modules' key first
        if "modules" in data and isinstance(data["modules"], dict):
            for k, v in data["modules"].items():
                if isinstance(v, dict) and ("code" in v or "docs" in v):
                    modules[k] = v

        # Also check root level for module definitions
        for k, v in data.items():
            if k == "modules":
                continue
            if isinstance(v, dict) and ("code" in v or "docs" in v):
                modules[k] = v

        return modules
    except Exception:
        return {}


def find_doc_chain(docs_path: Path) -> DocChainStatus:
    """Find documentation chain files in a docs directory."""
    chain = DocChainStatus()

    if not docs_path.exists():
        return chain

    # Search for doc types
    patterns = {
        "objectifs": "OBJECTIFS_*.md",
        "patterns": "PATTERNS_*.md",
        "behaviors": "BEHAVIORS_*.md",
        "algorithm": "ALGORITHM_*.md",
        "validation": "VALIDATION_*.md",
        "implementation": "IMPLEMENTATION_*.md",
        "health": "HEALTH_*.md",
        "sync": "SYNC_*.md",
    }

    for doc_type, pattern in patterns.items():
        matches = list(docs_path.glob(pattern))
        # Also check subdirectories
        if not matches:
            matches = list(docs_path.glob(f"**/{pattern}"))
        if matches:
            # Filter out archive files
            matches = [m for m in matches if "archive" not in m.name.lower()]
            if matches:
                setattr(chain, doc_type, matches[0])

    return chain


def extract_sync_status(sync_path: Path) -> Tuple[str, str]:
    """Extract STATUS and summary from a SYNC file."""
    if not sync_path or not sync_path.exists():
        return "NO_SYNC", ""

    try:
        content = sync_path.read_text()

        # Extract STATUS
        status_match = re.search(r'^STATUS:\s*(\w+)', content, re.MULTILINE)
        status = status_match.group(1) if status_match else "UNKNOWN"

        # Extract first paragraph after ## as summary
        summary = ""
        lines = content.split('\n')
        in_summary = False
        for line in lines:
            if line.startswith('## ') and not in_summary:
                in_summary = True
                continue
            if in_summary:
                if line.startswith('#') or line.startswith('```'):
                    break
                if line.strip():
                    summary = line.strip()[:100]
                    if len(line.strip()) > 100:
                        summary += "..."
                    break

        return status, summary
    except Exception:
        return "ERROR", ""


def extract_doc_status(doc_path: Path) -> str:
    """Extract STATUS from any doc file header."""
    if not doc_path or not doc_path.exists():
        return "MISSING"

    try:
        content = doc_path.read_text()[:500]  # Only read beginning
        status_match = re.search(r'^STATUS:\s*(\w+)', content, re.MULTILINE)
        return status_match.group(1) if status_match else "UNKNOWN"
    except Exception:
        return "ERROR"


def get_module_health_issues(project_dir: Path, module_name: str, code_pattern: str, docs_path: str) -> List[Dict]:
    """Get health issues for a specific module from doctor."""
    # Import doctor checks
    try:
        from .doctor import run_all_checks
        issues = run_all_checks(project_dir)

        # Filter issues related to this module
        module_issues = []
        for issue in issues:
            path = issue.path
            # Check if issue path matches module code or docs
            if code_pattern and _path_matches_glob(path, code_pattern):
                module_issues.append({
                    "type": issue.issue_type,
                    "severity": issue.severity,
                    "path": path,
                    "message": issue.message,
                })
            elif docs_path and path.startswith(docs_path):
                module_issues.append({
                    "type": issue.issue_type,
                    "severity": issue.severity,
                    "path": path,
                    "message": issue.message,
                })

        return module_issues
    except Exception as e:
        return [{"type": "ERROR", "severity": "warning", "path": "", "message": str(e)}]


def _path_matches_glob(path: str, pattern: str) -> bool:
    """Check if a path matches a glob pattern (simple implementation)."""
    import fnmatch
    # Handle ** patterns
    if "**" in pattern:
        base = pattern.split("**")[0].rstrip("/")
        return path.startswith(base)
    return fnmatch.fnmatch(path, pattern)


def get_module_status(project_dir: Path, module_name: str) -> ModuleStatus:
    """Get detailed status for a specific module."""
    modules = load_modules_yaml(project_dir)
    status = ModuleStatus(name=module_name)

    if module_name in modules:
        mod_config = modules[module_name]
        status.exists_in_yaml = True
        status.maturity = mod_config.get("maturity", "UNKNOWN")
        status.code_pattern = mod_config.get("code", "")
        status.docs_path = mod_config.get("docs", "")

        # Check if code exists
        if status.code_pattern:
            code_base = status.code_pattern.split("**")[0].rstrip("/*")
            status.code_exists = (project_dir / code_base).exists()

        # Check docs
        if status.docs_path:
            docs_full = project_dir / status.docs_path
            status.docs_exist = docs_full.exists()
            status.doc_chain = find_doc_chain(docs_full)

            # Get sync status
            if status.doc_chain.sync:
                status.sync_status, status.sync_summary = extract_sync_status(status.doc_chain.sync)

        # Get health issues
        status.health_issues = get_module_health_issues(
            project_dir, module_name, status.code_pattern, status.docs_path
        )

    return status


def get_all_modules_status(project_dir: Path) -> List[ModuleStatus]:
    """Get status for all modules."""
    modules = load_modules_yaml(project_dir)
    statuses = []

    for name in sorted(modules.keys()):
        status = get_module_status(project_dir, name)
        statuses.append(status)

    return statuses


def format_module_status(status: ModuleStatus, verbose: bool = False) -> str:
    """Format a module status for display."""
    lines = []

    # Header with name and maturity
    maturity_colors = {
        "CANONICAL": "\033[32m",  # Green
        "DESIGNING": "\033[33m",  # Yellow
        "PROPOSED": "\033[36m",   # Cyan
        "DEPRECATED": "\033[31m", # Red
        "UNKNOWN": "\033[37m",    # Gray
    }
    reset = "\033[0m"
    color = maturity_colors.get(status.maturity, reset)

    lines.append(f"\n{'='*60}")
    lines.append(f"  {status.name}")
    lines.append(f"{'='*60}")
    lines.append(f"  Maturity:    {color}{status.maturity}{reset}")

    if status.code_pattern:
        exists = "✓" if status.code_exists else "✗"
        lines.append(f"  Code:        {status.code_pattern} {exists}")

    if status.docs_path:
        exists = "✓" if status.docs_exist else "✗"
        lines.append(f"  Docs:        {status.docs_path} {exists}")

    # Doc chain
    lines.append(f"  Doc Chain:   {status.doc_chain.to_bar()}")

    if verbose:
        chain = status.doc_chain
        doc_items = [
            ("OBJECTIFS", chain.objectifs),
            ("PATTERNS", chain.patterns),
            ("BEHAVIORS", chain.behaviors),
            ("ALGORITHM", chain.algorithm),
            ("VALIDATION", chain.validation),
            ("IMPLEMENTATION", chain.implementation),
            ("HEALTH", chain.health),
            ("SYNC", chain.sync),
        ]
        for doc_name, doc_path in doc_items:
            if doc_path:
                doc_status = extract_doc_status(doc_path)
                lines.append(f"               ✓ {doc_name}: {doc_path.name} ({doc_status})")
            else:
                lines.append(f"               ✗ {doc_name}: missing")

    # SYNC status
    if status.sync_status != "NO_SYNC":
        lines.append(f"  SYNC Status: {status.sync_status}")
        if status.sync_summary:
            lines.append(f"               {status.sync_summary}")

    # Health issues
    if status.health_issues:
        critical = sum(1 for i in status.health_issues if i["severity"] == "critical")
        warnings = sum(1 for i in status.health_issues if i["severity"] == "warning")
        lines.append(f"  Health:      {critical} critical, {warnings} warnings")

        if verbose:
            for issue in status.health_issues[:5]:  # Show first 5
                sev = "!" if issue["severity"] == "critical" else "?"
                lines.append(f"               {sev} {issue['type']}: {issue['path']}")
            if len(status.health_issues) > 5:
                lines.append(f"               ... and {len(status.health_issues) - 5} more")
    else:
        lines.append(f"  Health:      ✓ No issues")

    return "\n".join(lines)


def format_global_status(statuses: List[ModuleStatus]) -> str:
    """Format global status overview."""
    lines = []

    # Header
    lines.append("\n" + "="*70)
    lines.append("  NGRAM MODULE STATUS")
    lines.append("="*70)

    # Summary counts
    total = len(statuses)
    by_maturity = {}
    total_issues = 0
    total_critical = 0

    for s in statuses:
        by_maturity[s.maturity] = by_maturity.get(s.maturity, 0) + 1
        total_issues += len(s.health_issues)
        total_critical += sum(1 for i in s.health_issues if i["severity"] == "critical")

    lines.append(f"\n  Total Modules: {total}")
    lines.append(f"  Maturity Breakdown:")
    for mat in ["CANONICAL", "DESIGNING", "PROPOSED", "DEPRECATED", "UNKNOWN"]:
        if mat in by_maturity:
            lines.append(f"    {mat}: {by_maturity[mat]}")

    lines.append(f"\n  Health Overview: {total_critical} critical, {total_issues - total_critical} warnings")

    # Table
    lines.append("\n" + "-"*70)
    lines.append(f"  {'MODULE':<30} {'MATURITY':<12} {'DOCS':<10} {'HEALTH':<10}")
    lines.append("-"*70)

    for s in statuses:
        present, total_docs = s.doc_chain.completeness_score()
        docs_str = f"{present}/{total_docs}"

        issues_count = len(s.health_issues)
        critical = sum(1 for i in s.health_issues if i["severity"] == "critical")
        if critical > 0:
            health_str = f"{critical}c/{issues_count}t"
        elif issues_count > 0:
            health_str = f"{issues_count}w"
        else:
            health_str = "✓"

        lines.append(f"  {s.name:<30} {s.maturity:<12} {docs_str:<10} {health_str:<10}")

    lines.append("-"*70)
    lines.append("")
    lines.append("  Legend: c=critical, w=warnings, t=total, ✓=healthy")
    lines.append("  Run 'ngram status <module>' for detailed view")
    lines.append("")

    return "\n".join(lines)


def status_command(project_dir: Path, module_name: Optional[str] = None, verbose: bool = False) -> int:
    """
    Main status command entry point.

    Args:
        project_dir: Project root directory
        module_name: Optional specific module to show
        verbose: Show detailed information

    Returns:
        Exit code (0 = success)
    """
    if not HAS_YAML:
        print("Error: PyYAML required for status command")
        print("Install with: pip install pyyaml")
        return 1

    modules_path = project_dir / "modules.yaml"
    if not modules_path.exists():
        print(f"No modules.yaml found in {project_dir}")
        print("Run 'ngram init' to create one, or add modules manually.")
        return 1

    if module_name:
        # Single module status
        status = get_module_status(project_dir, module_name)
        if not status.exists_in_yaml:
            print(f"Module '{module_name}' not found in modules.yaml")
            print("\nAvailable modules:")
            modules = load_modules_yaml(project_dir)
            for name in sorted(modules.keys()):
                print(f"  - {name}")
            return 1

        print(format_module_status(status, verbose=verbose))
    else:
        # Global status
        statuses = get_all_modules_status(project_dir)
        if not statuses:
            print("No modules defined in modules.yaml")
            return 1

        print(format_global_status(statuses))

        if verbose:
            for status in statuses:
                print(format_module_status(status, verbose=True))

    return 0
