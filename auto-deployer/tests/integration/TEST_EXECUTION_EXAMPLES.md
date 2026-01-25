# Integration Test Execution Examples

## Complete Test Run Example

### Setup

```bash
# 1. Navigate to project
cd auto-deployer

# 2. Create .env file with credentials
cat > .env << 'EOF'
AWS_ACCESS_KEY_ID=***REMOVED-AWS-ACCESS-KEY-ID***
AWS_SECRET_ACCESS_KEY=***REMOVED***
AWS_REGION=us-east-1
S3_BUCKET=my-deployment-bucket

GITHUB_TOKEN=***REMOVED-GITHUB-TOKEN***
GITHUB_ORG=my-organization

CLOUDFLARE_ACCOUNT_ID=1234567890abcdef1234567890abcdef
CLOUDFLARE_TOKEN=v1.0-aBcDeFgHiJkLmNoPqRsTuVwXyZ1234
CLOUDFLARE_EMAIL=your@email.com

GCP_SERVICE_ACCOUNT={"type":"service_account",...}
GCP_PROJECT_ID=my-gcp-project-123456

REDIS_URL=redis://localhost:6379
EOF

# 3. Load environment
source .env

# 4. Start Redis (if using local Redis)
redis-server &
```

---

## Scenario 1: First Run - Validate Credentials

### Command

```bash
pytest tests/integration/test_self_initialization.py -v
```

### Expected Output (All Pass)

```
================================ test session starts ==================================
platform darwin -- Python 3.10.0, pytest-7.0.0
collected 47 items

tests/integration/test_self_initialization.py::TestCredentialsPresence::test_aws_credentials_present PASSED [ 2%]
tests/integration/test_self_initialization.py::TestCredentialsPresence::test_github_credentials_present PASSED [ 4%]
tests/integration/test_self_initialization.py::TestCredentialsPresence::test_cloudflare_credentials_present PASSED [ 6%]
tests/integration/test_self_initialization.py::TestCredentialsPresence::test_gcp_credentials_present PASSED [ 8%]
tests/integration/test_self_initialization.py::TestCredentialsPresence::test_redis_credentials_present PASSED [ 10%]

tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_authentication PASSED [ 12%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_permissions PASSED [ 14%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_bucket_access PASSED [ 16%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_put_object_permission PASSED [ 18%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_get_object_permission PASSED [ 20%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_delete_object_permission PASSED [ 22%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_secrets_manager_permissions PASSED [ 24%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_secrets_manager_create_permission PASSED [ 26%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_secrets_manager_read_permission PASSED [ 28%]

tests/integration/test_self_initialization.py::TestGitHubPermissions::test_github_authentication PASSED [ 30%]
tests/integration/test_self_initialization.py::TestGitHubPermissions::test_github_user_read_permission PASSED [ 32%]
tests/integration/test_self_initialization.py::TestGitHubPermissions::test_github_org_read_permission PASSED [ 34%]
tests/integration/test_self_initialization.py::TestGitHubPermissions::test_github_org_repo_list_permission PASSED [ 36%]
tests/integration/test_self_initialization.py::TestGitHubPermissions::test_github_user_orgs_permission PASSED [ 38%]
tests/integration/test_self_initialization.py::TestGitHubPermissions::test_github_rate_limit_permission PASSED [ 40%]

tests/integration/test_self_initialization.py::TestCloudflarePermissions::test_cloudflare_authentication PASSED [ 42%]
tests/integration/test_self_initialization.py::TestCloudflarePermissions::test_cloudflare_user_read_permission PASSED [ 44%]
tests/integration/test_self_initialization.py::TestCloudflarePermissions::test_cloudflare_account_access_permission PASSED [ 46%]
tests/integration/test_self_initialization.py::TestCloudflarePermissions::test_cloudflare_zones_list_permission PASSED [ 48%]
tests/integration/test_self_initialization.py::TestCloudflarePermissions::test_cloudflare_pages_list_permission PASSED [ 50%]

tests/integration/test_self_initialization.py::TestGCPPermissions::test_gcp_credentials_valid PASSED [ 52%]
tests/integration/test_self_initialization.py::TestGCPPermissions::test_gcp_project_id_matches PASSED [ 54%]
tests/integration/test_self_initialization.py::TestGCPPermissions::test_gcp_authentication PASSED [ 56%]
tests/integration/test_self_initialization.py::TestGCPPermissions::test_gcp_storage_permissions PASSED [ 58%]
tests/integration/test_self_initialization.py::TestGCPPermissions::test_gcp_service_account_email_valid PASSED [ 60%]

tests/integration/test_self_initialization.py::TestRedisPermissions::test_redis_connection_valid PASSED [ 62%]
tests/integration/test_self_initialization.py::TestRedisPermissions::test_redis_string_operations PASSED [ 64%]
tests/integration/test_self_initialization.py::TestRedisPermissions::test_redis_list_operations PASSED [ 66%]
tests/integration/test_self_initialization.py::TestRedisPermissions::test_redis_hash_operations PASSED [ 68%]
tests/integration/test_self_initialization.py::TestRedisPermissions::test_redis_set_operations PASSED [ 70%]
tests/integration/test_self_initialization.py::TestRedisPermissions::test_redis_sorted_set_operations PASSED [ 72%]
tests/integration/test_self_initialization.py::TestRedisPermissions::test_redis_delete_operations PASSED [ 74%]
tests/integration/test_self_initialization.py::TestRedisPermissions::test_redis_ttl_operations PASSED [ 76%]

tests/integration/test_self_initialization.py::TestSelfInitializationSummary::test_all_credentials_configured PASSED [ 78%]
tests/integration/test_self_initialization.py::TestSelfInitializationSummary::test_self_initialization_approval PASSED [ 80%]

================================= 47 passed in 23.45s ==================================
```

