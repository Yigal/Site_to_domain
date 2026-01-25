# Cloudflare Pages Agent

## Purpose
Creates and manages Cloudflare Pages projects with GitHub integration for automated deployments.

## Responsibilities
- Create Cloudflare Pages projects linked to GitHub repositories
- Retrieve Pages deployment URLs (.pages.dev domain)
- Validate GitHub App installation prerequisites
- Handle Cloudflare API error responses
- Manage custom domain binding
- Create and manage DNS records for custom domains
- Delete Pages projects during rollback
- Resolve zone IDs from domain names

## Key Functions
- `create_pages_project()` - Create Pages project with GitHub source
- `get_deployment_url()` - Retrieve pages.dev URL
- `add_custom_domain()` - Bind custom domain to project
- `create_dns_record()` - Create CNAME records
- `delete_pages_project()` - Remove project (rollback)
- `delete_dns_record()` - Delete DNS records (rollback)
- `get_zone_id()` - Resolve domain to zone ID
- `_get_headers()` - Build auth headers
- `_handle_error()` - Parse Cloudflare error responses

## Authentication
- Cloudflare API Token (from AWS Secrets Manager)
- Token permissions: Account - Pages (Edit), Zone - DNS (Edit), Zone - Zone (Read)

## Prerequisites
- Cloudflare GitHub App must be installed on GitHub organization
- Failure without installation results in error 8000011

## Integration Points
- Receives repository info from GitHub Repository Agent
- Sends Pages URL to GCP Project Agent
- Coordinates with Domain Configuration Agent
- Supports rollback from Saga Orchestration Agent

## Build Configuration
- Build command: `npm run build`
- Destination directory: `dist`
- Production branch: `main`
- Auto-deployments enabled

## Error Handling
- Missing Cloudflare GitHub App (error 8000011)
- Invalid account or zone credentials
- API rate limiting
- Zone resolution failures
- Domain binding conflicts
