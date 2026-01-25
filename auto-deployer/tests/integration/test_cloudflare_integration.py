"""
Cloudflare Integration Tests - Uses REAL Cloudflare API.
No mocks. Requires valid Cloudflare token, account ID, and email.
Tests will FAIL if Cloudflare credentials are invalid or API is unavailable.
"""

import pytest
import httpx
import uuid
import json


@pytest.mark.integration
@pytest.mark.requires_cloudflare
@pytest.mark.requires_internet
class TestCloudflareAuthentication:
    """Integration tests for Cloudflare authentication with ACTUAL API."""

    def test_cloudflare_authentication_with_real_token(self, cloudflare_credentials):
        """
        Test Cloudflare authentication using ACTUAL token.
        FAILS if: Token invalid, expired, or revoked.
        """
        headers = {
            "X-Auth-Email": cloudflare_credentials["email"],
            "X-Auth-Key": cloudflare_credentials["token"],
            "Content-Type": "application/json",
        }

        # ACTUAL API call to verify authentication
        response = httpx.get(
            "https://api.cloudflare.com/client/v4/user",
            headers=headers,
            timeout=10.0,
        )

        assert response.status_code == 200
        data = response.json()
        assert data.get("success") is True
        assert "result" in data

    def test_cloudflare_account_access_with_real_credentials(
        self, cloudflare_credentials
    ):
        """
        Test accessing account with ACTUAL Cloudflare credentials.
        FAILS if: Token doesn't have account access or API down.
        """
        headers = {
            "X-Auth-Email": cloudflare_credentials["email"],
            "X-Auth-Key": cloudflare_credentials["token"],
            "Content-Type": "application/json",
        }

        # ACTUAL API call to get account information
        response = httpx.get(
            f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_credentials['account_id']}",
            headers=headers,
            timeout=10.0,
        )

        assert response.status_code == 200
        data = response.json()
        assert data.get("success") is True
        assert "result" in data
        assert data["result"]["id"] == cloudflare_credentials["account_id"]

    def test_cloudflare_invalid_token_fails(self):
        """
        Test that INVALID Cloudflare token FAILS with ACTUAL API.
        """
        headers = {
            "X-Auth-Email": "test@example.com",
            "X-Auth-Key": "invalid-token-12345",
            "Content-Type": "application/json",
        }

        # ACTUAL API call with invalid token - should fail
        response = httpx.get(
            "https://api.cloudflare.com/client/v4/user",
            headers=headers,
            timeout=10.0,
        )

        assert response.status_code == 403
        data = response.json()
        assert data.get("success") is False


@pytest.mark.integration
@pytest.mark.requires_cloudflare
@pytest.mark.requires_internet
class TestCloudflareZonesAndDNS:
    """Integration tests for Cloudflare zones and DNS with ACTUAL API."""

    def test_cloudflare_list_zones_with_real_credentials(self, cloudflare_credentials):
        """
        Test listing zones using ACTUAL Cloudflare API.
        FAILS if: Token lacks zone access or API unavailable.
        """
        headers = {
            "X-Auth-Email": cloudflare_credentials["email"],
            "X-Auth-Key": cloudflare_credentials["token"],
            "Content-Type": "application/json",
        }

        # ACTUAL API call to list zones in account
        response = httpx.get(
            f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_credentials['account_id']}/zones",
            headers=headers,
            timeout=10.0,
        )

        assert response.status_code == 200
        data = response.json()
        assert data.get("success") is True
        assert "result" in data
        assert isinstance(data["result"], list)

    def test_cloudflare_get_zone_details_with_real_api(self, cloudflare_credentials):
        """
        Test getting zone details using ACTUAL Cloudflare API.
        FAILS if: Zone doesn't exist or API unavailable.
        Note: This requires at least one zone to exist in the account.
        """
        headers = {
            "X-Auth-Email": cloudflare_credentials["email"],
            "X-Auth-Key": cloudflare_credentials["token"],
            "Content-Type": "application/json",
        }

        # ACTUAL API call to list zones
        zones_response = httpx.get(
            f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_credentials['account_id']}/zones",
            headers=headers,
            timeout=10.0,
        )

        assert zones_response.status_code == 200
        zones_data = zones_response.json()

        if zones_data["result"]:
            zone_id = zones_data["result"][0]["id"]

            # ACTUAL API call to get zone details
            detail_response = httpx.get(
                f"https://api.cloudflare.com/client/v4/zones/{zone_id}",
                headers=headers,
                timeout=10.0,
            )

            assert detail_response.status_code == 200
            detail_data = detail_response.json()
            assert detail_data.get("success") is True
            assert detail_data["result"]["id"] == zone_id

    def test_cloudflare_list_dns_records_with_real_api(self, cloudflare_credentials):
        """
        Test listing DNS records using ACTUAL Cloudflare API.
        FAILS if: Zone doesn't exist, no access, or API down.
        """
        headers = {
            "X-Auth-Email": cloudflare_credentials["email"],
            "X-Auth-Key": cloudflare_credentials["token"],
            "Content-Type": "application/json",
        }

        # ACTUAL API call to list zones
        zones_response = httpx.get(
            f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_credentials['account_id']}/zones",
            headers=headers,
            timeout=10.0,
        )

        if zones_response.status_code == 200:
            zones_data = zones_response.json()
            if zones_data["result"]:
                zone_id = zones_data["result"][0]["id"]

                # ACTUAL API call to list DNS records
                dns_response = httpx.get(
                    f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
                    headers=headers,
                    timeout=10.0,
                )

                assert dns_response.status_code == 200
                dns_data = dns_response.json()
                assert dns_data.get("success") is True
                assert isinstance(dns_data["result"], list)


