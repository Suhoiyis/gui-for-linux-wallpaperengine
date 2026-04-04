from __future__ import annotations

from pathlib import Path
from typing import Optional
from typing import TypedDict

from PySide6.QtCore import QObject, Property, Signal, Slot

from py_GUI.const import WORKSHOP_PATH
from py_GUI.core.config import ConfigManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.history import HistoryManager
from py_GUI.core.logger import LogManager
from py_GUI.core.nickname import NicknameManager
from py_GUI.core.playlists import FAVORITES_PLAYLIST_ID, PlaylistService
from py_GUI.core.performance import PerformanceMonitor


class _QtPerfHistory(TypedDict):
    cpu: list[float]
    memory_mb: list[float]


class _QtPerfDetail(TypedDict):
    pid: int
    name: str
    cpu: float
    cpu_fmt: str
    memory_mb: float
    memory_fmt: str
    threads: int
    status: str
    history: _QtPerfHistory


class _QtPerfTotal(TypedDict):
    cpu: float
    cpu_fmt: str
    memory_mb: float
    memory_fmt: str
    threads: int
    history: _QtPerfHistory
    thread_names: dict[str, list[str]]


class _QtPerfStats(TypedDict):
    total: _QtPerfTotal
    details: dict[str, _QtPerfDetail]


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
    playlistsChanged = Signal()
    activePlaylistIdChanged = Signal()
    linkedModeChanged = Signal()
    settingsChanged = Signal()
    performanceChanged = Signal()

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
        self.perf_monitor = PerformanceMonitor(None)

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
        self._active_playlist_id: str = ""
        self._linked_mode: bool = bool(self.config.get("apply_mode") == "same")
        self._performance_total: dict[str, object] = {
            "cpu": 0.0,
            "cpu_fmt": "0%",
            "memory_mb": 0.0,
            "memory_fmt": "0 MB",
            "threads": 0,
        }
        self._performance_details: list[dict[str, object]] = []
        self._perf_callback_registered = False
        self._ensure_perf_bridge()

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

    @Property(dict, notify=performanceChanged)
    def performanceTotal(self) -> dict[str, object]:
        return dict(self._performance_total)

    @Property(list, notify=performanceChanged)
    def performanceProcesses(self) -> list[dict[str, object]]:
        return list(self._performance_details)

    @Property(dict, notify=selectedIdChanged)
    def selectedWallpaper(self) -> dict[str, str]:
        if not self._selected_id:
            return {}
        for wp in self._wallpapers:
            if wp.get("id") == self._selected_id:
                return dict(wp)
        return {}

    @Property(list, notify=playlistsChanged)
    def playlists(self) -> list[dict[str, object]]:
        raw = self.playlist_service.get_playlists()
        out: list[dict[str, object]] = []
        for item in raw:
            out.append(
                {
                    "id": str(item.get("id", "")),
                    "name": str(item.get("name", "Unnamed")),
                    "wallpaper_ids": [
                        str(wid) for wid in item.get("wallpaper_ids", [])
                    ],
                }
            )
        return out

    @Property(str, notify=activePlaylistIdChanged)
    def activePlaylistId(self) -> str:
        return self._active_playlist_id

    @Property(bool, notify=linkedModeChanged)
    def linkedMode(self) -> bool:
        return self._linked_mode

    @Property(int, notify=settingsChanged)
    def fps(self) -> int:
        value = self.config.get("fps", 30)
        return int(value) if isinstance(value, (int, float)) else 30

    @Property(int, notify=settingsChanged)
    def volume(self) -> int:
        value = self.config.get("volume", 0)
        return int(value) if isinstance(value, (int, float)) else 0

    @Property(bool, notify=settingsChanged)
    def silence(self) -> bool:
        return bool(self.config.get("silence", True))

    @Property(str, notify=settingsChanged)
    def scaling(self) -> str:
        value = self.config.get("scaling", "default")
        return str(value)

    @Property(str, notify=settingsChanged)
    def clamping(self) -> str:
        value = self.config.get("clamping", "clamp")
        return str(value)

    @Property(str, notify=settingsChanged)
    def workshopPath(self) -> str:
        value = self.config.get("workshopPath", "")
        return str(value or "")

    @Slot(str)
    def selectWallpaper(self, wp_id: str) -> None:
        self._selected_id = wp_id
        self.selectedIdChanged.emit()
        self._set_status(f"Selected wallpaper: {wp_id}")

    @Slot(str)
    def setActivePlaylist(self, playlist_id: str) -> None:
        self._active_playlist_id = playlist_id
        self.activePlaylistIdChanged.emit()

    @Slot()
    def clearActivePlaylist(self) -> None:
        self._active_playlist_id = ""
        self.activePlaylistIdChanged.emit()

    @Slot(str)
    def createPlaylist(self, name: str) -> None:
        if not name.strip():
            self._set_status("Playlist name cannot be empty")
            return
        self.playlist_service.create_playlist(name)
        self.playlistsChanged.emit()
        self._set_status(f"Created playlist: {name.strip()}")

    @Slot(str, str)
    def renamePlaylist(self, playlist_id: str, name: str) -> None:
        self.playlist_service.rename_playlist(playlist_id, name)
        self.playlistsChanged.emit()
        self._set_status("Playlist renamed")

    @Slot(str)
    def deletePlaylist(self, playlist_id: str) -> None:
        self.playlist_service.delete_playlist(playlist_id)
        if self._active_playlist_id == playlist_id:
            self._active_playlist_id = ""
            self.activePlaylistIdChanged.emit()
        self.playlistsChanged.emit()
        self._set_status("Playlist deleted")

    @Slot(str)
    def setSelectedScreen(self, screen: str) -> None:
        self._selected_screen = screen
        self.state_manager.set_last_screen(screen)
        self.selectedScreenChanged.emit()

    @Slot(bool)
    def setLinkedMode(self, linked: bool) -> None:
        self._linked_mode = linked
        self.config.set("apply_mode", "same" if linked else "diff")
        self.linkedModeChanged.emit()
        self.settingsChanged.emit()
        self._set_status(f"Apply mode: {'same' if linked else 'diff'}")

    @Slot(int)
    def setFps(self, fps: int) -> None:
        clamped = max(1, min(144, int(fps)))
        self.config.set("fps", clamped)
        self.settingsChanged.emit()
        self._set_status(f"FPS set to {clamped}")

    @Slot(int)
    def setVolume(self, volume: int) -> None:
        clamped = max(0, min(100, int(volume)))
        self.config.set("volume", clamped)
        self.settingsChanged.emit()
        self._set_status(f"Volume set to {clamped}")

    @Slot(bool)
    def setSilence(self, silence: bool) -> None:
        self.config.set("silence", bool(silence))
        self.settingsChanged.emit()
        self._set_status(f"Silence {'enabled' if silence else 'disabled'}")

    @Slot(str)
    def setScaling(self, scaling: str) -> None:
        self.config.set("scaling", str(scaling))
        self.settingsChanged.emit()
        self._set_status(f"Scaling set to {scaling}")

    @Slot(str)
    def setClamping(self, clamping: str) -> None:
        self.config.set("clamping", str(clamping))
        self.settingsChanged.emit()
        self._set_status(f"Clamping set to {clamping}")

    @Slot(str)
    def setWorkshopPath(self, workshop_path: str) -> None:
        self.config.set("workshopPath", str(workshop_path))
        self.wallpaper_manager.workshop_path = str(workshop_path)
        self.settingsChanged.emit()
        self._set_status("Workshop path updated")

    @Slot(str)
    def applyWallpaper(self, wp_id: str) -> None:
        if self._linked_mode and self._screens:
            self.controller.apply(wp_id, screens=self._screens)
            wp = self.wallpaper_manager.get_wallpaper(wp_id)
            if wp:
                self.history_manager.add(
                    wp_id,
                    str(wp.get("title", "Unknown")),
                    str(wp.get("preview", "")),
                )
            self.activeMonitorsChanged.emit()
            self._set_status(
                f"Applied wallpaper {wp_id} on all screens ({len(self._screens)})"
            )
            return

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
        self.playlistsChanged.emit()
        self.activeMonitorsChanged.emit()
        self._set_status(f"Loaded {len(self._wallpapers)} wallpapers")

    def _ensure_perf_bridge(self) -> None:
        if self._perf_callback_registered:
            return
        self.perf_monitor.add_callback(self._on_performance_update)
        self._perf_callback_registered = True

    def _on_performance_update(self, stats: _QtPerfStats) -> None:
        total = stats.get("total", {}) if isinstance(stats, dict) else {}
        if isinstance(total, dict):
            self._performance_total = {
                "cpu": float(total.get("cpu", 0.0)),
                "cpu_fmt": str(total.get("cpu_fmt", "0%")),
                "memory_mb": float(total.get("memory_mb", 0.0)),
                "memory_fmt": str(total.get("memory_fmt", "0 MB")),
                "threads": int(total.get("threads", 0)),
            }

        details_obj = stats.get("details", {}) if isinstance(stats, dict) else {}
        rows: list[dict[str, object]] = []
        if isinstance(details_obj, dict):
            for category, item in details_obj.items():
                if not isinstance(item, dict):
                    continue
                rows.append(
                    {
                        "category": str(category),
                        "pid": int(item.get("pid", 0)),
                        "name": str(item.get("name", "")),
                        "cpu": float(item.get("cpu", 0.0)),
                        "cpu_fmt": str(item.get("cpu_fmt", "0%")),
                        "memory_mb": float(item.get("memory_mb", 0.0)),
                        "memory_fmt": str(item.get("memory_fmt", "0 MB")),
                        "threads": int(item.get("threads", 0)),
                        "status": str(item.get("status", "")),
                    }
                )

        self._performance_details = rows
        self.performanceChanged.emit()

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
