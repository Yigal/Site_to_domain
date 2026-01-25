"""Request models for API endpoints."""

from pydantic import BaseModel
from typing import Optional


class DeploymentRequest(BaseModel):
    """Request model for starting a deployment."""
    repo_url: Optional[str] = None
    zip_file_url: Optional[str] = None
    domain: str
    framework: str = "react"
    custom_domain: Optional[str] = None


class UploadRequest(BaseModel):
    """Request model for uploading source code."""
    filename: str
    size: int
    checksum: Optional[str] = None


class StatusRequest(BaseModel):
    """Request model for checking deployment status."""
    task_id: str


class ConfigurationRequest(BaseModel):
    """Request model for configuration updates."""
    environment: str
    variables: dict
