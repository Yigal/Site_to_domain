"""
AWS Credentials Resource Test
Tests that AWS credentials from .env have access to required AWS resources.
One test per required AWS resource.
"""

import pytest
import boto3
from botocore.exceptions import ClientError


@pytest.mark.credentials
@pytest.mark.aws
class TestAWSS3Resource:
    """Test AWS S3 resource access."""

    def test_s3_bucket_access(self, aws_credentials):
        """
        Test that AWS credentials can access S3 bucket.
        REQUIRES: S3_BUCKET environment variable or fixture parameter
        """
        s3_client = boto3.client(
            "s3",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )

        # Test S3 list_buckets permission
        try:
            response = s3_client.list_buckets()
            assert "Buckets" in response
            print(f"\n✅ S3 Access: Found {len(response['Buckets'])} bucket(s)")
        except ClientError as e:
            if e.response["Error"]["Code"] == "InvalidAccessKeyId":
                pytest.fail("❌ AWS_ACCESS_KEY_ID is invalid")
            elif e.response["Error"]["Code"] == "SignatureDoesNotMatch":
                pytest.fail("❌ AWS_SECRET_ACCESS_KEY is invalid")
            else:
                pytest.fail(f"❌ S3 access failed: {e}")


@pytest.mark.credentials
@pytest.mark.aws
class TestAWSSecretsManagerResource:
    """Test AWS Secrets Manager resource access."""

    def test_secrets_manager_access(self, aws_credentials):
        """
        Test that AWS credentials can access Secrets Manager.
        REQUIRES: SecretsManager permissions
        """
        secrets_client = boto3.client(
            "secretsmanager",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )

        try:
            response = secrets_client.list_secrets(MaxResults=1)
            assert "SecretList" in response
            print(f"\n✅ Secrets Manager Access: Successful")
        except ClientError as e:
            if "AccessDenied" in str(e):
                pytest.fail("❌ Access denied to Secrets Manager")
            else:
                pytest.fail(f"❌ Secrets Manager access failed: {e}")


@pytest.mark.credentials
@pytest.mark.aws
class TestAWSAuthenticationResource:
    """Test AWS authentication with provided credentials."""

    def test_aws_authentication(self, aws_credentials):
        """
        Test that AWS credentials are valid and authenticate successfully.
        This validates the credentials work with AWS.
        """
        s3_client = boto3.client(
            "s3",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )

        try:
            s3_client.list_buckets()
            print("\n✅ AWS Authentication: Credentials are valid")
        except ClientError as e:
            if e.response["Error"]["Code"] == "InvalidAccessKeyId":
                pytest.fail("❌ AWS Access Key ID is invalid")
            elif e.response["Error"]["Code"] == "SignatureDoesNotMatch":
                pytest.fail("❌ AWS Secret Access Key is invalid")
            else:
                pytest.fail(f"❌ Authentication failed: {e}")
