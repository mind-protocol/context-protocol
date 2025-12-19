# ngram TUI — Sync: Current State

```
LAST_UPDATED: 2025-12-18
UPDATED_BY: Claude (TUI session improvements)
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

**Status: FUNCTIONAL** — TUI working with Claude integration.

The TUI provides a Claude Code-style persistent chat interface for ngram. Entry point is `ngram` (no subcommand).

### Completed Features

#### Two-Panel Layout
- **Manager panel** (left, 45%): Displays orchestration messages, user input (magenta), Claude responses, thinking (collapsible)
- **Agent panel** (right, 55%): Shows SYNC_Project_State.md by default, agent panels during repair
- Responsive layout using Textual's Horizontal container
- Auto-scroll: All panels scroll to latest content when messages added (B10)
- Bottom padding on manager panel creates empty line above input bar

#### Status Bar
- **Left**: Project folder name (`ngram: {folder}`)
- **Right**: Health score with color coding (green ≥80, yellow ≥50, red <50)
- Dynamic width calculation for proper right-alignment
- Resize handling: Health score repositions automatically on terminal resize (B12)

#### Claude Integration
- Subprocess-based with `claude -p` and `--output-format stream-json`
- Conversation continuity via `--continue` flag (with fallback retry)
- System prompt from `.ngram/agents/manager/CLAUDE.md`
- Global learnings appended from `.ngram/views/GLOBAL_LEARNINGS.md`
- Streaming responses: Text streams to manager panel as it arrives (B6)
- Thinking blocks: 3-line preview with collapsible "Show more..." for longer thoughts
- Animated loading indicator (`. → .. → ...`) during Claude responses

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
- Up to 3 concurrent agents displayed in right panel
- Brown header showing: `{symbol} {issue_type}: {target_path}`
- Real-time streaming output with 100ms throttling
- Status colors: brown (running), green (completed), rust (failed)
- Output limited to last 50 lines to prevent slowdown

#### Error Handling
- All errors logged to `.ngram/error_log.txt` with timestamps
- Errors displayed in manager panel in red
- Infinite loop protection in error handler
- Chunk-based stdout reading (64KB) to avoid line length limits

#### Theme
- Paper & Parchment color palette (warm cream backgrounds, wood-tone text)
- Inline code: transparent background, dark bold text (#1a1a1a)
- Clean minimal design without footer
- Rich markup rendering (colors, bold, italic, dim)

### In Progress
- Queue management for >3 issues in repair

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

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Extend_Add_Features_To_Existing.md`

**Where I stopped:** TUI fully functional. Recent session added:
1. Command detection for interactive execution
2. Conversation history persistence
3. Agent panel streaming with throttling
4. Chunk-based stdout reading (fixes line length errors)
5. UI polish (colors, spacing, headers)

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
