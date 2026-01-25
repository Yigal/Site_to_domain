# Firebase Configuration Agent

## Purpose
Configures Firebase and Google Identity Platform for user authentication in deployed applications.

## Responsibilities
- Retrieve Firebase configuration details from GCP project
- Extract API keys, auth domain, and project identifiers
- Coordinate with Code Transformation Agent for config injection
- Configure Email/Password authentication provider
- Add authorized domains to Identity Platform
- Enable CORS for correct domains
- Support multi-push deployment strategy
- Validate identity configuration completeness

## Key Functions
- `get_firebase_config()` - Retrieve complete Firebase config
- `configure_auth_providers()` - Enable authentication methods
- `add_authorized_domain()` - Add domain to auth whitelist
- `validate_config()` - Verify configuration completeness
- `retrieve_api_key()` - Get Firebase API key
- `retrieve_auth_domain()` - Get auth domain
- `retrieve_project_id()` - Get GCP project ID
- `retrieve_database_url()` - Get Firestore/Realtime DB URL

## Firebase Configuration Output
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

## Authentication Methods Configured
- Email/Password authentication
- Support for future providers (Google, GitHub, etc.)

## Authorized Domains
- Primary: {project-name}.pages.dev
- Secondary: Custom domains (if configured)
- Additional domains added on-demand

## Integration Points
- Receives domain info from Cloudflare Pages Agent
- Sends config to Code Transformation Agent
- Coordinates with GCP Project Agent for configuration
- Works with two-push deployment strategy

## Deployment Strategy
- **Phase 1**: Initial code push without Firebase config (skeleton)
- **Phase 2**: GCP provisioning and Firebase setup concurrent
- **Phase 3**: Retrieve Firebase config and inject into source
- **Phase 4**: Second code push with complete configuration

## CORS Configuration
- Configured automatically for authorized domains
- Prevents cross-origin auth errors during login
- Dynamically updated when custom domains added

## Error Handling
- Missing Firebase configuration
- Incomplete API key retrieval
- Invalid auth domain configuration
- Authorization domain conflicts
- Firestore/Database URL retrieval failures

## Notes
- Firebase config must be injected for application functionality
- Identity Platform setup is project-specific
- Authorized domains critical for production deployments
- Config injection happens in Code Transformation Agent
