# Skill Specifications

This directory contains the specifications for all 14 reusable skills used by agents in the Auto-Deployer system.

## Skills Overview

### Cloud Integration Skills (8 skills)

1. **Git Operations Skill**
   - Clone repositories
   - Commit and push code
   - Branch management
   - File: `git_operations_skill.md`

2. **GitHub API Integration Skill**
   - Create repositories
   - Manage organization access
   - Webhook configuration
   - File: `github_api_integration_skill.md`

3. **Cloudflare API Integration Skill**
   - Create Pages projects
   - Configure deployments
   - Manage DNS records
   - File: `cloudflare_api_integration_skill.md`

4. **GCP API Integration Skill**
   - Create projects
   - Manage resources
   - Configure services
   - File: `gcp_api_integration_skill.md`

5. **GCP Billing Management Skill**
   - Link billing accounts
   - Manage quotas
   - Monitor costs
   - File: `gcp_billing_management_skill.md`

6. **S3 File Operations Skill**
   - Upload/download files
   - Manage buckets
   - Configure permissions
   - File: `s3_file_operations_skill.md`

7. **AWS Secrets Management Skill**
   - Store credentials
   - Retrieve secrets
   - Manage permissions
   - File: `aws_secrets_management_skill.md`

8. **DNS Record Management Skill**
   - Create DNS records
   - Update DNS configuration
   - Verify domain ownership
   - File: `dns_record_management_skill.md`

### Code & Data Skills (4 skills)

9. **AST Modification Skill**
   - Parse JavaScript code
   - Modify AST safely
   - Generate transformed code
   - File: `ast_modification_skill.md`

10. **ZIP Archive Handling Skill**
    - Extract ZIP files
    - Create archives
    - Validate contents
    - File: `zip_archive_handling_skill.md`

11. **Environment Configuration Skill**
    - Create .env files
    - Load variables
    - Manage configurations
    - File: `environment_configuration_skill.md`

12. **Credential Encoding Skill**
    - Encode credentials
    - Decode secrets
    - Hash passwords
    - File: `credential_encoding_skill.md`

### Infrastructure Skills (2 skills)

13. **Workspace Management Skill**
    - Create temporary directories
    - Manage file storage
    - Clean up resources
    - File: `workspace_management_skill.md`

14. **Celery Task Management Skill**
    - Manage task queues
    - Execute async tasks
    - Monitor task status
    - File: `celery_task_management_skill.md`

---

## Skill Categories

```
Cloud Integration (8)
├─ Git Operations
├─ GitHub API
├─ Cloudflare API
├─ GCP API
├─ GCP Billing
├─ S3 Operations
├─ AWS Secrets
└─ DNS Management

Code & Data (4)
├─ AST Modification
├─ ZIP Handling
├─ Environment Config
└─ Credential Encoding

Infrastructure (2)
├─ Workspace Management
└─ Celery Task Management
```

---

## Agent-to-Skill Mapping

### Source Acquisition Agent
- Git Operations Skill
- S3 File Operations Skill
- ZIP Archive Handling Skill

### Code Transformation Agent
- AST Modification Skill
- Environment Configuration Skill
- Credential Encoding Skill

### GitHub Repository Agent
- GitHub API Integration Skill
- Git Operations Skill

### Cloudflare Pages Agent
- Cloudflare API Integration Skill

### GCP Project Agent
- GCP API Integration Skill
- GCP Billing Management Skill

### AWS Storage Agent
- S3 File Operations Skill
- AWS Secrets Management Skill
- Credential Encoding Skill

### Domain Configuration Agent
- DNS Record Management Skill
- Cloudflare API Integration Skill

### Firebase Configuration Agent
- GCP API Integration Skill

### Saga Orchestration Agent
- Celery Task Management Skill

### Validation Agent
- AWS Secrets Management Skill
- GitHub API Integration Skill
- Cloudflare API Integration Skill
- GCP API Integration Skill

---

## Skill Characteristics

### Each Skill Specification Includes:

- **Purpose:** What the skill does
- **Key Operations:** Available functions
- **Error Handling:** Failure recovery
- **Integration Points:** Dependencies
- **Configuration Required:** Credentials needed
- **Success Criteria:** Validation tests

### Design Principles:

1. **Single Responsibility:** Each skill does one thing well
2. **Reusability:** Skills are used by multiple agents
3. **Error Handling:** Each skill handles its own errors gracefully
4. **Configuration:** Credentials externalized via environment
5. **Testing:** Each skill has unit tests

---

## Skill Dependencies

```
Celery Task Management ← all skills
    ↓
Workspace Management
    ├─ Git Operations
    ├─ ZIP Handling
    ├─ AST Modification
    └─ Environment Configuration

AWS Secrets ← credential-based skills
├─ S3 Operations
├─ Credential Encoding
├─ Git Operations
└─ GitHub API

GCP APIs
├─ GCP Billing
├─ Cloudflare API
└─ DNS Management
```

---

## How Skills Work

1. Skills are called by agents
2. Each skill has error handling
3. Skills communicate with external APIs
4. Results are returned to agent
5. Agent uses result in next step
6. Compensations use same skills for cleanup

---

## Common Patterns

### API Calls
```python
def operation(params):
    try:
        result = call_api(params)
        log_success(result)
        return result
    except Exception as e:
        log_error(e)
        return None
```

### Error Handling
```python
try:
    # operation
    return success_result
except SpecificError as e:
    # handle specific error
    return fallback_result
except Exception as e:
    # log unexpected error
    raise
```

### Compensation
```python
def compensate(resource_id):
    # Undo the operation
    # Delete created resource
    # Restore previous state
```

---

## See Also

- [Agent Documentation](../agents/README.md) - Agent definitions
- [API Documentation](../API.md) - REST API endpoints
- [Execution Plan](../../execution_plan_and_review/plans/) - Step-by-step execution

---

**Version:** 1.0.0
**Last Updated:** January 25, 2026
**Status:** Active

