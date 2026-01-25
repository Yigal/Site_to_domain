# GCP Billing Management Skill

## Description
Manages Google Cloud Platform billing account linkage and financial configuration for newly created projects.

## Capabilities
- Link projects to billing accounts
- Retrieve billing account information
- Update project billing configuration
- Check billing status and enablement
- Verify billing permissions
- Handle billing API operations
- Manage budget alerts
- Track spending and quotas
- Validate billing account access

## Key Operations
- `update_project_billing_info(project_id, billing_account)` - Link billing
- `get_billing_account_info(account_id)` - Retrieve account details
- `check_billing_enabled(project_id)` - Verify billing status
- `list_billing_accounts()` - Get available accounts
- `set_billing_budget(project_id, budget)` - Configure budget
- `get_project_spending(project_id)` - Check costs

## Billing Account Structure
- Format: `billingAccounts/{billing-account-id}`
- Example: billingAccounts/012345-ABCDEF-GHIJKL
- Access: Requires billing.user role on account
- Ownership: Organization or individual

## Linking Process
1. Obtain billing account ID
2. Verify service account has billing.user role
3. Call updateProjectBillingInfo API
4. Verify billing_enabled flag is true
5. Confirm project can use paid APIs

## Critical Requirement
- Role `roles/billing.user` MUST be granted on Billing Account, not project
- Most common configuration error
- Granting at project level will NOT work
- Requires billing admin to grant

## API Used
- Google Cloud Billing API
- Endpoint: billing.googleapis.com
- Service: CloudBillingClient
- Method: update_project_billing_info

## Request Payload
```json
{
  "name": "projects/{project_id}",
  "projectBillingInfo": {
    "billingAccountName": "billingAccounts/{billing_account_id}",
    "billingEnabled": true
  }
}
```

## Error Handling
- billing.user role not granted (403 Forbidden)
- Billing account not found (404 Not Found)
- Billing account closed (invalid operation)
- Project not found (404 Not Found)
- Invalid account format (400 Bad Request)
- Service not enabled (403 Permission Denied)

## Common Failures
1. Role granted on project instead of billing account
2. Wrong billing account ID format
3. Service account email incorrect
4. Billing account doesn't have payment method
5. Service account not activated in host project

## Verification
- Check billing.open flag (true = active)
- Verify billing_enabled on project (true = linked)
- Test API enablement after linking
- Confirm paid services can be used

## Required IAM Setup
- Service account must have:
  - roles/resourcemanager.projectCreator (Organization)
  - roles/billing.user (Billing Account) - CRITICAL
  - roles/serviceusage.serviceUsageAdmin (Project)
  - roles/firebase.admin (Project)

## Integration Points
- Used by GCP Project Agent
- Service account from AWS Secrets Manager
- Billing account ID from deployment request
- Required before API enablement
- Prerequisite for Firebase setup

## Cost Tracking
- Free tier: $0 for some services
- Paid services: Identity Platform requires billing
- Budget alerts: Configurable thresholds
- Spending reports: Available post-linkage

## Notes
- Billing must be linked before enabling paid APIs
- Identity Platform requires active billing
- Firestore requires billing for certain operations
- Budget alerts help manage costs
- Cost optimization: Use free tier services where possible

## Testing Checklist
- [ ] Service account has billing.user role on billing account
- [ ] Not on project level
- [ ] Billing account ID is correct format
- [ ] Billing account is active and has payment method
- [ ] Service account email is correct
- [ ] Test with small project creation first
