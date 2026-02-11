import json
import threading
import urllib.request
import urllib.error
from typing import Callable, Optional


class UpdateChecker:
    """Check for updates from GitHub releases."""
    
    GITHUB_API_URL = "https://api.github.com/repos/Suhoiyis/gui-for-linux-wallpaperengine/releases/latest"
    TIMEOUT = 5
    
    def check_update(self, current_version: str, callback: Callable[[Optional[str], Optional[str], bool], None]) -> None:
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
    
    def _check_update_thread(self, current_version: str, callback: Callable[[Optional[str], Optional[str], bool], None]) -> None:
        """Background thread worker for checking updates."""
        try:
            req = urllib.request.Request(
                self.GITHUB_API_URL,
                headers={'User-Agent': 'Linux-Wallpaper-Engine-GUI/UpdateChecker'}
            )
            with urllib.request.urlopen(req, timeout=self.TIMEOUT) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            tag_name = data.get('tag_name', '')
            release_url = data.get('html_url', '')
            
            latest_version = self._normalize_version(tag_name)
            current_normalized = self._normalize_version(current_version)
            
            has_update = self._compare_versions(current_normalized, latest_version)
            
            callback(latest_version, release_url, has_update)
            
        except urllib.error.HTTPError as e:
            if e.code == 404:
                callback("0.0.0", "", False)
            elif e.code == 403:
                callback("ERROR:RATE_LIMIT", None, False)
            else:
                callback(None, None, False)
        except (urllib.error.URLError, json.JSONDecodeError, Exception):
            callback(None, None, False)
    
    @staticmethod
    def _normalize_version(version: str) -> str:
        """Remove 'v' prefix from version string."""
        if version.startswith('v'):
            return version[1:]
        return version
    
    @staticmethod
    def _compare_versions(current: str, latest: str) -> bool:
        try:
            def parse_numeric_parts(version_str):
                base_version = version_str.split('-')[0].split('+')[0]
                return [int(part) for part in base_version.split('.')]
            
            current_parts = parse_numeric_parts(current)
            latest_parts = parse_numeric_parts(latest)
            
            max_len = max(len(current_parts), len(latest_parts))
            current_parts.extend([0] * (max_len - len(current_parts)))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            
            for curr_val, lat_val in zip(current_parts, latest_parts):
                if lat_val > curr_val:
                    return True
                elif lat_val < curr_val:
                    return False
            
            return False
        except (ValueError, AttributeError, IndexError):
            return False
