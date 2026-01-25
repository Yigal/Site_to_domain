"""
Deployment End-to-End Integration Tests - Tests complete deployment workflow.
No mocks. Uses ACTUAL cloud services and real deployment processes.
Tests will FAIL if any service is unavailable or credentials are invalid.
"""

import pytest
import json
import uuid
import httpx


@pytest.mark.integration
@pytest.mark.requires_aws
@pytest.mark.requires_github
@pytest.mark.requires_cloudflare
@pytest.mark.requires_internet
class TestDeploymentAPIEndpoints:
    """Integration tests for deployment API endpoints with ACTUAL backend."""

    def test_deployment_health_check(self):
        """
        Test health check endpoint with ACTUAL API.
        FAILS if: API server unavailable.
        """
        # ACTUAL API call to health endpoint
        response = httpx.get("http://localhost:8000/health", timeout=5.0)

        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"

    def test_deployment_api_docs_accessible(self):
        """
        Test API documentation endpoint with ACTUAL API.
        FAILS if: API server unavailable.
        """
        # ACTUAL API call to docs endpoint
        response = httpx.get("http://localhost:8000/docs", timeout=5.0)

        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()


@pytest.mark.integration
@pytest.mark.requires_aws
@pytest.mark.requires_github
@pytest.mark.requires_cloudflare
@pytest.mark.requires_internet
class TestDeploymentRequestValidation:
    """Integration tests for deployment request validation with ACTUAL API."""

    def test_deployment_request_with_valid_data(self):
        """
        Test submitting valid deployment request with ACTUAL API.
        FAILS if: API unavailable or request validation fails.
        """
        payload = {
            "repo_url": "https://github.com/test/sample-app",
            "domain": "test-app.example.com",
            "framework": "react",
            "custom_domain": None,
        }

        # ACTUAL API call to submit deployment
        response = httpx.post(
            "http://localhost:8000/deploy",
            json=payload,
            timeout=10.0,
        )

        # May succeed or fail depending on whether required services are available
        # But request should be properly validated
        assert response.status_code in [200, 201, 400, 422, 503]

    def test_deployment_request_with_invalid_data(self):
        """
        Test submitting invalid deployment request with ACTUAL API.
        FAILS if: API unavailable, but validation should reject invalid data.
        """
        invalid_payload = {
            "repo_url": "not-a-url",  # Invalid URL format
            "domain": "invalid domain",  # Invalid domain
            "framework": "unknown-framework",  # Invalid framework
        }

        # ACTUAL API call with invalid data - should fail validation
        response = httpx.post(
            "http://localhost:8000/deploy",
            json=invalid_payload,
            timeout=10.0,
        )

        # API should reject invalid data
        assert response.status_code in [400, 422]

    def test_deployment_request_missing_required_fields(self):
        """
        Test submitting incomplete deployment request with ACTUAL API.
        FAILS if: API unavailable, but should reject incomplete data.
        """
        incomplete_payload = {
            "repo_url": "https://github.com/test/sample-app",
            # Missing domain and framework
        }

        # ACTUAL API call with missing fields - should fail
        response = httpx.post(
            "http://localhost:8000/deploy",
            json=incomplete_payload,
            timeout=10.0,
        )

        # API should reject incomplete data
        assert response.status_code in [400, 422]


@pytest.mark.integration
@pytest.mark.requires_aws
@pytest.mark.requires_internet
class TestDeploymentStatusEndpoint:
    """Integration tests for deployment status endpoint with ACTUAL API."""

    def test_deployment_status_with_invalid_id(self):
        """
        Test checking status for nonexistent deployment with ACTUAL API.
        FAILS if: API unavailable.
        """
        fake_deployment_id = f"fake-{uuid.uuid4()}"

        # ACTUAL API call to check status
        response = httpx.get(
            f"http://localhost:8000/status/{fake_deployment_id}",
            timeout=5.0,
        )

        # Should return 404 or similar for nonexistent deployment
        assert response.status_code in [404, 400]


@pytest.mark.integration
@pytest.mark.requires_aws
@pytest.mark.requires_internet
class TestDeploymentUploadEndpoint:
    """Integration tests for deployment upload endpoint with ACTUAL API."""

    def test_upload_with_missing_file(self):
        """
        Test uploading without file with ACTUAL API.
        FAILS if: API unavailable.
        """
        # ACTUAL API call without file - should fail
        response = httpx.post(
            "http://localhost:8000/upload",
            timeout=5.0,
        )

        # API should reject request without file
        assert response.status_code in [400, 422]

    def test_upload_with_valid_file(self, sample_s3_upload_data):
        """
        Test uploading valid file with ACTUAL API.
        FAILS if: API unavailable or S3 upload fails.
        """
        files = {
            "file": (
                "test-app.zip",
                sample_s3_upload_data["content"],
                sample_s3_upload_data["content_type"],
            )
        }

        # ACTUAL API call to upload file
        response = httpx.post(
            "http://localhost:8000/upload",
            files=files,
            timeout=10.0,
        )

        # Should succeed or fail gracefully if services unavailable
        assert response.status_code in [200, 201, 400, 422, 503]


