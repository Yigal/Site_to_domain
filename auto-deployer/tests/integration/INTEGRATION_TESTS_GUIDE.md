# Integration Tests Complete Guide

## Overview

The Auto-Deployer integration test suite provides comprehensive validation of cloud service integrations without mocks or placeholders. All tests use **REAL credentials** and **ACTUAL service calls**.

**Test Files:**
- `test_self_initialization.py` - Credential validation (run FIRST)
- `test_aws_integration.py` - AWS S3 and Secrets Manager
- `test_github_integration.py` - GitHub API operations
- `test_cloudflare_integration.py` - Cloudflare Pages and DNS
- `test_gcp_integration.py` - Google Cloud Platform services
- `test_redis_integration.py` - Redis data structures and operations
- `test_deployment_integration.py` - End-to-end deployment workflow
- `conftest.py` - Pytest fixtures and configuration

---

## Test Execution Order

### 1. Self-Initialization (MANDATORY FIRST)

```bash
pytest auto-deployer/tests/integration/test_self_initialization.py -v
```

**What It Does:**
- Validates all credentials are present in environment
- Tests each credential has required permissions
- Acts as approval gate for system readiness

**Success Criteria:**
- All 47 tests pass
- No permission errors reported
- Ready for deployment

**If It Fails:**
- Review error messages to see which permission is missing
- Use SELF_INITIALIZATION_README.md for guidance
- Update credentials with required permissions
- Re-run until all tests pass

---

### 2. AWS Integration

```bash
pytest auto-deployer/tests/integration/test_aws_integration.py -v
```

**What It Tests:**
- S3 bucket operations (list, upload, download, delete)
- Secrets Manager operations (create, read, delete)
- Authentication failure handling
- Permission validation

**Test Classes:**
1. `TestAWSS3Integration` (4 tests)
   - ✅ List buckets with real credentials
   - ✅ Check bucket exists
   - ✅ Upload file to S3
   - ✅ Download nonexistent file fails

2. `TestAWSSecretsManagerIntegration` (3 tests)
   - ✅ List secrets with real credentials
   - ✅ Create and retrieve secret
   - ✅ Retrieve nonexistent secret fails

3. `TestAWSAuthenticationFailures` (2 tests)
   - ✅ Invalid credentials fail
   - ✅ Missing permissions fail

---

### 3. GitHub Integration

```bash
pytest auto-deployer/tests/integration/test_github_integration.py -v
```

**What It Tests:**
- GitHub authentication and user verification
- Organization and repository access
- Rate limit checking
- Authentication failure handling

**Test Classes:**
1. `TestGitHubAuthentication` (5 tests)
   - ✅ Authentication with real token
   - ✅ Organization access with real credentials
   - ✅ List repositories in organization
   - ✅ Invalid token fails
   - ✅ Invalid organization fails

2. `TestGitHubRepositoryOperations` (3 tests)
   - ✅ Repository metadata retrieval
   - ✅ Rate limit status checking
   - ✅ Authenticated user details

3. `TestGitHubRateLimiting` (1 test)
   - ✅ Rate limit status with real credentials

---

### 4. Cloudflare Integration

```bash
pytest auto-deployer/tests/integration/test_cloudflare_integration.py -v
```

**What It Tests:**
- Cloudflare authentication and account access
- Zone and DNS management
- Pages projects and deployments
- Authentication failure handling

**Test Classes:**
1. `TestCloudflareAuthentication` (3 tests)
   - ✅ Authentication with real token
   - ✅ Account access with real credentials
   - ✅ Invalid token fails

2. `TestCloudflareZonesAndDNS` (3 tests)
   - ✅ List zones with real credentials
   - ✅ Get zone details with real API
   - ✅ List DNS records with real API

3. `TestCloudflarePages` (2 tests)
   - ✅ List Pages projects with real credentials
   - ✅ List Pages deployments

4. `TestCloudflareAuthenticationFailures` (2 tests)
   - ✅ Invalid credentials fail
   - ✅ Missing auth headers fail

---

### 5. GCP Integration

```bash
pytest auto-deployer/tests/integration/test_gcp_integration.py -v
```

