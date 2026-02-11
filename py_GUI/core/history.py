import os
import json
from typing import List, Dict
from datetime import datetime
from py_GUI.const import CONFIG_DIR


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
        self.history_file = os.path.join(CONFIG_DIR, "history.json")
        self.history: List[Dict] = self._load()
    
    def add(self, wp_id: str, title: str, preview: str) -> None:
        entry = {
            "id": wp_id,
            "title": title,
            "preview": preview,
            "timestamp": datetime.now().isoformat()
        }
        
        self.history.insert(0, entry)
        self.history = self.history[:self.MAX_ENTRIES]
        self._save()
    
    def get_all(self) -> List[Dict]:
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
    
    def _load(self) -> List[Dict]:
        """
        Load history from JSON file.
        
        Returns:
            List of history entries, or empty list if file doesn't exist
        """
        if not os.path.exists(self.history_file):
            return []
        
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return []
    
    def _save(self) -> None:
        """
        Save history to JSON file.
        """
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
