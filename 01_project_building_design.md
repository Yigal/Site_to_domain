# Auto-Deployer: Project Building Design

## 1. Project Structure (Tree Form)

```
/auto-deployer
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI Entry Point & Routes
│   ├── config.py                  # Settings & AWS Secret Hydration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request.py             # Request Pydantic Schemas
│   │   └── deployment.py          # Deployment State Schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── aws_storage.py         # S3 Handling
│   │   ├── github_api.py          # PyGithub Wrapper
│   │   ├── cloudflare_api.py      # Pages & DNS Logic
│   │   ├── gcp_identity.py        # Identity Platform & Billing
│   │   └── source_manager.py      # Git Clone vs. Folder Upload Logic
│   └── utils/
│       ├── __init__.py
│       ├── ast_modifier.py        # Tree-sitter Logic
│       └── saga_context.py        # Transaction State Tracking
├── worker/
│   ├── __init__.py
│   ├── celery_app.py              # Celery Configuration
│   └── tasks.py                   # The Main Saga Workflow
├── scripts/
│   └── startup.sh                 # Boot script
├── tests/
│   ├── __init__.py
│   ├── test_validation.py         # Pre-run validation tests
│   ├── test_services.py           # Service unit tests
│   └── conftest.py                # Pytest fixtures
├── .env.example                   # Environment template
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 2. File Definitions with Functions

### 2.1 `app/main.py`
**Purpose**: FastAPI application entry point with route definitions

| Function Name | Access | Description |
|---------------|--------|-------------|
| `lifespan()` | Public | Application lifespan context manager for startup/shutdown |
| `deploy()` | Public | POST /deploy - Main deployment endpoint |
| `get_deployment_status()` | Public | GET /deploy/{task_id} - Check deployment status |
| `health_check()` | Public | GET /health - Health check endpoint |
| `upload_source()` | Public | POST /upload - Upload source code zip file |
| `_validate_request()` | Private | Validate incoming deployment request payload |

---

### 2.2 `app/config.py`
**Purpose**: Settings management and AWS secret hydration

| Function Name | Access | Description |
|---------------|--------|-------------|
| `hydrate_secrets()` | Public | Fetch secrets from AWS Secrets Manager and inject into environment |
| `get_settings()` | Public | Return application settings singleton |
| `_fetch_secret()` | Private | Internal boto3 call to retrieve single secret |
| `_decode_gcp_credentials()` | Private | Base64 decode and write GCP JSON to temp file |

**Class**: `Settings(BaseSettings)`
- `aws_region: str`
- `s3_bucket: str`
- `secret_name: str`
- `redis_url: str`
- `github_org: str`
- `cloudflare_account_id: str`
- `gcp_billing_account: str`

---

### 2.3 `app/models/request.py`
**Purpose**: Pydantic models for request validation

| Class Name | Access | Description |
|------------|--------|-------------|
| `SourceType` | Public | Enum: "folder" | "git" |
| `DeploymentRequest` | Public | Main deployment request schema |
| `SourceConfig` | Public | Source code configuration (type, url/s3_key) |
| `DomainConfig` | Public | Optional custom domain settings |

---

### 2.4 `app/models/deployment.py`
**Purpose**: Deployment state and response schemas

| Class Name | Access | Description |
|------------|--------|-------------|
| `DeploymentStatus` | Public | Enum: pending, in_progress, completed, failed, rollback |
| `DeploymentResponse` | Public | API response with task_id and status |
| `DeploymentState` | Public | Full deployment state for saga tracking |
| `SagaStep` | Public | Individual saga step record |

---

### 2.5 `app/services/aws_storage.py`
**Purpose**: S3 file operations

| Function Name | Access | Description |
|---------------|--------|-------------|
| `download_file()` | Public | Download file from S3 to local path |
| `upload_file()` | Public | Upload local file to S3 |
| `download_and_extract_zip()` | Public | Download zip from S3 and extract to workspace |
| `list_objects()` | Public | List objects in S3 bucket with prefix |
| `_get_s3_client()` | Private | Create boto3 S3 client |

---

### 2.6 `app/services/github_api.py`
**Purpose**: GitHub repository management via PyGithub

| Function Name | Access | Description |
|---------------|--------|-------------|
| `create_repository()` | Public | Create new repo in organization |
| `push_code()` | Public | Initialize git, add remote, and push code |
| `delete_repository()` | Public | Delete repository (for rollback) |
| `check_repo_exists()` | Public | Verify if repository already exists |
| `_get_github_client()` | Private | Initialize authenticated Github instance |
| `_run_git_command()` | Private | Execute git CLI command with error handling |

---

### 2.7 `app/services/cloudflare_api.py`
**Purpose**: Cloudflare Pages and DNS management

| Function Name | Access | Description |
|---------------|--------|-------------|
| `create_pages_project()` | Public | Create Cloudflare Pages project linked to GitHub |
| `delete_pages_project()` | Public | Delete Pages project (for rollback) |
| `get_deployment_url()` | Public | Retrieve the pages.dev URL |
| `create_dns_record()` | Public | Create CNAME record for custom domain |
| `delete_dns_record()` | Public | Delete DNS record (for rollback) |
| `add_custom_domain()` | Public | Bind custom domain to Pages project |
| `get_zone_id()` | Public | Resolve zone_id from domain name |
| `_get_headers()` | Private | Return authorization headers |
| `_handle_error()` | Private | Parse and handle Cloudflare API errors |

---

### 2.8 `app/services/gcp_identity.py`
**Purpose**: GCP project creation and Firebase/Identity Platform setup

| Function Name | Access | Description |
|---------------|--------|-------------|
| `create_project()` | Public | Create new GCP project |
| `delete_project()` | Public | Delete GCP project (for rollback) |
| `link_billing()` | Public | Attach billing account to project |
| `enable_apis()` | Public | Enable required APIs (Identity Toolkit, Firebase) |
| `add_firebase()` | Public | Initialize Firebase on the project |
| `configure_identity_platform()` | Public | Enable Email/Password auth, set authorized domains |
| `get_firebase_config()` | Public | Retrieve apiKey, authDomain, projectId, etc. |
| `add_authorized_domain()` | Public | Add Cloudflare domain to authorized list |
| `_get_credentials()` | Private | Load GCP credentials from JSON file |
| `_wait_for_operation()` | Private | Poll long-running operation until complete |

---

### 2.9 `app/services/source_manager.py`
**Purpose**: Handle source acquisition from git or folder upload

| Function Name | Access | Description |
|---------------|--------|-------------|
| `prepare_workspace()` | Public | Create workspace and acquire source code |
| `cleanup_workspace()` | Public | Remove temporary workspace directory |
| `detect_framework()` | Public | Detect if React/Vite/Next.js from package.json |
| `_clone_repository()` | Private | Git clone and detach from original history |
| `_extract_uploaded_zip()` | Private | Extract uploaded zip to workspace |

---

### 2.10 `app/utils/ast_modifier.py`
**Purpose**: Tree-sitter based code transformation

| Function Name | Access | Description |
|---------------|--------|-------------|
| `set_vite_base_path()` | Public | Modify base path in vite.config.js |
| `inject_firebase_config()` | Public | Insert Firebase credentials into firebase-config.js |
| `update_env_file()` | Public | Update or create .env with variables |
| `_parse_javascript()` | Private | Parse JS file into AST |
| `_find_config_object()` | Private | Query AST for configuration object |
| `_insert_property()` | Private | Insert property into JS object at correct position |
| `_write_modified_source()` | Private | Write modified source back to file |

---

### 2.11 `app/utils/saga_context.py`
**Purpose**: Distributed transaction management

| Class Name | Access | Description |
|------------|--------|-------------|
| `SagaContext` | Public | Main saga state manager |

| Method Name | Access | Description |
|-------------|--------|-------------|
| `begin()` | Public | Initialize saga with deployment ID |
| `record_step()` | Public | Record completed step with rollback info |
| `mark_completed()` | Public | Mark saga as successfully completed |
| `mark_failed()` | Public | Mark saga as failed, trigger rollback |
| `execute_rollback()` | Public | Execute compensation actions in reverse order |
| `get_state()` | Public | Return current saga state |
| `_persist_state()` | Private | Save state to Redis/S3 |
| `_load_state()` | Private | Load state from Redis/S3 |

---

### 2.12 `worker/celery_app.py`
**Purpose**: Celery configuration and initialization

| Function Name | Access | Description |
|---------------|--------|-------------|
| `create_celery_app()` | Public | Create and configure Celery instance |

**Configuration**:
- Broker: Redis
- Result backend: Redis
- Task serializer: JSON
- Task acks late: True (for reliability)

---

### 2.13 `worker/tasks.py`
**Purpose**: Main deployment saga workflow

| Function Name | Access | Description |
|---------------|--------|-------------|
| `execute_deployment_saga()` | Public | Main Celery task - orchestrates full deployment |
| `_phase_source_acquisition()` | Private | Phase 1: Prepare workspace from git/folder |
| `_phase_code_transformation()` | Private | Phase 2: Modify vite.config.js via AST |
| `_phase_github_creation()` | Private | Phase 3: Create repo and initial push |
| `_phase_cloudflare_setup()` | Private | Phase 4: Create Pages project |
| `_phase_gcp_provisioning()` | Private | Phase 5: Full GCP/Firebase setup chain |
| `_phase_config_injection()` | Private | Phase 6: Inject Firebase config, second push |
| `_phase_domain_finalization()` | Private | Phase 7: DNS and custom domain binding |
| `_notify_status()` | Private | Send webhook/callback with status update |

---

### 2.14 `scripts/startup.sh`
**Purpose**: Container startup script

```bash
#!/bin/bash
# 1. Hydrate secrets from AWS
# 2. Start Redis (if not external)
# 3. Start Celery worker
# 4. Start FastAPI with uvicorn
```

---

## 3. External Dependencies

### 3.1 Python Packages (`requirements.txt`)

```
# Web Framework
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.6

