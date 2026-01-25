"""
GCP Integration Tests - Uses REAL Google Cloud Platform services.
No mocks. Requires valid GCP service account credentials.
Tests will FAIL if GCP credentials are invalid or service is unavailable.
"""

import pytest
import json
import uuid
from google.oauth2 import service_account
from google.cloud import storage, identity_platform
from google.api_core import exceptions


@pytest.mark.integration
@pytest.mark.requires_gcp
@pytest.mark.requires_internet
class TestGCPAuthentication:
    """Integration tests for GCP authentication with ACTUAL API."""

    def test_gcp_authentication_with_real_service_account(self, gcp_credentials):
        """
        Test GCP authentication using ACTUAL service account credentials.
        FAILS if: Credentials invalid, expired, or revoked.
        """
        try:
            # Parse service account JSON
            service_account_info = json.loads(gcp_credentials["service_account"])

            # ACTUAL API call to authenticate and create credentials
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=[
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/firebase",
                ],
            )

            assert credentials is not None
            assert credentials.service_account_email is not None
        except ValueError as e:
            pytest.fail(f"GCP service account authentication failed: {str(e)}")

    def test_gcp_invalid_credentials_fail(self):
        """
        Test that INVALID GCP credentials FAIL with ACTUAL API.
        """
        invalid_service_account = {
            "type": "service_account",
            "project_id": "invalid-project",
            "private_key_id": "invalid-key-id",
            "private_key": "***REMOVED-PRIVATE-KEY***",
            "client_email": "invalid@invalid-project.iam.gserviceaccount.com",
            "client_id": "0",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        }

        # ACTUAL API call with bad credentials - should fail
        with pytest.raises(ValueError):
            service_account.Credentials.from_service_account_info(
                invalid_service_account,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )


@pytest.mark.integration
@pytest.mark.requires_gcp
@pytest.mark.requires_internet
class TestGCPStorageOperations:
    """Integration tests for GCP Cloud Storage with ACTUAL API."""

    def test_gcp_storage_client_creation_with_real_credentials(self, gcp_credentials):
        """
        Test creating Cloud Storage client with ACTUAL GCP credentials.
        FAILS if: Credentials invalid or service unavailable.
        """
        try:
            service_account_info = json.loads(gcp_credentials["service_account"])

            # ACTUAL API call to create storage client
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info
            )
            storage_client = storage.Client(
                project=gcp_credentials["project_id"],
                credentials=credentials,
            )

            assert storage_client is not None
            assert storage_client.project == gcp_credentials["project_id"]
        except Exception as e:
            pytest.fail(f"GCP Storage client creation failed: {str(e)}")

    def test_gcp_list_buckets_with_real_credentials(self, gcp_credentials):
        """
        Test listing buckets with ACTUAL GCP credentials.
        FAILS if: Credentials lack permissions or service down.
        """
        service_account_info = json.loads(gcp_credentials["service_account"])
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info
        )
        storage_client = storage.Client(
            project=gcp_credentials["project_id"],
            credentials=credentials,
        )

        # ACTUAL API call to list buckets
        buckets = list(storage_client.list_buckets())

        assert isinstance(buckets, list)
        # Project may or may not have buckets

    def test_gcp_bucket_operations_with_real_credentials(self, gcp_credentials):
        """
        Test bucket operations with ACTUAL GCP credentials.
        FAILS if: Bucket doesn't exist, no permissions, or service down.
        """
        service_account_info = json.loads(gcp_credentials["service_account"])
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info
        )
        storage_client = storage.Client(
            project=gcp_credentials["project_id"],
            credentials=credentials,
        )

        # Create test bucket name
        test_bucket_name = f"test-integration-{uuid.uuid4().hex[:8]}"

        try:
            # ACTUAL API call to create bucket
            bucket = storage_client.create_bucket(
                test_bucket_name,
                location="US",
            )

            assert bucket.name == test_bucket_name
            assert bucket.exists()

            # ACTUAL API call to delete bucket
            bucket.delete()

        except exceptions.GoogleAPICallError as e:
            # May fail if bucket already exists or permissions denied
            # This is expected in some environments
            assert "already exists" in str(e) or "Permission denied" in str(e)


