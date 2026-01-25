# Celery Task Management Skill

## Description
Manages asynchronous task execution, queuing, monitoring, and status tracking using Celery with Redis backend for long-running deployment operations.

## Capabilities
- Queue deployment tasks
- Monitor task status (pending, started, success, failure)
- Retrieve task results
- Implement retry logic with exponential backoff
- Track task progress
- Handle task timeouts
- Cancel running tasks
- Manage task priorities
- Implement task callbacks
- Support task chaining and workflows

## Key Operations
- `apply_async(task_name, args, kwargs)` - Queue task
- `get_task_status(task_id)` - Get task state
- `get_task_result(task_id)` - Retrieve result
- `revoke_task(task_id)` - Cancel task
- `retry_task(task_id, countdown)` - Retry with delay
- `set_task_timeout(timeout_seconds)` - Configure timeout
- `get_task_queue_length()` - Monitor queue
- `get_worker_status()` - Check worker health

## Task States
- **PENDING**: Task queued, not started
- **STARTED**: Task execution begun
- **SUCCESS**: Task completed successfully
- **FAILURE**: Task failed with exception
- **RETRY**: Task retrying after failure
- **REVOKED**: Task cancelled by user

## Configuration
- Broker: Redis (redis://localhost:6379/0)
- Result backend: Redis
- Task serializer: JSON
- Result serializer: JSON
- Timezone: UTC
- Task acks late: True (reliability)

## Deployment Task
- Task name: execute_deployment_saga
- Queue: default
- Priority: Normal
- Timeout: 30 minutes (configurable)
- Retry: 3 attempts with exponential backoff

## Retry Strategy
- Initial retry delay: 60 seconds
- Backoff factor: 2 (exponential)
- Max retries: 3
- Max delay: 3600 seconds (1 hour)
- Retry condition: Network errors, API rate limits

## Task Lifecycle
1. **Queue**: Task added to Redis queue
2. **Assign**: Worker picks up task
3. **Start**: Task execution begins
4. **Progress**: Status updates during execution
5. **Complete**: Task finished (success or failure)
6. **Store**: Result stored in Redis
7. **Cleanup**: Old results periodically purged

## Task Parameters
```python
@app.task(bind=True)
def execute_deployment_saga(self, deployment_request):
    # self.request.id = task_id
    # self.request.retries = retry count
    # self.update_state(state='PROGRESS', meta={...})
    return final_state
```

## Status Endpoint Integration
- GET /deploy/{task_id}
- Queries Celery task result
- Returns current deployment state
- Handles missing or expired tasks

## Result Storage
- Backend: Redis key value store
- Key format: celery-task-{task_id}
- Retention: Configurable (default 24 hours)
- Serialization: JSON

## Worker Configuration
- Concurrency: Configurable (default 4)
- Pool type: Prefork (process-based)
- Worker isolation: Independent processes
- Memory management: Automatic pooling

## Monitoring
- Redis connection status
- Task queue depth
- Worker availability
- Task processing rate
- Success/failure ratio
- Average task duration

## Error Handling
- Task exception capture
- Traceback logging
- Retry on transient failures
- Exponential backoff implementation
- Failed task notification

## Long-Running Operations
- GCP project creation: 60+ seconds
- Firebase setup: 30-60 seconds
- Cloudflare propagation: Minutes
- DNS propagation: 5 minutes - 48 hours
- Task timeout: 30 minutes total

## Task Updates During Execution
```python
self.update_state(
    state='PROGRESS',
    meta={
        'current': 3,
        'total': 7,
        'status': 'Creating GitHub repository',
        'workspace_id': workspace_id
    }
)
```

## Timeout Handling
- Hard timeout: 30 minutes for entire deployment
- Phase timeouts: 5 minutes per major phase
- Operation polling: 60 second timeout
- Network timeouts: 30 seconds per API call

## Result Expiration
- Successful tasks: 24 hours
- Failed tasks: 24 hours (for debugging)
- Cleanup: Automatic via TTL
- Manual cleanup: periodic task

## Integration Points
- Called by FastAPI /deploy endpoint
- Task ID returned immediately
- Status monitored via /deploy/{task_id}
- Results stored for webhook callbacks
- Coordinates with all deployment agents

## Callback Notifications
- On success: Webhook call with deployment details
- On failure: Webhook call with error information
- Payload: JSON with task state and metadata
- Retry: Exponential backoff for webhooks

## Performance Tuning
- Worker concurrency: Balance load
- Queue length: Monitor for bottlenecks
- Result backend: Redis performance critical
- Task serialization: JSON efficient
- Connection pooling: Reuse connections

## Failure Scenarios
1. Network error: Retry with backoff
2. API rate limit: Retry with longer delay
3. Permission denied: Don't retry (log and fail)
4. Timeout: Let saga rollback
5. Partial failure: Saga compensates

## Notes
- Celery essential for async deployment
- Redis required for broker and backend
- Multiple workers scale horizontally
- Task isolation prevents interference
- Results persistent for debugging
- Task completion enables polling model

## Monitoring Commands
```bash
# Check task status
celery inspect active

# View registered tasks
celery inspect registered

# Monitor worker stats
celery inspect stats

# Query task state
celery events
```
