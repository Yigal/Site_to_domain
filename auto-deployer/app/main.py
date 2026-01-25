"""
Auto-Deployer API - Main FastAPI application.
Provides REST endpoints for deployment orchestration.
"""

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import structlog
from app.config import settings
from app.models.request import DeploymentRequest, UploadRequest, StatusRequest
from app.models.deployment import DeploymentResponse, DeploymentStatusResponse, DeploymentStatus
from worker.celery_app import app as celery_app
from app.utils.saga_context import saga_orchestrator
from app.utils.middleware.error_handler import error_handler
from typing import Optional
import uuid
from datetime import datetime

# Configure logging
logger = structlog.get_logger()

# Initialize FastAPI application
app = FastAPI(
    title="Auto-Deployer API",
    description="Enterprise-grade asynchronous orchestration system for automated frontend deployment",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns 200 OK if service is running.
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "auto-deployer-api",
            "version": "1.0.0",
        },
    )


@app.get("/")
async def root():
    """
    Root endpoint.
    Returns API information.
    """
    return JSONResponse(
        status_code=200,
        content={
            "message": "Auto-Deployer API",
            "documentation": "/docs",
            "endpoints": {
                "health": "/health",
                "deploy": "/deploy",
                "status": "/deploy/{task_id}",
                "upload": "/upload",
            },
        },
    )


@app.post("/deploy", response_model=DeploymentResponse)
async def start_deployment(request: DeploymentRequest):
    """
    Start a new deployment.
    Accepts Git URL or ZIP upload URL and domain configuration.
    Returns task ID for tracking deployment progress.
    """
    try:
        task_id = str(uuid.uuid4())
        logger.info(
            "deployment_request_received",
            task_id=task_id,
            domain=request.domain,
            framework=request.framework,
        )

        # Create saga context
        saga_context = saga_orchestrator.create_saga(task_id)

        # Define deployment steps as saga
        saga_context.add_step(
            1,
            "Clone Repository",
            "clone_repo",
            "delete_repo",
        )
        saga_context.add_step(
            2,
            "Transform Code",
            "transform_code",
            "revert_transform",
        )
        saga_context.add_step(
            3,
            "Push to GitHub",
            "push_github",
            "delete_github_repo",
        )
        saga_context.add_step(
            4,
            "Deploy Cloudflare",
            "deploy_cloudflare",
            "delete_cloudflare",
        )
        saga_context.add_step(
            5,
            "Configure Domain",
            "configure_domain",
            "remove_dns",
        )

        # Start async deployment task
        celery_task = celery_app.send_task(
            "deploy.start",
            args=[request.repo_url or request.zip_file_url, request.domain],
            task_id=task_id,
        )

        logger.info(
            "deployment_started",
            task_id=task_id,
            celery_task=celery_task.id,
        )

        return DeploymentResponse(
            task_id=task_id,
            status=DeploymentStatus.PENDING,
            domain=request.domain,
            framework=request.framework,
            created_at=datetime.now().isoformat(),
            estimated_duration=270,  # 4.5 minutes
        )
    except Exception as e:
        logger.error("deployment_creation_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/deploy/{task_id}", response_model=DeploymentStatusResponse)
async def get_deployment_status(task_id: str):
    """
    Get deployment status.
    Returns current status and progress of deployment task.
    """
    try:
        logger.info("deployment_status_check", task_id=task_id)

        # Get saga context
        saga_context = saga_orchestrator.get_saga(task_id)
        if not saga_context:
            raise HTTPException(status_code=404, detail="Deployment not found")

        # Get celery task result
        celery_task = celery_app.AsyncResult(task_id)

        # Determine progress based on saga steps
        completed_steps = sum(
            1 for step in saga_context.steps.values()
            if step["status"].value == "completed"
        )
        total_steps = len(saga_context.steps) or 5
        progress = int((completed_steps / total_steps) * 100)

        status = DeploymentStatus.PENDING
        if celery_task.state == "SUCCESS":
            status = DeploymentStatus.COMPLETED
        elif celery_task.state == "FAILURE":
            status = DeploymentStatus.FAILED
        elif celery_task.state == "PROGRESS":
            status = DeploymentStatus.DEPLOYING

        return DeploymentStatusResponse(
            task_id=task_id,
            status=status,
            progress=progress,
            message=f"Step {completed_steps}/{total_steps} completed",
            created_at=saga_context.created_at,
            updated_at=datetime.now().isoformat(),
            completed_at=None,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("deployment_status_check_failed", error=str(e), task_id=task_id)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_source(file: UploadFile = File(...)):
    """
    Upload source code.
    Accepts ZIP file upload for deployment.
    Returns upload URL for use in deployment request.
    """
    try:
        logger.info("file_upload_start", filename=file.filename, size=file.size)

        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="Only ZIP files are supported")

        # In production, would save file to S3
        upload_id = str(uuid.uuid4())
        upload_url = f"s3://auto-deployer-uploads/{upload_id}/{file.filename}"

        logger.info("file_upload_success", filename=file.filename, url=upload_url)

        return {
            "upload_id": upload_id,
            "filename": file.filename,
            "size": file.size,
            "url": upload_url,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("file_upload_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
