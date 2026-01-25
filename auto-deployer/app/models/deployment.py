"""Deployment response and status models."""

from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class DeploymentStatus(str, Enum):
    """Deployment status enumeration."""
    PENDING = "pending"
    INITIALIZING = "initializing"
    CLONING = "cloning"
    TRANSFORMING = "transforming"
    PUSHING = "pushing"
    CONFIGURING = "configuring"
    DEPLOYING = "deploying"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class DeploymentResponse(BaseModel):
    """Response model for deployment creation."""
    task_id: str
    status: DeploymentStatus
    domain: str
    framework: str
    created_at: str
    estimated_duration: int


class DeploymentStatusResponse(BaseModel):
    """Response model for deployment status check."""
    task_id: str
    status: DeploymentStatus
    progress: int
    message: str
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None


class StepResult(BaseModel):
    """Result of a deployment step."""
    step_number: int
    step_name: str
    status: DeploymentStatus
    duration: int
    output: Optional[str] = None
    error: Optional[str] = None


class DeploymentDetails(BaseModel):
    """Detailed deployment information."""
    task_id: str
    status: DeploymentStatus
    domain: str
    framework: str
    steps: List[StepResult]
    total_duration: int
    rollback_info: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: str
    task_id: Optional[str] = None
    status_code: int
