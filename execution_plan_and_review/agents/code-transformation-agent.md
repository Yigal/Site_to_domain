# Code Transformation Agent

## Purpose
Modifies source code semantically using AST parsing to prepare it for cloud deployment on Cloudflare Pages and Firebase integration.

## Responsibilities
- Parse JavaScript/TypeScript configuration files using Tree-sitter
- Modify vite.config.js to set correct base path for Cloudflare Pages
- Inject Firebase configuration into application source
- Update or create .env files with deployment variables
- Ensure code modifications are framework-aware and non-destructive

## Key Functions
- `set_vite_base_path()` - Update base path in vite config
- `inject_firebase_config()` - Insert Firebase credentials
- `update_env_file()` - Manage environment variables
- `_parse_javascript()` - Parse JS files to AST
- `_find_config_object()` - Query AST for config structures
- `_insert_property()` - Insert properties at correct positions
- `_write_modified_source()` - Write modified code back to file

## Technologies Used
- Tree-sitter (code parsing)
- Tree-sitter JavaScript parser
- AST querying and manipulation

## Integration Points
- Receives workspace path from Source Acquisition Agent
- Outputs modified source to GitHub Repository Agent
- Coordinates with Firebase Configuration Agent for credentials
- Works with AST Modification Skill

## Error Handling
- Malformed configuration files
- Missing defineConfig calls
- Invalid JavaScript syntax
- Parsing failures

## Notes
- Uses semantic AST manipulation instead of regex for safety
- Supports multiple config file patterns
- Handles both ES6 modules and CommonJS
