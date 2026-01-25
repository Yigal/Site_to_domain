# Credentials Requirements Report

## Overview

This report details all credentials required for the credential resource testing framework to validate access to cloud resources. It specifies what information is needed, what's currently available, what's missing, and exactly where to obtain each missing piece.

**Current Status:** 3 out of 14 tests passing (AWS only)

---

## Credentials Status Summary

| Service | Status | Tests | Pass | Skip | Missing Items |
|---------|--------|-------|------|------|---|
| AWS | ✅ Complete | 3 | 3 | 0 | None |
| GitHub | 🔴 Incomplete | 3 | 0 | 3 | Organization name |
| Cloudflare | 🔴 Incomplete | 3 | 0 | 3 | Account ID, Email |
| GCP | 🔴 Corrupted | 3 | 0 | 3 | Fix service account JSON |
| Redis | 🔴 Missing | 2 | 0 | 2 | Redis URL |
| **TOTAL** | | **14** | **3** | **11** | |

---

## AWS Credentials ✅ (Complete)

### Current Status
✅ **Fully configured and working**

### What We Have
- `AWS_ACCESS_KEY_ID`: ***REMOVED-AWS-ACCESS-KEY-ID***
- `AWS_SECRET_ACCESS_KEY`: XTCj6vL/pHuleaW5lWaG9ot20inFJfd7pVuUuQnh
- `AWS_REGION`: us-east-1

### Test Results
- ✅ S3 bucket access: PASSED
- ✅ Secrets Manager access: PASSED
- ✅ AWS authentication: PASSED

### What's Missing
Nothing - AWS credentials are complete and validated.

---

## GitHub Credentials 🔴 (Incomplete)

### Current Status
⏭️ **1 out of 2 required items present**

### What We Have
✅ `GITHUB_TOKEN`: ***REMOVED-GITHUB-TOKEN***

### What's Missing
❌ `GITHUB_ORG`: (required) - Organization name for testing repository access

### Tests Affected
All 3 GitHub tests are skipped:
1. TestGitHubAuthenticationResource::test_github_authentication
2. TestGitHubOrganizationResource::test_github_organization_access
3. TestGitHubRepositoryResource::test_github_repository_listing

---

## How to Get GitHub Organization Name

### Step 1: Identify Your Organization
The GitHub organization is the account name you use for team/group repositories.

**Examples:**
- `https://github.com/my-organization` → Organization is `my-organization`
- `https://github.com/company` → Organization is `company`

### Step 2: Find Organization Name

**Method A: Through GitHub Web UI**
1. Go to https://github.com
2. Sign in with the account that owns the GitHub token
3. Click on your profile picture (top right)
4. Click "Your organizations"
5. Look at the list of organizations you belong to
6. Select the organization you want to use for testing
7. The organization name appears in the URL: `https://github.com/{ORG_NAME}`

**Method B: Through GitHub CLI**
```bash
gh auth login  # If not already authenticated
gh org list --limit 100
```

**Method C: Using GitHub API**
```bash
curl -H "Authorization: token ***REMOVED-GITHUB-TOKEN***" \
  https://api.github.com/user/orgs
```

This returns JSON showing all organizations the token owner belongs to:
```json
[
  {
    "login": "my-organization",
    "id": 12345678,
    ...
  }
]
```

### Step 3: Add to .env File

Once you have the organization name, add it to `.env`:

```bash
GITHUB_ORG=my-organization
```

Replace `my-organization` with your actual organization name.

### Step 4: Validate Configuration

Run GitHub tests to confirm:
```bash
python -m pytest auto-deployer/tests/credentials/ -m github -v
```

Expected output: 3 tests passing

---

## Cloudflare Credentials 🔴 (Incomplete)

### Current Status
⏭️ **1 out of 3 required items present**

### What We Have
✅ `CLOUDFLARE_TOKEN`: JNHIc0aucIaUMZ20ymehF5yjGD_kueIkJpSIZvGd

### What's Missing
❌ `CLOUDFLARE_ACCOUNT_ID`: (required) - Your Cloudflare account identifier
❌ `CLOUDFLARE_EMAIL`: (required) - Email associated with Cloudflare account

### Tests Affected
All 3 Cloudflare tests are skipped:
1. TestCloudflareAuthenticationResource::test_cloudflare_authentication
2. TestCloudflareAccountResource::test_cloudflare_account_access
3. TestCloudflarePagesResource::test_cloudflare_pages_access

---

## How to Get Cloudflare Account ID and Email