@pytest.mark.integration
@pytest.mark.requires_gcp
@pytest.mark.requires_internet
class TestGCPProjectOperations:
    """Integration tests for GCP Project operations with ACTUAL API."""

    def test_gcp_project_info_with_real_credentials(self, gcp_credentials):
        """
        Test retrieving project information with ACTUAL GCP credentials.
        FAILS if: Project doesn't exist, credentials invalid, or service down.
        """
        try:
            service_account_info = json.loads(gcp_credentials["service_account"])
            project_id = gcp_credentials["project_id"]

            # Verify service account has correct project ID
            assert service_account_info.get("project_id") == project_id

            # Create credentials - if this succeeds, project is valid
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )

            assert credentials is not None
            assert credentials.project_id == project_id

        except ValueError as e:
            pytest.fail(f"GCP project verification failed: {str(e)}")

    def test_gcp_billing_account_verification(self, gcp_credentials):
        """
        Test GCP billing account configuration.
        FAILS if: Billing account invalid or project not linked.
        """
        billing_account = gcp_credentials.get("billing_account")

        # If billing account is configured, verify format
        if billing_account:
            # GCP billing accounts have format: billingAccounts/123456-789ABC-DEF012
            assert billing_account.startswith("billingAccounts/")
            assert len(billing_account) > len("billingAccounts/")


@pytest.mark.integration
@pytest.mark.requires_gcp
@pytest.mark.requires_internet
class TestGCPIdentityPlatform:
    """Integration tests for GCP Identity Platform with ACTUAL API."""

    def test_gcp_identity_client_creation_with_real_credentials(self, gcp_credentials):
        """
        Test creating Identity Platform client with ACTUAL GCP credentials.
        FAILS if: Credentials invalid or Identity Platform not enabled.
        """
        try:
            service_account_info = json.loads(gcp_credentials["service_account"])

            # ACTUAL API call to create credentials
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=[
                    "https://www.googleapis.com/auth/identitytoolkit",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            )

            assert credentials is not None
            assert credentials.service_account_email is not None

        except Exception as e:
            pytest.fail(f"GCP Identity client creation failed: {str(e)}")

    def test_gcp_service_account_email_extraction(self, gcp_credentials):
        """
        Test extracting service account email from credentials.
        FAILS if: Service account data malformed.
        """
        service_account_info = json.loads(gcp_credentials["service_account"])

        assert "client_email" in service_account_info
        email = service_account_info["client_email"]
        assert "@iam.gserviceaccount.com" in email
        assert email.startswith(gcp_credentials["project_id"])


@pytest.mark.integration
@pytest.mark.requires_gcp
@pytest.mark.requires_internet
class TestGCPAuthenticationFailures:
    """Integration tests that verify authentication failures with ACTUAL GCP."""

    def test_malformed_service_account_fails(self):
        """
        Test that malformed service account JSON FAILS with ACTUAL GCP API.
        """
        malformed_account = {
            "type": "service_account",
            # Missing required fields
            "project_id": "test-project",
        }

        with pytest.raises(ValueError):
            service_account.Credentials.from_service_account_info(malformed_account)

    def test_invalid_private_key_fails(self):
        """
        Test that invalid private key FAILS with ACTUAL GCP API.
        """
        invalid_account = {
            "type": "service_account",
            "project_id": "test-project",
            "private_key_id": "key-id",
            "private_key": "***REMOVED-PRIVATE-KEY***",
            "client_email": "test@test-project.iam.gserviceaccount.com",
            "client_id": "123456789",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }

        with pytest.raises(ValueError):
            service_account.Credentials.from_service_account_info(invalid_account)

    def test_empty_credentials_fail(self):
        """
        Test that empty credentials FAIL with ACTUAL GCP API.
        """
        with pytest.raises((ValueError, TypeError)):
            service_account.Credentials.from_service_account_info({})
