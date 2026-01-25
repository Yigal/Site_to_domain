# Agent Specifications

This directory contains the specifications for all 10 core agents used in the Auto-Deployer system.

## Agents Overview

### 1. Source Acquisition Agent
**File:** `source_acquisition_agent.md`

Acquires code from Git repositories or ZIP uploads.

### 2. Code Transformation Agent
**File:** `code_transformation_agent.md`

Performs semantic code transformation using Tree-sitter AST parsing.

### 3. GitHub Repository Agent
**File:** `github_repository_agent.md`

Manages GitHub repository creation and code pushing.

### 4. Cloudflare Pages Agent
**File:** `cloudflare_pages_agent.md`

Configures and deploys to Cloudflare Pages.

### 5. GCP Project Agent
**File:** `gcp_project_agent.md`

Creates GCP projects and configures Firebase.

### 6. AWS Storage Agent
**File:** `aws_storage_agent.md`

Manages AWS S3 and Secrets Manager operations.

### 7. Domain Configuration Agent
**File:** `domain_configuration_agent.md`

Manages custom domain and DNS configuration.

### 8. Saga Orchestration Agent
**File:** `saga_orchestration_agent.md`

Coordinates all agents and manages distributed transactions.

### 9. Firebase Configuration Agent
**File:** `firebase_configuration_agent.md`

Configures Firebase and Identity Platform.

### 10. Validation Agent
**File:** `validation_agent.md`

Performs pre-flight validation of credentials and configuration.

---

## Agent Relationship Diagram

```
Validation Agent (Pre-checks)
        ↓
Saga Orchestration Agent (Main Coordinator)
        ├─ Source Acquisition Agent
        │  └─ AWS Storage Agent
        ├─ Code Transformation Agent
        ├─ GitHub Repository Agent
        ├─ Cloudflare Pages Agent
        ├─ GCP Project Agent
        │  └─ Firebase Configuration Agent
        └─ Domain Configuration Agent
```

---

## Common Patterns

### Each Agent Specification Includes:

- **Purpose:** What the agent does
- **Key Responsibilities:** Main functions
- **Key Functions:** Available operations
- **Integration Points:** Input/output
- **Error Handling:** Failure recovery
- **Skills Required:** Dependencies
- **Success Criteria:** Validation

---

## How Agents Work

1. **Saga Orchestration Agent** creates a deployment saga
2. **Validation Agent** pre-validates all credentials
3. **Source Acquisition Agent** gets the code
4. **Code Transformation Agent** modifies the code
5. **GitHub Repository Agent** creates and pushes to GitHub
6. **Cloudflare Pages Agent** deploys to Cloudflare
7. **GCP Project Agent** creates GCP project and Firebase
8. **AWS Storage Agent** manages credentials and storage
9. **Firebase Configuration Agent** configures Firebase
10. **Domain Configuration Agent** sets up DNS and custom domain

Each agent can execute compensating transactions if an error occurs, ensuring rollback capability.

---

## Agent Communication

Agents communicate through:
- **Redis queue** for async messaging
- **Saga context** for state management
- **Shared services** for API access

---

## Error Handling & Compensation

Each agent that modifies external resources registers a compensating transaction:

Example:
- **Action:** Create GitHub repository
- **Compensation:** Delete GitHub repository

This ensures automatic rollback if deployment fails.

---

## See Also

- [Skills Documentation](../skills/README.md) - Reusable skill definitions
- [API Documentation](../API.md) - REST API endpoints
- [Execution Plan](../../execution_plan_and_review/plans/) - Step-by-step execution

---

**Version:** 1.0.0
**Last Updated:** January 25, 2026
**Status:** Active

