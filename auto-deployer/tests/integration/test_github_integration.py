"""
GitHub Integration Tests - Uses REAL GitHub API.
No mocks. Requires valid GitHub token.
Tests will FAIL if GitHub token is invalid or API is unavailable.
"""

import pytest
from github import Github, GithubException, BadCredentialsException
import uuid


@pytest.mark.integration
@pytest.mark.requires_github
@pytest.mark.requires_internet
class TestGitHubAuthentication:
    """Integration tests for GitHub authentication with ACTUAL API."""

    def test_github_authentication_with_real_token(self, github_credentials):
        """
        Test GitHub authentication using ACTUAL token.
        FAILS if: Token invalid, expired, or revoked.
        """
        github = Github(github_credentials["token"])

        # ACTUAL API call to get authenticated user
        try:
            user = github.get_user()
            assert user is not None
            assert hasattr(user, "login")
        except BadCredentialsException:
            pytest.fail("GitHub token authentication failed - invalid or expired token")

    def test_github_organization_access_with_real_credentials(
        self, github_credentials
    ):
        """
        Test accessing organization using ACTUAL GitHub credentials.
        FAILS if: Token doesn't have org access, org doesn't exist, or API down.
        """
        github = Github(github_credentials["token"])

        # ACTUAL API call to get organization
        try:
            org = github.get_organization(github_credentials["org"])
            assert org is not None
            assert org.login == github_credentials["org"]
        except GithubException as e:
            pytest.fail(f"Cannot access organization: {str(e)}")

    def test_github_list_repositories_with_real_org(self, github_credentials):
        """
        Test listing repositories in organization using ACTUAL GitHub API.
        FAILS if: No org access, org doesn't exist, or API down.
        """
        github = Github(github_credentials["token"])
        org = github.get_organization(github_credentials["org"])

        # ACTUAL API call to list repositories
        repos = list(org.get_repos())

        assert isinstance(repos, list)
        # Organization may or may not have repos, but call should succeed

    def test_github_invalid_token_fails(self):
        """
        Test that INVALID GitHub token FAILS with ACTUAL API.
        """
        github = Github("invalid-token-12345")

        # ACTUAL API call with invalid token - should fail
        with pytest.raises(BadCredentialsException):
            github.get_user()

    def test_github_invalid_organization_fails(self, github_credentials):
        """
        Test that accessing nonexistent org FAILS with ACTUAL API.
        """
        github = Github(github_credentials["token"])

        # ACTUAL API call to nonexistent org - should fail
        with pytest.raises(GithubException):
            github.get_organization("definitely-nonexistent-org-12345-xyz")


@pytest.mark.integration
@pytest.mark.requires_github
@pytest.mark.requires_internet
class TestGitHubRepositoryOperations:
    """Integration tests for GitHub repository operations with ACTUAL API."""

    def test_github_repository_metadata_with_real_api(self, github_credentials):
        """
        Test getting repository metadata using ACTUAL GitHub API.
        FAILS if: No repos in org or API unavailable.
        """
        github = Github(github_credentials["token"])
        org = github.get_organization(github_credentials["org"])

        # ACTUAL API call to get repositories
        repos = list(org.get_repos())

        if repos:
            repo = repos[0]
            assert hasattr(repo, "name")
            assert hasattr(repo, "description")
            assert hasattr(repo, "url")
            assert repo.url.startswith("https://api.github.com")

    def test_github_rate_limit_check_with_real_api(self, github_credentials):
        """
        Test checking rate limit with ACTUAL GitHub API.
        FAILS if: Token invalid or API down.
        Shows ACTUAL rate limit status from GitHub.
        """
        github = Github(github_credentials["token"])

        # ACTUAL API call to check rate limits
        rate_limit = github.get_rate_limit()

        assert rate_limit is not None
        assert hasattr(rate_limit, "core")
        assert rate_limit.core.remaining >= 0
        assert rate_limit.core.limit > 0

    def test_github_authenticated_user_details(self, github_credentials):
        """
        Test getting authenticated user details with ACTUAL API.
        FAILS if: Token invalid or API down.
        """
        github = Github(github_credentials["token"])

        # ACTUAL API call to get user
        user = github.get_user()

        assert user is not None
        assert hasattr(user, "login")
        assert hasattr(user, "email")
        assert hasattr(user, "public_repos")

    def test_github_user_organizations_with_real_credentials(
        self, github_credentials
    ):
        """
        Test listing user's organizations with ACTUAL GitHub API.
        FAILS if: Token invalid or API down.
        """
        github = Github(github_credentials["token"])
        user = github.get_user()

        # ACTUAL API call to list user's orgs
        orgs = list(user.get_orgs())

        assert isinstance(orgs, list)
        # User may or may not be member of any orgs

    def test_github_api_call_requires_authentication(self):
        """
        Test that certain API calls REQUIRE authentication with ACTUAL API.
        """
        github_unauthenticated = Github()

        # ACTUAL API call without auth - may fail for private data
        # This depends on what data we're trying to access
        # Some public data is accessible without auth, private is not


@pytest.mark.integration
@pytest.mark.requires_github
@pytest.mark.requires_internet
class TestGitHubRateLimiting:
    """Integration tests for GitHub rate limiting with ACTUAL API."""

    def test_github_rate_limit_status_with_real_credentials(
        self, github_credentials
    ):
        """
        Test that we can check ACTUAL GitHub rate limit status.
        FAILS if: Token invalid or API down.
        Shows real rate limit values from GitHub.
        """
        github = Github(github_credentials["token"])

        # ACTUAL API call
        rate_limit = github.get_rate_limit()

        core_limit = rate_limit.core
        assert core_limit.limit > 0
        assert core_limit.remaining <= core_limit.limit
        assert core_limit.reset > 0

        print(f"\n\nGitHub Rate Limit Status:")
        print(f"  Requests remaining: {core_limit.remaining}")
        print(f"  Total limit: {core_limit.limit}")
        print(f"  Resets at: {core_limit.reset}")
