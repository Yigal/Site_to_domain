# Phase 2: Setup & Environment Configuration

**Start Time:** January 25, 2026
**Expected Duration:** 30 minutes
**Status:** IN PROGRESS

---

## Setup Objectives

- [ ] Create project directory structure
- [ ] Initialize Python virtual environment
- [ ] Create and install requirements.txt
- [ ] Configure environment variables
- [ ] Setup Redis (or use Docker)
- [ ] Verify all prerequisites

---

## Prerequisites Verification

### System Requirements
- [ ] Python 3.10 or higher
- [ ] Git installed
- [ ] Docker installed (for Redis)
- [ ] ~500MB disk space available

### Cloud Account Prerequisites
- [ ] AWS Account (for S3 and Secrets Manager)
- [ ] GitHub Account (for repository creation)
- [ ] Cloudflare Account (for Pages and DNS)
- [ ] Google Cloud Platform Account (for GCP and Firebase)

---

## Step 1: Create Project Directory Structure

**Action:** Create the complete project directory structure for auto-deployer

### Directory Layout
```
/auto-deployer/
├── app/                          # FastAPI Web Application
│   ├── __init__.py
│   ├── main.py                   # REST API endpoints
│   ├── config.py                 # Settings & secrets hydration
│   ├── models/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── request.py
│   │   ├── deployment.py
│   │   └── types.py
│   ├── services/                 # Cloud API clients
│   │   ├── __init__.py
│   │   ├── aws_storage.py
│   │   ├── github_api.py
│   │   ├── cloudflare_api.py
│   │   ├── gcp_identity.py
│   │   └── source_manager.py
│   └── utils/                    # Utilities
│       ├── __init__.py
│       ├── ast_modifier.py
│       ├── saga_context.py
│       └── middleware/
│           ├── __init__.py
│           └── error_handler.py
│
├── worker/                       # Celery Background Tasks
│   ├── __init__.py
│   ├── celery_app.py            # Celery configuration
│   └── tasks.py                 # Main saga workflow
│
├── tests/                        # Comprehensive test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   └── test_*.py                # 12+ test modules
│
├── deployment/                   # Container configuration
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── docker-compose.prod.yml
│
├── scripts/                      # Automation scripts
│   ├── startup.sh
│   └── healthcheck.sh
│
├── documentation/                # Reference documentation
│   ├── agents/                  # 14 agent specs
│   ├── skills/                  # 14 skill specs
│   └── API.md                   # OpenAPI docs
│
└── Project Configuration Files
    ├── requirements.txt         # Python dependencies
    ├── pytest.ini              # Test configuration
    ├── .env.example            # Environment template
    ├── .gitignore              # Git configuration
    └── README.md               # Documentation
```

**Status:** ✅ COMPLETED - All directories created successfully

---

## Step 2: Create requirements.txt

**Action:** Create Python dependencies file

### Python Dependencies

#### Web Framework
- fastapi==0.109.0
- uvicorn[standard]==0.27.0
- pydantic==2.5.0
- pydantic-settings==2.1.0
- python-dotenv==1.0.0

#### Async Task Processing
- celery==5.3.0
- redis==5.0.0

#### Cloud SDKs
- boto3==1.34.0
- PyGithub==2.1.0
- google-cloud-resource-manager==1.14.0
- google-cloud-billing==1.11.0
- google-cloud-service-usage==1.8.0
- google-cloud-firebase-admin==6.2.0

#### Code Analysis
- tree-sitter==0.21.0
- tree-sitter-javascript==0.21.0

#### HTTP Clients
- httpx==0.25.0
- requests==2.31.0

#### Logging
- structlog==24.1.0

#### Testing
- pytest==7.4.0
- pytest-asyncio==0.23.0
- pytest-cov==4.1.0
- moto==5.0.0
- responses==0.24.0

#### Utilities
- python-multipart==0.0.6

**Status:** ✅ COMPLETED - requirements.txt created with 33 dependencies

---

## Step 3: Create Virtual Environment

**Action:** Initialize Python virtual environment

```bash
python3.10 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

**Status:** [TO BE FILLED]

---

## Step 4: Install Dependencies

**Action:** Install all required Python packages

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Expected Output:**
- ~30 packages installed
- ~200MB disk usage

**Status:** [TO BE FILLED]

---

## Step 5: Create Environment Configuration

**Action:** Create .env file from template

### Environment Variables Required

```
# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_URL=redis://localhost:6379

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
S3_BUCKET=your_s3_bucket_name

# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_ORG=your_github_organization

# Cloudflare Configuration
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
CLOUDFLARE_TOKEN=your_cloudflare_api_token
CLOUDFLARE_EMAIL=your_cloudflare_email

# GCP Configuration
GCP_PROJECT_ID=your_gcp_project_id
GCP_SERVICE_ACCOUNT=base64_encoded_service_account_json
GCP_BILLING_ACCOUNT=your_billing_account_id

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

**Status:** [TO BE FILLED]

---

## Step 6: Start Redis

**Action:** Start Redis service using Docker

```bash
# Start Redis container
docker run -d --name auto-deployer-redis -p 6379:6379 redis:7-alpine

# Verify connection
redis-cli ping
# Expected response: PONG
```

**Status:** [TO BE FILLED]

---

## Setup Completion Checklist

- [ ] Project directory structure created
- [ ] requirements.txt created with all 30+ dependencies
- [ ] Virtual environment initialized and activated
- [ ] All dependencies installed successfully
- [ ] .env file created with all required variables
- [ ] Redis container running and accessible
- [ ] All system prerequisites verified
- [ ] Cloud credentials configured

---

## Configuration Guidelines

### S3 Bucket Naming (from Appendix D)
```
Format: {environment}-{app-name}-{timestamp}
Examples:
- dev-auto-deployer-1234567890
- staging-auto-deployer-1234567891
- prod-auto-deployer-1234567892
```

### Security Best Practices
1. Never commit .env file to version control
2. Use AWS Secrets Manager for production credentials
3. Rotate API tokens regularly
4. Use restricted IAM policies for cloud accounts
5. Enable MFA for all cloud accounts

### Development vs Production
```
Development:
  - LOCAL Redis
  - LOCAL credentials in .env
  - Debug mode enabled
  - Verbose logging

Production:
  - CLOUD Redis (AWS ElastiCache, Google Memorystore)
  - Secrets Manager for credentials
  - Debug mode disabled
  - Structured JSON logging
```

---

## Verification Commands

### Verify Python Installation
```bash
python3 --version
# Expected: Python 3.10.x or higher
```

### Verify Virtual Environment
```bash
which python
# Should show: /path/to/venv/bin/python
```

### Verify Dependencies
```bash
pip list | grep -E "fastapi|celery|boto3"
```

### Verify Redis Connection
```bash
redis-cli ping
# Expected: PONG
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Python version < 3.10 | Install Python 3.10+ from python.org or use Homebrew |
| pip install fails | Use `pip install --upgrade pip` first, then retry |
| Redis connection fails | Verify Docker is running: `docker ps \| grep redis` |
| Venv activation fails | Check file permissions: `chmod +x venv/bin/activate` |
| AWS credentials error | Verify .env file exists and has correct AWS keys |

---

## Next Phase

Once setup is complete:
1. Verify all prerequisites
2. Run a quick smoke test with `python -c "import fastapi; print('OK')"`
3. Move to **Phase 3: Execution** of all 15 deployment steps

---

**Status:** PENDING EXECUTION
**Time Estimate:** 30 minutes
**Last Updated:** January 25, 2026

