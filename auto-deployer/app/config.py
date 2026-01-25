"""
Application configuration and settings management.
Loads configuration from environment variables using Pydantic.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # FastAPI Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False

    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_url: str = "redis://localhost:6379"

    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    s3_bucket: Optional[str] = None

    # GitHub Configuration
    github_token: Optional[str] = None
    github_org: Optional[str] = None

    # Cloudflare Configuration
    cloudflare_account_id: Optional[str] = None
    cloudflare_token: Optional[str] = None
    cloudflare_email: Optional[str] = None

    # GCP Configuration
    gcp_project_id: Optional[str] = None
    gcp_service_account: Optional[str] = None
    gcp_billing_account: Optional[str] = None

    # Celery Configuration
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
