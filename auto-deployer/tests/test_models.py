"""Tests for Pydantic models."""

import pytest
from app.models.request import DeploymentRequest, UploadRequest, StatusRequest
from app.models.deployment import (
    DeploymentResponse,
    DeploymentStatus,
    StepResult,
    ErrorResponse,
)
from app.models.types import Framework, CloudProvider, SourceType, Environment


@pytest.mark.unit
def test_deployment_request_valid():
    """Test valid deployment request."""
    request = DeploymentRequest(
        repo_url="https://github.com/test/repo",
        domain="example.com",
        framework="react",
    )
    assert request.domain == "example.com"
    assert request.framework == "react"


@pytest.mark.unit
def test_deployment_request_missing_domain():
    """Test deployment request without domain."""
    with pytest.raises(ValueError):
        DeploymentRequest(
            repo_url="https://github.com/test/repo",
            framework="react",
        )


@pytest.mark.unit
def test_deployment_response():
    """Test deployment response."""
    response = DeploymentResponse(
        task_id="task-123",
        status=DeploymentStatus.PENDING,
        domain="example.com",
        framework="react",
        created_at="2026-01-25T20:48:00",
        estimated_duration=270,
    )
    assert response.task_id == "task-123"
    assert response.status == DeploymentStatus.PENDING


@pytest.mark.unit
def test_deployment_status_response():
    """Test deployment status response."""
    from datetime import datetime

    response = DeploymentStatusResponse(
        task_id="task-123",
        status=DeploymentStatus.DEPLOYING,
        progress=50,
        message="Deployment in progress",
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
    )
    assert response.progress == 50
    assert response.status == DeploymentStatus.DEPLOYING


@pytest.mark.unit
def test_deployment_status_enum():
    """Test deployment status enumeration."""
    assert DeploymentStatus.PENDING.value == "pending"
    assert DeploymentStatus.COMPLETED.value == "completed"
    assert DeploymentStatus.FAILED.value == "failed"


@pytest.mark.unit
def test_framework_enum():
    """Test framework enumeration."""
    assert Framework.REACT.value == "react"
    assert Framework.NEXTJS.value == "nextjs"
    assert Framework.VUE.value == "vue"


@pytest.mark.unit
def test_cloud_provider_enum():
    """Test cloud provider enumeration."""
    assert CloudProvider.AWS.value == "aws"
    assert CloudProvider.GITHUB.value == "github"
    assert CloudProvider.GCP.value == "gcp"


@pytest.mark.unit
def test_error_response():
    """Test error response model."""
    error = ErrorResponse(
        error="Deployment Failed",
        detail="Invalid repository URL",
        status_code=400,
    )
    assert error.error == "Deployment Failed"
    assert error.status_code == 400
