# Source Acquisition Agent

## Purpose
Responsible for acquiring source code from either a Git repository or an uploaded folder/zip file and preparing it for deployment.

## Responsibilities
- Clone Git repositories and detach from original history
- Extract and validate uploaded ZIP files from S3
- Detect framework type (React/Vite/Next.js) from package.json
- Create and manage temporary workspace directories
- Handle source code validation and error handling

## Key Functions
- `prepare_workspace()` - Initialize workspace and acquire source
- `detect_framework()` - Identify React framework type
- `cleanup_workspace()` - Remove temporary workspace
- `_clone_repository()` - Git clone with history detachment
- `_extract_uploaded_zip()` - Extract ZIP and validate contents

## Dependencies
- AWS Storage Service
- Git (subprocess)
- Python zipfile module
- Temporary file system

## Integration Points
- Receives source configuration from deployment request
- Outputs prepared workspace path to Code Transformation Agent
- Communicates with AWS Storage for ZIP retrieval

## Error Handling
- Invalid source type detection
- Git clone failures
- ZIP extraction errors
- Missing or corrupted source files
