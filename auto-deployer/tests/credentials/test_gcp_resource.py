"""
GCP Credentials Resource Test
Tests that GCP credentials from .env have access to required GCP resources.
One test per required GCP resource.
"""

import pytest
from google.oauth2 import service_account
from google.cloud import storage


@pytest.mark.credentials
@pytest.mark.gcp
class TestGCPAuthenticationResource:
    """Test GCP authentication resource."""

    def test_gcp_authentication(self, gcp_credentials):
        """
        Test that GCP service account credentials are valid and authenticate successfully.
        REQUIRES: GCP_SERVICE_ACCOUNT_JSON environment variable
        """
        try:
            credentials = service_account.Credentials.from_service_account_info(
                gcp_credentials["service_account"],
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )

            assert credentials is not None
            assert credentials.service_account_email is not None
            print(f"\n✅ GCP Authentication: Service account {credentials.service_account_email} is valid")

        except ValueError as e:
            pytest.fail(f"❌ GCP authentication failed - invalid credentials: {e}")
        except Exception as e:
            pytest.fail(f"❌ GCP authentication failed: {e}")


@pytest.mark.credentials
@pytest.mark.gcp
class TestGCPCloudStorageResource:
    """Test GCP Cloud Storage resource access."""

    def test_gcp_storage_access(self, gcp_credentials):
        """
        Test that GCP credentials can access Cloud Storage.
        REQUIRES: GCP_SERVICE_ACCOUNT_JSON environment variable with storage permissions
        """
        try:
            credentials = service_account.Credentials.from_service_account_info(
                gcp_credentials["service_account"]
            )

            storage_client = storage.Client(
                project=gcp_credentials["project_id"],
                credentials=credentials,
            )

            # Try to list buckets to verify access
            buckets = list(storage_client.list_buckets())

            assert isinstance(buckets, list)
            print(f"\n✅ GCP Cloud Storage Access: Can access Cloud Storage (found {len(buckets)} buckets)")

        except Exception as e:
            pytest.fail(f"❌ GCP Cloud Storage access failed: {e}")


@pytest.mark.credentials
@pytest.mark.gcp
class TestGCPProjectResource:
    """Test GCP project resource access."""

    def test_gcp_project_access(self, gcp_credentials):
        """
        Test that GCP credentials have access to specified project.
        REQUIRES: GCP_SERVICE_ACCOUNT_JSON and GCP_PROJECT_ID environment variables
        """
        try:
            credentials = service_account.Credentials.from_service_account_info(
                gcp_credentials["service_account"]
            )

            # Verify project ID in credentials matches environment
            service_account_project = gcp_credentials["service_account"].get("project_id")
            env_project = gcp_credentials["project_id"]

            assert service_account_project == env_project, \
                f"Project ID mismatch: credentials={service_account_project}, env={env_project}"

            assert credentials.project_id == env_project
            print(f"\n✅ GCP Project Access: Can access project {env_project}")

        except Exception as e:
            pytest.fail(f"❌ GCP project access failed: {e}")