**What It Tests:**
- GCP service account authentication
- Cloud Storage operations
- Project and identity verification
- Credential validation

**Test Classes:**
1. `TestGCPAuthentication` (2 tests)
   - ✅ Authentication with real service account
   - ✅ Invalid credentials fail

2. `TestGCPStorageOperations` (3 tests)
   - ✅ Storage client creation with real credentials
   - ✅ List buckets with real credentials
   - ✅ Bucket operations (create/delete)

3. `TestGCPProjectOperations` (2 tests)
   - ✅ Project info retrieval
   - ✅ Billing account verification

4. `TestGCPIdentityPlatform` (2 tests)
   - ✅ Identity client creation with real credentials
   - ✅ Service account email extraction

5. `TestGCPAuthenticationFailures` (3 tests)
   - ✅ Malformed service account fails
   - ✅ Invalid private key fails
   - ✅ Empty credentials fail

---

### 6. Redis Integration

```bash
pytest auto-deployer/tests/integration/test_redis_integration.py -v
```

**What It Tests:**
- Redis connection and authentication
- All data structure operations (strings, lists, hashes, sets, sorted sets)
- Key operations and TTL
- Transactions and blocking operations

**Test Classes:**
1. `TestRedisConnection` (2 tests)
   - ✅ Connection with real instance
   - ✅ Server info retrieval

2. `TestRedisStringOperations` (4 tests)
   - ✅ SET/GET operations
   - ✅ SET with expiration (SETEX)
   - ✅ Increment operations (INCR)
   - ✅ String append operations

3. `TestRedisListOperations` (2 tests)
   - ✅ List operations (PUSH/POP)
   - ✅ Blocking pop operations

4. `TestRedisHashOperations` (1 test)
   - ✅ Hash operations (HSET/HGET)

5. `TestRedisSetOperations` (1 test)
   - ✅ Set operations (SADD/SMEMBERS)

6. `TestRedisSortedSetOperations` (1 test)
   - ✅ Sorted set operations (ZADD/ZRANGE)

7. `TestRedisKeyOperations` (3 tests)
   - ✅ Key existence checking (EXISTS)
   - ✅ Key deletion (DELETE)
   - ✅ Pattern matching (KEYS)

8. `TestRedisTransactions` (2 tests)
   - ✅ MULTI/EXEC transactions
   - ✅ WATCH for optimistic locking

---

### 7. Deployment Integration (End-to-End)

```bash
pytest auto-deployer/tests/integration/test_deployment_integration.py -v
```

**What It Tests:**
- API endpoint accessibility
- Deployment request validation
- Status checking
- File uploads
- Complete service integration
- API response handling

**Test Classes:**
1. `TestDeploymentAPIEndpoints` (2 tests)
   - ✅ Health check endpoint
   - ✅ API documentation accessibility

2. `TestDeploymentRequestValidation` (3 tests)
   - ✅ Valid deployment request
   - ✅ Invalid data rejection
   - ✅ Missing required fields rejection

3. `TestDeploymentStatusEndpoint` (1 test)
   - ✅ Status check for nonexistent deployment

4. `TestDeploymentUploadEndpoint` (2 tests)
   - ✅ Upload without file fails
   - ✅ Upload with valid file

5. `TestDeploymentErrorHandling` (2 tests)
   - ✅ Network error handling
   - ✅ Timeout error handling

6. `TestDeploymentServiceIntegration` (3 tests)
   - ✅ AWS service integration
   - ✅ GitHub service integration
   - ✅ Cloudflare service integration

7. `TestDeploymentWithAllServices` (2 tests)
   - ✅ All services available verification
   - ✅ Deployment workflow prerequisites

8. `TestDeploymentAPIConnectivity` (2 tests)
   - ✅ API response time validation
   - ✅ API response headers validation

---

## Running All Tests

### Complete Test Suite

```bash
# Run all integration tests
pytest auto-deployer/tests/integration/ -v

# Run with coverage
pytest auto-deployer/tests/integration/ -v --cov=auto_deployer

# Run and save results
pytest auto-deployer/tests/integration/ -v --tb=short > integration_test_results.txt
```