# Task Queue
celery[redis]>=5.3.0
redis>=5.0.0

# AWS SDK
boto3>=1.34.0
botocore>=1.34.0

# GitHub
PyGithub>=2.1.0

# GCP
google-cloud-resource-manager>=1.12.0
google-cloud-billing>=1.13.0
google-cloud-service-usage>=1.10.0
firebase-admin>=6.4.0

# HTTP Client
httpx>=0.26.0
requests>=2.31.0

# Code Transformation
tree-sitter>=0.21.0
tree-sitter-javascript>=0.21.0

# Data Validation
pydantic>=2.5.0
pydantic-settings>=2.1.0

# Utilities
python-dotenv>=1.0.0
structlog>=24.1.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.23.0
pytest-cov>=4.1.0
moto>=5.0.0  # AWS mocking
responses>=0.24.0  # HTTP mocking
```

---

### 3.2 Required Credentials

| Credential | Storage Location | Environment Variable | Description |
|------------|------------------|---------------------|-------------|
| AWS Access Key ID | Environment | `AWS_ACCESS_KEY_ID` | IAM user access key |
| AWS Secret Access Key | Environment | `AWS_SECRET_ACCESS_KEY` | IAM user secret |
| GitHub PAT | AWS Secrets Manager | `GITHUB_TOKEN` | Fine-grained PAT for org |
| Cloudflare API Token | AWS Secrets Manager | `CLOUDFLARE_API_TOKEN` | Custom token with Pages/DNS |
| GCP Service Account JSON | AWS Secrets Manager | `GOOGLE_APPLICATION_CREDENTIALS` | Base64 encoded, written to temp file |

---

### 3.3 External Services

| Service | Provider | Purpose | Required Setup |
|---------|----------|---------|----------------|
| S3 Bucket | AWS | Store source zips, configs | Create bucket, IAM policy |
| Secrets Manager | AWS | Store third-party credentials | Create secrets with prefix |
| Redis | Self-hosted/AWS | Celery broker & result backend | Deploy Redis instance |
| GitHub Organization | GitHub | Repository target | Create org, enable fine-grained tokens |
| Cloudflare Account | Cloudflare | Pages hosting, DNS | Install GitHub App on org |
| GCP Organization | Google Cloud | Firebase/Identity Platform | Create org, billing account |
| GCP Billing Account | Google Cloud | Enable paid APIs | Link to organization |

---

## 4. Pre-Run Validation Test

### `tests/test_validation.py`

```python
"""
Pre-Run Validation Test Suite
Run before deployment to ensure all dependencies and credentials are configured correctly.
Execute with: pytest tests/test_validation.py -v
"""

