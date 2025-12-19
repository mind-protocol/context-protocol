# VIEW: Health — Define Health Checks and Verify System Health

**Vision:** HEALTH makes the system observable and trustworthy for humans and agents.
**Pattern:** A continuously running top-layer of docking-based checks that map to VALIDATION and run at safe, throttled rates without touching implementation files whenever possible.

---

## WHY THIS VIEW EXISTS

Code can pass tests and still fail in the real world. HEALTH exists to close that gap by making runtime behavior observable and trustworthy, continuously and explicitly. It gives humans and agents a shared operational language so they can detect risk, drift, and degradation before they become incidents. Without this, teams rely on intuition, ad-hoc logs, or post‑incident forensics — which is too late.

HEALTH is not about exhaustive testing. It is about the most meaningful signals: the ones tied to safety, correctness, money, security, state integrity, and user-visible outcomes. This view ensures those signals are defined, traced to VALIDATION criteria, and anchored to concrete docking points in the actual data flow.

---

## CONTEXT TO LOAD

**FIRST: Read all documentation listed below before defining HEALTH.** HEALTH verifies intent, and you must understand intent first. Do not skip this step. Skipping context leads to false signals, missed risk, or checks that cannot be implemented without invasive changes.

### For the Module You're Checking

```
docs/{area}/{module}/VALIDATION_*.md      — what invariants must hold
docs/{area}/{module}/BEHAVIORS_*.md       — what should be observable
docs/{area}/{module}/PATTERNS_*.md        — why the design exists
docs/{area}/{module}/IMPLEMENTATION_*.md  — flows + available docking points
```

### Existing Health Docs

```
docs/{area}/{module}/HEALTH_*.md
```

Understand what signals already exist, how they are throttled, and what gaps remain.

---

## WHAT TO DEFINE

You are not trying to cover everything. You are trying to define the handful of checks that make the system trustworthy under real conditions. This is a prioritization exercise: choose what matters most, then design minimal, observable checks around it.

### 1. Identify What Matters

From VALIDATION + BEHAVIORS, decide the vital signals for humans and agents. These are the checks that, if broken, cause harm or uncertainty:
- correctness, safety, money, security
- user-visible outputs
- state integrity and persistence
- cross-boundary IO (files, APIs, queues, DBs)

### 2. Choose Flows and Docks

Use IMPLEMENTATION to:
- pick the flows that are risky, transformative, or cross boundaries
- list all available docking points per flow
- select only significant docks for HEALTH (avoid trivial pass-throughs)

If a required dock does not exist, update IMPLEMENTATION to declare it and record the need for a hook in SYNC. HEALTH depends on visibility; if you cannot observe a critical boundary, the system is effectively unverifiable.

### 3. Design Checkers

For each checker:
- define input/output docks (by dock ID)
- define verification mechanisms (input vs output compared to VALIDATION)
- define throttling parameters
- define flags and link each to VALIDATION criteria
- define forwarding + display locations

Avoid “busywork” checkers. If a checker does not clearly support a VALIDATION criterion, drop it.

### 4. Choose Health Representation

Select how health is represented (binary, float, enum, tuple, vector) and how it aggregates. Keep it consistent with display surfaces, and ensure aggregation does not hide critical failures.

---

## WRITING GOOD HEALTH

**Use docking points, not implementation changes.** HEALTH should observe, not rewrite.

**Mirror VALIDATION language.** If VALIDATION says "must never," HEALTH should check that directly.

**Throttling is not optional.** HEALTH should run at safe cadence and avoid noisy signals.

**Prefer clarity over coverage.** A small set of well‑designed checks is better than a large set of vague ones.

---

## AFTER DEFINING HEALTH

### Update HEALTH Doc

- Fill in HEALTH_{name}.md using the template
- Ensure every flag links to VALIDATION criteria
- Ensure every checker uses dock IDs from IMPLEMENTATION

### Update SYNC

Note:
- what health checks were added or changed
- what docks are used
- what remains unverified

If a VALIDATION criterion remains unchecked, explicitly list it as a gap.

---

## OBSERVATIONS (Living Documentation)

**At the end of your work, add observations to SYNC AND relevant docs.**

### Remarks
What did you notice? Missing docks, unclear flows, unverifiable validation, or mismatched expectations between VALIDATION and actual data flow.
→ Add to SYNC and relevant VALIDATION/IMPLEMENTATION docs

### Suggestions
What should be improved? Additional docks, better throttling, missing checks.
→ Add to SYNC with `[ ]` checkbox - these become actionable items

### Propositions
What health checks should exist? Cross-module checks, aggregation surfaces.
→ Add to SYNC and HEALTH docs

**Format in SYNC:**
```markdown
## Agent Observations

### Remarks
- [What you noticed]

### Suggestions
- [ ] [Actionable improvement] <!-- Repair will prompt user -->

### Propositions
- [Future health improvements]
```

---

## HANDOFF

**For next agent:** What health checks exist, what docks are used, what is still missing.

**For human:** Health signal summary, any gaps or operational risks.

---

## VERIFICATION

- HEALTH checks run (throttled)
- Signals align with VALIDATION
- HEALTH doc updated
- SYNC updated
- Observations documented

---

## DOCTOR FALSE POSITIVES

If `/doctor` flags a false positive, add this line directly under the doc's `UPDATED: YYYY-MM-DD` metadata line:

`@ngram:doctor:CHECK_TYPE_NAME:false_positive Explanation message`

Place it in the doc referenced by the affected code's `DOCS:` line (or the closest module doc).
