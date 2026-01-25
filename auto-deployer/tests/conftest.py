"""
Pytest configuration and fixtures.
Provides common test setup and fixtures for all tests.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """
    FastAPI test client fixture.
    Provides a test client for making requests to the API.
    """
    return TestClient(app)


@pytest.fixture
def mock_aws_credentials():
    """
    Mock AWS credentials fixture.
    """
    return {
        "access_key_id": "***REMOVED-AWS-ACCESS-KEY-ID***",
        "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "region": "us-east-1",
    }


@pytest.fixture
def mock_github_credentials():
    """
    Mock GitHub credentials fixture.
    """
    return {
        "token": "***REMOVED-GITHUB-TOKEN***",
        "org": "test-org",
    }


@pytest.fixture
def mock_deployment_request():
    """
    Mock deployment request fixture.
    """
    return {
        "repo_url": "https://github.com/test/repo",
        "domain": "example.com",
        "framework": "react",
    }
