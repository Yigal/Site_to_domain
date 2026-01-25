"""
Celery application configuration.
Sets up the task queue, message broker, and result backend.
"""

from celery import Celery
from app.config import settings
import structlog

logger = structlog.get_logger()

# Create Celery app
app = Celery(
    "auto_deployer",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# Configure Celery
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)


@app.task(bind=True)
def deploy_task(self, repo_url: str, domain: str):
    """
    Main deployment task.
    Orchestrates the entire deployment workflow.
    """
    logger.info("deployment_started", repo_url=repo_url, domain=domain)
    try:
        self.update_state(state="PROCESSING", meta={"step": 1})
        logger.info("deployment_in_progress", step=1)
        return {"status": "success", "message": "Deployment workflow initiated"}
    except Exception as e:
        logger.error("deployment_failed", error=str(e))
        raise


if __name__ == "__main__":
    app.start()
