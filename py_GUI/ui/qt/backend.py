from __future__ import annotations

from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, Property, Signal, Slot

from py_GUI.const import WORKSHOP_PATH
from py_GUI.core.config import ConfigManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.history import HistoryManager
from py_GUI.core.logger import LogManager
from py_GUI.core.nickname import NicknameManager
from py_GUI.core.playlists import FAVORITES_PLAYLIST_ID, PlaylistService
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.screen import ScreenManager
from py_GUI.core.state import StateManager
from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.ui.qt.state_bus import QtAppStateBus


def _to_file_uri(path_value: str) -> str:
    if not path_value:
        return ""
    try:
        return Path(path_value).resolve().as_uri()
    except (OSError, ValueError):
        return ""


def _format_size_text(size_value: object) -> str:
    if isinstance(size_value, str):
        return size_value
    if isinstance(size_value, (int, float)):
        return f"{float(size_value) / (1024.0 * 1024.0):.1f} MB"
    return "0.0 MB"


def _to_qt_wallpaper_list(
    scanned: dict[str, dict[str, object]], workshop_path: str
) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for wp_id, wp in scanned.items():
        preview = str(wp.get("preview", ""))
        items.append(
            {
                "id": str(wp_id),
                "title": str(wp.get("title", "Unknown")),
                "preview": _to_file_uri(preview),
                "type": str(wp.get("type", "Scene")),
                "path": str(Path(workshop_path) / str(wp_id)),
                "size": _format_size_text(wp.get("size", 0)),
            }
        )
    return items


class Backend(QObject):
    wallpapersChanged = Signal()
    selectedIdChanged = Signal()
    favoriteIdsChanged = Signal()
    screensChanged = Signal()
    selectedScreenChanged = Signal()
    activeMonitorsChanged = Signal()
    statusMessageChanged = Signal()

    def __init__(self):
        super().__init__()

        self.state_bus = QtAppStateBus()
        self.config = ConfigManager()
        self.log_manager = LogManager()
        self.screen_manager = ScreenManager()
        self.state_manager = StateManager(None)
        self.properties_manager = PropertiesManager(self.config)
        self.wallpaper_manager = WallpaperManager(self._get_workshop_path())
        self.history_manager = HistoryManager(self.config)
        self.nickname_manager = NicknameManager(self.config)
        self.playlist_service = PlaylistService(self.config, None)

        self.controller = WallpaperController(
            self.config,
            self.properties_manager,
            self.log_manager,
            self.screen_manager,
            state_manager=self.state_manager,
            signal_bus=None,
        )

        self._wallpapers: list[dict[str, str]] = []
        self._selected_id: str = ""
        self._selected_screen: str = ""
        self._screens: list[str] = []
        self._status_message: str = ""

        self.refresh()

    @Property(list, notify=wallpapersChanged)
    def wallpapers(self) -> list[dict[str, str]]:
        return self._wallpapers

    @Property(str, notify=selectedIdChanged)
    def selectedId(self) -> str:
        return self._selected_id

    @Property(list, notify=favoriteIdsChanged)
    def favoriteIds(self) -> list[str]:
        favorites = self.playlist_service.get_playlist(FAVORITES_PLAYLIST_ID)
        if not favorites:
            return []
        ids = favorites.get("wallpaper_ids", [])
        if not isinstance(ids, list):
            return []
        return [str(item) for item in ids]

    @Property(list, notify=screensChanged)
    def screens(self) -> list[str]:
        return self._screens

    @Property(str, notify=selectedScreenChanged)
    def selectedScreen(self) -> str:
        return self._selected_screen

    @Property(dict, notify=activeMonitorsChanged)
    def activeMonitors(self) -> dict[str, str | None]:
        return self.state_manager.get_active_monitors()

    @Property(str, notify=statusMessageChanged)
    def statusMessage(self) -> str:
        return self._status_message

    @Slot(str)
    def selectWallpaper(self, wp_id: str) -> None:
        self._selected_id = wp_id
        self.selectedIdChanged.emit()
        self._set_status(f"Selected wallpaper: {wp_id}")

    @Slot(str)
    def setSelectedScreen(self, screen: str) -> None:
        self._selected_screen = screen
        self.state_manager.set_last_screen(screen)
        self.selectedScreenChanged.emit()

    @Slot(str)
    def applyWallpaper(self, wp_id: str) -> None:
        target = self._selected_screen or self._preferred_screen()
        if not target:
            self._set_status("No available screens detected")
            return
        self.controller.apply(wp_id, screen=target)
        wp = self.wallpaper_manager.get_wallpaper(wp_id)
        if wp:
            self.history_manager.add(
                wp_id,
                str(wp.get("title", "Unknown")),
                str(wp.get("preview", "")),
            )
        self.activeMonitorsChanged.emit()
        self._set_status(f"Applied wallpaper {wp_id} on {target}")

    @Slot()
    def applySelectedWallpaper(self) -> None:
        if not self._selected_id:
            self._set_status("No wallpaper selected")
            return
        self.applyWallpaper(self._selected_id)

    @Slot()
    def stopWallpaper(self) -> None:
        self.controller.stop()
        self.activeMonitorsChanged.emit()
        self._set_status("Stopped wallpaper engine")

    @Slot(str)
    def toggleFavorite(self, wp_id: str) -> None:
        is_favorite = self.playlist_service.toggle_favorite(wp_id)
        self.favoriteIdsChanged.emit()
        self._set_status(f"{'Added' if is_favorite else 'Removed'} favorite: {wp_id}")

    @Slot(str, result=bool)
    def isFavorite(self, wp_id: str) -> bool:
        return self.playlist_service.is_favorite(wp_id)

    @Slot()
    def refresh(self) -> None:
        self._refresh_screens()

        self.wallpaper_manager.workshop_path = self._get_workshop_path()
        scanned = self.wallpaper_manager.scan()
        self._wallpapers = _to_qt_wallpaper_list(
            {str(wp_id): wp for wp_id, wp in scanned.items()},
            self.wallpaper_manager.workshop_path,
        )
        self.wallpapersChanged.emit()

        if self._wallpapers and not self._selected_id:
            self._selected_id = self._wallpapers[0]["id"]
            self.selectedIdChanged.emit()

        self.favoriteIdsChanged.emit()
        self.activeMonitorsChanged.emit()
        self._set_status(f"Loaded {len(self._wallpapers)} wallpapers")

    def _refresh_screens(self) -> None:
        self._screens = self.screen_manager.refresh()
        self.screensChanged.emit()

        if self._selected_screen and self._selected_screen in self._screens:
            return

        preferred = self._preferred_screen()
        self._selected_screen = preferred or ""
        self.selectedScreenChanged.emit()

    def _preferred_screen(self) -> Optional[str]:
        last = self.state_manager.get_last_screen()
        if isinstance(last, str) and last in self._screens:
            return last
        primary = self.screen_manager.get_primary_screen()
        if isinstance(primary, str) and primary in self._screens:
            return primary
        if self._screens:
            return self._screens[0]
        return None

    def _get_workshop_path(self) -> str:
        configured = self.config.get("workshopPath")
        if isinstance(configured, str) and configured.strip():
            return configured
        return WORKSHOP_PATH

    def _set_status(self, message: str) -> None:
        self._status_message = message
        self.statusMessageChanged.emit()
