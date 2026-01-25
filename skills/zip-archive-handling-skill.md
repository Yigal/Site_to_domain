# ZIP Archive Handling Skill

## Description
Manages extraction, creation, and validation of ZIP archives for source code uploads and deployment artifacts.

## Capabilities
- Extract ZIP files to specified directory
- Create ZIP archives from directories
- Validate ZIP file integrity
- List ZIP file contents
- Extract selective files from archives
- Handle nested directory structures
- Verify member file checksums
- Support password-protected archives
- Stream extraction for large files
- Handle ZIP format variations

## Key Operations
- `extract_zip(zip_path, extract_to)` - Extract archive
- `create_zip(source_dir, output_path)` - Create archive
- `validate_zip(zip_path)` - Check integrity
- `list_contents(zip_path)` - Show member files
- `extract_file(zip_path, file_path)` - Extract single file
- `get_compression_info(zip_path)` - Get archive stats
- `verify_checksums(zip_path)` - Validate contents

## Extraction Process
1. Open ZIP archive
2. Validate archive structure
3. Check for path traversal attacks
4. Extract members to target directory
5. Preserve file permissions
6. Verify extracted file checksums
7. Cleanup on error

## Security Measures
- Path traversal prevention (relative path checks)
- ZIP bomb detection (uncompressed size limits)
- Archive integrity validation
- Member path validation
- Symbolic link handling
- File permission preservation
- Owner/group restrictions

## Supported ZIP Formats
- Standard ZIP (no compression)
- Deflate compression (most common)
- BZIP2 compression
- LZMA compression
- Stored files (no compression)

## Path Validation
- Reject paths with ../ (parent directory traversal)
- Reject absolute paths
- Reject paths outside extraction directory
- Convert to normalized paths
- Validate member names

## Size Limits
- Maximum archive size: 5 GB
- Maximum extracted size: 10 GB
- Maximum member file: 2 GB
- Compression ratio check: 10:1 max

## Error Handling
- Invalid ZIP format
- Corrupted archive
- Unreadable files
- Extraction directory doesn't exist
- Insufficient disk space
- Permission denied
- Path traversal attempts
- Unsupported compression

## Integration Points
- Used by Source Acquisition Agent
- Receives ZIP from S3 (AWS Storage Agent)
- Extracts to workspace
- Validates source code structure
- Supports folder upload option

## Validation Checks
- ZIP file signature verification
- Central directory integrity
- Member CRC32 checksums
- File count validation
- Compression method support

## Directory Structure Expected
```
project.zip
├── src/
├── public/
├── package.json
├── vite.config.js (or webpack.config.js)
├── .gitignore
└── README.md
```

## File Permissions
- Preserved from ZIP metadata
- Minimum permissions: 0644
- Executable bit honored where applicable
- Directory permissions: 0755

## Performance Optimization
- Stream extraction for large archives
- Parallel member extraction (where safe)
- Lazy validation (check as extract)
- Efficient file copying

## Nested ZIP Support
- Detection of ZIP files within archives
- Optional extraction of nested archives
- Recursive validation
- Size limit enforcement per level

## Cleanup on Error
- Partial extraction removal
- Temporary file cleanup
- Directory structure rollback
- Failed member logging

## Compatibility
- Python zipfile module
- Standard ZIP format compliance
- Cross-platform compatibility (Windows/Linux/macOS)
- Long filename support (LFH)

## Notes
- Large archives (> 100MB) may impact performance
- Extraction slower than git clone for equal-sized repos
- ZIP format more portable than tar.gz
- User-uploaded archives subject to stricter validation
- Nested directories preserved in extraction