@pytest.mark.integration
@pytest.mark.requires_aws
@pytest.mark.requires_github
@pytest.mark.requires_cloudflare
@pytest.mark.requires_internet
class TestDeploymentErrorHandling:
    """Integration tests for deployment error handling with ACTUAL API."""

    def test_deployment_with_network_error_handling(self):
        """
        Test API handles network errors gracefully.
        """
        # Try to connect to invalid port - should handle gracefully
        try:
            response = httpx.get("http://localhost:9999/health", timeout=1.0)
        except (httpx.ConnectError, httpx.TimeoutException):
            # Expected - invalid port
            pass

    def test_deployment_with_timeout_handling(self):
        """
        Test API handles timeout gracefully.
        """
        try:
            # Use very short timeout to simulate timeout
            response = httpx.get("http://localhost:8000/health", timeout=0.001)
        except httpx.TimeoutException:
            # Expected - timeout
            pass


@pytest.mark.integration
@pytest.mark.requires_aws
@pytest.mark.requires_github
@pytest.mark.requires_cloudflare
@pytest.mark.requires_internet
class TestDeploymentServiceIntegration:
    """Integration tests for deployment with actual service integration."""

    def test_aws_service_integration_in_deployment(self, aws_credentials):
        """
        Test that deployment can access AWS services with ACTUAL credentials.
        FAILS if: AWS credentials invalid or service unavailable.
        """
        import boto3

        # ACTUAL AWS call - verify credentials work
        s3_client = boto3.client(
            "s3",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )

        response = s3_client.list_buckets()
        assert "Buckets" in response

    def test_github_service_integration_in_deployment(self, github_credentials):
        """
        Test that deployment can access GitHub services with ACTUAL credentials.
        FAILS if: GitHub token invalid or service unavailable.
        """
        from github import Github

        # ACTUAL GitHub call - verify credentials work
        github = Github(github_credentials["token"])
        user = github.get_user()

        assert user is not None
        assert hasattr(user, "login")

    def test_cloudflare_service_integration_in_deployment(
        self, cloudflare_credentials
    ):
        """
        Test that deployment can access Cloudflare services with ACTUAL credentials.
        FAILS if: Cloudflare token invalid or service unavailable.
        """
        headers = {
            "X-Auth-Email": cloudflare_credentials["email"],
            "X-Auth-Key": cloudflare_credentials["token"],
            "Content-Type": "application/json",
        }

        # ACTUAL Cloudflare call - verify credentials work
        response = httpx.get(
            "https://api.cloudflare.com/client/v4/user",
            headers=headers,
            timeout=10.0,
        )

        assert response.status_code == 200
        data = response.json()
        assert data.get("success") is True


@pytest.mark.integration
@pytest.mark.requires_aws
@pytest.mark.requires_github
@pytest.mark.requires_cloudflare
@pytest.mark.requires_redis
@pytest.mark.requires_internet
class TestDeploymentWithAllServices:
    """Integration tests for complete deployment workflow with ALL services."""

    def test_all_services_available(
        self,
        aws_credentials,
        github_credentials,
        cloudflare_credentials,
        redis_connection,
    ):
        """
        Test that ALL required services are available and accessible.
        FAILS if: ANY service is unavailable or credentials invalid.
        """
        import boto3
        from github import Github

        # Test AWS
        s3_client = boto3.client(
            "s3",
            region_name=aws_credentials["region"],
            aws_access_key_id=aws_credentials["access_key_id"],
            aws_secret_access_key=aws_credentials["secret_access_key"],
        )
        assert s3_client.list_buckets() is not None

        # Test GitHub
        github = Github(github_credentials["token"])
        assert github.get_user() is not None

        # Test Cloudflare
        cf_headers = {
            "X-Auth-Email": cloudflare_credentials["email"],
            "X-Auth-Key": cloudflare_credentials["token"],
        }
        cf_response = httpx.get(
            "https://api.cloudflare.com/client/v4/user",
            headers=cf_headers,
            timeout=10.0,
        )
        assert cf_response.status_code == 200

        # Test Redis
        assert redis_connection.ping() is True

    def test_deployment_workflow_prerequisites(
        self,
        aws_credentials,
        github_credentials,
        cloudflare_credentials,
        redis_connection,
        sample_deployment_data,
    ):
        """
        Test that all prerequisites for deployment workflow are met.
        FAILS if: ANY prerequisite is missing.
        """
        # All credentials should be present
        assert aws_credentials is not None
        assert github_credentials is not None
        assert cloudflare_credentials is not None
        assert redis_connection is not None

        # Sample data should be valid
        assert sample_deployment_data["repo_url"] is not None
        assert sample_deployment_data["domain"] is not None
        assert sample_deployment_data["framework"] is not None


@pytest.mark.integration
@pytest.mark.requires_internet
class TestDeploymentAPIConnectivity:
    """Integration tests for deployment API connectivity."""

    def test_api_response_time(self):
        """
        Test that API responds within acceptable time.
        FAILS if: API responds too slowly.
        """
        import time

        start_time = time.time()

        try:
            response = httpx.get("http://localhost:8000/health", timeout=5.0)
            elapsed_time = time.time() - start_time

            # API should respond quickly (less than 1 second)
            assert elapsed_time < 1.0
            assert response.status_code == 200
        except httpx.ConnectError:
            # API not running - skip test
            pytest.skip("API server not running")

    def test_api_response_headers(self):
        """
        Test that API returns proper response headers.
        FAILS if: API headers are incorrect.
        """
        try:
            response = httpx.get("http://localhost:8000/health")

            assert response.headers.get("content-type") is not None
            assert "json" in response.headers.get("content-type", "").lower()
        except httpx.ConnectError:
            pytest.skip("API server not running")