### By Service

```bash
# AWS only
pytest auto-deployer/tests/integration/ -m requires_aws -v

# GitHub only
pytest auto-deployer/tests/integration/ -m requires_github -v

# Cloudflare only
pytest auto-deployer/tests/integration/ -m requires_cloudflare -v

# GCP only
pytest auto-deployer/tests/integration/ -m requires_gcp -v

# Redis only
pytest auto-deployer/tests/integration/ -m requires_redis -v

# Multiple services
pytest auto-deployer/tests/integration/ -m "requires_aws or requires_github" -v
```

### By Test Class

```bash
# Self-initialization
pytest auto-deployer/tests/integration/test_self_initialization.py::TestAWSPermissions -v

# AWS S3
pytest auto-deployer/tests/integration/test_aws_integration.py::TestAWSS3Integration -v

# GitHub repos
pytest auto-deployer/tests/integration/test_github_integration.py::TestGitHubRepositoryOperations -v
```

---

## Test Coverage Summary

### Total Tests: 75+

| Service | File | Tests | Classes | Coverage |
|---------|------|-------|---------|----------|
| Self-Init | `test_self_initialization.py` | 47 | 7 | Credential validation |
| AWS | `test_aws_integration.py` | 9 | 3 | S3, Secrets Manager |
| GitHub | `test_github_integration.py` | 9 | 3 | Auth, Repos, Rate limits |
| Cloudflare | `test_cloudflare_integration.py` | 12 | 4 | Auth, Zones, Pages |
| GCP | `test_gcp_integration.py` | 10 | 5 | Storage, Projects, Identity |
| Redis | `test_redis_integration.py` | 16 | 8 | All data structures |
| Deployment | `test_deployment_integration.py` | 21 | 8 | API, Integration, E2E |
| **TOTAL** | **7 files** | **75+** | **38** | **Complete** |

---

## Pytest Markers

All tests are tagged with markers indicating what they require:

```bash
@pytest.mark.integration          # All integration tests
@pytest.mark.requires_internet    # Tests requiring internet
@pytest.mark.requires_aws         # Tests requiring AWS credentials
@pytest.mark.requires_github      # Tests requiring GitHub token
@pytest.mark.requires_cloudflare  # Tests requiring Cloudflare token
@pytest.mark.requires_gcp         # Tests requiring GCP service account
@pytest.mark.requires_redis       # Tests requiring Redis connection
```

### Filter by Marker

```bash
# Only tests requiring AWS
pytest auto-deployer/tests/integration/ -m requires_aws

# Exclude tests requiring internet
pytest auto-deployer/tests/integration/ -m "not requires_internet"

# Only self-initialization tests
pytest auto-deployer/tests/integration/ -m "integration and not requires_aws and not requires_github"
```

---

## Handling Test Failures

### Test Skips vs Failures

**Skipped Tests** (green ✓)
- Credentials not configured
- Service not available
- Optional prerequisites missing
- These are OK - tests skip gracefully

**Failed Tests** (red ✗)
- Credentials invalid
- Permission denied
- Service unavailable
- These need investigation

### Debug Failed Tests