### What This Means

✅ **All Credentials Present** - Environment variables configured correctly
✅ **AWS Permissions Valid** - S3 and Secrets Manager access verified
✅ **GitHub Token Valid** - Full org and repo access confirmed
✅ **Cloudflare Token Valid** - Account and Pages access confirmed
✅ **GCP Credentials Valid** - Service account authenticated
✅ **Redis Connection Valid** - All operations working
✅ **APPROVAL GATE PASSED** - System ready for deployment

---

## Scenario 2: Missing AWS Permission

### Command

```bash
pytest tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_delete_object_permission -v
```

### Expected Output (Failure)

```
================================ test session starts ==================================
platform darwin -- Python 3.10.0, pytest-7.0.0
collected 1 item

tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_delete_object_permission FAILED [100%]

====================================== FAILURES =======================================
_________________________ test_aws_s3_delete_object_permission ________________________

    def test_aws_s3_delete_object_permission(self, s3_client):
        """Test that AWS can delete objects from S3."""
        bucket_name = os.getenv("S3_BUCKET")
        test_key = f"permission-test/{id(self)}-delete.txt"

        try:
            # Create test object
            s3_client.put_object(
                Bucket=bucket_name,
                Key=test_key,
                Body=b"Delete permission test",
            )

            # Try to delete it
            s3_client.delete_object(Bucket=bucket_name, Key=test_key)
        except ClientError as e:
            if e.response["Error"]["Code"] == "AccessDenied":
>               pytest.fail(f"Access denied - cannot delete from S3 bucket '{bucket_name}'")
E               Access denied - cannot delete from S3 bucket 'my-deployment-bucket'

tests/integration/test_self_initialization.py:86:87: AssertionError

================================== FAILED in 1.23s ====================================
```

### What To Do

1. **Check AWS IAM Policy** - Add `s3:DeleteObject` permission
   ```json
   {
     "Effect": "Allow",
     "Action": "s3:DeleteObject",
     "Resource": "arn:aws:s3:::my-deployment-bucket/*"
   }
   ```

2. **Update IAM** - Apply changes in AWS Console

3. **Re-run Test**
   ```bash
   pytest tests/integration/test_self_initialization.py::TestAWSPermissions -v
   ```

---

