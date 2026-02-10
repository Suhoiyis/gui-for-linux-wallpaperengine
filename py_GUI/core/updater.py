import json
import threading
import urllib.request
import urllib.error
from typing import Callable


class UpdateChecker:
    """Check for updates from GitHub releases."""
    
    GITHUB_API_URL = "https://api.github.com/repos/Suhoiyis/gui-for-linux-wallpaperengine/releases/latest"
    TIMEOUT = 5
    
    def check_update(self, current_version: str, callback: Callable[[str, str, bool], None]) -> None:
        """
        Check for updates in a background thread.
        
        Args:
            current_version: Current version string (e.g., "0.10.3" or "v0.10.3")
            callback: Function called with (latest_version, release_url, has_update)
                     - latest_version: Version from GitHub tag_name or None on error
                     - release_url: URL to the release page or None on error
                     - has_update: True if update available, False otherwise
        """
        thread = threading.Thread(
            target=self._check_update_thread,
            args=(current_version, callback),
            daemon=True
        )
        thread.start()
    
    def _check_update_thread(self, current_version: str, callback: Callable[[str, str, bool], None]) -> None:
        """Background thread worker for checking updates."""
        try:
            # Fetch latest release data
            req = urllib.request.Request(self.GITHUB_API_URL)
            with urllib.request.urlopen(req, timeout=self.TIMEOUT) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            # Extract version and URL
            tag_name = data.get('tag_name', '')
            release_url = data.get('html_url', '')
            
            # Normalize versions for comparison (remove 'v' prefix)
            latest_version = self._normalize_version(tag_name)
            current_normalized = self._normalize_version(current_version)
            
            # Compare versions
            has_update = self._compare_versions(current_normalized, latest_version)
            
            # Call callback with results
            callback(latest_version, release_url, has_update)
            
        except urllib.error.URLError as e:
            # Network error (timeout, connection error, etc.)
            callback(None, None, False)
        except json.JSONDecodeError:
            # Invalid JSON response
            callback(None, None, False)
        except Exception as e:
            # Any other unexpected error
            callback(None, None, False)
    
    @staticmethod
    def _normalize_version(version: str) -> str:
        """Remove 'v' prefix from version string."""
        if version.startswith('v'):
            return version[1:]
        return version
    
    @staticmethod
    def _compare_versions(current: str, latest: str) -> bool:
        """
        Compare two semantic versions.
        
        Args:
            current: Current version (e.g., "0.10.3")
            latest: Latest version (e.g., "0.10.4")
        
        Returns:
            True if latest > current, False otherwise
        """
        try:
            current_parts = [int(x) for x in current.split('.')]
            latest_parts = [int(x) for x in latest.split('.')]
            
            # Pad with zeros to match length
            max_len = max(len(current_parts), len(latest_parts))
            current_parts.extend([0] * (max_len - len(current_parts)))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            
            # Compare each part
            for curr, lat in zip(current_parts, latest_parts):
                if lat > curr:
                    return True
                elif lat < curr:
                    return False
            
            return False  # Versions are equal
        except (ValueError, AttributeError):
            # Invalid version format, assume no update
            return False
