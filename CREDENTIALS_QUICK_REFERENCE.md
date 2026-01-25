# Credentials Quick Reference

Quick lookup for what's needed to complete credential testing.

---

## Test Status Overview

```
✅ AWS        3/3 passing    (Complete)
🔴 GitHub     0/3 skipped    (Missing: GITHUB_ORG)
🔴 Cloudflare 0/3 skipped    (Missing: ACCOUNT_ID, EMAIL)
🔴 GCP        0/3 skipped    (Corrupted: Fix service account)
🔴 Redis      0/2 skipped    (Missing: REDIS_URL)

Total: 3/14 passing, 11/14 awaiting configuration
```

---

## What's Needed vs What's Missing

### AWS ✅
| Item | Status | Value |
|------|--------|-------|
| `AWS_ACCESS_KEY_ID` | ✅ Present | ***REMOVED-AWS-ACCESS-KEY-ID*** |
| `AWS_SECRET_ACCESS_KEY` | ✅ Present | XTCj6vL/pHuleaW5... |
| `AWS_REGION` | ✅ Present | us-east-1 |

### GitHub 🔴 (1/2 items)
| Item | Status | How to Get |
|------|--------|-----------|
| `GITHUB_TOKEN` | ✅ Present | ghp_NHrcVz4L2nKQ... |
| `GITHUB_ORG` | ❌ **MISSING** | Check GitHub.com → Profile → Organizations |

**Action:** Add 1 line to .env
```bash
GITHUB_ORG=your-org-name
```

---

### Cloudflare 🔴 (1/3 items)
| Item | Status | How to Get |
|------|--------|-----------|
| `CLOUDFLARE_TOKEN` | ✅ Present | JNHIc0aucIaUMZ... |
| `CLOUDFLARE_ACCOUNT_ID` | ❌ **MISSING** | Cloudflare Dashboard → Copy Account ID |
| `CLOUDFLARE_EMAIL` | ❌ **MISSING** | Email you use to log into Cloudflare |

**Action:** Add 2 lines to .env
```bash
CLOUDFLARE_ACCOUNT_ID=abc123xyz
CLOUDFLARE_EMAIL=your@email.com
```

---

### GCP ⚠️ (Corrupted)
| Item | Status | Issue |
|------|--------|-------|
| `GCP_PROJECT_ID` | ✅ Present | hyperdev-app |
| `GCP_SERVICE_ACCOUNT` | 🔴 **CORRUPTED** | Invalid Unicode escape: `\u000` → needs `\u0000` |

**Action:** Replace with fresh credentials
1. Download new service account from Google Cloud Console
2. Encode to base64
3. Replace entire `GCP_SERVICE_ACCOUNT` value

```bash
GCP_SERVICE_ACCOUNT=your-fresh-base64-encoded-value
```

---

### Redis 🔴 (0/1 items)
| Item | Status | How to Get |
|------|--------|-----------|
| `REDIS_URL` | ❌ **MISSING** | Redis host connection string |

**Action:** Add 1 line to .env
```bash
REDIS_URL=redis://:password@host:port
```

**Examples:**
- Local: `redis://localhost:6379`
- With password: `redis://:mypass@localhost:6379`
- Remote: `redis://redis.example.com:6379`
- Cloud: `redis://:apikey@instance.redis.cloud:port`

---

## Fastest Path to 100% Tests Passing

### Tier 1: Easiest (5 minutes)
```bash
# 1. Get GitHub org from https://github.com → Profile → Organizations
echo "GITHUB_ORG=your-org" >> .env

# 2. Run tests
python -m pytest auto-deployer/tests/credentials/ -m github -v
# Result: +3 tests passing
```

### Tier 2: Quick (10 minutes)
```bash
# 1. Cloudflare Dashboard → Get Account ID and confirm email
echo "CLOUDFLARE_ACCOUNT_ID=your-id" >> .env
echo "CLOUDFLARE_EMAIL=your@email.com" >> .env

# 2. Run tests
python -m pytest auto-deployer/tests/credentials/ -m cloudflare -v
# Result: +3 tests passing
```

### Tier 3: Medium (15 minutes)
```bash
# 1. Get Redis connection string from your Redis provider
#    Test it first: redis-cli -u "redis://..." ping
echo "REDIS_URL=your-redis-url" >> .env

# 2. Run tests
python -m pytest auto-deployer/tests/credentials/ -m redis -v
# Result: +2 tests passing
```

### Tier 4: Longer (15 minutes)
```bash
# 1. Google Cloud Console → Create/download service account JSON
# 2. Encode to base64: cat file.json | base64 | tr -d '\n'
# 3. Replace GCP_SERVICE_ACCOUNT value in .env

# 4. Run tests
python -m pytest auto-deployer/tests/credentials/ -m gcp -v
# Result: +3 tests passing
```

**Final Result: 14/14 tests passing ✅**

---

## Environment Variables Needed

### Current .env
```bash
# ✅ Have these
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=...
GITHUB_TOKEN=...
CLOUDFLARE_TOKEN=...
GCP_SERVICE_ACCOUNT=... (corrupted)
GCP_PROJECT_ID=...

# ❌ Missing these
GITHUB_ORG=                           # ADD THIS
CLOUDFLARE_ACCOUNT_ID=                # ADD THIS
CLOUDFLARE_EMAIL=                     # ADD THIS
GCP_SERVICE_ACCOUNT=... (FIX THIS)    # REPLACE THIS
REDIS_URL=                            # ADD THIS
```