## Scenario 3: Invalid GitHub Token

### Command

```bash
GITHUB_TOKEN=invalid_token_12345 pytest tests/integration/test_self_initialization.py::TestGitHubPermissions -v
```

### Expected Output (Failure)

```
================================ test session starts ==================================
platform darwin -- Python 3.10.0, pytest-7.0.0
collected 6 items

tests/integration/test_self_initialization.py::TestGitHubPermissions::test_github_authentication FAILED [ 16%]

====================================== FAILURES =======================================
_________________ test_github_authentication ____________________

    def test_github_authentication(self, github_client):
        """Test that GitHub token is valid and authenticates successfully."""
        try:
            user = github_client.get_user()
            assert user is not None
            assert hasattr(user, "login")
        except Exception as e:
>           pytest.fail(f"GitHub authentication failed: {e}")
E           GitHub authentication failed: 401 Unauthorized

tests/integration/test_self_initialization.py:165:165: AssertionError

================================== FAILED in 0.89s ====================================
```

### What To Do

1. **Generate New Token** - https://github.com/settings/tokens
2. **Set Correct Permissions** - Select `repo` and `read:org` scopes
3. **Update Environment**
   ```bash
   export GITHUB_TOKEN=ghp_new_token_here
   ```
4. **Re-run Test**
   ```bash
   pytest tests/integration/test_self_initialization.py::TestGitHubPermissions -v
   ```

---

## Scenario 4: Running Specific Service Tests

### AWS Only

```bash
pytest tests/integration/test_aws_integration.py -v
```

```
================================ test session starts ==================================
collected 9 items

tests/integration/test_aws_integration.py::TestAWSS3Integration::test_s3_bucket_list_with_real_credentials PASSED [ 11%]
tests/integration/test_aws_integration.py::TestAWSS3Integration::test_s3_bucket_exists_with_real_credentials PASSED [ 22%]
tests/integration/test_aws_integration.py::TestAWSS3Integration::test_s3_upload_file_with_real_credentials PASSED [ 33%]
tests/integration/test_aws_integration.py::TestAWSS3Integration::test_s3_download_nonexistent_file_fails PASSED [ 44%]
tests/integration/test_aws_integration.py::TestAWSSecretsManagerIntegration::test_secrets_manager_list_with_real_credentials PASSED [ 55%]
tests/integration/test_aws_integration.py::TestAWSSecretsManagerIntegration::test_secrets_manager_create_and_retrieve PASSED [ 66%]
tests/integration/test_aws_integration.py::TestAWSSecretsManagerIntegration::test_secrets_manager_retrieve_nonexistent_secret_fails PASSED [ 77%]
tests/integration/test_aws_integration.py::TestAWSAuthenticationFailures::test_invalid_aws_credentials_fail PASSED [ 88%]
tests/integration/test_aws_integration.py::TestAWSAuthenticationFailures::test_missing_permissions_fail PASSED [ 100%]

================================= 9 passed in 8.12s ==================================
```

### Redis Only

```bash
pytest tests/integration/test_redis_integration.py -v
```

