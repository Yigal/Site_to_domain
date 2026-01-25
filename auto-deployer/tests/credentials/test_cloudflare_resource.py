"""
Cloudflare Credentials Resource Test
Tests that Cloudflare credentials from .env have access to required resources.
One test per required Cloudflare resource.
"""

import pytest
import httpx


@pytest.mark.credentials
@pytest.mark.cloudflare
class TestCloudflareAuthenticationResource:
    """Test Cloudflare authentication resource."""

    def test_cloudflare_authentication(self, cloudflare_credentials):
        """
        Test that Cloudflare credentials are valid and authenticate successfully.
        REQUIRES: CLOUDFLARE_EMAIL and CLOUDFLARE_TOKEN environment variables
        """
        headers = {
            "X-Auth-Email": cloudflare_credentials["email"],
            "X-Auth-Key": cloudflare_credentials["token"],
            "Content-Type": "application/json",
        }

        try:
            response = httpx.get(
                "https://api.cloudflare.com/client/v4/user",
                headers=headers,
                timeout=10.0,
            )

            if response.status_code == 403:
                pytest.fail("❌ Cloudflare authentication failed - invalid token or email")
            elif response.status_code == 200:
                data = response.json()
                assert data.get("success") is True
                print("\n✅ Cloudflare Authentication: Credentials are valid")
            else:
                pytest.fail(f"❌ Unexpected status code: {response.status_code}")

        except Exception as e:
            pytest.fail(f"❌ Cloudflare authentication failed: {e}")


@pytest.mark.credentials
@pytest.mark.cloudflare
class TestCloudflareAccountResource:
    """Test Cloudflare account resource access."""

    def test_cloudflare_account_access(self, cloudflare_credentials):
        """
        Test that Cloudflare token can access specified account.
        REQUIRES: CLOUDFLARE_ACCOUNT_ID environment variable
        """
        headers = {
            "X-Auth-Email": cloudflare_credentials["email"],
            "X-Auth-Key": cloudflare_credentials["token"],
            "Content-Type": "application/json",
        }
        account_id = cloudflare_credentials["account_id"]

        try:
            response = httpx.get(
                f"https://api.cloudflare.com/client/v4/accounts/{account_id}",
                headers=headers,
                timeout=10.0,
            )

            if response.status_code == 403:
                pytest.fail(f"❌ Access denied to account {account_id}")
            elif response.status_code == 200:
                data = response.json()
                assert data.get("success") is True
                print(f"\n✅ Cloudflare Account Access: Can access account {account_id}")
            else:
                pytest.fail(f"❌ Unexpected status code: {response.status_code}")

        except Exception as e:
            pytest.fail(f"❌ Account access failed: {e}")


@pytest.mark.credentials
@pytest.mark.cloudflare
class TestCloudflarePagesResource:
    """Test Cloudflare Pages resource access."""

    def test_cloudflare_pages_access(self, cloudflare_credentials):
        """
        Test that Cloudflare token can access Pages projects.
        REQUIRES: CLOUDFLARE_ACCOUNT_ID environment variable
        """
        headers = {
            "X-Auth-Email": cloudflare_credentials["email"],
            "X-Auth-Key": cloudflare_credentials["token"],
            "Content-Type": "application/json",
        }
        account_id = cloudflare_credentials["account_id"]

        try:
            response = httpx.get(
                f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects",
                headers=headers,
                timeout=10.0,
            )

            if response.status_code == 403:
                pytest.fail("❌ Access denied to Pages projects")
            elif response.status_code == 200:
                data = response.json()
                assert data.get("success") is True
                print(f"\n✅ Cloudflare Pages Access: Can access Pages projects")
            else:
                pytest.fail(f"❌ Unexpected status code: {response.status_code}")

        except Exception as e:
            pytest.fail(f"❌ Pages access failed: {e}")
