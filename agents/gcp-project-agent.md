# GCP Project Agent

## Purpose
Orchestrates complete GCP infrastructure setup including project creation, billing linkage, API enablement, and Firebase/Identity Platform configuration.

## Responsibilities
- Create new GCP projects within organization
- Link billing accounts to projects (critical step)
- Enable required APIs (Identity Toolkit, Firebase)
- Configure Firebase on projects
- Set up Identity Platform with Email/Password authentication
- Add authorized domains for CORS compliance
- Retrieve Firebase configuration (API keys, auth domain)
- Delete projects during rollback
- Poll long-running operations until completion

## Key Functions
- `create_project()` - Create new GCP project
- `link_billing()` - Attach billing account to project
- `enable_apis()` - Enable Identity Toolkit and Firebase APIs
- `add_firebase()` - Initialize Firebase on project
- `configure_identity_platform()` - Enable auth methods
- `add_authorized_domain()` - Add Cloudflare domain to auth whitelist
- `get_firebase_config()` - Retrieve Firebase configuration
- `delete_project()` - Remove project (rollback)
- `_get_credentials()` - Load GCP service account JSON
- `_wait_for_operation()` - Poll operation completion

## Authentication
- GCP Service Account JSON (from AWS Secrets Manager, Base64 encoded)
- IAM Roles required:
  - `roles/resourcemanager.projectCreator` (Organization level)
  - `roles/billing.user` (Billing Account level - critical)
  - `roles/serviceusage.serviceUsageAdmin` (Project level)
  - `roles/firebase.admin` (Project level)

## Integration Points
- Receives Pages deployment URL from Cloudflare Pages Agent
- Sends Firebase config to Firebase Configuration Agent
- Coordinates with Saga Orchestration Agent
- Supports rollback operations

## Enabled APIs
- identitytoolkit.googleapis.com
- firebase.googleapis.com

## Auth Configuration
- Provider: Email/Password
- Authorized domains: project-name.pages.dev, custom domains

## Critical Notes
- Billing role MUST be granted on Billing Account, not project
- Project creation can take 60+ seconds (requires async handling)
- Two-phase process: project creation then Firebase setup

## Error Handling
- Billing permission denied
- Missing roles at organization or billing level
- API enablement failures
- Firebase initialization errors
- Long-running operation timeouts
