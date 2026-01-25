# Domain Configuration Agent

## Purpose
Manages custom domain configuration and DNS record management for deployed applications on Cloudflare.

## Responsibilities
- Validate domain ownership and management (Cloudflare vs. external)
- Create CNAME DNS records pointing to Pages deployment
- Bind custom domains to Cloudflare Pages projects
- Retrieve zone information from domains
- Handle external domain scenarios (return CNAME target to user)
- Manage DNS record deletion during rollback
- Coordinate between Cloudflare and domain registrars

## Key Functions
- `validate_domain_managed()` - Check if domain is in Cloudflare
- `create_dns_record()` - Add CNAME record for custom domain
- `bind_custom_domain()` - Link domain to Pages project
- `delete_dns_records()` - Remove DNS records (rollback)
- `get_zone_id()` - Resolve zone ID from domain name
- `get_dns_propagation_status()` - Monitor DNS propagation

## Integration Points
- Works with Cloudflare Pages Agent for domain binding
- Receives deployment URL from Cloudflare Pages Agent
- Communicates with Saga Orchestration Agent
- Supports rollback operations

## Domain Types Supported
- **Internally Managed**: Cloudflare-hosted domain
  - Agent automates CNAME creation and binding
- **Externally Managed**: Third-party registrar (GoDaddy, etc.)
  - Agent returns CNAME target for manual configuration

## DNS Configuration
- Record type: CNAME
- Target: project-name.pages.dev
- TTL: Standard (varies by Cloudflare account)
- Automatic CNAME flattening for root domains if supported

## Error Handling
- Zone not found or invalid domain
- Domain not managed by Cloudflare
- DNS record conflicts or duplicates
- Permission errors on zone operations
- External registrar coordination issues

## Output for External Domains
- CNAME target: (Pages deployment URL)
- Instruction: User must add CNAME record at their registrar

## Notes
- Domain binding can take time for propagation
- Supports both subdomain and root domain binding
- May require Cloudflare-specific DNS features for root domains
