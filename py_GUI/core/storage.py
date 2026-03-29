from __future__ import annotations

import json
import os

from py_GUI.const import (
    CONFIG_DIR,
    CONFIG_FILE,
    HISTORY_FILE,
    SCREENSHOT_HISTORY_FILE,
    STATE_FILE,
)
from py_GUI.core.schema import DEFAULT_CONFIG, DEFAULT_STATE


def _ensure_dir() -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)


def _atomic_write_json(path: str, data: object) -> None:
    _ensure_dir()
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, path)


def _read_json(path: str, fallback: object) -> object:
    if not os.path.exists(path):
        return fallback
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return fallback


def read_config() -> dict[str, Any]:
    data = _read_json(CONFIG_FILE, {})
    if not isinstance(data, dict):
        data = {}
    return {**DEFAULT_CONFIG, **data}


def write_config(data: dict[str, Any]) -> None:
    _atomic_write_json(CONFIG_FILE, data)


def read_state() -> dict[str, Any]:
    data = _read_json(STATE_FILE, {})
    if not isinstance(data, dict):
        data = {}
    merged = {**DEFAULT_STATE, **data}
    if not isinstance(merged.get("active_monitors"), dict):
        merged["active_monitors"] = {}
    return merged


def write_state(data: dict[str, Any]) -> None:
    _atomic_write_json(STATE_FILE, data)


def read_history() -> list[dict[str, Any]]:
    data = _read_json(HISTORY_FILE, [])
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def write_history(data: list[dict[str, Any]]) -> None:
    _atomic_write_json(HISTORY_FILE, data)


def read_screenshot_history() -> list[dict[str, Any]]:
    data = _read_json(SCREENSHOT_HISTORY_FILE, [])
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def write_screenshot_history(data: list[dict[str, Any]]) -> None:
    _atomic_write_json(SCREENSHOT_HISTORY_FILE, data)
