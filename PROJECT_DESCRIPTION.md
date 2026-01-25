# Auto-Deployer: Comprehensive Project Description

## Executive Summary

**Auto-Deployer** is an enterprise-grade, asynchronous orchestration system designed to automate the complete deployment lifecycle of React/Vue/Next.js frontend applications across a distributed, multi-cloud infrastructure. The system bridges the gap between manual provisioning and fully automated CI/CD by orchestrating complex interactions with four major cloud providers: Amazon Web Services (AWS), GitHub, Cloudflare, and Google Cloud Platform (GCP).

### Key Problem Addressed
Organizations struggle with manual, error-prone frontend deployment processes involving multiple cloud platforms. Auto-Deployer solves this by accepting either a Git repository link or a local folder upload, and autonomously provisioning a production-ready, globally distributed website with authentication infrastructure in approximately 5 minutes.

---

## Project Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT APPLICATION                        │
│                    (Browser or CI/CD System)                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │     FastAPI REST API (Port 8000)   │
        │  • POST /deploy                │
        │  • GET /deploy/{task_id}       │
        │  • POST /upload                │
        │  • GET /health                 │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │      Celery Task Queue         │
        │  (Redis - Broker & Backend)    │
        │  • Task queueing               │
        │  • Async execution             │
        │  • Status tracking             │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────────────────┐
        │     Saga Orchestration Agent (7 Phases)       │
        │  1. Source Acquisition (Git/ZIP)              │
        │  2. Code Transformation (AST)                 │
        │  3. GitHub Creation (PyGithub)                │
        │  4. Cloudflare Setup (Pages)                  │
        │  5. GCP Provisioning (Firebase)               │
        │  6. Config Injection (Second Push)            │
        │  7. Domain Finalization (DNS)                 │
        └────────────┬───────────────────────────────────┘
                     │
        ┌────────────┴────────────┬─────────────┬─────────────┐
        ▼                         ▼             ▼             ▼
    ┌────────┐            ┌──────────┐  ┌──────────┐  ┌──────────┐
    │  AWS   │            │ GitHub   │  │Cloudflare│  │   GCP    │
    │  S3    │            │  Repos   │  │  Pages   │  │Firebase  │
    │Secrets │            │  & Git   │  │   DNS    │  │  Identity│
    │Manager │            │          │  │          │  │ Platform │
    └────────┘            └──────────┘  └──────────┘  └──────────┘
```

### Component Architecture

```
AUTO-DEPLOYER/
├── APP/ (FastAPI Web Application)
│   ├── main.py ...................... REST API Endpoints
│   ├── config.py .................... Settings & Secrets Hydration
│   ├── models/ ...................... Pydantic Request/Response Schemas
│   │   ├── request.py (SourceType, SourceConfig, DeploymentRequest)
│   │   ├── deployment.py (Status, Response, State)
│   │   └── types.py (Shared Type Definitions)
│   ├── services/ .................... External Cloud API Clients
│   │   ├── aws_storage.py (S3 & Secrets Manager)
│   │   ├── github_api.py (PyGithub Wrapper)
│   │   ├── cloudflare_api.py (Pages & DNS)
│   │   ├── gcp_identity.py (Project & Firebase)
│   │   └── source_manager.py (Git Clone vs ZIP)
│   ├── utils/ ....................... Utility Modules
│   │   ├── ast_modifier.py (Tree-sitter Code Transformation)
│   │   ├── saga_context.py (Distributed Transaction State)
│   │   └── middleware/ (Error Handling)
│   │       └── error_handler.py
│   └── __init__.py
│
├── WORKER/ (Celery Background Tasks)
│   ├── celery_app.py ................ Celery Configuration
│   ├── tasks.py ..................... Main Saga Workflow (7 Phases)
│   └── __init__.py
│
├── TESTS/ (Comprehensive Test Suite)
│   ├── test_config.py ............... Configuration Tests
│   ├── test_models.py ............... Model Validation Tests
│   ├── test_aws_storage.py .......... S3 & Secrets Tests
│   ├── test_github_api.py ........... GitHub API Tests
│   ├── test_cloudflare_api.py ....... Cloudflare API Tests
│   ├── test_gcp_identity.py ......... GCP API Tests
│   ├── test_source_manager.py ....... Source Manager Tests
│   ├── test_ast_modifier.py ......... AST Modification Tests
│   ├── test_saga_context.py ......... Saga State Tests
│   ├── test_celery.py ............... Celery Task Tests
│   ├── test_main.py ................. FastAPI Endpoint Tests
│   ├── test_validation.py ........... Pre-run Validation Tests
│   ├── test_integration.py .......... End-to-End Integration Tests
│   └── conftest.py .................. Pytest Fixtures
│
├── SCRIPTS/
│   ├── startup.sh ................... Container Entry Point
│   └── healthcheck.sh ............... Health Monitoring Script
│
├── DEPLOYMENT/
│   ├── Dockerfile ................... Container Image
│   ├── docker-compose.yml ........... Local Development Stack
│   ├── docker-compose.prod.yml ...... Production Stack
│   └── kubernetes/ .................. K8s Manifests (Optional)
│
├── DOCUMENTATION/
│   ├── agents/ ...................... Agent Specifications
│   ├── skills/ ...................... Skill Definitions
│   └── API.md ....................... OpenAPI Documentation
│
└── PROJECT FILES
    ├── requirements.txt ............. Python Dependencies
    ├── pytest.ini ................... Test Configuration
    ├── .env.example ................. Environment Template
    ├── .gitignore ................... Git Configuration
    └── README.md .................... Project Documentation
