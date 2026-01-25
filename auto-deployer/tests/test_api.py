"""
Tests for API endpoints.
Covers health checks and basic endpoint functionality.
"""

import pytest


@pytest.mark.unit
def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.unit
def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.unit
def test_deploy_endpoint(client):
    """Test deploy endpoint."""
    response = client.post("/deploy")
    assert response.status_code == 200


@pytest.mark.unit
def test_upload_endpoint(client):
    """Test upload endpoint."""
    response = client.post("/upload")
    assert response.status_code == 200
