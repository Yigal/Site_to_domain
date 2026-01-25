# Auto-Deployer: User Credentials Setup Guide

This guide provides step-by-step instructions for obtaining and configuring all required credentials for the Auto-Deployer system. Follow each section carefully to ensure proper access and security.

---

## Table of Contents

1. [Overview](#overview)
2. [AWS Credentials](#aws-credentials)
3. [GitHub Personal Access Token](#github-personal-access-token)
4. [Cloudflare API Token](#cloudflare-api-token)
5. [Google Cloud Platform Credentials](#google-cloud-platform-credentials)
6. [Storing Credentials in AWS Secrets Manager](#storing-credentials-in-aws-secrets-manager)
7. [Environment Variables](#environment-variables)
8. [Verification Checklist](#verification-checklist)

---

## Overview

The Auto-Deployer requires credentials from four cloud providers:

| Provider | Purpose | Credential Type |
|----------|---------|-----------------|
| AWS | Secrets storage, S3 file storage | IAM User Access Keys |
| GitHub | Repository creation and management | Fine-Grained Personal Access Token |
| Cloudflare | Pages deployment, DNS management | API Token |
| GCP | Firebase/Identity Platform setup | Service Account JSON Key |

**Security Principle**: All third-party credentials (GitHub, Cloudflare, GCP) are stored in AWS Secrets Manager. Only AWS credentials are injected directly into the environment.

---

## AWS Credentials

### Purpose
- Read deployment configurations from S3
- Retrieve third-party credentials from Secrets Manager

### Required Permissions

| Permission | Resource | Purpose |
|------------|----------|---------|
| `s3:GetObject` | `arn:aws:s3:::deployment-assets/*` | Download config files |
| `s3:ListBucket` | `arn:aws:s3:::deployment-assets` | Verify bucket exists |
| `s3:PutObject` | `arn:aws:s3:::deployment-assets/*` | Upload source zips |
| `secretsmanager:GetSecretValue` | `arn:aws:secretsmanager:*:*:secret:prod/auto-deployer/*` | Retrieve API keys |

### Step-by-Step Instructions

#### 1. Create IAM Policy

1. Sign in to the **AWS Management Console**
2. Navigate to **IAM** → **Policies** → **Create Policy**
3. Select the **JSON** tab
4. Paste the following policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3Access",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::deployment-assets",
                "arn:aws:s3:::deployment-assets/*"
            ]
        },
        {
            "Sid": "SecretsManagerAccess",
            "Effect": "Allow",
            "Action": "secretsmanager:GetSecretValue",
            "Resource": "arn:aws:secretsmanager:*:*:secret:prod/auto-deployer/*"
        }
    ]
}
```

5. Click **Next: Tags** (optional)
6. Click **Next: Review**
7. Name: `auto-deployer-policy`
8. Click **Create policy**

#### 2. Create IAM User

1. Navigate to **IAM** → **Users** → **Create user**
2. User name: `svc-frontend-orchestrator`
3. Do NOT check "Provide user access to the AWS Management Console"
4. Click **Next**
5. Select **Attach policies directly**
6. Search for and select `auto-deployer-policy`
7. Click **Next** → **Create user**

#### 3. Generate Access Keys

1. Click on the newly created user
2. Go to **Security credentials** tab
3. Under **Access keys**, click **Create access key**
4. Select **Application running outside AWS**
5. Click **Next** → **Create access key**
6. **IMPORTANT**: Download or copy both values:
   - Access key ID (e.g., `***REMOVED-AWS-ACCESS-KEY-ID***`)
   - Secret access key (e.g., `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)

> ⚠️ **Warning**: The secret access key is shown only once. Store it securely.

---

## GitHub Personal Access Token

### Purpose
- Create repositories in your organization
- Push code to repositories

### Required Permissions

| Category | Permission | Level |
|----------|------------|-------|
| Administration | Read and write | Required |
| Contents | Read and write | Required |
| Metadata | Read-only | Required |
| Workflows | Read and write | Optional |

### Prerequisites

- You must be an **Owner** of the target GitHub Organization
- Fine-grained tokens must be enabled for your organization

### Step-by-Step Instructions

#### 1. Enable Fine-Grained Tokens (Organization Owner)

1. Go to your **Organization Settings**
2. Navigate to **Third-party Access** → **Personal access tokens**
3. Under "Fine-grained personal access tokens", click **Allow access via fine-grained personal access tokens**
4. Save changes

#### 2. Generate the Token

1. Go to your **GitHub User Settings** (click profile → Settings)
2. Navigate to **Developer settings** → **Personal access tokens** → **Fine-grained tokens**
3. Click **Generate new token**
4. Configure the token:

| Field | Value |
|-------|-------|
| Token name | `auto-deployer-production` |
| Expiration | 90 days (or custom - remember to rotate!) |
| Resource owner | **Select your Organization** (not personal) |
| Repository access | **All repositories** |

5. Under **Permissions**, expand **Repository permissions**:
   - **Administration**: Read and write
   - **Contents**: Read and write
   - **Metadata**: Read-only

6. Click **Generate token**
7. Copy the token (starts with `github_pat_...`)

> ⚠️ **Warning**: The token is shown only once. Store it securely.

> 📝 **Note**: "All repositories" is required because the automation creates NEW repositories that don't exist at token creation time.

---

## Cloudflare API Token

### Purpose
- Create and manage Cloudflare Pages projects
- Create DNS records for custom domains

### Required Permissions

| Category | Permission | Level |
|----------|------------|-------|
| Account - Cloudflare Pages | Edit | Required |
| Zone - DNS | Edit | Required (for custom domains) |
| Zone - Zone | Read | Required |

### Prerequisites

**Critical**: The Cloudflare GitHub App must be installed on your GitHub Organization before the API can link repositories.

#### Install Cloudflare GitHub App

1. Go to **Cloudflare Dashboard** → **Pages**
2. Click **Create a project** → **Connect to Git**
3. Select **GitHub**
4. Authorize the Cloudflare GitHub App for your organization
5. Grant access to **All repositories** (or "Future repositories")
6. Complete the OAuth flow

> ⚠️ **Important**: Without this step, the API will fail with error code `8000011`.

### Step-by-Step Instructions

#### 1. Create Custom API Token

1. Go to **Cloudflare Dashboard**
2. Click your profile icon → **My Profile** → **API Tokens**
3. Click **Create Token**
4. Click **Create Custom Token** (do NOT use templates)
5. Configure the token:

| Field | Value |
|-------|-------|
| Token name | `auto-deployer-pages-dns` |

6. Add permissions:

| Permission | Access |
|------------|--------|
| Account - Cloudflare Pages | Edit |
| Zone - DNS | Edit |
| Zone - Zone | Read |

7. Under **Account Resources**, select:
   - Include → Specific account → **Your Account**

8. Under **Zone Resources**, select:
   - Include → All zones (or specific zones if preferred)

9. Click **Continue to summary** → **Create Token**
10. Copy the token

> ⚠️ **Warning**: The token is shown only once. Store it securely.

### Find Your Account ID

1. Go to any **Zone** in your Cloudflare dashboard
2. On the right sidebar, find **Account ID**
3. Copy this value (you'll need it for environment variables)

---

## Google Cloud Platform Credentials

### Purpose
- Create GCP projects programmatically
- Enable Firebase and Identity Platform
- Configure authentication providers

### Required Roles

| Role | Scope | Purpose |
|------|-------|---------|
| `roles/resourcemanager.projectCreator` | Organization | Create new projects |
| `roles/billing.user` | Billing Account | Attach billing to projects |
| `roles/serviceusage.serviceUsageAdmin` | Projects (created) | Enable APIs |
| `roles/firebase.admin` | Projects (created) | Manage Firebase resources |

### Prerequisites

- Access to a GCP Organization
- Access to a Billing Account
- Permission to create Service Accounts

### Step-by-Step Instructions

#### 1. Create a Host Project

If you don't have an existing project to host the service account:

1. Go to **Google Cloud Console**
2. Click the project selector → **New Project**
3. Name: `automation-host-prod`
4. Organization: Select your organization
5. Click **Create**

#### 2. Create Service Account

1. Go to **IAM & Admin** → **Service Accounts**
2. Ensure you're in the host project (`automation-host-prod`)
3. Click **Create Service Account**
4. Configure:

| Field | Value |
|-------|-------|
| Service account name | `auto-deployer-sa` |
| Service account ID | `auto-deployer-sa` |
| Description | Automated frontend deployment service |

5. Click **Create and Continue**
6. Skip the "Grant this service account access to project" step (we'll do this at org level)
7. Click **Done**

#### 3. Generate JSON Key

1. Click on the newly created service account
2. Go to **Keys** tab
3. Click **Add Key** → **Create new key**
4. Select **JSON**
5. Click **Create**
6. The key file downloads automatically

> ⚠️ **Critical**: Store this file securely. It provides full access as this service account.

#### 4. Grant Organization-Level Permission

1. Go to **IAM & Admin** → **IAM**
2. In the project selector (top-left), select your **Organization**
3. Click **Grant Access**
4. In "New principals", enter the service account email:
   `auto-deployer-sa@automation-host-prod.iam.gserviceaccount.com`
5. Assign role: **Project Creator** (`roles/resourcemanager.projectCreator`)
6. Click **Save**

#### 5. Grant Billing Account Permission

This is the most commonly missed step and causes billing link failures.

1. Go to **Billing** in the Google Cloud Console
2. Select your Billing Account
3. Click **Account Management** (right panel)
4. Click **Add Principal**
5. Enter the service account email
6. Assign role: **Billing Account User** (`roles/billing.user`)
7. Click **Save**

> ⚠️ **Critical**: This role must be granted ON THE BILLING ACCOUNT, not on a project.

#### 6. Note Your Billing Account ID

1. In the Billing section, your billing account ID is shown
2. Format: `XXXXXX-XXXXXX-XXXXXX`
3. Save this for environment variables

---

## Storing Credentials in AWS Secrets Manager

All third-party credentials should be stored in AWS Secrets Manager, not as environment variables.

### Step-by-Step Instructions

1. Go to **AWS Secrets Manager**
2. Click **Store a new secret**
3. Select **Other type of secret**
4. Add the following key/value pairs:

| Key | Value |
|-----|-------|
| `GITHUB_TOKEN` | Your GitHub PAT (`github_pat_...`) |
| `CLOUDFLARE_API_TOKEN` | Your Cloudflare token |
| `GCP_SERVICE_ACCOUNT_JSON` | Base64-encoded contents of the JSON key file |

#### Base64 Encode the GCP Key

On macOS/Linux:
```bash
base64 -i /path/to/key.json | tr -d '\n'
```

On Windows (PowerShell):
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("C:\path\to\key.json"))
```

5. Click **Next**
6. Secret name: `prod/auto-deployer/keys`
7. Click **Next** → **Next** → **Store**

---

## Environment Variables

### Required Variables (Set in Deployment Environment)

```bash
# AWS Credentials (direct injection)
AWS_ACCESS_KEY_ID=AKIA...your-access-key
AWS_SECRET_ACCESS_KEY=...your-secret-key
AWS_REGION=us-east-1

# Resource Configuration
S3_BUCKET=deployment-assets
SECRET_NAME=prod/auto-deployer/keys

# Task Queue
REDIS_URL=redis://localhost:6379/0

# Target Configuration
GITHUB_ORG=your-github-organization
CLOUDFLARE_ACCOUNT_ID=your-cloudflare-account-id
GCP_BILLING_ACCOUNT=XXXXXX-XXXXXX-XXXXXX
```

### Variables Retrieved from Secrets Manager (Automatic)

These are fetched at runtime by the application:
- `GITHUB_TOKEN`
- `CLOUDFLARE_API_TOKEN`
- `GOOGLE_APPLICATION_CREDENTIALS` (path to decoded JSON file)

---

## Verification Checklist

Use this checklist to verify all credentials are properly configured:

### AWS
- [ ] IAM user `svc-frontend-orchestrator` exists
- [ ] Custom policy `auto-deployer-policy` is attached
- [ ] Access key ID and secret are saved
- [ ] S3 bucket `deployment-assets` exists
- [ ] Secret `prod/auto-deployer/keys` exists in Secrets Manager

### GitHub
- [ ] Fine-grained tokens enabled for organization
- [ ] Token generated with correct resource owner (organization)
- [ ] Administration, Contents, Metadata permissions granted
- [ ] Token stored in Secrets Manager

### Cloudflare
- [ ] Cloudflare GitHub App installed on GitHub organization
- [ ] Custom API token created with Pages and DNS permissions
- [ ] Account ID noted
- [ ] Token stored in Secrets Manager

### GCP
- [ ] Service account `auto-deployer-sa` created
- [ ] JSON key generated and Base64-encoded
- [ ] `roles/resourcemanager.projectCreator` granted at Organization level
- [ ] `roles/billing.user` granted ON the Billing Account (not project)
- [ ] Billing Account ID noted
- [ ] JSON key stored in Secrets Manager

### Environment
- [ ] All environment variables set
- [ ] Redis accessible
- [ ] Pre-run validation tests pass

---

## Troubleshooting Common Issues

### "Cloudflare error 8000011"
**Cause**: Cloudflare GitHub App not installed on the organization.
**Solution**: Follow the "Install Cloudflare GitHub App" steps in the Cloudflare section.

### "GCP: Billing account not found or permission denied"
**Cause**: `roles/billing.user` not granted on the billing account itself.
**Solution**: Grant the role ON THE BILLING ACCOUNT in the Billing console, not in IAM.

### "GitHub: Resource not accessible by integration"
**Cause**: Token doesn't have access to the organization.
**Solution**: Regenerate the token with the organization as the Resource Owner.

### "AWS: Access Denied for GetSecretValue"
**Cause**: IAM policy doesn't cover the secret path.
**Solution**: Ensure the secret name matches `prod/auto-deployer/*` pattern.

---

## Security Best Practices

1. **Rotate credentials regularly** - Set calendar reminders for token expiration
2. **Use least privilege** - Never use admin/owner tokens for automation
3. **Monitor access logs** - Enable CloudTrail, GitHub audit logs
4. **Never commit credentials** - Use `.gitignore` for `.env` files
5. **Encrypt at rest** - AWS Secrets Manager handles this automatically
6. **Restrict network access** - Use VPC endpoints for AWS services where possible
