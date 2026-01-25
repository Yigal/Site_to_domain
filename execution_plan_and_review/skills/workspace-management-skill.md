# Workspace Management Skill

## Description
Manages creation, organization, and cleanup of temporary workspace directories for deployment artifacts and source code.

## Capabilities
- Create temporary workspace directories
- Generate unique workspace identifiers
- Organize files within workspace
- Track workspace state
- Clean up workspace on completion
- Handle file permissions
- Support nested directory structures
- Validate workspace integrity
- Handle concurrent workspaces
- Error recovery and cleanup

## Key Operations
- `create_workspace()` - Create new workspace directory
- `create_workspace_id()` - Generate unique ID
- `get_workspace_path(workspace_id)` - Get workspace directory
- `validate_workspace()` - Check workspace exists
- `cleanup_workspace(workspace_id)` - Remove directory
- `list_files(workspace_id)` - List contents
- `get_workspace_size()` - Calculate disk usage
- `create_subdirectory()` - Create nested directories

## Workspace Structure
```
/tmp/deploy-{uuid}/
├── source/                # Extracted or cloned source code
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── build/                 # Build output location
├── config/                # Configuration files
└── temp/                  # Temporary working files
```

## Workspace Lifecycle
1. **Creation**: Unique directory created at /tmp/deploy-{uuid}
2. **Population**: Source code extracted or cloned
3. **Transformation**: Code modified via AST transformation
4. **Building**: Framework build occurs here
5. **Cleanup**: Directory recursively deleted

## Unique Identifier Generation
- Format: UUID version 4 (random)
- Example: /tmp/deploy-a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6
- Ensures no workspace conflicts
- Used for state tracking in saga

## Disk Management
- Default location: /tmp (Linux/macOS), %TEMP% (Windows)
- Automatic cleanup on process exit
- Size monitoring to prevent disk issues
- Quota enforcement if configured

## Permissions Handling
- Workspace permissions: 0755 (rwxr-xr-x)
- File permissions: Inherited from extraction/clone
- Write access: Restricted to application user
- Cleanup: Requires write permissions

## Error Handling
- Directory creation failures
- Permission denied errors
- Disk space exhaustion
- Cleanup failures
- Invalid workspace ID
- Concurrent access conflicts

## Cleanup Strategy
- Explicit cleanup after deployment (success/failure)
- Recursive directory removal (rm -rf equivalent)
- Error logging but continued cleanup
- Verification that directory is removed
- Force cleanup on timeout

## Concurrent Workspace Support
- Multiple deployments use separate workspaces
- UUID uniqueness prevents collisions
- Parallel cleanup operations safe
- Independent state per workspace

## Monitoring
- Track number of workspaces
- Monitor disk usage per workspace
- Log creation and deletion events
- Alert on cleanup failures
- Measure workspace lifetime

## Integration Points
- Created by Source Acquisition Agent
- Used by Code Transformation Agent
- Passed to GitHub Repository Agent
- Cleaned by Saga Orchestration Agent
- Referenced in deployment state

## Security Considerations
- Temporary directory on filesystem
- Restricted to application user
- Automatic cleanup prevents exposure
- No sensitive data persists post-cleanup
- Use secure temp location

## Performance Optimization
- Lazy directory creation
- Parallel cleanup operations
- Efficient file listing
- Minimal disk I/O overhead
- Reuse connections where possible

## Notes
- Workspace lifetime: Duration of deployment saga
- Max concurrent workspaces: Limited by disk space
- Cleanup is idempotent (safe to call multiple times)
- Large source files may impact cleanup time
- Docker volumes can bypass /tmp restrictions
