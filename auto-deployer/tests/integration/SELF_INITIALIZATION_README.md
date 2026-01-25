# Self-Initialization Test Guide

## Overview

The **Self-Initialization Test Suite** (`test_self_initialization.py`) validates that all provided credentials have the necessary permissions to use the Auto-Deployer system. Run these tests **FIRST** before running any other integration tests.

**Purpose:** If these tests pass, the application has everything it needs from each cloud service.

---

## Quick Start

### 1. Configure Credentials

Create a `.env` file in the project root with all required credentials:

```bash
# AWS
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET=your-bucket-name

# GitHub
GITHUB_TOKEN=ghp_your_github_token
GITHUB_ORG=your-org-name

# Cloudflare
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_TOKEN=your_api_token
CLOUDFLARE_EMAIL=your@email.com

# GCP
GCP_SERVICE_ACCOUNT={"type":"service_account",...}
GCP_PROJECT_ID=your-gcp-project-id
GCP_BILLING_ACCOUNT=billingAccounts/123456-789ABC-DEF012  # Optional

# Redis
REDIS_URL=redis://localhost:6379
```

### 2. Run Self-Initialization Tests

```bash
# Run ALL self-initialization tests
pytest auto-deployer/tests/integration/test_self_initialization.py -v

# Run credential checks only
pytest auto-deployer/tests/integration/test_self_initialization.py::TestCredentialsPresence -v

# Run AWS permissions only
pytest auto-deployer/tests/integration/test_self_initialization.py::TestAWSPermissions -v

# Run GitHub permissions only
pytest auto-deployer/tests/integration/test_self_initialization.py::TestGitHubPermissions -v
```

### 3. Review Results

If all tests pass, you'll see:
```
✅ TestCredentialsPresence - All credentials present
✅ TestAWSPermissions - AWS has all required permissions
✅ TestGitHubPermissions - GitHub token has all required permissions
✅ TestCloudflarePermissions - Cloudflare token has all required permissions
✅ TestGCPPermissions - GCP service account is valid
✅ TestRedisPermissions - Redis connection works
✅ TestSelfInitializationSummary - APPROVAL GATE PASSED
```

---

## What Each Test Suite Validates

### TestCredentialsPresence
Verifies that all required environment variables are configured.

**Environment Variables Checked:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `S3_BUCKET`
- `GITHUB_TOKEN`
- `GITHUB_ORG`
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_TOKEN`
- `CLOUDFLARE_EMAIL`
- `GCP_SERVICE_ACCOUNT`
- `GCP_PROJECT_ID`
- `REDIS_URL` (optional, defaults to `redis://localhost:6379`)

---

### TestAWSPermissions

**Validates:**
1. ✅ **Authentication** - AWS credentials are valid
2. ✅ **S3 List Buckets** - Can list all S3 buckets
3. ✅ **S3 Bucket Access** - Can access the configured bucket
4. ✅ **S3 Upload (PutObject)** - Can upload files to S3
5. ✅ **S3 Download (GetObject)** - Can download files from S3
6. ✅ **S3 Delete (DeleteObject)** - Can delete files from S3
7. ✅ **Secrets Manager List** - Can list secrets
8. ✅ **Secrets Manager Create** - Can create new secrets
9. ✅ **Secrets Manager Read** - Can read existing secrets

**Required IAM Permissions:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListAllMyBuckets",
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::*",
        "arn:aws:s3:::your-bucket-name/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:ListSecrets",
        "secretsmanager:CreateSecret",
        "secretsmanager:GetSecretValue",
        "secretsmanager:DeleteSecret"
      ],
      "Resource": "*"
    }
  ]
}
```

---

### TestGitHubPermissions

**Validates:**
1. ✅ **Authentication** - GitHub token is valid
2. ✅ **User Read** - Can read authenticated user info
3. ✅ **Organization Read** - Can read organization info
4. ✅ **Organization Repos** - Can list organization repositories
5. ✅ **User Organizations** - Can list user's organizations
6. ✅ **Rate Limit Check** - Can check API rate limits

**Required GitHub Scopes:**
```
repo           # Full control of repositories
read:org       # Read-only access to organizations
```

**Token Settings:**
- Token type: Personal Access Token (PAT) or GitHub App
- Expiration: Set appropriate expiration date
- Scopes: `repo`, `read:org`

---

### TestCloudflarePermissions

**Validates:**
1. ✅ **Authentication** - Email and API token are valid
2. ✅ **User Read** - Can read user information
3. ✅ **Account Access** - Can access the configured account
4. ✅ **Zones List** - Can list all zones
5. ✅ **Pages List** - Can list Pages projects

**Required Cloudflare Permissions:**
- User: Read
- Account: Read
- Zone: Read
- Pages: Read

**Token Type:**
- API Token (not API Key)
- Permission template: "Edit Cloudflare Workers" or custom with above permissions

---

### TestGCPPermissions

**Validates:**
1. ✅ **Credentials Valid** - JSON has all required fields
2. ✅ **Project ID Match** - Credential project matches environment variable
3. ✅ **Authentication** - Service account can authenticate
4. ✅ **Cloud Storage Access** - Can list Cloud Storage buckets
5. ✅ **Email Format** - Service account email is valid

**Required GCP Roles:**
```
roles/storage.admin        # Cloud Storage full access
roles/firebaseadmin        # Firebase admin access
roles/iam.serviceAccountAdmin  # Service account admin
```

**Service Account Setup:**
```bash
# Create service account
gcloud iam service-accounts create auto-deployer

