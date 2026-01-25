# User Post-Action Request: Additional Agents and Workflow

## Request Overview

Add a preaction agent and a post action agent, the preaction agent will get the specific guidlines and create a full description of everything that is going to happend in this step, he will save this in the steps_docs folder with the name of the step.

Add another agent who will after the plan have already started and think about everything that can go wrong with the current step based on the step document produced before, call this agent agent_basa.md.

Add a summary agent that will summaries everything that happen during the execution of this step, and commend if it was according to plan or not.

Add a retro_agent that will read the summary document and create a document on how to avaid these errors. Stracture the retro document by:

### 1. Problems resulting from the guidlines

For each problem add a tip to improve the guidlines to aviod this

### 2. Problems resulting from the agents definitions

For each problem add an agent or skill change request to avoid this in the future

### 3. Problems resulting from the environment

For each problem recomend a research agent that could have gather that information before

### 4. Problems that cannot be predicted

For each problem try to think about new ways to avoid that

---

## Implementation Notes

*The preaction agent should be executed at the beginning of each step to create comprehensive documentation before execution begins. This document serves as the baseline for comparison and helps teams understand what will happen.*

*The agent_basa (Before Action Step Analysis) should be executed after preaction documentation is created but before execution begins, providing risk identification and mitigation strategies.*

*The summary agent should be executed immediately after step completion to document actual outcomes against planned expectations.*

*The retro_agent should be executed after summary reports are available, creating actionable improvement recommendations that feed back into both immediate corrections and long-term process improvements.*

*A steps_docs folder structure is recommended to organize all these documents chronologically by step, making it easy to track the full lifecycle of each execution phase.*

---

## Deliverables Status

The following agents have been created:

- ✅ **preaction-agent.md** - Creates detailed pre-step documentation
- ✅ **agent-basa.md** - Analyzes risks and potential failures before execution
- ✅ **summary-agent.md** - Documents actual execution and compares to plan
- ✅ **retro-agent.md** - Creates improvement recommendations based on summary

*All agents are now available in the `/agents` folder and integrated with the overall execution framework.*
