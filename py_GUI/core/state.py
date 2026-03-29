from __future__ import annotations

from typing import Any

import gi

gi.require_version("GObject", "2.0")
from gi.repository import GObject

from py_GUI.core.storage import read_state, write_state


class AppStateBus(GObject.Object):
    __gsignals__ = {
        "config-changed": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        "state-changed": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        "history-changed": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        "screenshot-history-changed": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        "playlists-changed": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }


class StateManager:
    def __init__(self, bus: AppStateBus | None = None):
        self._bus = bus

    def _emit(self, reason: str = "updated") -> None:
        if self._bus:
            _ = self._bus.emit("state-changed", reason)

    def get_all(self) -> dict[str, Any]:
        return read_state()

    def get(self, key: str, default: Any = None) -> Any:
        return read_state().get(key, default)

    def set(self, key: str, value: Any) -> None:
        state = read_state()
        state[key] = value
        write_state(state)
        self._emit(key)

    def get_active_monitors(self) -> dict[str, str | None]:
        monitors = self.get("active_monitors", {})
        return dict(monitors) if isinstance(monitors, dict) else {}

    def set_active_monitors(self, value: dict[str, str | None]) -> None:
        self.set("active_monitors", dict(value))

    def clear_active_monitors(self) -> None:
        self.set("active_monitors", {})

    def get_last_wallpaper(self) -> str | None:
        val = self.get("lastWallpaper")
        return val if isinstance(val, str) or val is None else None

    def set_last_wallpaper(self, wp_id: str | None) -> None:
        self.set("lastWallpaper", wp_id)

    def get_last_screen(self) -> str | None:
        val = self.get("lastScreen")
        return val if isinstance(val, str) or val is None else None

    def set_last_screen(self, screen: str | None) -> None:
        self.set("lastScreen", screen)