# Grant roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member=serviceAccount:auto-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --role=roles/storage.admin

# Create and download key
gcloud iam service-accounts keys create key.json \
  --iam-account=auto-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Set environment variable
export GCP_SERVICE_ACCOUNT="$(cat key.json)"
export GCP_PROJECT_ID=YOUR_PROJECT_ID
```

---

### TestRedisPermissions

**Validates:**
1. ✅ **Connection Valid** - Can connect to Redis
2. ✅ **Ping** - Server is responsive
3. ✅ **String Operations** - SET/GET commands work
4. ✅ **List Operations** - RPUSH/LRANGE commands work
5. ✅ **Hash Operations** - HSET/HGET commands work
6. ✅ **Set Operations** - SADD/SMEMBERS commands work
7. ✅ **Sorted Set Operations** - ZADD/ZRANGE commands work
8. ✅ **Delete Operations** - DEL command works
9. ✅ **TTL Operations** - SETEX/TTL commands work

**Required Redis Configuration:**
- Redis server running and accessible
- No authentication required (or AUTH password in connection string)
- Default connection: `redis://localhost:6379`
- Custom connection: Set `REDIS_URL` environment variable

---

## Test Execution Flow

```
TestCredentialsPresence
├── All environment variables present?
│   └── FAIL: Exit early if missing

TestAWSPermissions
├── AWS credentials valid?
├── S3 list, read, write, delete?
├── Secrets Manager create, read, delete?
│   └── FAIL: Specify which permission is missing

TestGitHubPermissions
├── GitHub token valid?
├── User and org access?
├── Rate limit checking?
│   └── FAIL: Specify which permission is missing

TestCloudflarePermissions
├── Email and token valid?
├── Account and zone access?
├── Pages projects accessible?
│   └── FAIL: Specify which permission is missing

TestGCPPermissions
├── Service account credentials valid?
├── Project ID matches?
├── Authentication works?
├── Cloud Storage access?
│   └── FAIL: Specify which permission is missing

TestRedisPermissions
├── Connection valid?
├── All data structures work?
│   └── FAIL: Specify which operation failed

TestSelfInitializationSummary
└── APPROVAL GATE: All permissions validated ✅
    └── Application ready for deployment!
```

---

## Troubleshooting

### AWS Tests Failing

**Issue:** `InvalidAccessKeyId` or `SignatureDoesNotMatch`
```bash
✗ Check AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
✗ Verify keys haven't been rotated
✗ Ensure IAM user has S3 and Secrets Manager permissions
```

**Issue:** `Access denied to S3 bucket`
```bash
✗ Verify S3_BUCKET name is correct
✗ Check IAM policy includes `s3:ListBucket` on the bucket
✗ Ensure bucket exists in the configured region
```

### GitHub Tests Failing

**Issue:** `BadCredentialsException`
```bash
✗ Verify GITHUB_TOKEN is valid
✗ Check token hasn't been revoked or expired
✗ Ensure token has 'repo' and 'read:org' scopes
```

**Issue:** `GithubException: Organization not found`
```bash
✗ Verify GITHUB_ORG is spelled correctly
✗ Ensure authenticated user is a member of the organization
✗ Check token has organization access permissions
```

### Cloudflare Tests Failing

**Issue:** `Authentication failed - invalid token or email`
```bash
✗ Verify CLOUDFLARE_EMAIL is correct
✗ Verify CLOUDFLARE_TOKEN is valid (API Token, not API Key)
✗ Check token hasn't been revoked
✗ Ensure token has required permissions
```

