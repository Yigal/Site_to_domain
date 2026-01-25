# Agent BASA (Before Action Step Analysis)

## Purpose
Identifies and analyzes potential risks, failures, and issues that could occur during step execution based on the preaction documentation and current environment state.

## Responsibilities
- Analyze preaction step documentation
- Identify potential failures at each action point
- Predict resource constraints and bottlenecks
- Recognize security vulnerabilities
- Detect circular dependencies or conflicts
- Assess time and performance risks
- Create risk mitigation strategies
- Generate early warning indicators

## Key Functions
- `read_step_documentation()` - Loads preaction agent output
- `identify_failure_points()` - Finds where step could fail
- `assess_resource_availability()` - Checks if resources are available
- `detect_dependency_issues()` - Identifies unmet prerequisites
- `predict_timing_risks()` - Estimates if timeline will hold
- `check_security_risks()` - Identifies potential security issues
- `generate_risk_report()` - Creates comprehensive risk analysis
- `suggest_mitigations()` - Proposes preventive actions
- `create_contingency_plans()` - Plans for failure scenarios

## Risk Analysis Categories

### Technical Risks
- API rate limiting and throttling
- Network connectivity failures
- Service unavailability (AWS, GitHub, Cloudflare, GCP)
- Timeout and deadline issues
- Resource exhaustion
- Version compatibility issues

### Credential & Authentication Risks
- Token expiration during execution
- Missing or invalid credentials
- Permission issues (IAM, scope mismatches)
- Credential rotation conflicts
- Secret retrieval failures

### Dependency Risks
- Missing prerequisites from previous steps
- Circular or broken dependencies
- Concurrent execution conflicts
- State consistency issues
- Rollback mechanism failures

### Environmental Risks
- DNS propagation delays
- GCP project creation latency (60+ seconds)
- Cloudflare GitHub App not installed
- GitHub App authorization issues
- Rate limiting across multiple services

### Data & State Risks
- Workspace creation failures
- File system permissions
- Temporary directory cleanup
- Git state conflicts
- Large file handling issues

## Integration Points
- Reads output from preaction_agent
- Accesses EXECUTION_PLAN.json for dependencies
- Queries current environment state
- Provides input to all agents during execution
- Feeds forward to summary_agent

## Risk Report Format
```
STEP_X_RISK_ANALYSIS.md
├── Executive Summary
├── Critical Risks (Must Prevent)
├── High Risks (Monitor Closely)
├── Medium Risks (Plan Around)
├── Low Risks (Document)
├── Contingency Plans
├── Monitoring Checkpoints
└── Escalation Procedures
```

## Early Warning Indicators
For each risk, provides:
- Symptom to watch for
- Detection method
- Escalation trigger
- Rollback decision point

## Mitigation Recommendations
Each risk includes:
- Preventive action
- Detection strategy
- Recovery procedure
- Alternative approach

## Output Files
```
steps_docs/
├── STEP_X_PREACTION.md (from preaction_agent)
├── STEP_X_RISK_ANALYSIS.md (from agent_basa)
└── STEP_X_CONTINGENCY_PLANS.md (detailed fallbacks)
```

## Notes
- Executed after preaction_agent, before step begins
- Continuously updates during step execution
- Provides real-time risk assessment
- Helps teams prepare for failures
- Feeds data to retro_agent for learning
