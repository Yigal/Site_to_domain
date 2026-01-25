"""AWS S3 and Secrets Manager integration."""

import boto3
import structlog
from typing import Optional, Dict, Any
from app.config import settings

logger = structlog.get_logger()


class AWSStorageService:
    """AWS S3 and Secrets Manager operations."""

    def __init__(self):
        """Initialize AWS clients."""
        self.s3_client = boto3.client(
            "s3",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        self.secrets_client = boto3.client(
            "secretsmanager",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

    def upload_file(self, local_path: str, remote_key: str) -> bool:
        """Upload file to S3."""
        try:
            logger.info(
                "aws_upload_start",
                bucket=settings.s3_bucket,
                key=remote_key,
            )
            self.s3_client.upload_file(
                local_path,
                settings.s3_bucket,
                remote_key,
            )
            logger.info("aws_upload_success", key=remote_key)
            return True
        except Exception as e:
            logger.error("aws_upload_failed", error=str(e), key=remote_key)
            return False

    def download_file(self, remote_key: str, local_path: str) -> bool:
        """Download file from S3."""
        try:
            logger.info("aws_download_start", key=remote_key)
            self.s3_client.download_file(
                settings.s3_bucket,
                remote_key,
                local_path,
            )
            logger.info("aws_download_success", key=remote_key)
            return True
        except Exception as e:
            logger.error("aws_download_failed", error=str(e), key=remote_key)
            return False

    def store_secret(self, secret_name: str, secret_value: str) -> bool:
        """Store secret in Secrets Manager."""
        try:
            logger.info("aws_secret_store_start", secret_name=secret_name)
            self.secrets_client.create_secret(
                Name=secret_name,
                SecretString=secret_value,
            )
            logger.info("aws_secret_store_success", secret_name=secret_name)
            return True
        except Exception as e:
            logger.error(
                "aws_secret_store_failed",
                error=str(e),
                secret_name=secret_name,
            )
            return False

    def retrieve_secret(self, secret_name: str) -> Optional[str]:
        """Retrieve secret from Secrets Manager."""
        try:
            logger.info("aws_secret_retrieve_start", secret_name=secret_name)
            response = self.secrets_client.get_secret_value(
                SecretId=secret_name
            )
            logger.info("aws_secret_retrieve_success", secret_name=secret_name)
            return response.get("SecretString")
        except Exception as e:
            logger.error(
                "aws_secret_retrieve_failed",
                error=str(e),
                secret_name=secret_name,
            )
            return None

    def list_buckets(self) -> Dict[str, Any]:
        """List all S3 buckets."""
        try:
            logger.info("aws_list_buckets_start")
            response = self.s3_client.list_buckets()
            logger.info("aws_list_buckets_success")
            return response
        except Exception as e:
            logger.error("aws_list_buckets_failed", error=str(e))
            return {}


# Singleton instance
aws_service = AWSStorageService()
