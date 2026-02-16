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

        self._screens_cache = screens
        return screens

    def get_first_screen(self) -> Optional[str]:
        """Get the first detected screen.
        
        Returns:
            First screen name if available, None otherwise.
        """
        screens = self.get_screens()
        return screens[0] if screens else None

    def get_primary_screen(self) -> Optional[str]:
        """Get the primary screen via xrandr, falling back to first screen.
        
        Returns:
            Primary screen name if available, first screen if primary not found,
            None if no screens available.
        """
        try:
            result = subprocess.run(
                ['xrandr', '--query'],
                capture_output=True,
                text=True,
                timeout=5
            )
            for line in result.stdout.split('\n'):
                if ' connected primary' in line:
                    return line.split()[0]
        except Exception as e:
            print(f"[SCREEN] Failed to get primary screen: {e}")
        
        # Fallback to first screen
        return self.get_first_screen()

    def refresh(self):
        """Refresh screen list"""
        self._screens_cache = None
        return self.get_screens()
