import os
import json
from typing import Dict
from py_GUI.const import CONFIG_DIR, CONFIG_FILE, DEFAULT_CONFIG

class ConfigManager:
    def __init__(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        self.config = self.load()

    def load(self) -> Dict:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    cfg = json.load(f)
                    return {**DEFAULT_CONFIG, **cfg}
            except:
                pass
        return DEFAULT_CONFIG.copy()

    def save(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default=None):
        return self.config.get(key, default)

    def set(self, key: str, value):
        self.config[key] = value
        self.save()
