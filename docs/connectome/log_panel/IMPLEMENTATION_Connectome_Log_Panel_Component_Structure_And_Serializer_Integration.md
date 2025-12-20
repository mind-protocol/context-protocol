```

# log_panel — Implementation: Component Structure and Serializer Integration

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Log_Panel_Unified_Explain_And_Copyable_Event_Ledger_View_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Log_Panel_Step_Clarity_And_Copyable_Audit_Trail_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Log_Panel_Log_Rendering_Duration_Coloring_And_Export.md
VALIDATION:      ./VALIDATION_Connectome_Log_Panel_Invariants_For_Truthful_Durations_And_Stable_Export.md
THIS:            IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md
HEALTH:          ./HEALTH_Connectome_Log_Panel_Runtime_Verification_Of_Log_Truth_And_Export_Integrity.md
SYNC:            ./SYNC_Connectome_Log_Panel_Sync_Current_State.md

IMPL:            app/connectome/components/unified_now_and_copyable_ledger_log_panel (planned) (PROPOSED)
```

---

## CODE STRUCTURE

```
app/
└── connectome/
├── components/
│   ├── unified_now_and_copyable_ledger_log_panel (planned)
│   ├── connectome_log_duration_formatting_and_threshold_color_rules (planned)
│   ├── connectome_log_trigger_and_calltype_badge_color_tokens (planned)
│   └── connectome_log_export_buttons_using_state_store_serializers (planned)
```

### File Responsibilities

| File                                                              | Responsibility              | Key Exports                               |
| ----------------------------------------------------------------- | --------------------------- | ----------------------------------------- |
| `unified_now_and_copyable_ledger_log_panel (planned)`                   | main panel UI               | `LogPanel`                                |
| `connectome_log_duration_formatting_and_threshold_color_rules (planned)` | duration text + color class | `formatDuration`, `durationColorClass`    |
| `connectome_log_trigger_and_calltype_badge_color_tokens (planned)`       | badge palettes              | `triggerBadgeClass`, `callTypeBadgeClass` |
| `connectome_log_export_buttons_using_state_store_serializers (planned)` | copy/export actions         | `ExportButtons`                           |

---

## ENTRY POINTS

| Entry                       | Trigger                 |
| --------------------------- | ----------------------- |
| `LogPanel()`                | /connectome page render |
| `ExportButtons.copyJsonl()` | copy JSONL              |
| `ExportButtons.copyText()`  | copy text               |

---

## DATA FLOW

```
state_store selectors
→ LogPanel renders Now and Ledger
→ ExportButtons serializes ledger and copies to clipboard
```

---

## CONFIGURATION

| Config                     | Default                  |
| -------------------------- | ------------------------ |
| `SHOW_RAW_PAYLOAD`         | false                    |
| `MAX_LOG_ENTRIES_RENDERED` | ? (depends on retention) |

---

## BIDIRECTIONAL LINKS

* TSX components reference docs/connectome/log_panel/*
* serialization utilities reference state_store serializer docs

---

## GAPS / IDEAS / QUESTIONS

* [ ] Decide whether “Copy log” copies JSONL by default or offers both (recommend: both buttons).