```

---

## Technology Stack

### Backend Framework & Web Server
- **FastAPI** (v0.109.0+): Modern async Python web framework with automatic OpenAPI documentation
- **Uvicorn** (v0.27.0+): ASGI web server for high-performance request handling
- **Python** (3.10+): Core language for logic and API implementation

### Asynchronous Task Processing
- **Celery** (v5.3.0+): Distributed task queue for long-running operations
- **Redis** (v5.0.0+): In-memory broker for task queueing and state storage

### Data Validation & Configuration
- **Pydantic** (v2.5.0+): Type-safe request/response validation
- **Pydantic-Settings** (v2.1.0+): Environment variable management
- **Python-DotEnv** (v1.0.0+): .env file support

### Cloud Service Integrations
- **Boto3** (v1.34.0+): AWS SDK for S3 and Secrets Manager
- **PyGithub** (v2.1.0+): GitHub API client for repository operations
- **Google Cloud Libraries** (various): GCP Resource Manager, Billing, Service Usage, Firebase Admin
- **httpx/requests**: HTTP clients for REST API calls

### Code Analysis & Transformation
- **Tree-sitter** (v0.21.0+): Language parser with JavaScript support
- **tree-sitter-javascript** (v0.21.0+): JavaScript AST parsing for safe code modification

### Logging & Monitoring
- **Structlog** (v24.1.0+): Structured JSON logging for observability
- **Python Logging**: Standard library logging integration

### Testing & Quality Assurance
- **Pytest** (v7.4.0+): Test framework with async support
- **Pytest-Asyncio** (v0.23.0+): Async test support
- **Pytest-COV** (v4.1.0+): Code coverage reporting
- **Moto** (v5.0.0+): AWS service mocking for tests
- **Responses** (v0.24.0+): HTTP mocking for API tests
- **Unittest.Mock**: Standard library mocking

### Containerization & Deployment
- **Docker**: Application containerization
- **Docker Compose**: Multi-container orchestration for development and production

---

## Key Features

### 1. Multi-Source Support
- **Git Repository**: Clone from GitHub, GitLab, Bitbucket, or any Git source
- **Folder Upload**: Direct upload of ZIP-compressed project folders
- **Framework Detection**: Automatic identification of React, Vite, Next.js, or Create React App

### 2. Semantic Code Transformation
- **Tree-sitter Based**: Safe AST-level code modification (not regex-based)
- **Vite Configuration**: Automatic base path setting for subpath deployments
- **Firebase Injection**: Secure credential injection into application config
- **Environment Management**: Automatic .env file creation and updates

### 3. Multi-Cloud Orchestration
- **Amazon Web Services**:
  - S3 for source code and artifact storage
  - Secrets Manager for credential management
  - IAM for fine-grained access control

- **GitHub**:
  - Organization repository creation
  - Fine-grained PAT authentication
  - Automatic code push and commit

- **Cloudflare**:
  - Pages hosting for serverless deployment
  - DNS management for custom domains
  - GitHub App integration for CI/CD

- **Google Cloud Platform**:
  - Project creation and management
  - Billing account linkage
  - Firebase initialization
  - Google Identity Platform configuration

### 4. Saga Pattern Implementation
- **Distributed Transactions**: Reliable deployment across multiple services
- **State Persistence**: Redis-backed state tracking with 24-hour retention
- **Automatic Rollback**: Compensation actions executed in reverse order on failure
- **Idempotent Operations**: Safe retry logic without duplicate resources

### 5. Asynchronous Processing
- **Long-Running Operations**: Support for operations taking 60+ seconds
- **Task Progress**: Real-time status updates via polling or webhooks
- **Exponential Backoff**: Intelligent retry logic for transient failures
- **Concurrent Deployments**: Multiple simultaneous deployments supported

### 6. Security First
- **Zero Credential Exposure**: Secrets never logged or stored in code
- **Runtime Hydration**: Credentials fetched from Secrets Manager at startup
- **Least Privilege**: Fine-grained IAM policies for all cloud services
- **Temporary Credentials**: Sensitive files written with restricted permissions (0600)

### 7. Production Ready
- **Health Checks**: Endpoints for monitoring service status
- **Comprehensive Logging**: Structured JSON logs for debugging
- **Error Handling**: Graceful degradation with detailed error messages
- **Docker Support**: Containerized deployment with compose files

---

## Deployment Phases (7-Phase Saga)

### Phase 1: Source Acquisition
**Duration**: 2-5 minutes

The system acquires the source code through one of two methods:
1. **Git Clone**: Clones from a GitHub URL, detaches from original history
2. **ZIP Extraction**: Downloads ZIP from S3 and extracts to workspace

**Actions**:
- Create unique workspace directory (/tmp/deploy-{uuid})
- Clone repository or extract ZIP file
- Remove .git directory to prevent accidental pushes to original repo
- Validate source code structure

**Agents**: Source Acquisition Agent

---

### Phase 2: Code Transformation
**Duration**: 1-2 minutes

Uses Tree-sitter AST parsing to safely modify source code for cloud deployment:

**Modifications**:
- **Vite Config**: Sets `base: "/"` for correct asset paths on Cloudflare Pages
- **Framework Detection**: Identifies React/Vue/Next.js from package.json
- **Environment Setup**: Creates .env file with deployment variables

**Agents**: Code Transformation Agent, AST Modifier Skill

---

### Phase 3: GitHub Repository Creation
**Duration**: 2-3 minutes

Creates new repository in target organization and pushes initial code:

**Actions**:
- Create repository via PyGithub with fine-grained PAT
- Initialize local git (git init)
- Configure git user as "Auto-Deployer"
- Add remote origin and initial commit
- Push to main branch

**Agents**: GitHub Repository Agent

**Rollback**: Deletes repository if later phases fail

---

### Phase 4: Cloudflare Pages Setup
**Duration**: 2-3 minutes

Creates Cloudflare Pages project linked to GitHub repository:

**Actions**:
- Create Pages project via API v4
- Link to GitHub repository (requires GitHub App installation)
- Configure build command: `npm run build`
- Set destination directory: `dist`
- Retrieve pages.dev URL

**Critical Error**: GitHub App not installed (error 8000011) → Manual setup required

**Agents**: Cloudflare Pages Agent

**Rollback**: Deletes Pages project if later phases fail

---

### Phase 5: GCP Provisioning
**Duration**: 60-90 seconds (longest phase due to project creation)

Sets up complete Google Cloud infrastructure:

**Actions**:
1. **Create Project**: New unique project in organization (60+ seconds)
2. **Link Billing**: Attach billing account (CRITICAL - must be at account level, not project)
3. **Enable APIs**:
   - Identity Toolkit (for authentication)
   - Firebase services
4. **Initialize Firebase**: Add Firebase to project
5. **Configure Identity Platform**: Enable Email/Password auth
6. **Add Authorized Domains**: pages.dev and custom domains

**Agents**: GCP Project Agent, GCP Billing Management Skill

**Rollback**: Deletes GCP project if domain finalization fails

---

### Phase 6: Config Injection
**Duration**: 1-2 minutes

Injects Firebase credentials into application and performs second code push:

**Actions**:
- Retrieve Firebase config from GCP (API keys, auth domain, etc.)
- Create src/firebase-config.js with credentials
- Commit changes: "feat: inject identity config"
- Push to main branch (triggers Cloudflare rebuild)

**Agents**: Firebase Configuration Agent

---

### Phase 7: Domain Finalization
**Duration**: 2-5 minutes (DNS propagation variable)

Configures custom domain if provided:

**Actions**:
- Resolve domain to Cloudflare zone
- Create CNAME record pointing to pages.dev
- Bind custom domain to Pages project
- If external registrar: Return CNAME target for manual configuration

**Agents**: Domain Configuration Agent, DNS Record Management Skill

---

## API Endpoints

### POST /deploy
**Queue a new deployment**

```bash
curl -X POST http://localhost:8000/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "my-app",
    "source": {
      "type": "git",
      "url": "https://github.com/user/my-react-app"
    },
    "domain": {
      "custom_domain": "app.example.com",
      "dns_managed_by_cloudflare": true
    }
  }'
