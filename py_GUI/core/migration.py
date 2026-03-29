from __future__ import annotations

import json
import os
import shutil
from datetime import datetime
from typing import Any, Callable

from py_GUI.const import (
    CONFIG_DIR,
    CONFIG_FILE,
    HISTORY_FILE,
    SCREENSHOT_HISTORY_FILE,
    STATE_FILE,
)
from py_GUI.core.schema import (
    DEFAULT_CONFIG,
    DEFAULT_STATE,
    RUNTIME_KEYS,
    SCREENSHOT_HISTORY_KEY,
)
from py_GUI.core.storage import (
    read_config,
    read_history,
    read_screenshot_history,
    read_state,
    write_config,
    write_history,
    write_screenshot_history,
    write_state,
)
from py_GUI.core.schema import CONFIG_ALIASES_TO_INTERNAL


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def _backup(path: str) -> str:
    backup_path = f"{path}.bak.{_timestamp()}"
    shutil.copy2(path, backup_path)
    return backup_path


def _is_valid_json_file(path: str) -> bool:
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except (OSError, json.JSONDecodeError):
        return False


def _new_layout_ready() -> bool:
    return all(
        _is_valid_json_file(p)
        for p in (CONFIG_FILE, STATE_FILE, HISTORY_FILE, SCREENSHOT_HISTORY_FILE)
    )


def _file_exists(path: str) -> bool:
    return os.path.exists(path)


def _any_new_layout_file_exists() -> bool:
    return any(
        _file_exists(p)
        for p in (CONFIG_FILE, STATE_FILE, HISTORY_FILE, SCREENSHOT_HISTORY_FILE)
    )


def _legacy_backup_exists() -> bool:
    try:
        for name in os.listdir(CONFIG_DIR):
            if name.startswith("config.json.bak."):
                return True
    except OSError:
        return False
    return False


def _sanitize_screenshot_record(item: Any) -> dict[str, Any] | None:
    if not isinstance(item, dict):
        return None
    try:
        return {
            "timestamp": float(item.get("timestamp", 0)),
            "wp_id": str(item.get("wp_id", item.get("wpId", ""))),
            "output_path": str(item.get("output_path", item.get("outputPath", ""))),
            "duration": float(item.get("duration", 0)),
            "max_cpu": float(item.get("max_cpu", item.get("maxCpu", 0))),
            "max_mem": float(item.get("max_mem", item.get("maxMem", 0))),
            "avg_cpu": float(item.get("avg_cpu", item.get("avgCpu", 0))),
            "avg_mem": float(item.get("avg_mem", item.get("avgMem", 0))),
        }
    except (TypeError, ValueError):
        return None


class StorageMigrationManager:
    def __init__(
        self,
        log_info: Callable[[str, str], None] | None = None,
        log_error: Callable[[str, str], None] | None = None,
    ):
        self.log_info: Callable[[str, str], None] = log_info or (
            lambda _message, _source: None
        )
        self.log_error: Callable[[str, str], None] = log_error or (
            lambda _message, _source: None
        )

    def migrate_if_needed(self) -> None:
        if _new_layout_ready():
            _ = self.log_info("New 4-file layout detected, skip migration", "Migration")
            return

        if _any_new_layout_file_exists():
            _ = self.log_info(
                "Partial 4-file layout detected; only healing missing/invalid files",
                "Migration",
            )
            self._ensure_missing_files()
            return

        if not os.path.exists(CONFIG_FILE):
            _ = self.log_info(
                "No legacy config.json found; skip auto-import for non-legacy layouts",
                "Migration",
            )
            self._ensure_missing_files()
            return

        if _legacy_backup_exists():
            _ = self.log_info(
                "Legacy backup exists; treat as migrated and only heal missing files",
                "Migration",
            )
            self._ensure_missing_files()
            return

        if not _is_valid_json_file(CONFIG_FILE):
            _ = self.log_error(
                "Legacy config.json is invalid JSON, fallback to defaults", "Migration"
            )
            self._ensure_missing_files()
            return

        self._migrate_legacy_config()

    def _ensure_missing_files(self) -> None:
        if not os.path.exists(CONFIG_FILE) or not _is_valid_json_file(CONFIG_FILE):
            write_config(read_config())
        if not os.path.exists(STATE_FILE) or not _is_valid_json_file(STATE_FILE):
            write_state(read_state())
        if not os.path.exists(HISTORY_FILE):
            write_history([])
        elif not _is_valid_json_file(HISTORY_FILE):
            try:
                _ = _backup(HISTORY_FILE)
            except OSError:
                pass
            write_history([])
        if not os.path.exists(SCREENSHOT_HISTORY_FILE) or not _is_valid_json_file(
            SCREENSHOT_HISTORY_FILE
        ):
            write_screenshot_history(read_screenshot_history())

    def _migrate_legacy_config(self) -> None:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            legacy = json.load(f)
        if not isinstance(legacy, dict):
            legacy = {}

        with open(CONFIG_FILE, "r", encoding="utf-8") as _raw_f:
            original_legacy_blob = _raw_f.read()

        backup_path = _backup(CONFIG_FILE)
        _ = self.log_info(f"Legacy config backup created: {backup_path}", "Migration")

        old_config = read_config()
        old_state = read_state()
        old_history = read_history()
        old_screenshot_history = read_screenshot_history()

        state_payload: dict[str, Any] = dict(DEFAULT_STATE)
        state_payload["active_monitors"] = (
            legacy.get("active_monitors", legacy.get("activeMonitors", {})) or {}
        )
        state_payload["lastWallpaper"] = legacy.get("lastWallpaper")
        state_payload["lastScreen"] = legacy.get("lastScreen")

        screenshot_payload_raw = legacy.get(SCREENSHOT_HISTORY_KEY, [])
        if not isinstance(screenshot_payload_raw, list):
            screenshot_payload_raw = []
        screenshot_payload: list[dict[str, Any]] = []
        for x in screenshot_payload_raw:
            rec = _sanitize_screenshot_record(x)
            if rec is not None:
                screenshot_payload.append(rec)

        normalized_legacy: dict[str, Any] = {}
        for k, v in legacy.items():
            nk = CONFIG_ALIASES_TO_INTERNAL.get(k, k)
            if isinstance(nk, str):
                normalized_legacy[nk] = v

        config_payload = {**DEFAULT_CONFIG, **normalized_legacy}
        for k in list(config_payload.keys()):
            if k in RUNTIME_KEYS or k == SCREENSHOT_HISTORY_KEY:
                config_payload.pop(k, None)

        history_exists = os.path.exists(HISTORY_FILE)
        history_valid = _is_valid_json_file(HISTORY_FILE)

        try:
            write_state(state_payload)
            write_screenshot_history(screenshot_payload)
            write_config(config_payload)

            if not history_exists:
                write_history([])
            elif not history_valid:
                hist_backup = _backup(HISTORY_FILE)
                _ = self.log_error(
                    f"Invalid history.json backed up: {hist_backup}", "Migration"
                )
                write_history([])
            else:
                _ = read_history()

            _ = self.log_info("Legacy config migration completed", "Migration")
        except Exception as e:
            _ = self.log_error(f"Migration failed, rolling back: {e}", "Migration")
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    f.write(original_legacy_blob)
            except OSError:
                write_config(old_config)
            write_state(old_state)
            write_history(old_history)
            write_screenshot_history(old_screenshot_history)
            raise
