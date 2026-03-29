import os
from typing import Any
from py_GUI.const import CONFIG_DIR
from py_GUI.core.schema import (
    CONFIG_ALIASES_TO_INTERNAL,
    CONFIG_INTERNAL_TO_EXTERNAL,
    DEFAULT_CONFIG,
)
from py_GUI.core.storage import read_config, write_config


class ConfigManager:
    def __init__(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        self.config = self.load()

    def _normalize_key(self, key: str) -> str:
        return CONFIG_ALIASES_TO_INTERNAL.get(key, key)

    def load(self) -> dict[str, Any]:
        cfg = read_config()
        normalized: dict[str, Any] = dict(DEFAULT_CONFIG)
        for key, value in cfg.items():
            normalized[self._normalize_key(key)] = value
        return normalized

    def save(self):
        payload: dict[str, Any] = {}
        for key, value in self.config.items():
            ext_key = CONFIG_INTERNAL_TO_EXTERNAL.get(key, key)
            payload[ext_key] = value
        write_config(payload)

    def get(self, key: str, default=None):
        val = self.config.get(self._normalize_key(key))
        return val if val is not None else default

    def set(self, key: str, value):
        self.config[self._normalize_key(key)] = value
        self.save()
