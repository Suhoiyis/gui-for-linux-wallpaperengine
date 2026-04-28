from __future__ import annotations

import os
import random
import signal
import shutil
import sys
import time
from pathlib import Path
from typing import Optional
from typing import TypedDict

from PySide6.QtCore import (
    QCoreApplication,
    QObject,
    Property,
    QProcess,
    QTimer,
    Signal,
    Slot,
)
from PySide6.QtGui import QGuiApplication, QDesktopServices
from PySide6.QtCore import QUrl

from py_GUI.const import VERSION, WORKSHOP_PATH
from py_GUI.core.config import ConfigManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.history import HistoryManager
from py_GUI.core.logger import LogManager
from py_GUI.core.nickname import NicknameManager
from py_GUI.core.playlists import FAVORITES_PLAYLIST_ID, PlaylistService
from py_GUI.core.performance import PerformanceMonitor
from py_GUI.core.updater import UpdateChecker


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
        raw_tags = wp.get("tags", [])
        tags_text = (
            ", ".join([str(tag) for tag in raw_tags])
            if isinstance(raw_tags, list)
            else ""
        )
        items.append(
            {
                "id": str(wp_id),
                "title": str(wp.get("title", "Unknown")),
                "preview": _to_file_uri(preview),
                "type": str(wp.get("type", "Scene")),
                "path": str(Path(workshop_path) / str(wp_id)),
                "size": _format_size_text(wp.get("size", 0)),
                "description": str(wp.get("description", "")),
                "tags": tags_text,
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
    nicknameChanged = Signal()
    historyChanged = Signal()
    appMetaChanged = Signal()
    screenshotHistoryChanged = Signal()
    highlightSettingFieldChanged = Signal()
    screenshotHintActiveChanged = Signal()
    themeModeChanged = Signal()

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
        self.update_checker = UpdateChecker()

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
        self._cycle_timer: QTimer | None = None
        self._highlight_setting_field: str = ""
        self._screenshot_hint_active: bool = False
        self._theme_mode: str = str(self.config.get("themeMode", "dark") or "dark")
        self._ensure_perf_bridge()
        self._init_cycle_timer()

        self.refresh()

    def _init_cycle_timer(self) -> None:
        if self._cycle_timer is not None:
            return
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self._on_cycle_timeout)
        self._cycle_timer = timer

    def _on_cycle_timeout(self) -> None:
        self._cycle_once()
        if self._cfg_cycle_enabled():
            self._start_cycle_timer()

    def _cfg_cycle_enabled(self) -> bool:
        return bool(self.config.get("cycleEnabled", False))

    def _cfg_cycle_interval(self) -> int:
        value = self.config.get("cycleInterval", 15)
        if isinstance(value, (int, float)):
            return int(value)
        return 15

    def _cfg_cycle_order(self) -> str:
        value = self.config.get("cycleOrder", "random")
        return str(value or "random")

    def _cfg_cycle_playlist_id(self) -> str:
        value = self.config.get("cyclePlaylistId", None)
        return str(value).strip() if isinstance(value, str) else ""

    def _start_cycle_timer(self) -> None:
        self._init_cycle_timer()
        if self._cycle_timer is None:
            return
        if not self._cfg_cycle_enabled():
            self._cycle_timer.stop()
            return
        active_monitors = self.state_manager.get_active_monitors()
        if not active_monitors:
            self._cycle_timer.stop()
            return
        interval_ms = max(1, self._cfg_cycle_interval()) * 60 * 1000
        self._cycle_timer.start(interval_ms)

    def _stop_cycle_timer(self) -> None:
        if self._cycle_timer is not None:
            self._cycle_timer.stop()

    def _cycle_candidates(self) -> list[str]:
        all_ids = [str(item.get("id", "")) for item in self._wallpapers]
        all_ids = [wid for wid in all_ids if wid]
        if not all_ids:
            return []

        cycle_playlist_id = self._cfg_cycle_playlist_id()
        if not cycle_playlist_id:
            return all_ids

        playlist = self.playlist_service.get_playlist(cycle_playlist_id)
        if not playlist:
            return all_ids
        selected = [
            str(wid)
            for wid in playlist.get("wallpaper_ids", [])
            if str(wid) in set(all_ids)
        ]
        return selected if selected else all_ids

    def _cycle_once(self) -> None:
        active_monitors = self.state_manager.get_active_monitors()
        if not active_monitors:
            return

        screens = self.screen_manager.get_screens()
        candidates = self._cycle_candidates()
        if not candidates:
            self._set_status("Cycle skipped: no wallpapers available")
            return

        cycle_order = self._cfg_cycle_order()
        sorted_ids: list[str] = []
        if cycle_order != "random":
            sorted_ids = self.wallpaper_manager.get_sorted_wallpapers(cycle_order)
            allowed = set(candidates)
            sorted_ids = [wid for wid in sorted_ids if wid in allowed]
            if not sorted_ids:
                sorted_ids = candidates
                cycle_order = "random"

        new_monitors: dict[str, str | None] = {}
        for screen in active_monitors.keys():
            if screen not in screens:
                continue
            if cycle_order == "random":
                chosen = random.choice(candidates)
            else:
                current = active_monitors.get(screen)
                if current in sorted_ids:
                    idx = sorted_ids.index(str(current))
                    chosen = sorted_ids[(idx + 1) % len(sorted_ids)]
                else:
                    chosen = sorted_ids[0]
            new_monitors[screen] = chosen

        if not new_monitors:
            self._set_status("Cycle skipped: no active screens")
            return

        self.state_manager.set_active_monitors(new_monitors)
        primary = self.state_manager.get_last_screen()
        if primary not in new_monitors:
            primary = next(iter(new_monitors.keys()))
            self.state_manager.set_last_screen(primary)
        self.state_manager.set_last_wallpaper(new_monitors.get(primary))

        self.controller.restart_wallpapers()
        self.activeMonitorsChanged.emit()
        self._set_status(f"Cycled wallpaper ({cycle_order})")

    def _start_detached(self, program: str, args: list[str], workdir: str) -> bool:
        result = QProcess.startDetached(program, args, workdir)
        if isinstance(result, tuple):
            return bool(result[0])
        return bool(result)

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
                item = dict(wp)
                nickname = self.nickname_manager.get(self._selected_id)
                if nickname:
                    item["title"] = nickname
                return item
        return {}

    @Property(str, notify=nicknameChanged)
    def selectedOriginalTitle(self) -> str:
        if not self._selected_id:
            return ""
        wp = self.wallpaper_manager.get_wallpaper(self._selected_id)
        if not wp:
            return ""
        return str(wp.get("title", ""))

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

    @Property(bool, notify=settingsChanged)
    def cycleEnabled(self) -> bool:
        return bool(self.config.get("cycleEnabled", False))

    @Property(int, notify=settingsChanged)
    def cycleInterval(self) -> int:
        value = self.config.get("cycleInterval", 15)
        return int(value) if isinstance(value, (int, float)) else 15

    @Property(str, notify=settingsChanged)
    def cycleOrder(self) -> str:
        value = self.config.get("cycleOrder", "random")
        return str(value or "random")

    @Property(str, notify=settingsChanged)
    def cyclePlaylistId(self) -> str:
        value = self.config.get("cyclePlaylistId", None)
        if not isinstance(value, str):
            return ""
        return value.strip()

    @Property(bool, notify=settingsChanged)
    def disableParallax(self) -> bool:
        return bool(self.config.get("disableParallax", False))

    @Property(bool, notify=settingsChanged)
    def disableParticles(self) -> bool:
        return bool(self.config.get("disableParticles", False))

    @Property(bool, notify=settingsChanged)
    def noFullscreenPause(self) -> bool:
        return bool(self.config.get("noFullscreenPause", False))

    @Property(bool, notify=settingsChanged)
    def disableMouse(self) -> bool:
        return bool(self.config.get("disableMouse", False))

    @Property(bool, notify=settingsChanged)
    def noAutomute(self) -> bool:
        return bool(self.config.get("noAutomute", False))

    @Property(bool, notify=settingsChanged)
    def noAudioProcessing(self) -> bool:
        return bool(self.config.get("noAudioProcessing", False))

    @Property(bool, notify=settingsChanged)
    def waylandOnlyActive(self) -> bool:
        return bool(self.config.get("waylandOnlyActive", False))

    @Property(str, notify=settingsChanged)
    def waylandIgnoreAppids(self) -> str:
        value = self.config.get("waylandIgnoreAppids", "")
        return str(value or "")

    @Property(int, notify=settingsChanged)
    def screenshotDelay(self) -> int:
        value = self.config.get("screenshotDelay", 20)
        return int(value) if isinstance(value, (int, float)) else 20

    @Property(str, notify=settingsChanged)
    def screenshotRes(self) -> str:
        value = self.config.get("screenshotRes", "3840x2160")
        return str(value or "3840x2160")

    @Property(bool, notify=settingsChanged)
    def preferXvfb(self) -> bool:
        return bool(self.config.get("preferXvfb", True))

    @Property(str, notify=settingsChanged)
    def assetsPath(self) -> str:
        value = self.config.get("assetsPath", "")
        return str(value or "")

    @Property(bool, notify=settingsChanged)
    def startHidden(self) -> bool:
        return bool(self.config.get("startHidden", False))

    @Property(bool, notify=settingsChanged)
    def autoRestore(self) -> bool:
        return bool(self.config.get("autoRestore", True))

    @Property(str, notify=appMetaChanged)
    def appVersion(self) -> str:
        return str(VERSION)

    @Property(bool, notify=appMetaChanged)
    def onboardingCompleted(self) -> bool:
        return bool(self.config.get("onboardingCompleted", False))

    @Property(list, notify=statusMessageChanged)
    def logs(self) -> list[dict[str, str]]:
        raw = self.log_manager.get_logs()
        out: list[dict[str, str]] = []
        for item in raw:
            out.append(
                {
                    "timestamp": str(item.get("timestamp", "")),
                    "level": str(item.get("level", "")),
                    "source": str(item.get("source", "")),
                    "message": str(item.get("message", "")),
                }
            )
        return out

    @Property(list, notify=historyChanged)
    def history(self) -> list[dict[str, str]]:
        raw = self.history_manager.get_all()
        out: list[dict[str, str]] = []
        for item in raw:
            out.append(
                {
                    "id": str(item.get("id", "")),
                    "title": str(item.get("title", "Unknown")),
                    "preview": _to_file_uri(str(item.get("preview", ""))),
                    "timestamp": str(item.get("timestamp", "")),
                }
            )
        return out

    @Property(list, notify=screenshotHistoryChanged)
    def screenshotHistory(self) -> list[dict[str, object]]:
        raw = self.controller.perf_monitor.get_screenshot_history()
        out: list[dict[str, object]] = []
        for record in raw:
            wp_id = str(record.get("wp_id", ""))
            wp = self.wallpaper_manager.get_wallpaper(wp_id)
            out.append(
                {
                    "wpId": wp_id,
                    "title": str(wp.get("title", "Unknown")) if wp else "Unknown",
                    "preview": _to_file_uri(str(wp.get("preview", ""))) if wp else "",
                    "outputPath": str(record.get("output_path", "")),
                    "timestamp": float(record.get("timestamp", 0.0)),
                    "duration": float(record.get("duration", 0.0)),
                }
            )
        return out

    @Property(str, notify=highlightSettingFieldChanged)
    def highlightSettingField(self) -> str:
        return self._highlight_setting_field

    @Property(bool, notify=screenshotHintActiveChanged)
    def screenshotHintActive(self) -> bool:
        return self._screenshot_hint_active

    @Property(str, notify=themeModeChanged)
    def themeMode(self) -> str:
        return self._theme_mode

    @Slot(str)
    def selectWallpaper(self, wp_id: str) -> None:
        self._selected_id = wp_id
        self.selectedIdChanged.emit()
        self.nicknameChanged.emit()
        self._set_status(f"Selected wallpaper: {wp_id}")

    @Slot(str, str)
    def setWallpaperNickname(self, wp_id: str, nickname: str) -> None:
        self.nickname_manager.set(wp_id, nickname)
        if self._selected_id == wp_id:
            self.selectedIdChanged.emit()
            self.nicknameChanged.emit()
        self._set_status("Nickname updated")

    @Slot(str)
    def copyTextToClipboard(self, text: str) -> None:
        clipboard = QGuiApplication.clipboard()
        if clipboard is None:
            self._set_status("Clipboard unavailable")
            return
        clipboard.setText(str(text or ""))
        self._set_status("Copied to clipboard")

    @Slot(str)
    def openExternalUrl(self, url: str) -> None:
        if not url:
            self._set_status("No URL to open")
            return
        ok = QDesktopServices.openUrl(QUrl(url))
        self._set_status("Opened external link" if ok else "Failed to open link")

    @Slot(str)
    def openWorkshopForWallpaper(self, wp_id: str) -> None:
        clean_id = str(wp_id or "").strip()
        if not clean_id:
            self._set_status("No wallpaper selected")
            return
        self.openExternalUrl(
            f"https://steamcommunity.com/sharedfiles/filedetails/?id={clean_id}"
        )

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
        trimmed = name.strip()
        if not trimmed:
            self._set_status("Playlist name cannot be empty")
            return

        lowered = trimmed.lower()
        for item in self.playlist_service.get_playlists():
            existing = str(item.get("name", "")).strip().lower()
            if existing == lowered:
                self._set_status("Playlist name already exists")
                return

        self.playlist_service.create_playlist(trimmed)
        self.playlistsChanged.emit()
        self._set_status(f"Created playlist: {trimmed}")

    @Slot(str, str)
    def renamePlaylist(self, playlist_id: str, name: str) -> None:
        trimmed = name.strip()
        if not trimmed:
            self._set_status("Playlist name cannot be empty")
            return

        lowered = trimmed.lower()
        for item in self.playlist_service.get_playlists():
            item_id = str(item.get("id", ""))
            existing = str(item.get("name", "")).strip().lower()
            if item_id != playlist_id and existing == lowered:
                self._set_status("Playlist name already exists")
                return

        self.playlist_service.rename_playlist(playlist_id, trimmed)
        self.playlistsChanged.emit()
        self._set_status("Playlist renamed")

    @Slot(str)
    def deletePlaylist(self, playlist_id: str) -> None:
        try:
            self.playlist_service.delete_playlist(playlist_id)
        except ValueError as exc:
            self._set_status(str(exc))
            return
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

    @Slot(bool)
    def setCycleEnabled(self, enabled: bool) -> None:
        self.config.set("cycleEnabled", bool(enabled))
        self.settingsChanged.emit()
        self._set_status(f"Cycle wallpaper {'enabled' if enabled else 'disabled'}")
        if enabled:
            self._start_cycle_timer()
        else:
            self._stop_cycle_timer()

    @Slot(int)
    def setCycleInterval(self, interval: int) -> None:
        clamped = max(1, min(1440, int(interval)))
        self.config.set("cycleInterval", clamped)
        self.settingsChanged.emit()
        self._set_status(f"Cycle interval set to {clamped} minute(s)")
        if self.cycleEnabled:
            self._start_cycle_timer()

    @Slot(str)
    def setCycleOrder(self, order: str) -> None:
        normalized = str(order or "random").strip().lower()
        if normalized not in {"random", "title", "size", "id", "type"}:
            normalized = "random"
        self.config.set("cycleOrder", normalized)
        self.settingsChanged.emit()
        self._set_status(f"Cycle order set to {normalized}")

    @Slot(str)
    def setCyclePlaylistId(self, playlist_id: str) -> None:
        normalized = str(playlist_id or "").strip()
        self.config.set("cyclePlaylistId", normalized if normalized else None)
        self.settingsChanged.emit()
        self._set_status(
            f"Cycle source set to {'all wallpapers' if not normalized else normalized}"
        )

    @Slot()
    def startCycleTimer(self) -> None:
        self._start_cycle_timer()
        self._set_status("Cycle timer started")

    @Slot()
    def stopCycleTimer(self) -> None:
        self._stop_cycle_timer()
        self._set_status("Cycle timer stopped")

    @Slot(str, result="QVariantMap")
    def takeScreenshot(self, wp_id: str) -> dict[str, object]:
        target_id = str(wp_id or self._selected_id).strip()
        if not target_id:
            self._set_status("No wallpaper selected for screenshot")
            return {"ok": False, "error": "NO_WALLPAPER"}

        save_dir = Path.home() / "Pictures" / "wallpaperengine"
        try:
            save_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            save_dir = Path("/tmp")

        output_path = (
            save_dir / f"Screenshot_{target_id}_{time.strftime('%Y%m%d_%H%M%S')}.png"
        )

        wp = self.wallpaper_manager.get_wallpaper(target_id)
        wp_type = str((wp or {}).get("type", "unknown")).lower()
        delay_cfg = self.config.get("screenshotDelay", 20)
        user_delay = int(delay_cfg) if isinstance(delay_cfg, (int, float)) else 20
        delay_frames = 5 if wp_type == "video" else user_delay

        try:
            proc, tracker = self.controller.take_screenshot(
                target_id,
                str(output_path),
                delay=delay_frames,
            )
        except Exception as exc:
            self._set_status(f"Failed to start screenshot: {exc}")
            return {"ok": False, "error": str(exc)}

        start_time = time.time()
        has_file = False
        stable_ticks = 0
        last_size = -1

        def _kill_process_group() -> None:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGINT)
            except Exception:
                try:
                    proc.terminate()
                except Exception:
                    pass

        has_xvfb = bool(self.config.get("preferXvfb", True)) and bool(
            shutil.which("xvfb-run")
        )

        timeout_s = (delay_frames / (1.0 if has_xvfb else 60.0)) + (
            20.0 if has_xvfb else 3.0
        )

        while True:
            elapsed = time.time() - start_time

            if proc.poll() is not None:
                break

            if output_path.exists():
                try:
                    current_size = output_path.stat().st_size
                except OSError:
                    current_size = -1
                if current_size > 0:
                    has_file = True
                    if current_size == last_size:
                        stable_ticks += 1
                    else:
                        stable_ticks = 0
                    last_size = current_size
                    if stable_ticks >= 2:
                        _kill_process_group()
                        break

            if elapsed > timeout_s:
                _kill_process_group()
                break

            time.sleep(0.1)

        final_exists = output_path.exists()
        final_size = output_path.stat().st_size if final_exists else 0
        if final_exists and final_size > 0:
            stats = self.controller.perf_monitor.stop_task(tracker)
            self.controller.perf_monitor.add_screenshot_history(
                target_id,
                str(output_path),
                stats,
            )
            self.screenshotHistoryChanged.emit()
            self._set_status(f"Screenshot saved: {output_path}")
            return {
                "ok": True,
                "path": str(output_path),
                "duration": float(stats.get("duration", 0.0)),
                "maxCpu": float(stats.get("max_cpu", 0.0)),
                "maxMem": float(stats.get("max_mem", 0.0)),
                "avgCpu": float(stats.get("avg_cpu", 0.0)),
                "avgMem": float(stats.get("avg_mem", 0.0)),
            }

        _ = self.controller.perf_monitor.stop_task(tracker)
        self._set_status("Screenshot failed")
        return {
            "ok": False,
            "error": "SCREENSHOT_FAILED",
            "path": str(output_path),
            "captured": bool(has_file),
        }

    @Slot(result="QVariantList")
    def getScreenshotHistory(self) -> list[dict[str, object]]:
        return self.controller.perf_monitor.get_screenshot_history()

    @Slot()
    def clearScreenshotHistory(self) -> None:
        self.controller.perf_monitor.clear_screenshot_history()
        self.screenshotHistoryChanged.emit()
        self._set_status("Screenshot history cleared")

    @Slot(bool)
    def setDisableParallax(self, disabled: bool) -> None:
        self.config.set("disableParallax", bool(disabled))
        self.settingsChanged.emit()
        self._set_status(f"Parallax {'disabled' if disabled else 'enabled'}")

    @Slot(bool)
    def setDisableParticles(self, disabled: bool) -> None:
        self.config.set("disableParticles", bool(disabled))
        self.settingsChanged.emit()
        self._set_status(f"Particles {'disabled' if disabled else 'enabled'}")

    @Slot(bool)
    def setNoFullscreenPause(self, enabled: bool) -> None:
        self.config.set("noFullscreenPause", bool(enabled))
        self.settingsChanged.emit()
        self._set_status(f"No fullscreen pause {'enabled' if enabled else 'disabled'}")

    @Slot(bool)
    def setDisableMouse(self, disabled: bool) -> None:
        self.config.set("disableMouse", bool(disabled))
        self.settingsChanged.emit()
        self._set_status(f"Mouse interaction {'disabled' if disabled else 'enabled'}")

    @Slot(bool)
    def setNoAutomute(self, enabled: bool) -> None:
        self.config.set("noAutomute", bool(enabled))
        self.settingsChanged.emit()
        self._set_status(f"Auto mute {'disabled' if enabled else 'enabled'}")

    @Slot(bool)
    def setNoAudioProcessing(self, enabled: bool) -> None:
        self.config.set("noAudioProcessing", bool(enabled))
        self.settingsChanged.emit()
        self._set_status(f"Audio processing {'disabled' if enabled else 'enabled'}")

    @Slot(bool)
    def setWaylandOnlyActive(self, enabled: bool) -> None:
        self.config.set("waylandOnlyActive", bool(enabled))
        self.settingsChanged.emit()
        self._set_status(
            f"Wayland active-only pause {'enabled' if enabled else 'disabled'}"
        )

    @Slot(str)
    def setWaylandIgnoreAppids(self, appids: str) -> None:
        cleaned = str(appids or "").strip()
        self.config.set("waylandIgnoreAppids", cleaned)
        self.settingsChanged.emit()
        self._set_status("Wayland ignore app IDs updated")

    @Slot(int)
    def setScreenshotDelay(self, delay: int) -> None:
        clamped = max(0, min(300, int(delay)))
        self.config.set("screenshotDelay", clamped)
        self.settingsChanged.emit()
        self._set_status(f"Screenshot delay set to {clamped} second(s)")

    @Slot(str)
    def setScreenshotRes(self, resolution: str) -> None:
        cleaned = str(resolution or "").strip() or "3840x2160"
        self.config.set("screenshotRes", cleaned)
        self.settingsChanged.emit()
        self._set_status(f"Screenshot resolution set to {cleaned}")

    @Slot(bool)
    def setPreferXvfb(self, enabled: bool) -> None:
        self.config.set("preferXvfb", bool(enabled))
        self.settingsChanged.emit()
        self._set_status(f"Prefer Xvfb {'enabled' if enabled else 'disabled'}")

    @Slot(str)
    def setAssetsPath(self, assets_path: str) -> None:
        cleaned = str(assets_path or "").strip()
        self.config.set("assetsPath", cleaned if cleaned else None)
        self.settingsChanged.emit()
        self._set_status("Assets path updated")

    @Slot(bool)
    def setStartHidden(self, enabled: bool) -> None:
        self.config.set("startHidden", bool(enabled))
        self.settingsChanged.emit()
        self._set_status(f"Start hidden {'enabled' if enabled else 'disabled'}")

    @Slot(bool)
    def setAutoRestore(self, enabled: bool) -> None:
        self.config.set("autoRestore", bool(enabled))
        self.settingsChanged.emit()
        self._set_status(f"Auto restore {'enabled' if enabled else 'disabled'}")

    @Slot(str, str)
    def addToPlaylist(self, playlist_id: str, wp_id: str) -> None:
        clean_playlist = str(playlist_id or "").strip()
        clean_wp = str(wp_id or "").strip()
        if not clean_playlist or not clean_wp:
            self._set_status("Playlist and wallpaper ID are required")
            return
        try:
            self.playlist_service.add_wallpaper(clean_playlist, clean_wp)
        except ValueError as exc:
            self._set_status(str(exc))
            return
        self.playlistsChanged.emit()
        self._set_status(f"Added {clean_wp} to playlist")

    @Slot(str, str)
    def removeFromPlaylist(self, playlist_id: str, wp_id: str) -> None:
        clean_playlist = str(playlist_id or "").strip()
        clean_wp = str(wp_id or "").strip()
        if not clean_playlist or not clean_wp:
            self._set_status("Playlist and wallpaper ID are required")
            return
        try:
            self.playlist_service.remove_wallpaper(clean_playlist, clean_wp)
        except ValueError as exc:
            self._set_status(str(exc))
            return
        self.playlistsChanged.emit()
        self._set_status(f"Removed {clean_wp} from playlist")

    @Slot(list)
    def reorderPlaylists(self, ordered_ids: list[str]) -> None:
        ids = [str(item) for item in ordered_ids if str(item).strip()]
        self.playlist_service.reorder_playlists(ids)
        self.playlistsChanged.emit()
        self._set_status("Playlists reordered")

    @Slot(str, str)
    def removeWallpaper(self, wp_id: str, path: str) -> None:
        clean_wp = str(wp_id or "").strip()
        clean_path = str(path or "").strip()
        if not clean_wp and clean_path:
            clean_wp = Path(clean_path).name.strip()
        if not clean_wp:
            self._set_status("Wallpaper ID is required")
            return

        if clean_path:
            expected = str(Path(self.wallpaper_manager.workshop_path) / clean_wp)
            if Path(clean_path).resolve() != Path(expected).resolve():
                self._set_status("Wallpaper path does not match wallpaper ID")
                return

        deleted = self.wallpaper_manager.delete_wallpaper(clean_wp)
        if not deleted:
            self._set_status("Failed to delete wallpaper")
            return

        self.playlist_service.remove_wallpaper_from_all(clean_wp)

        if self._selected_id == clean_wp:
            self._selected_id = ""
            self.selectedIdChanged.emit()

        self.refresh()
        self._set_status(f"Deleted wallpaper {clean_wp}")

    @Slot()
    def applyRandomWallpaper(self) -> None:
        if not self._wallpapers:
            self._set_status("No wallpapers available")
            return

        chosen = random.choice(self._wallpapers)
        wp_id = str(chosen.get("id", ""))
        if not wp_id:
            self._set_status("Failed to choose a random wallpaper")
            return

        self._selected_id = wp_id
        self.selectedIdChanged.emit()
        self.applyWallpaper(wp_id)

    @Slot(str)
    def openFolder(self, path: str) -> None:
        clean = str(path or "").strip()
        if not clean:
            self._set_status("No path to open")
            return
        self.openExternalUrl(QUrl.fromLocalFile(clean).toString())

    @Slot()
    def clearHistory(self) -> None:
        self.history_manager.clear()
        self.historyChanged.emit()
        self._set_status("History cleared")

    @Slot()
    def completeOnboarding(self) -> None:
        self.config.set("onboardingCompleted", True)
        self.appMetaChanged.emit()
        self._set_status("Onboarding completed")

    @Slot()
    def saveSettings(self) -> None:
        self.config.save()
        self._set_status("Settings saved")

    @Slot()
    def restartWallpapers(self) -> None:
        self.controller.restart_wallpapers()
        self.activeMonitorsChanged.emit()
        self._set_status("Wallpapers restarted with updated settings")

    @Slot(str)
    def setHighlightSettingField(self, field_name: str) -> None:
        self._highlight_setting_field = str(field_name or "")
        self.highlightSettingFieldChanged.emit()

    @Slot(bool)
    def setScreenshotHintActive(self, active: bool) -> None:
        self._screenshot_hint_active = bool(active)
        self.screenshotHintActiveChanged.emit()

    @Slot(str)
    def setThemeMode(self, mode: str) -> None:
        valid = {"dark", "light", "system"}
        m = str(mode or "dark").strip()
        if m not in valid:
            m = "dark"
        self._theme_mode = m
        self.config.set("themeMode", m)
        self.themeModeChanged.emit()

    @Slot(result="QVariantMap")
    def checkForUpdates(self) -> dict[str, object]:
        result: dict[str, object] = {
            "hasUpdate": False,
            "latestVersion": "",
            "downloadUrl": "",
            "error": "",
        }

        done = {"ok": False}

        def _cb(latest: Optional[str], url: Optional[str], has_update: bool) -> None:
            result["hasUpdate"] = bool(has_update)
            result["latestVersion"] = str(latest or "")
            result["downloadUrl"] = str(url or "")
            if isinstance(latest, str) and latest.startswith("ERROR:"):
                result["error"] = latest
            done["ok"] = True

        self.update_checker.check_update(str(VERSION), _cb)

        import time

        deadline = time.time() + 6.0
        while not done["ok"] and time.time() < deadline:
            time.sleep(0.02)

        if not done["ok"]:
            result["error"] = "TIMEOUT"
            self._set_status("Update check timed out")
            return result

        if result["error"]:
            self._set_status("Update check failed")
        elif bool(result["hasUpdate"]):
            self._set_status("Update available")
        else:
            self._set_status("Already up to date")
        return result

    @Slot()
    def clearLogs(self) -> None:
        self.log_manager.clear()
        self._set_status("Logs cleared")

    @Slot(result="QVariantList")
    def getLogs(self) -> list[dict[str, str]]:
        raw = self.log_manager.get_logs()
        out: list[dict[str, str]] = []
        for item in raw:
            out.append(
                {
                    "timestamp": str(item.get("timestamp", "")),
                    "level": str(item.get("level", "")),
                    "source": str(item.get("source", "")),
                    "message": str(item.get("message", "")),
                }
            )
        return out

    @Slot()
    def restartApp(self) -> None:
        self._set_status("Restarting application...")

        try:
            self.controller.stop()
        except Exception:
            pass

        argv = [str(arg) for arg in QCoreApplication.arguments()]
        if not argv:
            argv = [sys.argv[0] if sys.argv else ""]

        filtered_args = [
            arg for arg in argv[1:] if arg not in ("--hidden", "--minimized")
        ]

        appimage_path = os.environ.get("APPIMAGE", "").strip()
        if appimage_path:
            program = appimage_path
            launch_args = filtered_args
            workdir = str(Path.home())
        else:
            app_path = QCoreApplication.applicationFilePath().strip()
            script_entry = Path(sys.argv[0]).resolve() if sys.argv else None
            if app_path and Path(app_path).resolve() != Path(sys.executable).resolve():
                program = app_path
                launch_args = filtered_args
            else:
                program = sys.executable
                if script_entry is not None:
                    launch_args = [str(script_entry)] + filtered_args
                else:
                    launch_args = filtered_args
            workdir = str(Path.home())

        ok = self._start_detached(program, launch_args, workdir)
        if ok:
            QCoreApplication.quit()
            return

        self._set_status("Failed to restart application")

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
                self.historyChanged.emit()
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
            self.historyChanged.emit()
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
        if self.cycleEnabled:
            self._start_cycle_timer()

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
