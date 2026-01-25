# Auto-Deployer: Implementation Plan

## Overview

This plan outlines the systematic approach to building the Auto-Deployer system. The implementation follows a bottom-up strategy: foundational infrastructure first, then core services, followed by the orchestration layer, and finally integration testing.

---

## Phase 1: Project Scaffolding & Infrastructure

### 1.1 Initialize Project Structure
- [ ] Create root project directory `/auto-deployer`
- [ ] Set up Python virtual environment (Python 3.10+)
- [ ] Create directory structure as defined in design document
- [ ] Initialize `requirements.txt` with all dependencies
- [ ] Create `.env.example` template
- [ ] Set up `.gitignore` for Python projects

### 1.2 Docker Configuration
- [ ] Create `Dockerfile` for the FastAPI application
- [ ] Create `docker-compose.yml` with:
  - FastAPI service
  - Celery worker service
  - Redis service
  - Shared volume for temporary workspaces
- [ ] Create `scripts/startup.sh` for container initialization

### 1.3 Configure Development Tools
- [ ] Set up `pytest` configuration (`pytest.ini` or `pyproject.toml`)
- [ ] Configure `structlog` for structured JSON logging
- [ ] Add `pre-commit` hooks for code quality (optional)

---

## Phase 2: Core Configuration Layer

### 2.1 Settings Management (`app/config.py`)
- [ ] Implement `Settings` class using `pydantic-settings`
- [ ] Define all configuration fields with types and defaults
- [ ] Add validation for required fields

### 2.2 Secret Hydration (`app/config.py`)
- [ ] Implement `hydrate_secrets()` function
- [ ] Add boto3 Secrets Manager client initialization
- [ ] Implement `_fetch_secret()` for retrieving secrets
- [ ] Implement `_decode_gcp_credentials()` for Base64 decoding
- [ ] Write GCP credentials to temp file with secure permissions
- [ ] Set environment variables from retrieved secrets

### 2.3 Validation Tests
- [ ] Write unit tests for settings loading
- [ ] Write unit tests for secret hydration (mocked with moto)

---

## Phase 3: Pydantic Models

### 3.1 Request Models (`app/models/request.py`)
- [ ] Define `SourceType` enum (folder, git)
- [ ] Define `SourceConfig` model
- [ ] Define `DomainConfig` model
- [ ] Define `DeploymentRequest` model with validators

### 3.2 Deployment Models (`app/models/deployment.py`)
- [ ] Define `DeploymentStatus` enum
- [ ] Define `SagaStep` model
- [ ] Define `DeploymentState` model
- [ ] Define `DeploymentResponse` model

### 3.3 Validation Tests
- [ ] Test valid request payloads
- [ ] Test invalid request rejections
- [ ] Test enum serialization

---

## Phase 4: Service Layer - AWS

### 4.1 S3 Storage Service (`app/services/aws_storage.py`)
- [ ] Implement `_get_s3_client()` singleton/factory
- [ ] Implement `download_file()` with error handling
- [ ] Implement `upload_file()` with multipart support
- [ ] Implement `download_and_extract_zip()` using zipfile module
- [ ] Implement `list_objects()` for bucket listing

### 4.2 Validation Tests
- [ ] Mock S3 with moto
- [ ] Test file upload/download cycle
- [ ] Test zip extraction
- [ ] Test error handling for missing objects

---

## Phase 5: Service Layer - GitHub

### 5.1 GitHub API Service (`app/services/github_api.py`)
- [ ] Implement `_get_github_client()` using PyGithub
- [ ] Implement `check_repo_exists()` 
- [ ] Implement `create_repository()` with org support
- [ ] Implement `_run_git_command()` subprocess wrapper
- [ ] Implement `push_code()`:
  - Initialize git repo in workspace
  - Configure git user (automation)
  - Add remote origin
  - Add all files
  - Commit with message
  - Push to main branch
- [ ] Implement `delete_repository()` for rollback

### 5.2 Validation Tests
- [ ] Mock GitHub API responses
- [ ] Test repository creation flow
- [ ] Test push operation (mock subprocess)
- [ ] Test error handling for API failures

---

## Phase 6: Service Layer - Cloudflare

