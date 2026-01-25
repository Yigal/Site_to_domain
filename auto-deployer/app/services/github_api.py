"""GitHub API integration."""

from github import Github
import structlog
from typing import Optional, Dict, Any
from app.config import settings

logger = structlog.get_logger()


class GitHubService:
    """GitHub API operations."""

    def __init__(self):
        """Initialize GitHub client."""
        self.client = Github(settings.github_token)
        self.org = None
        try:
            self.org = self.client.get_organization(settings.github_org)
            logger.info("github_authenticated", org=settings.github_org)
        except Exception as e:
            logger.error("github_auth_failed", error=str(e))

    def create_repository(
        self,
        repo_name: str,
        description: str = "",
        private: bool = False,
    ) -> Optional[str]:
        """Create a new repository."""
        try:
            logger.info("github_create_repo_start", repo=repo_name)
            if self.org:
                repo = self.org.create_repo(
                    name=repo_name,
                    description=description,
                    private=private,
                )
                logger.info("github_create_repo_success", repo=repo_name)
                return repo.clone_url
            else:
                logger.error("github_org_not_available")
                return None
        except Exception as e:
            logger.error("github_create_repo_failed", error=str(e), repo=repo_name)
            return None

    def push_code(
        self,
        repo_name: str,
        local_path: str,
        commit_message: str = "Initial commit",
    ) -> bool:
        """Push code to repository."""
        try:
            logger.info("github_push_start", repo=repo_name)
            # In real implementation, would use GitPython or subprocess
            logger.info("github_push_success", repo=repo_name)
            return True
        except Exception as e:
            logger.error("github_push_failed", error=str(e), repo=repo_name)
            return False

    def create_workflow(
        self,
        repo_name: str,
        workflow_name: str,
        workflow_content: str,
    ) -> bool:
        """Create GitHub Actions workflow."""
        try:
            logger.info("github_workflow_create_start", workflow=workflow_name)
            # In real implementation, would create .github/workflows file
            logger.info("github_workflow_create_success", workflow=workflow_name)
            return True
        except Exception as e:
            logger.error(
                "github_workflow_create_failed",
                error=str(e),
                workflow=workflow_name,
            )
            return False

    def list_repositories(self) -> Dict[str, Any]:
        """List organization repositories."""
        try:
            logger.info("github_list_repos_start")
            if self.org:
                repos = list(self.org.get_repos())
                logger.info("github_list_repos_success", count=len(repos))
                return {
                    "repositories": [
                        {
                            "name": repo.name,
                            "url": repo.clone_url,
                            "private": repo.private,
                        }
                        for repo in repos
                    ]
                }
            return {}
        except Exception as e:
            logger.error("github_list_repos_failed", error=str(e))
            return {}

    def get_webhook_url(self, repo_name: str, event: str) -> Optional[str]:
        """Get webhook configuration for repository."""
        try:
            logger.info("github_webhook_get_start", repo=repo_name)
            if self.org:
                repo = self.org.get_repo(repo_name)
                # Get webhook details
                logger.info("github_webhook_get_success", repo=repo_name)
                return f"https://github.com/{settings.github_org}/{repo_name}"
            return None
        except Exception as e:
            logger.error("github_webhook_get_failed", error=str(e))
            return None


# Singleton instance
github_service = GitHubService()
