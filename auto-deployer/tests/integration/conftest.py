"""
Pytest configuration and fixtures for integration tests.
These tests use REAL cloud services with ACTUAL credentials.
No mocks or placeholders.
"""

import pytest
import os
from app.config import settings


def pytest_configure(config):
    """Register custom markers for integration tests."""
    config.addinivalue_line(
        "markers",
        "requires_aws: mark test as requiring AWS credentials (S3 + Secrets Manager)",
    )
    config.addinivalue_line(
        "markers",
        "requires_github: mark test as requiring GitHub token and organization",
    )
    config.addinivalue_line(
        "markers",
        "requires_cloudflare: mark test as requiring Cloudflare account and token",
    )
    config.addinivalue_line(
        "markers",
        "requires_gcp: mark test as requiring GCP service account credentials",
    )
    config.addinivalue_line(
        "markers",
        "requires_redis: mark test as requiring Redis connection",
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test (uses real services)",
    )
    config.addinivalue_line(
        "markers",
        "requires_internet: mark test as requiring internet connection",
    )


@pytest.fixture
def aws_credentials():
    """
    Fixture providing AWS credentials from environment.
    SKIPS test if credentials not available.
    Uses ACTUAL AWS keys - no mocks.
    """
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    s3_bucket = os.getenv("S3_BUCKET")

    if not aws_key or not aws_secret or not s3_bucket:
        pytest.skip("AWS credentials not configured")

    return {
        "access_key_id": aws_key,
        "secret_access_key": aws_secret,
        "region": aws_region,
        "bucket": s3_bucket,
    }


@pytest.fixture
def github_credentials():
    """
    Fixture providing GitHub credentials from environment.
    SKIPS test if credentials not available.
    Uses ACTUAL GitHub token - no mocks.
    """
    token = os.getenv("GITHUB_TOKEN")
    org = os.getenv("GITHUB_ORG")

    if not token or not org:
        pytest.skip("GitHub credentials not configured")

    return {
        "token": token,
        "org": org,
    }


@pytest.fixture
def cloudflare_credentials():
    """
    Fixture providing Cloudflare credentials from environment.
    SKIPS test if credentials not available.
    Uses ACTUAL Cloudflare token - no mocks.
    """
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    token = os.getenv("CLOUDFLARE_TOKEN")
    email = os.getenv("CLOUDFLARE_EMAIL")

    if not account_id or not token or not email:
        pytest.skip("Cloudflare credentials not configured")

    return {
        "account_id": account_id,
        "token": token,
        "email": email,
    }


@pytest.fixture
def gcp_credentials():
    """
    Fixture providing GCP credentials from environment.
    SKIPS test if credentials not available.
    Uses ACTUAL GCP service account - no mocks.
    """
    service_account = os.getenv("GCP_SERVICE_ACCOUNT")
    project_id = os.getenv("GCP_PROJECT_ID")
    billing_account = os.getenv("GCP_BILLING_ACCOUNT")

    if not service_account or not project_id:
        pytest.skip("GCP credentials not configured")

    return {
        "service_account": service_account,
        "project_id": project_id,
        "billing_account": billing_account,
    }


@pytest.fixture
def redis_connection():
    """
    Fixture providing Redis connection.
    SKIPS test if Redis not available.
    Uses ACTUAL Redis instance - no mocks.
    """
    import redis

    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

    try:
        r = redis.from_url(redis_url)
        r.ping()
        return r
    except Exception as e:
        pytest.skip(f"Redis not available: {str(e)}")


@pytest.fixture
def sample_deployment_data():
    """Fixture providing sample deployment data for testing."""
    return {
        "repo_url": "https://github.com/test/sample-app",
        "domain": "test-app.example.com",
        "framework": "react",
        "custom_domain": None,
    }


@pytest.fixture
def sample_github_repo_data():
    """Fixture providing sample GitHub repository data."""
    return {
        "name": "test-deployment-repo",
        "description": "Test repository for auto-deployer integration testing",
        "private": False,
    }


@pytest.fixture
def sample_s3_upload_data():
    """Fixture providing sample S3 upload data."""
    return {
        "key": "test-uploads/sample-app.zip",
        "content": b"PK\x03\x04",  # ZIP file signature
        "content_type": "application/zip",
    }
