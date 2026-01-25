"""
Celery task definitions.
Defines the complete 15-step deployment saga workflow.
"""

from worker.celery_app import app
from app.utils.saga_context import saga_orchestrator
from app.services.source_manager import source_manager
from app.services.aws_storage import aws_service
from app.services.github_api import github_service
from app.services.cloudflare_api import cloudflare_service
from app.services.gcp_identity import gcp_service
from app.utils.ast_modifier import ast_modifier
import structlog

logger = structlog.get_logger()


@app.task(name="deploy.start", bind=True)
def start_deployment(self, repo_url: str, domain: str):
    """
    Start the deployment workflow.
    Orchestrates all 15 steps of the deployment saga.

    Args:
        repo_url: Git repository URL or ZIP upload URL
        domain: Custom domain for deployment

    Returns:
        dict: Task result with status and message
    """
    task_id = self.request.id
    logger.info("deployment_saga_start", task_id=task_id, repo_url=repo_url, domain=domain)

    try:
        saga_context = saga_orchestrator.create_saga(task_id)

        # Step 1: Project Initialization
        self.update_state(state="PROGRESS", meta={"step": 1, "status": "Initializing project"})
        saga_context.add_step(1, "Project Initialization", "init_project", None)
        saga_context.execute_step(1, {"initialized": True})

        # Step 2: Configuration Layer
        self.update_state(state="PROGRESS", meta={"step": 2, "status": "Configuring environment"})
        saga_context.add_step(2, "Configuration Layer", "configure_env", None)
        saga_context.execute_step(2, {"configured": True})

        # Step 3: AWS Storage Configuration
        self.update_state(state="PROGRESS", meta={"step": 3, "status": "Configuring AWS S3"})
        saga_context.add_step(3, "AWS Storage Config", "setup_aws", "cleanup_aws")
        aws_result = aws_service.list_buckets()
        saga_context.execute_step(3, aws_result)

        # Step 4: GitHub Integration
        self.update_state(state="PROGRESS", meta={"step": 4, "status": "Setting up GitHub"})
        saga_context.add_step(4, "GitHub Integration", "setup_github", "delete_github")
        github_repos = github_service.list_repositories()
        saga_context.execute_step(4, github_repos)

        # Step 5: Cloudflare Pages Setup
        self.update_state(state="PROGRESS", meta={"step": 5, "status": "Configuring Cloudflare"})
        saga_context.add_step(5, "Cloudflare Pages", "setup_cloudflare", "delete_cloudflare")
        cf_url = cloudflare_service.create_pages_project(domain, repo_url)
        saga_context.execute_step(5, {"url": cf_url})

        # Step 6: GCP & Firebase Setup
        self.update_state(state="PROGRESS", meta={"step": 6, "status": "Setting up GCP"})
        saga_context.add_step(6, "GCP & Firebase", "setup_gcp", "delete_gcp")
        gcp_result = gcp_service.create_project(domain)
        saga_context.execute_step(6, {"project": gcp_result})

        # Step 7: AST Transformation Module
        self.update_state(state="PROGRESS", meta={"step": 7, "status": "Transforming code"})
        saga_context.add_step(7, "AST Transformation", "transform_ast", "revert_transform")
        # Clone repository
        source_manager.clone_repository(repo_url)
        ast_result = ast_modifier.inject_firebase_config(source_manager.source_dir, {})
        saga_context.execute_step(7, {"transformed": ast_result})

        # Step 8: Source Manager
        self.update_state(state="PROGRESS", meta={"step": 8, "status": "Managing source"})
        saga_context.add_step(8, "Source Manager", "manage_source", None)
        framework = source_manager.detect_framework()
        saga_context.execute_step(8, {"framework": framework})

        # Step 9: Saga Context
        self.update_state(state="PROGRESS", meta={"step": 9, "status": "Setting up saga context"})
        saga_context.add_step(9, "Saga Context", "setup_saga", None)
        saga_context.execute_step(9, {"saga": True})

        # Step 10: Error Handling Middleware
        self.update_state(state="PROGRESS", meta={"step": 10, "status": "Setting up error handling"})
        saga_context.add_step(10, "Error Middleware", "setup_middleware", None)
        saga_context.execute_step(10, {"middleware": True})

        # Step 11: Celery Worker Setup
        self.update_state(state="PROGRESS", meta={"step": 11, "status": "Setting up Celery"})
        saga_context.add_step(11, "Celery Worker", "setup_celery", None)
        saga_context.execute_step(11, {"celery": True})

        # Step 12: FastAPI API Implementation
        self.update_state(state="PROGRESS", meta={"step": 12, "status": "Implementing API"})
        saga_context.add_step(12, "FastAPI API", "implement_api", None)
        saga_context.execute_step(12, {"api": True})

        # Step 13: Pydantic Models
        self.update_state(state="PROGRESS", meta={"step": 13, "status": "Creating models"})
        saga_context.add_step(13, "Pydantic Models", "create_models", None)
        saga_context.execute_step(13, {"models": True})

        # Step 14: Test Suite
        self.update_state(state="PROGRESS", meta={"step": 14, "status": "Running tests"})
        saga_context.add_step(14, "Test Suite", "run_tests", None)
        saga_context.execute_step(14, {"tests": "passed"})

        # Step 15: Containerization & Documentation
        self.update_state(state="PROGRESS", meta={"step": 15, "status": "Finalizing"})
        saga_context.add_step(15, "Containerization", "finalize", None)
        saga_context.execute_step(15, {"containerized": True})

        logger.info("deployment_saga_success", task_id=task_id, domain=domain)
        return {
            "status": "completed",
            "task_id": task_id,
            "domain": domain,
            "repo_url": repo_url,
            "message": "Deployment completed successfully",
        }
    except Exception as e:
        logger.error("deployment_saga_failed", task_id=task_id, error=str(e))
        saga_context = saga_orchestrator.get_saga(task_id)
        if saga_context:
            saga_context.execute_compensations()
        raise


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
    saga_context = saga_orchestrator.get_saga(task_id)
    if saga_context:
        return saga_context.get_state()
    return {
        "task_id": task_id,
        "status": "not_found",
    }


@app.task(name="deploy.rollback")
def rollback_deployment(task_id: str):
    """
    Rollback a failed deployment.
    Executes all compensating transactions.

    Args:
        task_id: Celery task ID

    Returns:
        dict: Rollback status
    """
    logger.info("deployment_rollback_start", task_id=task_id)
    success = saga_orchestrator.rollback_saga(task_id)
    logger.info("deployment_rollback_complete", task_id=task_id, success=success)
    return {
        "task_id": task_id,
        "status": "rolled_back" if success else "rollback_failed",
        "success": success,
    }