**Issue:** `Account access denied`
```bash
✗ Verify CLOUDFLARE_ACCOUNT_ID is correct
✗ Check token has account access permissions
✗ Ensure authenticated email belongs to the account
```

### GCP Tests Failing

**Issue:** `GCP_SERVICE_ACCOUNT is not valid JSON`
```bash
✗ Verify GCP_SERVICE_ACCOUNT is valid JSON
✗ For local testing, use: export GCP_SERVICE_ACCOUNT="$(cat key.json)"
✗ For CI/CD, ensure JSON is properly escaped
```

**Issue:** `GCP_PROJECT_ID mismatch`
```bash
✗ Verify GCP_PROJECT_ID matches the service account's project
✗ Service account must be in the same project
```

### Redis Tests Failing

**Issue:** `Redis connection failed`
```bash
✗ Verify Redis server is running: redis-cli ping
✗ Verify REDIS_URL is correct
✗ Check firewall allows connection to Redis port
✗ For local: redis-server should be running on localhost:6379
```

**Issue:** `Connection refused`
```bash
✗ Start Redis: redis-server
✗ Or use Docker: docker run -p 6379:6379 redis:latest
✗ Verify REDIS_URL points to correct host:port
```

---

## Environment Variable Reference

### AWS
| Variable | Required | Format | Example |
|----------|----------|--------|---------|
| `AWS_ACCESS_KEY_ID` | Yes | String | `***REMOVED-AWS-ACCESS-KEY-ID***` |
| `AWS_SECRET_ACCESS_KEY` | Yes | String | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `AWS_REGION` | No | String | `us-east-1` |
| `S3_BUCKET` | Yes | String | `my-deployment-bucket` |

### GitHub
| Variable | Required | Format | Example |
|----------|----------|--------|---------|
| `GITHUB_TOKEN` | Yes | String | `***REMOVED-GITHUB-TOKEN***` |
| `GITHUB_ORG` | Yes | String | `my-organization` |

### Cloudflare
| Variable | Required | Format | Example |
|----------|----------|--------|---------|
| `CLOUDFLARE_ACCOUNT_ID` | Yes | String | `1234567890abcdef1234567890abcdef` |
| `CLOUDFLARE_TOKEN` | Yes | String | `v1.0-aBcDeFgHiJkLmNoPqRsTuVwXyZ1234...` |
| `CLOUDFLARE_EMAIL` | Yes | Email | `your@email.com` |

### GCP
| Variable | Required | Format | Example |
|----------|----------|--------|---------|
| `GCP_SERVICE_ACCOUNT` | Yes | JSON | `{"type":"service_account",...}` |
| `GCP_PROJECT_ID` | Yes | String | `my-gcp-project-123456` |
| `GCP_BILLING_ACCOUNT` | No | String | `billingAccounts/123456-789ABC-DEF012` |

### Redis
| Variable | Required | Format | Example |
|----------|----------|--------|---------|
| `REDIS_URL` | No | URL | `redis://localhost:6379` |

---

## Next Steps

Once all self-initialization tests pass:

1. **Review Results**
   ```bash
   pytest auto-deployer/tests/integration/test_self_initialization.py -v
   ```

2. **Run Other Integration Tests**
   ```bash
   pytest auto-deployer/tests/integration/
   ```

3. **Start Using Auto-Deployer**
   ```bash
   # Configure your deployment
   # Submit deployment requests
   # Monitor progress
   ```

---

## Approval Checklist

Before using Auto-Deployer in production, ensure:

- [ ] All self-initialization tests pass
- [ ] No warnings in test output
- [ ] All AWS permissions verified
- [ ] All GitHub permissions verified
- [ ] All Cloudflare permissions verified
- [ ] All GCP permissions verified
- [ ] Redis connection working
- [ ] Credentials are secure and rotated regularly
- [ ] Backup credentials available in case of rotation
- [ ] API rate limits reviewed and understood
- [ ] Cost monitoring set up for AWS/GCP services

---

## Support

For issues with:
- **AWS:** Check IAM policies and credentials at console.aws.amazon.com
- **GitHub:** Check token scopes at github.com/settings/tokens
- **Cloudflare:** Check token permissions at dash.cloudflare.com
- **GCP:** Check service account roles at console.cloud.google.com
- **Redis:** Check server status with `redis-cli ping`

---

**Last Updated:** January 25, 2026
**Version:** 1.0
