"""Custom type definitions and enumerations."""

from enum import Enum
from typing import Dict, Any


class Framework(str, Enum):
    """Supported frontend frameworks."""
    REACT = "react"
    VUE = "vue"
    NEXTJS = "nextjs"
    CRA = "cra"
    VUE3 = "vue3"
    SVELTE = "svelte"


class CloudProvider(str, Enum):
    """Supported cloud providers."""
    AWS = "aws"
    GITHUB = "github"
    CLOUDFLARE = "cloudflare"
    GCP = "gcp"


class SourceType(str, Enum):
    """Source code input type."""
    GIT_REPO = "git_repo"
    ZIP_FILE = "zip_file"
    GITHUB_REPO = "github_repo"


class Environment(str, Enum):
    """Deployment environment."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


# Type aliases
ConfigDict = Dict[str, Any]
StepOutput = Dict[str, Any]
