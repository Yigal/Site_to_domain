# Credential Encoding Skill

## Description
Handles secure encoding, decoding, and transformation of credentials including Base64 encoding for cloud service credentials.

## Capabilities
- Encode credentials to Base64
- Decode Base64-encoded credentials
- Convert between encoding formats
- Validate credential formats
- Manage JSON credentials (GCP)
- Handle binary credential data
- Parse credential structures
- Validate credential fields
- Support credential versioning

## Key Operations
- `base64_encode(data)` - Encode to Base64
- `base64_decode(encoded_string)` - Decode from Base64
- `encode_gcp_json(json_file_path)` - Encode GCP key
- `decode_gcp_json(base64_string)` - Decode GCP key
- `validate_credential_format(credential)` - Check validity
- `extract_credential_fields(credential)` - Get values
- `parse_json_credential(json_string)` - Parse JSON

## Base64 Encoding
- Standard RFC 4648 Base64
- Padding: Required (= characters)
- Line length: No restrictions (single line)
- Charset: A-Z, a-z, 0-9, +, /, =

## GCP Service Account JSON
- Format: Standard JSON
- Fields:
  - type: "service_account"
  - project_id: GCP project ID
  - private_key_id: Key version
  - private_key: RSA private key (PEM)
  - client_email: Service account email
  - client_id: Unique client identifier
  - auth_uri: Google auth URI
  - token_uri: Google token URI
  - auth_provider_x509_cert_url: Certificate URL
  - client_x509_cert_url: Client certificate URL

## Encoding Process
1. Read GCP JSON file
2. Load JSON as Python dictionary
3. Serialize to JSON string
4. Encode to Base64
5. Remove line breaks (single line)
6. Store in Secrets Manager

## Decoding Process
1. Retrieve Base64 string from Secrets Manager
2. Decode from Base64
3. Validate UTF-8 encoding
4. Parse as JSON
5. Validate required fields
6. Write to temporary file
7. Set GOOGLE_APPLICATION_CREDENTIALS

## Encoding Command (Manual)
```bash
# Linux/macOS
base64 -i /path/to/key.json | tr -d '\n'

# macOS (alternative)
cat /path/to/key.json | base64

# Windows PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("C:\path\to\key.json"))
```

## Decoding Command (Manual)
```bash
# Linux/macOS
echo "{base64_string}" | base64 -d > key.json

# Windows PowerShell
[IO.File]::WriteAllBytes("key.json", [Convert]::FromBase64String("{base64_string}"))
```

## Validation Checks
- Base64 format validity
- Padding correctness
- JSON structure validity
- Required fields present
- UTF-8 encoding
- JSON array/object structure
- Credential type verification

## Error Handling
- Invalid Base64 (not padded correctly)
- Non-UTF-8 encoding
- Malformed JSON
- Missing required fields
- Invalid credential structure
- Corrupted data

## GCP Credential Validation
```python
required_fields = [
    'type',
    'project_id',
    'private_key_id',
    'private_key',
    'client_email',
    'client_id',
    'auth_uri',
    'token_uri'
]
```

## Integration Points
- Used by AWS Secrets Management Skill
- Receives GCP JSON file path
- Stores encoded string in Secrets Manager
- Decodes at application startup
- Writes to /tmp/gcp_creds.json

## Security Measures
- Never log unencoded credentials
- Base64 encoding is not encryption (for transport only)
- Credentials stored encrypted in Secrets Manager
- Temporary files use restrictive permissions
- Automatic cleanup of decoded files

## Python Libraries
- base64: Standard library
- json: Standard library
- No external dependencies

## Credential Storage Location
- Secrets Manager: prod/auto-deployer/keys
- Key name: GCP_SERVICE_ACCOUNT_JSON
- Format: Base64-encoded JSON string

## File Permissions
- Original GCP JSON: 0644 (readable)
- Temporary decoded file: 0600 (owner only)
- Secret storage: Encrypted at rest

## Notes
- Base64 is encoding, not encryption
- Transport security provided by TLS/HTTPS
- Secrets Manager provides at-rest encryption
- Credentials rotated via Secrets Manager updates
- Application restart required for rotation

## Testing
1. Encode GCP JSON with base64
2. Store in Secrets Manager
3. Retrieve and decode
4. Validate JSON structure
5. Verify required fields present
6. Test authentication with decoded credentials