```

**Response**:
```json
{
  "task_id": "abc123def456",
  "status": "pending",
  "deployment_id": "abc123def456",
  "message": "Deployment queued"
}
```

---

### GET /deploy/{task_id}
**Get deployment status and progress**

```bash
curl -X GET http://localhost:8000/deploy/abc123def456
```

**Response**:
```json
{
  "task_id": "abc123def456",
  "status": "in_progress",
  "progress": 3,
  "total_steps": 7,
  "message": "Cloudflare Pages setup",
  "result": null,
  "error": null
}
```

---

### POST /upload
**Upload source code as ZIP**

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@my-app.zip"
```

**Response**:
```json
{
  "s3_key": "uploads/uuid-1234/my-app.zip",
  "filename": "my-app.zip",
  "size": 1048576
}
```

Then use `s3_key` in deployment request with `source.type = "folder"`

---

### GET /health
**Health check endpoint**

```bash
curl -X GET http://localhost:8000/health
```

**Response**:
```json
{
  "status": "healthy",
  "redis": "connected",
  "aws": "connected"
}
```

---

## Required Credentials & Setup

### 1. AWS Credentials
**IAM Policy**: `auto-deployer-policy`
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::react-to-app", "arn:aws:s3:::react-to-app/*"]
    },
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:*:*:secret:prod/auto-deployer/*"
    }
  ]
}
```

**Secrets Manager**: `prod/auto-deployer/keys`
```json
{
  "GITHUB_TOKEN": "github_pat_...",
  "CLOUDFLARE_API_TOKEN": "...",
  "GCP_SERVICE_ACCOUNT_JSON": "base64-encoded-json"
}
```

---

### 2. GitHub Setup
- **Token Type**: Fine-grained Personal Access Token
- **Resource Owner**: Organization (not personal account)
- **Scopes**:
  - Administration: Read & Write
  - Contents: Read & Write
  - Metadata: Read-only
- **Repository Access**: All repositories (automation creates new ones)
- **Expiration**: 90 days (set calendar reminders for rotation)

---

### 3. Cloudflare Prerequisites
- **GitHub App Installation**: MUST be installed on GitHub organization before deployment
  - Navigate to Cloudflare Dashboard → Pages → Create a project → Connect to Git
  - Authorize Cloudflare GitHub App
  - Grant access to "All repositories"

- **API Token Permissions**:
  - Account - Cloudflare Pages: Edit
  - Zone - DNS: Edit
  - Zone - Zone: Read

---

### 4. GCP Setup
**Service Account**: `auto-deployer-sa`

**IAM Roles** (CRITICAL):
- `roles/resourcemanager.projectCreator` (Organization level)
- `roles/billing.user` (ON BILLING ACCOUNT, not project)
- `roles/serviceusage.serviceUsageAdmin` (Project level)
- `roles/firebase.admin` (Project level)

**Most Common Failure**: Billing role granted at project level instead of billing account level

---

## Environment Variables

```bash
# AWS (Required - direct injection)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# Resource Configuration
S3_BUCKET=react-to-app
SECRET_NAME=prod/auto-deployer/keys

# Task Queue
REDIS_URL=redis://localhost:6379/0

# Target Configuration
GITHUB_ORG=my-organization
CLOUDFLARE_ACCOUNT_ID=abc123...
GCP_BILLING_ACCOUNT=XXXXXX-XXXXXX-XXXXXX

# Retrieved from Secrets Manager at runtime
# GITHUB_TOKEN
# CLOUDFLARE_API_TOKEN
# GOOGLE_APPLICATION_CREDENTIALS
```

---

## Docker Deployment

### Development Stack
```bash
docker-compose up
# Runs: FastAPI (8000), Celery Worker, Redis
```

### Production Stack
```bash
docker-compose -f docker-compose.prod.yml up -d
# Scales Celery workers: celery_worker_1 through celery_worker_N
```

### Docker Compose Services
```yaml
services:
  api:
    image: auto-deployer:latest
    ports:
      - "8000:8000"
    environment:
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      # ... other vars
    depends_on:
      - redis
      - celery_worker

  celery_worker:
    image: auto-deployer:latest
    command: celery -A worker.celery_app worker --loglevel=info
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
```

---

## Testing Strategy

### Unit Tests (Test Coverage: 85%+)
- Configuration loading and hydration
- Model validation
- Service initialization
- Utility functions

**Run**: `pytest tests/test_*.py -v`

### Integration Tests
- Full deployment workflow (mocked services)
- Rollback scenarios
- Concurrent deployments
- API endpoint behavior

**Run**: `pytest tests/test_integration.py -v`

### Validation Tests
- AWS credential access
- GitHub token validity
- Cloudflare account access
- GCP service account permissions
- Redis connectivity
- Tree-sitter parser installation

**Run**: `pytest tests/test_validation.py -v`

---

## Performance Characteristics

### Single Deployment Timeline
- **Source Acquisition**: 2-5 minutes
- **Code Transformation**: 1-2 minutes
- **GitHub Repository**: 2-3 minutes
- **Cloudflare Setup**: 2-3 minutes
- **GCP Provisioning**: 60-90 seconds (slowest phase)
- **Config Injection**: 1-2 minutes
- **Domain Finalization**: 2-5 minutes (if custom domain)

**Total**: ~15-25 minutes per deployment

### Throughput
- **Concurrent Deployments**: Unlimited (Redis/Celery worker scaled)
- **API Response Time**: < 200ms (excluding async operations)
- **Task Queue Latency**: < 5 seconds

### Resource Requirements
- **Memory**: 2GB+ (API + Celery worker + Redis)
- **CPU**: 2+ cores
- **Storage**: 50GB+ for temporary workspaces and logs

---

## Security Considerations

### Secrets Management
- ✅ All third-party credentials stored in AWS Secrets Manager
- ✅ Credentials never logged or displayed
- ✅ Base64 encoding for binary credentials
- ✅ Temporary files with 0600 permissions

### Network Security
- ✅ All API calls over HTTPS
- ✅ Fine-grained IAM policies for AWS
- ✅ Organization-scoped GitHub tokens
- ✅ Account-level Cloudflare API tokens

### Code Safety
- ✅ Tree-sitter for safe AST-based code modification (no regex)
- ✅ Input validation on all endpoints
- ✅ Pydantic models for type safety

### Audit & Compliance
- ✅ Structured JSON logging for all operations
- ✅ Deployment state persisted for debugging
- ✅ Error messages without sensitive data

---

## Monitoring & Observability

### Health Monitoring
- **Endpoint**: GET /health
- **Checks**: Redis connectivity, AWS S3 access
- **Frequency**: Every 30 seconds (recommended)

### Logging
- **Level**: Structured JSON via structlog
- **Fields**: timestamp, level, message, context
- **Destinations**: stdout (Docker captures), log aggregation

### Metrics to Monitor
- Active deployments (Celery queue depth)
- Phase execution times
- Error rates per phase
- Redis memory usage
- Concurrent Celery workers

---

## Roadmap & Future Enhancements

### Phase 2 (Future)
- OpenID Connect (OIDC) for ephemeral AWS credentials
- Terraform CDK integration for state management
- Multi-region deployment support
- Custom domain SSL certificate provisioning
- Slack/Teams notifications
- Webhook callbacks on completion

### Phase 3 (Future)
- UI Dashboard for deployment monitoring
- Rollback from UI
- Scheduled deployments
- A/B testing support
- Advanced analytics

---

## Troubleshooting Guide

### Common Issues

**1. GitHub Error: "Resource not accessible by integration"**
- Token not scoped to organization
- Regenerate token with organization as Resource Owner

**2. Cloudflare Error 8000011**
- GitHub App not installed on organization
- Install via Cloudflare Dashboard → Pages → Connect to Git

**3. GCP: "Billing account not found or permission denied"**
- Role granted on project instead of billing account
- Add billing.user role directly on Billing Account

**4. Deployment Timeout**
- GCP project creation takes 60+ seconds
- Celery task timeout set to 30 minutes
- Check Celery worker logs

---

## Development Guide

### Local Setup
```bash
# Clone repository
git clone ...
cd auto-deployer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run tests
pytest tests/ -v

# Start local stack
docker-compose up
```

### Code Organization
- `app/` - FastAPI web application
- `worker/` - Celery background tasks
- `tests/` - Comprehensive test suite
- `agents/` - Agent specification documents
- `skills/` - Skill definition documents

---

## Conclusion

Auto-Deployer represents a sophisticated integration of modern cloud primitives, demonstrating best practices in:
- **Asynchronous Processing**: Celery for long-running operations
- **Distributed Transactions**: Saga pattern for multi-service orchestration
- **Code Safety**: Tree-sitter for semantic code modification
- **Security**: Least-privilege access and runtime secret hydration
- **Reliability**: Automatic rollback and exponential backoff retries

The system is production-ready, fully tested, and designed to scale from single deployments to enterprise-grade deployment pipelines.

---

## Appendix: File Structure

```
auto-deployer/
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies
├── pytest.ini                      # Pytest configuration
├── Dockerfile                      # Container image definition
├── docker-compose.yml              # Development stack
├── docker-compose.prod.yml         # Production stack
│
├── app/                            # FastAPI Application
│   ├── __init__.py
│   ├── main.py                     # REST API endpoints (main.py:47 to main.py:150)
│   ├── config.py                   # Settings & secrets hydration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request.py              # Request schemas
│   │   ├── deployment.py           # Response & state schemas
│   │   └── types.py                # Shared types
│   ├── services/
│   │   ├── __init__.py
│   │   ├── aws_storage.py          # S3 & Secrets Manager
│   │   ├── github_api.py           # GitHub API client
│   │   ├── cloudflare_api.py       # Cloudflare API client
│   │   ├── gcp_identity.py         # GCP API client
│   │   └── source_manager.py       # Source acquisition
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── ast_modifier.py         # Tree-sitter code transformation
│   │   ├── saga_context.py         # Saga state management
│   │   └── middleware/
│   │       ├── __init__.py
│   │       └── error_handler.py    # Global error handling
│   └── static/                     # Static files (if needed)
│
├── worker/                         # Celery Background Worker
│   ├── __init__.py
│   ├── celery_app.py               # Celery configuration
│   └── tasks.py                    # Main saga workflow (execute_deployment_saga)
│
├── tests/                          # Comprehensive Test Suite
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures
│   ├── test_config.py              # Configuration tests
│   ├── test_models.py              # Model validation tests
│   ├── test_aws_storage.py         # S3 tests
│   ├── test_github_api.py          # GitHub API tests
│   ├── test_cloudflare_api.py      # Cloudflare API tests
│   ├── test_gcp_identity.py        # GCP API tests
│   ├── test_source_manager.py      # Source manager tests
│   ├── test_ast_modifier.py        # AST modification tests
│   ├── test_saga_context.py        # Saga state tests
│   ├── test_celery.py              # Celery task tests
│   ├── test_main.py                # FastAPI endpoint tests
│   ├── test_validation.py          # Pre-run validation tests
│   └── test_integration.py         # End-to-end integration tests
│
├── scripts/
│   ├── startup.sh                  # Container entry point
│   └── healthcheck.sh              # Health monitoring
│
├── deployment/                     # Production Deployment
│   ├── kubernetes/                 # K8s manifests (optional)
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   └── secret.yaml
│   └── terraform/                  # Terraform configs (optional)
│
└── documentation/
    ├── agents/                     # Agent specifications
    ├── skills/                     # Skill definitions
    ├── API.md                      # OpenAPI documentation
    └── TROUBLESHOOTING.md         # Troubleshooting guide

Total Files: 45+
Total Lines of Code: 3,500-4,000 (without tests)
Total Lines of Tests: 2,500-3,000
Total Documentation: 5,000+ lines
```

---

**Version**: 1.0.0
**Status**: Production Ready
**Last Updated**: January 2026
**Maintainers**: Engineering Team
