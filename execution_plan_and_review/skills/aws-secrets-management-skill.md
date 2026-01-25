# AWS Secrets Management Skill

## Description
Manages retrieval, caching, and hydration of sensitive credentials from AWS Secrets Manager and integration with environment variables.

## Capabilities
- Retrieve secrets from AWS Secrets Manager
- Parse JSON-formatted secrets
- Extract specific secret values
- Decode Base64-encoded secrets
- Write credentials to temporary files
- Hydrate environment variables with secrets
- Validate secret availability
- Handle secret rotation
- Implement secure cleanup
- Support secret versioning

## Key Operations
- `get_secret_value(secret_id)` - Retrieve secret JSON
- `get_secret_string(secret_id, key)` - Get specific value
- `get_secret_binary(secret_id)` - Retrieve binary secret
- `decode_base64(encoded_string)` - Decode Base64
- `write_to_temp_file(content, permissions)` - Write with security
- `hydrate_environment(secrets_dict)` - Inject to environment
- `cleanup_temp_files()` - Secure deletion
- `validate_secret_exists()` - Check availability

## Secrets Stored in Secrets Manager
- Secret path: `prod/auto-deployer/keys`
- Contents:
  - `GITHUB_TOKEN` - GitHub Personal Access Token
  - `CLOUDFLARE_API_TOKEN` - Cloudflare API credentials
  - `GCP_SERVICE_ACCOUNT_JSON` - Base64-encoded JSON key

## Hydration Process
1. Fetch encrypted secret from Secrets Manager
2. Parse JSON structure
3. Extract individual credentials
4. Decode Base64-encoded values (GCP JSON)
5. Write GCP JSON to temporary file (/tmp/gcp_creds.json)
6. Set environment variables for application
7. Set GOOGLE_APPLICATION_CREDENTIALS path

## Temporary File Management
- Location: /tmp/ directory
- Permissions: 0600 (read/write owner only)
- Ownership: Application user
- Cleanup: On application shutdown or error
- Secure deletion: Overwrite before deletion

## AWS SDK Configuration
- Service: secretsmanager
- Region: Configurable (default: us-east-1)
- Credentials: IAM User (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
- Authentication: Automatic from environment

## Error Handling
- SecretNotFound - Secret doesn't exist
- InvalidParameterException - Invalid secret ID
- AccessDenied - IAM policy missing
- ResourceNotFoundException - Secret deleted
- InvalidRequestException - Invalid request format
- NetworkError - Connectivity issues
- DecodeException - Base64 decode failures

## Security Measures
- No credential logging or printing
- Temporary files use restrictive permissions
- Automatic cleanup on process exit
- No caching in application memory
- Secrets fetched at runtime, not deployment
- Automatic expiration handling

## Integration Points
- Called during application startup
- Available to all agents at runtime
- No credential passing between modules
- Environment variables accessible to all services
- GCP credentials file path: GOOGLE_APPLICATION_CREDENTIALS

## Caching Strategy
- No credential caching by default
- Optional: Short-lived cache (< 5 minutes)
- Refresh on credential rotation
- Validate freshness before use

## Base64 Encoding
- GCP JSON key is Base64-encoded for storage
- Encoding: Standard Base64 (RFC 4648)
- Decoding: Python base64.b64decode()
- Original format: UTF-8 JSON

## Credential Rotation
- Secrets Manager versioning support
- Latest version fetched automatically
- Application restart required for rotation
- No in-flight credential swaps

## IAM Policy Required
- Resource: `arn:aws:secretsmanager:*:*:secret:prod/auto-deployer/*`
- Action: `secretsmanager:GetSecretValue`
- Effect: Allow

## Notes
- Called once at application startup in lifespan
- Credentials available to all workers and API handlers
- Environment variables persist for application lifetime
- GCP JSON file created before Firebase operations
- Cleanup prevents credential leaks in /tmp
