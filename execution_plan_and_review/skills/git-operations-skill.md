# Git Operations Skill

## Description
Handles all Git operations required for repository management including cloning, committing, pushing, and configuration.

## Capabilities
- Clone remote repositories with various protocols (HTTPS, SSH)
- Configure git user name and email
- Initialize local git repositories
- Add remote origins to repositories
- Stage files for commit (add, add all)
- Create commits with custom messages
- Push to remote branches
- Manage branching and checkout operations
- Detach repositories from original history
- Handle authentication via PAT (Personal Access Token)

## Key Operations
- `git clone <url>` - Clone repository from GitHub or other sources
- `git init` - Initialize new repository
- `git remote add origin <url>` - Configure remote origin
- `git config user.name` - Set committer name (automation)
- `git config user.email` - Set committer email
- `git add .` - Stage all files for commit
- `git commit -m "message"` - Create commit
- `git push origin main` - Push to main branch
- `git rm -rf .git` - Detach from original history
- `git checkout -b <branch>` - Create and checkout branch

## Environment Setup
- Git authentication via GitHub PAT in HTTPS URL
- Automation user identity: `Auto-Deployer <noreply@deployer.local>`
- Default branch: main

## Subprocess Execution
- Wrapped in error-handling subprocess calls
- Captures stdout/stderr for diagnostics
- Returns exit codes for validation
- Implements timeout handling

## Integrations
- Used by GitHub Repository Agent
- Executed from workspace directory
- Supports multi-branch deployments
- Part of two-push deployment strategy

## Error Handling
- Git not installed
- Authentication failures with repository
- Network connectivity issues
- File permission errors
- Repository state conflicts

## Security Considerations
- PAT never logged or printed
- Git commands executed with restricted permissions
- Temporary credentials not cached
- Repository cleanup on failure