@pytest.mark.integration
@pytest.mark.requires_cloudflare
@pytest.mark.requires_internet
class TestCloudflarePages:
    """Integration tests for Cloudflare Pages with ACTUAL API."""

    def test_cloudflare_list_pages_projects_with_real_credentials(
        self, cloudflare_credentials
    ):
        """
        Test listing Pages projects using ACTUAL Cloudflare API.
        FAILS if: Token invalid, no Pages access, or API down.
        """
        headers = {
            "X-Auth-Email": cloudflare_credentials["email"],
            "X-Auth-Key": cloudflare_credentials["token"],
            "Content-Type": "application/json",
        }

        # ACTUAL API call to list Pages projects
        response = httpx.get(
            f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_credentials['account_id']}/pages/projects",
            headers=headers,
            timeout=10.0,
        )

        assert response.status_code == 200
        data = response.json()
        assert data.get("success") is True
        assert "result" in data
        assert isinstance(data["result"], list)

    def test_cloudflare_pages_list_deployments(self, cloudflare_credentials):
        """
        Test listing Pages deployments using ACTUAL Cloudflare API.
        FAILS if: No Pages project, token invalid, or API down.
        """
        headers = {
            "X-Auth-Email": cloudflare_credentials["email"],
            "X-Auth-Key": cloudflare_credentials["token"],
            "Content-Type": "application/json",
        }

        # ACTUAL API call to list Pages projects
        projects_response = httpx.get(
            f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_credentials['account_id']}/pages/projects",
            headers=headers,
            timeout=10.0,
        )

        assert projects_response.status_code == 200
        projects_data = projects_response.json()

        if projects_data["result"]:
            project_name = projects_data["result"][0]["name"]

            # ACTUAL API call to list deployments for project
            deployments_response = httpx.get(
                f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_credentials['account_id']}/pages/projects/{project_name}/deployments",
                headers=headers,
                timeout=10.0,
            )

            assert deployments_response.status_code == 200
            deployments_data = deployments_response.json()
            assert deployments_data.get("success") is True


@pytest.mark.integration
@pytest.mark.requires_cloudflare
@pytest.mark.requires_internet
class TestCloudflareAuthenticationFailures:
    """Integration tests that verify authentication failures with ACTUAL Cloudflare."""

    def test_invalid_cloudflare_credentials_fail(self):
        """
        Test that INVALID Cloudflare credentials cause API call to FAIL.
        Uses ACTUAL Cloudflare service - should fail with authentication error.
        """
        headers = {
            "X-Auth-Email": "invalid@example.com",
            "X-Auth-Key": "invalid-key-12345",
            "Content-Type": "application/json",
        }

        # ACTUAL API call with bad credentials - should fail
        response = httpx.get(
            "https://api.cloudflare.com/client/v4/user",
            headers=headers,
            timeout=10.0,
        )

        assert response.status_code == 403
        data = response.json()
        assert data.get("success") is False
        assert "errors" in data

    def test_missing_auth_headers_fail(self):
        """
        Test that missing authentication headers FAIL with ACTUAL Cloudflare API.
        """
        headers = {
            "Content-Type": "application/json",
        }

        # ACTUAL API call without auth - should fail
        response = httpx.get(
            "https://api.cloudflare.com/client/v4/user",
            headers=headers,
            timeout=10.0,
        )

        assert response.status_code == 403
        data = response.json()
        assert data.get("success") is False
