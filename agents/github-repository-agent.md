# GitHub Repository Agent

## Purpose
Manages the complete lifecycle of GitHub repository creation, code pushing, and cleanup for the deployment process.

## Responsibilities
- Create new repositories in target GitHub organization
- Validate repository doesn't already exist
- Configure Git credentials and remote URLs
- Push transformed code to repository
- Handle git commit and branch operations
- Delete repositories during rollback scenarios
- Execute Git operations via subprocess

## Key Functions
- `create_repository()` - Create new repo in organization
- `push_code()` - Initialize git, configure, and push
- `delete_repository()` - Remove repo (rollback)
- `check_repo_exists()` - Verify repo availability
- `_get_github_client()` - Initialize PyGithub client
- `_run_git_command()` - Execute git CLI commands

## Authentication
- Fine-grained GitHub Personal Access Token (from AWS Secrets Manager)
- Token scopes: Administration (Read/Write), Contents (Read/Write), Metadata (Read-only)

## Integration Points
- Receives transformed code from Code Transformation Agent
- Receives deployment configuration from Saga Orchestration Agent
- Links to Cloudflare Pages Agent for Pages project creation
- Supports rollback from Saga Orchestration Agent

## Error Handling
- Repository already exists
- Authentication failures
- Git command execution errors
- Network connectivity issues
- Push failures due to permissions

## Notes
- Creates organization-scoped repositories only
- Sets automation user as git committer
- Detaches from original repository history
- Supports two-push strategy (initial + config injection)
