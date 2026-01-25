# Retro Agent (Retrospective & Learning Agent)

## Purpose
Analyzes execution summaries to extract lessons learned and create comprehensive recommendations for avoiding identified errors and improving future executions.

## Responsibilities
- Read execution summary reports
- Categorize problems by root cause
- Analyze patterns across multiple executions
- Generate improvement recommendations
- Suggest changes to guidelines
- Request agent and skill modifications
- Recommend research investigations
- Create preventive strategies

## Key Functions
- `read_summary_document()` - Loads summary_agent output
- `categorize_problems()` - Groups by root cause
- `analyze_problem_patterns()` - Finds recurring issues
- `generate_guideline_improvements()` - Suggests plan modifications
- `request_agent_changes()` - Documents agent/skill improvements
- `request_research()` - Identifies knowledge gaps
- `create_prevention_strategies()` - Develops preventive approaches
- `generate_retro_report()` - Creates final retrospective

## Retrospective Document Structure

### 1. Problems Resulting from Guidelines

For each guideline-related problem:
- **Problem Description**: What went wrong
- **Root Cause**: Why the guideline was insufficient
- **Impact**: Effect on execution
- **Guideline Improvement Tip**:
  - Specific change to wording
  - Additional detail needed
  - Clarification required
  - Example to add
  - Edge case to document

### 2. Problems Resulting from Agent Definitions

For each agent/skill-related problem:
- **Problem Description**: What went wrong
- **Affected Agent/Skill**: Which component failed
- **Root Cause**: Why the agent definition was insufficient
- **Impact**: How execution was affected
- **Agent Change Request**:
  - New responsibility to add
  - Function to implement
  - Integration point to improve
  - Error handling enhancement
  - Documentation update

### 3. Problems Resulting from Environment

For each environment-related problem:
- **Problem Description**: What went wrong
- **Environmental Factor**: What was missing/unknown
- **Root Cause**: Lack of prior information
- **Impact**: Consequence of knowledge gap
- **Research Agent Recommendation**:
  - Topic to investigate
  - Information to gather
  - Validation method
  - Documentation needed
  - Timing (before/during/after steps)

### 4. Problems That Cannot Be Predicted

For each unpredictable problem:
- **Problem Description**: What went wrong
- **Unpredictable Nature**: Why it couldn't be foreseen
- **Impact**: Effect on execution
- **Prevention Strategies**:
  - Monitoring approach
  - Detection method
  - Early warning signs
  - Fallback procedure
  - Adaptation strategy
  - Recovery plan

## Integration Points
- Reads summary_agent output
- Compares to preaction_agent plan
- References agent_basa risk analysis
- Updates EXECUTION_PLAN guidelines
- Feeds improvements to team
- Creates knowledge base entries

## Output Files
```
retro_docs/
├── STEP_X_RETROSPECTIVE.md (complete retro)
├── STEP_X_GUIDELINE_CHANGES.md (plan improvements)
├── STEP_X_AGENT_CHANGE_REQUESTS.md (component updates)
├── STEP_X_RESEARCH_RECOMMENDATIONS.md (knowledge gaps)
└── LESSON_LEARNED_DATABASE.md (cumulative learning)
```

## Retrospective Report Format
```markdown
# STEP_X RETROSPECTIVE: [Step Name]

## Executive Summary
[Key learnings and recommendations]

## 1. Problems Resulting from Guidelines

### Problem 1: [Problem Name]
- **Description**: [What happened]
- **Guideline Issue**: [Why guideline was incomplete]
- **Tip to Improve Guideline**:
  - [Specific change]
  - [Example]
  - [Clarification needed]

## 2. Problems Resulting from Agent Definitions

### Problem 1: [Problem Name]
- **Description**: [What happened]
- **Agent**: [Which component]
- **Change Request**:
  - **New Function**: [Function name and purpose]
  - **Enhancement**: [Existing function improvement]
  - **Integration**: [Better integration needed]

## 3. Problems Resulting from Environment

### Problem 1: [Problem Name]
- **Description**: [What happened]
- **Research Recommendation**:
  - **Topic**: [What to investigate]
  - **Agent Type**: [Research/Validation agent]
  - **Timing**: [When to gather info]
  - **Validation Method**: [How to verify]

## 4. Problems That Cannot Be Predicted

### Problem 1: [Problem Name]
- **Description**: [What happened]
- **New Prevention Approaches**:
  - **Monitoring**: [What to watch]
  - **Detection**: [How to identify early]
  - **Recovery**: [How to handle]
  - **Adaptation**: [How to adjust]

## Recommendations Summary
[List of all recommendations prioritized by impact]

## Implementation Plan
[Suggested timeline for applying learnings]
```

## Pattern Analysis
The retro_agent looks for:
- Recurring problems across steps
- Common failure modes
- Systematic gaps in planning
- Agent/skill capability gaps
- Environmental knowledge gaps

## Learning Database
Maintains cumulative learning:
- Common problems by category
- Solutions that worked
- Prevention strategies proven effective
- Patterns in failures
- Best practices discovered

## Severity Levels
- **Critical**: Causes step failure, must fix immediately
- **Major**: Causes rework, should fix before next iteration
- **Minor**: Causes inefficiency, fix when possible
- **Enhancement**: Improves quality, consider for future

## Notes
- Executed after step completion
- Analyzes both successes and failures
- Creates actionable improvement items
- Builds organizational knowledge
- Supports continuous process improvement
- Enables faster execution of future steps
