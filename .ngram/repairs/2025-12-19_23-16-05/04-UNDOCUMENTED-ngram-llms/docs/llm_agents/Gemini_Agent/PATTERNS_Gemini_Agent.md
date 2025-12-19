# PATTERNS_Gemini_Agent.md

## Design Philosophy

The `Gemini_Agent` module (`ngram/llms/gemini_agent.py`) is designed as a standalone subprocess to interface with the Gemini Large Language Model (LLM) within the `ngram` CLI ecosystem. Its primary purpose is to enable the `ngram` CLI to leverage Gemini's generative capabilities and sophisticated tool-use mechanisms.

### Core Principles

1.  **Modularity:** The agent operates as an independent Python script, making it easy to swap out or add other LLM providers without deeply coupling them to the core `ngram` CLI logic.
2.  **Tool-Use Integration:** It exposes a rich set of predefined tools (e.g., `run_shell_command`, `read_file`, `write_file`, `google_web_search`) that the Gemini model can call during a chat session. This allows the LLM to interact with the system environment and retrieve real-time information or perform actions.
3.  **Standardized Communication:** Communication with the parent `ngram` CLI process is done via standard input/output (stdin/stdout), using JSON for structured data exchange. This facilitates clear parsing and handling of LLM responses and tool outputs.
4.  **Configuration Flexibility:** API keys and other settings are loaded from a `.env` file, environment variables, or command-line arguments, providing a flexible configuration hierarchy.
5.  **Streaming Output:** The agent supports streaming responses from the LLM, allowing for real-time interaction and feedback in the CLI.

## Architectural Patterns

### Provider-Specific LLM Subprocesses

This module exemplifies the "Provider-Specific LLM Subprocess" pattern. Each LLM provider (e.g., Gemini, OpenAI, Claude) integrated with `ngram` should ideally have its own dedicated subprocess module.

-   **Isolation:** Each LLM's unique API calls, tool function signatures, and response formats are encapsulated within its specific agent. This prevents a single change in an LLM API from breaking other integrations.
-   **Resource Management:** Running LLM interactions in subprocesses allows for better resource management and isolation of dependencies.
-   **Tool Definition Mapping:** The Python functions exposed as tools to the LLM are defined directly within this subprocess, mapping `ngram`'s conceptual tools (like `read_file`) to their Python implementations.

## In/Out of Scope

### In Scope

-   Direct API interaction with the Gemini LLM.
-   Mapping `ngram` CLI tools to Gemini tool definitions.
-   Handling streaming responses and tool call requests from Gemini.
-   Managing Gemini API key and base URL configuration.
-   Executing specific `ngram` tools via Python function calls and returning results to Gemini.

### Out of Scope

-   General `ngram` CLI argument parsing (handled by the main `ngram` CLI).
-   Core `ngram` project state management (handled by `SYNC_Project_State.md` and other core modules).
-   Implementing the actual logic of the tools (the tools are imported or called as Python functions; their core implementation resides elsewhere).
-   Integration with LLM providers other than Gemini.
