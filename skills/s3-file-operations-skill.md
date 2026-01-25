# S3 File Operations Skill

## Description
Manages file upload, download, and manipulation operations on AWS S3 for artifact and source code storage.

## Capabilities
- Upload files to S3 with multipart support for large files
- Download files from S3 with streaming
- Download and extract ZIP archives from S3
- List S3 objects with prefix filtering
- Delete objects from S3
- Check object existence
- Copy objects between locations
- Get object metadata (size, last modified, ETag)
- Configure bucket versioning and lifecycle

## Key Operations
- `put_object(bucket, key, file_body)` - Upload file
- `get_object(bucket, key)` - Download file
- `list_objects_v2(bucket, prefix)` - List objects
- `download_fileobj(bucket, key, fileobj)` - Stream download
- `upload_fileobj(fileobj, bucket, key)` - Stream upload
- `head_object(bucket, key)` - Get metadata
- `delete_object(bucket, key)` - Delete file
- `copy_object(source, destination)` - Copy between locations

## Multipart Upload
- Automatic chunking for large files (> 5MB recommended)
- Parallel part uploads for performance
- Configurable part size (default 5MB)
- Resume capability on failed parts
- Progress callback support

## Client Management
- Singleton S3 client for connection reuse
- Automatic credential discovery from environment
- Region configuration (us-east-1 default)
- Configurable retry policies and timeouts

## Archive Handling
- ZIP file download and extraction
- Automatic directory structure preservation
- Validation of archive integrity
- Memory-efficient streaming extraction
- Recursive directory extraction

## Error Handling
- NoSuchKey - Object not found
- NoSuchBucket - Bucket doesn't exist
- AccessDenied - Permission issues
- Timeout - Network connectivity
- InvalidPart - Corrupted multipart upload

## Integration Points
- Used by AWS Storage Agent
- Source code zip retrieval for Source Acquisition
- Configuration file storage and retrieval
- Temporary artifact management
- Deployment manifest storage

## Security Features
- IAM policy-based access control
- Bucket-level and prefix-level restrictions
- Encryption at rest (handled by S3)
- No credential exposure in logs
- Temporary file cleanup after operations

## Performance Optimization
- Connection pooling via boto3 session
- Parallel multipart uploads
- Streaming for large files
- Prefix-based filtering for efficient listing
- Caching of frequently accessed objects

## Configuration
- Bucket name: deployment-assets
- Region: Configurable via environment
- Default timeout: 30 seconds
- Retry attempts: 3 with exponential backoff
