# ngram TUI — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: codex (manager drift checks)
STATUS: IMPLEMENTED
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_TUI_Design.md
BEHAVIORS:       ./BEHAVIORS_TUI_Interactions.md
ALGORITHM:       ./ALGORITHM_TUI_Flow.md
VALIDATION:      ./VALIDATION_TUI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_TUI_Code_Architecture.md
TEST:            ./TEST_TUI_Coverage.md
THIS:            SYNC_TUI_State.md (you are here)
```

---

## CURRENT STATE

**Status: FUNCTIONAL** — TUI working with agent integration (Claude, Gemini, or Codex).

The TUI provides an agent-style persistent chat interface for ngram. Entry point is `ngram` (no subcommand).

### 2025-12-19: State helpers hardened

- Conversation history now handles non-positive limits and returns copies.
- Agent activity checks consider subprocess returncode.
- Session state de-duplicates agent handles by id and ignores empty manager messages.

### 2025-12-19: Manager drift detection hardening

- Drift parsing now recognizes non-markdown file updates beyond Python.
- Extracted paths are normalized to avoid punctuation artifacts.
- Claude PTY running state reflects subprocess exit.

### 2025-12-19: Module manifest mapping fixed

- `modules.yaml` now nests the `tui` entry under `modules` so widgets map to this doc chain.

### Completed Features

#### Two-Panel Layout
- **Manager panel** (left, 45%): Displays orchestration messages, user input (magenta), Claude responses, thinking (collapsible)
- **Agent panel** (right, 55%): Tabbed interface (CHANGES, SYNC, DOCTOR, MAP, AGENTS)
- Responsive layout using Textual's Horizontal container
- Auto-scroll: All panels scroll to latest content when messages added (B10)
- Bottom padding on manager panel creates empty line above input bar
- Parallelized startup: doctor, SYNC, map, git commands run concurrently

#### Status Bar
- **Left**: Project folder name (`ngram: {folder}`)
- **Right**: Health score with color coding (green ≥80, yellow ≥50, red <50)
- Dynamic width calculation for proper right-alignment
- Resize handling: Health score repositions automatically on terminal resize (B12)

#### Agent Integration
- Subprocess-based with `claude`, `gemini`, or `codex exec`
- Conversation continuity via `--continue` / `gemini --resume latest` / `codex exec resume --last`
- System prompt from `.ngram/agents/manager/CLAUDE.md` mirrored into `AGENTS.md`
- Global learnings appended from `.ngram/views/GLOBAL_LEARNINGS.md`
- Streaming responses for Claude; text output for Gemini/Codex
- Thinking blocks: 3-line preview with collapsible "Show more..." for longer thoughts (Claude only)
- Animated loading indicator (`. → .. → ...`) during agent responses

#### Command Detection
- Detects runnable commands in Claude responses (backticks, bold, code blocks, "Run X" patterns)
- Shows interactive numbered options: `1. ngram repair --depth full`
- User can type number to execute suggested command
- Supports ngram subcommands: doctor, repair, sync, init, validate, context, prompt

#### Input Handling
- Command routing (`/help`, `/repair`, `/doctor`, `/quit`, `/clear`, `/run`, `/issues`)
- `/run CMD` - Execute shell command with streaming output
- Non-command text sent to Claude manager
- User input echoed in magenta with blank line separator
- Input history: Up/Down arrows navigate previous commands (B8)
- Tab completion: Tab key completes `/` commands (B9)

#### Conversation History
- Persistent storage in `.ngram/state/conversation_history.json`
- Previous sessions displayed on TUI launch with separators
- Command outputs logged to history for later display

#### Agent Panels (during /repair)
- Up to 3 concurrent agents displayed in columns (side by side)
- Brown header showing: `{symbol} {issue_type}: {target_path}`
- Real-time streaming output with non-blocking updates via `call_later()`
- Status colors: copper (running), sage (completed), rust (failed)
- Output limited to last 50 lines to prevent slowdown
- Auto-collapse: Completed/failed agents collapse to header only (click to expand)
- 20 unique emoji symbols for agent identification
- Markdown widget for output (renders bold, code, lists)

#### Repair Session Folders
- Each `/repair` creates timestamped folder: `.ngram/repairs/{timestamp}/`
- Each agent gets subfolder with issue reference: `{index}-{issue_type}-{path_slug}`
- ISSUE.md created in each agent folder with issue details

#### Error Handling
- All errors logged to `.ngram/error_log.txt` with timestamps
- Errors displayed in manager panel in red
- Infinite loop protection in error handler
- Chunk-based stdout reading (64KB) to avoid line length limits

#### Theme
- Wood & Paper light theme (default) - paper backgrounds, wood text
- Key colors: #F5F0E6 (vellum screen), #FAF6ED (cream panels), #2C1810 (ebony text)
- Accents: #A0522D (rust), #B87333 (copper), #5F7A4A (sage)
- Dark theme also available (set `dark = True` in app.py)
- Clean minimal design without footer
- Rich markup rendering (colors, bold, italic, dim)

### In Progress
- Queue management for >3 issues in repair

### 2025-12-20: Added multi-agent provider support

- TUI accepts `--agents {claude,codex,gemini}` and uses the selected provider for manager and repairs
- Manager resumes sessions across turns for all providers

### Planned Features

#### Streaming & Display
- [x] Streaming responses - Stream text as it arrives (B6)
- [x] Auto-scroll - All panels auto-scroll to show latest content (B10)
- [x] Markdown rendering - SYNC file and responses render as markdown
- [ ] Syntax highlighting - Highlight code blocks in responses

#### Commands
- [x] `/issues` command - Switch right panel to show issues list
- [x] `/run` command - Execute shell commands with streaming output
- [ ] `/sync` auto-refresh - Right panel SYNC display refreshes automatically on file change
- [ ] `/repair --max N` - Configure max concurrent agents

#### Input
- [x] Input history - Up/down arrow to navigate previous commands (B8)
- [x] Tab completion - Complete `/` commands with Tab key (B9)
- [x] Command detection - Detect and offer to run commands from responses
- [ ] Right-click copy - Explicit copy functionality (terminal native works with Shift)

#### Layout
- [x] Resize handling - Status bar health alignment updates on terminal resize (B12)
- [x] Right panel scrolling - Long SYNC files wrapped in VerticalScroll (B10)
- [ ] Tab layout for >3 agents

### Known Gaps
- Tab layout for >3 agents not fully implemented
- Agent queue processing (issues beyond first 3) not implemented

---

## KNOWN ISSUES

None currently.

**Resolved 2025-12-18:**
- Previous BROKEN_IMPL_LINK resolved - IMPLEMENTATION doc now reflects actual implemented code
- INCOMPLETE_IMPL false positive resolved - `app.py` short methods (_startup_sequence, on_click,
  on_exception, action_doctor, action_repair, etc.) are complete implementations, just short
  delegating methods. Added to doctor-ignore.yaml.

**Resolved 2025-12-19:**
- INCOMPLETE_IMPL false positive in `widgets/input_bar.py` - 4 functions flagged (`CommandSubmitted.__init__`,
  `ShowSuggestions.__init__`, `value` getter/setter) are all properly implemented. These are standard
  Message subclass constructors (set attribute + super().__init__()) and property accessors (return/set
  self.text). Added to doctor-ignore.yaml.
- INCOMPLETE_IMPL false positive in `widgets/manager_panel.py` - 6 functions flagged (`__init__`,
  `on_mount`, `_is_at_bottom`, `_auto_scroll`, `add_tool_call`, `escape_markup`) are all complete.
  `__init__` calls super and inits _messages list; `on_mount` is intentionally empty (no header);
  scroll methods are 1-2 line implementations; `add_tool_call` is 30+ lines; `escape_markup` is
  a complete nested function. Added to doctor-ignore.yaml.
- INCOMPLETE_IMPL false positive in `app.py` - short UI actions (`action_doctor`, `action_repair`,
  tab switching, and input focus helpers) are complete delegating implementations. Added to
  doctor-ignore.yaml.
- INCOMPLETE_IMPL report in `tui/state.py` was outdated - all functions already implemented; no code change needed.
- INCOMPLETE_IMPL report in `widgets/status_bar.py` was outdated - all flagged methods already have implementations; no code change needed.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Extend_Add_Features_To_Existing.md`

