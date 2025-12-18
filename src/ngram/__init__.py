"""
ngram

A context management protocol for AI agents working on code.

DOCS: ../docs/protocol/

This package provides a CLI to install the ngram into any project.
The protocol helps AI agents:
- Load the right context for their current task
- Track state across sessions
- Navigate between code and documentation

The protocol itself is just markdown files. This package copies them to your project
and updates your CLAUDE.md to reference them.
"""

__version__ = "0.1.0"

from .cli import main

__all__ = ["main", "__version__"]
