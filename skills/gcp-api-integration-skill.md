# GCP API Integration Skill

## Description
Provides comprehensive Google Cloud Platform API access for project management, service enablement, billing, and Firebase configuration.

## Capabilities
- Create GCP projects within organization
- Delete GCP projects
- Link projects to billing accounts
- Enable APIs on projects
- Configure service usage
- Manage IAM roles and service accounts
- Create Firebase projects
- Configure Identity Platform and authentication
- Retrieve Firebase configuration
- Add authorized domains
- Monitor operation status
- Handle long-running operations

## Libraries and Clients
- google-cloud-resource-manager - Project management
- google-cloud-billing - Billing operations
- google-cloud-service-usage - API enablement
- firebase-admin - Firebase management
- google-auth - Credential handling

## Key Operations
- `create_project(parent, project_id, display_name)` - Create project
- `delete_project(project_id)` - Delete project
- `list_projects(parent)` - List projects
- `update_project_billing_info(project_id, billing_account)` - Link billing
- `batch_enable_services(project_id, services)` - Enable APIs
- `add_firebase(project_id)` - Initialize Firebase
- `update_identity_platform_config()` - Configure auth
- `add_authorized_domain()` - Whitelist domain
- `get_firebase_config()` - Retrieve config

## Authentication
- Google Cloud Service Account JSON (Base64 in Secrets Manager)
- Credential types: service_account
- Credential file path: /tmp/gcp_creds.json (written at runtime)

## Required IAM Roles
- roles/resourcemanager.projectCreator - Organization level
- roles/billing.user - Billing Account level (critical)
- roles/serviceusage.serviceUsageAdmin - Project level
- roles/firebase.admin - Project level

## Enabled APIs
- identitytoolkit.googleapis.com - Google Identity Toolkit
- firebase.googleapis.com - Firebase services
- cloudresourcemanager.googleapis.com - Resource management
- serviceusage.googleapis.com - Service usage management
- firebase-management.googleapis.com - Firebase management

## Operation Polling
- Long-running operations return operation objects
- Polling interval: 5 seconds
- Maximum wait time: 5 minutes for project creation
- Exponential backoff after repeated polls
- Returns operation metadata and result

## Identity Platform Configuration
- Auth provider: Email/Password
- Authorized domains: pages.dev domain, custom domains
- CORS configuration: Auto-enabled for authorized domains
- Email verification: Configurable
- Password policy: Default Google standards

## Firebase Configuration Structure
```json
{
  "apiKey": "...",
  "authDomain": "project-id.firebaseapp.com",
  "projectId": "project-id",
  "storageBucket": "project-id.appspot.com",
  "messagingSenderId": "...",
  "appId": "...",
  "databaseURL": "https://project-id.firebaseio.com"
}
```

## Error Handling
- Permission denied on project creation
- Billing account not found or access denied (common failure)
- Invalid parent organization
- Billing already linked
- API not available in region
- Operation timeout
- Service activation failures

## Critical Failure Points
1. Billing role not granted ON billing account (not project)
2. Project creator role not at organization level
3. Service account permissions not activated
4. Invalid billing account ID format
5. Region restrictions on APIs

## Project Naming
- Format: Project ID must be unique globally
- Auto-generation: Use timestamp + random suffix
- Display name: User-friendly project name
- Slug: Derived from display name

## Concurrency
- Multiple project creations can happen in parallel
- Separate billing checks per project
- Independent API enablement per project

## Notes
- Project creation is slowest operation (60+ seconds)
- Requires async handling in Celery
- Billing role commonly misconfigured by users
- Service account must be created in host project
- Organization roles take 5-10 minutes to propagate

## Integration Points
- Used by GCP Project Agent
- Service account credentials from AWS Secrets Manager
- Organization ID from configuration
- Billing account ID from deployment request
- Receives pages.dev domain from Cloudflare
