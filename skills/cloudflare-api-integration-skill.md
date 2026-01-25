# Cloudflare API Integration Skill

## Description
Manages interactions with Cloudflare API v4 for Pages project creation, DNS management, and custom domain configuration.

## Capabilities
- Authenticate with Cloudflare API tokens
- Create Cloudflare Pages projects
- Link Pages projects to GitHub repositories
- Retrieve Pages deployment URLs
- Create DNS records (CNAME, A, MX, TXT)
- Retrieve zone information from domain names
- Update DNS records
- Delete DNS records
- List existing projects and DNS records
- Add custom domains to Pages projects
- Handle API error responses and codes
- Manage account and zone resources

## Key Operations
- `list_zones()` - List all zones in account
- `get_zone_by_domain(domain)` - Resolve zone ID
- `create_pages_project(config)` - Create project with GitHub source
- `get_pages_project(account_id, project_name)` - Retrieve project
- `delete_pages_project(account_id, project_name)` - Delete project
- `get_deployment_url(account_id, project_name)` - Get pages.dev URL
- `create_dns_record(zone_id, type, name, target)` - Add DNS record
- `delete_dns_record(zone_id, record_id)` - Remove DNS record
- `add_custom_domain(project_name, domain)` - Bind domain

## API Endpoints
- Base URL: https://api.cloudflare.com/client/v4
- Authentication: Bearer token in Authorization header
- Response format: JSON with success flag and result/errors

## Pages Project Configuration
- Source type: GitHub
- Build command: npm run build
- Destination directory: dist
- Production branch: main
- Automatic deployments: enabled

## DNS Record Types Supported
- CNAME - Alias to Pages deployment
- A - Direct IP address
- AAAA - IPv6 address
- MX - Mail exchange
- TXT - Text records
- NS - Nameserver
- SRV - Service records

## Error Codes and Handling
- 8000011 - GitHub integration not installed (critical)
- 1000 - Invalid request
- 1001 - Invalid parameter
- 1003 - Invalid organization (authentication)
- 1004 - Invalid account or permissions
- 9000 - Rate limit exceeded
- 1009 - Zone not found

## Prerequisites
- Cloudflare GitHub App must be installed on GitHub organization
- Account ID must be known
- Zone must be managed by Cloudflare account
- API token must have proper scopes

## Token Scopes Required
- Account - Cloudflare Pages: Edit
- Zone - DNS: Edit
- Zone - Zone: Read

## Error Response Handling
- Parse error array from response
- Extract error codes and messages
- Implement retry logic for rate limits
- Log detailed error information
- Translate API errors to user-friendly messages

## Integration Points
- Used by Cloudflare Pages Agent
- Used by Domain Configuration Agent
- API token from AWS Secrets Manager
- Account ID from deployment configuration
- Zone ID resolution from custom domain

## Rate Limiting
- Standard: 1,200 requests/5 minutes
- Different limits per endpoint
- Exponential backoff on rate limit
- Monitor X-RateLimit headers

## Notes
- GitHub App installation not automated (manual prerequisite)
- DNS propagation can take 5-60 minutes
- CNAME records for subdomains preferred
- Root domain CNAME requires Cloudflare DNS
- Custom domain binding can happen concurrently with project creation