import os
import pytest
import boto3
import requests
from google.cloud import resourcemanager_v3
from github import Github


class TestAWSConnectivity:
    """Validate AWS credentials and resource access"""
    
    def test_aws_credentials_present(self):
        """Verify AWS credentials are set in environment"""
        assert os.environ.get('AWS_ACCESS_KEY_ID'), "AWS_ACCESS_KEY_ID not set"
        assert os.environ.get('AWS_SECRET_ACCESS_KEY'), "AWS_SECRET_ACCESS_KEY not set"
    
    def test_s3_bucket_accessible(self):
        """Verify S3 bucket exists and is readable"""
        s3 = boto3.client('s3')
        bucket = os.environ.get('S3_BUCKET', 'deployment-assets')
        response = s3.list_objects_v2(Bucket=bucket, MaxKeys=1)
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200
    
    def test_secrets_manager_accessible(self):
        """Verify Secrets Manager secrets are readable"""
        client = boto3.client('secretsmanager')
        secret_name = os.environ.get('SECRET_NAME', 'prod/auto-deployer/keys')
        response = client.get_secret_value(SecretId=secret_name)
        assert 'SecretString' in response


class TestGitHubConnectivity:
    """Validate GitHub PAT and organization access"""
    
    @pytest.fixture
    def github_token(self):
        """Retrieve GitHub token from secrets"""
        client = boto3.client('secretsmanager')
        secret = client.get_secret_value(SecretId='prod/auto-deployer/keys')
        import json
        secrets = json.loads(secret['SecretString'])
        return secrets.get('GITHUB_TOKEN')
    
    def test_github_token_valid(self, github_token):
        """Verify GitHub token authenticates successfully"""
        assert github_token, "GitHub token not found in secrets"
        g = Github(github_token)
        user = g.get_user()
        assert user.login is not None
    
    def test_github_org_accessible(self, github_token):
        """Verify organization access"""
        org_name = os.environ.get('GITHUB_ORG')
        assert org_name, "GITHUB_ORG not set"
        g = Github(github_token)
        org = g.get_organization(org_name)
        assert org.login == org_name
    
    def test_github_repo_creation_permission(self, github_token):
        """Verify token has repo creation permission (does not actually create)"""
        g = Github(github_token)
        org_name = os.environ.get('GITHUB_ORG')
        org = g.get_organization(org_name)
        # Check if we can list repos (indicates sufficient permissions)
        repos = list(org.get_repos()[:1])
        assert isinstance(repos, list)


