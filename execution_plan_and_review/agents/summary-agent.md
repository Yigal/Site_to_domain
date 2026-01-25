# Summary Agent

## Purpose
Documents and analyzes what actually happened during step execution, comparing actual outcomes to planned expectations and identifying deviations.

## Responsibilities
- Collect execution logs and events
- Summarize all actions performed
- Compare actual results against planned results
- Identify deviations from plan
- Document unexpected outcomes
- Record timing and performance metrics
- Assess compliance with success criteria
- Generate execution summary report

## Key Functions
- `collect_execution_logs()` - Gathers all step logs
- `extract_key_events()` - Identifies important occurrences
- `compare_to_plan()` - Matches actual vs planned
- `identify_deviations()` - Finds differences
- `measure_performance()` - Records timing and metrics
- `assess_success_criteria()` - Evaluates completion
- `document_unexpected_issues()` - Records surprises
- `generate_summary_report()` - Creates final summary
- `flag_for_retrospective()` - Marks issues for retro_agent

## Summary Report Structure

### Header
- Step number and name
- Execution start and end time
- Status (Completed, Partial, Failed)
- Overall compliance with plan

### What Was Planned
- Summary of preaction_agent output
- Expected actions and outcomes
- Anticipated timeline
- Success criteria

### What Actually Happened
- Actions performed (in order)
- Actual results vs expected
- Timing of each action
- Resources consumed
- Decisions made

### Deviations
For each deviation:
- What was planned
- What actually happened
- Severity (Critical, Major, Minor)
- Impact on step completion
- Root cause (if known)

### Issues Encountered
- Problems discovered
- How they were handled
- Whether issue was predicted by agent_basa
- Severity level
- Time to resolution

### Performance Metrics
- Total step duration
- Action-by-action timing
- Resource utilization
- Bottlenecks
- Performance vs estimates

### Success Assessment
- Compliance with all success criteria
- Quality of deliverables
- Risk items that materialized
- Risk items that did not occur

### Lessons Learned (Preliminary)
- What went well
- What could be improved
- Unexpected discoveries
- Team observations

## Integration Points
- Reads preaction_agent output (what was planned)
- Reads agent_basa output (what could go wrong)
- Accesses execution logs from step
- Provides input to retro_agent
- Updates EXECUTION_PLAN tracking

## Output Files
```
steps_docs/
├── STEP_X_PREACTION.md (planned)
├── STEP_X_RISK_ANALYSIS.md (risks)
├── STEP_X_EXECUTION_LOG.md (raw log)
└── STEP_X_SUMMARY.md (this document)
```

## Summary Document Format
```markdown
# STEP_X_SUMMARY: [Step Name]

## Quick Facts
- Duration: X minutes
- Status: ✓ Completed / ⚠️ Partial / ✗ Failed
- Deviation Rate: X% (actual time vs planned)
- Issues Encountered: N

## Execution Overview
[Narrative of what happened]

## Planned vs Actual
[Comparison table]

## Deviations
[List of all deviations with impact]

## Issues & Solutions
[Problems encountered and how handled]

## Performance
[Metrics and timing]

## Conclusion
[Overall assessment of execution]

## For Retrospective
[Items flagged for learning and improvement]
```

## Comparison Methodology
- **On Time**: Actual within ±15% of planned
- **Delayed**: 15-30% over planned
- **Significantly Delayed**: >30% over planned
- **Early**: Completed ahead of schedule

## Issues Categorization
- **Predicted**: Identified by agent_basa
- **Unpredicted**: New issues not in risk analysis
- **Self-Resolved**: Problem fixed automatically
- **Escalated**: Required intervention

## Notes
- Executed immediately after step completion
- Provides real-time feedback
- Input for retro_agent learning
- Creates historical record
- Supports continuous improvement