---

## Credentials by Service

### GitHub
```
What:     Organization name for your GitHub repositories
Where:    https://github.com → Profile dropdown → Your organizations
Example:  GITHUB_ORG=my-company
Takes:    2-3 minutes
```

### Cloudflare
```
What 1:   Account ID (unique identifier)
Where 1:  https://dash.cloudflare.com → Click account name → Copy ID
Example:  CLOUDFLARE_ACCOUNT_ID=a1b2c3d4e5f6g7h8i9j0

What 2:   Email (login email for Cloudflare account)
Where 2:  Your email address you use to log in
Example:  CLOUDFLARE_EMAIL=admin@company.com
Takes:    5-10 minutes
```

### GCP
```
What:     Service account credentials (JSON format, base64 encoded)
Where:    Google Cloud Console → IAM & Admin → Service Accounts
Steps:    1. Download new service account JSON
          2. Encode to base64
          3. Replace GCP_SERVICE_ACCOUNT value
Example:  GCP_SERVICE_ACCOUNT=ewogICJ0eXBlIjogInNlcnZpY2VfYWNj...
Takes:    10-15 minutes
```

### Redis
```
What:     Connection URL with host, port, and password
Where:    Depends on provider:
          - Local/Docker: redis://localhost:6379
          - AWS ElastiCache: redis://endpoint:6379
          - Redis Cloud: https://app.redis.com
          - Azure Cache: Portal → Access Keys

Example:  REDIS_URL=redis://:password@localhost:6379
Takes:    5-15 minutes depending on setup
```

---

## Quick Commands

```bash
# Run all tests
python -m pytest auto-deployer/tests/credentials/ -v

# Run by service
python -m pytest auto-deployer/tests/credentials/ -m aws -v
python -m pytest auto-deployer/tests/credentials/ -m github -v
python -m pytest auto-deployer/tests/credentials/ -m cloudflare -v
python -m pytest auto-deployer/tests/credentials/ -m gcp -v
python -m pytest auto-deployer/tests/credentials/ -m redis -v

# Show skipped reasons
python -m pytest auto-deployer/tests/credentials/ -v -ra

# Test a single service
python -m pytest auto-deployer/tests/credentials/test_github_resource.py -v

# View full error details
python -m pytest auto-deployer/tests/credentials/test_gcp_resource.py -v --tb=long
```

---

## Missing Items Summary

| # | Service | Missing | Location to Get | Difficulty | Time |
|---|---------|---------|-----------------|------------|------|
| 1 | GitHub | GITHUB_ORG | github.com/settings/organizations | Easy | 2 min |
| 2 | Cloudflare | ACCOUNT_ID | dash.cloudflare.com | Easy | 2 min |
| 3 | Cloudflare | EMAIL | Your login email | Easy | 1 min |
| 4 | Redis | REDIS_URL | Redis provider | Medium | 5-15 min |
| 5 | GCP | Fix service account | Google Cloud Console | Medium | 10 min |

**Total time to fix everything: 20-45 minutes**

---

## Validation Commands

After adding each credential:

```bash
# GitHub (after adding GITHUB_ORG)
python -m pytest auto-deployer/tests/credentials/test_github_resource.py::TestGitHubAuthenticationResource::test_github_authentication -v

# Cloudflare (after adding ACCOUNT_ID and EMAIL)
python -m pytest auto-deployer/tests/credentials/test_cloudflare_resource.py::TestCloudflareAuthenticationResource::test_cloudflare_authentication -v

# Redis (after adding REDIS_URL)
python -m pytest auto-deployer/tests/credentials/test_redis_resource.py::TestRedisConnectionResource::test_redis_connection -v

# GCP (after fixing service account)
python -m pytest auto-deployer/tests/credentials/test_gcp_resource.py::TestGCPAuthenticationResource::test_gcp_authentication -v
```

---

## Detailed Guide Location

For step-by-step instructions on obtaining each credential, see:
**`CREDENTIALS_REQUIREMENTS.md`**

This file includes:
- Detailed instructions for each service
- Screenshots and console examples
- Troubleshooting section
- Security best practices
- Official documentation links

---

## Files Reference

| File | Purpose |
|------|---------|
| `.env` | Your local credential storage (never commit) |
| `CREDENTIALS_REQUIREMENTS.md` | Detailed acquisition guide |
| `CREDENTIALS_QUICK_REFERENCE.md` | This file (quick lookup) |
| `CREDENTIAL_TEST_RESULTS.md` | Test execution results and analysis |
| `auto-deployer/tests/credentials/conftest.py` | Test configuration |
| `auto-deployer/tests/credentials/test_*.py` | Individual service tests |

---

## Current Status

```
Tests Run:     14
Tests Passed:  3 (AWS)
Tests Skipped: 11
  - GitHub:      3 (need GITHUB_ORG)
  - Cloudflare:  3 (need ACCOUNT_ID, EMAIL)
  - GCP:         3 (corrupted service account)
  - Redis:       2 (need REDIS_URL)

Pass Rate: 21.4%
Goal: 100% (14/14)
```

---

## Next Steps

1. **Pick one:** Start with GitHub (easiest, 2-3 minutes)
2. **Follow guide:** Use CREDENTIALS_REQUIREMENTS.md for detailed steps
3. **Add to .env:** Add the value following the format
4. **Test:** Run the service test to validate
5. **Repeat:** Move to next service

**Estimated total time: 20-45 minutes**

---

*Last Updated: 2026-01-25*
