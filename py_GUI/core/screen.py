import subprocess
from typing import List, Optional

class ScreenManager:
    def __init__(self):
        self._screens_cache: Optional[List[str]] = None

    def get_screens(self) -> List[str]:
        """Get list of available screens"""
        if self._screens_cache is not None:
            return self._screens_cache

        screens = []
        try:
            result = subprocess.run(
                ['xrandr', '--query'],
                capture_output=True,
                text=True,
                timeout=5
            )
            for line in result.stdout.split('\n'):
                if ' connected' in line:
                    screen_name = line.split()[0]
                    screens.append(screen_name)
        except Exception as e:
            print(f"[SCREEN] Failed to get screens: {e}")
            screens = ['eDP-1']  # Default fallback

        self._screens_cache = screens
        return screens

    def refresh(self):
        """Refresh screen list"""
        self._screens_cache = None
        return self.get_screens()
