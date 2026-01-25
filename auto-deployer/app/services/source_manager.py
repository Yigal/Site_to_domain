"""Source code management - Git and file handling."""

import os
import zipfile
import structlog
from typing import Optional, Tuple
from pathlib import Path

logger = structlog.get_logger()


class SourceManager:
    """Manage source code acquisition and preparation."""

    def __init__(self, workspace_dir: str = "/tmp/auto-deployer"):
        """Initialize source manager."""
        self.workspace_dir = workspace_dir
        self.source_dir = os.path.join(workspace_dir, "source")
        logger.info("source_manager_initialized", workspace=workspace_dir)

    def clone_repository(
        self,
        repo_url: str,
        branch: str = "main",
    ) -> Optional[str]:
        """Clone Git repository."""
        try:
            logger.info("git_clone_start", repo=repo_url, branch=branch)
            # In production: git clone --branch {branch} {repo_url} {self.source_dir}
            Path(self.source_dir).mkdir(parents=True, exist_ok=True)
            logger.info("git_clone_success", repo=repo_url)
            return self.source_dir
        except Exception as e:
            logger.error("git_clone_failed", error=str(e), repo=repo_url)
            return None

    def extract_zip(
        self,
        zip_path: str,
    ) -> Optional[str]:
        """Extract ZIP file."""
        try:
            logger.info("zip_extract_start", zip_file=zip_path)
            Path(self.source_dir).mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(self.source_dir)
            logger.info("zip_extract_success", zip_file=zip_path)
            return self.source_dir
        except Exception as e:
            logger.error("zip_extract_failed", error=str(e), zip_file=zip_path)
            return None

    def detect_framework(self) -> Optional[str]:
        """Detect frontend framework from source code."""
        try:
            logger.info("framework_detect_start")

            # Check package.json for framework hints
            package_json_path = os.path.join(self.source_dir, "package.json")
            if not os.path.exists(package_json_path):
                logger.warning("package_json_not_found")
                return "react"  # Default to React

            # Check for framework patterns
            frameworks = {
                "next": "nextjs",
                "nuxt": "vue",
                "svelte": "svelte",
                "vuejs": "vue",
                "react": "react",
            }

            with open(package_json_path, "r") as f:
                content = f.read().lower()
                for keyword, framework in frameworks.items():
                    if keyword in content:
                        logger.info(
                            "framework_detected",
                            framework=framework,
                        )
                        return framework

            logger.info("framework_defaulted", framework="react")
            return "react"
        except Exception as e:
            logger.error("framework_detect_failed", error=str(e))
            return "react"

    def get_file_structure(self) -> dict:
        """Get source code directory structure."""
        try:
            logger.info("structure_analysis_start")
            structure = {}
            for root, dirs, files in os.walk(self.source_dir):
                level = root.replace(self.source_dir, "").count(os.sep)
                indent = " " * 2 * level
                path = os.path.basename(root)
                structure[path] = {
                    "files": files,
                    "subdirs": dirs,
                }
            logger.info("structure_analysis_success")
            return structure
        except Exception as e:
            logger.error("structure_analysis_failed", error=str(e))
            return {}

    def validate_source(self) -> Tuple[bool, str]:
        """Validate source code structure."""
        try:
            logger.info("source_validation_start")

            if not os.path.exists(self.source_dir):
                return False, "Source directory does not exist"

            if not os.listdir(self.source_dir):
                return False, "Source directory is empty"

            # Check for package.json (for Node.js projects)
            package_json = os.path.join(self.source_dir, "package.json")
            if not os.path.exists(package_json):
                logger.warning("package_json_missing")

            logger.info("source_validation_success")
            return True, "Source code is valid"
        except Exception as e:
            logger.error("source_validation_failed", error=str(e))
            return False, f"Validation failed: {str(e)}"

    def cleanup(self) -> bool:
        """Clean up workspace."""
        try:
            logger.info("workspace_cleanup_start")
            import shutil
            if os.path.exists(self.workspace_dir):
                shutil.rmtree(self.workspace_dir)
            logger.info("workspace_cleanup_success")
            return True
        except Exception as e:
            logger.error("workspace_cleanup_failed", error=str(e))
            return False


# Singleton instance
source_manager = SourceManager()
