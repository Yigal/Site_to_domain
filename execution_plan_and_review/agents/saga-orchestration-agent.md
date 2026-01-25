# Saga Orchestration Agent

## Purpose
Central orchestrator implementing the Saga Pattern for distributed transaction management across multiple cloud services, ensuring consistency and enabling rollback on failure.

## Responsibilities
- Coordinate execution of all deployment phases in correct sequence
- Maintain deployment state and history in Redis/S3
- Record completed steps with their rollback compensation functions
- Execute rollback compensation actions in reverse order on failure
- Handle long-running asynchronous operations
- Manage timeout and retry policies
- Track saga completion and failure states
- Persist state for recovery and monitoring

## Key Functions
- `execute_deployment_saga()` - Main Celery task orchestrating full deployment
- `begin()` - Initialize saga with deployment ID
- `record_step()` - Record completed step with rollback info
- `mark_completed()` - Mark saga as successfully completed
- `mark_failed()` - Mark saga as failed and trigger rollback
- `execute_rollback()` - Execute compensation actions in reverse
- `get_state()` - Return current saga state
- `_persist_state()` - Save state to Redis/S3
- `_load_state()` - Load state from Redis/S3

## Phases Coordinated
1. Source Acquisition - Prepare workspace from git/folder
2. Code Transformation - Modify vite.config.js via AST
3. GitHub Creation - Create repo and initial push
4. Cloudflare Setup - Create Pages project
5. GCP Provisioning - Full GCP/Firebase setup chain
6. Config Injection - Inject Firebase config, second push
7. Domain Finalization - DNS and custom domain binding

## State Management
- Backend: Redis (primary), S3 (backup)
- State schema: deployment ID, status, steps array, failure reason
- Persistence frequency: After each phase completion

## Compensation/Rollback Actions
- Delete GitHub repository
- Delete Cloudflare Pages project
- Delete GCP project
- Remove DNS records
- Cleanup temporary workspaces

## Integration Points
- Acts as conductor for all agents
- Receives requests from FastAPI /deploy endpoint
- Updates deployment status via GET /deploy/{task_id}
- Sends notifications on completion/failure
- Implements retry logic with exponential backoff

## Error Scenarios
- Source acquisition failures
- Code transformation errors
- GitHub API failures
- Cloudflare API errors (e.g., missing GitHub App)
- GCP project creation failures
- Billing linkage failures
- Firebase configuration errors
- DNS propagation issues

## Success Criteria
- All phases execute successfully
- State persisted correctly
- Deployment completed within timeout
- All resources properly created

## Failure Scenarios
- Partial failure triggers rollback sequence
- Compensation failures logged but execution continues
- Failed deployments marked with error details
- State preserved for debugging

## Notes
- Implements Saga Pattern instead of distributed transactions
- Supports concurrent deployments via unique saga IDs
- Uses Celery for async background execution
- Idempotent operations allow safe retries
