# ngram LLM Agents — Implementation: Code Architecture

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against commit ad538f8
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Provider_Specific_LLM_Subprocesses.md
BEHAVIORS:       ./BEHAVIORS_Gemini_Agent_Output.md
ALGORITHM:       ./ALGORITHM_Gemini_Stream_Flow.md
VALIDATION:      ./VALIDATION_Gemini_Agent_Invariants.md
THIS:            IMPLEMENTATION_LLM_Agent_Code_Architecture.md (you are here)
TEST:            ./TEST_LLM_Agent_Coverage.md
SYNC:            ./SYNC_LLM_Agents_State.md
```

---

## MODULE LAYOUT

```
ngram/llms/gemini_agent.py  # Gemini adapter CLI
```

---

## ENTRY POINTS

- `ngram/llms/gemini_agent.py` (invoked by python -m ngram.llms.gemini_agent from `ngram/agent_cli.py`)

---

## KEY FUNCTIONS

- `main()` — CLI entry point; parses args, configures Gemini SDK, streams output.
- Tool helpers inside `main()` handle filesystem, search, and optional web fetch actions.

---

## DATA FLOW

```
ngram/agent_cli.py
    ↓ build subprocess command
ngram/llms/gemini_agent.py (python -m ngram.llms.gemini_agent)
    ↓ parse args + load env
    ↓ genai.configure(api_key)
    ↓ start_chat + send_message
    ↓ stdout JSON stream for TUI
```

---

## EXTERNAL DEPENDENCIES

- Google GenAI SDK (python package name: google.genai) for Gemini API access
- `dotenv` for `.env` loading

---

## CONFIGURATION

- `GEMINI_API_KEY` (CLI arg, `.env`, or environment variable)
- `NGRAM_GOOGLE_SEARCH_URL` (optional, `.env` or environment variable; defaults to `https://www.google.com/search`)
- `--output-format` determines JSON streaming vs plain text
- Tool outputs may persist under .ngram/state (agent_todos.json, agent_memory.jsonl)

---

## INTEGRATION POINTS

- `ngram/agent_cli.py` selects the Gemini adapter when the agent provider is `gemini`.
- The TUI expects stream-json output format; the adapter always emits JSON chunks + final result.
