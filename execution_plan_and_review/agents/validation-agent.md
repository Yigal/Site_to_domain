# Validation Agent

## Purpose
Performs pre-deployment validation to ensure all credentials, services, and infrastructure are properly configured before initiating the deployment process.

## Responsibilities
- Validate AWS credentials and resource access
- Test GitHub token and organization access
- Verify Cloudflare account and API token
- Confirm GCP service account and billing setup
- Check Redis connectivity for task queue
- Verify Tree-sitter JavaScript parser installation
- Validate Cloudflare GitHub App installation
- Generate detailed validation reports

## Validation Test Suites

### AWS Connectivity Tests
- AWS credentials presence and validity
- S3 bucket access and permissions
- Secrets Manager secret retrieval
- IAM policy verification

### GitHub Connectivity Tests
- GitHub token validity and authentication
- Organization access verification
- Repository creation permission check
- Fine-grained token scope validation

### Cloudflare Connectivity Tests
- API token validity
- Pages permission verification
- Account access confirmation
- GitHub App installation status (manual check)

### GCP Connectivity Tests
- Service account credentials validity
- Project creation permission
- Billing account access
- Required IAM roles assignment

### Redis Connectivity Tests
- Redis connection and ping test
- Task queue readiness

### Tree-Sitter Tests
- JavaScript parser installation verification
- AST parsing functionality test

### Integration Tests
- Cloudflare GitHub App installation hint

## Key Functions
- `run_all_validations()` - Execute entire validation suite
- `test_aws_credentials_present()` - Verify AWS env vars
- `test_s3_bucket_accessible()` - Test S3 access
- `test_secrets_manager_accessible()` - Test secret retrieval
- `test_github_token_valid()` - Verify GitHub auth
- `test_github_org_accessible()` - Check org access
- `test_cloudflare_token_valid()` - Verify Cloudflare token
- `test_gcp_credentials_valid()` - Check GCP auth
- `test_redis_connection()` - Verify Redis connectivity
- `test_tree_sitter_javascript()` - Verify parser setup

## Execution
- Run command: `pytest tests/test_validation.py -v`
- Timing: Before first deployment or after environment changes
- Output: Detailed pass/fail report for each test

## Test Coverage
- Authentication and authorization
- Resource availability
- API permissions
- Service readiness
- Dependency installation

## Critical Failure Points
1. AWS credentials missing or invalid
2. Secrets Manager not accessible
3. GitHub token invalid or insufficient permissions
4. Cloudflare GitHub App not installed
5. GCP billing role not granted on Billing Account
6. Redis not running or accessible
7. Tree-sitter JavaScript parser not installed

## Warnings and Hints
- Manual verification reminder for GitHub App installation
- Credential rotation recommendations
- Permission scope verification
- Service account role confirmation

## Notes
- Validation tests are non-destructive (no resource creation)
- Can be run repeatedly without side effects
- Provides clear error messages for troubleshooting
- Essential before production deployment
- Should be integrated into CI/CD pipeline
