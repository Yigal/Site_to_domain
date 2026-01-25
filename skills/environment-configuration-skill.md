# Environment Configuration Skill

## Description
Manages environment variable configuration, .env file creation/modification, and application settings management across deployment environments.

## Capabilities
- Create and modify .env files
- Parse existing .env files
- Add or update environment variables
- Export configuration to files
- Load configuration from files
- Validate environment variable formats
- Support variable interpolation
- Handle comments and formatting
- Merge multiple .env files
- Template variable expansion

## Key Operations
- `load_env_file(path)` - Parse .env file
- `save_env_file(path, variables)` - Write .env file
- `add_variable(key, value)` - Add or update variable
- `get_variable(key)` - Retrieve variable
- `delete_variable(key)` - Remove variable
- `merge_env(base, overrides)` - Combine environments
- `expand_variables(string)` - Interpolate variables
- `validate_variable(key, value)` - Check validity

## .env File Format
```bash
# Comments starting with #
VARIABLE_NAME=value
DATABASE_URL=postgresql://user:pass@host:5432/db
API_KEY=secret_key_value
FEATURE_FLAG=true
EMPTY_VAR=
QUOTED_VALUE="value with spaces"
```

## Environment Variable Sources
1. AWS Secrets Manager (hydrated at startup)
2. Deployment configuration request
3. Auto-generated values (project IDs, URLs)
4. Framework defaults
5. User-provided overrides

## Common Deployment Variables
- `VITE_APP_TITLE` - Application name
- `VITE_API_URL` - Backend API endpoint
- `VITE_FIREBASE_API_KEY` - Firebase API key
- `VITE_FIREBASE_AUTH_DOMAIN` - Firebase auth domain
- `VITE_PUBLIC_DEPLOYMENT_ID` - Deployment identifier
- `NODE_ENV` - Environment (production, development)

## Firebase-Specific Variables
- VITE_FIREBASE_PROJECT_ID
- VITE_FIREBASE_STORAGE_BUCKET
- VITE_FIREBASE_MESSAGING_SENDER_ID
- VITE_FIREBASE_APP_ID
- VITE_FIREBASE_AUTH_DOMAIN

## Variable Validation
- Key format: Alphanumeric + underscore
- Value format: No null characters
- Length restrictions: Reasonable limits
- Type checking: String, number, boolean
- URL validation: HTTP/HTTPS URLs
- Special character handling: Escape as needed

## Parsing Rules
- Lines starting with # are comments
- Empty lines are ignored
- Format: KEY=VALUE
- Quoted values preserve spaces
- Escaped characters: \n, \t, \", \\
- No multiline values (unless quoted)

## Error Handling
- Malformed .env syntax
- Invalid variable names
- Missing required variables
- Duplicate variable definitions
- File write permissions
- Invalid encoding (non-UTF-8)

## Integration Points
- Created by Code Transformation Agent
- Used during Cloudflare Pages build
- Consulted by frontend application
- Modified during config injection phase
- Referenced in second git push

## Variable Scope
- Project-level: Deployment-specific
- Build-time: Available during npm build
- Runtime: Exposed to application code
- Secrets: Never logged or exposed

## Vite-Specific Considerations
- VITE_ prefix for public variables
- All VITE_* vars exposed to frontend
- Build-time evaluation
- Static optimization

## Interpolation Examples
```bash
BASE_URL=https://example.com
API_URL=${BASE_URL}/api
LOG_LEVEL=info
LOG_FILE=/var/log/${LOG_LEVEL}.log
```

## Security Considerations
- Never store secrets in .env (use Secrets Manager)
- .env files should not be committed
- Restricted file permissions: 0644
- Sensitive values logged carefully
- Environment variable masking in logs

## File Operations
- Location: Workspace root or src/ directory
- Encoding: UTF-8
- Line endings: Unix (LF)
- Permissions: 0644 (readable by all, writable by owner)

## Notes
- Each deployment gets isolated .env
- Variables override each other by order
- Comments preserved during modification
- Vite-specific prefixes required for frontend exposure
- Firebase config injected after GCP project creation