### Step 1: Get Cloudflare Account ID

**Method A: Through Cloudflare Dashboard (Easiest)**
1. Go to https://dash.cloudflare.com
2. Sign in with your Cloudflare account
3. Look at the URL: `https://dash.cloudflare.com/...`
   - Or click on your domain
   - The account ID is shown on the Overview page
4. On any page in the dashboard, look for "Account ID" in the sidebar
5. Click on your account name (top right) → Account Home
6. Copy the **Account ID** displayed under your account name

**Alternative:** In the browser's developer console:
```javascript
// Paste this into DevTools Console while on Cloudflare dashboard
console.log(document.querySelector('[data-account-id]')?.getAttribute('data-account-id'))
```

**Method B: Using Cloudflare API**
```bash
curl -X GET "https://api.cloudflare.com/client/v4/accounts" \
  -H "X-Auth-Email: your-email@example.com" \
  -H "X-Auth-Key: JNHIc0aucIaUMZ20ymehF5yjGD_kueIkJpSIZvGd"
```

This returns JSON with account information:
```json
{
  "success": true,
  "result": [
    {
      "id": "abc123def456xyz789",
      "name": "My Account",
      "type": "standard",
      ...
    }
  ]
}
```

### Step 2: Get Cloudflare Email

The email is the one associated with your Cloudflare account - the email you use to log in.

**How to confirm:**
1. Go to https://dash.cloudflare.com
2. Click on your account name (top right corner)
3. Click "My Profile"
4. Your email address is displayed as "Login email"

### Step 3: Verify Token Permissions

The Cloudflare token needs specific permissions:
- **Required:** Account → Cloudflare Pages → Read
- **Required:** Account → Account Settings → Read

To check token permissions:
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Find the token used in `.env` (or create a new one)
3. Click on the token name
4. Verify it has necessary permissions

**If creating a new token:**
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Select "Custom token" template
4. Add these permissions:
   - Account → Cloudflare Pages → Read
   - Account → Account Settings → Read
5. Copy the token and add to `.env`

### Step 4: Add to .env File

Once you have both values:

```bash
CLOUDFLARE_ACCOUNT_ID=abc123def456xyz789
CLOUDFLARE_EMAIL=your-email@example.com
CLOUDFLARE_TOKEN=JNHIc0aucIaUMZ20ymehF5yjGD_kueIkJpSIZvGd
```

Replace the values with your actual Cloudflare information.

### Step 5: Validate Configuration

Run Cloudflare tests:
```bash
python -m pytest auto-deployer/tests/credentials/ -m cloudflare -v
```

Expected output: 3 tests passing

---

## GCP Credentials 🔴 (Corrupted)

### Current Status
⚠️ **Present but corrupted - cannot be parsed**

### What We Have
- `GCP_SERVICE_ACCOUNT`: Base64-encoded service account JSON (but corrupted)
- `GCP_PROJECT_ID`: hyperdev-app

### What's Wrong
The GCP service account JSON contains an invalid Unicode escape sequence:
- **Invalid:** `\u000` (only 3 hex digits, should be 4)
- **Location:** In the private key field of the service account

**Error Message:**
```
Invalid \uXXXX escape: line 5 column 1538 (char 1664)
```

### Tests Affected
All 3 GCP tests are skipped:
1. TestGCPAuthenticationResource::test_gcp_authentication
2. TestGCPCloudStorageResource::test_gcp_storage_access
3. TestGCPProjectResource::test_gcp_project_access

---

## How to Fix GCP Credentials

### Option 1: Download Fresh Credentials from Google Cloud (Recommended)

**Step 1: Access Google Cloud Console**
1. Go to https://console.cloud.google.com
2. Select project "hyperdev-app" from the dropdown (top left)

