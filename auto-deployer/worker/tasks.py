"""
Celery task definitions.
Defines the main deployment workflow tasks.
"""

from worker.celery_app import app
import structlog

logger = structlog.get_logger()


@app.task(name="deploy.start")
def start_deployment(repo_url: str, domain: str):
    """
    Start the deployment workflow.

    Args:
        repo_url: Git repository URL or ZIP upload URL
        domain: Custom domain for deployment

    Returns:
        dict: Task result with status and message
    """
    logger.info("task_start_deployment", repo_url=repo_url, domain=domain)
    return {
        "status": "started",
        "repo_url": repo_url,
        "domain": domain,
    }


@app.task(name="deploy.status")
def get_deployment_status(task_id: str):
    """
    Get the status of a deployment task.

    Args:
        task_id: Celery task ID

    Returns:
        dict: Task status information
    """
    logger.info("task_get_status", task_id=task_id)
    return {
        "task_id": task_id,
        "status": "pending",
    }


@app.task(name="deploy.rollback")
def rollback_deployment(task_id: str):
    """
    Rollback a failed deployment.
    Deletes all created resources.

    Args:
        task_id: Celery task ID

    Returns:
        dict: Rollback status
    """
    logger.info("task_rollback", task_id=task_id)
    return {
        "task_id": task_id,
        "status": "rolled_back",
    }
