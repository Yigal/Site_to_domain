# GitHub API Integration Skill

## Description
Provides programmatic access to GitHub operations through the PyGithub library for repository management and organization control.

## Capabilities
- Authenticate with GitHub Personal Access Tokens
- Create repositories within organizations
- List repositories (organizations and users)
- Check repository existence
- Delete repositories
- Manage repository settings and visibility
- Access organization information
- Query user permissions
- Handle GitHub API rate limits and pagination
- Support fine-grained token scopes

## Key Operations
- `get_organization(org_name)` - Retrieve organization object
- `create_repo(name, description, private)` - Create repository
- `get_repo(org_name, repo_name)` - Get repository object
- `delete_repo(org_name, repo_name)` - Delete repository
- `list_repos(org)` - List organization repositories
- `get_user()` - Get authenticated user
- `get_user_permissions()` - Check token permissions
- `get_rate_limit()` - Check API rate limits

## Authentication
- GitHub Personal Access Token (Fine-grained)
- Token scopes: Administration (R/W), Contents (R/W), Metadata (Read)
- Resource owner: Organization (not personal)
- Token validity check on initialization

## Repository Configuration
- Visibility: Private or Public (configurable)
- Description: Automated deployment via Auto-Deployer
- Auto-init: Usually false (we initialize locally)
- Topics: Optional auto-deployment tagging
- Permissions: Inherited from organization

## Error Handling
- Repository already exists
- Insufficient permissions
- Organization not found
- Rate limit exceeded
- Authentication failures
- Network errors

## Integration Points
- Used by GitHub Repository Agent
- Fine-grained token from AWS Secrets Manager
- Organization name from deployment request
- Repository creation before code push

## Rate Limiting
- Check rate limit status before operations
- Implement exponential backoff on 429 (Too Many Requests)
- Rate limit info: 5000 requests/hour for authenticated users
- Per-repository rate limits for specific operations

## Best Practices
- Verify token permissions before operations
- Check rate limits before bulk operations
- Log all repository creation attempts
- Verify successful creation before proceeding
- Handle rate limit headers in responses

## PyGithub Library
- Abstraction over REST API
- Object-oriented repository access
- Automatic pagination for large result sets
- Built-in retry logic
- Comprehensive exception types

## Notes
- Only operates on specified organization
- Cannot create repositories in personal namespace
- Requires organization owner to enable fine-grained tokens
- Token must be created with organization as resource owner
- All created repositories scoped to organization