```
================================ test session starts ==================================
collected 16 items

tests/integration/test_redis_integration.py::TestRedisConnection::test_redis_connection_with_real_instance PASSED [ 6%]
tests/integration/test_redis_integration.py::TestRedisConnection::test_redis_server_info_with_real_instance PASSED [ 12%]
tests/integration/test_redis_integration.py::TestRedisStringOperations::test_redis_set_and_get_with_real_instance PASSED [ 18%]
tests/integration/test_redis_integration.py::TestRedisStringOperations::test_redis_set_with_expiration_with_real_instance PASSED [ 25%]
tests/integration/test_redis_integration.py::TestRedisStringOperations::test_redis_increment_with_real_instance PASSED [ 31%]
tests/integration/test_redis_integration.py::TestRedisStringOperations::test_redis_append_with_real_instance PASSED [ 37%]
tests/integration/test_redis_integration.py::TestRedisListOperations::test_redis_list_operations_with_real_instance PASSED [ 43%]
tests/integration/test_redis_integration.py::TestRedisListOperations::test_redis_blocking_pop_with_real_instance PASSED [ 50%]
tests/integration/test_redis_integration.py::TestRedisHashOperations::test_redis_hash_operations_with_real_instance PASSED [ 56%]
tests/integration/test_redis_integration.py::TestRedisSetOperations::test_redis_set_operations_with_real_instance PASSED [ 62%]
tests/integration/test_redis_integration.py::TestRedisSortedSetOperations::test_redis_sorted_set_operations_with_real_instance PASSED [ 68%]
tests/integration/test_redis_integration.py::TestRedisKeyOperations::test_redis_key_exists_with_real_instance PASSED [ 75%]
tests/integration/test_redis_integration.py::TestRedisKeyOperations::test_redis_delete_with_real_instance PASSED [ 81%]
tests/integration/test_redis_integration.py::TestRedisKeyOperations::test_redis_keys_pattern_with_real_instance PASSED [ 87%]
tests/integration/test_redis_integration.py::TestRedisTransactions::test_redis_transaction_with_real_instance PASSED [ 93%]
tests/integration/test_redis_integration.py::TestRedisTransactions::test_redis_watched_transaction_with_real_instance PASSED [ 100%]

================================= 16 passed in 1.89s ==================================
```

---

## Scenario 5: Running by Marker

### All Tests Requiring AWS

```bash
pytest tests/integration/ -m requires_aws -v
```

```
================================ test session starts ==================================
collected 27 items

tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_authentication PASSED [ 3%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_permissions PASSED [ 7%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_bucket_access PASSED [ 11%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_put_object_permission PASSED [ 15%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_get_object_permission PASSED [ 18%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_delete_object_permission PASSED [ 22%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_secrets_manager_permissions PASSED [ 25%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_secrets_manager_create_permission PASSED [ 29%]
tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_secrets_manager_read_permission PASSED [ 33%]
tests/integration/test_aws_integration.py::TestAWSS3Integration::test_s3_bucket_list_with_real_credentials PASSED [ 37%]
tests/integration/test_aws_integration.py::TestAWSS3Integration::test_s3_bucket_exists_with_real_credentials PASSED [ 41%]
tests/integration/test_aws_integration.py::TestAWSS3Integration::test_s3_upload_file_with_real_credentials PASSED [ 44%]
tests/integration/test_aws_integration.py::TestAWSS3Integration::test_s3_download_nonexistent_file_fails PASSED [ 48%]
tests/integration/test_aws_integration.py::TestAWSSecretsManagerIntegration::test_secrets_manager_list_with_real_credentials PASSED [ 51%]
tests/integration/test_aws_integration.py::TestAWSSecretsManagerIntegration::test_secrets_manager_create_and_retrieve PASSED [ 55%]
tests/integration/test_aws_integration.py::TestAWSSecretsManagerIntegration::test_secrets_manager_retrieve_nonexistent_secret_fails PASSED [ 59%]
tests/integration/test_aws_integration.py::TestAWSAuthenticationFailures::test_invalid_aws_credentials_fail PASSED [ 62%]
tests/integration/test_aws_integration.py::TestAWSAuthenticationFailures::test_missing_permissions_fail PASSED [ 66%]
tests/integration/test_deployment_integration.py::TestDeploymentWithAllServices::test_all_services_available PASSED [ 70%]
tests/integration/test_deployment_integration.py::TestDeploymentWithAllServices::test_deployment_workflow_prerequisites PASSED [ 74%]
tests/integration/test_deployment_integration.py::TestDeploymentServiceIntegration::test_aws_service_integration_in_deployment PASSED [ 77%]

================================= 27 passed in 15.34s ==================================
```

---

## Scenario 6: Verbose Output with Failures

### Command

```bash
pytest tests/integration/test_self_initialization.py::TestAWSPermissions -vv --tb=short
```

### Output with Details