```bash
# Verbose output
pytest auto-deployer/tests/integration/test_aws_integration.py -vv

# Show print statements
pytest auto-deployer/tests/integration/test_aws_integration.py -s

# Stop on first failure
pytest auto-deployer/tests/integration/test_aws_integration.py -x

# Show local variables in traceback
pytest auto-deployer/tests/integration/test_aws_integration.py -l

# Run specific test
pytest auto-deployer/tests/integration/test_aws_integration.py::TestAWSS3Integration::test_s3_bucket_list_with_real_credentials -v
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Integration Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest-cov

      - name: Run self-initialization tests
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          S3_BUCKET: ${{ secrets.S3_BUCKET }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_ORG: ${{ secrets.GITHUB_ORG }}
          CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          CLOUDFLARE_TOKEN: ${{ secrets.CLOUDFLARE_TOKEN }}
          CLOUDFLARE_EMAIL: ${{ secrets.CLOUDFLARE_EMAIL }}
          GCP_SERVICE_ACCOUNT: ${{ secrets.GCP_SERVICE_ACCOUNT }}
          GCP_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
          REDIS_URL: redis://localhost:6379
        run: |
          pytest auto-deployer/tests/integration/test_self_initialization.py -v

      - name: Run AWS integration tests
        env:
          # ... (same as above)
        run: |
          pytest auto-deployer/tests/integration/test_aws_integration.py -v

      - name: Run all integration tests
        env:
          # ... (same as above)
        run: |
          pytest auto-deployer/tests/integration/ -v --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## Best Practices

### Before Running Tests

1. **Verify Credentials**
   ```bash
   # Check all environment variables are set
   env | grep -E "AWS_|GITHUB_|CLOUDFLARE_|GCP_|REDIS_"
   ```

2. **Test Connectivity**
   ```bash
   # AWS
   aws s3 ls

   # GitHub
   curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

   # Cloudflare
   curl -H "X-Auth-Email: $CLOUDFLARE_EMAIL" -H "X-Auth-Key: $CLOUDFLARE_TOKEN" \
     https://api.cloudflare.com/client/v4/user

   # Redis
   redis-cli ping
   ```

3. **Start Services**
   ```bash
   # Redis
   redis-server

   # Or Docker
   docker run -p 6379:6379 redis:latest
   ```

### Running Tests

1. **Always run self-initialization first**
   ```bash
   pytest auto-deployer/tests/integration/test_self_initialization.py
   ```

2. **Run by service for isolated testing**
   ```bash
   pytest -m requires_aws auto-deployer/tests/integration/
   ```

3. **Check test output carefully**
   - Look for permission errors
   - Note any skipped tests
   - Review any warnings

### After Tests Pass

1. **Document credentials used**
   ```bash
   # Save which credentials work
   echo "AWS: Production account" > CREDENTIALS_USED.txt
   echo "GitHub: Organization token" >> CREDENTIALS_USED.txt
   ```

2. **Backup credentials**
   - Keep secure backup of tokens
   - Rotate regularly
   - Monitor for unauthorized access

3. **Monitor API quotas**
   ```bash
   # GitHub rate limits
   curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/rate_limit

   # Cloudflare rate limits (check in dashboard)
   ```

---

## Troubleshooting Common Issues

### "ModuleNotFoundError: No module named 'boto3'"

```bash
pip install boto3 PyGithub google-cloud-storage redis httpx
```

### "Connection refused" (Redis)

```bash
# Start Redis
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis:latest

# Verify
redis-cli ping
```

### "Credential errors"

1. Check environment variables are set
2. Verify credentials haven't expired
3. Check IAM/permission policies
4. Run self-initialization tests for details

### "Timeout errors"

- Check internet connection
- Verify firewall allows outbound connections
- Check API service status pages
- Increase timeout if needed

### "Test skipped"

This is normal - means credentials weren't configured. Either:
1. Skip is expected (no integration testing environment)
2. Set credentials and re-run

---

## Performance Considerations

### Test Timing

- Self-initialization: ~10-30 seconds
- AWS tests: ~5-15 seconds
- GitHub tests: ~5-10 seconds
- Cloudflare tests: ~5-10 seconds
- GCP tests: ~5-15 seconds
- Redis tests: ~1-5 seconds
- Deployment tests: ~5-10 seconds
- **Total: ~45-90 seconds for full suite**

### Optimize Test Running

```bash
# Run tests in parallel (requires pytest-xdist)
pip install pytest-xdist
pytest auto-deployer/tests/integration/ -n auto

# Run only modified tests
pytest auto-deployer/tests/integration/ --lf

# Stop on first failure for faster feedback
pytest auto-deployer/tests/integration/ -x
```

---

## Next Steps

1. ✅ Configure all required credentials
2. ✅ Run self-initialization tests
3. ✅ Review any failures or warnings
4. ✅ Run full integration test suite
5. ✅ Verify all services accessible
6. ✅ Deploy with confidence!

---

**Last Updated:** January 25, 2026
**Version:** 1.0
**Total Test Count:** 75+ tests
**Coverage:** All cloud services
