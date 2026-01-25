# AWS Storage Agent

## Purpose
Manages secure storage and retrieval of deployment artifacts, secrets, and uploaded source code using AWS S3 and Secrets Manager.

## Responsibilities
- Upload and download files from S3 buckets
- Download and extract ZIP archives from S3
- List S3 objects with prefix filtering
- Retrieve third-party credentials from Secrets Manager
- Hydrate environment variables with secrets at runtime
- Decode Base64-encoded GCP credentials
- Write credentials to temporary files with secure permissions
- Handle S3 and Secrets Manager errors gracefully

## Key Functions
- `download_file()` - Retrieve file from S3
- `upload_file()` - Store file to S3 with multipart support
- `download_and_extract_zip()` - Download and extract archives
- `list_objects()` - List S3 objects with prefix
- `hydrate_secrets()` - Fetch and inject all credentials
- `_get_s3_client()` - Initialize S3 client
- `_fetch_secret()` - Retrieve single secret from Secrets Manager
- `_decode_gcp_credentials()` - Base64 decode GCP JSON

## Authentication
- AWS IAM credentials (Access Key ID and Secret Access Key)
- IAM Policy permissions:
  - `s3:GetObject` (react-to-app/*)
  - `s3:ListBucket` (react-to-app)
  - `s3:PutObject` (react-to-app/*)
  - `secretsmanager:GetSecretValue` (prod/auto-deployer/*)

## Stored Secrets
- GITHUB_TOKEN - GitHub Personal Access Token
- CLOUDFLARE_API_TOKEN - Cloudflare API credentials
- GCP_SERVICE_ACCOUNT_JSON - Base64-encoded GCP JSON key

## Integration Points
- Retrieves source code zips for Source Acquisition Agent
- Provides credentials to all cloud service agents
- Stores deployment configurations and manifests
- Manages temporary artifact storage

## S3 Bucket
- Name: react-to-app
- Contains: source zips, deployment configs, temporary files

## Secrets Manager
- Secret path: prod/auto-deployer/keys
- Contains: GitHub token, Cloudflare token, GCP service account

## Error Handling
- S3 access denied or bucket not found
- Secret not found in Secrets Manager
- Network connectivity issues
- File encoding/decoding errors
- Multipart upload failures

## Security Measures
- No credential caching - fetched at runtime
- Credentials written to temp files with restrictive permissions (0600)
- Automatic cleanup of sensitive files
- Base64 encoding for binary credentials in Secrets Manager
