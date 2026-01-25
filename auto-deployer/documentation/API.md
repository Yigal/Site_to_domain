# Auto-Deployer API Documentation

## Overview

The Auto-Deployer API provides REST endpoints for orchestrating automated frontend deployment across AWS, GitHub, Cloudflare, and Google Cloud Platform.

**Base URL:** `http://localhost:8000`
**API Version:** 1.0.0

---

## Authentication

Currently, no authentication is required. In production, API key or JWT authentication should be implemented.

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "auto-deployer-api",
  "version": "1.0.0"
}
```

**Status Code:** `200 OK`

---

### 2. Root Endpoint

**Endpoint:** `GET /`

**Description:** Get API information and available endpoints.

**Response:**
```json
{
  "message": "Auto-Deployer API",
  "documentation": "/docs",
  "endpoints": {
    "health": "/health",
    "deploy": "/deploy",
    "status": "/deploy/{task_id}",
    "upload": "/upload"
  }
}
```

**Status Code:** `200 OK`

---

### 3. Start Deployment

**Endpoint:** `POST /deploy`

**Description:** Start a new frontend deployment.

**Request Body:**
```json
{
  "repo_url": "https://github.com/username/repo",
  "domain": "myapp.com",
  "framework": "react",
  "custom_domain": null
}
```

**Parameters:**
- `repo_url` (string, optional): Git repository URL
- `zip_file_url` (string, optional): URL to ZIP file upload
- `domain` (string, required): Application domain
- `framework` (string, optional): Frontend framework (react, vue, nextjs, etc.)
- `custom_domain` (string, optional): Custom domain for binding

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "domain": "myapp.com",
  "framework": "react",
  "created_at": "2026-01-25T20:48:00",
  "estimated_duration": 270
}
```

**Status Code:** `200 OK`

**Error Responses:**
- `400 Bad Request`: Missing required fields
- `422 Unprocessable Entity`: Invalid data format
- `500 Internal Server Error`: Server error

---

### 4. Check Deployment Status

**Endpoint:** `GET /deploy/{task_id}`

**Description:** Get the current status and progress of a deployment.

**Path Parameters:**
- `task_id` (string, required): Unique deployment task ID

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "deploying",
  "progress": 60,
  "message": "Step 9/15 completed",
  "created_at": "2026-01-25T20:48:00",
  "updated_at": "2026-01-25T20:48:30",
  "completed_at": null
}
```

**Status Codes:**
- `pending`: Waiting to start
- `initializing`: Setting up
- `cloning`: Cloning repository
- `transforming`: Transforming code
- `pushing`: Pushing to GitHub
- `configuring`: Configuring services
- `deploying`: Deploying application
- `completed`: Successfully completed
- `failed`: Deployment failed
- `rolled_back`: Rolled back after failure

**Response Code:** `200 OK`

**Error Responses:**
- `404 Not Found`: Task ID not found
- `500 Internal Server Error`: Server error

---

### 5. Upload Source Code

**Endpoint:** `POST /upload`

**Description:** Upload source code as ZIP file.

**Request:**
- `Content-Type`: `multipart/form-data`
- `file`: ZIP file (binary)

**Response:**
```json
{
  "upload_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "myapp.zip",
  "size": 1048576,
  "url": "s3://auto-deployer-uploads/550e8400-e29b-41d4-a716-446655440000/myapp.zip"
}
```

**Status Code:** `200 OK`

**Error Responses:**
- `400 Bad Request`: Invalid file type
- `413 Payload Too Large`: File too large
- `500 Internal Server Error`: Upload failed

---

## Deployment Workflow

### Step-by-Step Process

1. **Step 1:** Project Initialization
   - Validates directory structure
   - Initializes logging

2. **Step 2:** Configuration Layer
   - Sets up environment variables
   - Loads cloud credentials

3. **Step 3:** AWS Storage Configuration
   - Creates S3 bucket
   - Configures Secrets Manager

4. **Step 4:** GitHub Integration
   - Creates repository
   - Sets up webhooks

5. **Step 5:** Cloudflare Pages Setup
   - Creates Pages project
   - Links GitHub

6. **Step 6:** GCP & Firebase Setup
   - Creates GCP project
   - Configures Firebase

7. **Step 7:** AST Transformation
   - Injects Firebase config
   - Sets Cloudflare base path

8. **Step 8:** Source Manager
   - Detects framework
   - Validates source

9. **Step 9:** Saga Context
   - Sets up transaction context
   - Registers compensations

10. **Step 10:** Error Middleware
    - Configures error handling

11. **Step 11:** Celery Worker
    - Starts task queue

12. **Step 12:** FastAPI API
    - Initializes API endpoints

13. **Step 13:** Pydantic Models
    - Creates data models

14. **Step 14:** Test Suite
    - Runs tests

15. **Step 15:** Containerization
    - Creates Docker image
    - Finalizes deployment

---

## Error Handling

### Error Response Format

All error responses follow this format:

```json
{
  "error": "Error Type",
  "detail": "Detailed error message",
  "status_code": 400,
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Common Errors

| Status | Error | Resolution |
|--------|-------|-----------|
| 400 | Bad Request | Check request format and required fields |
| 404 | Not Found | Verify task ID exists |
| 422 | Validation Error | Check data types and formats |
| 500 | Server Error | Check logs and retry |

---

## Rate Limiting

Currently not implemented. In production, rate limiting should be configured.

---

## Pagination

Not applicable for current endpoints. Large list responses will be added in future versions.

---

## Versioning

API version is specified in response headers:
- `API-Version: 1.0.0`

---

## Examples

### Example 1: Deploy from Git Repository

```bash
curl -X POST http://localhost:8000/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/user/my-app",
    "domain": "myapp.example.com",
    "framework": "react"
  }'
```

### Example 2: Check Deployment Status

```bash
curl http://localhost:8000/deploy/550e8400-e29b-41d4-a716-446655440000
```

### Example 3: Upload ZIP File

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@myapp.zip"
```

---

## API Documentation

Interactive API documentation is available at:
- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`
- **OpenAPI Schema:** `/openapi.json`

---

## Support

For issues or questions, refer to:
- GitHub Issues: https://github.com/your-org/auto-deployer/issues
- Documentation: `/docs`
- Email: support@example.com

---

**Last Updated:** January 25, 2026
**Status:** Active
**Version:** 1.0.0

