# Preaction Agent

## Purpose
Creates comprehensive, detailed descriptions of everything that will happen during a specific execution step before that step begins.

## Responsibilities
- Receive specific guidelines for a step
- Analyze all dependencies and prerequisites
- Create full detailed descriptions of all actions, decisions, and outcomes
- Document expected results and success criteria
- Save documentation in steps_docs folder with step name
- Generate actionable checklist from guidelines

## Key Functions
- `receive_step_guidelines()` - Accepts guidelines for a specific step
- `analyze_step_scope()` - Determines full scope of work
- `create_detailed_description()` - Generates comprehensive step description
- `identify_dependencies()` - Maps all required resources and prerequisites
- `generate_outcomes_list()` - Lists all expected outputs
- `create_checklist()` - Converts guidelines to actionable items
- `save_step_documentation()` - Persists to steps_docs/{step_name}.md

## Step Documentation Format
Each saved document includes:
- **Step Overview**: High-level summary of what will happen
- **Detailed Actions**: Complete breakdown of all actions in order
- **Dependencies**: Required resources, credentials, services
- **Expected Outcomes**: All outputs and deliverables
- **Decision Points**: Where choices will be made
- **Success Criteria**: How to verify step completion
- **Resource Requirements**: Compute, storage, time needed
- **Integration Points**: How this step connects to others

## Integration Points
- Called at the START of each execution step
- Receives guidelines from EXECUTION_PLAN.md
- Feeds into agent_basa for risk identification
- Output used by summary_agent for comparison

## Error Handling
- Missing or incomplete guidelines
- Circular dependencies detected
- Insufficient resource availability
- Prerequisite failures

## Output Structure
```
steps_docs/
├── STEP_1_PROJECT_INITIALIZATION.md
├── STEP_2_CONFIGURATION_LAYER_SETUP.md
├── STEP_3_DATA_MODELS.md
├── STEP_4_AWS_STORAGE_SERVICE.md
├── ...
└── STEP_15_PRODUCTION_DEPLOYMENT.md
```

## Notes
- Executed before step begins (pre-flight documentation)
- Uses EXECUTION_PLAN as input source
- Creates the baseline for comparison with actual execution
- Document serves as communication tool for team
- Helps identify missing information early
