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
