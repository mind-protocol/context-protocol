# Tools — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Tools.md
BEHAVIORS:       ./BEHAVIORS_Tools.md
ALGORITHM:       ./ALGORITHM_Tools.md
VALIDATION:      ./VALIDATION_Tools.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tools.md
HEALTH:          ./HEALTH_Tools.md
THIS:            ./SYNC_Tools.md
```

---

## CURRENT STATE

Documented the tools module so utility scripts are tracked in the protocol.
Added systemd user unit templates under `tools/systemd/user/`, a v3 ngrok
config at `tools/ngrok.yml`, and a WSL autostart guide at
`docs/infrastructure/wsl-autostart.md`. Added `.ngram/logs/` plus a
`.ngram/systemd.env` placeholder to wire frontend commands into systemd.
Added `blood-fe.service` to run the `the-blood-ledger` frontend and wired it
into `ngram-stack.target`.

## Agent Observations

### Remarks
- No frontend start command exists in-repo; `ngram-fe.service` now requires
  `FE_CMD` in `.ngram/systemd.env`.
- `ngram-fe.service` now targets `~/ngram/frontend`; the blood frontend has its
  own unit.

### Suggestions
- [ ] Confirm the exact frontend start command and update
  `.ngram/systemd.env` so `ngram-fe.service` can start cleanly.
- [ ] Confirm the blood frontend port/command once its build is finalized.

### Propositions
- If a canonical frontend repo exists, add a brief doc link here so future
  agents can locate its startup command quickly.

## TODO

- [ ] Add fixtures and run examples for each script to validate outputs.
