# DNS Record Management Skill

## Description
Manages DNS record creation, modification, deletion, and monitoring across Cloudflare for custom domain configuration.

## Capabilities
- Create DNS records (CNAME, A, AAAA, MX, TXT, NS, SRV)
- Update existing DNS records
- Delete DNS records
- List DNS records by type or name
- Query DNS record details
- Manage DNS zones
- Handle zone resolution from domain names
- Support DNS-only vs full setup
- Implement DNS propagation checking
- Manage TTL (Time To Live) settings

## Key Operations
- `create_dns_record(zone_id, type, name, content)` - Add record
- `update_dns_record(zone_id, record_id, content)` - Modify record
- `delete_dns_record(zone_id, record_id)` - Remove record
- `list_dns_records(zone_id, type)` - List by type
- `get_dns_record(zone_id, record_id)` - Get details
- `get_zone_id_from_domain(domain)` - Resolve zone
- `check_dns_propagation(domain)` - Monitor propagation

## Supported Record Types
- **CNAME**: Alias to Pages deployment (.pages.dev)
- **A**: IPv4 address (usually proxied)
- **AAAA**: IPv6 address
- **MX**: Mail exchange records
- **TXT**: Text records (verification, SPF, DKIM)
- **NS**: Nameserver records
- **SRV**: Service records

## CNAME Configuration
- Name: Subdomain (e.g., app)
- Content: Pages deployment URL (e.g., project.pages.dev)
- Proxied: true (orange cloud) for Cloudflare benefits
- TTL: Auto (Cloudflare default)

## Root Domain CNAME
- Cloudflare allows CNAME at root via CNAME flattening
- Alternative: A record to Cloudflare IP
- DNS CNAME at root not standard DNS
- Cloudflare manages internally

## TTL (Time To Live)
- Default: 1 hour (3600 seconds)
- Custom: 120 to 86400 seconds
- Lower TTL: Faster propagation (costs more queries)
- Higher TTL: Slower changes (better caching)
- Auto: Cloudflare managed (optimal)

## Zone Resolution
```
Input: app.example.com
1. Check if example.com zone exists
2. Return zone ID
3. Create CNAME record for app subdomain
```

## DNS Propagation
- Propagation time: 5 minutes to 48 hours
- Cloudflare: Minutes (internal)
- Nameserver updates: Up to 48 hours
- Monitor via DNS checkers
- Verify A record resolves

## API Integration
- Cloudflare API v4
- Authentication: API token
- Endpoint: /zones/{zone_id}/dns_records
- Rate limit: Standard Cloudflare limits

## Error Handling
- Zone not found
- Record already exists
- Invalid record content
- Proxying not supported for record type
- Permission denied on zone
- Invalid TTL value
- Too many records per zone

## Record Validation
- Name format: Valid subdomain
- Content format: Type-specific (IP, FQDN, etc.)
- TTL range: 120-86400 seconds
- Proxy support: Not all types support proxying

## Cloudflare Features
- **Proxying (Orange Cloud)**: Routes through Cloudflare
  - Adds DDoS protection
  - Enables WAF rules
  - Provides analytics
  - DNS-only (Gray Cloud): Direct records, no proxying

## Integration Points
- Used by Domain Configuration Agent
- Called after Pages project creation
- Coordinates with custom domain binding
- Uses zone ID from domain lookup
- Supports rollback via deletion

## Propagation Monitoring
- DNS propagation checkers
- Cloudflare provides instant results
- External nameservers may take time
- Test via nslookup or dig
- Monitor via external DNS tools

## Security Considerations
- API token scoped to zone operations only
- Restrict to specific zones where possible
- Monitor DNS changes via audit logs
- Implement DDoS protection via Cloudflare
- Use DNSSEC for additional security

## Cleanup (Rollback)
- Delete DNS records on failed deployment
- Restore previous records if available
- Verify deletion completed
- Check propagation afterward

## Performance
- Instant creation in Cloudflare system
- Propagation delay: 5 minutes typical
- Queries cached by nameservers
- TTL affects cache duration

## Testing
1. Create DNS record
2. Wait for propagation
3. Verify with `nslookup` or `dig`
4. Test HTTPS if applicable
5. Cleanup test records

## Notes
- Record updates may cause brief propagation
- Email records (MX) critical for mail delivery
- TXT records used for domain verification
- CNAME preferred for simplicity
- A records for root domain
- Multiple records can coexist per name
