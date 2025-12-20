# VIEW: Document New Module

**You're creating documentation for a module that exists in code but lacks proper docs.**

---

## WHY THIS VIEW EXISTS

Modules without documentation become black boxes. Future agents will:
- Reverse-engineer intent from implementation details
- Make changes that violate invisible design decisions
- Duplicate patterns that already exist

This view guides you through understanding the module deeply enough to document it properly.

---

## CONTEXT TO LOAD

**FIRST: Read all documentation listed below before writing docs.** You cannot document what you do not understand. Do not skip this step.

### Always

1. **Project state:** `.ngram/state/SYNC_Project_State.md`
   - Understand project context

2. **Module manifest:** `modules.yaml` (project root)
   - Check if this code already has a mapping
   - See related modules and dependencies

3. **The code itself:**
   - Read the module's source files
   - Trace its imports and dependencies
   - Run `ngram context {file}` to see what's connected

4. **Templates:**
   - `.ngram/templates/PATTERNS_TEMPLATE.md`
   - `.ngram/templates/SYNC_TEMPLATE.md`
   - Other templates as needed

### If Related Modules Exist

Check their docs for:
- Shared patterns you should reference
- Concepts this module might touch
- Conventions to follow

---

## THE WORK

### Phase 1: Understand

Before writing anything, answer these questions:

**Design (for PATTERNS):**
- Why does this module exist? What problem does it solve?
- What design approach was chosen? Why this over alternatives?
- What are the key invariants that must hold?
- What's in scope? What's explicitly out of scope (and where does that live instead)?

**Behavior (for BEHAVIORS):**
- What are the observable effects of this module?
- What inputs does it accept? What outputs does it produce?
- What side effects does it have?

**Logic (for ALGORITHM):**
- What's the step-by-step process?
- What are the key data structures?
- Where does complexity live?

**Verification (for VALIDATION):**
- How do you know it's working correctly?
- What are the edge cases?
- What could break?

**Architecture (for IMPLEMENTATION):**
- Where does the code live? What files/classes do what?
- How does data flow between modules?
- What are the entry points?
- What are the internal and external dependencies?

**Health (for HEALTH):**
- What verification mechanics exist?
- What health signals are monitored?
- How do you run the health checks?

### Phase 2: Name Descriptively

**Don't do this:**
```
PATTERNS_Auth.md
BEHAVIORS_Auth.md
```

**Do this:**
```
PATTERNS_Why_JWT_With_Refresh_Tokens.md
BEHAVIORS_Token_Lifecycle_And_Validation.md
ALGORITHM_Refresh_Token_Rotation.md
VALIDATION_Auth_Security_Invariants.md
IMPLEMENTATION_Auth_Code_Architecture.md
HEALTH_Auth_Verification.md
SYNC_Auth_Implementation_State.md
```

The name should tell you what insight the file contains, not just what module it's about.

### Phase 3: Write With Purpose

Each doc type serves a different reader need:

| Doc | Reader Question | Your Answer Should |
|-----|-----------------|-------------------|
| PATTERNS | "Why is it shaped this way?" | Explain design decisions and tradeoffs |
| BEHAVIORS | "What should it do?" | Describe observable effects, not implementation |
| ALGORITHM | "How does it work?" | Walk through the logic step-by-step |
| VALIDATION | "How do I verify it?" | List invariants, checks, verification steps |
| IMPLEMENTATION | "Where is the code?" | Code structure, data flows, entry points |
| HEALTH | "Is it healthy?" | Document verification mechanics and health signals |
| SYNC | "What's the current state?" | Status, recent changes, handoffs |

### Phase 4: Link the Chain

Every file should have a CHAIN block linking to related docs:

```
## CHAIN

PATTERNS:        ./PATTERNS_Why_JWT_With_Refresh_Tokens.md
BEHAVIORS:       ./BEHAVIORS_Token_Lifecycle_And_Validation.md
ALGORITHM:       ./ALGORITHM_Refresh_Token_Rotation.md
VALIDATION:      ./VALIDATION_Auth_Security_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Auth_Code_Architecture.md
HEALTH_Auth_Verification.md
THIS:            SYNC_Auth_Implementation_State.md
```

### Phase 5: Link Code to Docs

Add a DOCS reference in the main source file:

```python
# DOCS: docs/backend/auth/PATTERNS_Why_JWT_With_Refresh_Tokens.md
```

This enables `ngram context` to find the chain.

### Phase 6: Update Module Manifest

Add or update the mapping in `modules.yaml` (project root):

```yaml
modules:
  auth:
    code: "src/backend/auth/**"
    docs: "docs/backend/auth/"
    tests: "tests/auth/"

    maturity: DESIGNING          # or CANONICAL if stable
    owner: agent

    entry_points:
      - auth.py                  # Main file to start reading

    depends_on:
      - types
      - database

    patterns:
      - "JWT with refresh tokens"
      - "Middleware pattern"

    notes: |
      Authentication and authorization.
      See PATTERNS for why JWT over sessions.
```

This enables:
- `ngram validate` to check for unmapped code
- Agents to find docs from code paths
- Dependency tracking between modules

---

## MINIMUM VIABLE DOCUMENTATION

If you can't do the full chain, create at minimum:

1. **PATTERNS** — Why this design exists
2. **SYNC** — Current state
3. **modules.yaml entry** — Map code to docs

This passes validation and gives future agents something to build on.

---

## AFTER DOCUMENTATION

### Update State

Update `.ngram/state/SYNC_Project_State.md`:
- Module now has documentation
- Link to the new docs
- Any discoveries worth noting

### Handoffs

**For next agent:** The module is now documented. If they need to modify it, they should use VIEW_Implement and load these docs first.

---

## VERIFICATION

Before considering this complete:

- [ ] PATTERNS explains *why*, not just *what*
- [ ] Names are descriptive, not generic
- [ ] CHAIN links are valid (run `ngram validate`)
- [ ] Source file has DOCS: reference
- [ ] modules.yaml has mapping for this code
- [ ] SYNC reflects current state accurately
- [ ] Another agent could understand the module from your docs alone