### 6.1 Cloudflare API Service (`app/services/cloudflare_api.py`)
- [ ] Implement `_get_headers()` for auth
- [ ] Implement `_handle_error()` for API error parsing
- [ ] Implement `get_zone_id()` to resolve domain to zone
- [ ] Implement `create_pages_project()`:
  - Build payload with source config
  - Handle error code 8000011 (GitHub App not installed)
  - Return project details
- [ ] Implement `get_deployment_url()` to get pages.dev URL
- [ ] Implement `create_dns_record()` for CNAME creation
- [ ] Implement `add_custom_domain()` for domain binding
- [ ] Implement `delete_pages_project()` for rollback
- [ ] Implement `delete_dns_record()` for rollback

### 6.2 Validation Tests
- [ ] Mock Cloudflare API with responses library
- [ ] Test Pages project creation
- [ ] Test DNS record creation
- [ ] Test error handling for missing GitHub App
- [ ] Test zone ID resolution

---

## Phase 7: Service Layer - GCP

### 7.1 GCP Identity Service (`app/services/gcp_identity.py`)
- [ ] Implement `_get_credentials()` for loading JSON credentials
- [ ] Implement `_wait_for_operation()` with polling logic
- [ ] Implement `create_project()`:
  - Use resourcemanager_v3 client
  - Generate unique project ID
  - Wait for operation completion
- [ ] Implement `link_billing()`:
  - Use billing_v1 client
  - Handle billing.user permission errors
- [ ] Implement `enable_apis()`:
  - Enable identitytoolkit.googleapis.com
  - Enable firebase.googleapis.com
- [ ] Implement `add_firebase()`:
  - Use Firebase Management API
  - Wait for operation
- [ ] Implement `configure_identity_platform()`:
  - Enable Email/Password provider
  - Configure settings
- [ ] Implement `add_authorized_domain()`:
  - Add pages.dev domain to allowed list
- [ ] Implement `get_firebase_config()`:
  - Retrieve apiKey, authDomain, projectId, etc.
- [ ] Implement `delete_project()` for rollback

### 7.2 Validation Tests
- [ ] Mock GCP clients
- [ ] Test project creation flow
- [ ] Test billing linkage
- [ ] Test API enablement
- [ ] Test Firebase config retrieval
- [ ] Test error handling for permission issues

---

## Phase 8: Source Manager Service

### 8.1 Source Manager (`app/services/source_manager.py`)
- [ ] Implement `prepare_workspace()`:
  - Generate unique workspace ID
  - Create temp directory
  - Route to clone or extract based on source type
- [ ] Implement `_clone_repository()`:
  - Git clone to workspace
  - Remove .git directory (detach history)
- [ ] Implement `_extract_uploaded_zip()`:
  - Download from S3
  - Extract using zipfile
- [ ] Implement `detect_framework()`:
  - Parse package.json
  - Identify vite, create-react-app, next.js
- [ ] Implement `cleanup_workspace()`:
  - Remove temp directory
  - Handle errors gracefully

### 8.2 Validation Tests
- [ ] Test workspace creation
- [ ] Test git clone (mock subprocess)
- [ ] Test zip extraction
- [ ] Test framework detection for various package.json

---

## Phase 9: AST Modifier Utility

### 9.1 Tree-sitter Implementation (`app/utils/ast_modifier.py`)
- [ ] Implement `_parse_javascript()`:
  - Initialize Tree-sitter parser
  - Load JavaScript language
  - Parse source to AST
- [ ] Implement `_find_config_object()`:
  - Query for defineConfig call
  - Handle different config patterns
- [ ] Implement `_insert_property()`:
  - Calculate byte positions
  - Insert property string
- [ ] Implement `_write_modified_source()`:
  - Write bytes back to file
- [ ] Implement `set_vite_base_path()`:
  - Find vite.config.js
  - Insert or update base property
- [ ] Implement `inject_firebase_config()`:
  - Create/update firebase-config.js
  - Insert configuration object
- [ ] Implement `update_env_file()`:
  - Parse existing .env
  - Add/update variables

