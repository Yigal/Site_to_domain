"""
GitHub Credentials Resource Test
Tests that GitHub credentials from .env have access to required GitHub resources.
One test per required GitHub resource.
"""

import pytest
from github import Github, BadCredentialsException, GithubException


@pytest.mark.credentials
@pytest.mark.github
class TestGitHubAuthenticationResource:
    """Test GitHub authentication resource."""

    def test_github_authentication(self, github_credentials):
        """
        Test that GitHub token is valid and authenticates successfully.
        REQUIRES: GITHUB_TOKEN environment variable
        """
        github = Github(github_credentials["token"])

        try:
            user = github.get_user()
            assert user is not None
            assert hasattr(user, "login")
            print(f"\n✅ GitHub Authentication: Authenticated as {user.login}")
        except BadCredentialsException:
            pytest.fail("❌ GitHub token is invalid or expired")
        except Exception as e:
            pytest.fail(f"❌ GitHub authentication failed: {e}")


@pytest.mark.credentials
@pytest.mark.github
class TestGitHubOrganizationResource:
    """Test GitHub organization resource access."""

    def test_github_organization_access(self, github_credentials):
        """
        Test that GitHub token can access specified organization.
        REQUIRES: GITHUB_ORG environment variable and organization membership
        """
        github = Github(github_credentials["token"])
        org_name = github_credentials["org"]

        try:
            org = github.get_organization(org_name)
            assert org is not None
            assert org.login == org_name
            print(f"\n✅ GitHub Organization Access: Can access {org_name}")
        except GithubException as e:
            pytest.fail(f"❌ Cannot access organization {org_name}: {e}")
        except Exception as e:
            pytest.fail(f"❌ Organization access failed: {e}")


@pytest.mark.credentials
@pytest.mark.github
class TestGitHubRepositoryResource:
    """Test GitHub repository resource access."""

    def test_github_repository_listing(self, github_credentials):
        """
        Test that GitHub token can list repositories in organization.
        REQUIRES: GITHUB_ORG environment variable
        """
        github = Github(github_credentials["token"])
        org_name = github_credentials["org"]

        try:
            org = github.get_organization(org_name)
            repos = list(org.get_repos(per_page=1))
            # Organization may have 0 or more repos
            assert isinstance(repos, list)
            print(f"\n✅ GitHub Repository Access: Can list repos in {org_name}")
        except Exception as e:
            pytest.fail(f"❌ Repository listing failed: {e}")