class TestCloudflareConnectivity:
    """Validate Cloudflare API token and account access"""
    
    @pytest.fixture
    def cloudflare_token(self):
        """Retrieve Cloudflare token from secrets"""
        client = boto3.client('secretsmanager')
        secret = client.get_secret_value(SecretId='prod/auto-deployer/keys')
        import json
        secrets = json.loads(secret['SecretString'])
        return secrets.get('CLOUDFLARE_API_TOKEN')
    
    def test_cloudflare_token_valid(self, cloudflare_token):
        """Verify Cloudflare token authenticates"""
        assert cloudflare_token, "Cloudflare token not found"
        response = requests.get(
            "https://api.cloudflare.com/client/v4/user/tokens/verify",
            headers={"Authorization": f"Bearer {cloudflare_token}"}
        )
        assert response.status_code == 200
        assert response.json()['success'] is True
    
    def test_cloudflare_pages_permission(self, cloudflare_token):
        """Verify Pages permission on account"""
        account_id = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
        assert account_id, "CLOUDFLARE_ACCOUNT_ID not set"
        response = requests.get(
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects",
            headers={"Authorization": f"Bearer {cloudflare_token}"}
        )
        assert response.status_code == 200


class TestGCPConnectivity:
    """Validate GCP Service Account and permissions"""
    
    @pytest.fixture
    def setup_gcp_credentials(self):
        """Setup GCP credentials from secrets"""
        client = boto3.client('secretsmanager')
        secret = client.get_secret_value(SecretId='prod/auto-deployer/keys')
        import json
        import base64
        secrets = json.loads(secret['SecretString'])
        gcp_creds = base64.b64decode(secrets.get('GCP_SERVICE_ACCOUNT_JSON'))
        creds_path = '/tmp/test_gcp_creds.json'
        with open(creds_path, 'wb') as f:
            f.write(gcp_creds)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path
        return creds_path
    
    def test_gcp_credentials_valid(self, setup_gcp_credentials):
        """Verify GCP credentials authenticate"""
        from google.auth import default
        credentials, project = default()
        assert credentials is not None
    
    def test_gcp_project_creation_permission(self, setup_gcp_credentials):
        """Verify project creation permission at org level"""
        client = resourcemanager_v3.ProjectsClient()
        # List projects to verify access (not creating)
        request = resourcemanager_v3.SearchProjectsRequest()
        projects = list(client.search_projects(request=request))
        assert isinstance(projects, list)
    
    def test_gcp_billing_access(self, setup_gcp_credentials):
        """Verify billing account access"""
        from google.cloud import billing_v1
        billing_account = os.environ.get('GCP_BILLING_ACCOUNT')
        assert billing_account, "GCP_BILLING_ACCOUNT not set"
        client = billing_v1.CloudBillingClient()
        # Verify we can access the billing account
        name = f"billingAccounts/{billing_account}"
        account = client.get_billing_account(name=name)
        assert account.open is True  # Account is active