### 9.2 Validation Tests
- [ ] Test vite.config.js modification
- [ ] Test with various config styles
- [ ] Test firebase config injection
- [ ] Test .env file updates
- [ ] Test error handling for malformed files

---

## Phase 10: Saga Context Utility

### 10.1 Saga State Management (`app/utils/saga_context.py`)
- [ ] Implement `SagaContext` class:
  - Initialize with deployment ID
  - Store steps list
  - Track current status
- [ ] Implement `begin()`:
  - Create initial state
  - Persist to Redis
- [ ] Implement `record_step()`:
  - Add step with rollback function reference
  - Persist updated state
- [ ] Implement `mark_completed()`:
  - Update status
  - Clear rollback functions (no longer needed)
- [ ] Implement `mark_failed()`:
  - Update status
  - Trigger rollback
- [ ] Implement `execute_rollback()`:
  - Iterate steps in reverse
  - Execute compensation actions
  - Handle rollback failures
- [ ] Implement `_persist_state()` to Redis
- [ ] Implement `_load_state()` from Redis

### 10.2 Validation Tests
- [ ] Test saga initialization
- [ ] Test step recording
- [ ] Test successful completion
- [ ] Test failure and rollback execution
- [ ] Test partial rollback on compensation failure

---

## Phase 11: Celery Worker

### 11.1 Celery Configuration (`worker/celery_app.py`)
- [ ] Implement `create_celery_app()`:
  - Configure broker URL (Redis)
  - Configure result backend
  - Set task serializer to JSON
  - Enable late acknowledgment
  - Configure retry policy

### 11.2 Main Saga Task (`worker/tasks.py`)
- [ ] Implement `execute_deployment_saga()` Celery task:
  - Accept deployment request
  - Initialize saga context
  - Execute phases in sequence
  - Handle exceptions and rollback
  - Return final status
- [ ] Implement `_phase_source_acquisition()`:
  - Call SourceManager.prepare_workspace()
  - Record saga step
- [ ] Implement `_phase_code_transformation()`:
  - Detect framework
  - Modify vite.config.js
  - Record saga step
- [ ] Implement `_phase_github_creation()`:
  - Create repository
  - Push initial code
  - Record saga step with delete_repository rollback
- [ ] Implement `_phase_cloudflare_setup()`:
  - Create Pages project
  - Handle 8000011 error
  - Record saga step with delete_pages_project rollback
- [ ] Implement `_phase_gcp_provisioning()`:
  - Create project
  - Link billing
  - Enable APIs
  - Add Firebase
  - Configure Identity Platform
  - Record saga step with delete_project rollback
- [ ] Implement `_phase_config_injection()`:
  - Get Firebase config
  - Inject into source
  - Second git push
  - Add authorized domain
- [ ] Implement `_phase_domain_finalization()`:
  - Create DNS record (if managed)
  - Bind custom domain
  - Return external CNAME target if needed
- [ ] Implement `_notify_status()`:
  - Send webhook callback if configured

### 11.3 Integration Tests
- [ ] Test full saga execution (mocked services)
- [ ] Test saga rollback on phase failure
- [ ] Test Celery task retry behavior

---

## Phase 12: FastAPI Application

### 12.1 Main Application (`app/main.py`)
- [ ] Implement `lifespan()` context manager:
  - Call `hydrate_secrets()` on startup
  - Cleanup on shutdown
- [ ] Create FastAPI app with lifespan
- [ ] Implement `_validate_request()`:
  - Validate Pydantic model
  - Check source availability
- [ ] Implement `POST /deploy` endpoint:
  - Validate request
  - Generate deployment ID
  - Queue Celery task
  - Return task ID immediately
- [ ] Implement `GET /deploy/{task_id}` endpoint:
  - Query Celery task status
  - Return deployment state
- [ ] Implement `POST /upload` endpoint:
  - Accept multipart file upload
  - Upload to S3
  - Return S3 key
- [ ] Implement `GET /health` endpoint:
  - Check Redis connectivity
  - Check AWS connectivity
  - Return health status

### 12.2 API Tests
- [ ] Test deploy endpoint
- [ ] Test status endpoint
- [ ] Test upload endpoint
- [ ] Test health check
- [ ] Test error responses