**Step 2: Create Service Account (if one doesn't exist)**
1. In the left sidebar, go to IAM & Admin → Service Accounts
2. Click "Create Service Account"
3. Fill in details:
   - Service account name: `auto-deployer-sa`
   - Service account ID: `auto-deployer-sa`
4. Click "Create and Continue"
5. Grant roles (select as needed):
   - Storage Admin (for Cloud Storage)
   - Billing Account Viewer (for Billing API)
   - Service Usage Admin (for enabling APIs)
6. Click "Continue" → "Done"

**Step 3: Create and Download Key**
1. In the Service Accounts list, click on `auto-deployer-sa`
2. Go to the "Keys" tab
3. Click "Add Key" → "Create new key"
4. Select "JSON" format
5. Click "Create"
6. The JSON file downloads automatically
7. Save this file temporarily

**Step 4: Encode Service Account JSON to Base64**

The JSON file is in plain text. The `.env` file requires it to be base64-encoded.

**On macOS/Linux:**
```bash
# Replace path/to/downloaded/serviceaccount.json with actual file path
cat /path/to/downloaded/serviceaccount.json | base64 | tr -d '\n'
```

This outputs a single line of base64-encoded text. Copy this entire output.

**On Windows (PowerShell):**
```powershell
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content 'C:\path\to\serviceaccount.json' -Raw))) | Write-Host -NoNewline
```

**Step 5: Verify the Encoded JSON**

Before updating `.env`, verify the encoding is correct:
```bash
# Decode to verify it's valid JSON
echo "your-base64-string-here" | base64 -d | python -m json.tool
```

If it outputs formatted JSON without errors, the encoding is correct.

**Step 6: Update .env File**

Replace the corrupted `GCP_SERVICE_ACCOUNT` value with the fresh base64-encoded version:

```bash
GCP_SERVICE_ACCOUNT=your-new-base64-encoded-value-here
GCP_PROJECT_ID=hyperdev-app
```

**Step 7: Validate Configuration**

Run GCP tests:
```bash
python -m pytest auto-deployer/tests/credentials/ -m gcp -v
```

Expected output: 3 tests passing

---

### Option 2: Manual Repair of Corrupted String (Advanced)

If you want to repair the existing corrupted credentials:

**Step 1: Decode the corrupted string**
```bash
echo "ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAg..." | base64 -d > gcp_corrupted.json
```

**Step 2: Find and fix the invalid escape**
```bash
# Find the problematic character
grep -n "\\u000" gcp_corrupted.json
```

**Step 3: Edit the file**
Find the line with `\u000` and change it to `\u0000`

**Step 4: Re-encode to base64**
```bash
cat gcp_corrupted.json | base64 | tr -d '\n'
```

**Step 5: Update .env with the corrected version**

---

### Recommended: Option 1 (Fresh Credentials)

We recommend **Option 1** because:
- Ensures credentials are current and valid
- Eliminates uncertainty about the original corruption source
- Better security practice to regenerate service account keys periodically
- Guarantees all permissions are properly configured

---

## Redis Credentials 🔴 (Missing)

### Current Status
❌ **Not provided - no Redis configuration**

### What We Have
Nothing - no Redis configuration in `.env`

### What's Missing
❌ `REDIS_URL`: (required) - Complete Redis connection URL

### Tests Affected
Both Redis tests are skipped:
1. TestRedisConnectionResource::test_redis_connection
2. TestRedisOperationsResource::test_redis_operations

---

## How to Get Redis URL

### Determine Your Redis Setup

First, determine where your Redis instance is running:

**Option A: Redis is Already Running Locally**
```bash
# Test connection
redis-cli ping
# Response should be: PONG
```

**Option B: Redis is Running on a Remote Server**
You should have:
- Redis host/IP address
- Redis port (default: 6379)
- Redis password (if authentication enabled)

**Option C: Using Managed Redis Service**
Common providers:
- **AWS ElastiCache**
- **Redis Cloud** (formerly Redislabs)
- **Azure Cache for Redis**
- **Google Cloud Memorystore**
- **Heroku Redis**

---

## How to Construct Redis URL

### Format
```
redis://:password@host:port/db
```

### Examples

**Local Redis (no password):**
```
redis://localhost:6379
```

**Local Redis with password:**
```
redis://:mypassword@localhost:6379
```

**Remote Redis (no password):**
```
redis://redis.example.com:6379
```

**Remote Redis with password:**
```
redis://:mypassword@redis.example.com:6379
```

**Remote Redis with username and password (Redis 6.0+):**
```
redis://username:password@redis.example.com:6379
```

**Redis Cloud / Managed Service:**
```
redis://:your-api-key@redis-instance.redis.cloud:port
```

---

## How to Get Redis Credentials by Service

### AWS ElastiCache

**Step 1: Access AWS Console**
1. Go to https://console.aws.amazon.com/elasticache
2. Select "Redis" from left sidebar
3. Click on your Redis cluster name

**Step 2: Get Connection Details**
1. On the cluster page, find "Cluster endpoint"
2. Format: `primary-endpoint-address:port`
3. Example: `myredis.abc123.ng.0001.use1.cache.amazonaws.com:6379`

**Step 3: Get Authentication Token (if enabled)**
1. Click on cluster name
2. Go to "User" tab
3. Find the default user
4. Check if "Authentication token" is enabled
5. Copy the token

**Step 4: Construct URL**
```
redis://:your-auth-token@myredis.abc123.ng.0001.use1.cache.amazonaws.com:6379
```

---

### Redis Cloud (Redislabs)

**Step 1: Access Redis Cloud Console**
1. Go to https://app.redis.com
2. Sign in with your Redis Cloud account

**Step 2: Select Database**
1. Click on the database you want to use
2. In the "Overview" tab, find "Database Details"

**Step 3: Get Connection Details**
1. Find the "Public endpoint" or "Private endpoint"
2. Format: `redis-instance.redis.cloud:port`
3. Find the default user's password in "Security" section

**Step 4: Construct URL**
```
redis://:your-password@redis-instance.redis.cloud:port
```

Example:
```
redis://:mypassword@redis-12345.redis.cloud:19273
```

---

### Azure Cache for Redis

**Step 1: Access Azure Portal**
1. Go to https://portal.azure.com
2. Search for "Azure Cache for Redis"
3. Click on your Redis instance

**Step 2: Get Connection Details**
1. Go to "Access keys" in left sidebar
2. Copy the "Primary connection string"
3. It will be in format: `hostname:6380?ssl=True,password=...`

**Step 3: Convert to Standard URL Format**
The format above is Azure-specific. Convert it:
- Extract hostname
- Extract password
- Port is usually 6380 (SSL) or 6379 (non-SSL)

**Step 4: Construct URL**
```
redis://:your-password@your-instance.redis.cache.windows.net:6380
```

---

### Google Cloud Memorystore

**Step 1: Access Google Cloud Console**
1. Go to https://console.cloud.google.com
2. Go to Memorystore → Redis
3. Click on your Redis instance

**Step 2: Get Connection Details**
1. Find the "Primary endpoint" in the details
2. Format: `ip:port`
3. Example: `10.0.0.3:6379`

**Step 3: Note Authentication (if enabled)**
1. Check if authentication token is enabled
2. Copy the AUTH string from the "AUTH string" field

**Step 4: Construct URL**
```
redis://:your-auth-token@10.0.0.3:6379
```

---

### Local Development (Docker)

If running Redis locally via Docker:

**Step 1: Verify Redis Container is Running**
```bash
docker ps | grep redis
```

**Step 2: Get Container IP (if needed)**
```bash
docker inspect container-name | grep IPAddress
```

**Step 3: Construct URL**
```
redis://localhost:6379
```

Or if Docker container is on a custom network:
```
redis://redis:6379
```

---

## How to Test Redis Connection

Before adding to `.env`, test the URL:

**Using redis-cli:**
```bash
redis-cli -u "redis://:password@host:port" ping
```

Should return: `PONG`

**Using Python:**
```python
import redis

# Test the connection
r = redis.from_url("redis://:password@host:port")
print(r.ping())  # Should print: True
```

---

## Step 4: Add to .env File

Once you have the Redis URL:

```bash
REDIS_URL=redis://:password@host:port
```

Replace with your actual Redis URL.

**Example:**
```bash
REDIS_URL=redis://:mypassword@localhost:6379
```

### Step 5: Validate Configuration

Run Redis tests:
```bash
python -m pytest auto-deployer/tests/credentials/ -m redis -v
```

Expected output: 2 tests passing

---

## Summary of Missing Information

### Required Before Testing Can Be Complete

| Service | Missing | How to Get | Difficulty |
|---------|---------|-----------|------------|
| GitHub | `GITHUB_ORG` | Check GitHub account organizations | Easy |
| Cloudflare | `CLOUDFLARE_ACCOUNT_ID` | Cloudflare dashboard → Account ID | Easy |
| Cloudflare | `CLOUDFLARE_EMAIL` | Cloudflare login email | Easy |
| GCP | Fix corrupted service account | Download from Google Cloud Console | Medium |
| Redis | `REDIS_URL` | Connect to Redis instance | Medium |

### Estimated Time to Complete

- **GitHub:** 2-3 minutes
- **Cloudflare:** 5-10 minutes
- **GCP:** 10-15 minutes
- **Redis:** 5-15 minutes (varies by service)

**Total: 20-45 minutes**

---

## .env Configuration Template

Here's the complete template with placeholders:

```bash
# ============================================================
# AWS Credentials (✅ Already configured and working)
# ============================================================
AWS_ACCESS_KEY_ID=***REMOVED-AWS-ACCESS-KEY-ID***
AWS_SECRET_ACCESS_KEY=***REMOVED***
AWS_REGION=us-east-1

# ============================================================
# GitHub Credentials (🔴 Requires: GITHUB_ORG)
# ============================================================
GITHUB_TOKEN=***REMOVED-GITHUB-TOKEN***
GITHUB_ORG=your-organization-name

# ============================================================
# Cloudflare Credentials (🔴 Requires: ACCOUNT_ID, EMAIL)
# ============================================================
CLOUDFLARE_TOKEN=JNHIc0aucIaUMZ20ymehF5yjGD_kueIkJpSIZvGd
CLOUDFLARE_ACCOUNT_ID=your-account-id-here
CLOUDFLARE_EMAIL=your-email@example.com

# ============================================================
# GCP Credentials (🔴 Requires: Fix corrupted service account)
# ============================================================
GCP_SERVICE_ACCOUNT=your-fresh-base64-encoded-service-account-json
GCP_PROJECT_ID=hyperdev-app

# ============================================================
# Redis Credentials (🔴 Requires: REDIS_URL)
# ============================================================
REDIS_URL=redis://:password@host:port
```

---

## Validation Checklist

Once you've added all credentials, verify:

- [ ] GitHub organization name added and valid
- [ ] Cloudflare account ID and email added
- [ ] GCP service account JSON fixed or replaced
- [ ] Redis URL added and tested
- [ ] All 14 tests passing or skipped for valid reasons

**Run full test suite:**
```bash
python -m pytest auto-deployer/tests/credentials/ -v
```

**Expected results after completing all steps:**
- AWS: 3/3 passing
- GitHub: 3/3 passing
- Cloudflare: 3/3 passing
- GCP: 3/3 passing
- Redis: 2/2 passing
- **Total: 14/14 passing** ✅

---

## Troubleshooting

### Test Still Failing After Adding Credentials?

**Step 1: Verify Environment Variables are Loaded**
```bash
# Check if .env file exists
test -f .env && echo ".env exists" || echo ".env missing"

# Verify contents
grep "GITHUB_ORG\|CLOUDFLARE_ACCOUNT_ID\|REDIS_URL" .env
```

**Step 2: Restart Tests**
```bash
# Clear pytest cache
rm -rf .pytest_cache

# Run tests again
python -m pytest auto-deployer/tests/credentials/ -v --tb=short
```

**Step 3: Test Individual Services**
```bash
# Test specific service
python -m pytest auto-deployer/tests/credentials/ -m github -v
python -m pytest auto-deployer/tests/credentials/ -m cloudflare -v
python -m pytest auto-deployer/tests/credentials/ -m gcp -v
python -m pytest auto-deployer/tests/credentials/ -m redis -v
```

**Step 4: Check Specific Test Output**
```bash
# Show full error details
python -m pytest auto-deployer/tests/credentials/test_github_resource.py::TestGitHubAuthenticationResource::test_github_authentication -v --tb=long
```

---

## Security Notes

### Protecting Credentials

1. **Never commit credentials to git:**
   - `.env` file is in `.gitignore`
   - Keep credentials locally only

2. **Use AWS Secrets Manager for backup:**
   - AWS Secrets Manager stores encrypted backups
   - Credentials backed up as: `code-to-site/env-variables`

3. **Rotate keys periodically:**
   - AWS: Generate new access keys quarterly
   - GitHub: Rotate personal access tokens annually
   - Cloudflare: Update API tokens as needed
   - GCP: Rotate service account keys annually
   - Redis: Change passwords if exposed

4. **Limit scope of credentials:**
   - GitHub token: Only needs repository read access
   - Cloudflare token: Only needs Pages and Account Settings read
   - GCP: Use minimal IAM roles (e.g., roles/storage.objectViewer for read-only)
   - Redis: Use separate users/passwords for different applications

---

## Support References

### Official Documentation Links

- **GitHub API:** https://docs.github.com/en/rest
- **Cloudflare API:** https://developers.cloudflare.com/api/
- **Google Cloud:** https://cloud.google.com/docs
- **Redis:** https://redis.io/docs/

### Credential Management Best Practices

- AWS: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- GitHub: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
- Cloudflare: https://developers.cloudflare.com/fundamentals/api/get-started/
- GCP: https://cloud.google.com/docs/authentication/getting-started

---

**Report Generated:** 2026-01-25
**Credential Test Framework Version:** 1.0
**Status:** 3/14 tests passing, 11 awaiting configuration