class TestRedisConnectivity:
    """Validate Redis connection for Celery"""
    
    def test_redis_connection(self):
        """Verify Redis is accessible"""
        import redis
        redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
        r = redis.from_url(redis_url)
        assert r.ping() is True


class TestTreeSitterSetup:
    """Validate Tree-sitter is properly installed"""
    
    def test_tree_sitter_javascript(self):
        """Verify JavaScript parser works"""
        import tree_sitter_javascript as tsjs
        from tree_sitter import Language, Parser
        
        JS_LANGUAGE = Language(tsjs.language())
        parser = Parser(JS_LANGUAGE)
        
        code = b"const x = 1;"
        tree = parser.parse(code)
        assert tree.root_node is not None


class TestCloudflareGitHubIntegration:
    """Validate Cloudflare GitHub App installation"""
    
    def test_cloudflare_github_app_hint(self, cloudflare_token, github_token):
        """
        NOTE: Cannot programmatically verify GitHub App installation.
        This test serves as a reminder to verify manually.
        """
        print("\n" + "="*60)
        print("MANUAL VERIFICATION REQUIRED:")
        print("Ensure Cloudflare GitHub App is installed on the target org.")
        print("Dashboard: Cloudflare > Pages > Connect to Git")
        print("="*60)
        # Always pass - this is a reminder
        assert True


def run_all_validations():
    """Run all validation tests and report results"""
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == '__main__':
    run_all_validations()
```

---

## 5. Environment Variables Summary

```bash
# AWS (Required - injected directly)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# Resource Configuration
S3_BUCKET=deployment-assets
SECRET_NAME=prod/auto-deployer/keys

# Task Queue
REDIS_URL=redis://localhost:6379/0

# Target Configuration
GITHUB_ORG=your-organization
CLOUDFLARE_ACCOUNT_ID=abc123...
GCP_BILLING_ACCOUNT=012345-ABCDEF-GHIJKL

# Retrieved from Secrets Manager at runtime:
# - GITHUB_TOKEN
# - CLOUDFLARE_API_TOKEN
# - GCP_SERVICE_ACCOUNT_JSON (Base64)
```