---

## Phase 13: Pre-Run Validation Suite

### 13.1 Validation Test Implementation (`tests/test_validation.py`)
- [ ] Implement `TestAWSConnectivity`:
  - test_aws_credentials_present
  - test_s3_bucket_accessible
  - test_secrets_manager_accessible
- [ ] Implement `TestGitHubConnectivity`:
  - test_github_token_valid
  - test_github_org_accessible
  - test_github_repo_creation_permission
- [ ] Implement `TestCloudflareConnectivity`:
  - test_cloudflare_token_valid
  - test_cloudflare_pages_permission
- [ ] Implement `TestGCPConnectivity`:
  - test_gcp_credentials_valid
  - test_gcp_project_creation_permission
  - test_gcp_billing_access
- [ ] Implement `TestRedisConnectivity`:
  - test_redis_connection
- [ ] Implement `TestTreeSitterSetup`:
  - test_tree_sitter_javascript
- [ ] Implement `run_all_validations()` entry point

---

## Phase 14: Integration Testing

### 14.1 End-to-End Tests
- [ ] Test full deployment from git source (staging environment)
- [ ] Test full deployment from folder upload (staging environment)
- [ ] Test rollback scenario
- [ ] Test concurrent deployments
- [ ] Test rate limit handling

### 14.2 Load Testing
- [ ] Set up load testing with locust or similar
- [ ] Test API under concurrent requests
- [ ] Identify bottlenecks

---

## Phase 15: Documentation & Deployment

### 15.1 Documentation
- [ ] Write API documentation (auto-generated from FastAPI)
- [ ] Document deployment procedures
- [ ] Create troubleshooting guide

### 15.2 Production Deployment
- [ ] Deploy to target environment (EC2, ECS, or Kubernetes)
- [ ] Configure production Redis
- [ ] Set up monitoring and alerting
- [ ] Configure log aggregation
- [ ] Run pre-run validation in production environment

---

## Dependency Graph

```
Phase 1 (Scaffolding)
    │
    ├── Phase 2 (Config) ──────────────────────────────────┐
    │                                                       │
    ├── Phase 3 (Models) ──────────────────────────────────┤
    │                                                       │
    ├── Phase 4 (AWS Service) ─────────────────────────────┤
    │       │                                               │
    │       └── Phase 8 (Source Manager) ──────────────────┤
    │                                                       │
    ├── Phase 5 (GitHub Service) ──────────────────────────┤
    │                                                       │
    ├── Phase 6 (Cloudflare Service) ──────────────────────┤
    │                                                       │
    ├── Phase 7 (GCP Service) ─────────────────────────────┤
    │                                                       │
    ├── Phase 9 (AST Modifier) ────────────────────────────┤
    │                                                       │
    └── Phase 10 (Saga Context) ───────────────────────────┤
                                                            │
                                                            ▼
                                                    Phase 11 (Celery Worker)
                                                            │
                                                            ▼
                                                    Phase 12 (FastAPI)
                                                            │
                                                            ▼
                                                    Phase 13 (Validation Suite)
                                                            │
                                                            ▼
                                                    Phase 14 (Integration Testing)
                                                            │
                                                            ▼
                                                    Phase 15 (Deployment)
```

---

## Risk Mitigation

| Risk | Mitigation Strategy |
|------|---------------------|
| GCP project creation takes 60+ seconds | Use Celery for async processing; implement proper timeout handling |
| Cloudflare GitHub App not installed | Clear error message; add to pre-run validation hints |
| Billing permission denied | Detailed credential guide; test in pre-run validation |
| Rate limiting on APIs | Implement exponential backoff; use Celery retry mechanisms |
| Partial deployment failure | Saga pattern with compensation; thorough rollback testing |
| Secret rotation | Design for runtime secret fetching; no caching of credentials |

---

## Success Criteria

1. Pre-run validation passes all checks
2. Deployment from git source completes in < 5 minutes
3. Deployment from folder upload completes in < 5 minutes
4. Rollback executes successfully on any phase failure
5. System handles 10 concurrent deployments
6. All API endpoints respond within 200ms (excluding async operations)
7. Zero secrets exposed in logs or error messages
