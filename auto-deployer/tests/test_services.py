"""Tests for cloud service integrations."""

import pytest
from unittest.mock import Mock, patch
from app.services.source_manager import SourceManager
from app.services.aws_storage import AWSStorageService
from app.models.types import Framework


@pytest.mark.unit
def test_source_manager_initialization():
    """Test source manager initialization."""
    manager = SourceManager()
    assert manager.workspace_dir is not None
    assert manager.source_dir is not None


@pytest.mark.unit
def test_source_manager_detect_framework_react(tmp_path):
    """Test framework detection for React."""
    manager = SourceManager(str(tmp_path))

    # Create mock package.json
    import os
    os.makedirs(manager.source_dir, exist_ok=True)
    with open(os.path.join(manager.source_dir, "package.json"), "w") as f:
        f.write('{"dependencies": {"react": "^18.0.0"}}')

    framework = manager.detect_framework()
    assert framework == "react"


@pytest.mark.unit
def test_source_manager_detect_framework_default(tmp_path):
    """Test default framework detection."""
    manager = SourceManager(str(tmp_path))
    import os
    os.makedirs(manager.source_dir, exist_ok=True)

    framework = manager.detect_framework()
    assert framework == "react"


@pytest.mark.unit
def test_source_manager_validate_source_empty(tmp_path):
    """Test source validation with empty directory."""
    manager = SourceManager(str(tmp_path))
    import os
    os.makedirs(manager.source_dir, exist_ok=True)

    valid, message = manager.validate_source()
    # Empty directory validation
    assert isinstance(valid, bool)


@pytest.mark.unit
def test_source_manager_get_file_structure(tmp_path):
    """Test getting file structure."""
    manager = SourceManager(str(tmp_path))
    import os
    os.makedirs(manager.source_dir, exist_ok=True)

    # Create test files
    with open(os.path.join(manager.source_dir, "test.js"), "w") as f:
        f.write("console.log('test');")

    structure = manager.get_file_structure()
    assert isinstance(structure, dict)


@pytest.mark.unit
def test_aws_storage_service_initialization():
    """Test AWS storage service initialization."""
    service = AWSStorageService()
    assert service.s3_client is not None
    assert service.secrets_client is not None


@pytest.mark.unit
@patch("boto3.client")
def test_aws_upload_file(mock_boto_client):
    """Test S3 file upload."""
    mock_s3 = Mock()
    mock_boto_client.return_value = mock_s3

    service = AWSStorageService()
    service.s3_client = mock_s3

    result = service.upload_file("/tmp/test.txt", "test-key")
    assert result is True


@pytest.mark.unit
@patch("boto3.client")
def test_aws_store_secret(mock_boto_client):
    """Test storing secret in Secrets Manager."""
    mock_secrets = Mock()
    mock_boto_client.return_value = mock_secrets

    service = AWSStorageService()
    service.secrets_client = mock_secrets

    result = service.store_secret("my-secret", "secret-value")
    assert result is True


@pytest.mark.unit
def test_github_service_initialization():
    """Test GitHub service initialization."""
    from app.services.github_api import github_service
    assert github_service is not None


@pytest.mark.unit
def test_cloudflare_service_initialization():
    """Test Cloudflare service initialization."""
    from app.services.cloudflare_api import cloudflare_service
    assert cloudflare_service is not None
    assert cloudflare_service.account_id is not None


@pytest.mark.unit
def test_gcp_service_initialization():
    """Test GCP service initialization."""
    from app.services.gcp_identity import gcp_service
    assert gcp_service is not None
    assert gcp_service.project_id is not None
