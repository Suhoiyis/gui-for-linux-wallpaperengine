import os
import json
import gc
import shutil
from typing import Dict, Optional, List
import gi

gi.require_version('Gdk', '4.0')
from gi.repository import Gdk, GdkPixbuf

from py_GUI.const import WORKSHOP_PATH
from py_GUI.utils import get_folder_size

class WallpaperManager:
    def __init__(self, workshop_path: str = WORKSHOP_PATH):
        self.workshop_path = workshop_path
        self._wallpapers: Dict[str, Dict] = {}
        self._texture_cache: Dict[str, Gdk.Texture] = {}
        self._cache_max_size = 80
        self.last_scan_error: Optional[str] = None
        self.scan_errors: List[str] = []

    def scan(self) -> Dict[str, Dict]:
        self._wallpapers.clear()
        self.last_scan_error = None
        self.scan_errors = []
        
        if not os.path.exists(self.workshop_path):
            self.last_scan_error = f"Workshop directory not found: {self.workshop_path}"
            return self._wallpapers
        
        if not os.path.isdir(self.workshop_path):
            self.last_scan_error = f"Workshop path is not a directory: {self.workshop_path}"
            return self._wallpapers

        entries = []
        try:
            entries = sorted(os.listdir(self.workshop_path))
        except PermissionError:
            self.last_scan_error = f"Permission denied: {self.workshop_path}"
            return self._wallpapers
        except OSError as e:
            self.last_scan_error = f"Cannot read directory: {e}"
            return self._wallpapers

        for folder in entries:
            json_path = os.path.join(self.workshop_path, folder, "project.json")
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r') as f:
                        data = json.load(f)
                        preview_file = data.get("preview", "preview.jpg")
                        folder_path = os.path.join(self.workshop_path, folder)
                        self._wallpapers[folder] = {
                            "id": folder,
                            "title": data.get("title", "Unknown"),
                            "preview": os.path.join(folder_path, preview_file),
                            "description": data.get("description", ""),
                            "type": data.get("type", "Scene"),
                            "tags": data.get("tags", []),
                            "file": data.get("file", ""),
                            "contentrating": data.get("contentrating", ""),
                            "version": data.get("version", ""),
                            "size": get_folder_size(folder_path),
                        }
                except json.JSONDecodeError as e:
                    self.scan_errors.append(f"Invalid JSON in {folder}: {e}")
                except Exception as e:
                    self.scan_errors.append(f"Error reading {folder}: {e}")
        
        if not self._wallpapers and not self.last_scan_error:
            self.last_scan_error = f"No wallpapers found in: {self.workshop_path}"
        
        return self._wallpapers

    def get_texture(self, path: str, size: int = 170) -> Optional[Gdk.Texture]:
        """Get thumbnail texture with LRU cache"""
        cache_key = f"{path}_{size}"
        if cache_key in self._texture_cache:
            return self._texture_cache[cache_key]

        if not os.path.exists(path):
            return None

        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, size, size, True)
            texture = Gdk.Texture.new_for_pixbuf(pixbuf)
            del pixbuf  # Immediate release

            # LRU Cache: clear half if full
            if len(self._texture_cache) >= self._cache_max_size:
                keys = list(self._texture_cache.keys())[:self._cache_max_size // 2]
                for k in keys:
                    del self._texture_cache[k]
                gc.collect()

            self._texture_cache[cache_key] = texture
            return texture
        except:
            return None

    def clear_cache(self):
        """Clear texture cache"""
        self._texture_cache.clear()

    def delete_wallpaper(self, folder_id: str) -> bool:
        """Delete wallpaper folder"""
        if folder_id not in self._wallpapers:
            return False

        folder_path = os.path.join(self.workshop_path, folder_id)
        if not os.path.exists(folder_path):
            return False

        try:
            # Get preview path before deletion for cache clearing
            preview_path = self._wallpapers[folder_id].get('preview', '')

            # Delete folder and contents
            shutil.rmtree(folder_path)

            # Remove from list
            del self._wallpapers[folder_id]

            # Clear from cache
            if preview_path:
                cache_keys_to_remove = [k for k in self._texture_cache.keys() if k.startswith(preview_path)]
                for key in cache_keys_to_remove:
                    del self._texture_cache[key]
            
            gc.collect()
            return True
        except Exception as e:
            print(f"[ERROR] Failed to delete wallpaper {folder_id}: {e}")
            return False
