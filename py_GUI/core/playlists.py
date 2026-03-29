import time
import uuid
from typing import Any

from py_GUI.core.config import ConfigManager
from py_GUI.core.state import AppStateBus


FAVORITES_PLAYLIST_ID = "favorites"


class PlaylistService:
    def __init__(self, config: ConfigManager, bus: AppStateBus | None = None):
        self.config = config
        self.bus = bus
        self.ensure_favorites_playlist()

    def _emit(self, reason: str) -> None:
        if self.bus:
            _ = self.bus.emit("playlists-changed", reason)

    def _normalize(
        self, playlists: list[dict[str, Any]] | None
    ) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for p in playlists or []:
            if not isinstance(p, dict):
                continue
            pid = str(p.get("id", "")).strip()
            name = str(p.get("name", "")).strip()
            if not pid or not name:
                continue
            ids_raw = p.get("wallpaper_ids", [])
            ids: list[str] = []
            seen: set[str] = set()
            if isinstance(ids_raw, list):
                for wid in ids_raw:
                    sid = str(wid)
                    if sid and sid not in seen:
                        seen.add(sid)
                        ids.append(sid)
            created_at = int(p.get("created_at", int(time.time())))
            updated_at = int(p.get("updated_at", created_at))
            out.append(
                {
                    "id": pid,
                    "name": name,
                    "wallpaper_ids": ids,
                    "created_at": created_at,
                    "updated_at": updated_at,
                }
            )
        return out

    def get_playlists(self) -> list[dict[str, Any]]:
        playlists = self._normalize(self.config.get("playlists", []))
        return playlists

    def save_playlists(
        self, playlists: list[dict[str, Any]], reason: str = "update"
    ) -> None:
        self.config.set("playlists", self._normalize(playlists))
        self._emit(reason)

    def ensure_favorites_playlist(self) -> None:
        playlists = self.get_playlists()
        for p in playlists:
            if p["id"] == FAVORITES_PLAYLIST_ID:
                if p["name"] != "Favorites":
                    p["name"] = "Favorites"
                    p["updated_at"] = int(time.time())
                    self.save_playlists(playlists, "favorites-sync")
                return
        now = int(time.time())
        playlists.insert(
            0,
            {
                "id": FAVORITES_PLAYLIST_ID,
                "name": "Favorites",
                "wallpaper_ids": [],
                "created_at": now,
                "updated_at": now,
            },
        )
        self.save_playlists(playlists, "favorites-created")

    def get_playlist(self, playlist_id: str) -> dict[str, Any] | None:
        for p in self.get_playlists():
            if p["id"] == playlist_id:
                return p
        return None

    def create_playlist(self, name: str) -> dict[str, Any]:
        trimmed = name.strip()
        if not trimmed:
            raise ValueError("Playlist name cannot be empty")
        playlists = self.get_playlists()
        now = int(time.time())
        playlist = {
            "id": str(uuid.uuid4()),
            "name": trimmed,
            "wallpaper_ids": [],
            "created_at": now,
            "updated_at": now,
        }
        playlists.append(playlist)
        self.save_playlists(playlists, "playlist-created")
        return playlist

    def rename_playlist(self, playlist_id: str, name: str) -> None:
        trimmed = name.strip()
        if not trimmed:
            raise ValueError("Playlist name cannot be empty")
        playlists = self.get_playlists()
        for p in playlists:
            if p["id"] == playlist_id:
                p["name"] = (
                    "Favorites" if playlist_id == FAVORITES_PLAYLIST_ID else trimmed
                )
                p["updated_at"] = int(time.time())
                self.save_playlists(playlists, "playlist-renamed")
                return
        raise ValueError("Playlist not found")

    def delete_playlist(self, playlist_id: str) -> None:
        if playlist_id == FAVORITES_PLAYLIST_ID:
            raise ValueError("Favorites cannot be deleted")
        playlists = self.get_playlists()
        new_playlists = [p for p in playlists if p["id"] != playlist_id]
        if len(new_playlists) == len(playlists):
            raise ValueError("Playlist not found")
        self.save_playlists(new_playlists, "playlist-deleted")
        if self.config.get("cyclePlaylistId") == playlist_id:
            self.config.set("cyclePlaylistId", None)

    def add_wallpaper(self, playlist_id: str, wallpaper_id: str) -> None:
        playlists = self.get_playlists()
        for p in playlists:
            if p["id"] == playlist_id:
                ids = list(p["wallpaper_ids"])
                if wallpaper_id not in ids:
                    ids.append(wallpaper_id)
                    p["wallpaper_ids"] = ids
                    p["updated_at"] = int(time.time())
                    self.save_playlists(playlists, "playlist-item-added")
                return
        raise ValueError("Playlist not found")

    def remove_wallpaper(self, playlist_id: str, wallpaper_id: str) -> None:
        playlists = self.get_playlists()
        for p in playlists:
            if p["id"] == playlist_id:
                ids = [wid for wid in p["wallpaper_ids"] if wid != wallpaper_id]
                p["wallpaper_ids"] = ids
                p["updated_at"] = int(time.time())
                self.save_playlists(playlists, "playlist-item-removed")
                return
        raise ValueError("Playlist not found")

    def toggle_favorite(self, wallpaper_id: str) -> bool:
        favorites = self.get_playlist(FAVORITES_PLAYLIST_ID)
        if not favorites:
            self.ensure_favorites_playlist()
            favorites = self.get_playlist(FAVORITES_PLAYLIST_ID)
        if not favorites:
            return False
        ids = list(favorites["wallpaper_ids"])
        if wallpaper_id in ids:
            self.remove_wallpaper(FAVORITES_PLAYLIST_ID, wallpaper_id)
            return False
        self.add_wallpaper(FAVORITES_PLAYLIST_ID, wallpaper_id)
        return True

    def is_favorite(self, wallpaper_id: str) -> bool:
        favorites = self.get_playlist(FAVORITES_PLAYLIST_ID)
        if not favorites:
            return False
        return wallpaper_id in favorites["wallpaper_ids"]

    def remove_wallpaper_from_all(self, wallpaper_id: str) -> None:
        playlists = self.get_playlists()
        changed = False
        for p in playlists:
            ids = p.get("wallpaper_ids", [])
            new_ids = [wid for wid in ids if wid != wallpaper_id]
            if len(new_ids) != len(ids):
                p["wallpaper_ids"] = new_ids
                p["updated_at"] = int(time.time())
                changed = True
        if changed:
            self.save_playlists(playlists, "playlist-item-cleanup")
