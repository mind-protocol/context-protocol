# Repository Map: ngram

*Generated: 2025-12-22 19:22*

- **Files:** 529
- **Directories:** 133
- **Total Size:** 4.6M
- **Doc Files:** 405
- **Code Files:** 113
- **Areas:** 17 (docs/ subfolders)
- **Modules:** 49 (subfolders in areas)
- **DOCS Links:** 72 (0.64 avg per code file)

- markdown: 405
- python: 86
- tsx: 13
- typescript: 11
- css: 2
- shell: 1

```
├── agents/ (37.8K)
│   ├── narrator/ (9.8K)
│   │   └── CLAUDE.md (9.8K)
│   └── world_runner/ (28.0K)
│       └── CLAUDE.md (28.0K)
├── app/ (95.1K)
│   ├── api/ (7.5K)
│   │   ├── connectome/ (6.3K)
│   │   │   ├── graph/ (1.7K)
│   │   │   │   └── route.ts (1.7K)
│   │   │   ├── graphs/ (1.6K)
│   │   │   │   └── route.ts (1.6K) →
│   │   │   └── search/ (3.0K)
│   │   │       └── route.ts (3.0K)
│   │   └── sse/ (1.2K)
│   │       └── route.ts (1.2K)
│   ├── connectome/ (84.9K)
│   │   ├── components/ (71.3K)
│   │   │   ├── edge_kit/ (8.5K)
│   │   │   │   ├── connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx (937) →
│   │   │   │   ├── connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts (907) →
│   │   │   │   ├── connectome_node_boundary_intersection_geometry_helpers.ts (961) →
│   │   │   │   ├── semantic_edge_components_with_directional_shine_and_pulses.tsx (4.9K) →
│   │   │   │   └── (..2 more files)
│   │   │   ├── node_kit/ (14.1K)
│   │   │   │   ├── connectome_energy_badge_bucketed_glow_and_value_formatter.tsx (811) →
│   │   │   │   ├── connectome_node_background_theme_tokens_by_type_and_language.ts (1.3K) →
│   │   │   │   ├── connectome_node_frame_with_title_path_and_tooltip_shell.tsx (1.2K) →
│   │   │   │   ├── connectome_node_step_list_and_active_step_highlighter.tsx (1.3K) →
│   │   │   │   ├── connectome_player_wait_progress_bar_with_four_second_cap.tsx (2.0K) →
│   │   │   │   ├── connectome_tick_cron_circular_progress_ring_with_speed_label.tsx (2.4K) →
│   │   │   │   └── typed_connectome_node_components_with_energy_and_step_highlighting.tsx (5.1K) →
│   │   │   ├── connectome_health_panel.tsx (3.9K) →
│   │   │   ├── connectome_log_duration_formatting_and_threshold_color_rules.ts (808) →
│   │   │   ├── connectome_log_export_buttons_using_state_store_serializers.tsx (1.3K) →
│   │   │   ├── connectome_log_trigger_and_calltype_badge_color_tokens.ts (1.1K) →
│   │   │   ├── connectome_page_shell_route_layout_and_control_surface.tsx (10.9K) →
│   │   │   ├── deterministic_zone_and_node_layout_computation_helpers.ts (3.5K) →
│   │   │   ├── edge_label_declutter_and_visibility_policy_helpers.ts (898) →
│   │   │   ├── pannable_zoomable_zoned_flow_canvas_renderer.tsx (19.9K) →
│   │   │   └── unified_now_and_copyable_ledger_log_panel.tsx (6.5K) →
│   │   ├── connectome.css (13.3K)
│   │   └── (..1 more files)
│   ├── ngram/ (216)
│   │   └── (..1 more files)
│   ├── globals.css (1.9K)
│   └── (..2 more files)
├── docs/ (2.5M)
│   ├── agents/ (217.4K)
│   │   ├── narrator/ (112.3K)
│   │   │   ├── archive/ (20.5K)
│   │   │   │   └── SYNC_archive_2024-12.md (20.5K)
│   │   │   ├── ALGORITHM_Scene_Generation.md (10.8K)
│   │   │   ├── BEHAVIORS_Narrator.md (5.0K)
│   │   │   ├── HEALTH_Narrator.md (13.0K)
│   │   │   ├── IMPLEMENTATION_Narrator.md (10.5K)
│   │   │   ├── PATTERNS_Narrator.md (7.8K)
│   │   │   ├── SYNC_Narrator.md (11.4K)
│   │   │   ├── SYNC_Narrator_archive_2025-12.md (15.4K)
│   │   │   ├── TEMPLATE_Player_Notes.md (1.8K)
│   │   │   ├── TOOL_REFERENCE.md (3.2K)
│   │   │   ├── VALIDATION_Narrator.md (8.6K)
│   │   │   └── (..4 more files)
│   │   └── world-runner/ (105.0K)
│   │       ├── archive/ (23.7K)
│   │       │   └── SYNC_archive_2024-12.md (23.7K)
│   │       ├── ALGORITHM_World_Runner.md (11.3K)
│   │       ├── BEHAVIORS_World_Runner.md (8.0K)
│   │       ├── HEALTH_World_Runner.md (13.3K)
│   │       ├── IMPLEMENTATION_World_Runner_Service_Architecture.md (8.4K)
│   │       ├── INPUT_REFERENCE.md (1.8K)
│   │       ├── PATTERNS_World_Runner.md (7.4K)
│   │       ├── SYNC_World_Runner.md (16.2K)
│   │       ├── TEST_World_Runner_Coverage.md (3.6K)
│   │       ├── TOOL_REFERENCE.md (4.3K)
│   │       ├── VALIDATION_World_Runner_Invariants.md (6.3K)
│   │       └── (..1 more files)
│   ├── api/ (4.5K)
│   │   └── sse/ (4.5K)
│   │       ├── OBJECTIFS_SSE_API.md (1.2K)
│   │       ├── PATTERNS_SSE_API.md (2.6K)
│   │       └── SYNC_SSE_API.md (644)
│   ├── architecture/ (56.1K)
│   │   └── cybernetic_studio_architecture/ (56.1K)
│   │       ├── ALGORITHM_Cybernetic_Studio_Process_Flow.md (4.4K)
│   │       ├── BEHAVIORS_Cybernetic_Studio_System_Behaviors.md (7.4K)
│   │       ├── HEALTH_Cybernetic_Studio_Health_Checks.md (7.6K)
│   │       ├── IMPLEMENTATION_Cybernetic_Studio_Code_Structure.md (8.4K)
│   │       ├── OBJECTIFS_Cybernetic_Studio_Architecture_Goals.md (798)
│   │       ├── PATTERNS_Cybernetic_Studio_Architecture.md (16.1K)
│   │       ├── SYNC_Cybernetic_Studio_Architecture_State.md (6.3K)
│   │       └── VALIDATION_Cybernetic_Studio_Architectural_Invariants.md (5.0K)
│   ├── cli/ (137.8K)
│   │   ├── archive/ (5.4K)
│   │   │   ├── SYNC_CLI_Development_State_archive_2025-12.md (581)
│   │   │   ├── SYNC_CLI_State_Archive_2025-12.md (4.3K)
│   │   │   └── (..1 more files)
│   │   ├── core/ (68.8K)
│   │   │   ├── ALGORITHM_CLI_Command_Execution_Logic/ (8.0K)
│   │   │   │   └── ALGORITHM_Overview.md (8.0K)
│   │   │   ├── IMPLEMENTATION_CLI_Code_Architecture/ (24.4K)
│   │   │   │   ├── overview/ (6.2K)
│   │   │   │   │   └── IMPLEMENTATION_Overview.md (6.2K)
│   │   │   │   ├── runtime/ (5.7K)
│   │   │   │   │   └── IMPLEMENTATION_Runtime_And_Dependencies.md (5.7K)
│   │   │   │   ├── schema/ (4.6K)
│   │   │   │   │   └── IMPLEMENTATION_Schema.md (4.6K)
│   │   │   │   └── structure/ (8.0K)
│   │   │   │       └── IMPLEMENTATION_Code_Structure.md (8.0K)
│   │   │   ├── BEHAVIORS_CLI_Command_Effects.md (7.6K)
│   │   │   ├── HEALTH_CLI_Command_Test_Coverage.md (6.8K)
│   │   │   ├── PATTERNS_Why_CLI_Over_Copy.md (6.0K)
│   │   │   ├── SYNC_CLI_Development_State.md (10.3K)
│   │   │   └── VALIDATION_CLI_Instruction_Invariants.md (5.7K)
│   │   ├── prompt/ (39.8K)
│   │   │   ├── ALGORITHM_Prompt_Bootstrap_Prompt_Construction.md (4.4K)
│   │   │   ├── BEHAVIORS_Prompt_Command_Output_and_Flow.md (3.5K)
│   │   │   ├── HEALTH_Prompt_Runtime_Verification.md (6.8K)
│   │   │   ├── IMPLEMENTATION_Prompt_Code_Architecture.md (7.8K)
│   │   │   ├── PATTERNS_Prompt_Command_Workflow_Design.md (4.7K)
│   │   │   ├── SYNC_Prompt_Command_State.md (7.7K)
│   │   │   └── VALIDATION_Prompt_Bootstrap_Invariants.md (4.8K)
│   │   ├── ALGORITHM_CLI_Command_Execution_Logic.md (4.7K)
│   │   ├── BEHAVIORS_CLI_Module_Command_Surface_Effects.md (770)
│   │   ├── HEALTH_CLI_Module_Verification.md (602)
│   │   ├── IMPLEMENTATION_CLI_Code_Architecture.md (13.3K)
│   │   ├── OBJECTIFS_Cli_Goals.md (690)
│   │   ├── PATTERNS_CLI_Module_Overview_And_Scope.md (1.0K)
│   │   ├── VALIDATION_CLI_Module_Invariants.md (732)
│   │   ├── modules.md (1.8K)
│   │   └── (..1 more files)
│   ├── concepts/ (1.3K)
│   │   └── tempo-controller/ (1.3K)
│   │       └── CONCEPT_Tempo_Controller.md (1.3K)
│   ├── connectome/ (583.3K)
│   │   ├── edge_kit/ (57.1K)
│   │   │   ├── ALGORITHM_Connectome_Edge_Kit_Edge_Rendering_Pulse_Shine_And_Label_Placement_Rules.md (4.0K)
│   │   │   ├── BEHAVIORS_Connectome_Edge_Kit_Readable_Directional_And_Truthful_Link_Effects.md (7.3K)
│   │   │   ├── HEALTH_Connectome_Edge_Kit_Runtime_Verification_Of_Link_Visibility_And_Semantic_Styling.md (7.3K)
│   │   │   ├── IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md (13.5K)
│   │   │   ├── OBJECTIFS_Edge_Kit_Goals.md (710)
│   │   │   ├── PATTERNS_Connectome_Edge_Kit_Color_Coded_Trigger_Typed_Directional_Link_Styling_Patterns.md (7.6K)
│   │   │   ├── SYNC_Connectome_Edge_Kit_Sync_Current_State.md (10.4K)
│   │   │   └── VALIDATION_Connectome_Edge_Kit_Invariants_For_Color_Dash_And_Pulse_Truth.md (6.4K)
│   │   ├── event_model/ (43.6K)
│   │   │   ├── ALGORITHM_Connectome_Event_Normalization_And_Rendering_Event_Synthesis.md (6.3K)
│   │   │   ├── BEHAVIORS_Connectome_Event_Model_Observable_Event_Stream_Effects.md (4.9K)
│   │   │   ├── HEALTH_Connectome_Event_Model_Runtime_Verification_And_Signal_Coverage.md (8.3K)
│   │   │   ├── IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md (10.7K)
│   │   │   ├── OBJECTIFS_Event_Model_Goals.md (722)
│   │   │   ├── PATTERNS_Connectome_Event_Model_Contract_And_Normalization_Patterns.md (6.2K)
│   │   │   ├── SYNC_Connectome_Event_Model_Sync_Current_State.md (1.6K)
│   │   │   └── VALIDATION_Connectome_Event_Model_Invariants_And_Error_Conditions.md (4.9K)
│   │   ├── feature_shell/ (1.8K)
│   │   │   └── OBJECTIFS_Connectome_Feature_Shell.md (1.8K)
│   │   ├── flow_canvas/ (69.4K)
│   │   │   ├── ALGORITHM_Connectome_Flow_Canvas_Layout_Zones_And_Edge_Label_Decluttering.md (8.3K)
│   │   │   ├── BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md (4.5K)
│   │   │   ├── HEALTH_Connectome_Flow_Canvas_Runtime_Verification_Of_Render_Stability_And_Perf_Budgets.md (11.4K)
│   │   │   ├── IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md (12.6K)
│   │   │   ├── OBJECTIFS_Flow_Canvas_Goals.md (722)
│   │   │   ├── PATTERNS_Connectome_Flow_Canvas_Pannable_Zoomable_Zoned_System_Map_Rendering_Patterns.md (9.1K)
│   │   │   ├── SYNC_Connectome_Flow_Canvas_Sync_Current_State.md (17.4K)
│   │   │   └── VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md (5.4K)
│   │   ├── graph_api/ (6.1K)
│   │   │   ├── OBJECTIFS_Graph_API.md (1.4K)
│   │   │   └── PATTERNS_Graph_API.md (4.7K)
│   │   ├── graphs/ (4.6K)
│   │   │   ├── OBJECTIFS_Connectome_Graphs.md (1.4K)
│   │   │   ├── PATTERNS_Connectome_Graphs.md (1.8K)
│   │   │   └── SYNC_Connectome_Graphs_Sync_Current_State.md (1.4K)
│   │   ├── health/ (9.1K)
│   │   │   ├── CONNECTOME_HEALTH_PAYLOAD.md (965)
│   │   │   ├── HEALTH_Connectome_Live_Signals.md (6.0K)
│   │   │   ├── INTEGRATION_NOTES.md (1.3K)
│   │   │   └── OBJECTIFS_Connectome_Health.md (836)
│   │   ├── health_panel/ (6.2K)
│   │   │   ├── OBJECTIFS_Connectome_Health_Panel_Metrics_Display_And_Realtime_Feedback.md (1.5K)
│   │   │   └── PATTERNS_Connectome_Health_Panel_Live_Monitoring_And_Invariants_Visualization.md (4.7K)
│   │   ├── log_panel/ (72.1K)
│   │   │   ├── ALGORITHM_Connectome_Log_Panel_Log_Rendering_Duration_Coloring_And_Export.md (11.9K)
│   │   │   ├── BEHAVIORS_Connectome_Log_Panel_Step_Clarity_And_Copyable_Audit_Trail_Effects.md (4.5K)
│   │   │   ├── HEALTH_Connectome_Log_Panel_Runtime_Verification_Of_Log_Truth_And_Export_Integrity.md (15.4K)
│   │   │   ├── IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md (12.3K)
│   │   │   ├── OBJECTIFS_Log_Panel_Goals.md (714)
│   │   │   ├── PATTERNS_Connectome_Log_Panel_Unified_Explain_And_Copyable_Event_Ledger_View_Patterns.md (6.1K)
│   │   │   ├── SYNC_Connectome_Log_Panel_Sync_Current_State.md (15.5K)
│   │   │   └── VALIDATION_Connectome_Log_Panel_Invariants_For_Truthful_Durations_And_Stable_Export.md (5.6K)
│   │   ├── node_kit/ (84.1K)
│   │   │   ├── ALGORITHM_Connectome_Node_Kit_Node_Rendering_Spec_And_Energy_Glow_Mapping.md (10.1K)
│   │   │   ├── BEHAVIORS_Connectome_Node_Kit_Visible_Clarity_And_Trust_Effects.md (4.7K)
│   │   │   ├── HEALTH_Connectome_Node_Kit_Runtime_Verification_Of_Node_State_And_Visual_Signal_Truth.md (21.2K)
│   │   │   ├── IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md (13.2K)
│   │   │   ├── OBJECTIFS_Node_Kit_Goals.md (710)
│   │   │   ├── PATTERNS_Connectome_Node_Kit_Typed_Language_Coded_Energy_Aware_Node_Rendering_Patterns.md (7.2K)
│   │   │   ├── SYNC_Connectome_Node_Kit_Sync_Current_State.md (4.3K)
│   │   │   ├── SYNC_Connectome_Node_Kit_Sync_Current_State_archive_2025-12.md (15.6K)
│   │   │   └── VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md (7.0K)
│   │   ├── page_shell/ (13.5K)
│   │   │   ├── ALGORITHM_Connectome_Page_Shell_Control_Dispatch_And_Layout_Composition.md (1.0K)
│   │   │   ├── BEHAVIORS_Connectome_Page_Shell_Stable_Workflow_And_Mode_Control_Effects.md (1.1K)
│   │   │   ├── HEALTH_Connectome_Page_Shell_Runtime_Verification_Of_Control_Semantics_And_Mode_Gating.md (1.1K)
│   │   │   ├── IMPLEMENTATION_Connectome_Page_Shell_Nextjs_Route_And_Component_Wiring.md (1.0K)
│   │   │   ├── OBJECTIFS_Page_Shell_Goals.md (718)
│   │   │   ├── PATTERNS_Connectome_Page_Shell_Route_Composition_And_User_Control_Surface_Patterns.md (5.4K)
│   │   │   ├── SYNC_Connectome_Page_Shell_Sync_Current_State.md (2.1K)
│   │   │   └── VALIDATION_Connectome_Page_Shell_Invariants_For_Control_Correctness_And_No_Drift.md (1.1K)
│   │   ├── runtime_engine/ (75.7K)
│   │   │   ├── ALGORITHM_Connectome_Runtime_Engine_Step_Release_And_Realtime_Scheduling.md (6.6K)
│   │   │   ├── BEHAVIORS_Connectome_Runtime_Engine_User_Controlled_Traversal_Effects.md (6.5K)
│   │   │   ├── HEALTH_Connectome_Runtime_Engine_Runtime_Verification_Of_Pacing_And_Order.md (16.4K)
│   │   │   ├── IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md (12.6K)
│   │   │   ├── OBJECTIFS_Runtime_Engine_Goals.md (734)
│   │   │   ├── PATTERNS_Connectome_Runtime_Engine_Stepper_And_Realtime_Traversal_Control_Patterns.md (11.7K)
│   │   │   ├── SYNC_Connectome_Runtime_Engine_Sync_Current_State.md (14.9K)
│   │   │   └── VALIDATION_Connectome_Runtime_Engine_Invariants_For_Stepper_And_Realtime.md (6.3K)
│   │   ├── search_api/ (10.3K)
│   │   │   ├── OBJECTIFS_Connectome_Search_API_Objectives.md (2.2K)
│   │   │   └── PATTERNS_Connectome_Search_API_Design_Patterns.md (8.1K)
│   │   ├── state_store/ (95.4K)
│   │   │   ├── ALGORITHM_Connectome_State_Store_Atomic_Commits_For_Step_Releases_And_Realtime.md (10.1K)
│   │   │   ├── BEHAVIORS_Connectome_State_Store_Observable_State_Consistency_Effects.md (5.8K)
│   │   │   ├── HEALTH_Connectome_State_Store_Runtime_Verification_Of_Ledger_And_Timer_Correctness.md (33.4K)
│   │   │   ├── IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md (10.6K)
│   │   │   ├── OBJECTIFS_State_Store_Goals.md (722)
│   │   │   ├── PATTERNS_Connectome_State_Store_Single_Source_Of_Truth_For_Events_Focus_And_Timers.md (8.9K)
│   │   │   ├── SYNC_Connectome_State_Store_Sync_Current_State.md (4.4K)
│   │   │   ├── SYNC_Connectome_State_Store_Sync_Current_State_archive_2025-12.md (15.9K)
│   │   │   └── VALIDATION_Connectome_State_Store_Invariants_For_Ledger_Ordering_And_Focus.md (5.7K)
│   │   ├── telemetry_adapter/ (24.7K)
│   │   │   ├── ALGORITHM_Connectome_Telemetry_Adapter_Sse_Subscription_Event_Parsing_And_Raw_Event_Emission.md (3.4K)
│   │   │   ├── BEHAVIORS_Connectome_Telemetry_Adapter_Realtime_Ingestion_Buffering_And_Backpressure_Effects.md (3.1K)
│   │   │   ├── HEALTH_Connectome_Telemetry_Adapter_Runtime_Verification_Of_Stream_Integrity_And_Buffer_Bounds.md (3.8K)
│   │   │   ├── IMPLEMENTATION_Connectome_Telemetry_Adapter_Code_Structure_For_Sse_And_Snapshot_Docking.md (4.2K)
│   │   │   ├── OBJECTIFS_Telemetry_Adapter_Goals.md (746)
│   │   │   ├── PATTERNS_Connectome_Telemetry_Adapter_Sse_To_FlowEvent_Normalization_Docking_Patterns.md (5.1K)
│   │   │   ├── SYNC_Connectome_Telemetry_Adapter_Sync_Current_State.md (1.4K)
│   │   │   └── VALIDATION_Connectome_Telemetry_Adapter_Invariants_For_No_Dropped_Events_And_Stable_Order.md (3.0K)
│   │   └── VISUAL_STYLEGUIDE_Connectome.md (9.7K)
│   ├── core_utils/ (34.1K)
│   │   ├── ALGORITHM_Template_Path_Resolution_And_Doc_Discovery.md (3.9K)
│   │   ├── BEHAVIORS_Core_Utils_Helper_Effects.md (3.6K)
│   │   ├── HEALTH_Core_Utils_Verification.md (7.4K)
│   │   ├── IMPLEMENTATION_Core_Utils_Code_Architecture.md (8.3K)
│   │   ├── OBJECTIFS_Core_Utils_Goals.md (718)
│   │   ├── PATTERNS_Core_Utils_Functions.md (2.2K)
│   │   ├── SYNC_Core_Utils_State.md (4.3K)
│   │   └── VALIDATION_Core_Utils_Invariants.md (3.6K)
│   ├── engine/ (124.7K)
│   │   ├── membrane/ (32.7K)
│   │   │   ├── ALGORITHM_Membrane_Modulation.md (4.3K)
│   │   │   ├── BEHAVIORS_Membrane_Modulation.md (4.5K)
│   │   │   ├── HEALTH_Membrane_Modulation.md (2.8K)
│   │   │   ├── IMPLEMENTATION_Membrane_Modulation.md (2.5K)
│   │   │   ├── PATTERNS_Membrane_Scoping.md (7.0K)
│   │   │   ├── PATTERN_Membrane_Modulation.md (5.1K)
│   │   │   ├── SYNC_Membrane_Modulation.md (3.2K)
│   │   │   └── VALIDATION_Membrane_Modulation.md (3.3K)
│   │   ├── models/ (42.8K)
│   │   │   ├── ALGORITHM_Models.md (6.0K)
│   │   │   ├── BEHAVIORS_Models.md (4.0K)
│   │   │   ├── HEALTH_Models.md (4.4K)
│   │   │   ├── IMPLEMENTATION_Models.md (10.9K)
│   │   │   ├── PATTERNS_Models.md (6.8K)
│   │   │   ├── SYNC_Models.md (5.6K)
│   │   │   └── VALIDATION_Models.md (5.1K)
│   │   ├── moment-graph-engine/ (31.1K)
│   │   │   ├── validation/ (6.5K)
│   │   │   │   ├── player_dmz/ (2.4K)
│   │   │   │   │   └── VALIDATION_Player_DMZ.md (2.4K)
│   │   │   │   ├── simultaneity_contradiction/ (1.8K)
│   │   │   │   │   └── VALIDATION_Simultaneity_Contradiction.md (1.8K)
│   │   │   │   └── void_tension/ (2.3K)
│   │   │   │       └── VALIDATION_Void_Tension.md (2.3K)
│   │   │   ├── ALGORITHM_Click_Wait_Surfacing.md (3.1K)
│   │   │   ├── BEHAVIORS_Traversal_And_Surfacing.md (2.4K)
│   │   │   ├── IMPLEMENTATION_Moment_Graph_Runtime_Layout.md (2.4K)
│   │   │   ├── PATTERNS_Instant_Traversal_Moment_Graph.md (3.7K)
│   │   │   ├── SYNC_Moment_Graph_Engine.md (2.9K)
│   │   │   ├── SYNC_Moment_Graph_Engine_archive_2025-12.md (6.1K)
│   │   │   ├── TEST_Moment_Graph_Runtime_Coverage.md (1.8K)
│   │   │   └── VALIDATION_Moment_Traversal_Invariants.md (2.2K)
│   │   ├── moments/ (11.8K)
│   │   │   ├── ALGORITHM_Moment_Graph_Operations.md (1.3K)
│   │   │   ├── BEHAVIORS_Moment_Lifecycle.md (1.4K)
│   │   │   ├── IMPLEMENTATION_Moment_Graph_Stub.md (868)
│   │   │   ├── PATTERNS_Moments.md (3.7K)
│   │   │   ├── SYNC_Moments.md (2.1K)
│   │   │   ├── TEST_Moment_Graph_Coverage.md (1.3K)
│   │   │   └── VALIDATION_Moment_Graph_Invariants.md (1.1K)
│   │   ├── ALGORITHM_Engine.md (687)
│   │   ├── BEHAVIORS_Engine.md (865)
│   │   ├── HEALTH_Engine.md (515)
│   │   ├── IMPLEMENTATION_Engine.md (848)
│   │   ├── OBJECTIFS_Engine_Goals.md (702)
│   │   ├── PATTERNS_Engine.md (1.1K)
│   │   ├── SYNC_Engine.md (802)
│   │   └── VALIDATION_Engine.md (666)
│   ├── frontend/ (17.6K)
│   │   └── app_shell/ (17.6K)
│   │       ├── OBJECTIFS_App_Shell.md (2.2K)
│   │       ├── PATTERNS_App_Shell.md (7.9K)
│   │       └── SYNC_App_Shell_State.md (7.6K)
│   ├── infrastructure/ (158.2K)
│   │   ├── api/ (69.9K)
│   │   │   ├── ALGORITHM_Api.md (19.9K)
│   │   │   ├── ALGORITHM_Player_Input_Flow.md (7.3K)
│   │   │   ├── API_Graph_Management.md (4.3K)
│   │   │   ├── BEHAVIORS_Api.md (2.2K)
│   │   │   ├── HEALTH_Api.md (3.7K)
│   │   │   ├── IMPLEMENTATION_Api.md (7.8K)
│   │   │   ├── PATTERNS_Api.md (2.9K)
│   │   │   ├── SYNC_Api.md (4.0K)
│   │   │   ├── SYNC_Api_archive_2025-12.md (13.9K)
│   │   │   ├── VALIDATION_Api.md (2.4K)
│   │   │   └── (..2 more files)
│   │   ├── scene-memory/ (57.2K)
│   │   │   ├── archive/ (2.5K)
│   │   │   │   └── SYNC_archive_2024-12.md (2.5K)
│   │   │   ├── ALGORITHM_Scene_Memory.md (8.6K)
│   │   │   ├── BEHAVIORS_Scene_Memory.md (5.0K)
│   │   │   ├── HEALTH_Scene_Memory.md (518)
│   │   │   ├── IMPLEMENTATION_Scene_Memory.md (5.5K)
│   │   │   ├── OBJECTIFS_Scene_Memory_Goals.md (726)
│   │   │   ├── PATTERNS_Scene_Memory.md (4.7K)
│   │   │   ├── SYNC_Scene_Memory.md (6.0K)
│   │   │   ├── SYNC_Scene_Memory_archive_2025-12.md (15.2K)
│   │   │   ├── TEST_Scene_Memory.md (3.4K)
│   │   │   └── VALIDATION_Scene_Memory.md (5.1K)
│   │   ├── tempo/ (27.9K)
│   │   │   ├── ALGORITHM_Tempo_Controller.md (3.1K)
│   │   │   ├── BEHAVIORS_Tempo.md (3.0K)
│   │   │   ├── HEALTH_Tempo.md (4.9K)
│   │   │   ├── IMPLEMENTATION_Tempo.md (7.0K)
│   │   │   ├── OBJECTIFS_Tempo_Goals.md (698)
│   │   │   ├── PATTERNS_Tempo.md (3.3K)
│   │   │   ├── SYNC_Tempo.md (3.3K)
│   │   │   └── VALIDATION_Tempo.md (2.6K)
│   │   └── wsl-autostart.md (3.2K)
│   ├── llm_agents/ (80.0K)
│   │   ├── ALGORITHM_Gemini_Stream_Flow.md (5.7K)
│   │   ├── BEHAVIORS_Gemini_Agent_Output.md (5.8K)
│   │   ├── HEALTH_LLM_Agent_Coverage.md (13.8K)
│   │   ├── IMPLEMENTATION_LLM_Agent_Code_Architecture.md (16.1K)
│   │   ├── OBJECTIFS_Llm_Agents_Goals.md (718)
│   │   ├── PATTERNS_Provider_Specific_LLM_Subprocesses.md (5.3K)
│   │   ├── SYNC_LLM_Agents_State.md (3.6K)
│   │   ├── SYNC_LLM_Agents_State_archive_2025-12.md (20.8K)
│   │   └── VALIDATION_Gemini_Agent_Invariants.md (8.1K)
│   ├── ngram_cli_core/ (7.2K)
│   │   ├── OBJECTIFS_ngram_cli_core.md (2.0K)
│   │   ├── PATTERNS_ngram_cli_core.md (3.0K)
│   │   └── SYNC_ngram_cli_core.md (2.1K)
│   ├── ngram_feature/ (2.4K)
│   │   ├── OBJECTIFS_Ngram_Feature.md (533)
│   │   ├── PATTERNS_Ngram_Feature.md (701)
│   │   └── SYNC_Ngram_Feature_State.md (1.2K)
│   ├── physics/ (353.8K)
│   │   ├── BEHAVIORS_Physics/ (14.6K)
│   │   │   ├── BEHAVIORS_Physics_Behaviors_Advanced.md (8.2K)
│   │   │   └── BEHAVIORS_Physics_Overview.md (6.4K)
│   │   ├── VALIDATION_Physics/ (20.8K)
│   │   │   ├── VALIDATION_Physics_Invariants.md (18.4K)
│   │   │   └── VALIDATION_Physics_Procedures.md (2.4K)
│   │   ├── algorithms/ (106.7K)
│   │   │   ├── ALGORITHM_Physics_Energy_Flow_Sources_Sinks_And_Moment_Dynamics.md (985)
│   │   │   ├── ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md (101.6K)
│   │   │   ├── ALGORITHM_Physics_Handler_And_Input_Processing_Flows.md (915)
│   │   │   ├── ALGORITHM_Physics_Mechanisms.md (1.4K)
│   │   │   ├── ALGORITHM_Physics_Speed_Control_And_Display_Filtering.md (898)
│   │   │   └── ALGORITHM_Physics_Tick_Cycle_Gating_Flips_And_Dispatch.md (932)
│   │   ├── archive/ (24.6K)
│   │   │   ├── IMPLEMENTATION_Physics_archive_2025-12.md (1.9K)
│   │   │   ├── SYNC_Physics_History_2025-12.md (4.5K)
│   │   │   ├── SYNC_Physics_archive_2025-12.md (17.8K)
│   │   │   └── (..1 more files)
│   │   ├── attention/ (22.0K)
│   │   │   ├── ALGORITHM_Attention_Energy_Split.md (1.3K)
│   │   │   ├── BEHAVIORS_Attention_Split_And_Interrupts.md (3.9K)
│   │   │   ├── IMPLEMENTATION_Attention_Energy_Split.md (1.1K)
│   │   │   ├── PATTERNS_Attention_Energy_Split.md (6.0K)
│   │   │   ├── SYNC_Attention_Energy_Split.md (1.0K)
│   │   │   ├── VALIDATION_Attention_Split_And_Interrupts.md (8.3K)
│   │   │   └── (..1 more files)
│   │   ├── graph/ (117.5K)
│   │   │   ├── archive/ (17.6K)
│   │   │   │   └── ALGORITHM_Energy_Flow_archived_2025-12-20.md (17.6K)
│   │   │   ├── BEHAVIORS_Graph.md (8.6K)
│   │   │   ├── PATTERNS_Graph.md (4.9K)
│   │   │   ├── SYNC_Graph.md (8.6K)
│   │   │   ├── SYNC_Graph_archive_2025-12.md (33.8K)
│   │   │   └── VALIDATION_Living_Graph.md (44.1K)
│   │   ├── mechanisms/ (9.0K)
│   │   │   ├── MECHANISMS_Attention_Energy_Split.md (4.3K)
│   │   │   ├── MECHANISMS_Contradiction_Pressure.md (2.5K)
│   │   │   └── MECHANISMS_Primes_Lag_Decay.md (2.2K)
│   │   ├── ALGORITHM_Physics.md (4.4K)
│   │   ├── API_Physics.md (6.9K)
│   │   ├── BEHAVIORS_Physics.md (1.4K)
│   │   ├── HEALTH_Physics.md (6.7K)
│   │   ├── IMPLEMENTATION_Physics.md (6.4K)
│   │   ├── OBJECTIFS_Physics_Goals.md (706)
│   │   ├── PATTERNS_Physics.md (9.3K)
│   │   ├── SYNC_Physics.md (1.7K)
│   │   └── VALIDATION_Physics.md (1.1K)
│   ├── protocol/ (105.7K)
│   │   ├── ALGORITHM/ (2.5K)
│   │   │   └── ALGORITHM_Protocol_Process_Flow.md (2.5K)
│   │   ├── IMPLEMENTATION/ (5.5K)
│   │   │   └── IMPLEMENTATION_Protocol_File_Structure.md (5.5K)
│   │   ├── archive/ (839)
│   │   │   └── SYNC_Archive_2024-12.md (839)
│   │   ├── doctor/ (54.3K)
│   │   │   ├── ALGORITHM_Project_Health_Doctor.md (17.3K)
│   │   │   ├── BEHAVIORS_Project_Health_Doctor.md (9.3K)
│   │   │   ├── HEALTH_Project_Health_Doctor.md (5.0K)
│   │   │   ├── IMPLEMENTATION_Project_Health_Doctor.md (5.7K)
│   │   │   ├── PATTERNS_Project_Health_Doctor.md (4.0K)
│   │   │   ├── SYNC_Project_Health_Doctor.md (7.8K)
│   │   │   └── VALIDATION_Project_Health_Doctor.md (5.2K)
│   │   ├── features/ (9.5K)
│   │   │   ├── BEHAVIORS_Agent_Trace_Logging.md (3.7K)
│   │   │   ├── PATTERNS_Agent_Trace_Logging.md (3.6K)
│   │   │   └── SYNC_Agent_Trace_Logging.md (2.1K)
│   │   ├── ALGORITHM_Protocol_Core_Mechanics.md (569)
│   │   ├── BEHAVIORS_Observable_Protocol_Effects.md (6.7K)
│   │   ├── HEALTH_Protocol_Verification.md (5.6K)
│   │   ├── IMPLEMENTATION_Protocol_System_Architecture.md (697)
│   │   ├── OBJECTIFS_Protocol_Goals.md (710)
│   │   ├── PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md (5.1K)
│   │   ├── SYNC_Protocol_Current_State.md (8.0K)
│   │   └── VALIDATION_Protocol_Invariants.md (5.8K)
│   ├── schema/ (86.8K)
│   │   ├── SCHEMA/ (6.6K)
│   │   │   ├── SCHEMA_Links.md (1.6K)
│   │   │   ├── SCHEMA_Nodes.md (2.9K)
│   │   │   ├── SCHEMA_Overview.md (1.0K)
│   │   │   └── SCHEMA_Tensions.md (1.1K)
│   │   ├── SCHEMA_Moments/ (3.3K)
│   │   │   ├── SCHEMA_Moments_Links.md (1.2K)
│   │   │   ├── SCHEMA_Moments_Node.md (893)
│   │   │   ├── SCHEMA_Moments_Overview.md (784)
│   │   │   └── (..1 more files)
│   │   ├── graph-health/ (11.6K)
│   │   │   ├── PATTERNS_Graph_Health_Validation.md (3.7K)
│   │   │   ├── SYNC_Graph_Health.md (3.9K)
│   │   │   └── SYNC_Graph_Health_archive_2025-12.md (4.0K)
│   │   ├── link-axes/ (25.2K)
│   │   │   ├── BEHAVIORS_Link_Axes.md (1.9K)
│   │   │   ├── PATTERNS_Link_Axes_Not_Types.md (2.6K)
│   │   │   ├── SCHEMA_Link_Axes.md (14.7K)
│   │   │   ├── SYNC_Link_Axes.md (2.9K)
│   │   │   └── VALIDATION_Link_Axes.md (3.0K)
│   │   ├── models/ (27.3K)
│   │   │   ├── PATTERNS_Pydantic_Schema_Models.md (1.4K)
│   │   │   ├── SYNC_Schema_Models.md (1.5K)
│   │   │   └── SYNC_Schema_Models_archive_2025-12.md (24.4K)
│   │   ├── ALGORITHM_Schema_Module_Doc_Routing.md (678)
│   │   ├── BEHAVIORS_Schema_Module_Observable_Schema_Effects.md (689)
│   │   ├── HEALTH_Schema_Module_Verification.md (605)
│   │   ├── IMPLEMENTATION_Schema_Module_Doc_Structure.md (639)
│   │   ├── OBJECTIFS_Schema_Goals.md (702)
│   │   ├── PATTERNS_Schema_Module_Overview_And_Ownership.md (681)
│   │   ├── SCHEMA_Code.md (4.5K)
│   │   ├── SYNC_Schema_Module_Current_State.md (520)
│   │   ├── VALIDATION_Graph.md (3.1K)
│   │   └── (..2 more files)
│   ├── tools/ (57.6K)
│   │   ├── ALGORITHM_Tools.md (6.7K)
│   │   ├── BEHAVIORS_Tools.md (4.8K)
│   │   ├── HEALTH_Tools.md (10.8K)
│   │   ├── IMPLEMENTATION_Tools.md (7.4K)
│   │   ├── OBJECTIFS_Tools_Goals.md (698)
│   │   ├── PATTERNS_Tools.md (5.9K)
│   │   ├── SYNC_Tools.md (16.3K)
│   │   └── VALIDATION_Tools.md (5.1K)
│   ├── tui/ (63.0K)
│   │   ├── IMPLEMENTATION_TUI_Code_Architecture/ (9.9K)
│   │   │   └── IMPLEMENTATION_TUI_Code_Architecture_Structure.md (9.9K)
│   │   ├── archive/ (8.0K)
│   │   │   ├── IMPLEMENTATION_Archive_2024-12.md (2.5K)
│   │   │   ├── SYNC_TUI_State_Archive_2025-12.md (5.2K)
│   │   │   └── (..1 more files)
│   │   ├── ALGORITHM_TUI_Widget_Interaction_Flow.md (6.3K)
│   │   ├── BEHAVIORS_TUI_Interactions.md (6.9K)
│   │   ├── HEALTH_TUI_Component_Test_Coverage.md (6.2K)
│   │   ├── IMPLEMENTATION_TUI_Code_Architecture.md (3.8K)
│   │   ├── OBJECTIFS_TUI.md (1.4K)
│   │   ├── OBJECTIFS_Tui_Goals.md (690)
│   │   ├── PATTERNS_TUI.md (2.9K)
│   │   ├── PATTERNS_TUI_Modular_Interface_Design.md (5.2K)
│   │   ├── SYNC_TUI_Development_Current_State.md (6.9K)
│   │   └── VALIDATION_TUI_User_Interface_Invariants.md (4.8K)
│   ├── SYNC_Project_Repository_Map.md (5.5K)
│   ├── SYNC_Project_Repository_Map_archive_2025-12.md (53.3K)
│   └── map.md (347.5K)
├── engine/ (736.8K)
│   ├── graph/ (119.4K)
│   │   └── health/ (119.4K)
│   │       ├── README.md (3.4K)
│   │       ├── check_health.py (14.1K) →
│   │       ├── example_queries.cypher (18.2K)
│   │       ├── lint_terminology.py (14.9K) →
│   │       ├── query_outputs.md (23.3K)
│   │       ├── query_results.md (16.2K)
│   │       └── test_schema.py (29.3K)
│   ├── infrastructure/ (164.5K)
│   │   ├── api/ (94.4K)
│   │   │   ├── app.py (27.9K) →
│   │   │   ├── graphs.py (15.0K) →
│   │   │   ├── moments.py (17.7K)
│   │   │   ├── playthroughs.py (24.2K) →
│   │   │   ├── sse_broadcast.py (2.8K) →
│   │   │   ├── tempo.py (6.7K) →
│   │   │   └── (..1 more files)
│   │   ├── canon/ (265)
│   │   │   └── (..2 more files)
│   │   ├── embeddings/ (7.2K)
│   │   │   ├── __init__.py (501) →
│   │   │   └── service.py (6.7K) →
│   │   ├── memory/ (19.6K)
│   │   │   ├── moment_processor.py (19.4K) →
│   │   │   └── (..1 more files)
│   │   ├── orchestration/ (41.4K)
│   │   │   ├── __init__.py (522)
│   │   │   ├── agent_cli.py (6.2K)
│   │   │   ├── narrator.py (6.6K) →
│   │   │   ├── orchestrator.py (19.3K)
│   │   │   └── world_runner.py (8.8K) →
│   │   └── tempo/ (1.7K)
│   │       ├── tempo_controller.py (1.6K)
│   │       └── (..1 more files)
│   ├── membrane/ (3.3K)
│   │   ├── __init__.py (517)
│   │   ├── functions.py (1.3K)
│   │   ├── provider.py (665)
│   │   └── (..2 more files)
│   ├── models/ (32.7K)
│   │   ├── __init__.py (2.2K) →
│   │   ├── base.py (12.3K)
│   │   ├── links.py (7.2K)
│   │   └── nodes.py (11.0K) →
│   ├── moment_graph/ (30.9K)
│   │   ├── __init__.py (541) →
│   │   ├── queries.py (15.8K) →
│   │   ├── surface.py (6.8K)
│   │   └── traversal.py (7.7K) →
│   ├── moments/ (896)
│   │   └── __init__.py (896) →
│   ├── physics/ (238.4K)
│   │   ├── graph/ (197.7K)
│   │   │   ├── graph_interface.py (5.5K) →
│   │   │   ├── graph_ops.py (28.7K) →
│   │   │   ├── graph_ops_apply.py (30.4K)
│   │   │   ├── graph_ops_links.py (19.9K)
│   │   │   ├── graph_ops_moments.py (20.0K)
│   │   │   ├── graph_ops_read_only_interface.py (8.9K) →
│   │   │   ├── graph_queries.py (30.4K)
│   │   │   ├── graph_queries_moments.py (19.3K) →
│   │   │   ├── graph_queries_search.py (12.9K) →
│   │   │   ├── graph_query_utils.py (9.1K) →
│   │   │   └── (..5 more files)
│   │   ├── attention_split_sink_mass_distribution_mechanism.py (4.1K)
│   │   ├── cluster_energy_monitor.py (2.6K)
│   │   ├── constants.py (3.7K)
│   │   ├── contradiction_pressure_from_negative_polarity_mechanism.py (2.3K)
│   │   ├── display_snap_transition_checker.py (3.3K)
│   │   ├── monitoring.py (3.2K)
│   │   ├── primes_lag_and_half_life_decay_mechanism.py (2.4K)
│   │   ├── tick.py (18.6K) →
│   │   └── (..1 more files)
│   ├── scripts/ (3.6K)
│   │   └── inject_to_narrator.py (3.6K) →
│   ├── tests/ (134.3K)
│   │   ├── test_e2e_moment_graph.py (16.7K)
│   │   ├── test_moment.py (10.7K)
│   │   ├── test_moment_graph.py (33.3K)
│   │   ├── test_moment_lifecycle.py (11.5K)
│   │   ├── test_moments_api.py (16.5K)
│   │   ├── test_narrator_integration.py (16.5K)
│   │   ├── test_physics_mechanisms.py (3.6K)
│   │   ├── test_physics_monitoring.py (1.8K)
│   │   ├── test_router_schema_validation.py (2.8K)
│   │   ├── test_spec_consistency.py (18.7K)
│   │   └── (..2 more files)
│   └── init_db.py (8.7K)
├── ngram/ (706.0K)
│   ├── llms/ (12.6K)
│   │   └── gemini_agent.py (12.6K) →
│   ├── tui/ (182.1K)
│   │   ├── styles/ (18.7K)
│   │   │   ├── theme.tcss (9.2K)
│   │   │   └── theme_light.tcss (9.6K)
│   │   ├── widgets/ (47.8K)
│   │   │   ├── agent_container.py (13.8K) →
│   │   │   ├── agent_panel.py (9.5K) →
│   │   │   ├── input_bar.py (7.9K) →
│   │   │   ├── manager_panel.py (8.0K) →
│   │   │   ├── status_bar.py (7.0K) →
│   │   │   ├── suggestions.py (1.2K) →
│   │   │   └── (..1 more files)
│   │   ├── app.py (547) →
│   │   ├── app_core.py (28.4K) →
│   │   ├── app_manager.py (11.0K) →
│   │   ├── commands.py (32.1K) →
│   │   ├── commands_agent.py (26.4K) →
│   │   ├── manager.py (9.9K) →
│   │   ├── state.py (6.9K) →
│   │   └── (..1 more files)
│   ├── cli.py (20.5K) →
│   ├── doctor_checks_content.py (31.3K) →
│   ├── doctor_files.py (23.4K) →
│   ├── doctor_report.py (24.1K)
│   ├── init_cmd.py (19.2K) →
│   ├── repair.py (25.5K) →
│   ├── repair_core.py (30.5K) →
│   ├── repair_instructions.py (31.3K) →
│   ├── repo_overview.py (28.5K) →
│   ├── validate.py (29.4K) →
│   └── (..28 more files)
├── templates/ (153.2K)
│   ├── ngram/ (146.3K)
│   │   ├── agents/ (2.8K)
│   │   │   └── manager/ (2.8K)
│   │   │       └── CLAUDE.md (2.8K)
│   │   ├── skills/ (13.0K)
│   │   │   ├── SKILL_Create_Module_Documentation_Chain_From_Templates_And_Seed_Todos.md (1.4K)
│   │   │   ├── SKILL_Debug_Investigate_And_Fix_Issues_With_Evidence_First.md (1.1K)
│   │   │   ├── SKILL_Define_And_Verify_Health_Signals_Mapped_To_Validation_Invariants.md (1.3K)
│   │   │   ├── SKILL_Extend_Add_Features_To_Existing_Systems_With_Canon_Constraints.md (1.1K)
│   │   │   ├── SKILL_Implement_Write_Or_Modify_Code_With_Doc_Chain_Coupling.md (1.2K)
│   │   │   ├── SKILL_Ingest_Raw_Data_Sources_And_Route_To_Modules.md (1.3K)
│   │   │   ├── SKILL_Onboard_Understand_Existing_Module_Codebase_And_Confirm_Canon.md (1.1K)
│   │   │   ├── SKILL_Orchestrate_Feature_Integration_Pipeline_Orchestrator_And_Progress_Router.md (1.4K)
│   │   │   ├── SKILL_Review_Evaluate_Changes_And_Produce_Auditable_Report.md (1.1K)
│   │   │   ├── SKILL_Update_Module_Sync_State_And_Record_Markers.md (1.1K)
│   │   │   └── (..1 more files)
│   │   ├── state/ (2.3K)
│   │   │   ├── SYNC_Project_State.md (2.1K)
│   │   │   └── (..1 more files)
│   │   ├── templates/ (41.1K)
│   │   │   ├── ALGORITHM_TEMPLATE.md (2.7K)
│   │   │   ├── BEHAVIORS_TEMPLATE.md (2.6K)
│   │   │   ├── CONCEPT_TEMPLATE.md (1.1K)
│   │   │   ├── HEALTH_TEMPLATE.md (14.2K)
│   │   │   ├── IMPLEMENTATION_TEMPLATE.md (8.8K)
│   │   │   ├── OBJECTIFS_TEMPLATE.md (544)
│   │   │   ├── PATTERNS_TEMPLATE.md (2.9K)
│   │   │   ├── SYNC_TEMPLATE.md (3.1K)
│   │   │   ├── TOUCHES_TEMPLATE.md (1.6K)
│   │   │   └── VALIDATION_TEMPLATE.md (3.5K)
│   │   ├── views/ (66.4K)
│   │   │   ├── VIEW_Analyze_Structural_Analysis.md (4.1K)
│   │   │   ├── VIEW_Debug_Investigate_And_Fix_Issues.md (3.7K)
│   │   │   ├── VIEW_Document_Create_Module_Documentation.md (6.1K)
│   │   │   ├── VIEW_Escalation_How_To_Handle_Vague_Tasks_Missing_Information_And_Complex_Non-Obvious_Problems.md (11.2K)
│   │   │   ├── VIEW_Extend_Add_Features_To_Existing.md (4.9K)
│   │   │   ├── VIEW_Health_Define_Health_Checks_And_Verify.md (5.9K)
│   │   │   ├── VIEW_Implement_Write_Or_Modify_Code.md (4.6K)
│   │   │   ├── VIEW_Ingest_Process_Raw_Data_Sources.md (5.3K)
│   │   │   ├── VIEW_Onboard_Understand_Existing_Codebase.md (5.2K)
│   │   │   ├── VIEW_Refactor_Improve_Code_Structure.md (5.1K)
│   │   │   └── (..18 more files)
│   │   ├── PRINCIPLES.md (8.4K)
│   │   └── PROTOCOL.md (12.2K)
│   ├── CODEX_SYSTEM_PROMPT_ADDITION.md (3.2K)
│   ├── GEMINI_SYSTEM_PROMPT_ADDITION.md (2.4K)
│   ├── ngramignore (839)
│   └── (..1 more files)
├── tools/ (22.2K)
│   ├── systemd/ (3.3K)
│   │   └── user/ (3.3K)
│   │       ├── blood-fe.service (581)
│   │       ├── falkor-mcp.service (657)
│   │       ├── ngram-be.service (501)
│   │       ├── ngram-fe.service (670)
│   │       ├── ngrok-falkor.service (552)
│   │       └── (..1 more files)
│   ├── connectome_doc_bundle_splitter_and_fence_rewriter.py (2.8K) →
│   ├── run_stack.sh (2.4K)
│   └── stream_dialogue.py (13.7K) →
├── .ngramignore (839)
├── AGENTS.md (26.2K)
├── CLAUDE.md (1.2K)
├── README.md (4.7K)
├── map.md (348.4K)
├── map_app.md (9.1K)
├── map_docs.md (148.0K)
├── map_docs_cli.md (12.5K)
├── map_docs_protocol.md (9.5K)
└── tsconfig.tsbuildinfo (75.0K)
```

**Code refs:**
- `stream_dialogue.py`

**Sections:**
- # Narrator Agent
- ## Quick Reference
- ## When You're Called
- ## Tool Calls
- # Semantic search - returns markdown for LLM consumption
- # Direct Cypher for complex queries
- # playthroughs/default/mutations/flip_aldric_edmund.yaml
- # New narratives (relationships ARE narratives)
- # New moments (type is always "thought")
- # Belief links
- # CAN_SPEAK links (who can voice each moment)
- # ATTACHED_TO links (presence requirements)
- ## Schema Reference
- # Family relationship
- # Sworn oath
- # Enmity
- # NARRATIVE (relationships, memories, knowledge)
- # MOMENT (always type: thought)
- # BELIEF (character believes narrative)
- # CAN_SPEAK (character can voice moment)
- # ATTACHED_TO (moment attached to entity)
- # CAN_LEAD_TO (moment can trigger another)
- # NARRATIVE_LINK (narrative relationships)
- # PRESENT (character at place)
- # CONTAINS (place hierarchy)
- # ABOUT (query→result connections)
- ## The Core Loop
- ## Moment Generation Guidelines
- ## Flip Types
- ## What You Don't Do
- ## File Locations

**Sections:**
- # World Runner Agent
- ## Quick Reference
- ## 1. Global Context
- ## 2. Our Aim
- ## 3. Your Role
- ## 4. When You're Called
- ## 5. Execution Interface
- # Seeds and arc plans live in narrator_notes fields
- # Get comprehensive details for each flipped tension and its related narratives
- # Get current locations and statuses of all relevant characters
- # Get character relationships (e.g., from BELIEVES links that might be strained)
- # Natural language search (if needed for deeper contextualization)
- # read.search("Who is involved with Edmund?", embed_fn=get_embedding)
- # If result indicates failure, read feedback and retry
- ## 6. Processing Steps
- ## 7. What You Produce
- ## 8. Guidelines
- ## 9. Authorship Principles
- # Graph Schema Reference
- ## Nodes
- # NOTE: "where" is expressed via OCCURRED_AT link to Place, not an attribute
- # NOTE: Speaker is NOT an attribute. Use SAID link: Character -[SAID]-> Moment
- ## Links
- # OCCURRED_AT link — no properties, just indicates where the narrative event took place
- # CONTAINS (hierarchy) — no attributes needed, relationship is binary
- # place_york CONTAINS place_york_market CONTAINS place_merchants_hall CONTAINS place_back_room
- # ROUTE (travel between settlements/regions) — computed from waypoints
- ## Tensions
- ## Modifiers
- ## Moment Links

**Definitions:**
- `runGraphFetch()`
- `GET()`

**Docs:** `docs/connectome/graphs/OBJECTIFS_Connectome_Graphs.md`

**Definitions:**
- `runListGraphs()`
- `GET()`

**Definitions:**
- `runSearchWithPython()`
- `runSearch()`
- `GET()`

**Definitions:**
- `formatEvent()`
- `GET()`

**Docs:** `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md`

**Docs:** `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md`

**Definitions:**
- `dash_for_trigger()`
- `color_for_call_type()`
- `trigger_label()`

**Docs:** `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md`

**Definitions:**
- `clamp()`
- `intersect_line_with_rect()`

**Docs:** `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md`

**Definitions:**
- `EdgeComponent()`
- `strokeWidth()`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Definitions:**
- `bucket_for_energy()`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Definitions:**
- `theme_for_node()`
- `title_color_for_node()`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Definitions:**
- `color_for_call_type()`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Definitions:**
- `color_for_seconds()`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Definitions:**
- `color_for_speed()`
- `elapsed()`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Definitions:**
- `build_node_tooltip()`
- `BaseNode()`
- `renderHint()`
- `PlayerNode()`
- `renderHint()`
- `handleClick()`
- `handleKeyDown()`
- `TickCronNode()`
- `renderHint()`

**Docs:** `docs/connectome/health/HEALTH_Connectome_Live_Signals.md`

**Definitions:**
- `status_label()`

**Docs:** `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md`

**Definitions:**
- `duration_text()`
- `duration_class()`

**Docs:** `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md`

**Definitions:**
- `copy_to_clipboard()`
- `handleCopyJsonl()`
- `handleCopyText()`

**Docs:** `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md`

**Definitions:**
- `trigger_badge_class()`
- `call_type_badge_class()`

**Docs:** `docs/connectome/page_shell/PATTERNS_Connectome_Page_Shell_Route_Composition_And_User_Control_Surface_Patterns.md`

**Definitions:**
- `connect()`
- `loadGraphs()`
- `loadGraph()`
- `handleNext()`
- `handleRestart()`
- `handleSpeedChange()`
- `handleModeChange()`
- `handleSearch()`
- `nodeIds()`
- `edgeIds()`

**Docs:** `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md`

**Definitions:**
- `compute_zones()`
- `compute_node_positions()`

**Docs:** `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md`

**Definitions:**
- `compute_label_anchors()`

**Docs:** `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md`

**Definitions:**
- `hex_to_rgb()`
- `build_shader()`
- `build_program()`
- `CanvasInner()`
- `searchNodes()`
- `searchEdges()`
- `searchEdges()`
- `render()`
- `sx()`
- `sy()`
- `handleWheel()`
- `handleMouseDown()`
- `handleMouseMove()`
- `worldX()`
- `worldY()`
- `handleMouseUp()`
- `worldX()`
- `worldY()`

**Docs:** `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md`

**Definitions:**
- `node_label()`
- `node_class()`
- `call_type_detail()`
- `trigger_detail()`

**Doc refs:**
- `agents/narrator/CLAUDE.md`
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md`
- `docs/agents/narrator/HEALTH_Narrator.md`
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md`
- `docs/agents/narrator/PATTERNS_Narrator.md`
- `docs/agents/narrator/SYNC_Narrator.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12.md`
- `docs/agents/narrator/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Narrator Archive - 2024-12
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## Archived Sections (2025-12-19)
- ## HANDOFF_Rolling_Window_Architecture (Full Detail)
- # Handoff - Rolling Window Architecture
- ## The Problem
- ## The Solution: Rolling Window
- ## Why SSE (Not WebSocket)
- ## API Design
- ## Frontend Responsibilities
- ## Backend Responsibilities
- ## Generation Queue
- # 1. Return cached response immediately
- # 2. Queue generation for new clickables
- # 1. Call narrator
- # 2. Cache it
- # 3. Push to frontend
- ## Edge Cases
- ## Narrator Prompt Implications
- ## Open Questions
- ## Files Changed
- ## Next Steps
- ## TOOL_REFERENCE: Complete Example + JSON Schema (Archived)
- ## INPUT_REFERENCE: Complete Example Input (Archived)

**Doc refs:**
- `agents/narrator/CLAUDE.md`

**Sections:**
- # Narrator — Algorithm: Scene Generation
- ## CHAIN
- ## PURPOSE
- ## OVERVIEW
- ## OBJECTIVES AND BEHAVIORS
- ## DATA STRUCTURES
- ## ALGORITHM: generate_scene_output
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS
- ## ROLLING WINDOW (SUMMARY)
- ## THREAD CONTINUITY (SUMMARY)
- ## QUALITY CHECKS (MINIMUM)

**Doc refs:**
- `docs/agents/narrator/INPUT_REFERENCE.md`
- `docs/agents/narrator/TOOL_REFERENCE.md`

**Sections:**
- # Narrator — Behaviors: What the Narrator Produces
- ## CHAIN
- ## Two Response Modes
- ## Dialogue Chunks
- ## Graph Mutations
- ## SceneTree (Significant Actions)
- ## time_elapsed Rules
- ## BEHAVIORS
- ## OBJECTIVES SERVED
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS
- ## World Injection Handling
- ## Quality Indicators

**Sections:**
- # Narrator — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## OBJECTIVES COVERAGE
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## HOW TO USE THIS TEMPLATE
- ## CHECKER INDEX
- ## INDICATOR: author_coherence
- ## INDICATOR: mutation_validity
- ## INDICATOR: stream_latency
- ## HOW TO RUN
- # Run narrator integration checks
- ## MARKERS

**Code refs:**
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/orchestration/narrator.py`
- `narrator/prompt_builder.py`
- `tools/stream_dialogue.py`

**Doc refs:**
- `agents/narrator/CLAUDE.md`

**Sections:**
- # Narrator — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## RUNTIME BEHAVIOR
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Code refs:**
- `engine/infrastructure/orchestration/narrator.py`
- `engine/physics/graph/graph_ops.py`
- `engine/physics/graph/graph_queries.py`

**Doc refs:**
- `agents/narrator/CLAUDE.md`
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md`

**Sections:**
- # Narrator — Patterns: Why This Design
- ## Core Insight
- ## The Problem
- ## The Pattern
- ## Scope
- ## Data
- ## Behaviors Supported
- ## Behaviors Prevented
- ## Principles
- ## Dependencies
- ## Inspirations
- ## Pre-Generation Model
- ## What the Narrator Controls
- ## Free Input (Exception)
- ## Workflow (High Level)
- ## Gaps / Ideas / Questions
- ## CHAIN

**Code refs:**
- `tools/stream_dialogue.py`

**Doc refs:**
- `agents/narrator/CLAUDE.md`
- `docs/agents/narrator/BEHAVIORS_Narrator.md`
- `docs/agents/narrator/HEALTH_Narrator.md`
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md`
- `docs/agents/narrator/PATTERNS_Narrator.md`
- `docs/agents/narrator/SYNC_Narrator.md`
- `docs/agents/narrator/VALIDATION_Narrator.md`
- `docs/schema/SCHEMA.md`

**Sections:**
- # Narrator — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## CHAIN

**Code refs:**
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/orchestration/narrator.py`

**Doc refs:**
- `agents/narrator/CLAUDE_old.md`
- `docs/agents/narrator/ALGORITHM_Scene_Generation.md`
- `docs/agents/narrator/BEHAVIORS_Narrator.md`
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md`
- `docs/agents/narrator/HEALTH_Narrator.md`
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md`
- `docs/agents/narrator/INPUT_REFERENCE.md`
- `docs/agents/narrator/PATTERNS_Narrator.md`
- `docs/agents/narrator/PATTERNS_World_Building.md`
- `docs/agents/narrator/SYNC_Narrator.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12.md`
- `docs/agents/narrator/TEST_Narrator.md`
- `docs/agents/narrator/TOOL_REFERENCE.md`
- `docs/agents/narrator/VALIDATION_Narrator.md`
- `docs/agents/narrator/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Archived: SYNC_Narrator.md
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## RECENT CHANGES

**Sections:**
- # Player Notes — {playthrough_id}
- ## Player Setup
- ## Current Understanding
- ## Session Observations
- ## Emerging Patterns
- ## Narrator Adjustments
- ## Open Questions

**Doc refs:**
- `docs/schema/SCHEMA.md`

**Sections:**
- # Narrator Tool Reference
- ## How To Use
- # First call (starts session)
- # Subsequent calls (continues session)
- ## Output Schema (NarratorOutput)
- ## SceneTree (Significant Actions)
- ## Dialogue Chunks (Conversational Actions)
- ## Graph Mutations
- ## Time Elapsed
- ## Validation Rules (Minimum)

**Sections:**
- # Narrator — Validation: Behavioral Invariants and Output Verification
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## INVARIANTS
- ## VERIFICATION PROCEDURE
- ## TEST COVERAGE (Snapshot)
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # World Runner — Archive (2024-12)
- ## Purpose
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## Archived From TOOL_REFERENCE.md
- ## Complete Example
- ## Validation Rules
- ## Processing Order
- ## JSON Schema (for programmatic validation)
- ## Archived From BEHAVIORS_World_Runner.md
- ## Injection as Markdown (Narrator Input)
- # WORLD INJECTION
- ## Status: INTERRUPTED
- ## EVENT: Ambush on the Road
- ## CLUSTER: Relevant Nodes
- ## WORLD CHANGES (Background)
- ## NEWS AVAILABLE
- ## Injection: Completed
- # WORLD INJECTION
- ## Status: COMPLETED
- ## WORLD CHANGES (While You Traveled)
- ## NEWS AVAILABLE
- ## ARRIVAL: York
- ## Archived From INPUT_REFERENCE.md
- ## Complete Example Input
- ## Processing Guidance
- ## CHAIN

**Sections:**
- # World Runner — Algorithm: How It Works
- ## OVERVIEW
- ## OBJECTIVES AND BEHAVIORS
- ## DATA STRUCTURES
- ## Core Principle: Runner Owns the Tick Loop
- ## ALGORITHM: run_world
- ## ALGORITHM: affects_player
- ## Algorithm Steps (Condensed)
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## Stateless Between Calls
- ## Cluster Context for Flips
- ## MARKERS
- ## CHAIN

**Sections:**
- # World Runner — Behaviors: What It Produces
- ## Injection Interface
- ## BEHAVIORS
- ## OBJECTIVES SERVED
- ## INPUTS / OUTPUTS
- ## OUTPUTS
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## Interrupted Injection
- ## Completed Injection
- ## Injection Queue (In-Scene Events)
- ## Event / WorldChange / News
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS
- ## Resume Pattern (Narrator)
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS
- ## CHAIN

**Sections:**
- # World Runner — Health: Verification Checklist and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## CHECKS
- ## HOW TO USE THIS TEMPLATE
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## OBJECTIVES COVERAGE
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: background_consistency
- ## INDICATOR: adapter_resilience
- ## HOW TO RUN
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `engine/infrastructure/orchestration/world_runner.py`

**Doc refs:**
- `agents/world_runner/CLAUDE.md`

**Sections:**
- # World Runner — Implementation: Service Architecture and Boundaries
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## CONCURRENCY MODEL
- ## LOGIC CHAINS
- ## RUNTIME BEHAVIOR
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # World Runner Input Reference
- ## Script Location
- ## Prompt Structure
- ## Flip Context
- ## Graph Context
- ## Player Context
- ## Processing Guidance (Short)
- ## CHAIN

**Code refs:**
- `engine/infrastructure/orchestration/world_runner.py`
- `engine/physics/graph/graph_ops.py`
- `engine/physics/graph/graph_queries.py`

**Doc refs:**
- `agents/world_runner/CLAUDE.md`

**Sections:**
- # World Runner — Patterns: Why This Shape
- ## The Core Insight
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## Interrupt/Resume Pattern
- ## Stateless Runner
- ## What the Runner Is Not
- ## Player Impact Threshold
- ## Why Separation Matters
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS
- ## CHAIN

**Sections:**
- # World Runner — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## POINTERS
- ## CHAIN
- ## CONSCIOUSNESS TRACE

**Code refs:**
- `engine/infrastructure/orchestration/world_runner.py`

**Sections:**
- # World Runner — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## CHECKER INDEX
- ## INDICATOR: adapter_resilience
- ## KNOWN GAPS

**Sections:**
- # World Runner Tool Reference
- ## WorldRunnerOutput
- ## Graph Mutations
- ## World Injection
- ## Validation Rules (Summary)
- ## Processing Order
- ## Archive Note
- ## CHAIN

**Code refs:**
- `engine/infrastructure/orchestration/world_runner.py`

**Sections:**
- # World Runner — Validation: Service Invariants and Failure Behavior
- ## CHAIN
- ## INVARIANTS
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## HEALTH COVERAGE
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- # No automated tests for World Runner service yet.
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # OBJECTIFS: SSE API Module
- ## CHAIN:
- ## OBJECTIVE:
- ## KEY RESULTS:
- ## STAKEHOLDERS:
- ## CONSTRAINTS:
- ## OUT OF SCOPE:

**Code refs:**
- `route.ts`

**Sections:**
- # PATTERNS: SSE API Module
- ## CHAIN:
- ## PATTERN: Server-Sent Events (SSE) Endpoint
- ## RELATED PATTERNS:

**Code refs:**
- `app/api/sse/route.ts`

**Sections:**
- # SYNC: SSE API Module
- ## CHAIN:
- ## CONTEXT:
- ## STATUS: Documented
- ## CHANGES:

**Sections:**
- # ARCHITECTURE — Cybernetic Studio — Algorithm: Stimulus-to-Surface Flow
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: Stimulus-to-Surface Flow
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## INTERACTIONS
- ## MARKERS

**Sections:**
- # ARCHITECTURE — Cybernetic Studio — Behaviors: System Observable Effects
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Sections:**
- # ARCHITECTURE — Cybernetic Studio — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## CHECKER INDEX
- ## INDICATOR: evidence_ref_only_storage
- ## INDICATOR: graph_ownership_boundary
- ## HOW TO RUN
- # Pending: add health runner once graph hooks exist.
- ## KNOWN GAPS
- ## MARKERS

**Sections:**
- # ARCHITECTURE — Cybernetic Studio — Implementation: Code Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## BOUNDARIES
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## MODULE DEPENDENCIES
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Cybernetic Studio Architecture
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `ngram/doctor_checks.py`

**Sections:**
- # ARCHITECTURE — Cybernetic Studio (Game + Dev Framework + Graph Layer)
- ## CHAIN
- ## 0) One-Sentence Summary
- ## 1) Validated Axioms (Non-Negotiable)
- ## 2) Repo Topology (How Many Repos, What Owns What)
- ## 3) Linking Between Repos (Three Kinds of Links)
- ## 4) Unified Ontology (Minimal Node/Link Set)
- ## 5) Evidence References (How the Graph Touches the Repo Without Duplicating It)
- ## 6) Stimulus → Energy Injection (Granular, Bottom-Up, No Overmind)
- ## 7) Physics Loop (What Runs Every Tick)
- ## 8) Places (Rooms, Views, and SYNC as Living Surfaces)
- ## 9) Agents and Identity (Story Characters vs Dev Agents)
- ## 10) Homeostasis and Safety (Prevent Runaway Refactors)
- ## 11) Concrete Deliverables (What Gets Built Where)
- ## 12) Acceptance Criteria (V1)
- ## 13) Open Questions (Explicitly Remaining)
- ## Appendix A — Minimal YAML Examples (V1)

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`
- `docs/architecture/cybernetic_studio_architecture/ALGORITHM_Cybernetic_Studio_Process_Flow.md`
- `docs/architecture/cybernetic_studio_architecture/BEHAVIORS_Cybernetic_Studio_System_Behaviors.md`
- `docs/architecture/cybernetic_studio_architecture/HEALTH_Cybernetic_Studio_Health_Checks.md`
- `docs/architecture/cybernetic_studio_architecture/IMPLEMENTATION_Cybernetic_Studio_Code_Structure.md`
- `docs/architecture/cybernetic_studio_architecture/PATTERNS_Cybernetic_Studio_Architecture.md`
- `docs/architecture/cybernetic_studio_architecture/SYNC_Cybernetic_Studio_Architecture_State.md`
- `docs/architecture/cybernetic_studio_architecture/VALIDATION_Cybernetic_Studio_Architectural_Invariants.md`

**Sections:**
- # Cybernetic Studio Architecture — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- # Pending: integration checks once graph service wiring exists.
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Sections:**
- # ARCHITECTURE — Cybernetic Studio — Validation: Architectural Invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Pending: add integration checks once graph service wiring exists.
- ## SYNC STATUS
- ## MARKERS

**Doc refs:**
- `docs/cli/archive/SYNC_CLI_State_Archive_2025-12.md`

**Sections:**
- # Archived: SYNC_CLI_Development_State.md
- ## STATUS
- ## CHAIN

**Code refs:**
- `ngram/doctor_checks.py`
- `ngram/repair_core.py`

**Doc refs:**
- `docs/cli/core/SYNC_CLI_Development_State.md`
- `docs/protocol/archive/SYNC_Archive_2024-12.md`

**Sections:**
- # Archived: SYNC_CLI_State.md
- ## MATURITY
- ## RECENT CHANGES (ARCHIVED)
- ## NOTES
- ## RELATED ARCHIVES
- ## MERGED SNAPSHOTS
- ## CHAIN
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Sections:**
- # ngram Framework CLI — Algorithm: Command Processing Logic (Overview)
- ## CHAIN
- ## OVERVIEW
- ## COMMAND ALGORITHMS
- ## DATA STRUCTURES
- ## DATA FLOW (SUMMARY)
- ## PERFORMANCE NOTES

**Code refs:**
- `ngram/cli.py`
- `ngram/core_utils.py`
- `ngram/doctor.py`
- `ngram/doctor_checks.py`
- `ngram/doctor_checks_content.py`
- `ngram/doctor_checks_docs.py`
- `ngram/doctor_checks_naming.py`
- `ngram/doctor_checks_quality.py`
- `ngram/doctor_checks_sync.py`
- `ngram/doctor_files.py`
- `ngram/refactor.py`
- `ngram/repair.py`
- `ngram/repair_core.py`
- `ngram/repair_escalation_interactive.py`
- `ngram/repair_instructions.py`
- `ngram/repair_instructions_docs.py`
- `ngram/repair_report.py`
- `ngram/repo_overview.py`
- `ngram/repo_overview_formatters.py`
- `ngram/solve_escalations.py`
- `ngram/validate.py`

**Doc refs:**
- `docs/cli/archive/SYNC_archive_2024-12.md`
- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Sections:**
- # ngram Framework CLI — Implementation: Code Architecture and Structure (Overview)
- ## CHAIN
- ## OVERVIEW
- ## DESIGN PATTERNS
- ## SUBSYSTEM IMPLEMENTATIONS
- ## BIDIRECTIONAL LINKS (ENTRY)
- ## CODE STRUCTURE
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS
- ## GAPS (ACTIVE)
- ## ARCHIVE POINTER

**Code refs:**
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/doctor.py`
- `ngram/doctor_report.py`
- `ngram/init_cmd.py`
- `ngram/repair.py`
- `ngram/repair_report.py`

**Sections:**
- # ngram Framework CLI — Implementation: Runtime and Dependencies
- ## CHAIN
- ## CONTEXT
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Code refs:**
- `ngram/cli.py`
- `ngram/doctor.py`
- `ngram/doctor_report.py`
- `ngram/repair.py`
- `ngram/repair_report.py`
- `ngram/validate.py`

**Sections:**
- # ngram Framework CLI — Implementation: Schema Definitions for CLI Flows
- ## CHAIN
- ## CONTEXT
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Code refs:**
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/core_utils.py`
- `ngram/doctor.py`
- `ngram/doctor_checks.py`
- `ngram/doctor_checks_content.py`
- `ngram/doctor_checks_core.py`
- `ngram/doctor_checks_docs.py`
- `ngram/doctor_checks_metadata.py`
- `ngram/doctor_checks_prompt_integrity.py`
- `ngram/doctor_checks_quality.py`
- `ngram/doctor_checks_reference.py`
- `ngram/doctor_checks_stub.py`
- `ngram/doctor_checks_sync.py`
- `ngram/doctor_files.py`
- `ngram/doctor_report.py`
- `ngram/doctor_types.py`
- `ngram/github.py`
- `ngram/init_cmd.py`
- `ngram/project_map.py`
- `ngram/project_map_html.py`
- `ngram/prompt.py`
- `ngram/repair.py`
- `ngram/repair_core.py`
- `ngram/repair_escalation_interactive.py`
- `ngram/repair_instructions.py`
- `ngram/repair_instructions_docs.py`
- `ngram/repair_report.py`
- `ngram/repo_overview.py`
- `ngram/repo_overview_formatters.py`
- `ngram/solve_escalations.py`
- `ngram/sync.py`
- `ngram/validate.py`

**Sections:**
- # ngram Framework CLI — Implementation: Code Structure
- ## CHAIN
- ## CONTEXT
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## FILE RESPONSIBILITIES

**Doc refs:**
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `docs/cli/core/HEALTH_CLI_Command_Test_Coverage.md`
- `docs/cli/core/VALIDATION_CLI_Instruction_Invariants.md`

**Sections:**
- # ngram Framework CLI — Behaviors: Command Effects and Observable Outcomes
- ## CHAIN
- ## BEHAVIORS
- ## NOTES
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Doc refs:**
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- `docs/tui/HEALTH_TUI_Coverage.md`

**Sections:**
- # ngram Framework CLI — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## INDICATOR: CLI Command Health
- ## CHECKER INDEX
- ## INDICATOR: Init Integrity
- ## HOW TO RUN
- # Run all health checks via validate
- # Run project health via doctor
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `agent_cli.py`
- `ngram/core_utils.py`
- `ngram/doctor_files.py`
- `ngram/github.py`
- `ngram/repair_core.py`
- `ngram/repair_escalation_interactive.py`
- `ngram/repair_instructions.py`
- `ngram/repair_instructions_docs.py`
- `ngram/repair_report.py`
- `ngram/repo_overview.py`
- `ngram/solve_escalations.py`

**Sections:**
- # ngram Framework CLI — Patterns: Why CLI Over Copy
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## DATA
- ## SCOPE
- ## WHAT THIS DOES NOT SOLVE
- ## CLI SUBSYSTEM REFERENCES
- ## MARKERS

**Code refs:**
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/doctor_checks_content.py`
- `ngram/doctor_checks_docs.py`
- `ngram/doctor_checks_stub.py`
- `ngram/doctor_files.py`
- `ngram/init_cmd.py`
- `ngram/prompt.py`
- `ngram/refactor.py`
- `ngram/repair_core.py`
- `ngram/repo_overview.py`
- `ngram/solve_escalations.py`

**Doc refs:**
- `archive/SYNC_CLI_Development_State_archive_2025-12.md`
- `docs/cli/ALGORITHM_CLI_Command_Execution_Logic.md`
- `docs/cli/archive/SYNC_CLI_Development_State_archive_2025-12.md`
- `docs/cli/archive/SYNC_CLI_State_Archive_2025-12.md`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `docs/cli/core/BEHAVIORS_CLI_Command_Effects.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md`
- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`
- `docs/cli/core/SYNC_CLI_Development_State.md`
- `docs/cli/core/VALIDATION_CLI_Instruction_Invariants.md`
- `docs/protocol/doctor/SYNC_Project_Health_Doctor.md`
- `docs/tui/ALGORITHM_TUI_Widget_Interaction_Flow.md`
- `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md`

**Sections:**
- # ngram Framework CLI — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## CONFLICTS
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## RECENT CHANGES
- ## GAPS
- ## Agent Observations
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## ARCHIVE

**Doc refs:**
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `docs/cli/core/SYNC_CLI_Development_State.md`

**Sections:**
- # ngram Framework CLI — Validation: Invariants and Correctness Checks
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## SYNC STATUS
- ## VERIFICATION PROCEDURE
- # Run CLI commands manually for now
- # No automated test suite yet
- # TODO: Add pytest tests
- ## CHECK REFERENCES
- ## MARKERS

**Code refs:**
- `ngram/cli.py`
- `ngram/prompt.py`

**Doc refs:**
- `state/SYNC_Project_State.md`

**Sections:**
- # CLI Prompt — Algorithm: Assemble the bootstrap prompt
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: `generate_bootstrap_prompt()`
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Code refs:**
- `ngram/prompt.py`

**Doc refs:**
- `data/NGRAM Documentation Chain Pattern (Draft “Marco”).md`

**Sections:**
- # CLI Prompt — Behaviors: What the bootstrap command surfaces to agents
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Code refs:**
- `ngram/prompt.py`

**Sections:**
- # CLI Prompt — Health: Runtime verification of bootstrap guidance
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## HEALTH SIGNAL MAPPING
- ## VERIFICATION RESULTS
- ## INDICATOR: Prompt Doc Reference Health
- ## INDICATOR: Prompt Checklist Presence
- ## HOW TO RUN
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `ngram/cli.py`
- `ngram/prompt.py`

**Doc refs:**
- `docs/cli/prompt/ALGORITHM_Prompt_Bootstrap_Prompt_Construction.md`

**Sections:**
- # CLI Prompt — Implementation: Code architecture and docking
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Code refs:**
- `agent_cli.py`
- `ngram/prompt.py`

**Doc refs:**
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`

**Sections:**
- # CLI Prompt — Patterns: Workflow that surfacing protocol context
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `ngram/prompt.py`

**Doc refs:**
- `docs/cli/core/SYNC_CLI_Development_State.md`
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`
- `docs/protocol/HEALTH_Protocol_Verification.md`

**Sections:**
- # CLI Prompt Module — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `ngram/prompt.py`

**Doc refs:**
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`
- `docs/cli/prompt/SYNC_Prompt_Command_State.md`
- `docs/protocol/HEALTH_Protocol_Verification.md`

**Sections:**
- # CLI Prompt — Validation: Bootstrap prompt invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## MARKERS

**Code refs:**
- `cli.py`
- `doctor.py`
- `ngram/cli.py`
- `ngram/doctor.py`
- `ngram/repair.py`

**Sections:**
- # ngram Framework CLI — Algorithm: Command Execution Logic
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: `dispatch_command()`
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Sections:**
- # ngram Framework CLI — Behaviors: Command Surface Effects
- ## CHAIN
- ## BEHAVIORS

**Sections:**
- # ngram Framework CLI — Health: Verification Checklist
- ## CHAIN
- ## CHECKS

**Code refs:**
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/core_utils.py`
- `ngram/doctor.py`
- `ngram/doctor_checks_core.py`
- `ngram/doctor_checks_metadata.py`
- `ngram/doctor_files.py`
- `ngram/init_cmd.py`
- `ngram/prompt.py`
- `ngram/repair.py`
- `ngram/repair_core.py`

**Doc refs:**
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md`
- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Sections:**
- # ngram Framework CLI — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Cli
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # ngram Framework CLI — Patterns: Command Surface Overview and Scope
- ## CHAIN
- ## PURPOSE
- ## SCOPE

**Sections:**
- # ngram Framework CLI — Validation: Command Invariants
- ## CHAIN
- ## INVARIANTS

**Doc refs:**
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `docs/cli/core/BEHAVIORS_CLI_Command_Effects.md`
- `docs/cli/core/HEALTH_CLI_Command_Test_Coverage.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`
- `docs/cli/core/SYNC_CLI_Development_State.md`
- `docs/cli/core/VALIDATION_CLI_Instruction_Invariants.md`
- `docs/cli/prompt/PATTERNS_Prompt_Command_Workflow_Design.md`
- `docs/cli/prompt/SYNC_Prompt_Command_State.md`
- `docs/protocol/doctor/PATTERNS_Project_Health_Doctor.md`
- `docs/protocol/doctor/SYNC_Project_Health_Doctor.md`

**Sections:**
- # CLI Modules

**Doc refs:**
- `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md`
- `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`
- `docs/infrastructure/tempo/PATTERNS_Tempo.md`

**Sections:**
- # CONCEPT: Tempo Controller — The Main Loop That Paces Reality
- ## WHAT IT IS
- ## WHY IT EXISTS
- ## KEY PROPERTIES
- ## RELATIONSHIPS TO OTHER CONCEPTS
- ## THE CORE INSIGHT
- ## COMMON MISUNDERSTANDINGS
- ## SEE ALSO

**Sections:**
- # edge_kit — Algorithm: Rendering, Pulses, Directional Shine, and Label Rules
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: `style_for_edge(edge)`
- ## ALGORITHM: `compute_label_style(edge)`
- ## ALGORITHM: `compute_pulse_duration_ms(edge, declared_duration_ms, speed)`
- ## ALGORITHM: `compute_pulse_path_clamped_to_node_bounds(edge, geometry)`
- ## ALGORITHM: directional shine animation
- ## ALGORITHM: energy magnitude mapping → pulse visuals
- ## COMPLEXITY
- ## MARKERS

**Sections:**
- # edge_kit — Behaviors: Readable, Directional, Truthful Link Effects
- ## CHAIN
- ## OBJECTIVES SERVED
- ## BEHAVIORS
- ## ANTI-BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## MARKERS

**Sections:**
- # edge_kit — Health: Link Visibility and Semantic Styling Verification
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## OBJECTIVES COVERAGE
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## HOW TO RUN
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `app/connectome/components/edge_kit/connectome_edge_directional_shine_animation_helpers.ts`
- `app/connectome/components/edge_kit/connectome_edge_label_renderer_with_halo_and_zoom_policy.ts`
- `app/connectome/components/edge_kit/connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx`
- `app/connectome/components/edge_kit/connectome_edge_pulse_particle_animation_and_boundary_clamp_helpers.ts`
- `app/connectome/components/edge_kit/connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts`
- `app/connectome/components/edge_kit/connectome_node_boundary_intersection_geometry_helpers.ts`
- `app/connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.ts`
- `app/connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.tsx`
- `connectome_edge_directional_shine_animation_helpers.ts`
- `connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx`
- `connectome_edge_pulse_particle_animation_and_boundary_clamp_helpers.ts`
- `connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts`
- `connectome_node_boundary_intersection_geometry_helpers.ts`
- `semantic_edge_components_with_directional_shine_and_pulses.tsx`

**Doc refs:**
- `docs/connectome/edge_kit/HEALTH_Connectome_Edge_Kit_Runtime_Verification_Of_Link_Visibility_And_Semantic_Styling.md`
- `docs/connectome/event_model/ALGORITHM_Connectome_Event_Normalization_And_Rendering_Event_Synthesis.md`
- `event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md`

**Sections:**
- # edge_kit — Implementation: Component Map and Render Tokens
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## BIDIRECTIONAL LINKS
- ## RENDER TOKENS (V1)
- ## ENTRY POINTS
- ## CONFIGURATION
- ## MARKERS

**Sections:**
- # OBJECTIFS — Edge Kit
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # edge_kit — Patterns: Color-Coded, Trigger-Typed, Directional Edge Styling
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## DATA
- ## INSPIRATIONS
- ## PRINCIPLES
- ## EDGE TYPES (V1)
- ## DEPENDENCIES
- ## SCOPE
- ## MARKERS

**Code refs:**
- `app/connectome/components/edge_kit/connectome_edge_directional_shine_animation_helpers.ts`
- `app/connectome/components/edge_kit/connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx`
- `app/connectome/components/edge_kit/connectome_edge_pulse_particle_animation_and_boundary_clamp_helpers.ts`
- `app/connectome/components/edge_kit/connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts`
- `app/connectome/components/edge_kit/connectome_node_boundary_intersection_geometry_helpers.ts`
- `app/connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.tsx`
- `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`

**Doc refs:**
- `docs/connectome/edge_kit/BEHAVIORS_Connectome_Edge_Kit_Readable_Directional_And_Truthful_Link_Effects.md`
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md`
- `docs/connectome/edge_kit/PATTERNS_Connectome_Edge_Kit_Color_Coded_Trigger_Typed_Directional_Link_Styling_Patterns.md`
- `docs/connectome/edge_kit/SYNC_Connectome_Edge_Kit_Sync_Current_State.md`
- `docs/connectome/edge_kit/VALIDATION_Connectome_Edge_Kit_Invariants_For_Color_Dash_And_Pulse_Truth.md`
- `docs/engine/membrane/PATTERN_Membrane_Modulation.md`

**Sections:**
- # edge_kit — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## TODO
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Sections:**
- # edge_kit — Validation: Invariants for Color, Dash, Direction, and Pulse Truth
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## PROPERTIES
- ## INVARIANTS
- ## SYNC STATUS
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## MARKERS

**Sections:**
- # event_model — Algorithm: Normalizing Inputs into FlowEvents
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: `normalize_flow_event(raw_input)`
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Sections:**
- # event_model — Behaviors: Observable Effects of the FlowEvent Contract
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Sections:**
- # event_model — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: event_schema_conformance
- ## HOW TO RUN
- # Run all health checks for this module
- # Run a specific checker
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `app/connectome/lib/flow_event_schema_and_normalization_contract.ts`
- `flow_event_schema_and_normalization_contract.ts`

**Sections:**
- # event_model — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Event Model
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # event_model — Patterns: Contract-First Event Stream for Stepper + Realtime
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `app/connectome/lib/flow_event_duration_bucket_color_classifier.ts`
- `app/connectome/lib/flow_event_schema_and_normalization_contract.ts`
- `app/connectome/lib/flow_event_trigger_and_calltype_inference_rules.ts`

**Sections:**
- # event_model — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## TODO

**Sections:**
- # event_model — Validation: Invariants for FlowEvent Correctness
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Run health checks (module scoped)
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Connectome Feature Shell
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)
- ## MARKERS

**Sections:**
- # flow_canvas — Algorithm: Zones, Layout, and Label Decluttering
- ## CHAIN
- ## OVERVIEW
- ## OBJECTIVES AND BEHAVIORS
- ## ALGORITHM: `render_flow_canvas_frame(store_state, camera, interaction_queue)`
- ## DATA STRUCTURES
- ## ALGORITHM: `compute_zone_layout(viewport)`
- ## ALGORITHM: `place_nodes_with_force_layout(nodes, edges, zones)`
- ## ALGORITHM: `route_edges_and_place_labels(edges, node_layouts)`
- ## ALGORITHM: `apply_camera_transform(camera, world_coords)`
- ## KEY DECISIONS
- ## DATA FLOW
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## COMPLEXITY
- ## MARKERS

**Sections:**
- # flow_canvas — Behaviors: Readability, Stability, and Navigation Effects
- ## CHAIN
- ## OBJECTIVES SERVED
- ## INPUTS / OUTPUTS
- ## BEHAVIORS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS
- ## OBSERVATIONS

**Sections:**
- # flow_canvas — Health: Render Stability and Performance Budget Checks
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## OBJECTIVES COVERAGE
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## CHECKER INDEX
- ## INDICATOR: canvas_edge_disappearance_detector
- ## INDICATOR: canvas_layout_determinism_integrity
- ## INDICATOR: canvas_edge_attachment_and_visibility_integrity
- ## HOW TO RUN
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `app/connectome/components/deterministic_zone_and_node_layout_computation_helpers.ts`
- `app/connectome/components/edge_label_declutter_and_visibility_policy_helpers.ts`
- `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.ts`
- `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`
- `app/connectome/components/telemetry_camera_controls.ts`
- `pannable_zoomable_zoned_flow_canvas_renderer.tsx`

**Doc refs:**
- `runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md`

**Sections:**
- # flow_canvas — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## ENTRY POINTS
- ## SCHEMA
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Flow Canvas
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # flow_canvas — Patterns: Pannable/Zoomable Zoned Map with Stable Edge Readability
- ## CHAIN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## PATTERNS USED (SUB-PATTERNS)
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## MARKERS

**Code refs:**
- `app/connectome/components/deterministic_zone_and_node_layout_computation_helpers.ts`
- `app/connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.tsx`
- `app/connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`
- `app/connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.tsx`
- `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`

**Doc refs:**
- `docs/connectome/flow_canvas/ALGORITHM_Connectome_Flow_Canvas_Layout_Zones_And_Edge_Label_Decluttering.md`
- `docs/connectome/flow_canvas/BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md`
- `docs/connectome/flow_canvas/HEALTH_Connectome_Flow_Canvas_Runtime_Verification_Of_Render_Stability_And_Perf_Budgets.md`
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md`
- `docs/connectome/flow_canvas/PATTERNS_Connectome_Flow_Canvas_Pannable_Zoomable_Zoned_System_Map_Rendering_Patterns.md`
- `docs/connectome/flow_canvas/SYNC_Connectome_Flow_Canvas_Sync_Current_State.md`
- `docs/connectome/flow_canvas/VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md`
- `docs/engine/membrane/PATTERN_Membrane_Modulation.md`

**Sections:**
- # flow_canvas — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## TODO
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## Agent Observations

**Sections:**
- # flow_canvas — Validation: Invariants for Readability and Render Stability
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## PROPERTIES
- ## INVARIANTS
- ## SYNC STATUS
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## MARKERS

**Sections:**
- # OBJECTIFS — Connectome Graph API
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)
- ## MARKERS

**Code refs:**
- `app/api/connectome/graph/route.ts`

**Sections:**
- # Connectome Graph API — Patterns: RESTful Graph Data Exposure
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `app/api/connectome/graphs/route.ts`

**Sections:**
- # OBJECTIFS: Connectome Graphs Module
- ## Context
- ## Objectives
- ## Non-Objectives
- ## CHAIN

**Code refs:**
- `app/api/connectome/graphs/route.ts`
- `route.ts`

**Sections:**
- # PATTERNS: Connectome Graphs Module
- ## Context
- ## Patterns
- ## Anti-Patterns
- ## CHAIN

**Code refs:**
- `app/api/connectome/graphs/route.ts`

**Doc refs:**
- `docs/connectome/graphs/OBJECTIFS_Connectome_Graphs.md`
- `docs/connectome/graphs/PATTERNS_Connectome_Graphs.md`
- `docs/connectome/graphs/SYNC_Connectome_Graphs_Sync_Current_State.md`

**Sections:**
- # SYNC: Connectome Graphs Module Sync Current State
- ## Current State
- ## GAPS
- ## CONFLICTS
- ## CHAIN

**Sections:**
- # Connectome Health SSE Payload (v0)

**Sections:**
- # Moment Graph Engine — HEALTH: Connectome Live Signals
- ## PURPOSE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## INDICATOR: query_write_attempts
- ## INDICATOR: interrupt_reason_stream
- ## INDICATOR: attention_sink_stats
- ## INDICATOR: focus_reconfig_rate
- ## INDICATOR: contradiction_pressure
- ## INDICATOR: async_epoch_mismatch
- ## INDICATOR: dmz_violation_attempts
- ## HOW TO RUN (MANUAL)
- ## DISPLAY (CONNECTOME PAGE)

**Sections:**
- # Integration Notes — Connectome Health (v0)
- ## Backend wiring (minimal)
- ## Frontend wiring (minimal)

**Sections:**
- # OBJECTIFS — Connectome Health
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # OBJECTIFS — Connectome Health Panel: Metrics Display and Realtime Feedback
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)
- ## MARKERS

**Code refs:**
- `app/connectome/components/connectome_health_panel.ts`

**Sections:**
- # Connectome Health Panel — Patterns: Live Monitoring and Invariants Visualization
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `app/api/connectome/graph/route.ts`
- `app/connectome/components/connectome_log_export_buttons_using_state_store_serializers.tsx`
- `app/connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`

**Sections:**
- # log_panel — Algorithm: Rendering, Duration Coloring, Trigger Badges, and Export
- ## CHAIN
- ## OVERVIEW
- ## OBJECTIVES AND BEHAVIORS
- ## DATA STRUCTURES
- ## ALGORITHM: `render_log_panel(store_state)`
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## ALGORITHM: `render_now_section(store_state)`
- ## ALGORITHM: `render_ledger_list(store_state)`
- ## ALGORITHM: duration formatting and coloring
- ## ALGORITHM: export
- ## MARKERS

**Sections:**
- # log_panel — Behaviors: Step Clarity and Copyable Audit Trail
- ## CHAIN
- ## OBJECTIVES SERVED
- ## INPUTS / OUTPUTS
- ## BEHAVIORS
- ## ANTI-BEHAVIORS
- ## EDGE CASES
- ## MARKERS

**Sections:**
- # log_panel — Health: Verification of Log Truth and Export Integrity
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## OBJECTIVES COVERAGE
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: log_now_matches_last_event_integrity
- ## INDICATOR: log_duration_color_mapping_integrity
- ## INDICATOR: log_export_equals_ledger_integrity
- ## HOW TO RUN
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `app/connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts`
- `app/connectome/components/connectome_log_export_buttons_using_state_store_serializers.ts`
- `app/connectome/components/connectome_log_export_buttons_using_state_store_serializers.tsx`
- `app/connectome/components/connectome_log_trigger_and_calltype_badge_color_tokens.ts`
- `app/connectome/components/unified_now_and_copyable_ledger_log_panel.ts`
- `app/connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`

**Sections:**
- # log_panel — Implementation: Component Structure and Serializer Integration
- ## CHAIN
- ## DESIGN PATTERNS
- ## SCHEMA
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CODE STRUCTURE
- ## ENTRY POINTS
- ## DATA FLOW
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Log Panel
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # log_panel — Patterns: Unified Explain + Copyable Event Ledger View
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `app/api/connectome/graph/route.ts`
- `app/api/connectome/graphs/route.ts`
- `app/api/connectome/search/route.ts`
- `app/connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts`
- `app/connectome/components/connectome_log_export_buttons_using_state_store_serializers.tsx`
- `app/connectome/components/connectome_log_trigger_and_calltype_badge_color_tokens.ts`
- `app/connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`

**Doc refs:**
- `docs/connectome/log_panel/ALGORITHM_Connectome_Log_Panel_Log_Rendering_Duration_Coloring_And_Export.md`
- `docs/connectome/log_panel/BEHAVIORS_Connectome_Log_Panel_Step_Clarity_And_Copyable_Audit_Trail_Effects.md`
- `docs/connectome/log_panel/HEALTH_Connectome_Log_Panel_Runtime_Verification_Of_Log_Truth_And_Export_Integrity.md`
- `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md`
- `docs/connectome/log_panel/PATTERNS_Connectome_Log_Panel_Unified_Explain_And_Copyable_Event_Ledger_View_Patterns.md`
- `docs/connectome/log_panel/SYNC_Connectome_Log_Panel_Sync_Current_State.md`
- `docs/connectome/log_panel/VALIDATION_Connectome_Log_Panel_Invariants_For_Truthful_Durations_And_Stable_Export.md`
- `docs/engine/membrane/PATTERN_Membrane_Modulation.md`

**Sections:**
- # log_panel — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## TODO
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Sections:**
- # log_panel — Validation: Invariants for Truthful Durations and Stable Export
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # node_kit — Algorithm: Node Rendering Spec and Energy Glow Mapping
- ## CHAIN
- ## OVERVIEW
- ## OBJECTIVES AND BEHAVIORS
- ## DATA STRUCTURES
- ## ALGORITHM: render_node
- ## KEY DECISIONS
- ## DATA FLOW
- ## HELPER FUNCTIONS
- ## ALGORITHM: map_energy_to_color
- ## ALGORITHM: wait_progress_display
- ## INTERACTIONS
- ## COMPLEXITY
- ## MARKERS

**Sections:**
- # node_kit - Behaviors: Visible Clarity and Trust Effects
- ## CHAIN
- ## OBJECTIVES SERVED
- ## BEHAVIORS
- ## ANTI-BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## MARKERS

**Sections:**
- # node_kit — Health: Runtime Verification of Node Signal Truthfulness
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## OBJECTIVES COVERAGE
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: node_active_step_singularity_integrity
- ## INDICATOR: node_energy_color_bucket_integrity
- ## INDICATOR: node_wait_progress_clamp_integrity
- ## INDICATOR: node_tick_cron_progress_clamp_integrity
- ## HOW TO RUN
- # Run all node_kit health checks (highlight, energy, wait, tick)
- # Run a specific checker when you only touched one widget
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `app/connectome/components/node_kit/connectome_energy_badge_bucketed_glow_and_value_formatter.ts`
- `app/connectome/components/node_kit/connectome_energy_badge_bucketed_glow_and_value_formatter.tsx`
- `app/connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts`
- `app/connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.ts`
- `app/connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`
- `app/connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.ts`
- `app/connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.tsx`
- `app/connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.ts`
- `app/connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.tsx`
- `app/connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.ts`
- `app/connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.tsx`
- `app/connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.ts`
- `app/connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.tsx`
- `connectome_energy_badge_bucketed_glow_and_value_formatter.ts`
- `connectome_node_background_theme_tokens_by_type_and_language.ts`

**Doc refs:**
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md`
- `docs/connectome/node_kit/PATTERNS_Connectome_Node_Kit_Typed_Language_Coded_Energy_Aware_Node_Rendering_Patterns.md`
- `event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md`
- `runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md`
- `state_store/IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md`

**Sections:**
- # node_kit — Implementation: Component Map and Styling Tokens
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## STYLING TOKENS (V1)
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Node Kit
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # node_kit — Patterns: Typed, Language-Coded, Energy-Aware Node Rendering
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## NODE TYPES (V1)
- ## DEPENDENCIES
- ## DATA
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Doc refs:**
- `docs/connectome/node_kit/BEHAVIORS_Connectome_Node_Kit_Visible_Clarity_And_Trust_Effects.md`
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`
- `docs/connectome/node_kit/PATTERNS_Connectome_Node_Kit_Typed_Language_Coded_Energy_Aware_Node_Rendering_Patterns.md`
- `docs/connectome/node_kit/VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md`

**Sections:**
- # node_kit - Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## AGENT OBSERVATIONS
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## ARCHIVE

**Code refs:**
- `app/connectome/components/node_kit/connectome_energy_badge_bucketed_glow_and_value_formatter.tsx`
- `app/connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts`
- `app/connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`
- `app/connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.tsx`
- `app/connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.tsx`
- `app/connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.tsx`
- `app/connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.tsx`

**Doc refs:**
- `docs/connectome/node_kit/ALGORITHM_Connectome_Node_Kit_Node_Rendering_Spec_And_Energy_Glow_Mapping.md`
- `docs/connectome/node_kit/BEHAVIORS_Connectome_Node_Kit_Visible_Clarity_And_Trust_Effects.md`
- `docs/connectome/node_kit/HEALTH_Connectome_Node_Kit_Runtime_Verification_Of_Node_State_And_Visual_Signal_Truth.md`
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`
- `docs/connectome/node_kit/PATTERNS_Connectome_Node_Kit_Typed_Language_Coded_Energy_Aware_Node_Rendering_Patterns.md`
- `docs/connectome/node_kit/SYNC_Connectome_Node_Kit_Sync_Current_State.md`
- `docs/connectome/node_kit/VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md`
- `docs/engine/membrane/PATTERN_Membrane_Modulation.md`

**Sections:**
- # Archived: SYNC_Connectome_Node_Kit_Sync_Current_State.md
- ## RECENT CHANGES
- ## TODO

**Sections:**
- # node_kit — Validation: Invariants for Readability and Correct State Reflection
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## PROPERTIES
- ## INVARIANTS
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # page_shell — Algorithm: Control Dispatch and Layout Composition
- ## CHAIN
- ## NOTES

**Sections:**
- # page_shell — Behaviors: Stable Workflow and Mode Control Effects
- ## CHAIN
- ## NOTES

**Sections:**
- # page_shell — Health: Runtime Verification of Control Semantics and Mode Gating
- ## CHAIN
- ## NOTES

**Sections:**
- # page_shell — Implementation: Next.js Route and Component Wiring
- ## CHAIN
- ## NOTES

**Sections:**
- # OBJECTIFS — Page Shell
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `app/connectome/components/connectome_page_shell_route_layout_and_control_surface.ts`

**Sections:**
- # page_shell — Patterns: Route Composition and User Control Surface
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `app/connectome/components/connectome_page_shell_route_layout_and_control_surface.tsx`
- `app/connectome/page.tsx`

**Sections:**
- # page_shell — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## TODO
- ## HANDOFF

**Sections:**
- # page_shell — Validation: Invariants for Control Correctness and No Drift
- ## CHAIN
- ## NOTES

**Sections:**
- # runtime_engine — Algorithm: Step Release Gate and Realtime Scheduling
- ## CHAIN
- ## OVERVIEW
- ## OBJECTIVES AND BEHAVIORS
- ## ALGORITHM: `runtime_engine_step_release_and_realtime_scheduler()`
- ## DATA STRUCTURES
- ## ALGORITHM: `release_next_step()`
- ## ALGORITHM: `dispatch_runtime_command(cmd)`
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Sections:**
- # runtime_engine — Behaviors: User-Controlled Traversal and Playback Effects
- ## CHAIN
- ## BEHAVIORS
- ## OBJECTIVES SERVED
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # runtime_engine — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## OBJECTIVES COVERAGE
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: runtime_stepper_single_step_integrity
- ## INDICATOR: runtime_speed_authorization_separation
- ## INDICATOR: runtime_min_duration_enforced
- ## INDICATOR: runtime_autoplay_leak_detector
- ## HOW TO RUN
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `app/connectome/lib/connectome_step_script_sample_sequence.ts`
- `app/connectome/lib/connectome_system_map_node_edge_manifest.ts`
- `app/connectome/lib/connectome_wait_timer_progress_and_tick_display_signal_selectors.ts`
- `app/connectome/lib/next_step_gate_and_realtime_playback_runtime_engine.ts`
- `app/connectome/page.tsx`
- `connectome_system_map_node_edge_manifest.ts`

**Sections:**
- # runtime_engine — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Runtime Engine
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # runtime_engine — Patterns: Stepper-Gated Traversal and Realtime Playback Control
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## DATA STRUCTURES
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Code refs:**
- `app/connectome/lib/connectome_step_script_sample_sequence.ts`
- `app/connectome/lib/minimum_duration_clamp_and_speed_based_default_policy.ts`
- `app/connectome/lib/next_step_gate_and_realtime_playback_runtime_engine.ts`
- `app/connectome/lib/step_script_cursor_and_replay_determinism_helpers.ts`

**Doc refs:**
- `docs/connectome/runtime_engine/ALGORITHM_Connectome_Runtime_Engine_Step_Release_And_Realtime_Scheduling.md`
- `docs/connectome/runtime_engine/BEHAVIORS_Connectome_Runtime_Engine_User_Controlled_Traversal_Effects.md`
- `docs/connectome/runtime_engine/HEALTH_Connectome_Runtime_Engine_Runtime_Verification_Of_Pacing_And_Order.md`
- `docs/connectome/runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md`
- `docs/connectome/runtime_engine/PATTERNS_Connectome_Runtime_Engine_Stepper_And_Realtime_Traversal_Control_Patterns.md`
- `docs/connectome/runtime_engine/SYNC_Connectome_Runtime_Engine_Sync_Current_State.md`
- `docs/connectome/runtime_engine/VALIDATION_Connectome_Runtime_Engine_Invariants_For_Stepper_And_Realtime.md`
- `docs/engine/membrane/PATTERN_Membrane_Modulation.md`

**Sections:**
- # runtime_engine — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## TODO
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Sections:**
- # runtime_engine — Validation: Invariants for Stepper Gating and Realtime Playback
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Run tests
- # Run with coverage
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Connectome Search API
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)
- ## MARKERS

**Code refs:**
- `app/api/connectome/search/route.ts`

**Sections:**
- # Connectome Search API — Patterns: API Gateway for Graph Search
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Sections:**
- # state_store — Algorithm: Atomic Commits for Releases, Focus, and Timers
- ## CHAIN
- ## OVERVIEW
- ## OBJECTIVES AND BEHAVIORS
- ## DATA STRUCTURES
- ## ALGORITHM: `commit_step_release_append_event_and_set_focus_and_explanation(release)`
- ## ALGORITHM: `restart_session_clear_or_boundary()`
- ## ALGORITHM: `append_realtime_event_and_update_focus_if_needed(event)` (deferred)
- ## KEY DECISIONS
- ## DATA FLOW
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## ALGORITHM: wait progress computation (selector)
- ## COMPLEXITY
- ## MARKERS

**Sections:**
- # state_store — Behaviors: Observable Effects of a Single Canonical Store
- ## CHAIN
- ## OBJECTIVES SERVED
- ## BEHAVIORS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## INPUTS / OUTPUTS
- ## MARKERS

**Sections:**
- # state_store — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## OBJECTIVES COVERAGE
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: store_ledger_append_only_integrity
- ## INDICATOR: store_atomic_commit_integrity
- ## INDICATOR: store_single_focus_integrity
- ## INDICATOR: store_wait_timer_clamp_integrity
- ## INDICATOR: store_export_equals_ledger
- ## INDICATOR: store_restart_policy_consistency
- ## HOW TO RUN
- # Run all state_store health checks
- # Run a specific indicator checker only
- ## KNOWN GAPS
- ## MARKERS

**Sections:**
- # state_store — Implementation: Code Architecture and Structure
- ## CHAIN
- ## SCHEMA
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## STATE MANAGEMENT
- ## CONFIGURATION
- ## MODULE DEPENDENCIES
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## BIDIRECTIONAL LINKS
- ## MARKERS
- ## AGENT OBSERVATIONS

**Sections:**
- # OBJECTIFS — State Store
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # state_store — Patterns: Single Source of Truth for Ledger, Focus, and Timers
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## ENTRY POINTS (ACTIONS)
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## MARKERS

**Doc refs:**
- `docs/connectome/state_store/BEHAVIORS_Connectome_State_Store_Observable_State_Consistency_Effects.md`
- `docs/connectome/state_store/HEALTH_Connectome_State_Store_Runtime_Verification_Of_Ledger_And_Timer_Correctness.md`
- `docs/connectome/state_store/IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md`
- `docs/connectome/state_store/PATTERNS_Connectome_State_Store_Single_Source_Of_Truth_For_Events_Focus_And_Timers.md`

**Sections:**
- # state_store — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## TODO
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## POINTERS
- ## CONSCIOUSNESS TRACE
- ## ARCHIVE

**Code refs:**
- `app/connectome/lib/connectome_export_jsonl_and_text_log_serializer.ts`
- `app/connectome/lib/connectome_session_boundary_and_restart_policy_controller.ts`
- `app/connectome/lib/connectome_wait_timer_progress_and_tick_display_signal_selectors.ts`
- `app/connectome/lib/zustand_connectome_state_store_with_atomic_commit_actions.ts`

**Doc refs:**
- `docs/connectome/state_store/ALGORITHM_Connectome_State_Store_Atomic_Commits_For_Step_Releases_And_Realtime.md`
- `docs/connectome/state_store/BEHAVIORS_Connectome_State_Store_Observable_State_Consistency_Effects.md`
- `docs/connectome/state_store/HEALTH_Connectome_State_Store_Runtime_Verification_Of_Ledger_And_Timer_Correctness.md`
- `docs/connectome/state_store/IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md`
- `docs/connectome/state_store/PATTERNS_Connectome_State_Store_Single_Source_Of_Truth_For_Events_Focus_And_Timers.md`
- `docs/connectome/state_store/SYNC_Connectome_State_Store_Sync_Current_State.md`
- `docs/connectome/state_store/VALIDATION_Connectome_State_Store_Invariants_For_Ledger_Ordering_And_Focus.md`
- `docs/engine/membrane/PATTERN_Membrane_Modulation.md`

**Sections:**
- # Archived: SYNC_Connectome_State_Store_Sync_Current_State.md
- ## RECENT CHANGES
- ## AGENT OBSERVATIONS

**Sections:**
- # state_store — Validation: Invariants for Ledger, Focus, and Timers
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # telemetry_adapter — Algorithm: SSE Subscribe, Parse, Envelope, Emit
- ## CHAIN
- ## DATA STRUCTURES
- ## ALGORITHM: `connect_to_sse_stream(stream_config)`
- ## ALGORITHM: `on_sse_message(frame) → RawTelemetryEnvelope`
- ## ALGORITHM: local pause buffering gate (owned jointly with runtime_engine)
- ## ALGORITHM: rate estimation (health signal)
- ## COMPLEXITY
- ## MARKERS

**Sections:**
- # telemetry_adapter — Behaviors: Realtime Ingestion, Buffering, and Backpressure Effects
- ## CHAIN
- ## BEHAVIORS
- ## ANTI-BEHAVIORS
- ## EDGE CASES
- ## MARKERS

**Sections:**
- # telemetry_adapter — Health: Stream Integrity, Parse Errors, Rate, and Buffer Bounds
- ## PURPOSE OF THIS FILE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## CHECKER INDEX
- ## HOW TO RUN
- ## KNOWN GAPS
- ## MARKERS

**Sections:**
- # telemetry_adapter — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Telemetry Adapter
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # telemetry_adapter — Patterns: SSE-to-FlowEvent Docking for Realtime Connectome Playback
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Sections:**
- # telemetry_adapter — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## TODO

**Sections:**
- # telemetry_adapter — Validation: Invariants for Stream Integrity, Ordering, and No Silent Drops
- ## CHAIN
- ## INVARIANTS
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## MARKERS

**Sections:**
- # VISUAL STYLE GUIDE: The Connectome
- ## Introduction: A Declaration of Intent
- ## 1. Aesthetic Manifesto: Physics Over Psychology
- ## 2. Color Palette: The Substance of the System
- ## 3. Typography & Iconography: The Written Record
- ## 4. Component Styling: Nodes, Edges, and the Ledger
- ## 5. Motion Physics: Weight, Friction, and Consequence

**Code refs:**
- `ngram/core_utils.py`

**Sections:**
- # Core Utils — Algorithm: Template Path Resolution and Doc Discovery
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: `get_templates_path()`
- ## ALGORITHM: `find_module_directories(docs_dir)`
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Code refs:**
- `ngram/core_utils.py`

**Sections:**
- # Core Utils — Behaviors: Template Path Resolution and Docs Discovery
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Sections:**
- # Core Utils — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## CHECKER INDEX
- ## INDICATOR: templates_path_valid
- ## INDICATOR: docs_module_discovery_valid
- ## HOW TO RUN
- # Manual checks only
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `ngram/core_utils.py`

**Doc refs:**
- `docs/core_utils/PATTERNS_Core_Utils_Functions.md`

**Sections:**
- # Core Utils — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Core Utils
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `ngram/core_utils.py`

**Sections:**
- # PATTERNS: Core Utility Functions
- ## CHAIN
- ## WHY THIS SHAPE
- ## SCOPE
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## IMPLEMENTATION REFERENCES
- ## MARKERS

**Code refs:**
- `core_utils.py`
- `ngram/core_utils.py`
- `utils.py`

**Doc refs:**
- `docs/core_utils/ALGORITHM_Core_Utils_Template_Path_And_Module_Discovery.md`
- `docs/core_utils/ALGORITHM_Template_Path_Resolution_And_Doc_Discovery.md`
- `docs/core_utils/PATTERNS_Core_Utils_Functions.md`

**Sections:**
- # SYNC: Core Utility Functions State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## GAPS

**Code refs:**
- `ngram/core_utils.py`

**Sections:**
- # Core Utils — Validation: Core Utility Invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # No tests currently exist for core_utils.
- # Add tests under tests/core_utils/ if behaviors become critical.
- ## SYNC STATUS
- ## MARKERS

**Code refs:**
- `engine/membrane/functions.py`
- `engine/membrane/provider.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/moment_graph/traversal.py`

**Sections:**
- # Engine — Algorithm: Membrane Modulation Frame
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: compute_modulation_frame
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS
- ## COMPUTE SKELETON (V0)

**Code refs:**
- `engine/physics/tick.py`

**Sections:**
- # Engine — Behaviors: Membrane Modulation Effects
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Code refs:**
- `engine/membrane/health_check.py`

**Sections:**
- # Membrane Modulation — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## CHECKER INDEX
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/moment_graph/traversal.py`

**Sections:**
- # Engine — Implementation: Membrane Modulation (Scoping + Hooks)
- ## CHAIN
- ## OVERVIEW
- ## CODE STRUCTURE (PLANNED)
- ## ENTRY POINTS (PLANNED)
- ## RESPONSIBILITIES
- ## DATA FLOW (PLANNED)
- ## MARKERS

**Code refs:**
- `engine/membrane/functions.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/physics/tick.py`

**Doc refs:**
- `docs/physics/PATTERNS_Physics.md`

**Sections:**
- # Engine — Patterns: Membrane Scoping (Per-Place Modulation)
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `engine/physics/tick.py`

**Doc refs:**
- `docs/engine/moments/PATTERNS_Moments.md`
- `docs/physics/PATTERNS_Physics.md`

**Sections:**
- # Engine — Patterns: Membrane Modulation (Pre-Runtime Field Shaping)
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Doc refs:**
- `docs/engine/membrane/BEHAVIORS_Membrane_Modulation.md`
- `docs/engine/membrane/PATTERNS_Membrane_Scoping.md`
- `docs/engine/membrane/PATTERN_Membrane_Modulation.md`
- `docs/engine/membrane/SYNC_Membrane_Modulation.md`
- `docs/physics/attention/PATTERNS_Attention_Energy_Split.md`

**Sections:**
- # Membrane Modulation — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## IN PROGRESS
- ## TODO
- ## POINTERS

**Code refs:**
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/physics/tick.py`

**Sections:**
- # Engine — Validation: Membrane Modulation Invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # No automated tests yet
- ## MARKERS

**Code refs:**
- `engine/infrastructure/embeddings/service.py`

**Sections:**
- # Data Models — Algorithm: Pydantic Data Flow and Validation
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: model_instantiate_and_validate
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Sections:**
- # Data Models — Behaviors: Consistent Data Interactions
- ## CHAIN
- ## OVERVIEW
- ## BEHAVIORS
- ## MARKERS

**Sections:**
- # Data Models — Health: Pydantic Schema Integrity
- ## PURPOSE OF THIS FILE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## CHECKER INDEX
- ## INDICATOR: model_validation_success
- ## HOW TO RUN
- # Execute all tests for the data models module
- # Run Pydantic schema consistency checks
- ## MARKERS

**Code refs:**
- `engine/models/__init__.py`
- `engine/models/base.py`
- `engine/models/links.py`
- `engine/models/nodes.py`

**Doc refs:**
- `docs/engine/models/PATTERNS_Models.md`
- `docs/engine/models/VALIDATION_Models.md`
- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`

**Sections:**
- # Data Models — Implementation: Pydantic Code Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Code refs:**
- `base.py`

**Sections:**
- # Data Models — Patterns: Pydantic for Graph Schema Enforcement
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `engine/models/base.py`
- `engine/models/links.py`
- `engine/models/nodes.py`
- `nodes.py`

**Doc refs:**
- `docs/engine/models/HEALTH_Models.md`
- `docs/engine/models/PATTERNS_Models.md`

**Sections:**
- # Data Models — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## Agent Observations
- ## GAPS
- ## CHAIN

**Sections:**
- # Data Models — Validation: Pydantic Invariants and Properties
- ## CHAIN
- ## OVERVIEW
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Run all tests for data models
- # Run tests specifically for base models and enums
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # Moment Graph Engine — Validation: Player DMZ Invariants (Stub)
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # Moment Graph Engine — Validation: Simultaneity + CONTRADICTS (Stub)
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## VERIFICATION PROCEDURE
- ## MARKERS

**Sections:**
- # Moment Graph Engine — Validation: Void Tension (Stub)
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## MARKERS

**Code refs:**
- `engine/moment_graph/traversal.py`

**Sections:**
- # Moment Graph Engine — Algorithm: Click, Wait, Surfacing
- ## CHAIN
- ## CLICK TRAVERSAL
- ## WAIT TRIGGER TRAVERSAL
- ## SURFACING AND DECAY
- ## SCENE CHANGE
- ## TENSION BOOST

**Code refs:**
- `engine/moment_graph/__init__.py`

**Sections:**
- # Moment Graph Engine — Behaviors: Traversal And Surfacing
- ## CHAIN
- ## OBSERVABLE BEHAVIORS
- ## INPUTS AND OUTPUTS
- ## SIDE EFFECTS

**Code refs:**
- `engine/moment_graph/__init__.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/moment_graph/traversal.py`
- `engine/physics/graph/graph_ops.py`
- `engine/physics/graph/graph_queries.py`

**Sections:**
- # Moment Graph Engine — Implementation: Runtime Layout
- ## CHAIN
- ## FILES AND ROLES
- ## DATA FLOW
- ## DEPENDENCIES

**Code refs:**
- `engine/moment_graph/__init__.py`

**Sections:**
- # Moment Graph Engine — Patterns: Instant Traversal Hot Path
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## MARKERS

**Code refs:**
- `engine/moment_graph/__init__.py`
- `engine/moment_graph/queries.py`

**Sections:**
- # Moment Graph Engine — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## HANDOFF: FOR AGENTS
- ## TODO
- ## CONFLICTS
- ## Agent Observations
- ## ARCHIVE

**Code refs:**
- `engine/moment_graph/__init__.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/moment_graph/traversal.py`

**Doc refs:**
- `docs/physics/attention/VALIDATION_Attention_Split_And_Interrupts.md`

**Sections:**
- # Archived: SYNC_Moment_Graph_Engine.md
- ## RECENT CHANGES

**Code refs:**
- `engine/moment_graph/traversal.py`
- `engine/tests/test_e2e_moment_graph.py`
- `engine/tests/test_moment_graph.py`

**Sections:**
- # Moment Graph Engine — Tests: Runtime Coverage
- ## CHAIN
- ## EXISTING TESTS
- ## HOW TO RUN
- # Requires FalkorDB running on localhost:6379
- ## GAPS

**Code refs:**
- `engine/moment_graph/traversal.py`

**Sections:**
- # Moment Graph Engine — Validation: Traversal Invariants
- ## CHAIN
- ## INVARIANTS
- ## PERFORMANCE EXPECTATIONS
- ## FAILURE MODES TO WATCH

**Code refs:**
- `engine/moments/__init__.py`

**Doc refs:**
- `docs/schema/SCHEMA_Moments.md`

**Sections:**
- # Moment Graph — Algorithm: Graph Operations
- ## CHAIN
- ## OVERVIEW
- ## TARGET FLOW
- ## DATA SOURCES

**Code refs:**
- `engine/moments/__init__.py`

**Doc refs:**
- `docs/schema/SCHEMA_Moments.md`

**Sections:**
- # Moment Graph — Behaviors: Moment Lifecycle
- ## CHAIN
- ## BEHAVIOR SUMMARY
- ## EXPECTED BEHAVIORS
- ## NOTES

**Code refs:**
- `engine/moments/__init__.py`

**Sections:**
- # Moment Graph — Implementation: Stub Layout
- ## CHAIN
- ## FILES
- ## CURRENT IMPLEMENTATION NOTES

**Code refs:**
- `engine/moments/__init__.py`

**Sections:**
- # Moment Graph — Patterns
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## MARKERS

**Code refs:**
- `engine/moments/__init__.py`

**Doc refs:**
- `docs/engine/moments/PATTERNS_Moments.md`
- `docs/engine/moments/SYNC_Moments.md`
- `docs/schema/SCHEMA_Moments.md`

**Sections:**
- # Moment Graph — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO

**Code refs:**
- `engine/moments/__init__.py`
- `engine/tests/test_e2e_moment_graph.py`
- `engine/tests/test_moment_graph.py`
- `engine/tests/test_moment_lifecycle.py`
- `engine/tests/test_moments_api.py`

**Sections:**
- # Moment Graph — Test Coverage
- ## CHAIN
- ## CURRENT COVERAGE
- ## GAPS
- ## HOW TO RUN

**Code refs:**
- `engine/moments/__init__.py`

**Doc refs:**
- `docs/schema/SCHEMA_Moments.md`

**Sections:**
- # Moment Graph — Validation: Invariants
- ## CHAIN
- ## INVARIANTS
- ## VERIFICATION NOTES

**Sections:**
- # Engine — Algorithm: High-Level Flow
- ## CHAIN
- ## HIGH-LEVEL FLOW

**Sections:**
- # Engine — Behaviors: Runtime Effects
- ## CHAIN
- ## BEHAVIORS

**Sections:**
- # Engine — Health: Verification
- ## CHAIN
- ## HEALTH CHECKS

**Sections:**
- # Engine — Implementation: Code Mapping
- ## CHAIN
- ## CODE LOCATIONS
- ## NOTES

**Sections:**
- # OBJECTIFS — Engine
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # Engine — Patterns: Runtime Ownership And Boundaries
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES

**Sections:**
- # Engine — Sync: Current State
- ## CHAIN
- ## CURRENT STATE
- ## TODO

**Sections:**
- # Engine — Validation: Invariants
- ## CHAIN
- ## INVARIANTS

**Code refs:**
- `layout.tsx`

**Sections:**
- # OBJECTIFS — App Shell
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)
- ## MARKERS

**Code refs:**
- `app/layout.ts`
- `app/layout.tsx`
- `app/page.ts`
- `app/page.tsx`
- `layout.tsx`
- `page.tsx`

**Sections:**
- # App Shell — Patterns: Consistent Layout and Global Functionality for Next.js Application
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `app.py`
- `app/api/route.ts`
- `app/layout.tsx`
- `app/ngram/page.tsx`
- `app/page.tsx`
- `layout.tsx`
- `page.tsx`

**Doc refs:**
- `docs/frontend/app_shell/OBJECTIFS_App_Shell.md`
- `docs/frontend/app_shell/PATTERNS_App_Shell.md`
- `docs/frontend/app_shell/SYNC_App_Shell_State.md`

**Sections:**
- # App Shell — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE

**Code refs:**
- `engine/infrastructure/api/playthroughs.py`
- `engine/init_db.py`
- `engine/physics/graph/graph_ops.py`
- `frontend/app/scenarios/page.tsx`
- `frontend/app/start/page.tsx`
- `frontend/hooks/useGameState.ts`

**Sections:**
- # API — Algorithm
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: create_scenario_playthrough
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS
- ## Graph Helpers
- ## Health Check
- ## Debug Mutation Stream
- ## Playthrough Creation
- ## CHAIN

**Code refs:**
- `app.py`
- `graph_ops_moments.py`
- `narrator.py`
- `orchestrator.py`
- `surface.py`

**Sections:**
- # Player Input → Moment Output Flow
- ## Overview
- ## Fast Path: Word Click
- ## Full Path: Action
- ## Thresholds
- ## Validation
- # 1. Create playthrough
- # 2. Get current moments
- # 3. Click a word (get moment_id from step 2)
- # 4. Verify weight changed
- # Action with narrator
- ## Chain

**Code refs:**
- `engine/infrastructure/api/graphs.py`
- `engine/infrastructure/api/playthroughs.py`

**Sections:**
- # Graph Management API
- ## Purpose
- ## Endpoints
- ## Implementation Notes
- ## Migration: What Moves to blood-ledger
- ## Status

**Sections:**
- # API — Behaviors
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## Health Check
- ## Debug Mutation Stream
- ## ANTI-BEHAVIORS
- ## MARKERS
- ## CHAIN

**Code refs:**
- `engine/infrastructure/api/app.py`
- `engine/tests/test_moments_api.py`
- `engine/tests/test_router_schema_validation.py`

**Sections:**
- # API — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: api_availability
- ## MANUAL RUN
- # Verify API Health
- # Verify Action Loop
- ## KNOWN GAPS

**Sections:**
- # API — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # API — Patterns
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS
- ## CHAIN

**Code refs:**
- `app.py`
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/api/moments.py`
- `engine/tests/test_moments_api.py`
- `engine/tests/test_router_schema_validation.py`

**Doc refs:**
- `docs/infrastructure/api/IMPLEMENTATION_Api.md`
- `docs/infrastructure/api/PATTERNS_Api.md`

**Sections:**
- # API — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO
- ## POINTERS
- ## CHAIN

**Code refs:**
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/api/playthroughs.py`

**Doc refs:**
- `docs/infrastructure/api/ALGORITHM_Api.md`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md`
- `docs/infrastructure/api/BEHAVIORS_Api.md`
- `docs/infrastructure/api/IMPLEMENTATION_Api.md`
- `docs/infrastructure/api/PATTERNS_Api.md`
- `docs/infrastructure/api/SYNC_Api.md`
- `docs/infrastructure/api/TEST_Api.md`
- `docs/infrastructure/api/VALIDATION_Api.md`

**Sections:**
- # Archived: SYNC_Api.md
- ## RECENT CHANGES

**Code refs:**
- `engine/tests/test_moments_api.py`
- `engine/tests/test_router_schema_validation.py`

**Doc refs:**
- `docs/infrastructure/api/SYNC_Api.md`

**Sections:**
- # API — Validation
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## CHAIN

**Sections:**
- # Scene Memory System — Legacy Archive (2024-12)
- ## PURPOSE
- ## LEGACY SUMMARY
- ## CANONICAL REFERENCES
- ## NOTE ON REMOVALS

**Code refs:**
- `engine/infrastructure/memory/transcript.py`
- `engine/models/nodes.py`
- `engine/physics/graph/graph_ops.py`

**Sections:**
- # Scene Memory System — Algorithm (Legacy)
- ## CHAIN
- ## STATUS
- ## LEGACY ALGORITHM OUTLINE
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: process_scene_memory (legacy)
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS
- ## CANONICAL REFERENCES
- ## NEXT IN CHAIN

**Sections:**
- # Scene Memory System — Behavior (Legacy)
- ## CHAIN
- ## STATUS
- ## LEGACY BEHAVIOR SUMMARY
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## ANTI-BEHAVIORS
- ## MARKERS
- ## LEGACY EDGE CASES
- ## NEXT IN CHAIN

**Sections:**
- # Scene Memory — Health: Verification Checklist
- ## CHAIN
- ## CHECKS

**Code refs:**
- `engine/infrastructure/memory/__init__.py`
- `engine/infrastructure/memory/moment_processor.py`

**Sections:**
- # Scene Memory System — Implementation: Moment Processing Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## ENTRY POINTS
- ## DATA FLOW (SUMMARY)
- ## LOGIC CHAINS
- ## CONCURRENCY MODEL
- ## MODULE DEPENDENCIES
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Scene-Memory
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # Scene Memory System — Pattern (Legacy)
- ## CHAIN
- ## STATUS
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## LEGACY PATTERN SUMMARY
- ## LEGACY LIMITS
- ## NEXT IN CHAIN

**Code refs:**
- `engine/infrastructure/api/moments.py`
- `engine/infrastructure/memory/moment_processor.py`
- `engine/physics/graph/graph_ops_moments.py`
- `engine/physics/graph/graph_queries_moments.py`

**Sections:**
- # Scene Memory System — Sync
- ## ARCHITECTURE EVOLUTION
- ## IMPLEMENTATION STATUS
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## REPAIR LOG (2025-12-20)
- ## OPEN QUESTIONS
- ## ARCHIVE

**Code refs:**
- `engine/infrastructure/memory/__init__.py`
- `engine/infrastructure/memory/moment_processor.py`
- `engine/models/nodes.py`
- `engine/tests/test_moment.py`
- `moment_processor.py`

**Sections:**
- # Archived: SYNC_Scene_Memory.md
- ## Maturity
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## MOMENT NODE TYPE
- # Moment Graph fields
- # Tick tracking
- # Transcript reference
- ## MOMENT PROCESSOR API
- # Immediate moments (added to transcript)
- # Potential moments (graph only)
- # Links
- ## CHANGELOG
- # Archived: SYNC_Scene_Memory.md
- ## RECENT CHANGES
- # Archived: SYNC_Scene_Memory.md
- ## DOCUMENT CHAIN
- ## REPAIR LOG (2025-12-19)
- ## Agent Observations

**Code refs:**
- `engine/tests/test_e2e_moment_graph.py`
- `engine/tests/test_moment.py`
- `engine/tests/test_moment_graph.py`
- `engine/tests/test_moment_lifecycle.py`
- `engine/tests/test_moments_api.py`

**Sections:**
- # Scene Memory System — Test: Moment Processing Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run MomentProcessor unit tests
- # Run full moment-related suite
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## MARKERS

**Sections:**
- # Scene Memory System — Validation (Legacy)
- ## CHAIN
- ## STATUS
- ## LEGACY INVARIANTS (SUMMARY)
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## LEGACY TEST NOTES
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## MARKERS
- ## NEXT IN CHAIN

**Code refs:**
- `engine/infrastructure/tempo/tempo_controller.py`
- `engine/physics/tick.py`

**Sections:**
- # Tempo Controller — Algorithm: Tick Loop and Pacing
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: run
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Code refs:**
- `engine/infrastructure/tempo/tempo_controller.py`

**Sections:**
- # Tempo Controller — Behaviors: Observable Pacing Effects
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Code refs:**
- `engine/infrastructure/tempo/health_check.py`

**Sections:**
- # Tempo Controller — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: tempo_tick_advances
- ## HOW TO RUN
- # Run all health checks for this module
- # Run a specific checker
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `engine/infrastructure/api/tempo.py`
- `engine/infrastructure/canon/canon_holder.py`
- `engine/infrastructure/tempo/tempo_controller.py`
- `engine/physics/tick.py`

**Sections:**
- # Tempo Controller — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Tempo
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `engine/infrastructure/api/tempo.py`
- `engine/infrastructure/tempo/tempo_controller.py`
- `engine/physics/tick.py`

**Sections:**
- # Tempo Controller — Patterns: Pacing the Main Loop
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `engine/infrastructure/tempo/tempo_controller.py`

**Doc refs:**
- `docs/infrastructure/canon/PATTERNS_Canon.md`
- `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md`
- `docs/infrastructure/tempo/PATTERNS_Tempo.md`

**Sections:**
- # Tempo Controller — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `engine/infrastructure/tempo/tempo_controller.py`

**Sections:**
- # Tempo Controller — Validation: Pacing Invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # No automated tests yet
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # WSL autostart (systemd user)
- ## 1) Activer systemd dans WSL
- ## 2) Activer linger pour l'auto-start
- ## 3) Binaries et chemins absolus
- ## 4) Configurer le frontend
- ## 5) Installer les units systemd
- ## 6) Config ngrok v3
- ## 7) Logs et status
- ## 8) Checks de sante
- ## 9) Depannage

**Code refs:**
- `ngram/llms/gemini_agent.py`

**Sections:**
- # ngram LLM Agents — Algorithm: Gemini Stream Flow
- ## CHAIN
- ## OVERVIEW
- ## OBJECTIVES AND BEHAVIORS
- ## ALGORITHM: main
- ## DATA FLOW
- ## COMPLEXITY
- ## DATA STRUCTURES
- ## KEY DECISIONS
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Sections:**
- # ngram LLM Agents — Behaviors: Gemini Agent Output
- ## CHAIN
- ## BEHAVIORS
- ## NOTES
- ## OBJECTIVES SERVED
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Code refs:**
- `gemini_agent.py`
- `ngram/llms/gemini_agent.py`

**Doc refs:**
- `docs/cli/HEALTH_CLI_Coverage.md`

**Sections:**
- # ngram LLM Agents — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## OBJECTIVES COVERAGE
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## HOW TO USE THIS TEMPLATE
- ## CHECKER INDEX
- ## INDICATOR: Stream Validity
- ## INDICATOR: api_connectivity
- ## HOW TO RUN
- # Manual verification of stream JSON
- # Manual verification of plain text
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `agent_cli.py`
- `gemini_agent.py`
- `ngram/agent_cli.py`
- `ngram/llms/gemini_agent.py`
- `ngram/llms/tool_helpers.py`

**Sections:**
- # ngram LLM Agents — Implementation: Code Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## MODULE LAYOUT
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## MARKERS

**Sections:**
- # OBJECTIFS — Llm Agents
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `agent_cli.py`
- `ngram/llms/gemini_agent.py`

**Sections:**
- # ngram LLM Agents — Patterns: Provider-Specific LLM Subprocesses
- ## CHAIN
- ## THE PROBLEM
- ## SCOPE
- ## DATA
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## MARKERS

**Code refs:**
- `gemini_agent.py`
- `ngram/agent_cli.py`
- `ngram/llms/gemini_agent.py`

**Sections:**
- # LLM Agents — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## TODO
- ## ARCHIVE
- ## ARCHIVE

**Code refs:**
- `ngram/agent_cli.py`
- `ngram/llms/gemini_agent.py`

**Doc refs:**
- `docs/llm_agents/ALGORITHM_Gemini_Stream_Flow.md`
- `docs/llm_agents/BEHAVIORS_Gemini_Agent_Output.md`
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md`
- `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`
- `docs/llm_agents/SYNC_LLM_Agents_State.md`
- `docs/llm_agents/SYNC_LLM_Agents_State_archive_2025-12.md`
- `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md`

**Sections:**
- # Archived: SYNC_LLM_Agents_State.md
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## RECENT CHANGES
- ## TODO
- # No module-specific tests documented yet.
- # Archived: SYNC_LLM_Agents_State.md
- ## RECENT CHANGES
- ## Agent Observations

**Doc refs:**
- `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`

**Sections:**
- # ngram LLM Agents — Validation: Gemini Agent Invariants
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## INVARIANTS
- ## EDGE CASES
- ## VERIFICATION METHODS
- ## FAILURE MODES
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## MARKERS

**Code refs:**
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/doctor.py`
- `ngram/prompt.py`
- `ngram/repair.py`
- `ngram/validate.py`

**Doc refs:**
- `docs/ngram_cli_core/PATTERNS_ngram_cli_core.md`

**Sections:**
- # ngram_cli_core — OBJECTIFS: Core CLI Functionality and Design Goals
- ## CHAIN
- ## OBJECTIVE
- ## CONSTRAINTS
- ## MEASUREMENT

**Code refs:**
- `core_utils.py`
- `doctor_checks.py`
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/doctor.py`
- `ngram/prompt.py`
- `ngram/repair.py`
- `ngram/validate.py`

**Doc refs:**
- `docs/ngram_cli_core/OBJECTIFS_ngram_cli_core.md`

**Sections:**
- # ngram_cli_core — PATTERNS: Design and Implementation Conventions
- ## CHAIN
- ## PATTERNS
- ## ANTI-PATTERNS TO AVOID

**Code refs:**
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/doctor.py`
- `ngram/prompt.py`
- `ngram/repair.py`
- `ngram/validate.py`

**Doc refs:**
- `docs/ngram_cli_core/OBJECTIFS_ngram_cli_core.md`
- `docs/ngram_cli_core/PATTERNS_ngram_cli_core.md`
- `docs/ngram_cli_core/SYNC_ngram_cli_core.md`

**Sections:**
- # ngram_cli_core — SYNC: Project State and Recent Changes
- ## CHAIN
- ## SYNC

**Sections:**
- # OBJECTIFS: Ngram Feature
- ## Chain
- ## 1. Purpose
- ## 2. Current State
- ## 3. Future Intent

**Code refs:**
- `app/ngram/page.tsx`

**Sections:**
- # PATTERNS: Ngram Feature
- ## Chain
- ## 1. Structural Patterns
- ## 2. Integration Patterns
- ## 3. Future Patterns (Anticipated)

**Code refs:**
- `app/ngram/page.tsx`

**Sections:**
- # SYNC: Ngram Feature State
- ## Chain
- ## 1. Current Status
- ## 2. Decisions
- ## 3. Open Questions/Next Steps

**Sections:**
- # Physics — Behaviors: Extended Interactions
- ## CHAIN
- ## Extended Behaviors
- ## B7: Actions Have Consequences
- ## B8: Cascades Create Drama
- ## B9: Characters Have Opinions About Each Other
- ## B10: The World Continues Elsewhere
- ## B11: The Snap
- ## B12: Journey Conversations
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS
- ## Summary: What To Expect

**Doc refs:**
- `docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md`

**Sections:**
- # Physics — Behaviors: What Should Happen
- ## CHAIN
- ## Overview
- ## MECHANISMS (Implementation Anchors)
- ## BEHAVIORS
- ## B1: Instant Display, Eventual Depth
- ## B2: Conversations Are Multi-Participant
- ## B3: Characters Think Unprompted
- ## B4: Silence Is An Answer
- ## B5: Names Have Power
- ## B6: History Is Traversable

**Doc refs:**
- `docs/physics/ALGORITHM_Physics.md`
- `docs/physics/SYNC_Physics.md`
- `docs/physics/TEST_Physics.md`

**Sections:**
- # Physics — Validation: Invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## Core Invariants
- # No state stored outside graph
- # (This is architectural, not queryable)
- # Verify: handlers don't cache state
- # Verify: no files store moment state
- # Verify: display queue reads from graph
- # Physics tick runs continuously
- # (Verify via tick counter)
- # THEN links only from spoken moments
- # THEN links must have tick
- # No THEN links deleted in test run
- # (Track count before/after)
- # All moments created by handler X are ATTACHED_TO character X
- # (This requires tracking handler outputs)
- # Verify in handler code:
- # - No writes to other character's moments
- # - No direct graph modifications outside ATTACHED_TO scope
- # Spoken moments cannot revert to possible
- # THEN links are permanent
- # (No DELETE on THEN links in codebase)
- # Run same scenario at 1x and 3x
- # Compare THEN link chains
- # Should be identical (display differs, canon same)
- # Sum of all weights before tick
- # Tick
- # Sum after = before - decay + injection
- # Handlers only triggered by flip
- # (Verify handler trigger conditions in code)
- # No cooldown logic in handler system
- # No artificial caps on handler runs per tick
- ## Graph State Invariants
- # Status must be valid enum
- # Spoken moments must have tick_spoken
- # Decayed moments must have tick_decayed
- # Weight must be 0-1
- # CAN_SPEAK weight must be 0-1
- # CAN_SPEAK must originate from Character
- # ATTACHED_TO targets must be valid types
- # THEN links connect Moments only
- ## Physics Invariants
- # At 3x speed, total decay over 10 seconds real-time
- # should equal decay at 1x over 10 seconds real-time
- # Same state → same flips
- # After player input, something responds (eventually)
- # Run physics until stable or max ticks
- # Either NPC responded or player character observed silence
- ## Handler Invariants
- # Handler must produce valid moment drafts
- # Handler does NOT set weight
- # Handler output only attaches to its character
- # When injected, should only attach to Aldric
- ## Canon Invariants
- # Two characters grabbing same item should BOTH canonize
- # Both should flip (high weight)
- # Both should be canon
- # Action processing handles the conflict, not canon holder
- # Same character, incompatible actions → mutex
- # Only one should canonize (higher weight)
- ## Speed Invariants
- # At 3x, low-weight moments still create THEN links
- # Not displayed (below threshold)
- # But is canon
- # At 3x, interrupt moments always display
- # Must display (combat is interrupt)
- # Speed should drop to 1x
- ## Action Invariants
- # Actions process one at a time
- # First succeeds
- # Second gets blocked consequence
- # Stale action fails validation
- # Sword already taken by someone else
- # Action should fail validation
- ## Question Answering Invariants
- # Handler doesn't wait for QA
- # Should complete in LLM time, not LLM time × 2 (waiting for QA)
- # QA cannot contradict existing facts
- # Aldric already has a father defined
- # QA for "who is my father" must return existing, not invent new
- # Should reference existing father, not create new one
- ## Performance Benchmarks
- # Setup: 1000 moments, 50 characters, 20 places
- # Setup: 10000 moments
- # 4 characters flip simultaneously
- # Should be ~1 LLM call time, not 4
- ## Verification Checklist
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS

**Doc refs:**
- `docs/physics/SYNC_Physics.md`
- `docs/physics/TEST_Physics.md`

**Sections:**
- # Physics — Validation: Procedures
- ## CHAIN
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # Physics — Algorithm: Energy Flow Sources Sinks And Moment Dynamics (consolidated)
- ## CHAIN
- ## CONSOLIDATION

**Code refs:**
- `engine/moment_graph/queries.py`
- `engine/physics/cluster_energy_monitor.py`
- `engine/physics/display_snap_transition_checker.py`
- `engine/physics/graph/graph_ops_moments.py`
- `engine/physics/graph/graph_queries.py`
- `engine/tests/test_cluster_energy_monitor.py`
- `engine/tests/test_physics_display_snap.py`

**Doc refs:**
- `algorithms/ALGORITHM_Physics_Mechanisms.md`

**Sections:**
- # Physics — Algorithm: Energy Mechanics And Link Semantics
- ## CHAIN
- ## Energy Mechanics
- ## NODE TYPES
- ## LINK TYPES
- ## NARRATIVE TYPES
- ## LINK STRENGTH
- ## STRENGTH MECHANICS (Six Categories)
- # Speaking is stronger than thinking
- # Direct address is strongest
- # Speaker's belief activated
- # ABOUT links activated
- # Check what this evidence supports
- # Check what this evidence contradicts
- # Create new association if co-occurrence is strong enough
- # Recent narratives in same conversation
- # Co-occurring narratives associate
- # How much does receiver trust source?
- # Average trust from relationship narratives
- # Direct witness vs secondhand
- # Higher cost = stronger commitment
- # What beliefs motivated this action?
- # Tension pressure
- # Danger
- # Emotional weight of moment
- # All strength changes multiplied by intensity
- ## Consolidated: Energy Flow Sources, Sinks, And Moment Dynamics
- ## ENERGY SOURCES
- # Baseline regeneration
- # State modifier
- # Pump budget
- # Distribute by belief strength only
- # Things don't hold energy — redirect to related narratives
- # Character arrives — they bring their energy with them
- # News creates/energizes a narrative
- # Discovery energizes existing narrative
- # Draw energy from involved characters
- # Inject into related narratives
- ## ENERGY SINKS
- # Core types resist decay
- # Draw from speakers
- # Draw from attached narratives
- ## ENERGY TRANSFER (Links)
- # A pulls from B
- # B pulls from A
- # Energy flows toward equilibrium
- # Additional drain: old loses extra (world moved on)
- # Things don't hold energy — skip
- # Forward flow
- # Reverse flow only if bidirectional
- # Only if character is awake and present
- # Only nodes with energy
- # Reverse flow: target → moment
- # Partial drain — recent speech still has presence
- # Status change
- # Remaining energy decays normally from here
- ## MOMENT ENERGY & WEIGHT
- ## Consolidated: Tick Cycle Gating, Flips, And Dispatch
- ## FULL TICK CYCLE
- # 1. Characters pump into narratives
- # 2. Narrative-to-narrative transfer
- # 3. ABOUT links (focal point pulls)
- # 4. Moment energy flow
- # 5. Tension injection (structural pressure)
- # 6. Decay (energy leaves system)
- # 7. Detect breaks
- # Energy decay (fast)
- # Check for status transition
- # Weight decay (slow, only without reinforcement)
- ## PHYSICAL GATING
- ## PARAMETERS
- ## EMERGENT BEHAVIORS
- ## M11: FLIP DETECTION
- # Check still valid (state may have changed)
- # Flip to active
- # Handler needed?
- # Async - handler will call record_to_canon when done
- # Direct record
- # ... process ...
- ## M12: CANON HOLDER
- # 1. Status change
- # 2. Energy cost (actualization)
- # 3. THEN link (history chain)
- # 4. Time passage
- # 5. Strength mechanics
- # 6. Actions
- # 7. Notify frontend
- # ABOUT links activated
- # Confirming evidence
- # Contradicting evidence
- # Recent narratives in same conversation
- # Adjust by text length
- # Check for time-based events
- # Decay check (large time jumps)
- # Apply Commitment mechanic (M5)
- # Winner proceeds to canon
- # Loser returns to possible, decayed
- ## M13: AGENT DISPATCH
- # Detect and process breaks
- # Scheduled events
- ## WHAT WE DON'T DO
- ## Consolidated: Handler And Input Processing Flows
- ## Player Input Processing
- # Character names
- # Also check nicknames, titles
- # Place names
- # Thing names
- # ATTACHED_TO player (they said it)
- # ATTACHED_TO current location
- # ATTACHED_TO all present characters (they heard it)
- # REFERENCES for recognized names/things (strong energy transfer)
- # CAN_SPEAK link (player spoke this)
- # Direct references get full energy
- # Boost all moments attached to this character
- # All present characters get partial energy (they heard)
- ## "Aldric, what do you think?"
- ## Aldric directly referenced → full energy boost
- ## "What does everyone think?"
- ## No direct reference → distributed partial energy
- # 1. Parse
- # 2. Create moment
- # 3. Create links
- # 4. Inject energy
- # 5. Emit player moment to display (immediate)
- # 6. Trigger physics tick (may be immediate based on settings)
- # After physics tick, check if anything flipped
- # No response from NPCs
- # Energy flows back to player character
- # Player character's handler will produce observation
- # "The silence stretches. No one meets your eye."
- # Or: pause until submit
- ## Question Answering
- ## In character handler
- # Handler needs to know about father
- # Queue question for answering
- # Handler continues with what it knows
- # Does NOT block waiting for answer
- # 1. GATHER — Get relevant existing facts
- # 2. GENERATE — Invent answer via LLM
- # 3. VALIDATE — Check consistency
- # 4. INJECT — Create nodes in graph
- # Character's existing family
- # Character's origin place
- # Character's existing beliefs/narratives
- # Historical events character witnessed
- # Check family conflicts
- # Check place conflicts
- # Check temporal conflicts
- # Create new character nodes
- # Create relationship link
- # Create new place nodes
- # Create relationship link
- # Create potential memory moments
- # Create ANSWERED_BY link for traceability
- ## After injection, physics handles integration:
- ## New father character exists
- ## Memory moments attached to asker exist
- ## These have initial weight (e.g., 0.4)
- ## Next tick:
- ## - Energy propagates through FAMILY links
- ## - Memory moments may get boosted if relevant
- ## - If weight crosses threshold, memory surfaces
- ## No special "integrate answer" logic
- ## Just physics
- ## Consolidated: Speed Control And Display Filtering
- ## Speed Controller
- # Player character directly addressed
- # Combat initiated
- # Major character arrival
- # Tension threshold crossed
- # Decision point (player choices available)
- # Discovery (new significant narrative)
- # Danger to player or companions
- # Phase 1: Running (player sees this already)
- # - Motion blur effect
- # - Muted colors
- # - Text small, streaming upward
- # Phase 2: The Beat (300-500ms)
- # Phase 3: Arrival
- # - Crystal clear, full color
- # - Large, centered, deliberate
- # Player can resume after input processed
- ## At 3x, low-weight moments:
- ## - Actualize in graph ✓
- ## - Create THEN links ✓
- ## - Become history ✓
- ## - Display to player ✗ (filtered)
- ## Player can review history later
- ## Mechanisms — Function-Level Map (consolidated)

**Sections:**
- # Physics — Algorithm: Handler And Input Processing Flows (consolidated)
- ## CHAIN
- ## CONSOLIDATION

**Code refs:**
- `engine/moment_graph/surface.py`
- `engine/moment_graph/traversal.py`
- `engine/physics/attention_split_sink_mass_distribution_mechanism.py`
- `engine/physics/contradiction_pressure_from_negative_polarity_mechanism.py`
- `engine/physics/graph/graph_ops_moments.py`
- `engine/physics/graph/graph_queries.py`
- `engine/physics/primes_lag_and_half_life_decay_mechanism.py`
- `engine/physics/tick.py`

**Doc refs:**
- `algorithms/ALGORITHM_Physics_Mechanisms.md`

**Sections:**
- # Physics — Algorithm: Mechanisms (Energy, Pressure, Surfacing)
- ## CHAIN
- ## CONSOLIDATION

**Sections:**
- # Physics — Algorithm: Speed Control And Display Filtering (consolidated)
- ## CHAIN
- ## CONSOLIDATION

**Sections:**
- # Physics — Algorithm: Tick Cycle Gating Flips And Dispatch (consolidated)
- ## CHAIN
- ## CONSOLIDATION

**Code refs:**
- `engine/physics/tick.py`

**Doc refs:**
- `implementation/IMPLEMENTATION_Physics_Architecture.md`
- `implementation/IMPLEMENTATION_Physics_Code_Structure.md`
- `implementation/IMPLEMENTATION_Physics_Dataflow.md`
- `implementation/IMPLEMENTATION_Physics_Runtime.md`

**Sections:**
- # Physics — Implementation: Code Architecture and Structure
- ## CHAIN
- ## OVERVIEW
- ## DOCUMENT LAYOUT
- ## SIGNPOSTS

**Code refs:**
- `engine/physics/cluster_energy_monitor.py`
- `engine/physics/display_snap_transition_checker.py`
- `engine/physics/tick.py`

**Doc refs:**
- `docs/physics/SYNC_Physics.md`
- `docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md`

**Sections:**
- # Physics — Sync History (2025-12)
- ## RECENT CHANGES

**Code refs:**
- `engine/handlers/base.py`
- `engine/infrastructure/api/moments.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/traversal.py`
- `engine/physics/tick.py`
- `graph_ops.py`
- `graph_ops_apply.py`
- `graph_ops_events.py`
- `graph_ops_image.py`
- `graph_ops_types.py`
- `graph_queries.py`
- `graph_queries_search.py`

**Doc refs:**
- `docs/physics/ALGORITHM_Physics.md`
- `docs/physics/BEHAVIORS_Physics.md`
- `docs/physics/IMPLEMENTATION_Physics.md`
- `docs/physics/PATTERNS_Physics.md`
- `docs/physics/SYNC_Physics.md`
- `docs/physics/SYNC_Physics_archive_2025-12.md`
- `docs/physics/TEST_Physics.md`
- `docs/physics/VALIDATION_Physics.md`

**Sections:**
- # Archived: SYNC_Physics.md
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## Agent Observations
- # Archived: SYNC_Physics.md
- ## RECENT CHANGES
- ## Agent Observations
- # Archived: SYNC_Physics.md
- ## CHAIN

**Code refs:**
- `engine/physics/attention_split_sink_mass_distribution_mechanism.py`

**Sections:**
- # Physics — Algorithm: Attention Energy Split
- ## CHAIN
- ## OVERVIEW
- ## PROCEDURE (ABRIDGED)

**Code refs:**
- `engine/physics/attention_split_sink_mass_distribution_mechanism.py`

**Sections:**
- # Physics — Behaviors: Attention Split and Interrupts
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Code refs:**
- `engine/physics/attention_split_sink_mass_distribution_mechanism.py`

**Sections:**
- # Physics — Implementation: Attention Energy Split
- ## CHAIN
- ## CODE MAP
- ## NOTES

**Code refs:**
- `engine/physics/attention_split_sink_mass_distribution_mechanism.py`
- `engine/physics/tick.py`

**Doc refs:**
- `docs/engine/membrane/PATTERNS_Membrane_Scoping.md`
- `docs/engine/moments/PATTERNS_Moments.md`
- `docs/physics/PATTERNS_Physics.md`

**Sections:**
- # Physics — Patterns: Attention Energy Split (Focus Redistribution as Physics)
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## INTERRUPT PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `engine/physics/attention_split_sink_mass_distribution_mechanism.py`

**Sections:**
- # Physics — Sync: Attention Energy Split
- ## CURRENT STATE
- ## RECENT CHANGES
- ## TODO

**Sections:**
- # Physics — Validation: Attention Split + Interrupt Invariants
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## INVARIANTS (MUST ALWAYS HOLD)
- ## PROPERTIES (PROPERTY-BASED TESTS)
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / QUESTIONS

**Sections:**
- # Graph — Algorithm: Energy Flow
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: graph_tick
- ## Per-Tick Processing
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS
- ## Step 1: Compute Character Energies
- # Relationship intensity: how much player cares
- # Geographical proximity
- ## Step 2: Flow Energy Into Narratives
- ## Step 3: Propagate Between Narratives
- # Link type factors — each type has its own propagation strength
- # Collect all transfers first (avoid order dependency)
- # Bidirectional: contradiction heats both sides
- # Reverse direction handled when processing from target
- # Bidirectional: allies rise together
- # Unidirectional: general → specific
- # Unidirectional: specific → general
- # Draining: old loses, new gains
- # Apply transfers
- # Apply drains (supersession)
- ## Step 4: Decay Energy
- # Dynamic — adjusted by criticality feedback
- # Apply decay
- # Floor at minimum
- # Skip recently active
- # Core narratives decay slower
- # Focused narratives decay slower
- # System too cold — let it heat
- # System too hot — dampen
- # Clamp to sane range
- # NEVER DYNAMICALLY ADJUST:
- # - breaking_point (changes story meaning)
- # - belief_flow_rate (changes character importance)
- # - link propagation factors (changes story structure)
- ## Step 5: Recompute Weights
- # Clamp and apply focus evolution
- # Direct: player believes it
- # Indirect: about someone player knows
- # Distant: no direct connection
- # Bonus is limited by weaker of the two
- ## Step 6: Tick Pressures
- # Check for flip
- # Tick gradual component
- # Find scheduled floor
- # Use higher of ticked or floor
- ## Step 7: Detect Flips
- ## Full Tick
- # 1. Character energies (relationship × proximity)
- # 2. Flow into narratives (characters pump)
- # 3. Propagate between narratives (link-type dependent)
- # 4. Decay
- # 5. Check conservation (soft global constraint)
- # 6. Adjust criticality (dynamic decay_rate)
- # 7. Weight recomputation
- # 8. Pressure ticks
- # 9. Detect flips
- ## Automatic Tension from Approach
- # Edmund's energy as player approaches York
- # Day 1 (one day travel):
- # Edmund: intensity=4.0, proximity=0.2 → energy=0.8
- # Day 2 (same region):
- # Edmund: intensity=4.0, proximity=0.7 → energy=2.8
- # No one decided this. Physics decided this.
- # Confrontation tension rises because Edmund's narratives heat up.
- ## Parameters Summary
- ## Link Type Factors
- ## Conservation Parameters
- ## Never Adjust Dynamically
- ## CHAIN

**Sections:**
- # Graph — Behaviors: What Should Happen
- ## CHAIN
- ## Overview
- ## BEHAVIORS
- ## Behavior: Companions Matter More
- ## Behavior: Contradictions Intensify Together
- ## Behavior: Support Clusters Rise and Fall Together
- ## Behavior: Old Truths Fade When Replaced
- ## Behavior: Core Oaths Persist
- ## Behavior: Tensions Build Toward Breaking
- ## Behavior: Cascades Ripple Through
- ## Behavior: System Stays Near Criticality
- ## Behavior: Agents Update Links, Not Energy
- ## Summary: What To Expect
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Code refs:**
- `engine/physics/tick.py`

**Doc refs:**
- `docs/schema/SCHEMA_Moments.md`

**Sections:**
- # Graph — Patterns: Why This Shape
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## The Core Insight
- ## Energy As Attention
- ## Computed, Not Declared
- ## Pressure Requires Release
- ## The Graph Breathes
- ## Criticality
- ## What Agents Never Do
- ## MARKERS

**Code refs:**
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/canon/canon_holder.py`
- `engine/infrastructure/orchestration/narrator.py`
- `engine/infrastructure/orchestration/orchestrator.py`
- `engine/infrastructure/orchestration/world_runner.py`
- `engine/physics/graph/graph_interface.py`
- `engine/physics/graph/graph_ops_events.py`
- `engine/physics/graph/graph_ops_read_only_interface.py`
- `engine/physics/graph/graph_ops_types.py`
- `engine/physics/graph/graph_queries_moments.py`
- `engine/physics/tick.py`
- `graph_ops.py`
- `graph_ops_events.py`
- `graph_ops_types.py`
- `orchestrator.py`
- `tick.py`

**Doc refs:**
- `docs/physics/ALGORITHM_Physics.md`
- `docs/physics/IMPLEMENTATION_Physics.md`
- `docs/physics/graph/BEHAVIORS_Graph.md`
- `docs/physics/graph/SYNC_Graph.md`

**Sections:**
- # Graph — Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## What Exists ✓
- ## Two Paths (Both Valid)
- ## Known False Positives
- ## CONFLICTS
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## CHAIN
- ## Agent Observations
- ## Agent Observations
- ## Agent Observations
- ## ARCHIVE
- ## ARCHIVE
- ## ARCHIVE

**Code refs:**
- `engine/graph/health/check_health.py`
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/orchestration/orchestrator.py`
- `engine/physics/graph/connectome_read_cli.py`
- `engine/physics/graph/graph_interface.py`
- `engine/physics/graph/graph_ops.py`
- `engine/physics/graph/graph_ops_events.py`
- `engine/physics/graph/graph_ops_read_only_interface.py`
- `engine/physics/graph/graph_ops_types.py`
- `engine/physics/graph/graph_queries_moments.py`
- `engine/physics/graph/graph_queries_search.py`
- `engine/physics/graph/graph_query_utils.py`
- `graph_ops.py`

**Doc refs:**
- `docs/physics/graph/ALGORITHM_Energy_Flow.md`
- `docs/physics/graph/ALGORITHM_Weight.md`
- `docs/physics/graph/BEHAVIORS_Graph.md`
- `docs/physics/graph/PATTERNS_Graph.md`
- `docs/physics/graph/SYNC_Graph.md`
- `docs/physics/graph/SYNC_Graph_archive_2025-12.md`
- `docs/physics/graph/VALIDATION_Living_Graph.md`

**Sections:**
- # Archived: SYNC_Graph.md
- ## Maturity
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## Key Design Decisions
- ## The Full Energy Cycle
- ## Next Steps
- ## CONFLICTS
- # Archived: SYNC_Graph.md
- ## Key Design Decisions
- ## The Full Energy Cycle
- ## Next Steps
- ## CONFLICTS
- # Archived: SYNC_Graph.md
- ## Key Design Decisions
- ## The Full Energy Cycle
- ## Next Steps
- ## CONFLICTS
- ## Agent Observations
- # Archived: SYNC_Graph.md
- ## Key Design Decisions
- ## The Full Energy Cycle
- ## Next Steps
- ## CONFLICTS
- ## Agent Observations
- # Archived: SYNC_Graph.md
- ## What's Missing: ONE ENDPOINT
- # TODO: SSE streaming version
- ## RECENT CHANGES
- # Archived: SYNC_Graph.md
- ## RECENT CHANGES
- # Archived: SYNC_Graph.md
- ## RECENT CHANGES

**Doc refs:**
- `docs/physics/graph/SYNC_Graph.md`

**Sections:**
- # THE BLOOD LEDGER — Validation Specification
- # Version: 1.0
- # =============================================================================
- # PURPOSE
- # =============================================================================
- # =============================================================================
- # CHAIN
- # =============================================================================
- ## CHAIN
- # =============================================================================
- # INVARIANTS
- # =============================================================================
- ## INVARIANTS
- # =============================================================================
- # PROPERTIES
- # =============================================================================
- ## PROPERTIES
- # =============================================================================
- # ERROR CONDITIONS
- # =============================================================================
- ## ERROR CONDITIONS
- # =============================================================================
- # TEST COVERAGE
- # =============================================================================
- ## TEST COVERAGE
- # =============================================================================
- # VERIFICATION PROCEDURE
- # =============================================================================
- ## VERIFICATION PROCEDURE
- # =============================================================================
- # SYNC STATUS
- # =============================================================================
- ## SYNC STATUS
- # =============================================================================
- # GRAPH INTEGRITY RULES
- # =============================================================================
- # No links — char_wulfric would be orphaned
- # result.persisted = ["char_aldric", "narr_oath", "link_belief_1"]
- # result.rejected = [
- # {"item": "char_wulfric", "error": "orphaned_node", "fix": "Add link..."}
- # ]
- # =============================================================================
- # VISION MAPPING
- # =============================================================================
- # --- COVERED BY ENERGY SYSTEM ---
- # --- REQUIRES NARRATOR/CONTENT ---
- # =============================================================================
- # EXPECTED BEHAVIORS
- # =============================================================================
- # ---------------------------------------------------------------------------
- # PRESENCE & PROXIMITY
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # LIVING WORLD
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # NARRATIVE TENSION
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # COMPANION DEPTH
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # SYSTEM HEALTH
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # TIME & PRESSURE
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # ENGAGEMENT
- # ---------------------------------------------------------------------------
- # =============================================================================
- # ANTI-PATTERNS
- # =============================================================================
- # =============================================================================
- # TEST SUITE
- # =============================================================================
- # ---------------------------------------------------------------------------
- # PRESENCE & PROXIMITY
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # LIVING WORLD
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # NARRATIVE TENSION
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # COMPANION DEPTH
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # SYSTEM HEALTH
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # TIME & PRESSURE
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # ENGAGEMENT
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # CRITICALITY
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # CASCADE
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # ANTI-PATTERNS
- # ---------------------------------------------------------------------------
- # =============================================================================
- # SUMMARY
- # =============================================================================
- ## MARKERS

**Sections:**
- # MECHANISMS — Attention Energy Split (v0)
- ## CHAIN
- ## PURPOSE
- ## INPUTS (REQUIRED)
- ## STEP 1 — Build Player Neighborhood
- ## STEP 2 — Enumerate Eligible Sinks
- ## STEP 3 — Compute Sink Mass (Node↔Link Jointure)
- ## STEP 4 — Allocate Attention
- ## STEP 5 — Update Moment Energies (and only moment energies)
- ## OUTPUTS
- ## INTERRUPT COUPLING (uses separate pattern)
- ## FAILURE MODES
- ## VALIDATION HOOKS

**Sections:**
- # MECHANISMS — Contradiction Pressure (v0)
- ## CHAIN
- ## PURPOSE
- ## INPUTS
- ## EDGE PRESSURE
- ## EFFECT (INDIRECT ONLY)
- ## BEHAVIORAL EXPECTATIONS
- ## FAILURE MODES
- ## VALIDATION HOOKS

**Sections:**
- # MECHANISMS — PRIMES Lag + Half-Life (v0)
- ## CHAIN
- ## PURPOSE
- ## PRIMES LINK FIELDS (REQUIRED)
- ## INPUTS
- ## PRIME EFFECT FUNCTION
- ## HOW PRIMES IS USED (v0)
- ## FAILURE MODES
- ## VALIDATION HOOKS

**Doc refs:**
- `algorithms/ALGORITHM_Physics_Energy_Flow_Sources_Sinks_And_Moment_Dynamics.md`
- `algorithms/ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md`
- `algorithms/ALGORITHM_Physics_Handler_And_Input_Processing_Flows.md`
- `algorithms/ALGORITHM_Physics_Mechanisms.md`
- `algorithms/ALGORITHM_Physics_Speed_Control_And_Display_Filtering.md`
- `algorithms/ALGORITHM_Physics_Tick_Cycle_Gating_Flips_And_Dispatch.md`

**Sections:**
- # Physics — Algorithm: System Overview
- ## CHAIN
- ## Consolidation Note
- ## OVERVIEW
- ## DETAILED ALGORITHMS
- ## LEGACY ALGORITHM REDIRECTS
- ## DATA STRUCTURES
- ## ALGORITHM: Physics Tick Cycle
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Code refs:**
- `engine/api/app.py`

**Sections:**
- # Physics — API Reference
- ## CHAIN
- ## Endpoints
- ## Removed Endpoints
- ## Frontend Types
- ## SSE Callbacks
- ## Narrator Output Format
- ## Graph Operations
- # Creation
- # Links
- # Status changes
- # Queries
- # Lifecycle

**Sections:**
- # Physics — Behaviors: What Should Happen
- ## CHAIN
- ## SUMMARY
- ## LINKS
- ## NOTABLE CHANGES SINCE PREVIOUS VERSION

**Code refs:**
- `engine/physics/cluster_energy_monitor.py`
- `engine/physics/display_snap_transition_checker.py`
- `engine/physics/tick.py`

**Sections:**
- # Physics — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: energy_momentum
- ## TRACE SCENARIOS (VERIFICATION)
- ## CHECK: Snap Display Sequence
- ## CHECK: Cluster Energy Monitor
- ## HOW TO RUN
- # Run physics tests (unit and integration)
- ## NEW HEALTH CHECKS

**Code refs:**
- `engine/infrastructure/api/moments.py`
- `engine/infrastructure/orchestration/orchestrator.py`
- `engine/moment_graph/queries.py`
- `engine/physics/constants.py`
- `engine/physics/graph/graph_ops.py`
- `engine/physics/graph/graph_ops_read_only_interface.py`
- `engine/physics/graph/graph_queries.py`
- `engine/physics/tick.py`
- `graph_ops.py`
- `graph_ops_events.py`
- `graph_ops_read_only_interface.py`
- `graph_queries.py`
- `moment_graph/traversal.py`

**Doc refs:**
- `docs/physics/PATTERNS_Physics.md`
- `docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md`

**Sections:**
- # Physics — Implementation: Code Architecture & Runtime
- ## CHAIN
- ## SUMMARY
- ## CODE STRUCTURE & RESPONSIBILITIES
- ## DESIGN & RUNTIME PATTERNS
- ## STATE MANAGEMENT
- ## TICK METABOLISM (FLOWS)
- ## CONCURRENCY, CONFIG & DEPENDENCIES
- ## OBSERVABILITY & LINKS
- ## GAPS / PROPOSITIONS

**Sections:**
- # OBJECTIFS — Physics
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Doc refs:**
- `docs/schema/SCHEMA_Moments.md`

**Sections:**
- # Physics — Patterns: Why This Shape
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## Core Principle
- ## P1: Potential vs Actual
- ## P2: The Graph Is Alive
- ## P3: Everything Is Moments
- ## P4: Moments Are Specific, Narratives Emerge
- ## P5: Energy Must Land
- ## P6: Sequential Actions, Parallel Potentials
- ## P7: The World Moves Without You
- ## P8: Time Is Elastic
- ## P9: Physics Is The Scheduler
- ## P10: Simultaneous Actions Are Drama
- ## What This Pattern Does NOT Solve
- ## The Philosophy
- ## MARKERS

**Doc refs:**
- `docs/physics/IMPLEMENTATION_Physics.md`
- `docs/physics/archive/SYNC_Physics_archive_2025-12.md`
- `docs/physics/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Physics — Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## ARCHIVE REFERENCES
- ## HANDOFF NOTES

**Sections:**
- # Physics — Validation: How To Verify
- ## CHAIN
- ## SUMMARY
- ## FRAMEWORK

**Doc refs:**
- `templates/CLAUDE_ADDITION.md`
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`
- `templates/ngram/agents/manager/CLAUDE.md`

**Sections:**
- # ngram Framework — Algorithm: Overview
- ## CHAIN
- ## OVERVIEW
- ## CONTENTS
- ## ALGORITHM: Install Protocol in Project
- ## ALGORITHM: Agent Starts Task
- ## ALGORITHM: Create New Module
- ## ALGORITHM: Modify Existing Module
- ## ALGORITHM: Document Cross-Cutting Concept
- ## NOTES

**Doc refs:**
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`

**Sections:**
- # ngram Framework — Implementation: Overview
- ## CHAIN
- ## OVERVIEW
- ## FILE STRUCTURE
- ## SCHEMAS AND CONFIG
- ## FLOWS AND LINKS
- # DOCS: docs/{area}/{module}/PATTERNS_*.md

**Sections:**
- # Archived: Protocol SYNC Notes (2024-12)
- ## SUMMARY OF 2024-12 CHANGES
- ## ARCHIVED NOTES

**Sections:**
- # ALGORITHM: Project Health Doctor
- ## MAIN FLOW
- ## 1. LOAD CONFIGURATION
- ## 2. DISCOVER PROJECT STRUCTURE
- # Also find subdirectories
- ## 3. RUN CHECKS
- # Check if mapped in modules.yaml
- # Check for template placeholders
- # Look for DOCS: comment
- # Find most recent SYNC update across all SYNC files
- # 1. Folders must be snake_case
- # 2. Code files must be snake_case.py and not contain 'and'
- # 3. Doc files must be PREFIX_PascalCase_With_Underscores.md
- # Group into tasks of 10
- # Skip if no docs at all (that's UNDOCUMENTED, not ABANDONED)
- # Check if only has PATTERNS or SYNC (started but not continued)
- # Started (has 1-2 docs) but incomplete (missing 3+ docs)
- # Check if stale
- # Check directories
- # Check files
- ## 4. AGGREGATE RESULTS
- # Apply severity overrides
- # Group by severity
- ## 5. CALCULATE SCORE
- ## 6. GENERATE OUTPUT
- ## 7. EXIT CODE
- ## CHAIN

**Sections:**
- # BEHAVIORS: Project Health Doctor
- ## COMMAND INTERFACE
- # Basic health check
- # With specific directory
- # Output formats
- # Filter by severity
- # Specific checks
- ## HEALTH CHECKS
- ## SPECIAL MARKERS
- ## OUTPUT BEHAVIOR
- ## Critical (2 issues)
- ## Warnings (3 issues)
- ## Info (3 issues)
- ## Suggested Actions
- ## GUIDED REMEDIATION
- ## Current State
- ## Recommended Steps
- # DOCS: docs/api/PATTERNS_Api_Design.md
- ## Template Commands
- # Generate PATTERNS from template
- ## Reference
- ## EXIT CODES
- ## CONFIGURATION
- # Thresholds
- # Ignore patterns
- # Disable specific checks
- # Custom severity overrides
- ## FALSE POSITIVE SUPPRESSION
- ## DOC TEMPLATE DRIFT DEFERMENTS
- ## NON-STANDARD DOC TYPE DEFERMENTS
- ## RESOLVED ESCALATION MARKERS
- ## MARKER STANDARDIZATION
- ## CHAIN

**Code refs:**
- `doctor_checks.py`
- `doctor_report.py`
- `ngram/doctor.py`

**Doc refs:**
- `docs/tui/HEALTH_TUI_Coverage.md`

**Sections:**
- # Project Health Doctor — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: Score Sanity
- ## HOW TO RUN
- # Run all doctor checks on the current project
- # Run with JSON output for machine parsing
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `ngram/doctor.py`
- `ngram/doctor_checks.py`
- `ngram/doctor_checks_content.py`
- `ngram/doctor_checks_core.py`
- `ngram/doctor_checks_docs.py`
- `ngram/doctor_checks_metadata.py`
- `ngram/doctor_checks_naming.py`
- `ngram/doctor_checks_prompt_integrity.py`
- `ngram/doctor_checks_quality.py`
- `ngram/doctor_checks_reference.py`
- `ngram/doctor_checks_stub.py`
- `ngram/doctor_checks_sync.py`
- `ngram/doctor_files.py`

**Doc refs:**
- `..ngram/state/SYNC_Project_Health.md`

**Sections:**
- # Project Health Doctor — Implementation: Code architecture and docking
- ## CHAIN
- ## CODE STRUCTURE
- ## DATA FLOW
- ## DOC-LINK COMPLIANCE
- ## LOCATIONS
- ## GAPS / IDEAS

**Sections:**
- # PATTERNS: Project Health Doctor
- ## THE PROBLEM
- ## THE INSIGHT
- ## DESIGN DECISIONS
- ## WHAT WE CHECK
- ## WHAT WE DON'T CHECK
- ## ALTERNATIVES CONSIDERED
- ## CHAIN

**Code refs:**
- `doctor.py`
- `ngram/doctor.py`
- `ngram/doctor_checks.py`
- `ngram/solve_escalations.py`

**Doc refs:**
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`
- `docs/cli/prompt/SYNC_Prompt_Command_State.md`
- `docs/protocol/doctor/IMPLEMENTATION_Project_Health_Doctor.md`
- `docs/protocol/doctor/SYNC_Project_Health_Doctor.md`

**Sections:**
- # SYNC: Project Health Doctor
- ## MATURITY
- ## CURRENT STATE
- ## IMPLEMENTATION ORDER
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## GAPS
- ## CHAIN

**Sections:**
- # VALIDATION: Project Health Doctor
- ## INVARIANTS
- ## CHECK CORRECTNESS
- ## OUTPUT FORMAT CORRECTNESS
- ## EDGE CASES
- ## PERFORMANCE BOUNDS
- ## VERIFICATION COMMANDS
- # Verify determinism
- # Verify exit codes
- # Verify JSON validity
- # Verify ignore patterns
- ## CHAIN

**Sections:**
- # Agent Trace Logging — Behaviors: Observable Effects
- ## CHAIN
- ## COMMANDS
- ## AUTOMATIC TRACING
- ## TRACE FILE FORMAT
- ## INTEGRATION POINTS
- ## Usage (auto-generated)
- ## WHAT GETS TRACED
- ## WHAT DOESN'T GET TRACED

**Sections:**
- # Agent Trace Logging — Patterns: Why This Design
- ## CHAIN
- ## THE PROBLEM
- ## THE INSIGHT
- ## DESIGN DECISIONS
- ## WHAT THIS ENABLES
- ## TRADEOFFS
- ## ALTERNATIVES CONSIDERED
- ## OPEN QUESTIONS

**Code refs:**
- `ngram/cli.py`

**Sections:**
- # Agent Trace Logging — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IMPLEMENTATION PLAN
- ## HANDOFF: FOR AGENTS
- ## TODO
- ## OPEN QUESTIONS

**Sections:**
- # ngram Framework — Algorithm: Overview
- ## CHAIN
- ## ENTRY POINT

**Sections:**
- # ngram Framework — Behaviors: Observable Protocol Effects
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Code refs:**
- `ngram/prompt.py`
- `ngram/validate.py`

**Doc refs:**
- `docs/cli/HEALTH_CLI_Coverage.md`

**Sections:**
- # ngram Framework — Health: Protocol Verification and Mechanics
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: Chain Completeness
- ## HOW TO RUN
- # Verify protocol health for the current project
- # Verify a specific module
- ## KNOWN GAPS
- ## MARKERS

**Doc refs:**
- `docs/protocol/ALGORITHM/ALGORITHM_Protocol_Process_Flow.md`

**Sections:**
- # ngram Framework — Implementation: Overview
- ## CHAIN
- ## ENTRY POINT

**Sections:**
- # OBJECTIFS — Protocol
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # ngram Framework — Patterns: Bidirectional Documentation Chain for AI Agent Workflows
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- # Descriptive names
- # Not
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## MARKERS

**Code refs:**
- `ngram/cli.py`

**Doc refs:**
- `archive/SYNC_archive_2024-12.md`
- `docs/protocol/BEHAVIORS_Observable_Protocol_Effects.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_File_Structure.md`
- `docs/protocol/PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md`
- `docs/protocol/SYNC_Protocol_Current_State.md`
- `templates/CLAUDE_ADDITION.md`
- `templates/ngram/PRINCIPLES.md`
- `templates/ngram/PROTOCOL.md`

**Sections:**
- # ngram Framework — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## STRUCTURE
- ## POINTERS
- ## ARCHIVE
- ## Agent Observations
- ## GAPS

**Code refs:**
- `scripts/check_chain_links.py`
- `scripts/check_doc_completeness.py`
- `scripts/check_doc_refs.py`
- `scripts/check_orphans.py`

**Sections:**
- # ngram Framework — Validation: Protocol Invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Check all invariants
- # Check specific invariant
- # Check specific module
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # Schema Links
- ## Common Metrics
- ## NARRATIVE -> NARRATIVE
- ## CHARACTER -> PLACE (Presence)
- ## CHARACTER -> THING (Possession)
- ## THING -> PLACE (Location)
- ## PLACE -> PLACE (Containment)
- ## PLACE -> PLACE (Route)

**Sections:**
- # Schema Nodes
- ## Common Metrics
- ## CHARACTER
- ## PLACE
- ## THING
- ## NARRATIVE

**Doc refs:**
- `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Overview.md`

**Sections:**
- # Schema Overview
- ## CHAIN
- ## Scope
- ## Core Principles (Concise)

**Sections:**
- # Schema Tensions
- # Gradual
- # Scheduled
- # Hybrid

**Sections:**
- # Moment Links
- ## CHARACTER -> MOMENT (SAID)
- ## MOMENT -> PLACE (AT)
- ## MOMENT -> MOMENT (THEN)
- ## MOMENT -> TARGET (ATTACHED_TO)
- ## MOMENT -> MOMENT (CAN_LEAD_TO)
- ## MOMENT -> TARGET (REFERENCES)
- ## MOMENT -> TARGET (TARGETS)
- ## MOMENT -> TARGET (ANSWERED_BY)
- ## MOMENT -> CHARACTER (THREATENS)

**Sections:**
- # Moment Node Schema

**Code refs:**
- `engine/db/graph_ops.py`

**Doc refs:**
- `docs/schema/SCHEMA/SCHEMA_Links.md`
- `docs/schema/SCHEMA/SCHEMA_Nodes.md`

**Sections:**
- # Moments Schema Overview
- ## CHAIN
- ## Scope

**Code refs:**
- `check_health.py`
- `engine/graph/health/check_health.py`
- `test_schema.py`

**Sections:**
- # Graph Health — Patterns: Schema-Driven Validation And Query Artifacts
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## WHAT THIS DOES NOT SOLVE
- ## MARKERS

**Code refs:**
- `check_health.py`
- `engine/graph/health/check_health.py`
- `engine/graph/health/lint_terminology.py`
- `engine/graph/health/test_schema.py`
- `test_schema.py`

**Sections:**
- # Graph Health — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## Agent Observations
- ## ARCHIVE

**Code refs:**
- `engine/graph/health/check_health.py`

**Sections:**
- # Archived: SYNC_Graph_Health.md
- ## RECENT CHANGES

**Sections:**
- # Schema — Behaviors: Link Axes Semantics
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Doc refs:**
- `docs/engine/moments/PATTERNS_Moments.md`
- `docs/physics/PATTERNS_Physics.md`
- `docs/schema/SCHEMA/SCHEMA_Links.md`

**Sections:**
- # Schema — Patterns: Link Axes, Not Link Types
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Sections:**
- # Schema — Link Axes: Nodes, Links, and Examples
- ## CHAIN
- ## OVERVIEW
- ## NODE TYPES (V0)
- ## UNIVERSAL FIELDS (ALL NODES)
- ## LINK TYPES (V0)
- ## UNIVERSAL FIELDS (ALL LINKS)
- ## LINK AXES (REQUIRED FOR RELATES/PRIMES)
- ## INSTANCES (10) WITH NODE ATTRIBUTES
- ## LINK MATRIX (EXPLICIT LINKS)
- ## ATTRIBUTE CATALOG (RICH)
- ## RULES
- ## OBSERVABLE BEHAVIORS (TARGET)

**Sections:**
- # Link Axes — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Sections:**
- # Schema — Validation: Link Axes Invariants
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## MARKERS

**Doc refs:**
- `docs/engine/models/PATTERNS_Models.md`

**Sections:**
- # Schema Models — Patterns: Redirect to Canonical Data Model Patterns
- ## WHAT CHANGED
- ## TRANSITION NOTES
- ## CHAIN

**Doc refs:**
- `docs/engine/models/BEHAVIORS_Models.md`
- `docs/engine/models/IMPLEMENTATION_Models.md`
- `docs/engine/models/PATTERNS_Models.md`
- `docs/engine/models/SYNC_Models.md`

**Sections:**
- # Schema Models — Sync: Redirect
- ## WHAT CHANGED
- ## TRANSITION NOTES
- ## CHAIN

**Code refs:**
- `engine/models/__init__.py`
- `engine/models/base.py`
- `engine/models/links.py`
- `engine/models/nodes.py`
- `engine/tests/test_models.py`

**Doc refs:**
- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`
- `docs/schema/models/SYNC_Schema_Models.md`

**Sections:**
- # Archived: SYNC_Schema_Models.md
- ## RECENT CHANGES
- ## Agent Observations
- # Archived: SYNC_Schema_Models.md
- ## RECENT CHANGES
- ## Agent Observations

**Sections:**
- # Schema — Algorithm: Documentation Routing
- ## CHAIN
- ## FLOW

**Sections:**
- # Schema — Behaviors: Observable Schema Effects
- ## CHAIN
- ## BEHAVIORS

**Sections:**
- # Schema — Health: Verification Checklist
- ## CHAIN
- ## CHECKS

**Sections:**
- # Schema — Implementation: Documentation Structure
- ## CHAIN
- ## STRUCTURE

**Sections:**
- # OBJECTIFS — Schema
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # Schema — Patterns: Module Overview and Ownership
- ## CHAIN
- ## PURPOSE

**Sections:**
- # SCHEMA: Code Graph
- ## CORE INSIGHT
- ## DESIGN PATTERNS
- ## THE EVOLUTION: DOCTOR TO PHYSICS
- # Physics Properties
- ## MECHANICS
- ## SCHEMA EVOLUTION

**Doc refs:**
- `docs/schema/SCHEMA.md`

**Sections:**
- # Schema — Sync: Current State
- ## CURRENT STATE
- ## RECENT CHANGES

**Code refs:**
- `engine/graph/health/test_schema.py`
- `engine/tests/test_spec_consistency.py`

**Sections:**
- # Graph Validation
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # Tools — Algorithm: Script Flow
- ## CHAIN
- ## OVERVIEW
- ## OBJECTIVES AND BEHAVIORS
- ## DATA STRUCTURES
- ## ALGORITHM: stream_dialogue.main
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS
- ## FLOWS

**Sections:**
- # Tools — Behaviors: Utility Outcomes
- ## CHAIN
- ## BEHAVIORS
- ## OBJECTIVES SERVED
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Doc refs:**
- `docs/tools/HEALTH_Tools.md`
- `docs/tools/OBJECTIFS_Tools_Goals.md`

**Sections:**
- # Tools — Health: Verification
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## HOW TO USE THIS TEMPLATE
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## OBJECTIVES COVERAGE
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: tool_doc_completeness
- ## INDICATOR: tool_execution_consistency
- ## HEALTH CHECKS
- ## HOW TO RUN
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `connectome_doc_bundle_splitter_and_fence_rewriter.py`
- `stream_dialogue.py`
- `tools/connectome_doc_bundle_splitter_and_fence_rewriter.py`
- `tools/stream_dialogue.py`

**Sections:**
- # Tools — Implementation: Code Mapping
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## CODE LOCATIONS
- ## MARKERS
- ## CODE LOCATIONS

**Sections:**
- # OBJECTIFS — Tools
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `stream_dialogue.py`
- `tools/connectome_doc_bundle_splitter_and_fence_rewriter.py`
- `tools/stream_dialogue.py`

**Sections:**
- # Tools — Patterns: Utility Scripts
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `tools/connectome_doc_bundle_splitter_and_fence_rewriter.py`
- `tools/stream_dialogue.py`

**Doc refs:**
- `docs/engine/membrane/PATTERN_Membrane_Modulation.md`
- `docs/tools/ALGORITHM_Tools.md`
- `docs/tools/BEHAVIORS_Tools.md`
- `docs/tools/HEALTH_Tools.md`
- `docs/tools/IMPLEMENTATION_Tools.md`
- `docs/tools/PATTERNS_Tools.md`
- `docs/tools/SYNC_Tools.md`
- `docs/tools/VALIDATION_Tools.md`

**Sections:**
- # Tools — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## RECENT CHANGES
- ## Agent Observations
- ## TODO
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## POINTERS
- ## CONSCIOUSNESS TRACE

**Code refs:**
- `tools/stream_dialogue.py`

**Doc refs:**
- `tools/HEALTH_Tools.md`

**Sections:**
- # Tools — Validation: Invariants
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # None of these scripts currently ship automated tests; run them manually when making doc changes.
- ## SYNC STATUS
- ## MARKERS

**Code refs:**
- `ngram/cli.py`
- `ngram/doctor.py`
- `ngram/repair_core.py`
- `ngram/tui/__init__.py`
- `ngram/tui/app.py`
- `ngram/tui/app_core.py`
- `ngram/tui/app_manager.py`
- `ngram/tui/commands.py`
- `ngram/tui/commands_agent.py`
- `ngram/tui/manager.py`
- `ngram/tui/state.py`
- `ngram/tui/widgets/agent_container.py`
- `ngram/tui/widgets/agent_panel.py`
- `ngram/tui/widgets/input_bar.py`
- `ngram/tui/widgets/manager_panel.py`
- `ngram/tui/widgets/status_bar.py`
- `ngram/tui/widgets/suggestions.py`

**Doc refs:**
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`
- `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md`

**Sections:**
- # ngram TUI — Implementation Details: Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## BOUNDARIES
- ## SCHEMA
- ## MODULE DEPENDENCIES
- ## CONFIGURATION
- ## DATA FLOW
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## BIDIRECTIONAL LINKS

**Code refs:**
- `ngram/cli.py`
- `ngram/repair_core.py`
- `ngram/tui/app.py`
- `ngram/tui/commands.py`
- `ngram/tui/state.py`

**Sections:**
- # Archive: TUI Implementation Details (2024-12)
- ## Design Patterns (Historical Detail)
- ## Runtime Behavior (Historical Detail)
- ## Concurrency Model (Historical Detail)
- ## Configuration (Historical Detail)
- ## Bidirectional Links (Historical Detail)
- ## Remaining Work (Historical Detail)
- ## Decisions Made (Historical Detail)

**Code refs:**
- `app.py`
- `commands.py`
- `repair.py`
- `repair_core.py`
- `state.py`

**Sections:**
- # Archived: SYNC_TUI_State.md
- ## DESIGN DECISIONS
- ## FILE STRUCTURE (Planned)
- ## HISTORICAL SNAPSHOT (2024-12 CONDENSED)
- ## CHAIN

**Code refs:**
- `doctor.py`
- `repair_core.py`

**Sections:**
- # ngram TUI — Algorithm: Application Flow and Event Handling
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: Main Event Loop
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Code refs:**
- `ngram/tui/commands.py`

**Sections:**
- # ngram TUI — Behaviors: User Interactions and Observable Effects
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## IMPLEMENTATION REFERENCES
- ## MARKERS

**Code refs:**
- `manager.py`

**Doc refs:**
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`

**Sections:**
- # ngram TUI — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: Input Responsiveness
- ## HOW TO RUN
- # Manual verification of slash commands
- # Type /help, /doctor, /repair in the TUI input bar.
- # Manual verification of agent panels
- # Run /repair and verify that agent panels appear and stream output.
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `ngram/cli.py`
- `ngram/repair_core.py`
- `ngram/tui/__init__.py`
- `ngram/tui/app.py`
- `ngram/tui/app_core.py`
- `ngram/tui/app_manager.py`
- `ngram/tui/commands.py`
- `ngram/tui/commands_agent.py`
- `ngram/tui/manager.py`
- `ngram/tui/state.py`
- `ngram/tui/widgets/__init__.py`
- `ngram/tui/widgets/agent_container.py`
- `ngram/tui/widgets/agent_panel.py`
- `ngram/tui/widgets/manager_panel.py`
- `ngram/tui/widgets/status_bar.py`
- `ngram/tui/widgets/suggestions.py`

**Doc refs:**
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md`

**Sections:**
- # ngram TUI — Implementation: Code Architecture (Overview)
- ## CHAIN
- ## SUMMARY
- ## QUICK STRUCTURE (Top-Level)
- ## COMPONENT REFERENCES
- ## ENTRY POINTS
- ## WHAT TO READ NEXT
- ## REMAINING WORK
- ## DECISIONS MADE

**Code refs:**
- `app.py`
- `app_core.py`
- `app_manager.py`
- `commands.py`
- `commands_agent.py`
- `state.py`

**Sections:**
- # OBJECTIFS: Text User Interface (TUI) Module
- ## Objective
- ## Scope
- ## Non-Objectives
- ## CHAIN

**Sections:**
- # OBJECTIFS — Tui
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `commands.py`
- `commands_agent.py`
- `ngram/tui/app.py`
- `ngram/tui/app_core.py`
- `ngram/tui/app_manager.py`
- `ngram/tui/commands.py`
- `ngram/tui/commands_agent.py`
- `ngram/tui/manager.py`
- `ngram/tui/state.py`
- `state.py`

**Sections:**
- # PATTERNS: Text User Interface (TUI) Module
- ## Core Technologies
- ## Architectural Patterns
- ## Styling Conventions
- ## File Structure
- ## CHAIN

**Code refs:**
- `ngram/cli.py`
- `ngram/tui/__init__.py`
- `ngram/tui/app.py`
- `ngram/tui/app_core.py`
- `ngram/tui/manager.py`
- `repair_core.py`

**Sections:**
- # ngram TUI — Patterns: Agent CLI-Style Interface
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## IMPLEMENTATION REFERENCES
- ## MARKERS

**Code refs:**
- `ngram/repair_core.py`
- `ngram/tui/app.py`
- `ngram/tui/app_core.py`
- `ngram/tui/app_manager.py`
- `ngram/tui/commands.py`
- `ngram/tui/state.py`
- `ngram/tui/widgets/status_bar.py`

**Doc refs:**
- `archive/SYNC_Archive_2024-12.md`
- `archive/SYNC_TUI_State_Archive_2025-12.md`
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md`
- `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md`

**Sections:**
- # ngram TUI — Sync: Current State
- ## CHAIN
- ## CURRENT STATE
- ## IN PROGRESS
- ## PLANNED FEATURES (HIGH LEVEL)
- ## KNOWN GAPS
- ## CONFLICTS
- ## AGENT OBSERVATIONS

**Sections:**
- # ngram TUI — Validation: Invariants and Verification
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Once tests exist:
- # With coverage:
- ## SYNC STATUS
- ## MARKERS

**Code refs:**
- `ngram/repo_overview.py`

**Doc refs:**
- `docs/SYNC_Project_Repository_Map.md`

**Sections:**
- # Project Repository Map - Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## CONSCIOUSNESS TRACE
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## ARCHIVE

**Code refs:**
- `agent_cli.py`
- `app.py`
- `commands.py`
- `context.py`
- `doctor.py`
- `doctor_checks.py`
- `doctor_files.py`
- `doctor_report.py`
- `file_utils.py`
- `gemini_agent.py`
- `github.py`
- `init_cmd.py`
- `manager.py`
- `ngram.py`
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/doctor.py`
- `ngram/doctor_checks.py`
- `ngram/doctor_checks_content.py`
- `ngram/doctor_checks_docs.py`
- `ngram/doctor_checks_quality.py`
- `ngram/doctor_checks_sync.py`
- `ngram/doctor_files.py`
- `ngram/doctor_report.py`
- `ngram/doctor_types.py`
- `ngram/github.py`
- `ngram/init_cmd.py`
- `ngram/llms/gemini_agent.py`
- `ngram/project_map.py`
- `ngram/project_map_html.py`
- `ngram/prompt.py`
- `ngram/repair.py`
- `ngram/repair_core.py`
- `ngram/repair_escalation_interactive.py`
- `ngram/repair_instructions.py`
- `ngram/repair_instructions_docs.py`
- `ngram/repair_report.py`
- `ngram/repo_overview.py`
- `ngram/repo_overview_formatters.py`
- `ngram/solve_escalations.py`
- `ngram/sync.py`
- `ngram/tui/app.py`
- `ngram/tui/commands.py`
- `ngram/tui/commands_agent.py`
- `ngram/tui/manager.py`
- `ngram/tui/state.py`
- `ngram/tui/widgets/agent_container.py`
- `ngram/tui/widgets/agent_panel.py`
- `ngram/tui/widgets/input_bar.py`
- `ngram/tui/widgets/manager_panel.py`
- `ngram/tui/widgets/status_bar.py`
- `ngram/tui/widgets/suggestions.py`
- `ngram/utils.py`
- `ngram/utils/file_utils.py`
- `ngram/utils/string_utils.py`
- `ngram/utils/validation_utils.py`
- `ngram/validate.py`
- `project_map.py`
- `project_map_html.py`
- `prompt.py`
- `repair.py`
- `repair_core.py`
- `repo_overview.py`
- `scripts/check_chain_links.py`
- `scripts/check_doc_completeness.py`
- `scripts/check_doc_refs.py`
- `scripts/check_orphans.py`
- `src/analytics/batch_ingest.py`
- `src/analytics/storage/event_store.py`
- `src/analytics/stream_ingest.py`
- `src/analytics/validation/schema_rules.py`
- `src/dashboard/op_metrics.py`
- `src/dashboard/product_metrics.py`
- `state.py`
- `string_utils.py`
- `sync.py`
- `utils.py`
- `validate.py`

**Doc refs:**
- `archive/SYNC_archive_2024-12.md`
- `docs/SYNC_Project_Repository_Map.md`
- `docs/cli/ALGORITHM_CLI_Logic.md`
- `docs/cli/HEALTH_CLI_Coverage.md`
- `docs/cli/SYNC_CLI_State.md`
- `docs/cli/VALIDATION_CLI_Invariants.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture.md`
- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`
- `docs/llm_agents/ALGORITHM_Gemini_Stream_Flow.md`
- `docs/llm_agents/BEHAVIORS_Gemini_Agent_Output.md`
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md`
- `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`
- `docs/llm_agents/SYNC_LLM_Agents_State.md`
- `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_File_Structure.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_Overview.md`
- `docs/tui/BEHAVIORS_TUI_Interactions.md`
- `docs/tui/HEALTH_TUI_Coverage.md`
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md`
- `docs/tui/PATTERNS_TUI_Design.md`
- `docs/tui/SYNC_TUI_State.md`
- `docs/tui/archive/SYNC_archive_2024-12.md`
- `templates/CLAUDE_ADDITION.md`
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`
- `templates/ngram/PRINCIPLES.md`
- `templates/ngram/PROTOCOL.md`
- `templates/ngram/agents/manager/CLAUDE.md`
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # Archived: SYNC_Project_Repository_Map.md
- ## TODO
- ## POINTERS
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## CONSCIOUSNESS TRACE
- # Repository Map:

**Code refs:**
- `__init__.py`
- `agent_cli.py`
- `api/connectome/graph/route.ts`
- `api/connectome/graphs/route.ts`
- `api/connectome/search/route.ts`
- `api/sse/route.ts`
- `app.py`
- `app/api/connectome/graph/route.ts`
- `app/api/connectome/graphs/route.ts`
- `app/api/connectome/search/route.ts`
- `app/api/route.ts`
- `app/api/sse/route.ts`
- `app/connectome/components/connectome_health_panel.ts`
- `app/connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts`
- `app/connectome/components/connectome_log_export_buttons_using_state_store_serializers.ts`
- `app/connectome/components/connectome_log_export_buttons_using_state_store_serializers.tsx`
- `app/connectome/components/connectome_log_trigger_and_calltype_badge_color_tokens.ts`
- `app/connectome/components/connectome_page_shell_route_layout_and_control_surface.ts`
- `app/connectome/components/connectome_page_shell_route_layout_and_control_surface.tsx`
- `app/connectome/components/deterministic_zone_and_node_layout_computation_helpers.ts`
- `app/connectome/components/edge_kit/connectome_edge_directional_shine_animation_helpers.ts`
- `app/connectome/components/edge_kit/connectome_edge_label_renderer_with_halo_and_zoom_policy.ts`
- `app/connectome/components/edge_kit/connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx`
- `app/connectome/components/edge_kit/connectome_edge_pulse_particle_animation_and_boundary_clamp_helpers.ts`
- `app/connectome/components/edge_kit/connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts`
- `app/connectome/components/edge_kit/connectome_node_boundary_intersection_geometry_helpers.ts`
- `app/connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.ts`
- `app/connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.tsx`
- `app/connectome/components/edge_label_declutter_and_visibility_policy_helpers.ts`
- `app/connectome/components/node_kit/connectome_energy_badge_bucketed_glow_and_value_formatter.ts`
- `app/connectome/components/node_kit/connectome_energy_badge_bucketed_glow_and_value_formatter.tsx`
- `app/connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts`
- `app/connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.ts`
- `app/connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`
- `app/connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.ts`
- `app/connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.tsx`
- `app/connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.ts`
- `app/connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.tsx`
- `app/connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.ts`
- `app/connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.tsx`
- `app/connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.ts`
- `app/connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.tsx`
- `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.ts`
- `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`
- `app/connectome/components/stepper/node_stepper_control.tsx`
- `app/connectome/components/telemetry_camera_controls.ts`
- `app/connectome/components/unified_now_and_copyable_ledger_log_panel.ts`
- `app/connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`
- `app/connectome/lib/connectome_export_jsonl_and_text_log_serializer.ts`
- `app/connectome/lib/connectome_session_boundary_and_restart_policy_controller.ts`
- `app/connectome/lib/connectome_step_script_sample_sequence.ts`
- `app/connectome/lib/connectome_system_map_node_edge_manifest.ts`
- `app/connectome/lib/connectome_wait_timer_progress_and_tick_display_signal_selectors.ts`
- `app/connectome/lib/flow_event_duration_bucket_color_classifier.ts`
- `app/connectome/lib/flow_event_schema_and_normalization_contract.ts`
- `app/connectome/lib/flow_event_trigger_and_calltype_inference_rules.ts`
- `app/connectome/lib/minimum_duration_clamp_and_speed_based_default_policy.ts`
- `app/connectome/lib/next_step_gate_and_realtime_playback_runtime_engine.ts`
- `app/connectome/lib/step_script_cursor_and_replay_determinism_helpers.ts`
- `app/connectome/lib/zustand_connectome_state_store_with_atomic_commit_actions.ts`
- `app/connectome/page.tsx`
- `app/layout.ts`
- `app/layout.tsx`
- `app/ngram/page.tsx`
- `app/page.ts`
- `app/page.tsx`
- `app_core.py`
- `app_manager.py`
- `base.py`
- `check_health.py`
- `cli.py`
- `commands.py`
- `commands_agent.py`
- `connectome/components/connectome_health_panel.tsx`
- `connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts`
- `connectome/components/connectome_log_export_buttons_using_state_store_serializers.tsx`
- `connectome/components/connectome_log_trigger_and_calltype_badge_color_tokens.ts`
- `connectome/components/connectome_page_shell_route_layout_and_control_surface.tsx`
- `connectome/components/deterministic_zone_and_node_layout_computation_helpers.ts`
- `connectome/components/edge_kit/connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx`
- `connectome/components/edge_kit/connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts`
- `connectome/components/edge_kit/connectome_node_boundary_intersection_geometry_helpers.ts`
- `connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.tsx`
- `connectome/components/edge_label_declutter_and_visibility_policy_helpers.ts`
- `connectome/components/node_kit/connectome_energy_badge_bucketed_glow_and_value_formatter.tsx`
- `connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts`
- `connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`
- `connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.tsx`
- `connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.tsx`
- `connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.tsx`
- `connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.tsx`
- `connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`
- `connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`
- `connectome_doc_bundle_splitter_and_fence_rewriter.py`
- `connectome_edge_directional_shine_animation_helpers.ts`
- `connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx`
- `connectome_edge_pulse_particle_animation_and_boundary_clamp_helpers.ts`
- `connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts`
- `connectome_energy_badge_bucketed_glow_and_value_formatter.ts`
- `connectome_node_background_theme_tokens_by_type_and_language.ts`
- `connectome_node_boundary_intersection_geometry_helpers.ts`
- `connectome_system_map_node_edge_manifest.ts`
- `context.py`
- `core_utils.py`
- `doctor.py`
- `doctor_checks.py`
- `doctor_cli_parser_and_run_checker.py`
- `doctor_files.py`
- `doctor_report.py`
- `engine/api/app.py`
- `engine/db/graph_ops.py`
- `engine/graph/health/check_health.py`
- `engine/graph/health/lint_terminology.py`
- `engine/graph/health/test_schema.py`
- `engine/handlers/base.py`
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/api/graphs.py`
- `engine/infrastructure/api/moments.py`
- `engine/infrastructure/api/playthroughs.py`
- `engine/infrastructure/api/sse_broadcast.py`
- `engine/infrastructure/api/tempo.py`
- `engine/infrastructure/canon/canon_holder.py`
- `engine/infrastructure/embeddings/service.py`
- `engine/infrastructure/memory/__init__.py`
- `engine/infrastructure/memory/moment_processor.py`
- `engine/infrastructure/memory/transcript.py`
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/orchestration/narrator.py`
- `engine/infrastructure/orchestration/orchestrator.py`
- `engine/infrastructure/orchestration/speed.py`
- `engine/infrastructure/orchestration/world_runner.py`
- `engine/infrastructure/tempo/health_check.py`
- `engine/infrastructure/tempo/tempo_controller.py`
- `engine/init_db.py`
- `engine/membrane/functions.py`
- `engine/membrane/health_check.py`
- `engine/membrane/provider.py`
- `engine/models/__init__.py`
- `engine/models/base.py`
- `engine/models/links.py`
- `engine/models/nodes.py`
- `engine/moment_graph/__init__.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/moment_graph/traversal.py`
- `engine/moments/__init__.py`
- `engine/physics/attention_split_sink_mass_distribution_mechanism.py`
- `engine/physics/cluster_energy_monitor.py`
- `engine/physics/constants.py`
- `engine/physics/contradiction_pressure_from_negative_polarity_mechanism.py`
- `engine/physics/display_snap_transition_checker.py`
- `engine/physics/graph/connectome_read_cli.py`
- `engine/physics/graph/graph_interface.py`
- `engine/physics/graph/graph_ops.py`
- `engine/physics/graph/graph_ops_events.py`
- `engine/physics/graph/graph_ops_moments.py`
- `engine/physics/graph/graph_ops_read_only_interface.py`
- `engine/physics/graph/graph_ops_types.py`
- `engine/physics/graph/graph_queries.py`
- `engine/physics/graph/graph_queries_moments.py`
- `engine/physics/graph/graph_queries_search.py`
- `engine/physics/graph/graph_query_utils.py`
- `engine/physics/primes_lag_and_half_life_decay_mechanism.py`
- `engine/physics/tick.py`
- `engine/tests/test_cluster_energy_monitor.py`
- `engine/tests/test_e2e_moment_graph.py`
- `engine/tests/test_models.py`
- `engine/tests/test_moment.py`
- `engine/tests/test_moment_graph.py`
- `engine/tests/test_moment_lifecycle.py`
- `engine/tests/test_moments_api.py`
- `engine/tests/test_physics_display_snap.py`
- `engine/tests/test_router_schema_validation.py`
- `engine/tests/test_spec_consistency.py`
- `file_utils.py`
- `flow_event_schema_and_normalization_contract.ts`
- `frontend/app/scenarios/page.tsx`
- `frontend/app/start/page.tsx`
- `frontend/hooks/useGameState.ts`
- `gemini_agent.py`
- `github.py`
- `graph_ops.py`
- `graph_ops_apply.py`
- `graph_ops_events.py`
- `graph_ops_image.py`
- `graph_ops_moments.py`
- `graph_ops_read_only_interface.py`
- `graph_ops_types.py`
- `graph_queries.py`
- `graph_queries_narratives.py`
- `graph_queries_search.py`
- `init_cmd.py`
- `layout.tsx`
- `links.py`
- `lint_terminology.py`
- `manager.py`
- `moment_graph/traversal.py`
- `moment_processor.py`
- `moments.py`
- `narrator.py`
- `narrator/prompt_builder.py`
- `next_step_gate_and_realtime_playback_runtime_engine.ts`
- `ngram.py`
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/core_utils.py`
- `ngram/docs_fix.py`
- `ngram/doctor.py`
- `ngram/doctor_checks.py`
- `ngram/doctor_checks_content.py`
- `ngram/doctor_checks_core.py`
- `ngram/doctor_checks_docs.py`
- `ngram/doctor_checks_metadata.py`
- `ngram/doctor_checks_naming.py`
- `ngram/doctor_checks_prompt_integrity.py`
- `ngram/doctor_checks_quality.py`
- `ngram/doctor_checks_reference.py`
- `ngram/doctor_checks_stub.py`
- `ngram/doctor_checks_sync.py`
- `ngram/doctor_files.py`
- `ngram/doctor_report.py`
- `ngram/doctor_types.py`
- `ngram/github.py`
- `ngram/init_cmd.py`
- `ngram/llms/gemini_agent.py`
- `ngram/llms/tool_helpers.py`
- `ngram/project_map.py`
- `ngram/project_map_html.py`
- `ngram/prompt.py`
- `ngram/refactor.py`
- `ngram/repair.py`
- `ngram/repair_core.py`
- `ngram/repair_escalation_interactive.py`
- `ngram/repair_instructions.py`
- `ngram/repair_instructions_docs.py`
- `ngram/repair_report.py`
- `ngram/repo_overview.py`
- `ngram/repo_overview_formatters.py`
- `ngram/solve_escalations.py`
- `ngram/sync.py`
- `ngram/tui/__init__.py`
- `ngram/tui/app.py`
- `ngram/tui/app_core.py`
- `ngram/tui/app_manager.py`
- `ngram/tui/commands.py`
- `ngram/tui/commands_agent.py`
- `ngram/tui/manager.py`
- `ngram/tui/state.py`
- `ngram/tui/widgets/__init__.py`
- `ngram/tui/widgets/agent_container.py`
- `ngram/tui/widgets/agent_panel.py`
- `ngram/tui/widgets/input_bar.py`
- `ngram/tui/widgets/manager_panel.py`
- `ngram/tui/widgets/status_bar.py`
- `ngram/tui/widgets/suggestions.py`
- `ngram/utils.py`
- `ngram/utils/file_utils.py`
- `ngram/utils/string_utils.py`
- `ngram/utils/validation_utils.py`
- `ngram/validate.py`
- `nodes.py`
- `orchestrator.py`
- `page.tsx`
- `pannable_zoomable_zoned_flow_canvas_renderer.tsx`
- `playthroughs.py`
- `project_map.py`
- `project_map_html.py`
- `prompt.py`
- `repair.py`
- `repair_core.py`
- `repo_overview.py`
- `route.ts`
- `scripts/check_chain_links.py`
- `scripts/check_doc_completeness.py`
- `scripts/check_doc_refs.py`
- `scripts/check_orphans.py`
- `scripts/connectome/health/node_kit_health_check_runner.ts`
- `semantic_edge_components_with_directional_shine_and_pulses.tsx`
- `semantic_proximity_based_character_node_selector.py`
- `snake_case.py`
- `src/analytics/batch_ingest.py`
- `src/analytics/storage/event_store.py`
- `src/analytics/stream_ingest.py`
- `src/analytics/validation/schema_rules.py`
- `src/dashboard/op_metrics.py`
- `src/dashboard/product_metrics.py`
- `sse_broadcast.py`
- `state.py`
- `stream_dialogue.py`
- `string_utils.py`
- `surface.py`
- `sync.py`
- `tensions.py`
- `test_schema.py`
- `tick.py`
- `tools/connectome_doc_bundle_splitter_and_fence_rewriter.py`
- `tools/dialogue/clickables.py`
- `tools/stream_dialogue.py`
- `utils.py`
- `validate.py`
- `views.py`
- `zustand_connectome_state_store_with_atomic_commit_actions.ts`

**Doc refs:**
- `agents/narrator/CLAUDE.md`
- `agents/narrator/CLAUDE_old.md`
- `agents/world_runner/CLAUDE.md`
- `algorithms/ALGORITHM_Physics_Energy_Flow_Sources_Sinks_And_Moment_Dynamics.md`
- `algorithms/ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md`
- `algorithms/ALGORITHM_Physics_Handler_And_Input_Processing_Flows.md`
- `algorithms/ALGORITHM_Physics_Mechanisms.md`
- `algorithms/ALGORITHM_Physics_Speed_Control_And_Display_Filtering.md`
- `algorithms/ALGORITHM_Physics_Tick_Cycle_Gating_Flips_And_Dispatch.md`
- `archive/SYNC_Archive_2024-12.md`
- `archive/SYNC_CLI_Development_State_archive_2025-12.md`
- `archive/SYNC_CLI_State_Archive_2025-12.md`
- `archive/SYNC_TUI_State_Archive_2025-12.md`
- `archive/SYNC_archive_2024-12.md`
- `core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `core/BEHAVIORS_CLI_Command_Effects.md`
- `core/HEALTH_CLI_Command_Test_Coverage.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md`
- `core/PATTERNS_Why_CLI_Over_Copy.md`
- `core/SYNC_CLI_Development_State.md`
- `core/VALIDATION_CLI_Instruction_Invariants.md`
- `data/ARCHITECTURE — Cybernetic Studio.md`
- `data/NGRAM Documentation Chain Pattern (Draft “Marco”).md`
- `docs/SYNC_Project_Repository_Map.md`
- `docs/agents/narrator/ALGORITHM_Scene_Generation.md`
- `docs/agents/narrator/BEHAVIORS_Narrator.md`
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md`
- `docs/agents/narrator/HEALTH_Narrator.md`
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md`
- `docs/agents/narrator/INPUT_REFERENCE.md`
- `docs/agents/narrator/PATTERNS_Narrator.md`
- `docs/agents/narrator/PATTERNS_World_Building.md`
- `docs/agents/narrator/SYNC_Narrator.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12.md`
- `docs/agents/narrator/TEST_Narrator.md`
- `docs/agents/narrator/TOOL_REFERENCE.md`
- `docs/agents/narrator/VALIDATION_Narrator.md`
- `docs/agents/narrator/archive/SYNC_archive_2024-12.md`
- `docs/architecture/cybernetic_studio_architecture/ALGORITHM_Cybernetic_Studio_Process_Flow.md`
- `docs/architecture/cybernetic_studio_architecture/BEHAVIORS_Cybernetic_Studio_System_Behaviors.md`
- `docs/architecture/cybernetic_studio_architecture/HEALTH_Cybernetic_Studio_Health_Checks.md`
- `docs/architecture/cybernetic_studio_architecture/IMPLEMENTATION_Cybernetic_Studio_Code_Structure.md`
- `docs/architecture/cybernetic_studio_architecture/PATTERNS_Cybernetic_Studio_Architecture.md`
- `docs/architecture/cybernetic_studio_architecture/SYNC_Cybernetic_Studio_Architecture_State.md`
- `docs/architecture/cybernetic_studio_architecture/VALIDATION_Cybernetic_Studio_Architectural_Invariants.md`
- `docs/cli/ALGORITHM_CLI_Command_Execution_Logic.md`
- `docs/cli/ALGORITHM_CLI_Logic.md`
- `docs/cli/HEALTH_CLI_Coverage.md`
- `docs/cli/SYNC_CLI_State.md`
- `docs/cli/VALIDATION_CLI_Invariants.md`
- `docs/cli/archive/SYNC_CLI_Development_State_archive_2025-12.md`
- `docs/cli/archive/SYNC_CLI_State_Archive_2025-12.md`
- `docs/cli/archive/SYNC_archive_2024-12.md`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic.md`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `docs/cli/core/BEHAVIORS_CLI_Command_Effects.md`
- `docs/cli/core/HEALTH_CLI_Command_Test_Coverage.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md`
- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`
- `docs/cli/core/SYNC_CLI_Development_State.md`
- `docs/cli/core/VALIDATION_CLI_Instruction_Invariants.md`
- `docs/cli/prompt/ALGORITHM_Prompt_Bootstrap_Prompt_Construction.md`
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`
- `docs/cli/prompt/PATTERNS_Prompt_Command_Workflow_Design.md`
- `docs/cli/prompt/SYNC_Prompt_Command_State.md`
- `docs/connectome/edge_kit/BEHAVIORS_Connectome_Edge_Kit_Readable_Directional_And_Truthful_Link_Effects.md`
- `docs/connectome/edge_kit/HEALTH_Connectome_Edge_Kit_Runtime_Verification_Of_Link_Visibility_And_Semantic_Styling.md`
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md`
- `docs/connectome/edge_kit/PATTERNS_Connectome_Edge_Kit_Color_Coded_Trigger_Typed_Directional_Link_Styling_Patterns.md`
- `docs/connectome/edge_kit/SYNC_Connectome_Edge_Kit_Sync_Current_State.md`
- `docs/connectome/edge_kit/VALIDATION_Connectome_Edge_Kit_Invariants_For_Color_Dash_And_Pulse_Truth.md`
- `docs/connectome/event_model/ALGORITHM_Connectome_Event_Normalization_And_Rendering_Event_Synthesis.md`
- `docs/connectome/flow_canvas/ALGORITHM_Connectome_Flow_Canvas_Layout_Zones_And_Edge_Label_Decluttering.md`
- `docs/connectome/flow_canvas/BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md`
- `docs/connectome/flow_canvas/HEALTH_Connectome_Flow_Canvas_Runtime_Verification_Of_Render_Stability_And_Perf_Budgets.md`
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md`
- `docs/connectome/flow_canvas/PATTERNS_Connectome_Flow_Canvas_Pannable_Zoomable_Zoned_System_Map_Rendering_Patterns.md`
- `docs/connectome/flow_canvas/SYNC_Connectome_Flow_Canvas_Sync_Current_State.md`
- `docs/connectome/flow_canvas/VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md`
- `docs/connectome/graphs/OBJECTIFS_Connectome_Graphs.md`
- `docs/connectome/graphs/PATTERNS_Connectome_Graphs.md`
- `docs/connectome/graphs/SYNC_Connectome_Graphs_Sync_Current_State.md`
- `docs/connectome/health/HEALTH_Connectome_Live_Signals.md`
- `docs/connectome/log_panel/ALGORITHM_Connectome_Log_Panel_Log_Rendering_Duration_Coloring_And_Export.md`
- `docs/connectome/log_panel/BEHAVIORS_Connectome_Log_Panel_Step_Clarity_And_Copyable_Audit_Trail_Effects.md`
- `docs/connectome/log_panel/HEALTH_Connectome_Log_Panel_Runtime_Verification_Of_Log_Truth_And_Export_Integrity.md`
- `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md`
- `docs/connectome/log_panel/PATTERNS_Connectome_Log_Panel_Unified_Explain_And_Copyable_Event_Ledger_View_Patterns.md`
- `docs/connectome/log_panel/SYNC_Connectome_Log_Panel_Sync_Current_State.md`
- `docs/connectome/log_panel/VALIDATION_Connectome_Log_Panel_Invariants_For_Truthful_Durations_And_Stable_Export.md`
- `docs/connectome/node_kit/ALGORITHM_Connectome_Node_Kit_Node_Rendering_Spec_And_Energy_Glow_Mapping.md`
- `docs/connectome/node_kit/BEHAVIORS_Connectome_Node_Kit_Visible_Clarity_And_Trust_Effects.md`
- `docs/connectome/node_kit/HEALTH_Connectome_Node_Kit_Runtime_Verification_Of_Node_State_And_Visual_Signal_Truth.md`
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`
- `docs/connectome/node_kit/PATTERNS_Connectome_Node_Kit_Typed_Language_Coded_Energy_Aware_Node_Rendering_Patterns.md`
- `docs/connectome/node_kit/SYNC_Connectome_Node_Kit_Sync_Current_State.md`
- `docs/connectome/node_kit/VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md`
- `docs/connectome/page_shell/PATTERNS_Connectome_Page_Shell_Route_Composition_And_User_Control_Surface_Patterns.md`
- `docs/connectome/runtime_engine/ALGORITHM_Connectome_Runtime_Engine_Step_Release_And_Realtime_Scheduling.md`
- `docs/connectome/runtime_engine/BEHAVIORS_Connectome_Runtime_Engine_User_Controlled_Traversal_Effects.md`
- `docs/connectome/runtime_engine/HEALTH_Connectome_Runtime_Engine_Runtime_Verification_Of_Pacing_And_Order.md`
- `docs/connectome/runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md`
- `docs/connectome/runtime_engine/PATTERNS_Connectome_Runtime_Engine_Stepper_And_Realtime_Traversal_Control_Patterns.md`
- `docs/connectome/runtime_engine/SYNC_Connectome_Runtime_Engine_Sync_Current_State.md`
- `docs/connectome/runtime_engine/VALIDATION_Connectome_Runtime_Engine_Invariants_For_Stepper_And_Realtime.md`
- `docs/connectome/state_store/ALGORITHM_Connectome_State_Store_Atomic_Commits_For_Step_Releases_And_Realtime.md`
- `docs/connectome/state_store/BEHAVIORS_Connectome_State_Store_Observable_State_Consistency_Effects.md`
- `docs/connectome/state_store/HEALTH_Connectome_State_Store_Runtime_Verification_Of_Ledger_And_Timer_Correctness.md`
- `docs/connectome/state_store/IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md`
- `docs/connectome/state_store/PATTERNS_Connectome_State_Store_Single_Source_Of_Truth_For_Events_Focus_And_Timers.md`
- `docs/connectome/state_store/SYNC_Connectome_State_Store_Sync_Current_State.md`
- `docs/connectome/state_store/VALIDATION_Connectome_State_Store_Invariants_For_Ledger_Ordering_And_Focus.md`
- `docs/core_utils/ALGORITHM_Core_Utils_Template_Path_And_Module_Discovery.md`
- `docs/core_utils/ALGORITHM_Template_Path_Resolution_And_Doc_Discovery.md`
- `docs/core_utils/PATTERNS_Core_Utils_Functions.md`
- `docs/engine/membrane/BEHAVIORS_Membrane_Modulation.md`
- `docs/engine/membrane/PATTERNS_Membrane_Scoping.md`
- `docs/engine/membrane/PATTERN_Membrane_Modulation.md`
- `docs/engine/membrane/SYNC_Membrane_Modulation.md`
- `docs/engine/models/BEHAVIORS_Models.md`
- `docs/engine/models/HEALTH_Models.md`
- `docs/engine/models/IMPLEMENTATION_Models.md`
- `docs/engine/models/PATTERNS_Models.md`
- `docs/engine/models/SYNC_Models.md`
- `docs/engine/models/VALIDATION_Models.md`
- `docs/engine/moments/PATTERNS_Moments.md`
- `docs/engine/moments/SYNC_Moments.md`
- `docs/frontend/app_shell/OBJECTIFS_App_Shell.md`
- `docs/frontend/app_shell/PATTERNS_App_Shell.md`
- `docs/frontend/app_shell/SYNC_App_Shell_State.md`
- `docs/infrastructure/api/ALGORITHM_Api.md`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md`
- `docs/infrastructure/api/API_Graph_Management.md`
- `docs/infrastructure/api/BEHAVIORS_Api.md`
- `docs/infrastructure/api/IMPLEMENTATION_Api.md`
- `docs/infrastructure/api/PATTERNS_Api.md`
- `docs/infrastructure/api/SYNC_Api.md`
- `docs/infrastructure/api/TEST_Api.md`
- `docs/infrastructure/api/VALIDATION_Api.md`
- `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`
- `docs/infrastructure/canon/PATTERNS_Canon.md`
- `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md`
- `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`
- `docs/infrastructure/tempo/PATTERNS_Tempo.md`
- `docs/llm_agents/ALGORITHM_Gemini_Stream_Flow.md`
- `docs/llm_agents/BEHAVIORS_Gemini_Agent_Output.md`
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md`
- `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`
- `docs/llm_agents/SYNC_LLM_Agents_State.md`
- `docs/llm_agents/SYNC_LLM_Agents_State_archive_2025-12.md`
- `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md`
- `docs/ngram_cli_core/OBJECTIFS_ngram_cli_core.md`
- `docs/ngram_cli_core/PATTERNS_ngram_cli_core.md`
- `docs/ngram_cli_core/SYNC_ngram_cli_core.md`
- `docs/physics/ALGORITHM_Physics.md`
- `docs/physics/BEHAVIORS_Physics.md`
- `docs/physics/IMPLEMENTATION_Physics.md`
- `docs/physics/PATTERNS_Physics.md`
- `docs/physics/SYNC_Physics.md`
- `docs/physics/SYNC_Physics_archive_2025-12.md`
- `docs/physics/TEST_Physics.md`
- `docs/physics/VALIDATION_Physics.md`
- `docs/physics/algorithms/ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md`
- `docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md`
- `docs/physics/archive/IMPLEMENTATION_Physics_archive_2025-12.md`
- `docs/physics/archive/SYNC_Physics_archive_2025-12.md`
- `docs/physics/archive/SYNC_archive_2024-12.md`
- `docs/physics/attention/PATTERNS_Attention_Energy_Split.md`
- `docs/physics/attention/PATTERNS_Interrupt_By_Focus_Reconfiguration.md`
- `docs/physics/attention/VALIDATION_Attention_Split_And_Interrupts.md`
- `docs/physics/graph/ALGORITHM_Energy_Flow.md`
- `docs/physics/graph/ALGORITHM_Weight.md`
- `docs/physics/graph/BEHAVIORS_Graph.md`
- `docs/physics/graph/PATTERNS_Graph.md`
- `docs/physics/graph/SYNC_Graph.md`
- `docs/physics/graph/SYNC_Graph_archive_2025-12.md`
- `docs/physics/graph/VALIDATION_Living_Graph.md`
- `docs/physics/mechanisms/MECHANISMS_Attention_Energy_Split.md`
- `docs/physics/mechanisms/MECHANISMS_Contradiction_Pressure.md`
- `docs/physics/mechanisms/MECHANISMS_Primes_Lag_Decay.md`
- `docs/protocol/ALGORITHM/ALGORITHM_Protocol_Process_Flow.md`
- `docs/protocol/BEHAVIORS_Observable_Protocol_Effects.md`
- `docs/protocol/HEALTH_Protocol_Verification.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_File_Structure.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_Overview.md`
- `docs/protocol/PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md`
- `docs/protocol/SYNC_Protocol_Current_State.md`
- `docs/protocol/archive/SYNC_Archive_2024-12.md`
- `docs/protocol/doctor/IMPLEMENTATION_Project_Health_Doctor.md`
- `docs/protocol/doctor/PATTERNS_Project_Health_Doctor.md`
- `docs/protocol/doctor/SYNC_Project_Health_Doctor.md`
- `docs/schema/SCHEMA.md`
- `docs/schema/SCHEMA/SCHEMA_Links.md`
- `docs/schema/SCHEMA/SCHEMA_Nodes.md`
- `docs/schema/SCHEMA_Moments.md`
- `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Overview.md`
- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`
- `docs/schema/models/SYNC_Schema_Models.md`
- `docs/tools/ALGORITHM_Tools.md`
- `docs/tools/BEHAVIORS_Tools.md`
- `docs/tools/HEALTH_Tools.md`
- `docs/tools/IMPLEMENTATION_Tools.md`
- `docs/tools/OBJECTIFS_Tools_Goals.md`
- `docs/tools/PATTERNS_Tools.md`
- `docs/tools/SYNC_Tools.md`
- `docs/tools/VALIDATION_Tools.md`
- `docs/tui/ALGORITHM_TUI_Widget_Interaction_Flow.md`
- `docs/tui/BEHAVIORS_TUI_Interactions.md`
- `docs/tui/HEALTH_TUI_Coverage.md`
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md`
- `docs/tui/PATTERNS_TUI_Design.md`
- `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md`
- `docs/tui/SYNC_TUI_State.md`
- `docs/tui/archive/SYNC_archive_2024-12.md`
- `doctor/ALGORITHM_Project_Health_Doctor.md`
- `doctor/BEHAVIORS_Project_Health_Doctor.md`
- `doctor/HEALTH_Project_Health_Doctor.md`
- `doctor/PATTERNS_Project_Health_Doctor.md`
- `doctor/SYNC_Project_Health_Doctor.md`
- `doctor/VALIDATION_Project_Health_Doctor.md`
- `event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md`
- `features/BEHAVIORS_Agent_Trace_Logging.md`
- `features/PATTERNS_Agent_Trace_Logging.md`
- `features/SYNC_Agent_Trace_Logging.md`
- `implementation/IMPLEMENTATION_Physics_Architecture.md`
- `implementation/IMPLEMENTATION_Physics_Code_Structure.md`
- `implementation/IMPLEMENTATION_Physics_Dataflow.md`
- `implementation/IMPLEMENTATION_Physics_Runtime.md`
- `..ngram/state/SYNC_Project_Health.md`
- `..ngram/state/SYNC_Prompt_Command_State.md`
- `prompt/ALGORITHM_Prompt_Bootstrap_Prompt_Construction.md`
- `prompt/BEHAVIORS_Prompt_Command_Output_and_Flow.md`
- `prompt/HEALTH_Prompt_Runtime_Verification.md`
- `prompt/IMPLEMENTATION_Prompt_Code_Architecture.md`
- `prompt/PATTERNS_Prompt_Command_Workflow_Design.md`
- `prompt/SYNC_Prompt_Command_State.md`
- `prompt/VALIDATION_Prompt_Bootstrap_Invariants.md`
- `runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md`
- `state/SYNC_Project_State.md`
- `state_store/IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md`
- `templates/CLAUDE_ADDITION.md`
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`
- `templates/ngram/PRINCIPLES.md`
- `templates/ngram/PROTOCOL.md`
- `templates/ngram/agents/manager/CLAUDE.md`
- `tools/HEALTH_Tools.md`
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # Repository Map: ngram

**Code refs:**
- `check_health.py`
- `lint_terminology.py`
- `test_schema.py`

**Sections:**
- # Graph Health & Queries
- ## Files
- ## Query Quality Ratings
- ## Top Queries by Category
- ## Running Health Checks
- # Basic health check
- # Full schema test suite (22 tests)
- # With pytest for CI integration
- # Terminology linter
- ## Schema Tests
- ## Using Queries
- # Run a query

**Docs:** `docs/schema/graph-health/PATTERNS_Graph_Health_Validation.md`

**Definitions:**
- `class Issue`
- `class HealthReport`
- `def add_issue()`
- `def error_count()`
- `def warning_count()`
- `def is_healthy()`
- `def to_dict()`
- `def print_summary()`
- `def load_schema()`
- `def validate_node()`
- `def validate_link()`
- `def check_graph_health()`
- `def get_nodes_missing_field()`
- `def get_detailed_missing_report()`
- `def main()`

**Docs:** `docs/schema/graph-health/PATTERNS_Graph_Health_Validation.md`

**Definitions:**
- `def get_player_name_from_graph()`
- `def get_player_name_from_yaml()`
- `class LintIssue`
- `class LintResult`
- `class TerminologyLinter`
- `def __init__()`
- `def should_skip()`
- `def get_files()`
- `def is_ok_context()`
- `def check_npc_usage()`
- `def check_player_as_name()`
- `def lint_file()`
- `def fix_file()`
- `def run()`
- `def report()`
- `def main()`

**Sections:**
- # Query Expected Outputs
- ## CHARACTER QUERIES
- ## KNOWLEDGE & BELIEFS
- ## PLACE & GEOGRAPHY
- ## THINGS & POSSESSIONS
- ## NARRATIVES & TENSIONS
- ## COMPLEX RELATIONSHIP QUERIES
- ## GAMEPLAY QUERIES
- ## ATMOSPHERIC QUERIES
- ## DEBUGGING & HEALTH CHECKS

**Sections:**
- # Query Results - Actual Data
- ## DATABASE STATS
- ## CHARACTER QUERIES
- ## KNOWLEDGE & BELIEFS
- ## SECRETS
- ## RUMORS
- ## OATHS & BLOOD
- ## PLACES
- ## TENSIONS
- ## COMPLEX QUERIES
- ## THINGS
- ## NARRATIVE TYPES

**Definitions:**
- `class SchemaViolation`
- `class TestResult`
- `class SchemaValidator`
- `def __init__()`
- `def _load_schema()`
- `def _query()`
- `def test_character_required_fields()`
- `def test_character_type_enum()`
- `def test_character_flaw_enum()`
- `def test_place_required_fields()`
- `def test_place_type_enum()`
- `def test_thing_required_fields()`
- `def test_thing_significance_enum()`
- `def test_narrative_required_fields()`
- `def test_narrative_type_enum()`
- `def test_tension_required_fields()`
- `def test_tension_pressure_range()`
- `def test_believes_link_structure()`
- `def test_believes_value_ranges()`
- `def test_at_link_structure()`
- `def test_carries_link_structure()`
- `def test_located_at_link_structure()`
- `def test_connects_link_structure()`
- `def test_orphan_characters()`
- `def test_characters_have_location()`
- `def test_things_have_location_or_carrier()`
- `def test_narratives_have_believers()`
- `def test_player_exists()`
- `def run_all_tests()`
- `def print_report()`
- `def validator()`
- `def test_character_required_fields()`
- `def test_character_type_enum()`
- `def test_place_required_fields()`
- `def test_place_type_enum()`
- `def test_thing_required_fields()`
- `def test_narrative_required_fields()`
- `def test_narrative_type_enum()`
- `def test_tension_pressure_range()`
- `def test_believes_link_structure()`
- `def test_at_link_structure()`
- `def test_player_exists()`
- `def main()`

**Docs:** `docs/infrastructure/api/`

**Definitions:**
- `class ActionRequest`
- `class SceneResponse`
- `class DialogueChunk`
- `class NewPlaythroughRequest`
- `class QueryRequest`
- `def create_app()`
- `def _mutation_event_handler()`
- `def get_orchestrator()`
- `def get_graph_queries()`
- `def get_playthrough_queries()`
- `def get_moment_queries()`
- `def get_graph_ops()`
- `async def health_check()`
- `async def create_playthrough()`
- `async def player_action()`
- `async def get_playthrough()`
- `class MomentClickRequest`
- `class MomentClickResponse`
- `async def moment_click()`
- `async def get_moment_view()`
- `async def get_current_view()`
- `async def get_moment_view_as_scene_tree()`
- `async def update_moment_weight()`
- `async def debug_stream()`
- `async def event_generator()`
- `async def get_map()`
- `async def get_ledger()`
- `async def get_faces()`
- `async def get_chronicle()`
- `async def semantic_query_post()`
- `async def semantic_query_get()`
- `async def inject_event()`

**Docs:** `docs/infrastructure/api/API_Graph_Management.md`

**Definitions:**
- `class CreateGraphRequest`
- `class CreateGraphResponse`
- `class GraphInfo`
- `class QueryRequest`
- `def create_graphs_router()`
- `def get_db()`
- `def clone_graph()`
- `async def create_graph()`
- `async def delete_graph()`
- `async def list_graphs()`
- `async def get_graph_info()`
- `async def list_nodes()`
- `async def query_graph()`
- `async def mutate_graph()`

**Definitions:**
- `def _resolve_graph_name()`
- `def _get_queries()`
- `def _get_traversal()`
- `def _get_surface()`
- `def _get_graph_queries()`
- `class MomentResponse`
- `class TransitionResponse`
- `class CurrentMomentsResponse`
- `class ClickRequest`
- `class ClickResponse`
- `class SurfaceRequest`
- `def create_moments_router()`
- `async def get_current_moments()`
- `async def click_word()`
- `async def get_moment_stats()`
- `async def surface_moment()`
- `async def moment_stream()`
- `async def event_generator()`
- `async def get_moment()`
- `def get_moments_router()`

**Docs:** `docs/infrastructure/api/PATTERNS_Api.md`

**Definitions:**
- `class PlaythroughCreateRequest`
- `class MomentRequest`
- `def _opening_to_scene_tree()`
- `def build_beat_narration()`
- `def _count_branches()`
- `def count_clickables()`
- `def _delete_branch()`
- `def create_playthroughs_router()`
- `def _get_playthrough_queries()`
- `async def create_playthrough()`
- `async def create_scenario_playthrough()`
- `async def send_moment()`
- `def dummy_embed()`
- `async def get_discussion_topics()`
- `async def get_discussion_topic()`
- `async def use_discussion_branch()`

**Docs:** `docs/infrastructure/api/IMPLEMENTATION_Api.md`

**Definitions:**
- `def get_sse_clients()`
- `def register_sse_client()`
- `def unregister_sse_client()`
- `def broadcast_moment_event()`

**Docs:** `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`

**Definitions:**
- `class SetSpeedRequest`
- `class PlayerInputRequest`
- `class TempoStateResponse`
- `class QueueSizeUpdate`
- `def create_tempo_router()`
- `async def set_speed()`
- `async def get_tempo_state()`
- `async def player_input()`
- `async def update_queue_size()`
- `async def start_tempo()`
- `async def stop_tempo()`
- `def _get_or_create_controller()`
- `def get_tempo_controller()`

**Docs:** `docs/infrastructure/embeddings/`

**Docs:** `docs/infrastructure/embeddings/`

**Definitions:**
- `class EmbeddingService`
- `def __init__()`
- `def _load_model()`
- `def _fallback_embed()`
- `def embed()`
- `def embed_batch()`
- `def embed_node()`
- `def _node_to_text()`
- `def similarity()`
- `def get_embedding_service()`

**Docs:** `docs/infrastructure/scene-memory/`

**Definitions:**
- `class MomentProcessor`
- `def __init__()`
- `def _load_transcript_line_count()`
- `def _write_transcript()`
- `def _append_to_transcript()`
- `def set_context()`
- `def process_dialogue()`
- `def process_narration()`
- `def process_player_action()`
- `def process_hint()`
- `def create_possible_moment()`
- `def link_moments()`
- `def link_narrative_to_moments()`
- `def _generate_id()`
- `def _tick_to_time_of_day()`
- `def last_moment_id()`
- `def transcript_line_count()`
- `def get_moment_processor()`

**Definitions:**
- `class AgentCliResult`
- `def get_agent_model()`
- `def _load_dotenv_if_needed()`
- `def build_agent_command()`
- `def run_agent()`
- `def parse_claude_json_output()`
- `def extract_claude_text()`
- `def _strip_code_fence()`
- `def parse_codex_stream_output()`

**Docs:** `docs/agents/narrator/`

**Definitions:**
- `class NarratorService`
- `def __init__()`
- `def generate()`
- `def _build_prompt()`
- `def _call_claude()`
- `def _fallback_response()`
- `def reset_session()`

**Definitions:**
- `class Orchestrator`
- `def __init__()`
- `def process_action()`
- `def process_action_streaming()`
- `def _build_scene_context()`
- `def _get_player_location()`
- `def _get_time_of_day()`
- `def _get_game_day()`
- `def _get_player_goal()`
- `def _get_recent_action()`
- `def _apply_mutations()`
- `def _parse_time()`
- `def _process_flips()`
- `def _build_graph_context()`
- `def _get_character_location_by_id()`
- `def _apply_wr_mutations()`
- `def new_game()`
- `def _world_injection_path()`
- `def _get_world_tick()`
- `def _load_world_injection()`
- `def _save_world_injection()`
- `def _clear_world_injection()`

**Docs:** `docs/agents/world-runner/PATTERNS_World_Runner.md`

**Definitions:**
- `class WorldRunnerService`
- `def __init__()`
- `def process_flips()`
- `def _build_prompt()`
- `def _call_claude()`
- `def _fallback_response()`

**Definitions:**
- `class TempoState`
- `class TempoController`
- `def __init__()`
- `def speed()`
- `def running()`
- `def set_speed()`
- `def _tick_interval()`
- `async def run()`
- `def stop()`

**Definitions:**
- `class MembraneContext`
- `def clamp()`
- `def activation_threshold()`
- `def weight_transfer_multiplier()`
- `def decay_scale()`
- `def tension_boost_scale()`

**Definitions:**
- `class MembraneProvider`
- `def __init__()`
- `def set_frame()`
- `def get_frame()`
- `def reset_place()`

**Docs:** `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`

**Definitions:**
- `class CharacterType`
- `class Face`
- `class SkillLevel`
- `class VoiceTone`
- `class VoiceStyle`
- `class Approach`
- `class Value`
- `class Flaw`
- `class PlaceType`
- `class Weather`
- `class Mood`
- `class ThingType`
- `class Significance`
- `class NarrativeType`
- `class NarrativeTone`
- `class NarrativeVoiceStyle`
- `class BeliefSource`
- `class PathDifficulty`
- `class MomentType`
- `class MomentStatus`
- `class MomentTrigger`
- `class ModifierType`
- `class ModifierSeverity`
- `class Modifier`
- `class Skills`
- `class CharacterVoice`
- `class Personality`
- `class Backstory`
- `class Atmosphere`
- `class NarrativeAbout`
- `class NarrativeVoice`
- `class TimeOfDay`
- `class NarrativeSource`
- `class GameTimestamp`
- `def __str__()`
- `def parse()`
- `def __lt__()`
- `def __le__()`
- `def __gt__()`
- `def __ge__()`

**Definitions:**
- `class CharacterNarrative`
- `def belief_intensity()`
- `class NarrativeNarrative`
- `def link_type()`
- `class CharacterPlace`
- `def is_present()`
- `class CharacterThing`
- `def has_item()`
- `class ThingPlace`
- `def is_here()`
- `class PlacePlace`
- `def travel_days()`

**Docs:** `docs/schema/`

**Definitions:**
- `class Character`
- `def embeddable_text()`
- `class Place`
- `def embeddable_text()`
- `class Thing`
- `def embeddable_text()`
- `class Narrative`
- `def embeddable_text()`
- `def is_core_type()`
- `class Moment`
- `def tick()`
- `def embeddable_text()`
- `def should_embed()`
- `def is_active()`
- `def is_spoken()`
- `def can_surface()`
- `class Config`

**Docs:** `docs/engine/moment-graph-engine/PATTERNS_Instant_Traversal_Moment_Graph.md`

**Docs:** `docs/engine/moment-graph-engine/PATTERNS_Instant_Traversal_Moment_Graph.md`

**Definitions:**
- `class MomentQueries`
- `def __init__()`
- `def get_current_view()`
- `def _get_transitions()`
- `def get_moment_by_id()`
- `def find_click_targets()`
- `def get_speaker_for_moment()`
- `def get_dormant_moments()`
- `def get_wait_triggers()`

**Definitions:**
- `class MomentSurface`
- `def __init__()`
- `def check_for_flips()`
- `def apply_decay()`
- `def handle_scene_change()`
- `def set_moment_weight()`
- `def get_surface_stats()`

**Docs:** `docs/engine/moment-graph-engine/PATTERNS_Instant_Traversal_Moment_Graph.md`

**Definitions:**
- `class MomentTraversal`
- `def __init__()`
- `def handle_click()`
- `def activate_moment()`
- `def speak_moment()`
- `def make_dormant()`
- `def decay_moment()`
- `def reactivate_dormant()`
- `def process_wait_triggers()`
- `def _update_status()`
- `def _set_weight()`
- `def _boost_weight()`
- `def _create_then_link()`

**Docs:** `docs/engine/moments/PATTERNS_Moments.md`

**Definitions:**
- `class Moment`
- `def not_implemented()`

**Docs:** `docs/physics/graph/PATTERNS_Graph.md`

**Definitions:**
- `class GraphClient`
- `def query()`
- `def get_character()`
- `def get_all_characters()`
- `def get_characters_at()`
- `def get_place()`
- `def get_path_between()`
- `def get_player_location()`
- `def get_narrative()`
- `def get_character_beliefs()`
- `def get_narrative_believers()`
- `def get_narratives_about()`
- `def get_all_tensions()`
- `def build_scene_context()`

**Docs:** `docs/physics/graph/PATTERNS_Graph.md`

**Definitions:**
- `class GraphOps`
- `def __init__()`
- `def _query()`
- `def _cosine_similarity()`
- `def _find_similar_nodes()`
- `def check_duplicate()`
- `def add_character()`
- `def add_place()`
- `def add_thing()`
- `def add_narrative()`
- `def add_tension()`
- `def add_moment()`
- `def apply_mutations()`
- `def get_graph()`

**Definitions:**
- `class ApplyOperationsMixin`
- `def apply()`
- `def _get_existing_node_ids()`
- `def _node_has_links()`
- `def _validate_link_targets()`
- `def _link_id()`
- `def _extract_character_args()`
- `def _extract_place_args()`
- `def _extract_thing_args()`
- `def _extract_narrative_args()`
- `def _extract_tension_args()`
- `def _extract_moment_args()`
- `def _extract_belief_args()`
- `def _extract_presence_args()`
- `def _extract_possession_args()`
- `def _extract_geography_args()`
- `def _extract_narrative_link_args()`
- `def _extract_thing_location_args()`
- `def _apply_node_update()`
- `def _apply_tension_update()`

**Definitions:**
- `class LinkCreationMixin`
- `def add_said()`
- `def add_moment_at()`
- `def add_moment_then()`
- `def add_narrative_from_moment()`
- `def add_can_speak()`
- `def add_attached_to()`
- `def add_can_lead_to()`
- `def add_belief()`
- `def add_presence()`
- `def move_character()`
- `def add_possession()`
- `def add_narrative_link()`
- `def add_thing_location()`
- `def add_geography()`
- `def add_contains()`
- `def add_about()`

**Definitions:**
- `class MomentOperationsMixin`
- `def handle_click()`
- `def update_moment_weight()`
- `def propagate_embedding_energy()`
- `def _get_current_tick()`
- `def decay_moments()`
- `def on_player_leaves_location()`
- `def on_player_arrives_location()`
- `def garbage_collect_moments()`
- `def boost_moment_weight()`

**Docs:** `docs/physics/graph/PATTERNS_Graph.md`

**Definitions:**
- `class GraphReadOps`
- `def __init__()`
- `def _query()`
- `def _parse_natural_language()`
- `def _collect_nodes_and_links()`
- `def query_cypher()`
- `def list_graphs()`
- `def query_natural_language()`
- `def search_semantic()`
- `def fetch_full_graph()`
- `def get_graph_reader()`

**Definitions:**
- `class QueryError`
- `def __init__()`
- `class GraphQueries`
- `def __init__()`
- `def _inject_energy_for_node()`
- `def _connect()`
- `def _query()`
- `def query()`
- `def _parse_node()`
- `def get_character()`
- `def get_all_characters()`
- `def get_characters_at()`
- `def get_place()`
- `def get_path_between()`
- `def get_narrative()`
- `def get_character_beliefs()`
- `def get_narrative_believers()`
- `def get_narratives_by_type()`
- `def get_narratives_about()`
- `def get_high_weight_narratives()`
- `def get_contradicting_narratives()`
- `def get_tension()`
- `def get_all_tensions()`
- `def get_flipped_tensions()`
- `def build_scene_context()`
- `def get_player_location()`
- `def get_queries()`

**Docs:** `docs/physics/IMPLEMENTATION_Physics.md`

**Definitions:**
- `class MomentQueryMixin`
- `def _maybe_inject_energy()`
- `def get_moment()`
- `def get_moments_at_place()`
- `def get_moments_by_character()`
- `def get_moments_in_tick_range()`
- `def get_moment_sequence()`
- `def get_narrative_moments()`
- `def get_narratives_from_moment()`
- `def search_moments()`
- `def _find_similar_moments_by_embedding()`
- `def get_current_view()`
- `def get_live_moments()`
- `def resolve_speaker()`
- `def get_available_transitions()`
- `def get_clickable_words()`

**Docs:** `docs/physics/IMPLEMENTATION_Physics.md`

**Definitions:**
- `class SearchQueryMixin`
- `def search()`
- `def _to_markdown()`
- `def _cosine_similarity()`
- `def _find_similar_by_embedding()`
- `def _get_connected_cluster()`

**Docs:** `None yet (extracted during monolith split)`

**Definitions:**
- `def cosine_similarity()`
- `def extract_node_props()`
- `def extract_link_props()`
- `def to_markdown()`
- `def view_to_scene_tree()`

**Definitions:**
- `def clamp()`
- `def softmax()`
- `def blend()`
- `class AttentionSplitContext`
- `class IncomingAxisLink`
- `class AttentionSink`
- `class AttentionSplitResult`
- `def compute_sink_mass()`
- `def apply_attention_split()`

**Definitions:**
- `class ClusterEnergyReading`
- `class ClusterEnergyMonitor`
- `def record()`
- `def recent_readings()`
- `def large_clusters()`
- `def detect_spike()`
- `def summary()`

**Definitions:**
- `def distance_to_proximity()`

**Definitions:**
- `def clamp()`
- `class ContradictionEdge`
- `class ContradictionPressureContext`
- `class ContradictionContribution`
- `class ContradictionPressureResult`
- `def compute_contradiction_pressure()`

**Definitions:**
- `class SnapPhase`
- `class SnapMomentContext`
- `class SnapPhaseRecord`
- `class SnapDisplayState`
- `def set_speed()`
- `def is_interrupt()`
- `def should_display()`
- `def execute_snap()`

**Definitions:**
- `class DisplaySnapshot`
- `class SnapCheckResult`
- `class ClusterEnergySummary`
- `def average_energy()`
- `def validate_snap_transition()`
- `def summarize_cluster_energy()`
- `def detect_cluster_surges()`

**Definitions:**
- `def clamp()`
- `class PrimeLink`
- `class PrimeDecayContext`
- `class PrimeContribution`
- `def compute_prime_effect()`
- `def compute_prime_contributions()`

**Docs:** `docs/physics/PATTERNS_Physics.md`

**Definitions:**
- `class TickResult`
- `class GraphTick`
- `def __init__()`
- `def run()`
- `def _process_moment_tick()`
- `def _compute_character_energies()`
- `def _compute_relationship_intensity()`
- `def _compute_proximity()`
- `def _get_character_location()`
- `def _parse_distance()`
- `def _flow_energy_to_narratives()`
- `def _propagate_energy()`
- `def _get_narrative_links()`
- `def _decay_energy()`
- `def _update_narrative_weights()`
- `def _adjust_criticality()`
- `def _tick_pressures()`
- `def _detect_flips()`

**Docs:** `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`

**Definitions:**
- `def is_narrator_running()`
- `def inject_via_queue()`
- `def inject_via_direct_call()`
- `def inject()`
- `def main()`

**Definitions:**
- `def graph_ops()`
- `def graph_queries()`
- `def setup_location()`
- `def setup_character()`
- `class TestE2EMomentCreation`
- `def test_create_moment_basic()`
- `def test_create_moment_with_clickables()`
- `class TestE2EViewQuery`
- `def test_get_current_view()`
- `class TestE2EClickHandling`
- `def test_click_triggers_weight_transfer()`
- `def test_click_no_match()`
- `class TestE2ELifecycle`
- `def test_decay_reduces_weight()`
- `def test_decay_to_decayed_status()`
- `def test_dormancy_on_leave()`
- `def test_reactivation_on_arrive()`
- `class TestE2EFullFlow`
- `def test_complete_conversation_flow()`

**Definitions:**
- `class TestMomentModel`
- `def test_moment_creation()`
- `def test_embeddable_text_dialogue()`
- `def test_embeddable_text_narration()`
- `def test_should_embed_long_text()`
- `def test_should_embed_short_text()`
- `class TestMomentGraphOps`
- `def test_extract_moment_args()`
- `class TestMomentProcessor`
- `def test_generate_id()`
- `def test_tick_to_time_of_day()`
- `def test_process_dialogue()`
- `def test_process_narration()`
- `def test_sequence_linking()`
- `def test_link_narrative_to_moments()`

**Definitions:**
- `def mock_graph_ops()`
- `def tracking_query()`
- `def mock_graph_queries()`
- `class TestMomentCreation`
- `def test_add_moment_basic()`
- `def test_add_moment_with_status_and_weight()`
- `def test_add_moment_with_tone()`
- `def test_add_moment_with_tick_spoken()`
- `def test_add_moment_with_speaker_creates_said_link()`
- `def test_add_moment_with_place_creates_at_link()`
- `def test_add_moment_with_after_creates_then_link()`
- `class TestCanSpeakLink`
- `def test_add_can_speak_basic()`
- `def test_add_can_speak_with_weight()`
- `class TestAttachedToLink`
- `def test_add_attached_to_basic()`
- `def test_add_attached_to_with_presence_required()`
- `def test_add_attached_to_non_persistent()`
- `def test_add_attached_to_dies_with_target()`
- `class TestCanLeadToLink`
- `def test_add_can_lead_to_basic()`
- `def test_add_can_lead_to_with_trigger()`
- `def test_add_can_lead_to_with_require_words()`
- `def test_add_can_lead_to_with_weight_transfer()`
- `def test_add_can_lead_to_bidirectional()`
- `def test_add_can_lead_to_with_wait_ticks()`
- `def test_add_can_lead_to_consumes_origin_false()`
- `class TestGetCurrentView`
- `def test_get_current_view_returns_structure()`
- `def test_get_current_view_queries_present_characters()`
- `class TestGetLiveMoments`
- `def test_get_live_moments_builds_correct_query()`
- `class TestResolveSpeaker`
- `def test_resolve_speaker_returns_highest_weight()`
- `def test_resolve_speaker_none_when_no_speakers()`
- `class TestGetAvailableTransitions`
- `def test_get_available_transitions_from_active()`
- `def test_get_available_transitions_empty_for_no_active()`
- `class TestGetClickableWords`
- `def test_get_clickable_words_extracts_from_transitions()`
- `class TestHandleClick`
- `def test_handle_click_no_transitions_queues_narrator()`
- `def test_handle_click_word_not_in_require_words()`
- `def test_handle_click_applies_weight_transfer()`
- `def tracking_query()`
- `def test_handle_click_flip_threshold()`
- `def tracking_query()`
- `def test_handle_click_no_flip_below_threshold()`
- `def tracking_query()`
- `class TestUpdateMomentWeight`
- `def test_update_weight_clamps_to_bounds()`
- `def tracking_query()`
- `def test_update_weight_triggers_flip()`
- `def tracking_query()`
- `def test_update_weight_no_flip_already_active()`
- `def tracking_query()`
- `class TestViewToSceneTree`
- `def test_view_to_scene_tree_basic_structure()`
- `def test_view_to_scene_tree_with_clickables()`
- `class TestInvariants`
- `def test_weight_bounds_invariant()`
- `def test_status_consistency_invariant()`
- `class TestBehavioralVisibility`
- `def test_presence_required_filters_correctly()`
- `class TestBehavioralSpeakerResolution`
- `def test_speaker_resolution_by_weight()`
- `class TestIntegrationConversationFlow`
- `def test_moment_creation_and_linking_flow()`
- `def test_click_to_flip_flow()`
- `def flow_query()`
- `class TestExtractMomentArgs`
- `def test_extract_moment_args_basic()`

**Definitions:**
- `def mock_graph_ops()`
- `def tracking_query()`
- `class TestDecayMoments`
- `def test_decay_applies_rate_to_possible_moments()`
- `def test_decay_marks_below_threshold_as_decayed()`
- `def test_decay_returns_counts()`
- `def test_decay_with_custom_tick()`
- `class TestDormancy`
- `def test_leaves_marks_persistent_as_dormant()`
- `def test_leaves_deletes_non_persistent()`
- `def test_leaves_returns_counts()`
- `def test_arrives_reactivates_dormant()`
- `def test_arrives_returns_count()`
- `class TestGarbageCollection`
- `def test_gc_removes_old_decayed()`
- `def test_gc_returns_count()`
- `class TestBoostMomentWeight`
- `def test_boost_adds_weight()`
- `def test_boost_caps_at_one()`
- `def test_boost_flips_above_threshold()`
- `class TestWorldTickIntegration`
- `def test_tick_calls_moment_decay()`
- `def test_tick_result_includes_moments_decayed()`
- `def test_tick_decay_iterations_scale_with_time()`

**Definitions:**
- `def mock_moment_queries()`
- `def mock_moment_traversal()`
- `def mock_moment_surface()`
- `def mock_graph_queries()`
- `def test_client()`
- `class TestGetCurrentMoments`
- `def test_get_current_moments_basic()`
- `def test_get_current_moments_with_clickable_words()`
- `def test_get_current_moments_auto_location()`
- `def test_get_current_moments_with_present_chars()`
- `class TestClickWord`
- `def test_click_word_success()`
- `def test_click_word_no_match()`
- `def test_click_word_error_handling()`
- `class TestGetMoment`
- `def test_get_moment_exists()`
- `def test_get_moment_not_found()`
- `class TestSurfaceMoment`
- `def test_surface_moment()`
- `class TestMomentStats`
- `def test_get_stats()`
- `class TestMomentStream`
- `def test_stream_connection()`
- `async def test_sse_broadcast_handles_queue_overload()`
- `class TestRequestValidation`
- `def test_click_requires_playthrough_id()`
- `def test_click_requires_moment_id()`
- `def test_surface_requires_both_ids()`
- `class TestResponseModels`
- `def test_current_moments_response_shape()`
- `def test_click_response_shape()`

**Definitions:**
- `def mock_graph_ops()`
- `def tracking_add_moment()`
- `def tracking_add_can_lead_to()`
- `def tracking_add_can_speak()`
- `def tracking_add_attached_to()`
- `def mock_moment_processor()`
- `class TestClickableParsing`
- `def test_parse_single_clickable()`
- `def test_parse_multiple_clickables()`
- `def test_parse_no_clickables()`
- `def test_parse_clickable_with_special_chars()`
- `class TestMomentProcessorSchema`
- `def test_process_dialogue_with_tone()`
- `def test_process_dialogue_with_weight_and_status()`
- `def test_process_narration_with_tone()`
- `def test_process_hint_defaults()`
- `def test_spoken_status_sets_tick_spoken()`
- `def test_possible_status_no_tick_spoken()`
- `class TestPossibleMomentCreation`
- `def test_create_possible_moment_basic()`
- `def test_create_possible_moment_with_attachments()`
- `class TestMomentLinking`
- `def test_link_moments_basic()`
- `def test_link_moments_with_weight_transfer()`
- `class TestGraphModeIntegration`
- `def test_create_moment_with_single_clickable()`
- `def test_create_moment_with_multiple_clickables()`
- `def test_create_moment_with_tone()`
- `class TestWeightActivation`
- `def test_weight_below_threshold_stays_possible()`

**Definitions:**
- `def test_attention_split_conserves_budget()`
- `def test_primes_lag_and_half_life()`
- `def test_contradiction_pressure_accumulates_and_decays()`

**Definitions:**
- `def test_validate_snap_transition_success()`
- `def test_validate_snap_transition_fails_when_missing_beat()`
- `def test_summarize_cluster_energy_and_detect_surges()`
- `def test_detect_cluster_surges_returns_empty_for_no_data()`

**Definitions:**
- `def playthroughs_client()`
- `def tempo_client()`
- `class TestPlaythroughRouterValidation`
- `def test_playthrough_requires_player_name()`
- `def test_playthrough_scenario_alias_requires_scenario_id()`
- `def test_send_moment_requires_text()`
- `class TestTempoRouterValidation`
- `def test_set_speed_requires_speed()`
- `def test_set_speed_rejects_invalid_literal()`
- `def test_player_input_requires_text()`
- `def test_queue_size_requires_queue_length()`

**Definitions:**
- `def extract_yaml_from_markdown()`
- `def extract_enums_from_schema()`
- `def find_enums()`
- `def extract_constants_from_content()`
- `class TestSchemaSpecAlignment`
- `def test_node_types_exist()`
- `def test_character_type_enum()`
- `def test_narrative_type_enum()`
- `class TestEnumConsistency`
- `def test_character_types_complete()`
- `def test_place_scales_hierarchical()`
- `def test_narrative_types_cover_all_categories()`
- `def test_skill_levels_ordered()`
- `def test_pressure_types_complete()`
- `def test_moment_types_cover_all_sources()`
- `class TestConstantsConsistency`
- `def test_belief_flow_rate_valid()`
- `def test_max_propagation_hops_positive()`
- `def test_decay_rate_valid()`
- `def test_min_weight_small()`
- `def test_breaking_point_valid()`
- `def test_link_factors_sum_reasonable()`
- `def test_link_factors_all_positive()`
- `def test_supersedes_has_drain_effect()`
- `def test_contradicts_highest_factor()`
- `class TestSpecInternalConsistency`
- `def test_core_types_for_slow_decay()`
- `def test_character_flaws_distinct()`
- `def test_voice_styles_cover_emotional_range()`
- `def test_modifier_types_cover_all_node_types()`
- `def test_road_types_have_speed_ordering()`
- `class TestCrossReferences`
- `def test_tension_references_narratives()`
- `def test_belief_source_types_make_sense()`
- `def test_narrative_about_fields_valid()`

**Definitions:**
- `def create_indexes()`
- `def load_initial_state()`
- `def verify_data()`
- `def main()`

**Docs:** `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`

**Definitions:**
- `def main()`
- `def run_shell_command()`
- `def read_file()`
- `def list_directory()`
- `def search_file_content()`
- `def glob_files()`
- `def replace_text()`
- `def write_file()`
- `def google_web_search()`
- `def web_fetch()`
- `def codebase_investigator()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class ShimmerStatic`
- `def __init__()`
- `def on_mount()`
- `def _render_shimmer()`
- `async def _animate_shimmer()`
- `def stop_shimmer()`
- `class ClickableStatic`
- `def __init__()`
- `def on_click()`
- `class AgentContainer`
- `def __init__()`
- `def _prepare_markdown()`
- `def _set_markdown_content()`
- `def compose()`
- `def on_mount()`
- `def add_agent()`
- `def update_agent()`
- `def remove_agent()`
- `def set_agent_status()`
- `def update_sync_content()`
- `def update_doctor_content()`
- `def get_path()`
- `def update_map_content()`
- `def update_changes_content()`
- `def switch_to_tab()`
- `def add_summary()`
- `def add_shimmer_agent()`
- `def stop_shimmer_agent()`
- `def clear_summary()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class AgentPanel`
- `def __init__()`
- `def on_mount()`
- `def on_scroll()`
- `def toggle_collapse()`
- `def collapse()`
- `def expand()`
- `def _update_header_text()`
- `def set_output()`
- `def append_output()`
- `def _maybe_render()`
- `def _flush_render()`
- `def _do_render()`
- `def set_status()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class InputBar`
- `class CommandSubmitted`
- `def __init__()`
- `class InputChanged`
- `class ShowSuggestions`
- `def __init__()`
- `def __init__()`
- `def on_mount()`
- `def _update_height()`
- `def on_text_area_changed()`
- `def value()`
- `def value()`
- `def _submit()`
- `def on_key()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class ClickableStatic`
- `def __init__()`
- `def on_click()`
- `async def update()`
- `class ClickableMarkdown`
- `def __init__()`
- `def on_click()`
- `async def update()`
- `class ManagerPanel`
- `def __init__()`
- `def on_mount()`
- `def _is_at_bottom()`
- `def _auto_scroll()`
- `def add_message()`
- `def add_thinking()`
- `def add_tool_call()`
- `def escape_markup()`
- `def clear()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class StatusBar`
- `def __init__()`
- `def set_folder()`
- `def update_health()`
- `def set_repair_progress()`
- `def clear_repair_progress()`
- `def _start_animation()`
- `def _stop_animation()`
- `def _animate()`
- `def _format_progress_bar()`
- `def _format_bar()`
- `def _refresh_display()`
- `def _get_health_color()`
- `def on_resize()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class SuggestionsBar`
- `def __init__()`
- `def show_suggestions()`

**Docs:** `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md`

**Definitions:**
- `def main()`

**Docs:** `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md`

**Definitions:**
- `def check_textual()`
- `class NgramApp`
- `def __init__()`
- `def compose()`
- `async def on_mount()`
- `async def _startup_sequence()`
- `async def _start_claude_pty()`
- `async def on_claude_output()`
- `async def _animate_loading()`
- `def on_click()`
- `async def on_input_bar_command_submitted()`
- `def on_input_bar_input_changed()`
- `def on_input_bar_show_suggestions()`
- `async def _run_doctor()`
- `async def _run_doctor_with_display()`
- `async def _load_doctor_data()`
- `async def _load_sync_data()`
- `async def _load_map_data()`
- `async def _load_git_data()`
- `async def get_status()`
- `async def get_log()`
- `async def get_recent_commit_rate()`
- `async def get_recent_change_rate()`
- `async def _refresh_changes_tab()`
- `async def _refresh_sync_tab()`
- `async def _refresh_map_tab()`
- `async def _refresh_doctor_tab()`
- `async def _run_doctor_async()`
- `async def _handle_drift_warning()`
- `async def handle_command()`
- `def log_error()`
- `def on_exception()`
- `def notify_manager_response()`
- `def reset_manager_session()`
- `async def action_interrupt_or_quit()`
- `def _reset_ctrl_c()`
- `async def action_quit()`
- `async def action_doctor()`
- `async def action_repair()`
- `def action_tab_agents()`
- `def action_tab_sync()`
- `def action_tab_doctor()`
- `def action_tab_map()`
- `def action_tab_changes()`
- `def action_next_tab()`
- `def action_prev_tab()`
- `def _switch_tab()`
- `def _cycle_tab()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `def build_manager_overview_prompt()`
- `async def show_static_overview()`
- `async def start_manager_with_overview()`

**Docs:** `docs/tui/BEHAVIORS_TUI_Interactions.md`

**Definitions:**
- `def _truncate_thinking()`
- `def _output_indicates_rate_limit()`
- `async def handle_command()`
- `async def handle_message()`
- `async def _animate_loading()`
- `async def handle_help()`
- `async def handle_run()`
- `async def _run_shell_command()`
- `async def handle_repair()`
- `def _get_last_messages()`
- `async def _periodic_agent_summary()`
- `async def _run_git_command()`
- `async def _spawn_agent()`
- `async def on_output()`
- `async def _run_agent()`
- `async def _spawn_next_from_queue()`
- `async def _manager_review_agent()`
- `async def handle_doctor()`
- `async def handle_quit()`
- `async def handle_clear()`
- `async def handle_issues()`
- `async def handle_logs()`
- `async def handle_reset_manager()`
- `async def _refresh_map()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `def _detect_commands()`
- `def _build_codex_history_prompt()`
- `async def _run_agent_message()`
- `async def run_agent()`
- `def throttled_update()`
- `async def drain_stderr()`
- `def _build_review_prompt()`
- `async def _run_manager_review()`
- `def _parse_correction_feedback()`
- `async def _relaunch_agent_with_feedback()`
- `async def run_continuation()`

**Docs:** `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md`

**Definitions:**
- `class DriftWarning`
- `class ClaudePTY`
- `def __init__()`
- `async def start()`
- `async def _read_output()`
- `def _clean_output()`
- `async def send()`
- `async def stop()`
- `def is_running()`
- `class ManagerSupervisor`
- `def __init__()`
- `def _normalize_path()`
- `def extract_changed_files()`
- `def extract_doc_updates()`
- `async def check_agent_output()`
- `async def monitor_agent()`
- `async def on_agent_complete()`
- `def write_guidance()`
- `def clear_guidance()`

**Docs:** `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`

**Definitions:**
- `class ConversationMessage`
- `def to_dict()`
- `def from_dict()`
- `class ConversationHistory`
- `def __init__()`
- `def _load()`
- `def _save()`
- `def add_message()`
- `def get_recent()`
- `def clear()`
- `def start_new_session()`
- `class AgentHandle`
- `def duration()`
- `def is_active()`
- `def append_output()`
- `def get_output()`
- `class SessionState`
- `def add_agent()`
- `def remove_agent()`
- `def get_agent()`
- `def add_manager_message()`
- `def active_count()`
- `def clear_completed()`

**Docs:** `docs/ngram_cli_core/OBJECTIFS_ngram_cli_core.md`

**Definitions:**
- `def _add_module_translation_args()`
- `def _validate_module_translation()`
- `def _add_refactor_conflict_args()`
- `def _validate_refactor_conflicts()`
- `def main()`

**Docs:** `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`

**Definitions:**
- `def doctor_check_new_undoc_code()`
- `def doctor_check_doc_duplication()`
- `def doctor_check_recent_log_errors()`
- `def doctor_check_long_strings()`
- `def _strip_code_blocks()`
- `def _extract_questions_from_text()`
- `def doctor_check_legacy_markers()`
- `def _extract_marker_priority()`
- `def doctor_check_special_markers()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `def save_doctor_config()`
- `def parse_gitignore()`
- `def load_doctor_config()`
- `def load_doctor_ignore()`
- `def is_issue_ignored()`
- `def filter_ignored_issues()`
- `def extract_docs_references_from_file()`
- `def _parse_doc_false_positives()`
- `def parse_doctor_doc_tags()`
- `def load_doctor_false_positives()`
- `def filter_false_positive_issues()`
- `def add_doctor_ignore()`
- `def should_ignore_path()`
- `def is_binary_file()`
- `def find_code_directories()`
- `def has_direct_code_files()`
- `def find_leaf_code_dirs()`
- `def find_source_files()`
- `def count_lines()`
- `def find_long_sections()`

**Definitions:**
- `def get_issue_guidance()`
- `def get_issue_explanation()`
- `def generate_health_markdown()`
- `def print_doctor_report()`
- `def check_sync_status()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `def _escape_marker_tokens()`
- `def _copy_skills()`
- `def _update_root_claude_md()`
- `def _build_root_claude_section()`
- `def _build_claude_addition()`
- `def _build_agents_addition()`
- `def _build_manager_agents_addition()`
- `def _remove_write_permissions()`
- `def _enforce_readonly_for_views()`
- `def _enforce_readonly_for_templates()`
- `def init_protocol()`
- `def copy_protocol_partial()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `def get_severity_color()`
- `def get_agent_color()`
- `def get_agent_symbol()`
- `def load_github_issue_mapping()`
- `def save_github_issue_mapping()`
- `def spawn_repair_agent()`
- `async def _on_output()`
- `def repair_command()`
- `def run_repair()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `def get_symbol_name()`
- `def get_issue_folder_name()`
- `class RepairResult`
- `class EscalationDecision`
- `def get_learnings_content()`
- `def _get_git_head()`
- `def get_issue_symbol()`
- `def get_issue_action_parts()`
- `def get_issue_action()`
- `def get_depth_types()`
- `def split_docs_to_read()`
- `def _detect_recent_issue_number()`
- `def build_agent_prompt()`
- `def parse_decisions_from_output()`
- `def parse_stream_json_line()`
- `async def spawn_repair_agent_async()`
- `def run_agent_sync()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `def get_issue_instructions()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `class FileInfo`
- `class DependencyInfo`
- `class RepoOverview`
- `def get_language()`
- `def extract_docs_ref()`
- `def extract_markdown_sections()`
- `def extract_markdown_code_refs()`
- `def extract_markdown_doc_refs()`
- `def extract_code_definitions()`
- `def count_chars()`
- `def _filter_local_imports()`
- `def build_file_tree()`
- `def get_dependency_info()`
- `def count_tree_stats()`
- `def traverse()`
- `def count_docs_structure()`
- `def generate_repo_overview()`
- `def _save_single_map()`
- `def generate_and_save()`

**Docs:** `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Definitions:**
- `class ValidationResult`
- `def check_protocol_installed()`
- `def check_project_sync_exists()`
- `def check_module_docs_minimum()`
- `def check_full_chain()`
- `def check_chain_links()`
- `def check_naming_conventions()`
- `def check_views_exist()`
- `def check_module_manifest()`
- `def generate_fix_prompt()`
- `def validate_protocol()`

**Sections:**
- # ngram Manager
- ## Your Role
- ## Context You Have
- ## What You Can Do
- ## What You Output
- ## Guidelines
- ## Special Marker Check
- ## Files to Check
- ## Updating LEARNINGS Files
- ## After Your Response

**Sections:**
- # Skill: `ngram.create_module_documentation`
- ## Maps to VIEW
- ## Purpose
- ## Inputs (YAML)
- ## Outputs (YAML)
- ## Gates (non-negotiable)
- ## Evidence & referencing
- ## Markers
- ## Never-stop rule

**Sections:**
- # Skill: `ngram.debug_investigate_fix_issues`
- ## Maps to VIEW
- ## Purpose
- ## Inputs (YAML)
- ## Outputs (YAML)
- ## Gates (non-negotiable)
- ## Evidence & referencing
- ## Markers
- ## Never-stop rule

**Sections:**
- # Skill: `ngram.health_define_and_verify`
- ## Maps to VIEW
- ## Purpose
- ## Inputs (YAML)
- ## Outputs (YAML)
- ## Gates (non-negotiable)
- ## Evidence & referencing
- ## Markers
- ## Never-stop rule

**Sections:**
- # Skill: `ngram.extend_add_features`
- ## Maps to VIEW
- ## Purpose
- ## Inputs (YAML)
- ## Outputs (YAML)
- ## Gates (non-negotiable)
- ## Evidence & referencing
- ## Markers
- ## Never-stop rule

**Sections:**
- # Skill: `ngram.implement_write_or_modify_code`
- ## Maps to VIEW
- ## Purpose
- ## Inputs (YAML)
- ## Outputs (YAML)
- ## Gates (non-negotiable)
- ## Evidence & referencing
- ## Markers
- ## Never-stop rule

**Sections:**
- # Skill: `ngram.ingest_raw_data_sources`
- ## Maps to VIEW
- ## Purpose
- ## Inputs (YAML)
- ## Outputs (YAML)
- ## Gates (non-negotiable)
- ## Evidence & referencing
- ## Markers
- ## Never-stop rule

**Sections:**
- # Skill: `ngram.onboard_understand_module_codebase`
- ## Maps to VIEW
- ## Purpose
- ## Inputs (YAML)
- ## Outputs (YAML)
- ## Gates (non-negotiable)
- ## Evidence & referencing
- ## Markers
- ## Never-stop rule

**Sections:**
- # Skill: `ngram.orchestrate_feature_integration`
- ## Maps to VIEW
- ## Purpose
- ## Inputs (YAML)
- ## Outputs (YAML)
- ## Gates (non-negotiable)
- ## Evidence & referencing
- ## Markers
- ## Never-stop rule

**Sections:**
- # Skill: `ngram.review_evaluate_changes`
- ## Maps to VIEW
- ## Purpose
- ## Inputs (YAML)
- ## Outputs (YAML)
- ## Gates (non-negotiable)
- ## Evidence & referencing
- ## Markers
- ## Never-stop rule

**Sections:**
- # Skill: `ngram.sync_update_module_state`
- ## Maps to VIEW
- ## Purpose
- ## Inputs (YAML)
- ## Outputs (YAML)
- ## Gates (non-negotiable)
- ## Evidence & referencing
- ## Markers
- ## Never-stop rule

**Sections:**
- # Project — Sync: Current State
- ## CURRENT STATE
- ## ACTIVE WORK
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## AREAS
- ## MODULE COVERAGE

**Code refs:**
- `{path/to/main/source/file.py`

**Sections:**
- # {Module Name} — Algorithm: {Brief Description of Procedures and Logic}
- ## CHAIN
- ## OVERVIEW
- ## OBJECTIVES AND BEHAVIORS
- ## DATA STRUCTURES
- ## ALGORITHM: {Primary Function Name}
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## MARKERS

**Code refs:**
- `{path/to/main/source/file.py`

**Sections:**
- # {Module Name} — Behaviors: {Brief Description of Observable Effects}
- ## CHAIN
- ## BEHAVIORS
- ## OBJECTIVES SERVED
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## MARKERS

**Sections:**
- # CONCEPT: {Concept Name} — {What This Concept Is}
- ## WHAT IT IS
- ## WHY IT EXISTS
- ## KEY PROPERTIES
- ## RELATIONSHIPS TO OTHER CONCEPTS
- ## THE CORE INSIGHT
- ## COMMON MISUNDERSTANDINGS
- ## SEE ALSO

**Code refs:**
- `{path/to/health/checker_script.py`

**Sections:**
- # {Module} — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## OBJECTIVES COVERAGE
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: {Indicator Name}
- ## HOW TO RUN
- # Run all health checks for this module
- # Run a specific checker
- ## KNOWN GAPS
- ## MARKERS

**Code refs:**
- `{path/to/main/source/file.py`

**Sections:**
- # {Module} — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## EXTRACTION CANDIDATES
- ## MARKERS

**Sections:**
- # OBJECTIFS — {Module}
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `{path/to/main/source/file.py`

**Sections:**
- # {Module Name} — Patterns: {Brief Design Philosophy Description}
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Sections:**
- # {Module/Area/Project} — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Sections:**
- # TOUCHES: Where {Concept Name} Appears in the System
- ## MODULES THAT IMPLEMENT
- ## INTERFACES
- ## DEPENDENCIES
- ## INVARIANTS ACROSS MODULES
- ## CONFLICTS / TENSIONS
- ## SYNC
- ## WHEN TO UPDATE THIS FILE

**Code refs:**
- `{path/to/main/source/file.py`

**Sections:**
- # {Module Name} — Validation: {Brief Description of Invariants and Tests}
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Run tests
- # Run with coverage
- ## SYNC STATUS
- ## MARKERS

**Sections:**
- # VIEW: Analyze — Structural Analysis and Recommendations
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## ANALYSIS CHECKLIST
- ## OUTPUT FORMAT
- ## Current Structure
- ## Recommendations
- ## Proposed Structure
- ## AFTER ANALYSIS
- ## Structural Analysis — [DATE]
- ## HANDOFF
- ## VERIFICATION

**Sections:**
- # VIEW: Debug
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## THE WORK
- ## WHEN YOU FIND IT
- ## HANDOFFS
- ## OBSERVATIONS (Living Documentation)
- ## Agent Observations
- ## VERIFICATION

**Sections:**
- # VIEW: Document New Module
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## THE WORK
- ## CHAIN
- # DOCS: docs/backend/auth/PATTERNS_Why_JWT_With_Refresh_Tokens.md
- ## MINIMUM VIABLE DOCUMENTATION
- ## AFTER DOCUMENTATION
- ## VERIFICATION

**Code refs:**
- `file_utils.py`
- `ngram/utils/file_utils.py`
- `ngram/utils/string_utils.py`
- `ngram/utils/validation_utils.py`
- `src/analytics/batch_ingest.py`
- `src/analytics/storage/event_store.py`
- `src/analytics/stream_ingest.py`
- `src/analytics/validation/schema_rules.py`
- `src/dashboard/op_metrics.py`
- `src/dashboard/product_metrics.py`
- `string_utils.py`
- `utils.py`

**Sections:**
- # VIEW: Escalation & Proposition
- ## VISION
- ## THE PATTERN
- ## HOW ESCALATION WORKS
- ## HOW PROPOSITION WORKS
- ## HOW TODO WORKS
- ## WHEN TO ESCALATE (PRECISE)
- ## WHEN NOT TO ESCALATE
- ## ESCALATION TYPES
- ## ESCALATION MARKER FORMAT (YAML)
- ## PROPOSITION MARKER FORMAT (YAML)
- ## PRIORITY SCALE (HOW TO SET)
- ## HOOKS (WHEN TO INCLUDE)
- ## TODO MARKER FORMAT (YAML)

**Sections:**
- # VIEW: Extend
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## PLANNING
- ## THE WORK
- ## BEFORE VERIFICATION: DOC VERIFICATION
- ## AFTER EXTENDING
- # modules.yaml (project root)
- ## HANDOFFS
- ## OBSERVATIONS (Living Documentation)
- ## Agent Observations
- ## VERIFICATION

**Sections:**
- # VIEW: Health — Define Health Checks and Verify System Health
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## WHAT TO DEFINE
- ## WRITING GOOD HEALTH
- ## AFTER DEFINING HEALTH
- ## OBSERVATIONS (Living Documentation)
- ## Agent Observations
- ## HANDOFF
- ## VERIFICATION
- ## DOCTOR FALSE POSITIVES

**Sections:**
- # VIEW: Implement
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## THE WORK
- ## BEFORE VERIFICATION: DOC VERIFICATION
- ## AFTER IMPLEMENTATION
- # modules.yaml (project root)
- # ... other fields as relevant
- ## OBSERVATIONS (Living Documentation)
- ## Agent Observations
- ## VERIFICATION

**Sections:**
- # VIEW: Ingest — Process Raw Data Sources
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## THE WORK
- ## OUTPUT
- ## HANDOFF
- ## VERIFICATION
- ## TIPS

**Sections:**
- # VIEW: Onboard — Understand Existing Codebase
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## WHAT TO BUILD
- ## QUESTIONS TO ANSWER
- ## CODE RESTRUCTURE ANALYSIS
- ## Proposed Structure Changes
- ## OUTPUT
- ## HANDOFF

**Sections:**
- # VIEW: Refactor — Improve Code Structure Without Changing Behavior
- ## WHY THIS VIEW EXISTS
- ## CONTEXT TO LOAD
- ## BEFORE REFACTORING
- ## WHILE REFACTORING
- ## AFTER REFACTORING
- ## OBSERVATIONS (Living Documentation)
- ## Agent Observations
- ## HANDOFF
- ## VERIFICATION

**Sections:**
- # Working Principles
- ## Architecture: One Solution Per Problem
- ## Verification: Test Before Claiming Built
- ## Communication: Depth Over Brevity
- ## Quality: Never Degrade
- ## Experience: User Before Infrastructure
- ## Feedback Loop: Human-Agent Collaboration
- ## How These Principles Integrate

**Code refs:**
- `doctor_cli_parser_and_run_checker.py`
- `semantic_proximity_based_character_node_selector.py`
- `snake_case.py`

**Doc refs:**
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # ngram Framework
- ## WHY THIS PROTOCOL EXISTS
- ## COMPANION: PRINCIPLES.md
- ## THE CORE INSIGHT
- ## HOW TO USE THIS
- ## FILE TYPES AND THEIR PURPOSE
- ## KEY PRINCIPLES (from PRINCIPLES.md)
- ## STRUCTURING YOUR DOCS
- ## WHEN DOCS DON'T EXIST
- ## THE DOCUMENTATION PROCESS
- ## Maturity
- ## NAMING ENGINEERING PRINCIPLES
- ## THE PROTOCOL IS A TOOL

**Sections:**
- ## 4. Protocol-First Reading
- ## 5. Parallel Work Awareness
- ## 6. Operational Proactivity
- ## 5. Communication Principles

**Sections:**
- ## GEMINI Agent Operating Principles (Derived from ngram Protocol)
- ## Operational Directives

**Docs:** `docs/tools/PATTERNS_Tools.md`

**Definitions:**
- `def _is_safe_relative_path()`
- `def _split_sections()`
- `def main()`

**Docs:** `docs/tools/PATTERNS_Tools.md`

**Definitions:**
- `def get_playthrough_graph_name()`
- `def get_graph_ops()`
- `def get_graph_queries()`
- `def get_current_tick()`
- `def get_current_place()`
- `def create_moment_with_clickables()`
- `def parse_inline_clickables()`
- `def replace_match()`
- `def stream_event()`
- `def main()`

**Code refs:**
- `doctor_cli_parser_and_run_checker.py`
- `semantic_proximity_based_character_node_selector.py`
- `snake_case.py`

**Doc refs:**
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # ngram
- # Working Principles
- ## Architecture: One Solution Per Problem
- ## Verification: Test Before Claiming Built
- ## Communication: Depth Over Brevity
- ## Quality: Never Degrade
- ## Experience: User Before Infrastructure
- ## Feedback Loop: Human-Agent Collaboration
- ## How These Principles Integrate
- # ngram Framework
- ## WHY THIS PROTOCOL EXISTS
- ## COMPANION: PRINCIPLES.md
- ## THE CORE INSIGHT
- ## HOW TO USE THIS
- ## FILE TYPES AND THEIR PURPOSE
- ## KEY PRINCIPLES (from PRINCIPLES.md)
- ## STRUCTURING YOUR DOCS
- ## WHEN DOCS DON'T EXIST
- ## THE DOCUMENTATION PROCESS
- ## Maturity
- ## NAMING ENGINEERING PRINCIPLES
- ## THE PROTOCOL IS A TOOL
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change
- ## CLI Commands
- ## 4. Protocol-First Reading
- ## 5. Parallel Work Awareness
- ## 6. Operational Proactivity
- ## 5. Communication Principles

**Sections:**
- # ngram
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change

**Sections:**
- # ngram
- ## The Problem
- ## The Solution
- ## Quick Start
- # Install
- # Initialize in your project
- # Check protocol health
- # Check project health (monoliths, stale docs, etc.)
- # Auto-fix issues with agents
- # Get documentation context for a file
- # Generate bootstrap prompt for LLM
- # Expose local port 3005 via ngrok
- # Run FalkorDB MCP server
- # Restart full stack (FalkorDB, BE, FE, MCP server, ngrok)
- ## CLI Commands
- ## How It Works
- # ngram
- # VIEW: Implement
- ## LOAD FIRST
- ## AFTER CHANGES
- ## Documentation Chain
- ## Key Concepts
- ## Design Principles
- ## License
- ## Contributing

**Code refs:**
- `__init__.py`
- `agent_cli.py`
- `api/connectome/graph/route.ts`
- `api/connectome/graphs/route.ts`
- `api/connectome/search/route.ts`
- `api/sse/route.ts`
- `app.py`
- `app/api/connectome/graph/route.ts`
- `app/api/connectome/graphs/route.ts`
- `app/api/connectome/search/route.ts`
- `app/api/route.ts`
- `app/api/sse/route.ts`
- `app/connectome/components/connectome_health_panel.ts`
- `app/connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts`
- `app/connectome/components/connectome_log_export_buttons_using_state_store_serializers.ts`
- `app/connectome/components/connectome_log_export_buttons_using_state_store_serializers.tsx`
- `app/connectome/components/connectome_log_trigger_and_calltype_badge_color_tokens.ts`
- `app/connectome/components/connectome_page_shell_route_layout_and_control_surface.ts`
- `app/connectome/components/connectome_page_shell_route_layout_and_control_surface.tsx`
- `app/connectome/components/deterministic_zone_and_node_layout_computation_helpers.ts`
- `app/connectome/components/edge_kit/connectome_edge_directional_shine_animation_helpers.ts`
- `app/connectome/components/edge_kit/connectome_edge_label_renderer_with_halo_and_zoom_policy.ts`
- `app/connectome/components/edge_kit/connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx`
- `app/connectome/components/edge_kit/connectome_edge_pulse_particle_animation_and_boundary_clamp_helpers.ts`
- `app/connectome/components/edge_kit/connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts`
- `app/connectome/components/edge_kit/connectome_node_boundary_intersection_geometry_helpers.ts`
- `app/connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.ts`
- `app/connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.tsx`
- `app/connectome/components/edge_label_declutter_and_visibility_policy_helpers.ts`
- `app/connectome/components/node_kit/connectome_energy_badge_bucketed_glow_and_value_formatter.ts`
- `app/connectome/components/node_kit/connectome_energy_badge_bucketed_glow_and_value_formatter.tsx`
- `app/connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts`
- `app/connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.ts`
- `app/connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`
- `app/connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.ts`
- `app/connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.tsx`
- `app/connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.ts`
- `app/connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.tsx`
- `app/connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.ts`
- `app/connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.tsx`
- `app/connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.ts`
- `app/connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.tsx`
- `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.ts`
- `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`
- `app/connectome/components/stepper/node_stepper_control.tsx`
- `app/connectome/components/telemetry_camera_controls.ts`
- `app/connectome/components/unified_now_and_copyable_ledger_log_panel.ts`
- `app/connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`
- `app/connectome/lib/connectome_export_jsonl_and_text_log_serializer.ts`
- `app/connectome/lib/connectome_session_boundary_and_restart_policy_controller.ts`
- `app/connectome/lib/connectome_step_script_sample_sequence.ts`
- `app/connectome/lib/connectome_system_map_node_edge_manifest.ts`
- `app/connectome/lib/connectome_wait_timer_progress_and_tick_display_signal_selectors.ts`
- `app/connectome/lib/flow_event_duration_bucket_color_classifier.ts`
- `app/connectome/lib/flow_event_schema_and_normalization_contract.ts`
- `app/connectome/lib/flow_event_trigger_and_calltype_inference_rules.ts`
- `app/connectome/lib/minimum_duration_clamp_and_speed_based_default_policy.ts`
- `app/connectome/lib/next_step_gate_and_realtime_playback_runtime_engine.ts`
- `app/connectome/lib/step_script_cursor_and_replay_determinism_helpers.ts`
- `app/connectome/lib/zustand_connectome_state_store_with_atomic_commit_actions.ts`
- `app/connectome/page.tsx`
- `app/layout.ts`
- `app/layout.tsx`
- `app/ngram/page.tsx`
- `app/page.ts`
- `app/page.tsx`
- `app_core.py`
- `app_manager.py`
- `base.py`
- `check_health.py`
- `cli.py`
- `commands.py`
- `commands_agent.py`
- `connectome/components/connectome_health_panel.tsx`
- `connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts`
- `connectome/components/connectome_log_export_buttons_using_state_store_serializers.tsx`
- `connectome/components/connectome_log_trigger_and_calltype_badge_color_tokens.ts`
- `connectome/components/connectome_page_shell_route_layout_and_control_surface.tsx`
- `connectome/components/deterministic_zone_and_node_layout_computation_helpers.ts`
- `connectome/components/edge_kit/connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx`
- `connectome/components/edge_kit/connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts`
- `connectome/components/edge_kit/connectome_node_boundary_intersection_geometry_helpers.ts`
- `connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.tsx`
- `connectome/components/edge_label_declutter_and_visibility_policy_helpers.ts`
- `connectome/components/node_kit/connectome_energy_badge_bucketed_glow_and_value_formatter.tsx`
- `connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts`
- `connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`
- `connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.tsx`
- `connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.tsx`
- `connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.tsx`
- `connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.tsx`
- `connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`
- `connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`
- `connectome_doc_bundle_splitter_and_fence_rewriter.py`
- `connectome_edge_directional_shine_animation_helpers.ts`
- `connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx`
- `connectome_edge_pulse_particle_animation_and_boundary_clamp_helpers.ts`
- `connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts`
- `connectome_energy_badge_bucketed_glow_and_value_formatter.ts`
- `connectome_node_background_theme_tokens_by_type_and_language.ts`
- `connectome_node_boundary_intersection_geometry_helpers.ts`
- `connectome_system_map_node_edge_manifest.ts`
- `context.py`
- `core_utils.py`
- `doctor.py`
- `doctor_checks.py`
- `doctor_cli_parser_and_run_checker.py`
- `doctor_files.py`
- `doctor_report.py`
- `engine/api/app.py`
- `engine/db/graph_ops.py`
- `engine/graph/health/check_health.py`
- `engine/graph/health/lint_terminology.py`
- `engine/graph/health/test_schema.py`
- `engine/handlers/base.py`
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/api/graphs.py`
- `engine/infrastructure/api/moments.py`
- `engine/infrastructure/api/playthroughs.py`
- `engine/infrastructure/api/sse_broadcast.py`
- `engine/infrastructure/api/tempo.py`
- `engine/infrastructure/canon/canon_holder.py`
- `engine/infrastructure/embeddings/service.py`
- `engine/infrastructure/memory/__init__.py`
- `engine/infrastructure/memory/moment_processor.py`
- `engine/infrastructure/memory/transcript.py`
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/orchestration/narrator.py`
- `engine/infrastructure/orchestration/orchestrator.py`
- `engine/infrastructure/orchestration/speed.py`
- `engine/infrastructure/orchestration/world_runner.py`
- `engine/infrastructure/tempo/health_check.py`
- `engine/infrastructure/tempo/tempo_controller.py`
- `engine/init_db.py`
- `engine/membrane/functions.py`
- `engine/membrane/health_check.py`
- `engine/membrane/provider.py`
- `engine/models/__init__.py`
- `engine/models/base.py`
- `engine/models/links.py`
- `engine/models/nodes.py`
- `engine/moment_graph/__init__.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/moment_graph/traversal.py`
- `engine/moments/__init__.py`
- `engine/physics/attention_split_sink_mass_distribution_mechanism.py`
- `engine/physics/cluster_energy_monitor.py`
- `engine/physics/constants.py`
- `engine/physics/contradiction_pressure_from_negative_polarity_mechanism.py`
- `engine/physics/display_snap_transition_checker.py`
- `engine/physics/graph/connectome_read_cli.py`
- `engine/physics/graph/graph_interface.py`
- `engine/physics/graph/graph_ops.py`
- `engine/physics/graph/graph_ops_events.py`
- `engine/physics/graph/graph_ops_moments.py`
- `engine/physics/graph/graph_ops_read_only_interface.py`
- `engine/physics/graph/graph_ops_types.py`
- `engine/physics/graph/graph_queries.py`
- `engine/physics/graph/graph_queries_moments.py`
- `engine/physics/graph/graph_queries_search.py`
- `engine/physics/graph/graph_query_utils.py`
- `engine/physics/primes_lag_and_half_life_decay_mechanism.py`
- `engine/physics/tick.py`
- `engine/tests/test_cluster_energy_monitor.py`
- `engine/tests/test_e2e_moment_graph.py`
- `engine/tests/test_models.py`
- `engine/tests/test_moment.py`
- `engine/tests/test_moment_graph.py`
- `engine/tests/test_moment_lifecycle.py`
- `engine/tests/test_moments_api.py`
- `engine/tests/test_physics_display_snap.py`
- `engine/tests/test_router_schema_validation.py`
- `engine/tests/test_spec_consistency.py`
- `file_utils.py`
- `flow_event_schema_and_normalization_contract.ts`
- `frontend/app/scenarios/page.tsx`
- `frontend/app/start/page.tsx`
- `frontend/hooks/useGameState.ts`
- `gemini_agent.py`
- `github.py`
- `graph_ops.py`
- `graph_ops_apply.py`
- `graph_ops_events.py`
- `graph_ops_image.py`
- `graph_ops_moments.py`
- `graph_ops_read_only_interface.py`
- `graph_ops_types.py`
- `graph_queries.py`
- `graph_queries_narratives.py`
- `graph_queries_search.py`
- `init_cmd.py`
- `layout.tsx`
- `links.py`
- `lint_terminology.py`
- `manager.py`
- `moment_graph/traversal.py`
- `moment_processor.py`
- `moments.py`
- `narrator.py`
- `narrator/prompt_builder.py`
- `next_step_gate_and_realtime_playback_runtime_engine.ts`
- `ngram.py`
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/core_utils.py`
- `ngram/docs_fix.py`
- `ngram/doctor.py`
- `ngram/doctor_checks.py`
- `ngram/doctor_checks_content.py`
- `ngram/doctor_checks_core.py`
- `ngram/doctor_checks_docs.py`
- `ngram/doctor_checks_metadata.py`
- `ngram/doctor_checks_naming.py`
- `ngram/doctor_checks_prompt_integrity.py`
- `ngram/doctor_checks_quality.py`
- `ngram/doctor_checks_reference.py`
- `ngram/doctor_checks_stub.py`
- `ngram/doctor_checks_sync.py`
- `ngram/doctor_files.py`
- `ngram/doctor_report.py`
- `ngram/doctor_types.py`
- `ngram/github.py`
- `ngram/init_cmd.py`
- `ngram/llms/gemini_agent.py`
- `ngram/llms/tool_helpers.py`
- `ngram/project_map.py`
- `ngram/project_map_html.py`
- `ngram/prompt.py`
- `ngram/refactor.py`
- `ngram/repair.py`
- `ngram/repair_core.py`
- `ngram/repair_escalation_interactive.py`
- `ngram/repair_instructions.py`
- `ngram/repair_instructions_docs.py`
- `ngram/repair_report.py`
- `ngram/repo_overview.py`
- `ngram/repo_overview_formatters.py`
- `ngram/solve_escalations.py`
- `ngram/sync.py`
- `ngram/tui/__init__.py`
- `ngram/tui/app.py`
- `ngram/tui/app_core.py`
- `ngram/tui/app_manager.py`
- `ngram/tui/commands.py`
- `ngram/tui/commands_agent.py`
- `ngram/tui/manager.py`
- `ngram/tui/state.py`
- `ngram/tui/widgets/__init__.py`
- `ngram/tui/widgets/agent_container.py`
- `ngram/tui/widgets/agent_panel.py`
- `ngram/tui/widgets/input_bar.py`
- `ngram/tui/widgets/manager_panel.py`
- `ngram/tui/widgets/status_bar.py`
- `ngram/tui/widgets/suggestions.py`
- `ngram/utils.py`
- `ngram/utils/file_utils.py`
- `ngram/utils/string_utils.py`
- `ngram/utils/validation_utils.py`
- `ngram/validate.py`
- `nodes.py`
- `orchestrator.py`
- `page.tsx`
- `pannable_zoomable_zoned_flow_canvas_renderer.tsx`
- `playthroughs.py`
- `project_map.py`
- `project_map_html.py`
- `prompt.py`
- `repair.py`
- `repair_core.py`
- `repo_overview.py`
- `route.ts`
- `scripts/check_chain_links.py`
- `scripts/check_doc_completeness.py`
- `scripts/check_doc_refs.py`
- `scripts/check_orphans.py`
- `scripts/connectome/health/node_kit_health_check_runner.ts`
- `semantic_edge_components_with_directional_shine_and_pulses.tsx`
- `semantic_proximity_based_character_node_selector.py`
- `snake_case.py`
- `src/analytics/batch_ingest.py`
- `src/analytics/storage/event_store.py`
- `src/analytics/stream_ingest.py`
- `src/analytics/validation/schema_rules.py`
- `src/dashboard/op_metrics.py`
- `src/dashboard/product_metrics.py`
- `sse_broadcast.py`
- `state.py`
- `stream_dialogue.py`
- `string_utils.py`
- `surface.py`
- `sync.py`
- `tensions.py`
- `test_schema.py`
- `tick.py`
- `tools/connectome_doc_bundle_splitter_and_fence_rewriter.py`
- `tools/dialogue/clickables.py`
- `tools/stream_dialogue.py`
- `utils.py`
- `validate.py`
- `views.py`
- `zustand_connectome_state_store_with_atomic_commit_actions.ts`

**Doc refs:**
- `agents/narrator/CLAUDE.md`
- `agents/narrator/CLAUDE_old.md`
- `agents/world_runner/CLAUDE.md`
- `algorithms/ALGORITHM_Physics_Energy_Flow_Sources_Sinks_And_Moment_Dynamics.md`
- `algorithms/ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md`
- `algorithms/ALGORITHM_Physics_Handler_And_Input_Processing_Flows.md`
- `algorithms/ALGORITHM_Physics_Mechanisms.md`
- `algorithms/ALGORITHM_Physics_Speed_Control_And_Display_Filtering.md`
- `algorithms/ALGORITHM_Physics_Tick_Cycle_Gating_Flips_And_Dispatch.md`
- `archive/SYNC_Archive_2024-12.md`
- `archive/SYNC_CLI_Development_State_archive_2025-12.md`
- `archive/SYNC_CLI_State_Archive_2025-12.md`
- `archive/SYNC_TUI_State_Archive_2025-12.md`
- `archive/SYNC_archive_2024-12.md`
- `core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `core/BEHAVIORS_CLI_Command_Effects.md`
- `core/HEALTH_CLI_Command_Test_Coverage.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md`
- `core/PATTERNS_Why_CLI_Over_Copy.md`
- `core/SYNC_CLI_Development_State.md`
- `core/VALIDATION_CLI_Instruction_Invariants.md`
- `data/ARCHITECTURE — Cybernetic Studio.md`
- `data/NGRAM Documentation Chain Pattern (Draft “Marco”).md`
- `docs/SYNC_Project_Repository_Map.md`
- `docs/agents/narrator/ALGORITHM_Scene_Generation.md`
- `docs/agents/narrator/BEHAVIORS_Narrator.md`
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md`
- `docs/agents/narrator/HEALTH_Narrator.md`
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md`
- `docs/agents/narrator/INPUT_REFERENCE.md`
- `docs/agents/narrator/PATTERNS_Narrator.md`
- `docs/agents/narrator/PATTERNS_World_Building.md`
- `docs/agents/narrator/SYNC_Narrator.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12.md`
- `docs/agents/narrator/TEST_Narrator.md`
- `docs/agents/narrator/TOOL_REFERENCE.md`
- `docs/agents/narrator/VALIDATION_Narrator.md`
- `docs/agents/narrator/archive/SYNC_archive_2024-12.md`
- `docs/architecture/cybernetic_studio_architecture/ALGORITHM_Cybernetic_Studio_Process_Flow.md`
- `docs/architecture/cybernetic_studio_architecture/BEHAVIORS_Cybernetic_Studio_System_Behaviors.md`
- `docs/architecture/cybernetic_studio_architecture/HEALTH_Cybernetic_Studio_Health_Checks.md`
- `docs/architecture/cybernetic_studio_architecture/IMPLEMENTATION_Cybernetic_Studio_Code_Structure.md`
- `docs/architecture/cybernetic_studio_architecture/PATTERNS_Cybernetic_Studio_Architecture.md`
- `docs/architecture/cybernetic_studio_architecture/SYNC_Cybernetic_Studio_Architecture_State.md`
- `docs/architecture/cybernetic_studio_architecture/VALIDATION_Cybernetic_Studio_Architectural_Invariants.md`
- `docs/cli/ALGORITHM_CLI_Command_Execution_Logic.md`
- `docs/cli/ALGORITHM_CLI_Logic.md`
- `docs/cli/HEALTH_CLI_Coverage.md`
- `docs/cli/SYNC_CLI_State.md`
- `docs/cli/VALIDATION_CLI_Invariants.md`
- `docs/cli/archive/SYNC_CLI_Development_State_archive_2025-12.md`
- `docs/cli/archive/SYNC_CLI_State_Archive_2025-12.md`
- `docs/cli/archive/SYNC_archive_2024-12.md`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic.md`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `docs/cli/core/BEHAVIORS_CLI_Command_Effects.md`
- `docs/cli/core/HEALTH_CLI_Command_Test_Coverage.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md`
- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`
- `docs/cli/core/SYNC_CLI_Development_State.md`
- `docs/cli/core/VALIDATION_CLI_Instruction_Invariants.md`
- `docs/cli/prompt/ALGORITHM_Prompt_Bootstrap_Prompt_Construction.md`
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`
- `docs/cli/prompt/PATTERNS_Prompt_Command_Workflow_Design.md`
- `docs/cli/prompt/SYNC_Prompt_Command_State.md`
- `docs/connectome/edge_kit/BEHAVIORS_Connectome_Edge_Kit_Readable_Directional_And_Truthful_Link_Effects.md`
- `docs/connectome/edge_kit/HEALTH_Connectome_Edge_Kit_Runtime_Verification_Of_Link_Visibility_And_Semantic_Styling.md`
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md`
- `docs/connectome/edge_kit/PATTERNS_Connectome_Edge_Kit_Color_Coded_Trigger_Typed_Directional_Link_Styling_Patterns.md`
- `docs/connectome/edge_kit/SYNC_Connectome_Edge_Kit_Sync_Current_State.md`
- `docs/connectome/edge_kit/VALIDATION_Connectome_Edge_Kit_Invariants_For_Color_Dash_And_Pulse_Truth.md`
- `docs/connectome/event_model/ALGORITHM_Connectome_Event_Normalization_And_Rendering_Event_Synthesis.md`
- `docs/connectome/flow_canvas/ALGORITHM_Connectome_Flow_Canvas_Layout_Zones_And_Edge_Label_Decluttering.md`
- `docs/connectome/flow_canvas/BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md`
- `docs/connectome/flow_canvas/HEALTH_Connectome_Flow_Canvas_Runtime_Verification_Of_Render_Stability_And_Perf_Budgets.md`
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md`
- `docs/connectome/flow_canvas/PATTERNS_Connectome_Flow_Canvas_Pannable_Zoomable_Zoned_System_Map_Rendering_Patterns.md`
- `docs/connectome/flow_canvas/SYNC_Connectome_Flow_Canvas_Sync_Current_State.md`
- `docs/connectome/flow_canvas/VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md`
- `docs/connectome/graphs/OBJECTIFS_Connectome_Graphs.md`
- `docs/connectome/graphs/PATTERNS_Connectome_Graphs.md`
- `docs/connectome/graphs/SYNC_Connectome_Graphs_Sync_Current_State.md`
- `docs/connectome/health/HEALTH_Connectome_Live_Signals.md`
- `docs/connectome/log_panel/ALGORITHM_Connectome_Log_Panel_Log_Rendering_Duration_Coloring_And_Export.md`
- `docs/connectome/log_panel/BEHAVIORS_Connectome_Log_Panel_Step_Clarity_And_Copyable_Audit_Trail_Effects.md`
- `docs/connectome/log_panel/HEALTH_Connectome_Log_Panel_Runtime_Verification_Of_Log_Truth_And_Export_Integrity.md`
- `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md`
- `docs/connectome/log_panel/PATTERNS_Connectome_Log_Panel_Unified_Explain_And_Copyable_Event_Ledger_View_Patterns.md`
- `docs/connectome/log_panel/SYNC_Connectome_Log_Panel_Sync_Current_State.md`
- `docs/connectome/log_panel/VALIDATION_Connectome_Log_Panel_Invariants_For_Truthful_Durations_And_Stable_Export.md`
- `docs/connectome/node_kit/ALGORITHM_Connectome_Node_Kit_Node_Rendering_Spec_And_Energy_Glow_Mapping.md`
- `docs/connectome/node_kit/BEHAVIORS_Connectome_Node_Kit_Visible_Clarity_And_Trust_Effects.md`
- `docs/connectome/node_kit/HEALTH_Connectome_Node_Kit_Runtime_Verification_Of_Node_State_And_Visual_Signal_Truth.md`
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`
- `docs/connectome/node_kit/PATTERNS_Connectome_Node_Kit_Typed_Language_Coded_Energy_Aware_Node_Rendering_Patterns.md`
- `docs/connectome/node_kit/SYNC_Connectome_Node_Kit_Sync_Current_State.md`
- `docs/connectome/node_kit/VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md`
- `docs/connectome/page_shell/PATTERNS_Connectome_Page_Shell_Route_Composition_And_User_Control_Surface_Patterns.md`
- `docs/connectome/runtime_engine/ALGORITHM_Connectome_Runtime_Engine_Step_Release_And_Realtime_Scheduling.md`
- `docs/connectome/runtime_engine/BEHAVIORS_Connectome_Runtime_Engine_User_Controlled_Traversal_Effects.md`
- `docs/connectome/runtime_engine/HEALTH_Connectome_Runtime_Engine_Runtime_Verification_Of_Pacing_And_Order.md`
- `docs/connectome/runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md`
- `docs/connectome/runtime_engine/PATTERNS_Connectome_Runtime_Engine_Stepper_And_Realtime_Traversal_Control_Patterns.md`
- `docs/connectome/runtime_engine/SYNC_Connectome_Runtime_Engine_Sync_Current_State.md`
- `docs/connectome/runtime_engine/VALIDATION_Connectome_Runtime_Engine_Invariants_For_Stepper_And_Realtime.md`
- `docs/connectome/state_store/ALGORITHM_Connectome_State_Store_Atomic_Commits_For_Step_Releases_And_Realtime.md`
- `docs/connectome/state_store/BEHAVIORS_Connectome_State_Store_Observable_State_Consistency_Effects.md`
- `docs/connectome/state_store/HEALTH_Connectome_State_Store_Runtime_Verification_Of_Ledger_And_Timer_Correctness.md`
- `docs/connectome/state_store/IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md`
- `docs/connectome/state_store/PATTERNS_Connectome_State_Store_Single_Source_Of_Truth_For_Events_Focus_And_Timers.md`
- `docs/connectome/state_store/SYNC_Connectome_State_Store_Sync_Current_State.md`
- `docs/connectome/state_store/VALIDATION_Connectome_State_Store_Invariants_For_Ledger_Ordering_And_Focus.md`
- `docs/core_utils/ALGORITHM_Core_Utils_Template_Path_And_Module_Discovery.md`
- `docs/core_utils/ALGORITHM_Template_Path_Resolution_And_Doc_Discovery.md`
- `docs/core_utils/PATTERNS_Core_Utils_Functions.md`
- `docs/engine/membrane/BEHAVIORS_Membrane_Modulation.md`
- `docs/engine/membrane/PATTERNS_Membrane_Scoping.md`
- `docs/engine/membrane/PATTERN_Membrane_Modulation.md`
- `docs/engine/membrane/SYNC_Membrane_Modulation.md`
- `docs/engine/models/BEHAVIORS_Models.md`
- `docs/engine/models/HEALTH_Models.md`
- `docs/engine/models/IMPLEMENTATION_Models.md`
- `docs/engine/models/PATTERNS_Models.md`
- `docs/engine/models/SYNC_Models.md`
- `docs/engine/models/VALIDATION_Models.md`
- `docs/engine/moments/PATTERNS_Moments.md`
- `docs/engine/moments/SYNC_Moments.md`
- `docs/frontend/app_shell/OBJECTIFS_App_Shell.md`
- `docs/frontend/app_shell/PATTERNS_App_Shell.md`
- `docs/frontend/app_shell/SYNC_App_Shell_State.md`
- `docs/infrastructure/api/ALGORITHM_Api.md`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md`
- `docs/infrastructure/api/API_Graph_Management.md`
- `docs/infrastructure/api/BEHAVIORS_Api.md`
- `docs/infrastructure/api/IMPLEMENTATION_Api.md`
- `docs/infrastructure/api/PATTERNS_Api.md`
- `docs/infrastructure/api/SYNC_Api.md`
- `docs/infrastructure/api/TEST_Api.md`
- `docs/infrastructure/api/VALIDATION_Api.md`
- `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`
- `docs/infrastructure/canon/PATTERNS_Canon.md`
- `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md`
- `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`
- `docs/infrastructure/tempo/PATTERNS_Tempo.md`
- `docs/llm_agents/ALGORITHM_Gemini_Stream_Flow.md`
- `docs/llm_agents/BEHAVIORS_Gemini_Agent_Output.md`
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md`
- `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`
- `docs/llm_agents/SYNC_LLM_Agents_State.md`
- `docs/llm_agents/SYNC_LLM_Agents_State_archive_2025-12.md`
- `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md`
- `docs/ngram_cli_core/OBJECTIFS_ngram_cli_core.md`
- `docs/ngram_cli_core/PATTERNS_ngram_cli_core.md`
- `docs/ngram_cli_core/SYNC_ngram_cli_core.md`
- `docs/physics/ALGORITHM_Physics.md`
- `docs/physics/BEHAVIORS_Physics.md`
- `docs/physics/IMPLEMENTATION_Physics.md`
- `docs/physics/PATTERNS_Physics.md`
- `docs/physics/SYNC_Physics.md`
- `docs/physics/SYNC_Physics_archive_2025-12.md`
- `docs/physics/TEST_Physics.md`
- `docs/physics/VALIDATION_Physics.md`
- `docs/physics/algorithms/ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md`
- `docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md`
- `docs/physics/archive/IMPLEMENTATION_Physics_archive_2025-12.md`
- `docs/physics/archive/SYNC_Physics_archive_2025-12.md`
- `docs/physics/archive/SYNC_archive_2024-12.md`
- `docs/physics/attention/PATTERNS_Attention_Energy_Split.md`
- `docs/physics/attention/PATTERNS_Interrupt_By_Focus_Reconfiguration.md`
- `docs/physics/attention/VALIDATION_Attention_Split_And_Interrupts.md`
- `docs/physics/graph/ALGORITHM_Energy_Flow.md`
- `docs/physics/graph/ALGORITHM_Weight.md`
- `docs/physics/graph/BEHAVIORS_Graph.md`
- `docs/physics/graph/PATTERNS_Graph.md`
- `docs/physics/graph/SYNC_Graph.md`
- `docs/physics/graph/SYNC_Graph_archive_2025-12.md`
- `docs/physics/graph/VALIDATION_Living_Graph.md`
- `docs/physics/mechanisms/MECHANISMS_Attention_Energy_Split.md`
- `docs/physics/mechanisms/MECHANISMS_Contradiction_Pressure.md`
- `docs/physics/mechanisms/MECHANISMS_Primes_Lag_Decay.md`
- `docs/protocol/ALGORITHM/ALGORITHM_Protocol_Process_Flow.md`
- `docs/protocol/BEHAVIORS_Observable_Protocol_Effects.md`
- `docs/protocol/HEALTH_Protocol_Verification.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_File_Structure.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_Overview.md`
- `docs/protocol/PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md`
- `docs/protocol/SYNC_Protocol_Current_State.md`
- `docs/protocol/archive/SYNC_Archive_2024-12.md`
- `docs/protocol/doctor/IMPLEMENTATION_Project_Health_Doctor.md`
- `docs/protocol/doctor/PATTERNS_Project_Health_Doctor.md`
- `docs/protocol/doctor/SYNC_Project_Health_Doctor.md`
- `docs/schema/SCHEMA.md`
- `docs/schema/SCHEMA/SCHEMA_Links.md`
- `docs/schema/SCHEMA/SCHEMA_Nodes.md`
- `docs/schema/SCHEMA_Moments.md`
- `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Overview.md`
- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`
- `docs/schema/models/SYNC_Schema_Models.md`
- `docs/tools/ALGORITHM_Tools.md`
- `docs/tools/BEHAVIORS_Tools.md`
- `docs/tools/HEALTH_Tools.md`
- `docs/tools/IMPLEMENTATION_Tools.md`
- `docs/tools/OBJECTIFS_Tools_Goals.md`
- `docs/tools/PATTERNS_Tools.md`
- `docs/tools/SYNC_Tools.md`
- `docs/tools/VALIDATION_Tools.md`
- `docs/tui/ALGORITHM_TUI_Widget_Interaction_Flow.md`
- `docs/tui/BEHAVIORS_TUI_Interactions.md`
- `docs/tui/HEALTH_TUI_Coverage.md`
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md`
- `docs/tui/PATTERNS_TUI_Design.md`
- `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md`
- `docs/tui/SYNC_TUI_State.md`
- `docs/tui/archive/SYNC_archive_2024-12.md`
- `doctor/ALGORITHM_Project_Health_Doctor.md`
- `doctor/BEHAVIORS_Project_Health_Doctor.md`
- `doctor/HEALTH_Project_Health_Doctor.md`
- `doctor/PATTERNS_Project_Health_Doctor.md`
- `doctor/SYNC_Project_Health_Doctor.md`
- `doctor/VALIDATION_Project_Health_Doctor.md`
- `event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md`
- `features/BEHAVIORS_Agent_Trace_Logging.md`
- `features/PATTERNS_Agent_Trace_Logging.md`
- `features/SYNC_Agent_Trace_Logging.md`
- `implementation/IMPLEMENTATION_Physics_Architecture.md`
- `implementation/IMPLEMENTATION_Physics_Code_Structure.md`
- `implementation/IMPLEMENTATION_Physics_Dataflow.md`
- `implementation/IMPLEMENTATION_Physics_Runtime.md`
- `..ngram/state/SYNC_Project_Health.md`
- `..ngram/state/SYNC_Prompt_Command_State.md`
- `prompt/ALGORITHM_Prompt_Bootstrap_Prompt_Construction.md`
- `prompt/BEHAVIORS_Prompt_Command_Output_and_Flow.md`
- `prompt/HEALTH_Prompt_Runtime_Verification.md`
- `prompt/IMPLEMENTATION_Prompt_Code_Architecture.md`
- `prompt/PATTERNS_Prompt_Command_Workflow_Design.md`
- `prompt/SYNC_Prompt_Command_State.md`
- `prompt/VALIDATION_Prompt_Bootstrap_Invariants.md`
- `runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md`
- `state/SYNC_Project_State.md`
- `state_store/IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md`
- `templates/CLAUDE_ADDITION.md`
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`
- `templates/ngram/PRINCIPLES.md`
- `templates/ngram/PROTOCOL.md`
- `templates/ngram/agents/manager/CLAUDE.md`
- `tools/HEALTH_Tools.md`
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # Repository Map: ngram

**Code refs:**
- `api/connectome/graph/route.ts`
- `api/connectome/graphs/route.ts`
- `api/connectome/search/route.ts`
- `api/sse/route.ts`
- `connectome/components/connectome_health_panel.tsx`
- `connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts`
- `connectome/components/connectome_log_export_buttons_using_state_store_serializers.tsx`
- `connectome/components/connectome_log_trigger_and_calltype_badge_color_tokens.ts`
- `connectome/components/connectome_page_shell_route_layout_and_control_surface.tsx`
- `connectome/components/deterministic_zone_and_node_layout_computation_helpers.ts`
- `connectome/components/edge_kit/connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx`
- `connectome/components/edge_kit/connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts`
- `connectome/components/edge_kit/connectome_node_boundary_intersection_geometry_helpers.ts`
- `connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.tsx`
- `connectome/components/edge_label_declutter_and_visibility_policy_helpers.ts`
- `connectome/components/node_kit/connectome_energy_badge_bucketed_glow_and_value_formatter.tsx`
- `connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts`
- `connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`
- `connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.tsx`
- `connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.tsx`
- `connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.tsx`
- `connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.tsx`
- `connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`
- `connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`

**Doc refs:**
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md`
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md`
- `docs/connectome/graphs/OBJECTIFS_Connectome_Graphs.md`
- `docs/connectome/health/HEALTH_Connectome_Live_Signals.md`
- `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md`
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`
- `docs/connectome/page_shell/PATTERNS_Connectome_Page_Shell_Route_Composition_And_User_Control_Surface_Patterns.md`

**Sections:**
- # Repository Map: ngram/app
- ## Statistics
- ## File Tree
- ## File Details

**Code refs:**
- `__init__.py`
- `agent_cli.py`
- `app.py`
- `base.py`
- `check_health.py`
- `cli.py`
- `commands.py`
- `context.py`
- `core_utils.py`
- `doctor.py`
- `doctor_checks.py`
- `doctor_cli_parser_and_run_checker.py`
- `doctor_files.py`
- `doctor_report.py`
- `engine/api/app.py`
- `engine/db/graph_ops.py`
- `engine/graph/health/check_health.py`
- `engine/graph/health/lint_terminology.py`
- `engine/graph/health/test_schema.py`
- `engine/handlers/base.py`
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/api/moments.py`
- `engine/infrastructure/api/playthroughs.py`
- `engine/infrastructure/api/sse_broadcast.py`
- `engine/infrastructure/api/tempo.py`
- `engine/infrastructure/canon/canon_holder.py`
- `engine/infrastructure/embeddings/service.py`
- `engine/infrastructure/memory/__init__.py`
- `engine/infrastructure/memory/moment_processor.py`
- `engine/infrastructure/memory/transcript.py`
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/orchestration/narrator.py`
- `engine/infrastructure/orchestration/orchestrator.py`
- `engine/infrastructure/orchestration/speed.py`
- `engine/infrastructure/orchestration/world_runner.py`
- `engine/init_db.py`
- `engine/models/__init__.py`
- `engine/models/base.py`
- `engine/models/links.py`
- `engine/models/nodes.py`
- `engine/moment_graph/__init__.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/moment_graph/traversal.py`
- `engine/moments/__init__.py`
- `engine/physics/constants.py`
- `engine/physics/graph/graph_ops.py`
- `engine/physics/graph/graph_ops_events.py`
- `engine/physics/graph/graph_ops_moments.py`
- `engine/physics/graph/graph_ops_types.py`
- `engine/physics/graph/graph_queries.py`
- `engine/physics/graph/graph_queries_moments.py`
- `engine/physics/graph/graph_queries_search.py`
- `engine/physics/tick.py`
- `engine/tests/test_e2e_moment_graph.py`
- `engine/tests/test_models.py`
- `engine/tests/test_moment.py`
- `engine/tests/test_moment_graph.py`
- `engine/tests/test_moment_lifecycle.py`
- `engine/tests/test_moments_api.py`
- `engine/tests/test_spec_consistency.py`
- `file_utils.py`
- `frontend/app/scenarios/page.tsx`
- `frontend/app/start/page.tsx`
- `frontend/hooks/useGameState.ts`
- `gemini_agent.py`
- `github.py`
- `graph_ops.py`
- `graph_ops_apply.py`
- `graph_ops_events.py`
- `graph_ops_image.py`
- `graph_ops_types.py`
- `graph_queries.py`
- `graph_queries_narratives.py`
- `graph_queries_search.py`
- `init_cmd.py`
- `links.py`
- `lint_terminology.py`
- `manager.py`
- `moment_processor.py`
- `moments.py`
- `narrator.py`
- `ngram.py`
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/core_utils.py`
- `ngram/doctor.py`
- `ngram/doctor_checks.py`
- `ngram/doctor_checks_content.py`
- `ngram/doctor_checks_core.py`
- `ngram/doctor_checks_docs.py`
- `ngram/doctor_checks_metadata.py`
- `ngram/doctor_checks_naming.py`
- `ngram/doctor_checks_prompt_integrity.py`
- `ngram/doctor_checks_quality.py`
- `ngram/doctor_checks_reference.py`
- `ngram/doctor_checks_stub.py`
- `ngram/doctor_checks_sync.py`
- `ngram/doctor_files.py`
- `ngram/doctor_report.py`
- `ngram/doctor_types.py`
- `ngram/github.py`
- `ngram/init_cmd.py`
- `ngram/llms/gemini_agent.py`
- `ngram/project_map.py`
- `ngram/project_map_html.py`
- `ngram/prompt.py`
- `ngram/refactor.py`
- `ngram/repair.py`
- `ngram/repair_core.py`
- `ngram/repair_escalation_interactive.py`
- `ngram/repair_instructions.py`
- `ngram/repair_instructions_docs.py`
- `ngram/repair_report.py`
- `ngram/repo_overview.py`
- `ngram/repo_overview_formatters.py`
- `ngram/solve_escalations.py`
- `ngram/sync.py`
- `ngram/tui/__init__.py`
- `ngram/tui/app.py`
- `ngram/tui/app_core.py`
- `ngram/tui/app_manager.py`
- `ngram/tui/commands.py`
- `ngram/tui/commands_agent.py`
- `ngram/tui/manager.py`
- `ngram/tui/state.py`
- `ngram/tui/widgets/__init__.py`
- `ngram/tui/widgets/agent_container.py`
- `ngram/tui/widgets/agent_panel.py`
- `ngram/tui/widgets/input_bar.py`
- `ngram/tui/widgets/manager_panel.py`
- `ngram/tui/widgets/status_bar.py`
- `ngram/tui/widgets/suggestions.py`
- `ngram/utils.py`
- `ngram/utils/file_utils.py`
- `ngram/utils/string_utils.py`
- `ngram/utils/validation_utils.py`
- `ngram/validate.py`
- `nodes.py`
- `orchestrator.py`
- `playthroughs.py`
- `project_map.py`
- `project_map_html.py`
- `prompt.py`
- `repair.py`
- `repair_core.py`
- `repo_overview.py`
- `scripts/check_chain_links.py`
- `scripts/check_doc_completeness.py`
- `scripts/check_doc_refs.py`
- `scripts/check_orphans.py`
- `semantic_proximity_based_character_node_selector.py`
- `snake_case.py`
- `src/analytics/batch_ingest.py`
- `src/analytics/storage/event_store.py`
- `src/analytics/stream_ingest.py`
- `src/analytics/validation/schema_rules.py`
- `src/dashboard/op_metrics.py`
- `src/dashboard/product_metrics.py`
- `sse_broadcast.py`
- `state.py`
- `stream_dialogue.py`
- `string_utils.py`
- `sync.py`
- `tensions.py`
- `test_schema.py`
- `tick.py`
- `tools/stream_dialogue.py`
- `utils.py`
- `validate.py`
- `views.py`

**Doc refs:**
- `agents/narrator/CLAUDE.md`
- `agents/narrator/CLAUDE_old.md`
- `agents/world_runner/CLAUDE.md`
- `archive/SYNC_Archive_2024-12.md`
- `archive/SYNC_CLI_Development_State_archive_2025-12.md`
- `archive/SYNC_CLI_State_Archive_2025-12.md`
- `archive/SYNC_TUI_State_Archive_2025-12.md`
- `archive/SYNC_archive_2024-12.md`
- `core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `core/BEHAVIORS_CLI_Command_Effects.md`
- `core/HEALTH_CLI_Command_Test_Coverage.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md`
- `core/PATTERNS_Why_CLI_Over_Copy.md`
- `core/SYNC_CLI_Development_State.md`
- `core/VALIDATION_CLI_Instruction_Invariants.md`
- `data/ARCHITECTURE — Cybernetic Studio.md`
- `data/NGRAM Documentation Chain Pattern (Draft “Marco”).md`
- `docs/SYNC_Project_Repository_Map.md`
- `docs/agents/narrator/ALGORITHM_Scene_Generation.md`
- `docs/agents/narrator/BEHAVIORS_Narrator.md`
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md`
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md`
- `docs/agents/narrator/INPUT_REFERENCE.md`
- `docs/agents/narrator/PATTERNS_Narrator.md`
- `docs/agents/narrator/PATTERNS_World_Building.md`
- `docs/agents/narrator/SYNC_Narrator.md`
- `docs/agents/narrator/TEST_Narrator.md`
- `docs/agents/narrator/TOOL_REFERENCE.md`
- `docs/agents/narrator/VALIDATION_Narrator.md`
- `docs/agents/narrator/archive/SYNC_archive_2024-12.md`
- `docs/architecture/cybernetic_studio_architecture/ALGORITHM_Cybernetic_Studio_Process_Flow.md`
- `docs/architecture/cybernetic_studio_architecture/BEHAVIORS_Cybernetic_Studio_System_Behaviors.md`
- `docs/architecture/cybernetic_studio_architecture/HEALTH_Cybernetic_Studio_Health_Checks.md`
- `docs/architecture/cybernetic_studio_architecture/IMPLEMENTATION_Cybernetic_Studio_Code_Structure.md`
- `docs/architecture/cybernetic_studio_architecture/PATTERNS_Cybernetic_Studio_Architecture.md`
- `docs/architecture/cybernetic_studio_architecture/SYNC_Cybernetic_Studio_Architecture_State.md`
- `docs/architecture/cybernetic_studio_architecture/VALIDATION_Cybernetic_Studio_Architectural_Invariants.md`
- `docs/cli/ALGORITHM_CLI_Command_Execution_Logic.md`
- `docs/cli/ALGORITHM_CLI_Logic.md`
- `docs/cli/HEALTH_CLI_Coverage.md`
- `docs/cli/SYNC_CLI_State.md`
- `docs/cli/VALIDATION_CLI_Invariants.md`
- `docs/cli/archive/SYNC_CLI_Development_State_archive_2025-12.md`
- `docs/cli/archive/SYNC_CLI_State_Archive_2025-12.md`
- `docs/cli/archive/SYNC_archive_2024-12.md`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic.md`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `docs/cli/core/BEHAVIORS_CLI_Command_Effects.md`
- `docs/cli/core/HEALTH_CLI_Command_Test_Coverage.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md`
- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`
- `docs/cli/core/SYNC_CLI_Development_State.md`
- `docs/cli/core/VALIDATION_CLI_Instruction_Invariants.md`
- `docs/cli/prompt/ALGORITHM_Prompt_Bootstrap_Prompt_Construction.md`
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`
- `docs/cli/prompt/PATTERNS_Prompt_Command_Workflow_Design.md`
- `docs/cli/prompt/SYNC_Prompt_Command_State.md`
- `docs/core_utils/ALGORITHM_Core_Utils_Template_Path_And_Module_Discovery.md`
- `docs/core_utils/ALGORITHM_Template_Path_Resolution_And_Doc_Discovery.md`
- `docs/core_utils/PATTERNS_Core_Utils_Functions.md`
- `docs/engine/models/PATTERNS_Models.md`
- `docs/engine/models/VALIDATION_Models.md`
- `docs/engine/moments/PATTERNS_Moments.md`
- `docs/engine/moments/SYNC_Moments.md`
- `docs/infrastructure/api/ALGORITHM_Api.md`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md`
- `docs/infrastructure/api/BEHAVIORS_Api.md`
- `docs/infrastructure/api/IMPLEMENTATION_Api.md`
- `docs/infrastructure/api/PATTERNS_Api.md`
- `docs/infrastructure/api/SYNC_Api.md`
- `docs/infrastructure/api/TEST_Api.md`
- `docs/infrastructure/api/VALIDATION_Api.md`
- `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`
- `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`
- `docs/llm_agents/ALGORITHM_Gemini_Stream_Flow.md`
- `docs/llm_agents/BEHAVIORS_Gemini_Agent_Output.md`
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md`
- `docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md`
- `docs/llm_agents/SYNC_LLM_Agents_State.md`
- `docs/llm_agents/VALIDATION_Gemini_Agent_Invariants.md`
- `docs/physics/ALGORITHM_Physics.md`
- `docs/physics/BEHAVIORS_Physics.md`
- `docs/physics/IMPLEMENTATION_Physics.md`
- `docs/physics/PATTERNS_Physics.md`
- `docs/physics/SYNC_Physics.md`
- `docs/physics/SYNC_Physics_archive_2025-12.md`
- `docs/physics/TEST_Physics.md`
- `docs/physics/VALIDATION_Physics.md`
- `docs/physics/graph/ALGORITHM_Energy_Flow.md`
- `docs/physics/graph/ALGORITHM_Weight.md`
- `docs/physics/graph/BEHAVIORS_Graph.md`
- `docs/physics/graph/PATTERNS_Graph.md`
- `docs/physics/graph/SYNC_Graph.md`
- `docs/physics/graph/SYNC_Graph_archive_2025-12.md`
- `docs/physics/graph/VALIDATION_Living_Graph.md`
- `docs/protocol/ALGORITHM/ALGORITHM_Protocol_Process_Flow.md`
- `docs/protocol/BEHAVIORS_Observable_Protocol_Effects.md`
- `docs/protocol/HEALTH_Protocol_Verification.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_File_Structure.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_Overview.md`
- `docs/protocol/PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md`
- `docs/protocol/SYNC_Protocol_Current_State.md`
- `docs/protocol/archive/SYNC_Archive_2024-12.md`
- `docs/protocol/doctor/IMPLEMENTATION_Project_Health_Doctor.md`
- `docs/protocol/doctor/PATTERNS_Project_Health_Doctor.md`
- `docs/protocol/doctor/SYNC_Project_Health_Doctor.md`
- `docs/schema/SCHEMA.md`
- `docs/schema/SCHEMA/SCHEMA_Links.md`
- `docs/schema/SCHEMA/SCHEMA_Nodes.md`
- `docs/schema/SCHEMA_Moments.md`
- `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Overview.md`
- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`
- `docs/schema/models/SYNC_Schema_Models.md`
- `docs/tui/BEHAVIORS_TUI_Interactions.md`
- `docs/tui/HEALTH_TUI_Coverage.md`
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md`
- `docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md`
- `docs/tui/PATTERNS_TUI_Design.md`
- `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md`
- `docs/tui/SYNC_TUI_State.md`
- `docs/tui/archive/SYNC_archive_2024-12.md`
- `doctor/ALGORITHM_Project_Health_Doctor.md`
- `doctor/BEHAVIORS_Project_Health_Doctor.md`
- `doctor/HEALTH_Project_Health_Doctor.md`
- `doctor/PATTERNS_Project_Health_Doctor.md`
- `doctor/SYNC_Project_Health_Doctor.md`
- `doctor/VALIDATION_Project_Health_Doctor.md`
- `features/BEHAVIORS_Agent_Trace_Logging.md`
- `features/PATTERNS_Agent_Trace_Logging.md`
- `features/SYNC_Agent_Trace_Logging.md`
- `..ngram/state/SYNC_Project_Health.md`
- `..ngram/state/SYNC_Prompt_Command_State.md`
- `prompt/ALGORITHM_Prompt_Bootstrap_Prompt_Construction.md`
- `prompt/BEHAVIORS_Prompt_Command_Output_and_Flow.md`
- `prompt/HEALTH_Prompt_Runtime_Verification.md`
- `prompt/IMPLEMENTATION_Prompt_Code_Architecture.md`
- `prompt/PATTERNS_Prompt_Command_Workflow_Design.md`
- `prompt/SYNC_Prompt_Command_State.md`
- `prompt/VALIDATION_Prompt_Bootstrap_Invariants.md`
- `state/SYNC_Project_State.md`
- `templates/CLAUDE_ADDITION.md`
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`
- `templates/ngram/PRINCIPLES.md`
- `templates/ngram/PROTOCOL.md`
- `templates/ngram/agents/manager/CLAUDE.md`
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # Repository Map: ngram/docs

**Code refs:**
- `agent_cli.py`
- `context.py`
- `core_utils.py`
- `doctor.py`
- `doctor_files.py`
- `github.py`
- `init_cmd.py`
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/core_utils.py`
- `ngram/doctor.py`
- `ngram/doctor_checks.py`
- `ngram/doctor_checks_content.py`
- `ngram/doctor_checks_docs.py`
- `ngram/doctor_checks_quality.py`
- `ngram/doctor_checks_sync.py`
- `ngram/doctor_files.py`
- `ngram/doctor_report.py`
- `ngram/doctor_types.py`
- `ngram/github.py`
- `ngram/init_cmd.py`
- `ngram/project_map.py`
- `ngram/project_map_html.py`
- `ngram/prompt.py`
- `ngram/repair.py`
- `ngram/repair_core.py`
- `ngram/repair_escalation_interactive.py`
- `ngram/repair_instructions.py`
- `ngram/repair_instructions_docs.py`
- `ngram/repair_report.py`
- `ngram/repo_overview.py`
- `ngram/repo_overview_formatters.py`
- `ngram/solve_escalations.py`
- `ngram/sync.py`
- `ngram/validate.py`
- `project_map.py`
- `prompt.py`
- `repair.py`
- `sync.py`
- `validate.py`

**Doc refs:**
- `archive/SYNC_CLI_Development_State_archive_2025-12.md`
- `archive/SYNC_CLI_State_Archive_2025-12.md`
- `core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `core/BEHAVIORS_CLI_Command_Effects.md`
- `core/HEALTH_CLI_Command_Test_Coverage.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md`
- `core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md`
- `core/PATTERNS_Why_CLI_Over_Copy.md`
- `core/SYNC_CLI_Development_State.md`
- `core/VALIDATION_CLI_Instruction_Invariants.md`
- `data/NGRAM Documentation Chain Pattern (Draft “Marco”).md`
- `docs/cli/SYNC_CLI_State.md`
- `docs/cli/archive/SYNC_CLI_Development_State_archive_2025-12.md`
- `docs/cli/archive/SYNC_CLI_State_Archive_2025-12.md`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `docs/cli/core/BEHAVIORS_CLI_Command_Effects.md`
- `docs/cli/core/HEALTH_CLI_Command_Test_Coverage.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`
- `docs/cli/core/SYNC_CLI_Development_State.md`
- `docs/cli/core/VALIDATION_CLI_Instruction_Invariants.md`
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`
- `docs/cli/prompt/PATTERNS_Prompt_Command_Workflow_Design.md`
- `docs/cli/prompt/SYNC_Prompt_Command_State.md`
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- `docs/protocol/HEALTH_Protocol_Verification.md`
- `docs/protocol/doctor/PATTERNS_Project_Health_Doctor.md`
- `docs/protocol/doctor/SYNC_Project_Health_Doctor.md`
- `docs/tui/HEALTH_TUI_Coverage.md`
- `prompt/ALGORITHM_Prompt_Bootstrap_Prompt_Construction.md`
- `prompt/BEHAVIORS_Prompt_Command_Output_and_Flow.md`
- `prompt/HEALTH_Prompt_Runtime_Verification.md`
- `prompt/IMPLEMENTATION_Prompt_Code_Architecture.md`
- `prompt/PATTERNS_Prompt_Command_Workflow_Design.md`
- `prompt/SYNC_Prompt_Command_State.md`
- `prompt/VALIDATION_Prompt_Bootstrap_Invariants.md`
- `state/SYNC_Project_State.md`
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`

**Sections:**
- # Repository Map: ngram/docs/cli
- ## Statistics
- ## File Tree
- ## File Details

**Code refs:**
- `doctor.py`
- `doctor_checks.py`
- `doctor_report.py`
- `ngram/cli.py`
- `ngram/doctor.py`
- `ngram/prompt.py`
- `ngram/validate.py`
- `scripts/check_chain_links.py`
- `scripts/check_doc_completeness.py`
- `scripts/check_doc_refs.py`
- `scripts/check_orphans.py`

**Doc refs:**
- `archive/SYNC_Archive_2024-12.md`
- `archive/SYNC_archive_2024-12.md`
- `docs/cli/HEALTH_CLI_Coverage.md`
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`
- `docs/protocol/ALGORITHM/ALGORITHM_Protocol_Process_Flow.md`
- `docs/protocol/BEHAVIORS_Observable_Protocol_Effects.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_File_Structure.md`
- `docs/protocol/PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md`
- `docs/protocol/SYNC_Protocol_Current_State.md`
- `docs/tui/HEALTH_TUI_Coverage.md`
- `doctor/ALGORITHM_Project_Health_Doctor.md`
- `doctor/BEHAVIORS_Project_Health_Doctor.md`
- `doctor/HEALTH_Project_Health_Doctor.md`
- `doctor/PATTERNS_Project_Health_Doctor.md`
- `doctor/SYNC_Project_Health_Doctor.md`
- `doctor/VALIDATION_Project_Health_Doctor.md`
- `features/BEHAVIORS_Agent_Trace_Logging.md`
- `features/PATTERNS_Agent_Trace_Logging.md`
- `features/SYNC_Agent_Trace_Logging.md`
- `templates/CLAUDE_ADDITION.md`
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`
- `templates/ngram/PRINCIPLES.md`
- `templates/ngram/PROTOCOL.md`
- `templates/ngram/agents/manager/CLAUDE.md`

**Sections:**
- # Repository Map: ngram/docs/protocol
- ## Statistics
- ## File Tree
- ## File Details
