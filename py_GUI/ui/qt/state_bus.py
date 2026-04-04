from __future__ import annotations

import inspect
from collections import defaultdict
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, Signal


class QtAppStateSignals(QObject):
    configChanged = Signal(str)
    stateChanged = Signal(str)
    historyChanged = Signal(str)
    screenshotHistoryChanged = Signal(str)
    playlistsChanged = Signal(str)


class QtAppStateBus:
    _ALIASES: dict[str, str] = {
        "config-changed": "config-changed",
        "configChanged": "config-changed",
        "state-changed": "state-changed",
        "stateChanged": "state-changed",
        "history-changed": "history-changed",
        "historyChanged": "history-changed",
        "screenshot-history-changed": "screenshot-history-changed",
        "screenshotHistoryChanged": "screenshot-history-changed",
        "playlists-changed": "playlists-changed",
        "playlistsChanged": "playlists-changed",
    }

    def __init__(self):
        self.signals = QtAppStateSignals()
        self._callbacks: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def emit(self, event_name: str, reason: str = "updated") -> bool:
        key = self._ALIASES.get(event_name)
        if key is None:
            return False

        for callback in list(self._callbacks.get(key, [])):
            self._call_callback(callback, reason)

        self._emit_qt_signal(key, reason)
        return True

    def connect(self, event_name: str, callback: Callable[..., Any]) -> bool:
        key = self._ALIASES.get(event_name)
        if key is None:
            return False
        if callback not in self._callbacks[key]:
            self._callbacks[key].append(callback)
        return True

    def disconnect(self, event_name: str, callback: Callable[..., Any]) -> bool:
        key = self._ALIASES.get(event_name)
        if key is None:
            return False
        callbacks = self._callbacks.get(key)
        if callbacks is None:
            return False
        try:
            callbacks.remove(callback)
            return True
        except ValueError:
            return False

    def _emit_qt_signal(self, key: str, reason: str) -> None:
        if key == "config-changed":
            self.signals.configChanged.emit(reason)
        elif key == "state-changed":
            self.signals.stateChanged.emit(reason)
        elif key == "history-changed":
            self.signals.historyChanged.emit(reason)
        elif key == "screenshot-history-changed":
            self.signals.screenshotHistoryChanged.emit(reason)
        elif key == "playlists-changed":
            self.signals.playlistsChanged.emit(reason)

    def _call_callback(self, callback: Callable[..., Any], reason: str) -> None:
        try:
            argc = self._count_positional_args(callback)
        except (TypeError, ValueError):
            callback(self, reason)
            return

        if argc >= 2:
            callback(self, reason)
        elif argc == 1:
            callback(reason)
        else:
            callback()

    def _count_positional_args(self, callback: Callable[..., Any]) -> int:
        params = list(inspect.signature(callback).parameters.values())
        count = 0
        for param in params:
            if param.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            ):
                count += 1
            elif param.kind == inspect.Parameter.VAR_POSITIONAL:
                return 2
        return count
