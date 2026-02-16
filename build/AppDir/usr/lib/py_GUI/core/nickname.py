from typing import Dict, Optional, List, Tuple
from py_GUI.core.config import ConfigManager


class NicknameManager:
    """Manage wallpaper nicknames stored in config.json"""
    
    def __init__(self, config: ConfigManager):
        self._config = config
        self._nicknames: Dict[str, str] = {}
        self.load_from_config()
    
    def load_from_config(self):
        """Load nicknames from config"""
        nicknames_data = self._config.get("wallpaperNicknames", {})
        self._nicknames = nicknames_data.copy()
    
    def save_to_config(self):
        """Save nicknames to config"""
        self._config.set("wallpaperNicknames", self._nicknames)
    
    def get(self, wp_id: str) -> Optional[str]:
        """Get nickname for wallpaper, return None if not set"""
        return self._nicknames.get(wp_id)
    
    def set(self, wp_id: str, nickname: str):
        """
        Set nickname for wallpaper.
        - Trim whitespace
        - If empty after trim -> delete
        - Max length 100 chars (truncate if longer)
        - Save to config
        """
        trimmed = nickname.strip()
        
        if not trimmed:
            # Empty after trim, delete if exists
            if wp_id in self._nicknames:
                del self._nicknames[wp_id]
        else:
            # Truncate to 100 chars
            trimmed = trimmed[:100]
            self._nicknames[wp_id] = trimmed
        
        self.save_to_config()
    
    def delete(self, wp_id: str):
        """Remove nickname for wallpaper"""
        if wp_id in self._nicknames:
            del self._nicknames[wp_id]
            self.save_to_config()
    
    def get_all(self) -> Dict[str, str]:
        """Return all nicknames as a copy"""
        return self._nicknames.copy()
    
    def has(self, wp_id: str) -> bool:
        """Check if wallpaper has a nickname"""
        return wp_id in self._nicknames
    
    def cleanup(self, valid_ids: List[str]):
        """Remove entries for invalid wp_ids (ids not in valid_ids)"""
        valid_set = set(valid_ids)
        to_delete = [wp_id for wp_id in self._nicknames if wp_id not in valid_set]
        
        for wp_id in to_delete:
            del self._nicknames[wp_id]
        
        if to_delete:
            self.save_to_config()
    
    def get_display_name(self, wp: Dict) -> Tuple[str, Optional[str]]:
        """
        Get display name for a wallpaper.
        
        Returns:
            Tuple of (display_name, secondary_text)
            - If nickname exists: (nickname, original_title)
            - Otherwise: (original_title, None)
        """
        wp_id = str(wp.get('id', ''))
        nickname = self.get(wp_id)
        title = wp.get('title', 'Unknown')
        
        if nickname:
            return (nickname, title)
        else:
            return (title, None)