**Where I stopped:** TUI fully functional. Recent session added:
1. Dark Wood & Paper theme with better contrast
2. Parallelized startup (doctor, SYNC, map, git run concurrently)
3. Agents displayed in columns (side by side layout)
4. Auto-collapse for completed/failed agents
5. Repair session folders with issue-based naming
6. UI performance fix: Non-blocking agent updates via `call_later()`, batched subprocess output with periodic yields

**What you need to understand:**
- TUI uses Textual framework (async, CSS styling)
- Integrates with `repair_core.py` for agent spawning via `spawn_repair_agent_async()`
- Theme in `styles/theme.tcss` - Paper & Parchment palette
- Commands in `commands.py`, app in `app.py`, widgets in `widgets/`

**Watch out for:**
- Textual is optional dependency — CLI must work without it
- Rich markup vs Markdown: `add_message()` auto-detects, but `[color]` patterns need Static not Markdown
- Stdout reading: Use 64KB chunks, not readline() to avoid length limit errors

---

## HANDOFF: FOR HUMAN

**Executive summary:**
TUI is functional with Claude integration, repair agent spawning, and conversation history.

**Decisions made:**
- Entry point: `ngram` (no subcommand)
- Layout: Manager left (45%), agents right (55%)
- Theme: Paper & Parchment (warm cream, wood tones)
- Max 3 concurrent agents during repair
- User input color: magenta
- Thinking: 3-line preview with collapsible expansion

**Needs your input:**
- Should `/repair --max N` be configurable?
- Priority for remaining features (syntax highlighting, tab layout, queue processing)

---

## Agent Observations

### Remarks
- INCOMPLETE_IMPL findings for short TUI action helpers were false positives and are now suppressed.
- State helper methods in `ngram/tui/state.py` now include guardrails (copying history slices, de-dup agent ids).
- Verified `ngram/tui/state.py` functions are fully implemented; no empty stubs remain.
- Manager drift detection now normalizes file paths and checks PTY subprocess state.

### Suggestions
- [ ] Keep doctor-ignore and SYNC notes updated together to avoid drift.

### Propositions
- If more false positives appear, consider refining the doctor heuristic for short methods.

---

## POINTERS

| What | Where |
|------|-------|
| Design rationale | `docs/tui/PATTERNS_TUI_Design.md` |
| Shared repair logic | `ngram/repair_core.py` |
| CLI integration point | `ngram/cli.py` |
| Implementation plan | `/home/mind-protocol/.claude/plans/structured-cooking-alpaca.md` |


---

## ARCHIVE

Older content archived to: `SYNC_TUI_State_archive_2025-12.md`
