"""
Data types for the doctor command.

Contains shared types used by both doctor.py and doctor_report.py.
Extracted to avoid circular imports.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class DoctorIssue:
    """A health issue found by the doctor command."""
    issue_type: str      # MONOLITH, UNDOCUMENTED, STALE_SYNC, etc.
    severity: str        # critical, warning, info
    path: str            # Affected file/directory
    message: str         # Human description
    details: Dict[str, Any] = field(default_factory=dict)
    suggestion: str = ""


@dataclass
class DoctorConfig:
    """Configuration for doctor checks."""
    monolith_lines: int = 800
    stale_sync_days: int = 14
    ignore: List[str] = field(default_factory=lambda: [
        "node_modules/**",
        ".next/**",
        "dist/**",
        "build/**",
        "vendor/**",
        "__pycache__/**",
        ".git/**",
        "*.min.js",
        "*.bundle.js",
        ".venv/**",
        "venv/**",
    ])
    disabled_checks: List[str] = field(default_factory=list)


@dataclass
class IgnoreEntry:
    """A suppressed issue in doctor-ignore.yaml.

    Issues can be ignored by:
    - issue_type + path: Exact match (e.g., MONOLITH on src/big_file.py)
    - issue_type + path pattern: Glob match (e.g., MAGIC_VALUES on tests/**)
    - issue_type only: Suppress all issues of that type (rarely used)
    """
    issue_type: str       # MONOLITH, HARDCODED_SECRET, etc.
    path: str             # File/dir path or glob pattern
    reason: str = ""      # Why this is being ignored (required for audit)
    added_by: str = ""    # Who/what added this ignore
    added_date: str = ""  # When added (YYYY-MM-DD)