```
================================ test session starts ==================================
platform darwin -- Python 3.10.0, pytest-7.0.0
collecting ...

tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_authentication

    def test_aws_authentication(self, s3_client):
        """Test that AWS credentials are valid and authenticate successfully."""
        try:
            # This call verifies authentication
            s3_client.list_buckets()
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "InvalidAccessKeyId":
                pytest.fail("AWS Access Key ID is invalid")
            elif e.response["Error"]["Code"] == "SignatureDoesNotMatch":
                pytest.fail("AWS Secret Access Key is invalid")
            raise

PASSED [ 11%]

tests/integration/test_self_initialization.py::TestAWSPermissions::test_aws_s3_permissions

    s3_client.list_buckets()

/opt/homebrew/lib/python3.10/site-packages/botocore/endpoint.py:275: in _make_request
    return self.make_request(operation_model, request_dict)

PASSED [ 22%]

[... more tests ...]
```

---

## Scenario 7: Test Output to File

### Command

```bash
pytest tests/integration/ -v --tb=short > integration_test_results.txt 2>&1
```

### View Results

```bash
cat integration_test_results.txt | head -100
```

---

## Scenario 8: Stopping on First Failure

### Command

```bash
pytest tests/integration/ -x -v
```

### Output

```
================================ test session starts ==================================
collected 75 items

tests/integration/test_self_initialization.py::TestCredentialsPresence::test_aws_credentials_present PASSED
tests/integration/test_self_initialization.py::TestCredentialsPresence::test_github_credentials_present FAILED

====================================== FAILURES =======================================
_______________________ test_github_credentials_present ______________________

    def test_github_credentials_present(self):
        """Verify GitHub credentials are configured."""
>       assert os.getenv("GITHUB_TOKEN"), "GITHUB_TOKEN not configured"
E       AssertionError: GITHUB_TOKEN not configured

tests/integration/test_self_initialization.py:29:29: AssertionError

================================ 1 failed, 0 skipped in 0.78s =================================

Tests stopped at first failure with -x option.
```

---

## Scenario 9: Missing Redis - Graceful Skip

### Command

```bash
# Stop Redis
redis-cli shutdown

# Run tests
pytest tests/integration/test_redis_integration.py -v
```

### Output

```
================================ test session starts ==================================
collected 16 items

tests/integration/conftest.py::redis_connection: ERROR

!!!!!!!!!!!!!!!!! ERROR at setup of test_redis_connection_with_real_instance !!!!!!!!!

    @pytest.fixture
    def redis_connection(self):
        """
        Fixture providing Redis connection.
        SKIPS test if Redis not available.
        Uses ACTUAL Redis instance - no mocks.
        """
        import redis

        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

        try:
            r = redis.from_url(redis_url)
            r.ping()
            return r
        except Exception as e:
>           pytest.skip(f"Redis not available: {str(e)}")
E           Redis not available: Error 61 connecting to 127.0.0.1:6379. Connection refused.

tests/integration/conftest.py:136: AssertionError

============================================ ERROR in 0.56s ============================================
```

### What This Means

✅ Tests will skip if Redis isn't available
✅ This is expected behavior - tests are designed to be flexible
✅ Simply start Redis and tests will run

---

## Summary Table

| Scenario | Command | Expected Result |
|----------|---------|-----------------|
| **First Run** | `pytest test_self_initialization.py` | All 47 pass = Ready for deployment |
| **AWS Only** | `pytest test_aws_integration.py` | 9 pass = AWS working |
| **GitHub Only** | `pytest test_github_integration.py` | 9 pass = GitHub working |
| **By Marker** | `pytest -m requires_aws` | 27 pass = All AWS tests |
| **Verbose** | `pytest -vv` | Detailed output with stacks |
| **Stop Early** | `pytest -x` | Stop on first failure |
| **Save Results** | `pytest > results.txt` | Output saved to file |
| **Missing Service** | Run without service available | Tests skip gracefully |
| **Invalid Creds** | Wrong password/token | Clear error message |
| **All Tests** | `pytest tests/integration/` | 75+ tests = Complete validation |

---

**Test Execution Complete!**

Once all tests pass, your system is ready to deploy with full cloud service integration.
