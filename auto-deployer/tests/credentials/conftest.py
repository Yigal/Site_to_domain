"""
Pytest configuration for credentials tests.
Loads credentials from project root .env file.
"""

import pytest
import os
from pathlib import Path
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env_credentials():
    """
    Load credentials from .env file in project root.
    This is automatically loaded for all tests in this folder.
    """
    # Find .env file in project root (not in tests directory)
    project_root = Path(__file__).parent.parent.parent.parent
    env_file = project_root / ".env"

    if not env_file.exists():
        pytest.skip(f"No .env file found at {env_file}")

    # Load .env file
    load_dotenv(env_file)

    # Verify all required AWS credentials are loaded
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION']
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        pytest.skip(f"Missing AWS credentials in .env: {', '.join(missing)}")


@pytest.fixture
def aws_credentials():
    """
    Fixture providing AWS credentials from .env file.
    SKIPS test if credentials not available.
    """
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_key or not aws_secret:
        pytest.skip("AWS credentials not configured in .env")

    return {
        "access_key_id": aws_key,
        "secret_access_key": aws_secret,
        "region": aws_region,
    }


@pytest.fixture
def github_credentials():
    """
    Fixture providing GitHub credentials from .env file.
    SKIPS test if credentials not available.
    """
    token = os.getenv("GITHUB_TOKEN")
    org = os.getenv("GITHUB_ORG")

    if not token or not org:
        pytest.skip("GitHub credentials not configured in .env")

    return {
        "token": token,
        "org": org,
    }


@pytest.fixture
def cloudflare_credentials():
    """
    Fixture providing Cloudflare credentials from .env file.
    SKIPS test if credentials not available.
    """
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    token = os.getenv("CLOUDFLARE_TOKEN")
    email = os.getenv("CLOUDFLARE_EMAIL")

    if not account_id or not token or not email:
        pytest.skip("Cloudflare credentials not configured in .env")

    return {
        "account_id": account_id,
        "token": token,
        "email": email,
    }


@pytest.fixture
def gcp_credentials():
    """
    Fixture providing GCP credentials from .env file.
    SKIPS test if credentials not available.
    """
    import json

    service_account_json = os.getenv("GCP_SERVICE_ACCOUNT_JSON")
    project_id = os.getenv("GCP_PROJECT_ID")

    if not service_account_json or not project_id:
        pytest.skip("GCP credentials not configured in .env")

    try:
        service_account_dict = json.loads(service_account_json)
    except json.JSONDecodeError:
        pytest.skip("GCP_SERVICE_ACCOUNT_JSON is not valid JSON")

    return {
        "service_account": service_account_dict,
        "project_id": project_id,
    }


@pytest.fixture
def redis_credentials():
    """
    Fixture providing Redis credentials from .env file.
    SKIPS test if credentials not available.
    """
    redis_url = os.getenv("REDIS_URL")

    if not redis_url:
        pytest.skip("REDIS_URL not configured in .env")

    return {
        "url": redis_url,
    }


def pytest_configure(config):
    """Register custom markers for credential tests."""
    config.addinivalue_line(
        "markers",
        "aws: mark test as AWS credential test",
    )
    config.addinivalue_line(
        "markers",
        "github: mark test as GitHub credential test",
    )
    config.addinivalue_line(
        "markers",
        "cloudflare: mark test as Cloudflare credential test",
    )
    config.addinivalue_line(
        "markers",
        "gcp: mark test as GCP credential test",
    )
    config.addinivalue_line(
        "markers",
        "redis: mark test as Redis credential test",
    )
    config.addinivalue_line(
        "markers",
        "credentials: mark test as credential validation test",
    )
