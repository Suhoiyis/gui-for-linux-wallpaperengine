import os
from typing import Any
from datetime import datetime
from py_GUI.const import CONFIG_DIR, HISTORY_FILE
from py_GUI.core.storage import read_history, write_history


class HistoryManager:
    """
    Manages wallpaper playback history with persistence.

    - Stores up to 30 entries in history.json
    - Deduplicates by wp_id (moves existing to top)
    - Saves automatically on modifications
    """

    MAX_ENTRIES = 30

    def __init__(self, config_manager):
        """
        Initialize HistoryManager.

        Args:
            config_manager: ConfigManager instance (for future extensibility)
        """
        self.history_file = HISTORY_FILE
        self.history: list[dict[str, Any]] = self._load()

    def add(self, wp_id: str, title: str, preview: str) -> None:
        self.history = [e for e in self.history if e.get("id") != wp_id]

        entry = {
            "id": wp_id,
            "title": title,
            "preview": preview,
            "timestamp": datetime.now().isoformat(),
        }

        self.history.insert(0, entry)
        self.history = self.history[: self.MAX_ENTRIES]
        self._save()

    def get_all(self) -> list[dict[str, Any]]:
        """
        Get all history entries in order.

        Returns:
            List of history entries (most recent first)
        """
        return self.history.copy()

    def has_history(self) -> bool:
        """
        Check if history has any entries.

        Returns:
            True if history is not empty, False otherwise
        """
        return len(self.history) > 0

    def clear(self) -> None:
        """
        Clear all history and save.
        """
        self.history = []
        self._save()

    def _load(self) -> list[dict[str, Any]]:
        """
        Load history from JSON file.

        Returns:
            List of history entries, or empty list if file doesn't exist
        """
        if not os.path.exists(self.history_file):
            return []
        return read_history()

    def _save(self) -> None:
        """
        Save history to JSON file.
        """
        os.makedirs(CONFIG_DIR, exist_ok=True)
        write_history(self.history)
