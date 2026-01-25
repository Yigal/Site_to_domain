"""
AWS Integration Tests - Uses REAL AWS services.
No mocks. Requires valid AWS credentials.
Tests will FAIL if AWS credentials are invalid or service is unavailable.
"""

import pytest
import boto3
import uuid
import json
from botocore.exceptions import ClientError


@pytest.mark.integration
@pytest.mark.requires_aws
@pytest.mark.requires_internet
class TestAWSS3Integration:
    """Integration tests for AWS S3 operations with ACTUAL S3 service."""

    def test_s3_bucket_list_with_real_credentials(self, aws_credentials):
        """
        Test listing S3 buckets using ACTUAL AWS credentials.
        FAILS if: AWS key invalid, credentials lack permissions, or AWS is down.
        """
        s3_client = boto3.client(
            "s3",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )

        # ACTUAL API call to list buckets
        response = s3_client.list_buckets()

        assert "Buckets" in response
        assert isinstance(response["Buckets"], list)

    def test_s3_bucket_exists_with_real_credentials(self, aws_credentials):
        """
        Test checking if specific bucket exists using ACTUAL AWS credentials.
        FAILS if: Bucket doesn't exist, credentials invalid, or AWS is down.
        """
        s3_client = boto3.client(
            "s3",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )

        # ACTUAL API call to check bucket
        try:
            s3_client.head_bucket(Bucket=aws_credentials["bucket"])
            bucket_exists = True
        except ClientError as e:
            bucket_exists = False

        assert bucket_exists, f"Bucket {aws_credentials['bucket']} does not exist"

    def test_s3_upload_file_with_real_credentials(self, aws_credentials):
        """
        Test uploading file to S3 using ACTUAL AWS credentials.
        FAILS if: Bucket doesn't exist, no permissions, or AWS is down.
        Creates actual file in S3 - cleans up after test.
        """
        s3_client = boto3.client(
            "s3",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )

        # Test file content (ACTUAL upload)
        test_key = f"integration-test/{uuid.uuid4()}/test-file.txt"
        test_content = b"Integration test content - ACTUAL AWS S3 UPLOAD"

        # ACTUAL API call to upload
        s3_client.put_object(
            Bucket=aws_credentials["bucket"],
            Key=test_key,
            Body=test_content,
            ContentType="text/plain",
        )

        # ACTUAL API call to verify upload
        response = s3_client.get_object(Bucket=aws_credentials["bucket"], Key=test_key)
        uploaded_content = response["Body"].read()

        assert uploaded_content == test_content
        assert response["ContentType"] == "text/plain"

        # Cleanup: ACTUAL deletion
        s3_client.delete_object(Bucket=aws_credentials["bucket"], Key=test_key)

    def test_s3_download_nonexistent_file_fails(self, aws_credentials):
        """
        Test downloading nonexistent file FAILS with ACTUAL S3.
        FAILS if: S3 credentials invalid or service down.
        """
        s3_client = boto3.client(
            "s3",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )

        # ACTUAL API call that should fail
        with pytest.raises(ClientError):
            s3_client.get_object(
                Bucket=aws_credentials["bucket"],
                Key="definitely-does-not-exist-12345.txt",
            )


@pytest.mark.integration
@pytest.mark.requires_aws
@pytest.mark.requires_internet
class TestAWSSecretsManagerIntegration:
    """Integration tests for AWS Secrets Manager with ACTUAL service."""

    def test_secrets_manager_list_with_real_credentials(self, aws_credentials):
        """
        Test listing secrets using ACTUAL AWS Secrets Manager.
        FAILS if: Credentials invalid, no permissions, or AWS is down.
        """
        secrets_client = boto3.client(
            "secretsmanager",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )

        # ACTUAL API call to list secrets
        response = secrets_client.list_secrets(MaxResults=10)

        assert "SecretList" in response
        assert isinstance(response["SecretList"], list)

    def test_secrets_manager_create_and_retrieve(self, aws_credentials):
        """
        Test creating and retrieving secret with ACTUAL AWS Secrets Manager.
        FAILS if: Credentials invalid, permissions denied, or AWS is down.
        Creates ACTUAL secret - cleans up after test.
        """
        secrets_client = boto3.client(
            "secretsmanager",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )

        # Generate unique secret name
        secret_name = f"integration-test/secret-{uuid.uuid4()}"
        secret_value = {"api_key": "test-key-12345", "endpoint": "https://api.example.com"}

        try:
            # ACTUAL API call to create secret
            create_response = secrets_client.create_secret(
                Name=secret_name,
                SecretString=json.dumps(secret_value),
                Description="Integration test secret",
            )

            assert "ARN" in create_response
            secret_arn = create_response["ARN"]

            # ACTUAL API call to retrieve secret
            retrieve_response = secrets_client.get_secret_value(SecretId=secret_arn)

            assert "SecretString" in retrieve_response
            retrieved_value = json.loads(retrieve_response["SecretString"])
            assert retrieved_value == secret_value

        finally:
            # Cleanup: ACTUAL deletion (force delete)
            try:
                secrets_client.delete_secret(
                    SecretId=secret_name,
                    ForceDeleteWithoutRecovery=True,
                )
            except Exception:
                pass

    def test_secrets_manager_retrieve_nonexistent_secret_fails(
        self, aws_credentials
    ):
        """
        Test retrieving nonexistent secret FAILS with ACTUAL Secrets Manager.
        FAILS if: Credentials invalid or service down.
        """
        secrets_client = boto3.client(
            "secretsmanager",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )

        # ACTUAL API call that should fail
        with pytest.raises(ClientError):
            secrets_client.get_secret_value(SecretId="nonexistent-secret-12345")


@pytest.mark.integration
@pytest.mark.requires_aws
@pytest.mark.requires_internet
class TestAWSAuthenticationFailures:
    """Integration tests that verify authentication failures with ACTUAL AWS."""

    def test_invalid_aws_credentials_fail(self):
        """
        Test that INVALID AWS credentials cause API call to FAIL.
        Uses ACTUAL AWS service - should fail with authentication error.
        """
        s3_client = boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id="INVALID-KEY-12345",
            aws_secret_access_key="INVALID-SECRET-12345",
        )

        # ACTUAL API call with bad credentials - should fail
        with pytest.raises(ClientError) as exc_info:
            s3_client.list_buckets()

        # Verify it's an authentication error
        assert exc_info.value.response["Error"]["Code"] in [
            "InvalidAccessKeyId",
            "SignatureDoesNotMatch",
            "UnrecognizedClientException",
        ]

    def test_missing_permissions_fail(self, aws_credentials):
        """
        Test that operations without required permissions FAIL with ACTUAL AWS.
        Uses real credentials but operates on non-existent or restricted resource.
        """
        s3_client = boto3.client(
            "s3",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )

        # ACTUAL API call to non-existent bucket - should fail
        with pytest.raises(ClientError):
            s3_client.head_bucket(Bucket="nonexistent-bucket-12345-xyz")
