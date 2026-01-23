#!/usr/bin/env python3
"""
Linux Wallpaper Engine GUI
A modern GTK4/Libadwaita GUI for linux-wallpaperengine
Inspired by linux-wallpaperengine-gui (Electron version)
"""

import os
import sys
import json
import subprocess
import webbrowser
import gc
import random
import threading
import os.path
from datetime import datetime



from typing import Optional, Dict, List, Any

# 托盘库需要在 GTK 前导入，以便使用合适的后端
try:
    os.environ['PYSTRAY_BACKEND'] = 'dbus'  # 强制使用 D-Bus 后端（避免 GTK 3 冲突）
    import pystray
    from PIL import Image
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GdkPixbuf, Gdk, GLib, Pango

# ============================================================================
# 配置
# ============================================================================
CONFIG_DIR = os.path.expanduser("~/.config/linux-wallpaperengine-gui")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
WORKSHOP_PATH = os.path.expanduser("~/.local/share/Steam/steamapps/workshop/content/431960")

DEFAULT_CONFIG = {
    "fps": 30,
    "volume": 0,
    "scaling": "default",
    "silence": True,
    "noFullscreenPause": False,
    "disableMouse": False,
    "lastWallpaper": None,
    "lastScreen": None,
    "wallpaperProperties": {},
}

# ============================================================================
# CSS 样式 - 模仿 linux-wallpaperengine-gui 的现代深色主题
# ============================================================================
CSS_STYLE = """
/* Global */
window {
    background-color: #1d1d1d;
}

/* Top navigation bar */
.nav-bar {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 12px;
    padding: 6px;
    margin: 10px 20px;
}

.nav-btn {
    background: #2a2a2a;
    color: rgba(255,255,255,0.87);
    border-radius: 10px;
    padding: 8px 16px;
    font-weight: 600;
    border: none;
    min-height: 36px;
    transition: all 0.2s;
}

.nav-btn:hover {
    background: #464646;
}

.nav-btn.active, .nav-btn:checked {
    background: #007bff;
    color: white;
    box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

/* Toolbar */
.toolbar {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 20px;
    padding: 10px 15px;
    margin: 0 20px 10px 20px;
}

.status-label {
    color: rgba(255,255,255,0.4);
    font-weight: 600;
    font-size: 0.85em;
    letter-spacing: 0.5px;
}

.status-value {
    color: #007bff;
    font-weight: 700;
    text-transform: uppercase;
}

.mode-btn {
    background: #2a2a2a;
    color: rgba(255,255,255,0.87);
    border-radius: 10px;
    padding: 8px 12px;
    border: none;
    min-height: 32px;
}

.mode-btn:hover {
    background: #464646;
}

.mode-btn.active, .mode-btn:checked {
    background: #007bff;
    color: white;
}

/* Wallpaper card - Grid view */
.wallpaper-card {
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.wallpaper-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
}

.wallpaper-item {
    background: rgba(66, 66, 66, 0.5);
    border-radius: 5px;
    border: 3px solid transparent;
    transition: all 0.2s ease-out;
    padding: 0;
}

.wallpaper-item:hover {
    border-color: rgba(0, 123, 255, 0.5);
    box-shadow: 0 0 15px rgba(0, 123, 255, 0.7);
}

.wallpaper-item.selected {
    border-color: #007bff;
    box-shadow: 0 0 15px rgba(0, 123, 255, 0.7);
}

.wallpaper-name {
    background: black;
    border-radius: 10px;
    border: 2px solid #007bff;
    padding: 5px 10px;
    font-weight: 400;
    font-size: 0.9em;
}

/* Wallpaper list - List view */
.list-item {
    background: rgba(61, 61, 61, 0.4);
    border-radius: 12px;
    border: 2px solid transparent;
    padding: 12px;
    margin: 5px 0;
    transition: all 0.2s;
}

.list-item:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.15);
}

.list-item.selected {
    border-color: #007bff;
    background: rgba(0, 123, 255, 0.1);
}

.list-title {
    font-weight: 600;
    font-size: 1.1em;
}

.list-type {
    color: #7dd3fc;
    font-size: 0.85em;
}

.list-tags {
    color: #fbbf24;
    font-size: 0.85em;
}

.list-folder {
    color: #86efac;
    font-size: 0.85em;
}

/* Sidebar */
.sidebar {
    background: #2a2a2a;
    border-radius: 15px;
    margin: 20px;
    margin-left: 0;
    box-shadow: -5px 0 15px rgba(0, 0, 0, 0.3);
    min-width: 320px;
    max-width: 320px;
    width: 320px;
}

.sidebar-preview {
    border-radius: 10px;
    margin: 20px;
}

.sidebar-title {
    font-size: 1.3em;
    font-weight: bold;
    margin: 0 20px;
}

.sidebar-subtitle {
    color: rgba(255,255,255,0.6);
    font-size: 0.9em;
    margin: 5px 20px;
}

.sidebar-section {
    font-weight: 600;
    font-size: 0.9em;
    color: rgba(255,255,255,0.6);
    margin: 15px 20px 5px 20px;
    padding-bottom: 5px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

.sidebar-desc {
    font-size: 0.9em;
    color: rgba(255,255,255,0.8);
    margin: 0 20px;
    line-height: 1.4;
}

.tag-chip {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 4px 12px;
    font-size: 0.85em;
    margin: 2px;
}

.sidebar-btn {
    background: #007bff;
    color: white;
    border-radius: 25px;
    font-weight: bold;
    padding: 10px 20px;
    border: none;
    margin: 10px 20px;
}

.sidebar-btn:hover {
    background: #53a6ff;
}

.sidebar-btn.secondary {
    background: transparent;
    border: 1px solid rgba(255,255,255,0.2);
}

.sidebar-btn.secondary:hover {
    background: rgba(255,255,255,0.1);
}

/* Settings page */
.settings-container {
    background: rgba(20, 20, 20, 0.5);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    margin: 20px;
}

.settings-sidebar {
    background: rgba(20, 20, 20, 0.6);
    border-right: 1px solid rgba(255,255,255,0.08);
    padding: 32px 16px;
}

.settings-header {
    font-size: 1.5em;
    font-weight: 800;
    margin-bottom: 8px;
}

.settings-subheader {
    color: rgba(255,255,255,0.4);
    font-size: 0.85em;
}

.settings-nav-item {
    background: transparent;
    color: rgba(255,255,255,0.4);
    border-radius: 10px;
    padding: 12px 16px;
    font-weight: 500;
    border: none;
}

.settings-nav-item:hover {
    background: rgba(255,255,255,0.15);
    color: rgba(255,255,255,0.87);
}

.settings-nav-item.active, .settings-nav-item:checked {
    background: #007bff;
    color: white;
    box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.settings-section-title {
    font-size: 1.4em;
    font-weight: 700;
    margin-bottom: 8px;
}

.settings-section-desc {
    color: rgba(255,255,255,0.5);
    font-size: 0.9em;
    margin-bottom: 20px;
}

.setting-row {
    background: rgba(61, 61, 61, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
}

.setting-label {
    font-weight: 500;
}

.setting-desc {
    color: rgba(255,255,255,0.5);
    font-size: 0.85em;
}

.action-btn {
    border-radius: 10px;
    padding: 12px;
    font-weight: 600;
    border: none;
}

.action-btn.primary {
    background: #007bff;
    color: white;
}

.action-btn.primary:hover {
    background: #53a6ff;
}

.action-btn.secondary {
    background: rgba(61, 61, 61, 0.4);
    border: 1px solid rgba(255,255,255,0.08);
}

.action-btn.secondary:hover {
    background: rgba(255,255,255,0.15);
}

.action-btn.danger {
    background: transparent;
    color: #ef4444;
}

.action-btn.danger:hover {
    background: rgba(255, 77, 77, 0.1);
}

/* Scrollbar */
scrollbar {
    background: transparent;
}

scrollbar slider {
    background: #007bff;
    border-radius: 9999px;
    min-width: 6px;
    min-height: 6px;
}

scrollbar slider:hover {
    background: #53a6ff;
}

/* Common */
.text-muted {
    color: rgba(255,255,255,0.4);
}

.card {
    border-radius: 12px;
}

spinbutton {
    background: rgba(61, 61, 61, 0.4);
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.08);
}

entry {
    background: rgba(61, 61, 61, 0.4);
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 8px 12px;
}

switch {
    background: rgba(61, 61, 61, 0.6);
}

switch:checked {
    background: #007bff;
}

dropdown button {
    background: rgba(61, 61, 61, 0.4);
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.08);
}
"""

# ============================================================================
# 配置管理
# ============================================================================
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


# ============================================================================
# 壁纸数据管理（带内存优化）
# ============================================================================
class WallpaperManager:
    def __init__(self, workshop_path: str = WORKSHOP_PATH):
        self.workshop_path = workshop_path
        self._wallpapers: Dict[str, Dict] = {}
        self._texture_cache: Dict[str, Gdk.Texture] = {}
        self._cache_max_size = 80  # 限制缓存数量

    def scan(self) -> Dict[str, Dict]:
        """扫描壁纸目录"""
        self._wallpapers.clear()
        if not os.path.exists(self.workshop_path):
            return self._wallpapers

        for folder in sorted(os.listdir(self.workshop_path)):
            json_path = os.path.join(self.workshop_path, folder, "project.json")
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r') as f:
                        data = json.load(f)
                        preview_file = data.get("preview", "preview.jpg")
                        self._wallpapers[folder] = {
                            "id": folder,
                            "title": data.get("title", "Unknown"),
                            "preview": os.path.join(self.workshop_path, folder, preview_file),
                            "description": data.get("description", ""),
                            "type": data.get("type", "Scene"),
                            "tags": data.get("tags", []),
                            "file": data.get("file", ""),
                            "contentrating": data.get("contentrating", ""),
                            "version": data.get("version", ""),
                        }
                except:
                    pass
        return self._wallpapers

    def get_texture(self, path: str, size: int = 170) -> Optional[Gdk.Texture]:
        """获取缩略图纹理（带LRU缓存）"""
        cache_key = f"{path}_{size}"
        if cache_key in self._texture_cache:
            return self._texture_cache[cache_key]

        if not os.path.exists(path):
            return None

        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, size, size, True)
            texture = Gdk.Texture.new_for_pixbuf(pixbuf)
            del pixbuf  # 立即释放 pixbuf

            # LRU缓存：超过限制时清除一半
            if len(self._texture_cache) >= self._cache_max_size:
                keys = list(self._texture_cache.keys())[:self._cache_max_size // 2]
                for k in keys:
                    del self._texture_cache[k]
                gc.collect()

            self._texture_cache[cache_key] = texture
            return texture
        except:
            return None

    def clear_cache(self):
        """清空纹理缓存"""
        self._texture_cache.clear()

    def delete_wallpaper(self, folder_id: str) -> bool:
        """删除壁纸文件夹"""
        if folder_id not in self._wallpapers:
            return False

        folder_path = os.path.join(self.workshop_path, folder_id)
        if not os.path.exists(folder_path):
            return False

        try:
            # 删除文件夹及其内容
            import shutil
            shutil.rmtree(folder_path)

            # 从壁纸列表中移除
            del self._wallpapers[folder_id]

            # 清理缓存
            cache_keys_to_remove = [k for k in self._texture_cache.keys() if k.startswith(self._wallpapers.get(folder_id, {}).get('preview', ''))]
            for key in cache_keys_to_remove:
                del self._texture_cache[key]

            return True
        except Exception as e:
            print(f"[ERROR] Failed to delete wallpaper {folder_id}: {e}")
            return False
        gc.collect()


# ============================================================================
# 屏幕管理
# ============================================================================
class ScreenManager:
    def __init__(self):
        self._screens_cache: Optional[List[str]] = None

    def get_screens(self) -> List[str]:
        """获取可用的屏幕列表"""
        if self._screens_cache is not None:
            return self._screens_cache

        screens = []
        try:
            result = subprocess.run(
                ['xrandr', '--query'],
                capture_output=True,
                text=True,
                timeout=5
            )
            for line in result.stdout.split('\n'):
                if ' connected' in line:
                    screen_name = line.split()[0]
                    screens.append(screen_name)
        except Exception as e:
            print(f"[SCREEN] Failed to get screens: {e}")
            screens = ['eDP-1']  # 默认值

        self._screens_cache = screens
        return screens

    def refresh(self):
        """刷新屏幕列表"""
        self._screens_cache = None
        return self.get_screens()

# ============================================================================
# 壁纸属性管理
# ============================================================================
class PropertiesManager:
    def __init__(self, config: ConfigManager):
        self._properties_cache: Dict[str, List[Dict]] = {}
        self._property_types: Dict[str, Dict[str, str]] = {}
        self._user_properties: Dict[str, Dict] = {}
        self._config = config
        self.load_from_config()

    def parse_properties_output(self, output: str) -> List[Dict]:
        """解析 --list-properties 输出"""
        properties = []
        lines = output.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or 'Running with:' in line:
                i += 1
                continue

            if ' - ' in line:
                parts = line.split(' - ', 1)
                name = parts[0].strip()
                prop_type = parts[1].strip()

                prop = {
                    'name': name,
                    'type': prop_type,
                    'text': '',
                    'value': None,
                    'min': 0,
                    'max': 100,
                    'step': 1,
                    'options': []
                }

                i += 1
                while i < len(lines):
                    subline = lines[i].strip()
                    if not subline:
                        i += 1
                        continue
                    if ' - ' in subline:
                        i -= 1
                        break

                    if subline.startswith('Text:'):
                        prop['text'] = subline[5:].strip()
                    elif subline.startswith('Value:'):
                        value_str = subline[6:].strip()
                        if prop_type == 'color':
                            prop['value'] = self._parse_color(value_str)
                        elif prop_type == 'boolean':
                            prop['value'] = value_str == '1'
                        else:
                            try:
                                prop['value'] = float(value_str)
                                if prop['value'] == int(prop['value']):
                                    prop['value'] = int(prop['value'])
                            except:
                                prop['value'] = value_str
                    elif subline.startswith('Min:'):
                        prop['min'] = float(subline[4:].strip())
                    elif subline.startswith('Max:'):
                        prop['max'] = float(subline[5:].strip())
                    elif subline.startswith('Step:'):
                        prop['step'] = float(subline[5:].strip())
                    elif subline.startswith('Values:'):
                        i += 1
                        while i < len(lines) and '\t\t' in lines[i]:
                            opt_line = lines[i].strip()
                            if '=' in opt_line:
                                label, val = opt_line.split('=', 1)
                                prop['options'].append({'label': label.strip(), 'value': val.strip()})
                            i += 1
                        continue

                    i += 1
                properties.append(prop)
            else:
                i += 1
        return properties

    def _parse_color(self, value_str: str) -> tuple:
        """解析颜色值"""
        parts = [p.strip() for p in value_str.split(',')]
        return (float(parts[0]), float(parts[1]), float(parts[2]))

    def get_properties(self, wp_id: str) -> List[Dict]:
        """获取壁纸属性列表"""
        if wp_id in self._properties_cache:
            return self._properties_cache[wp_id]

        try:
            result = subprocess.run(
                ['linux-wallpaperengine', '--list-properties', wp_id],
                capture_output=True,
                text=True,
                timeout=5
            )
            properties = self.parse_properties_output(result.stdout)

            # 过滤掉对用户无意义的属性（UI 相关等）
            properties = self._filter_properties(properties)

            self._properties_cache[wp_id] = properties
            # 存储属性类型信息
            self._property_types[wp_id] = {p['name']: p['type'] for p in properties}
            return properties
        except Exception as e:
            print(f"[PROPERTIES] Failed to get properties for {wp_id}: {e}")
            return []

    def _filter_properties(self, properties: List[Dict]) -> List[Dict]:
        """过滤掉对用户无意义的属性"""
        filtered = []
        ui_keywords = ['ui_', 'ui_browse', 'scheme_']

        # 音量相关属性（Settings 中已有全局音量控制）
        audio_keywords = ['volume', 'music', 'sound', 'bell']

        for prop in properties:
            name = prop.get('name', '').lower()
            text = prop.get('text', '').lower()

            # 检查是否包含 UI 相关关键词
            should_hide = any(keyword in name or keyword in text for keyword in ui_keywords)

            # 检查是否为音量相关属性
            is_audio_prop = any(keyword in name for keyword in audio_keywords)

            if not should_hide and not is_audio_prop:
                filtered.append(prop)
            else:
                reason = []
                if should_hide:
                    reason.append("UI-related")
                if is_audio_prop:
                    reason.append("audio-related")
                print(f"[PROPERTIES] Hiding property: {prop['name']} (text: {prop['text']}, reason: {', '.join(reason)})")

        return filtered

    def get_property_type(self, wp_id: str, prop_name: str) -> str:
        """获取属性类型"""
        if wp_id in self._property_types and prop_name in self._property_types[wp_id]:
            return self._property_types[wp_id][prop_name]
        return 'unknown'

    def load_from_config(self):
        """从配置文件加载用户属性"""
        props_data = self._config.get("wallpaperProperties", {})
        self._user_properties = props_data

    def save_to_config(self):
        """保存用户属性到配置文件"""
        self._config.set("wallpaperProperties", self._user_properties)

    def get_user_property(self, wp_id: str, prop_name: str):
        """获取用户修改的属性值"""
        if wp_id in self._user_properties and prop_name in self._user_properties[wp_id]:
            return self._user_properties[wp_id][prop_name]
        return None

    def set_user_property(self, wp_id: str, prop_name: str, value):
        """设置用户修改的属性值"""
        if wp_id not in self._user_properties:
            self._user_properties[wp_id] = {}
        self._user_properties[wp_id][prop_name] = value
        self.save_to_config()

    def format_property_value(self, prop_type: str, value) -> str:
        """格式化属性值为命令行参数格式"""
        # 修复：同时支持 tuple 和 list（JSON 加载时为 list）
        # 即使 prop_type 未知，只要是列表/元组，就格式化为逗号分隔字符串
        if isinstance(value, (tuple, list)):
            return ",".join(map(str, value))
        elif isinstance(value, bool):
            return '1' if value else '0'
        elif isinstance(value, float):
            return f"{value:.6f}"
        return str(value)

# ============================================================================
# 日志管理
# ============================================================================
class LogManager:
    def __init__(self, max_entries: int = 500):
        self._logs: List[Dict] = []
        self._max_entries = max_entries
        self._callbacks: List[callable] = []

    def add(self, level: str, message: str, source: str = "GUI"):
        """添加日志条目"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "source": source,
            "message": message
        }
        self._logs.append(log_entry)

        # 限制日志数量
        if len(self._logs) > self._max_entries:
            self._logs = self._logs[-self._max_entries:]

        # 通知监听器
        for callback in self._callbacks:
            try:
                callback(log_entry)
            except Exception as e:
                print(f"[LOG] Callback error: {e}")

    def add_debug(self, message: str, source: str = "GUI"):
        self.add("DEBUG", message, source)

    def add_info(self, message: str, source: str = "GUI"):
        self.add("INFO", message, source)

    def add_warning(self, message: str, source: str = "GUI"):
        self.add("WARNING", message, source)

    def add_error(self, message: str, source: str = "GUI"):
        self.add("ERROR", message, source)

    def get_logs(self) -> List[Dict]:
        """获取所有日志"""
        return self._logs.copy()

    def clear(self):
        """清空日志"""
        self._logs.clear()

    def register_callback(self, callback: callable):
        """注册日志更新回调"""
        self._callbacks.append(callback)

# ============================================================================
# 壁纸控制器
# ============================================================================
class WallpaperController:
    def __init__(self, config: ConfigManager, prop_manager: PropertiesManager, log_manager: LogManager):
        self.config = config
        self.prop_manager = prop_manager
        self.log_manager = log_manager
        self.current_proc: Optional[subprocess.Popen] = None

    def apply(self, wp_id: str, screen: Optional[str] = None):
        """应用壁纸"""
        self.stop()
        # 确保screen是有效字符串，避免None被转成字符串"None"
        if not screen:
            screen = self.config.get("lastScreen")
        if not screen or screen == "None":
            screen = "eDP-1"

        self.log_manager.add_info(f"Applying wallpaper {wp_id} to screen {screen}", "Controller")

        # 使用兼容旧版本的短参数格式
        cmd = [
            "linux-wallpaperengine",
            str(wp_id),  # 直接传入壁纸ID作为第一个参数
            "-r", screen,
            "-f", str(self.config.get("fps", 30)),
        ]

        if self.config.get("silence", True):
            cmd.append("--silent")
        else:
            cmd.extend(["--volume", str(self.config.get("volume", 50))])

        scaling = self.config.get("scaling", "default")
        if scaling != "default":
            cmd.extend(["--scaling", scaling])

        if self.config.get("noFullscreenPause", False):
            cmd.append("--no-fullscreen-pause")

        if self.config.get("disableMouse", False):
            cmd.append("--disable-mouse")

        # 添加用户自定义属性
        # 在静音模式下跳过音量相关属性
        is_silent = self.config.get("silence", True)
        audio_props = {'musicvolume', 'music', 'bellvolume', 'sound', 'soundsettings', 'volume'}

        user_props = self.prop_manager._user_properties.get(wp_id, {})
        self.log_manager.add_debug(f"User properties for {wp_id}: {user_props}", "Controller")
        for prop_name, prop_value in user_props.items():
            # 静音模式下跳过音量相关属性
            if is_silent and prop_name.lower() in audio_props:
                self.log_manager.add_debug(f"Skipping audio property {prop_name} in silent mode", "Controller")
                continue

            prop_type = self.prop_manager.get_property_type(wp_id, prop_name)
            formatted_value = self.prop_manager.format_property_value(prop_type, prop_value)
            cmd.extend(["--set-property", f"{prop_name}={formatted_value}"])
            self.log_manager.add_debug(f"Adding property: {prop_name}={formatted_value} (type: {prop_type})", "Controller")

        # 【调试输出】
        self.log_manager.add_debug(f"Executing: {' '.join(cmd)}", "Controller")

        try:
            self.current_proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # 检查进程是否立即退出
            import time
            time.sleep(0.5)
            if self.current_proc.poll() is not None:
                stdout, stderr = self.current_proc.communicate()
                error_msg = f"Process exited!\nSTDOUT: {stdout.decode()}\nSTDERR: {stderr.decode()}"
                self.log_manager.add_error(error_msg, "Engine")
                return

            self.config.set("lastWallpaper", wp_id)
            self.config.set("lastScreen", screen)
            self.log_manager.add_info(f"Wallpaper applied: {wp_id}", "Controller")

            # 颜色同步脚本
            colors_script = os.path.expanduser("~/niri/scripts/sync_colors.sh")
            if os.path.exists(colors_script):
                try:
                    subprocess.run([
                        "bash", colors_script
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                except Exception:
                    pass
        except Exception as e:
            self.log_manager.add_error(f"Failed to apply wallpaper: {e}", "Controller")

    def stop(self):
        """停止壁纸"""
        self.log_manager.add_info("Stopping wallpaper", "Controller")
        if self.current_proc:
            self.current_proc.terminate()
            self.current_proc = None
        subprocess.run(
            ["pkill", "-f", "linux-wallpaperengine"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )


# ============================================================================
# 主应用
# ============================================================================
class WallpaperApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='com.github.wallpaperengine.gui',
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        )
        self.config = ConfigManager()
        self.log_manager = LogManager()
        workshop_path = self.config.get("workshopPath", WORKSHOP_PATH)
        self.wp_manager = WallpaperManager(workshop_path)
        self.prop_manager = PropertiesManager(self.config)
        self.screen_manager = ScreenManager()
        self.controller = WallpaperController(self.config, self.prop_manager, self.log_manager)

        self.view_mode = "grid"  # grid, list
        self.selected_wp: Optional[str] = None
        self.active_wp: Optional[str] = None
        self.search_query = ""  # 搜索关键词

        # CLI 控制：支持 --minimized/--hidden、--show/--hide/--toggle 等
        self.start_hidden = False
        self.cli_actions: List[str] = []
        self.initialized = False
        self._is_first_activation = True

        # 托盘
        self.tray_icon = None
        self.tray_thread: Optional[threading.Thread] = None

    def do_command_line(self, command_line):
        argv = command_line.get_arguments()[1:]
        for arg in argv:
            if arg in ("--minimized", "--hidden"):
                if self.initialized:
                    self.cli_actions.append("hide")
                else:
                    self.start_hidden = True
            elif arg == "--show":
                self.cli_actions.append("show")
            elif arg == "--hide":
                self.cli_actions.append("hide")
            elif arg == "--toggle":
                self.cli_actions.append("toggle")
            elif arg == "--refresh":
                self.cli_actions.append("refresh")
            elif arg == "--apply-last":
                self.cli_actions.append("apply-last")
            elif arg == "--quit":
                self.cli_actions.append("quit")

        self.activate()
        return 0

    def do_activate(self):
        # 已初始化时仅响应 CLI 动作/显示窗口
        if self.initialized:
            # 只在首次启动时考虑 start_hidden，后续 CLI 调用不受影响
            if self._is_first_activation and not self.start_hidden:
                self.show_window()
            self._is_first_activation = False
            self.start_hidden = False
            self._is_first_activation = False
            self.consume_cli_actions()
            return

        # Load CSS
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS_STYLE.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # 创建窗口
        self.win = Adw.ApplicationWindow(application=self)
        self.win.set_title("Linux Wallpaper Engine GUI")
        self.win.set_default_size(1200, 800)
        # 固定一个下限尺寸，避免内容变化导致最小宽度抖动
        self.win.set_size_request(1000, 700)

        # 窗口关闭时隐藏而非退出（托盘支持）
        self.win.connect("close-request", self.on_window_close)

        # 主容器
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.win.set_content(main_box)

        # 顶部导航栏
        self.build_nav_bar(main_box)

        # 内容区域（Stack）
        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.content_stack.set_vexpand(True)
        main_box.append(self.content_stack)

        # 壁纸页面
        self.build_wallpapers_page()

        # 设置页面
        self.build_settings_page()

        # 加载壁纸
        self.wp_manager.scan()
        self.refresh_wallpaper_grid()

        # 恢复上次的壁纸选中状态
        last_wp = self.config.get("lastWallpaper")
        if last_wp and last_wp in self.wp_manager._wallpapers:
            self.selected_wp = last_wp
            self.active_wp = last_wp
            self.update_sidebar()
            wp = self.wp_manager._wallpapers.get(last_wp)
            if wp:
                self.active_wp_label.set_label(wp['title'])

            # 自动应用上次壁纸
            GLib.timeout_add(500, lambda: self.auto_apply_wallpaper(last_wp))

        # 启动时可选择隐藏（配合 --minimized/--hidden）
        if self.start_hidden:
            self.win.set_visible(False)
        else:
            self.win.present()
        self.start_hidden = False

        self.initialized = True
        
        # 启动托盘（如果库可用）
        if TRAY_AVAILABLE:
            self.setup_tray()
        
        self.consume_cli_actions()

    # ========================================================================
    # 顶部导航栏
    # ========================================================================
    def build_nav_bar(self, parent: Gtk.Box):
        nav_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        nav_container.set_halign(Gtk.Align.CENTER)
        nav_container.add_css_class("nav-bar")

        # Home 按钮
        self.btn_home = Gtk.ToggleButton(label="🏠 Home")
        self.btn_home.add_css_class("nav-btn")
        self.btn_home.set_active(True)
        self.btn_home.connect("toggled", self.on_nav_home)
        nav_container.append(self.btn_home)

        # Settings 按钮
        self.btn_settings = Gtk.ToggleButton(label="⚙️ Settings")
        self.btn_settings.add_css_class("nav-btn")
        self.btn_settings.connect("toggled", self.on_nav_settings)
        nav_container.append(self.btn_settings)

        # 拉伸空间
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        nav_container.append(spacer)

        parent.append(nav_container)

    def show_window(self):
        if self.win:
            self.win.set_visible(True)
            self.win.present()

    def hide_window(self):
        if self.win:
            self.win.set_visible(False)

    def toggle_window(self):
        if self.win:
            if self.win.get_visible():
                self.hide_window()
            else:
                self.show_window()

    def apply_last_from_cli(self):
        last_wp = self.config.get("lastWallpaper")
        if last_wp:
            self.controller.apply(last_wp)
            self.active_wp = last_wp
            wp = self.wp_manager._wallpapers.get(last_wp)
            if wp:
                self.active_wp_label.set_label(wp['title'])

    def refresh_from_cli(self):
        self.on_reload_wallpapers(None)

    def consume_cli_actions(self):
        if not self.cli_actions:
            return
        actions = list(self.cli_actions)
        self.cli_actions.clear()

        for action in actions:
            if action == "show":
                self.show_window()
            elif action == "hide":
                self.hide_window()
            elif action == "toggle":
                self.toggle_window()
            elif action == "refresh":
                self.refresh_from_cli()
            elif action == "apply-last":
                self.apply_last_from_cli()
            elif action == "quit":
                self.controller.stop()
                self.quit()

    def on_nav_home(self, btn):
        if btn.get_active():
            self.btn_settings.set_active(False)
            self.content_stack.set_visible_child_name("wallpapers")

    def on_nav_settings(self, btn):
        if btn.get_active():
            self.btn_home.set_active(False)
            self.content_stack.set_visible_child_name("settings")

    def on_window_close(self, win):
        """窗口关闭事件处理：隐藏而非退出（托盘支持）"""
        self.hide_window()
        return True  # 阻止默认关闭行为

    # ========================================================================
    # 托盘集成
    # ========================================================================
    def setup_tray(self):
        """在后台线程中设置托盘图标"""
        if not TRAY_AVAILABLE:
            return
        
        self.tray_thread = threading.Thread(target=self._run_tray, daemon=True)
        self.tray_thread.start()

    def _run_tray(self):
        """在独立线程中运行托盘"""
        try:
            # 创建简单的图标（蓝色圆形）
            image = self._create_tray_icon()
            
            # 菜单项
            menu = (
                pystray.MenuItem(
                    "显示/隐藏",
                    lambda: GLib.idle_add(self.toggle_window),
                    default=True
                ),
                pystray.MenuItem(
                    "刷新壁纸",
                    lambda: GLib.idle_add(self.refresh_from_cli)
                ),
                pystray.MenuItem(
                    "应用上次壁纸",
                    lambda: GLib.idle_add(self.apply_last_from_cli)
                ),
                pystray.MenuItem(
                    "退出",
                    lambda: GLib.idle_add(self._quit_from_tray)
                ),
            )
            
            # 创建托盘图标
            self.tray_icon = pystray.Icon(
                "wallpaper-engine-gui",
                image,
                "Linux Wallpaper Engine GUI",
                menu
            )
            
            # 运行托盘（阻塞，直到退出）
            self.tray_icon.run()
        except Exception as e:
            print(f"[TRAY] 启动失败: {e}")

    def _create_tray_icon(self) -> Image.Image:
        """创建托盘图标（蓝色圆形）"""
        try:
            size = 64
            image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            pixels = image.load()
            
            # 绘制蓝色圆形
            center = size // 2
            radius = size // 2 - 2
            for x in range(size):
                for y in range(size):
                    dx = x - center
                    dy = y - center
                    if dx*dx + dy*dy <= radius*radius:
                        pixels[x, y] = (0, 123, 255, 255)  # 蓝色
            
            return image
        except:
            # 降级：如果绘图失败，创建最小透明图
            return Image.new('RGBA', (64, 64), (0, 0, 0, 0))

    def _quit_from_tray(self):
        """托盘退出"""
        self.controller.stop()
        if self.tray_icon:
            self.tray_icon.stop()
        self.quit()

    # ========================================================================
    # 壁纸页面
    # ========================================================================
    def build_wallpapers_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.content_stack.add_named(page, "wallpapers")

        # 顶部工具栏 (Row 1)
        self.build_toolbar(page)

        # 主内容区（左右布局）
        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        content_box.set_vexpand(True)
        content_box.set_hexpand(True)
        page.append(content_box)

        # 左侧：状态面板 + 壁纸网格区
        left_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        left_area.set_hexpand(True)
        content_box.append(left_area)

        # 状态面板 (显示当前壁纸，仅在左侧顶部)
        self.build_status_panel(left_area)

        # 壁纸容器
        self.wallpaper_scroll = Gtk.ScrolledWindow()
        self.wallpaper_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.wallpaper_scroll.set_vexpand(True)
        left_area.append(self.wallpaper_scroll)

        # FlowBox (网格)
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_halign(Gtk.Align.CENTER)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flowbox.set_homogeneous(False)
        self.flowbox.set_row_spacing(5)
        self.flowbox.set_column_spacing(5)
        self.flowbox.set_margin_top(20)
        self.flowbox.set_margin_bottom(20)
        self.flowbox.set_margin_start(20)
        self.flowbox.set_margin_end(20)

        # ListBox (列表)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.set_margin_top(20)
        self.listbox.set_margin_bottom(20)
        self.listbox.set_margin_start(20)
        self.listbox.set_margin_end(20)

        # 默认显示网格
        self.wallpaper_scroll.set_child(self.flowbox)

        # 右侧侧边栏 (壁纸详情)
        self.build_sidebar(content_box)

    def build_toolbar(self, parent: Gtk.Box):
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        toolbar.add_css_class("toolbar")

        # 左侧搜索框
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        toolbar.append(search_box)

        search_label = Gtk.Label(label="🔍")
        search_label.add_css_class("status-label")
        search_box.append(search_label)

        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Search wallpapers...")
        self.search_entry.set_width_chars(25)
        self.search_entry.connect('changed', self.on_search_changed)
        self.search_entry.connect('activate', self.on_search_activate)
        search_box.append(self.search_entry)

        # 拉伸空间
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        toolbar.append(spacer)

        # 功能按钮组 (图标化，带Tooltip)
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        toolbar.append(actions_box)

        # Stop 按钮
        stop_btn = Gtk.Button(label="⏹")
        stop_btn.add_css_class("mode-btn")
        stop_btn.set_tooltip_text("Stop Wallpaper")
        stop_btn.connect("clicked", lambda _: self.controller.stop())
        actions_box.append(stop_btn)

        # Refresh 按钮
        refresh_btn = Gtk.Button(label="⟳")
        refresh_btn.add_css_class("mode-btn")
        refresh_btn.set_tooltip_text("Refresh Wallpapers")
        refresh_btn.connect("clicked", self.on_reload_wallpapers)
        actions_box.append(refresh_btn)

        # Lucky 按钮
        lucky_btn = Gtk.Button(label="🎲")
        lucky_btn.add_css_class("mode-btn")
        lucky_btn.set_tooltip_text("I'm feeling lucky")
        lucky_btn.connect("clicked", self.on_feeling_lucky)
        actions_box.append(lucky_btn)

        # 视图切换
        view_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        view_box.set_margin_start(10)
        toolbar.append(view_box)

        self.btn_grid = Gtk.ToggleButton(label="⊞")
        self.btn_grid.set_tooltip_text("Grid View")
        self.btn_grid.add_css_class("mode-btn")
        self.btn_grid.set_active(True)
        self.btn_grid.connect("toggled", self.on_view_grid)
        view_box.append(self.btn_grid)

        self.btn_list = Gtk.ToggleButton(label="☰")
        self.btn_list.set_tooltip_text("List View")
        self.btn_list.add_css_class("mode-btn")
        self.btn_list.connect("toggled", self.on_view_list)
        view_box.append(self.btn_list)

        parent.append(toolbar)

    def build_status_panel(self, parent: Gtk.Box):
        """构建左侧状态面板"""
        status_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        status_box.add_css_class("status-panel")
        status_box.set_margin_start(20)
        status_box.set_margin_end(10)
        status_box.set_margin_top(10)
        status_box.set_margin_bottom(10)

        title = Gtk.Label(label="CURRENTLY USING")
        title.add_css_class("status-label")
        title.set_halign(Gtk.Align.START)
        status_box.append(title)

        self.active_wp_label = Gtk.Label(label="-")
        self.active_wp_label.add_css_class("status-value")
        self.active_wp_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.active_wp_label.set_halign(Gtk.Align.START)
        status_box.append(self.active_wp_label)

        parent.append(status_box)

    def on_view_grid(self, btn):
        if btn.get_active():
            self.btn_list.set_active(False)
            self.view_mode = "grid"
            self.refresh_wallpaper_grid()

    def on_view_list(self, btn):
        if btn.get_active():
            self.btn_grid.set_active(False)
            self.view_mode = "list"
            self.refresh_wallpaper_grid()

    def on_search_changed(self, entry):
        """搜索框内容变化"""
        self.search_query = entry.get_text().lower().strip()
        self.refresh_wallpaper_grid()

    def on_search_activate(self, entry):
        """回车键触发搜索"""
        self.search_query = entry.get_text().lower().strip()
        self.refresh_wallpaper_grid()

    def filter_wallpapers(self) -> Dict[str, Dict]:
        """根据搜索关键词过滤壁纸"""
        if not self.search_query:
            return self.wp_manager._wallpapers

        filtered = {}
        for wp_id, wp in self.wp_manager._wallpapers.items():
            title = wp.get('title', '').lower()
            description = wp.get('description', '').lower()
            tags_str = ' '.join(str(t).lower() for t in wp.get('tags', []))
            folder = wp_id.lower()

            if (self.search_query in title or
                self.search_query in description or
                self.search_query in tags_str or
                self.search_query in folder):
                filtered[wp_id] = wp
        return filtered

    def build_sidebar(self, parent: Gtk.Box):
        self.sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sidebar.add_css_class("sidebar")
        self.sidebar.set_size_request(320, -1)
        self.sidebar.set_hexpand(False)  # 防止水平扩展
        parent.append(self.sidebar)

        # 侧边栏内容（可滚动）
        sidebar_scroll = Gtk.ScrolledWindow()
        sidebar_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sidebar_scroll.set_vexpand(True)
        sidebar_scroll.set_hexpand(False)  # 防止水平扩展
        self.sidebar.append(sidebar_scroll)

        sidebar_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_content.set_hexpand(False)  # 防止水平扩展
        sidebar_content.set_size_request(320, -1)  # 强制宽度
        sidebar_scroll.set_child(sidebar_content)

        # 预览图（包裹在固定宽度容器中）
        preview_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_container.set_size_request(280, 280)
        preview_container.set_hexpand(False)
        preview_container.set_halign(Gtk.Align.CENTER)
        preview_container.add_css_class("sidebar-preview")

        self.sidebar_picture = Gtk.Picture()
        self.sidebar_picture.set_content_fit(Gtk.ContentFit.COVER)
        self.sidebar_picture.set_size_request(280, 280)
        self.sidebar_picture.set_hexpand(False)
        preview_container.append(self.sidebar_picture)

        sidebar_content.append(preview_container)

        # 标题
        self.sidebar_title = Gtk.Label(label="Select a Wallpaper")
        self.sidebar_title.add_css_class("sidebar-title")
        self.sidebar_title.set_halign(Gtk.Align.START)
        self.sidebar_title.set_wrap(True)
        self.sidebar_title.set_max_width_chars(25)
        sidebar_content.append(self.sidebar_title)

        # 副标题（文件夹名）
        self.sidebar_subtitle = Gtk.Label(label="")
        self.sidebar_subtitle.add_css_class("sidebar-subtitle")
        self.sidebar_subtitle.set_halign(Gtk.Align.START)
        sidebar_content.append(self.sidebar_subtitle)

        # 类型
        type_label = Gtk.Label(label="Type")
        type_label.add_css_class("sidebar-section")
        type_label.set_halign(Gtk.Align.START)
        sidebar_content.append(type_label)

        self.sidebar_type = Gtk.Label(label="-")
        self.sidebar_type.add_css_class("sidebar-desc")
        self.sidebar_type.set_halign(Gtk.Align.START)
        sidebar_content.append(self.sidebar_type)

        # 标签
        tags_label = Gtk.Label(label="Tags")
        tags_label.add_css_class("sidebar-section")
        tags_label.set_halign(Gtk.Align.START)
        sidebar_content.append(tags_label)

        tags_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        tags_container.set_hexpand(False)  # 防止扩展
        sidebar_content.append(tags_container)

        self.sidebar_tags = Gtk.FlowBox()
        self.sidebar_tags.set_selection_mode(Gtk.SelectionMode.NONE)
        self.sidebar_tags.set_max_children_per_line(4)
        self.sidebar_tags.set_hexpand(False)  # 防止扩展
        tags_container.append(self.sidebar_tags)

        # 描述
        desc_label = Gtk.Label(label="Description")
        desc_label.add_css_class("sidebar-section")
        desc_label.set_halign(Gtk.Align.START)
        sidebar_content.append(desc_label)

        self.sidebar_desc = Gtk.Label(label="No description.")
        self.sidebar_desc.add_css_class("sidebar-desc")
        self.sidebar_desc.set_halign(Gtk.Align.START)
        self.sidebar_desc.set_wrap(True)
        self.sidebar_desc.set_max_width_chars(30)
        self.sidebar_desc.set_selectable(True)
        sidebar_content.append(self.sidebar_desc)

        # 属性折叠区
        properties_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        properties_separator.set_margin_top(20)
        sidebar_content.append(properties_separator)

        properties_label = Gtk.Label(label="Properties")
        properties_label.add_css_class("sidebar-section")
        properties_label.set_margin_top(15)
        properties_label.set_halign(Gtk.Align.START)
        sidebar_content.append(properties_label)

        # 属性容器
        self.properties_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.properties_box.set_margin_start(15)
        self.properties_box.set_margin_end(15)
        self.properties_box.set_hexpand(False)  # 防止水平扩展
        sidebar_content.append(self.properties_box)

        self.properties_loading_label = Gtk.Label(label="Loading properties...")
        self.properties_loading_label.add_css_class("text-muted")
        self.properties_box.append(self.properties_loading_label)

        # 底部按钮区
        btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        btn_box.set_margin_top(20)
        btn_box.set_margin_bottom(20)
        self.sidebar.append(btn_box)

        # 应用按钮
        self.apply_btn = Gtk.Button(label="Apply Wallpaper")
        self.apply_btn.add_css_class("sidebar-btn")
        self.apply_btn.connect("clicked", self.on_apply_clicked)
        btn_box.append(self.apply_btn)

        # Workshop 链接
        workshop_btn = Gtk.Button(label="Open in Workshop")
        workshop_btn.add_css_class("sidebar-btn")
        workshop_btn.add_css_class("secondary")
        workshop_btn.connect("clicked", self.on_workshop_clicked)
        btn_box.append(workshop_btn)

    def update_sidebar(self):
        """更新侧边栏内容"""
        if not self.selected_wp:
            return

        wp = self.wp_manager._wallpapers.get(self.selected_wp)
        if not wp:
            return

# 更新预览图（使用较大尺寸）
        preview_path = wp['preview']
        texture = self.wp_manager.get_texture(preview_path, 500)
        if texture:
            self.sidebar_picture.set_paintable(texture)
        else:
            self.sidebar_picture.set_paintable(None)

        # 更新文本
        self.sidebar_title.set_label(wp['title'])
        self.sidebar_subtitle.set_label(f"Folder: {wp['id']}")
        self.sidebar_type.set_label(wp.get('type', 'Unknown'))
        self.sidebar_desc.set_label(wp.get('description') or 'No description.')

        # 更新标签
        while True:
            child = self.sidebar_tags.get_first_child()
            if child is None:
                break
            self.sidebar_tags.remove(child)

        tags = wp.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]

        if not tags:
            lbl = Gtk.Label(label="None")
            lbl.add_css_class("text-muted")
            self.sidebar_tags.append(lbl)
        else:
            for tag in tags[:8]:  # 限制标签数量节省内存
                chip = Gtk.Label(label=str(tag))
                chip.add_css_class("tag-chip")
                self.sidebar_tags.append(chip)

        # 加载属性
        self.load_properties(self.selected_wp)

    def load_properties(self, wp_id: str):
        """加载并显示壁纸属性"""
        # 清空现有属性控件
        while True:
            child = self.properties_box.get_first_child()
            if child is None:
                break
            self.properties_box.remove(child)

        # 显示加载状态
        self.properties_box.append(self.properties_loading_label)

        # 异步加载属性
        def load_async():
            properties = self.prop_manager.get_properties(wp_id)
            GLib.idle_add(lambda: self.display_properties(properties))

        threading.Thread(target=load_async, daemon=True).start()

    def display_properties(self, properties: List[Dict]):
        """显示属性控件"""
        # 移除加载标签
        self.properties_box.remove(self.properties_loading_label)

        if not properties:
            no_props = Gtk.Label(label="No properties available.")
            no_props.add_css_class("text-muted")
            self.properties_box.append(no_props)
            return

        # 为每个属性创建控件
        for prop in properties:
            prop_widget = self.create_property_widget(prop)
            self.properties_box.append(prop_widget)

    def create_property_widget(self, prop: Dict) -> Gtk.Widget:
        """根据属性类型创建控件"""
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        container.set_margin_top(8)
        container.set_hexpand(False)  # 防止水平扩展影响侧边栏宽度

        # 属性标题
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        title_box.set_hexpand(False)
        container.append(title_box)

        title_label = Gtk.Label(label=prop.get('text', prop['name']))
        title_label.set_halign(Gtk.Align.START)
        title_label.add_css_class("setting-label")
        title_box.append(title_label)

        # 根据类型创建控件
        prop_type = prop['type']
        prop_name = prop['name']

        # 获取用户自定义值
        user_value = self.prop_manager.get_user_property(self.selected_wp, prop_name)
        current_value = user_value if user_value is not None else prop['value']

        if prop_type == 'boolean':
            switch = Gtk.Switch()
            switch.set_active(bool(current_value))
            switch.set_valign(Gtk.Align.CENTER)
            switch.set_halign(Gtk.Align.START)
            switch.set_hexpand(False)
            switch.connect('state-set', lambda s, v: self.on_property_changed(prop_name, v, 'boolean'))
            container.append(switch)

        elif prop_type == 'slider':
            slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, prop['min'], prop['max'], prop['step'])
            slider.set_value(float(current_value))
            slider.set_hexpand(False)  # 防止水平扩展
            slider.set_size_request(280, -1)  # 固定宽度
            slider.connect('value-changed', lambda s: self.on_property_changed(prop_name, s.get_value(), 'slider'))
            container.append(slider)

            # 显示当前值
            value_label = Gtk.Label(label=f"{current_value}")
            value_label.add_css_class("text-muted")
            value_label.set_halign(Gtk.Align.START)
            container.append(value_label)

        elif prop_type == 'color':
            color = Gtk.ColorButton()
            color.set_hexpand(False)  # 防止水平扩展
            if isinstance(current_value, tuple) and len(current_value) >= 3:
                gdk_color = Gdk.RGBA()
                gdk_color.parse(f"rgb({int(current_value[0]*255)}, {int(current_value[1]*255)}, {int(current_value[2]*255)})")
                color.set_rgba(gdk_color)
            color.connect('color-set', lambda w: self.on_color_property_changed(prop_name, w.get_rgba(), 'color'))
            container.append(color)

        elif prop_type == 'combo':
            if prop['options']:
                option_strings = [opt['label'] for opt in prop['options']]
                dropdown = Gtk.DropDown.new_from_strings(option_strings)
                dropdown.set_hexpand(False)  # 防止水平扩展
                dropdown.set_size_request(280, -1)  # 固定宽度
                current_idx = 0
                for i, opt in enumerate(prop['options']):
                    if str(opt['value']) == str(current_value):
                        current_idx = i
                        break
                dropdown.set_selected(current_idx)
                dropdown.connect('notify::selected', lambda w, p: self.on_combo_property_changed(prop_name, prop['options'], w.get_selected(), 'combo'))
                container.append(dropdown)
            else:
                lbl = Gtk.Label(label="No options available")
                lbl.add_css_class("text-muted")
                lbl.set_hexpand(False)
                container.append(lbl)

        return container

    def on_property_changed(self, prop_name: str, value, prop_type: str):
        """属性值变化处理"""
        if prop_type == 'boolean':
            self.prop_manager.set_user_property(self.selected_wp, prop_name, bool(value))
        elif prop_type == 'slider':
            self.prop_manager.set_user_property(self.selected_wp, prop_name, float(value))
        # 如果当前正在播放这个壁纸，重新应用以立即生效
        if self.active_wp == self.selected_wp:
            print(f"[PROPERTY] Re-applying wallpaper {self.selected_wp} with updated property {prop_name}")
            self.controller.apply(self.selected_wp)

    def on_color_property_changed(self, prop_name: str, color: Gdk.RGBA, prop_type: str):
        """颜色属性值变化处理"""
        if prop_type == 'color':
            r, g, b, a = color.red, color.green, color.blue, color.alpha
            self.prop_manager.set_user_property(self.selected_wp, prop_name, (r, g, b))
            # 如果当前正在播放这个壁纸，重新应用以立即生效
            if self.active_wp == self.selected_wp:
                print(f"[PROPERTY] Re-applying wallpaper {self.selected_wp} with updated property {prop_name}")
                self.controller.apply(self.selected_wp)

    def on_combo_property_changed(self, prop_name: str, options: List[Dict], selected_idx: int, prop_type: str):
        """下拉选择属性值变化处理"""
        if prop_type == 'combo' and selected_idx < len(options):
            self.prop_manager.set_user_property(self.selected_wp, prop_name, options[selected_idx]['value'])
            # 如果当前正在播放这个壁纸，重新应用以立即生效
            if self.active_wp == self.selected_wp:
                print(f"[PROPERTY] Re-applying wallpaper {self.selected_wp} with updated property {prop_name}")
                self.controller.apply(self.selected_wp)

    def refresh_wallpaper_grid(self):
        """刷新壁纸显示"""
        if self.view_mode == "grid":
            self.wallpaper_scroll.set_child(self.flowbox)
            self.populate_grid()
        else:
            self.wallpaper_scroll.set_child(self.listbox)
            self.populate_list()

    def populate_grid(self):
        """填充网格视图"""
        while True:
            child = self.flowbox.get_first_child()
            if child is None:
                break
            self.flowbox.remove(child)

        filtered = self.filter_wallpapers()
        for folder_id, wp in filtered.items():
            card = self.create_grid_item(folder_id, wp)
            self.flowbox.append(card)

    def create_grid_item(self, folder_id: str, wp: Dict) -> Gtk.Widget:
        """创建网格项"""
        btn = Gtk.Button()
        btn.add_css_class("wallpaper-item")
        btn.add_css_class("wallpaper-card")
        btn.set_size_request(170, 170)
        btn.set_has_frame(False)
        btn.connect("clicked", lambda _: self.on_select_wallpaper(folder_id))

        # 双击直接应用壁纸（使用 GestureClick 捕获双击，限制主键并提前捕获阶段）
        gesture = Gtk.GestureClick.new()
        gesture.set_button(Gdk.BUTTON_PRIMARY)
        gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        gesture.connect("pressed", lambda g, n_press, x, y: self.on_wallpaper_activated(folder_id, n_press))
        btn.add_controller(gesture)

        # 右键菜单（GestureClick 捕获右键）
        context_gesture = Gtk.GestureClick.new()
        context_gesture.set_button(Gdk.BUTTON_SECONDARY)
        context_gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        context_gesture.connect("pressed", lambda g, n_press, x, y: self.on_wallpaper_context_menu(btn, folder_id))
        btn.add_controller(context_gesture)

        overlay = Gtk.Overlay()
        btn.set_child(overlay)

# 背景图片（使用纹理缓存或占位符）
        preview_path = wp['preview']
        texture = self.wp_manager.get_texture(preview_path, 170)
        if texture:
            picture = Gtk.Picture.new_for_paintable(texture)
            picture.set_content_fit(Gtk.ContentFit.COVER)
            picture.set_size_request(170, 170)
            overlay.set_child(picture)
        else:
            placeholder = Gtk.Box()
            placeholder.set_size_request(170, 170)
            lbl = Gtk.Label(label=wp['title'][:1].upper())
            lbl.set_halign(Gtk.Align.CENTER)
            lbl.set_valign(Gtk.Align.CENTER)
            placeholder.append(lbl)
            overlay.set_child(placeholder)

        # 标题（底部）
        name_box = Gtk.Box()
        name_box.set_halign(Gtk.Align.CENTER)
        name_box.set_valign(Gtk.Align.END)
        name_box.set_margin_bottom(10)

        name_label = Gtk.Label(label=wp['title'])
        name_label.add_css_class("wallpaper-name")
        name_label.set_ellipsize(Pango.EllipsizeMode.END)
        name_label.set_max_width_chars(15)
        name_box.append(name_label)

        overlay.add_overlay(name_box)

        wp['_grid_btn'] = btn
        if folder_id == self.selected_wp:
            btn.add_css_class("selected")

        return btn

    def populate_list(self):
        """填充列表视图"""
        while True:
            row = self.listbox.get_first_child()
            if row is None:
                break
            self.listbox.remove(row)

        filtered = self.filter_wallpapers()
        for folder_id, wp in filtered.items():
            row = self.create_list_item(folder_id, wp)
            self.listbox.append(row)

    def create_list_item(self, folder_id: str, wp: Dict) -> Gtk.Widget:
        """创建列表项"""
        btn = Gtk.Button()
        btn.add_css_class("list-item")
        btn.set_has_frame(False)
        btn.connect("clicked", lambda _: self.on_select_wallpaper(folder_id))

        # 双击直接应用壁纸（使用 GestureClick 捕获双击，限制主键并提前捕获阶段）
        gesture = Gtk.GestureClick.new()
        gesture.set_button(Gdk.BUTTON_PRIMARY)
        gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        gesture.connect("pressed", lambda g, n_press, x, y: self.on_wallpaper_activated(folder_id, n_press))
        btn.add_controller(gesture)

        # 右键菜单（GestureClick 捕获右键）
        context_gesture = Gtk.GestureClick.new()
        context_gesture.set_button(Gdk.BUTTON_SECONDARY)
        context_gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        context_gesture.connect("pressed", lambda g, n_press, x, y: self.on_wallpaper_context_menu(btn, folder_id))
        btn.add_controller(context_gesture)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        btn.set_child(hbox)

# 缩略图（使用纹理缓存）
        preview_path = wp['preview']
        texture = self.wp_manager.get_texture(preview_path, 100)
        if texture:
            picture = Gtk.Picture.new_for_paintable(texture)
            picture.set_content_fit(Gtk.ContentFit.COVER)
            picture.set_size_request(100, 100)
            picture.add_css_class("card")
            hbox.append(picture)

        # 信息
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info_box.set_hexpand(True)
        hbox.append(info_box)

        title = Gtk.Label(label=wp['title'])
        title.add_css_class("list-title")
        title.set_halign(Gtk.Align.START)
        title.set_ellipsize(Pango.EllipsizeMode.END)
        info_box.append(title)

        type_lbl = Gtk.Label(label=f"Type: {wp.get('type', 'Unknown')}")
        type_lbl.add_css_class("list-type")
        type_lbl.set_halign(Gtk.Align.START)
        info_box.append(type_lbl)

        tags = wp.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        tags_str = ', '.join(str(t) for t in tags[:5]) if tags else 'None'
        tags_lbl = Gtk.Label(label=f"Tags: {tags_str}")
        tags_lbl.add_css_class("list-tags")
        tags_lbl.set_halign(Gtk.Align.START)
        tags_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        info_box.append(tags_lbl)

        folder_lbl = Gtk.Label(label=f"Folder: {folder_id}")
        folder_lbl.add_css_class("list-folder")
        folder_lbl.set_halign(Gtk.Align.START)
        info_box.append(folder_lbl)

        wp['_list_btn'] = btn
        if folder_id == self.selected_wp:
            btn.add_css_class("selected")

        return btn

    def on_select_wallpaper(self, folder_id: str):
        """选择壁纸"""
        # 取消之前的选中状态
        if self.selected_wp and self.selected_wp in self.wp_manager._wallpapers:
            old_wp = self.wp_manager._wallpapers[self.selected_wp]
            if '_grid_btn' in old_wp:
                old_wp['_grid_btn'].remove_css_class("selected")
            if '_list_btn' in old_wp:
                old_wp['_list_btn'].remove_css_class("selected")

        # 设置新选中
        self.selected_wp = folder_id
        wp = self.wp_manager._wallpapers.get(folder_id)
        if wp:
            if '_grid_btn' in wp:
                wp['_grid_btn'].add_css_class("selected")
            if '_list_btn' in wp:
                wp['_list_btn'].add_css_class("selected")

        self.update_sidebar()

    def on_wallpaper_activated(self, folder_id: str, n_press: int):
        """双击直接应用壁纸"""
        if n_press == 2:
            self.on_select_wallpaper(folder_id)
            self.controller.apply(folder_id)
            self.active_wp = folder_id
            wp = self.wp_manager._wallpapers.get(folder_id)
            if wp:
                self.active_wp_label.set_label(wp['title'])

    def on_wallpaper_context_menu(self, widget: Gtk.Widget, folder_id: str):
        """显示壁纸右键菜单"""
        menu = Gtk.PopoverMenu()

        # 应用壁纸
        apply_action = Gio.SimpleAction.new("apply", None)
        apply_action.connect("activate", lambda a, p: self._apply_wallpaper_from_context(folder_id))
        self.win.add_action(apply_action)

        # 停止壁纸
        stop_action = Gio.SimpleAction.new("stop", None)
        stop_action.connect("activate", lambda a, p: self._stop_wallpaper_from_context())
        self.win.add_action(stop_action)

        # 删除壁纸
        delete_action = Gio.SimpleAction.new("delete", None)
        delete_action.connect("activate", lambda a, p: self._delete_wallpaper_from_context(folder_id))
        self.win.add_action(delete_action)

        # 创建菜单模型
        menu_model = Gio.Menu()
        apply_item = Gio.MenuItem.new("Apply Wallpaper", "win.apply")
        stop_item = Gio.MenuItem.new("Stop Wallpaper", "win.stop")
        delete_item = Gio.MenuItem.new("Delete Wallpaper", "win.delete")

        menu_model.append_item(apply_item)
        menu_model.append_item(stop_item)
        menu_model.append_item(delete_item)

        menu.set_menu_model(menu_model)
        menu.set_parent(widget)
        menu.set_pointing_to(Gdk.Rectangle())
        menu.popup()

    def _apply_wallpaper_from_context(self, folder_id: str):
        """从右键菜单应用壁纸"""
        self.on_select_wallpaper(folder_id)
        self.controller.apply(folder_id)
        self.active_wp = folder_id
        wp = self.wp_manager._wallpapers.get(folder_id)
        if wp:
            self.active_wp_label.set_label(wp['title'])

    def _stop_wallpaper_from_context(self):
        """从右键菜单停止壁纸"""
        self.controller.stop()
        self.active_wp = None
        self.active_wp_label.set_label("None")

    def _delete_wallpaper_from_context(self, folder_id: str):
        """从右键菜单删除壁纸"""
        # 创建确认对话框
        dialog = Gtk.MessageDialog(
            transient_for=self.win,
            modal=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Delete Wallpaper?"
        )
        dialog.set_property("secondary-text", f"Are you sure you want to delete wallpaper {folder_id}?\\nThis action cannot be undone.")

        # 连接响应信号
        def on_dialog_response(dialog, response):
            if response == Gtk.ResponseType.YES:
                self.log_manager.add_info(f"Deleting wallpaper {folder_id}", "GUI")
                if self.wp_manager.delete_wallpaper(folder_id):
                    self.log_manager.add_info(f"Wallpaper {folder_id} deleted successfully", "GUI")
                    # 从属性管理器中移除
                    if hasattr(self.prop_manager, '_user_properties') and folder_id in self.prop_manager._user_properties:
                        del self.prop_manager._user_properties[folder_id]
                    # 刷新壁纸列表
                    self.refresh_wallpaper_grid()
                    # 如果删除的是当前选中的壁纸，清空侧边栏
                    if self.selected_wp == folder_id:
                        self.selected_wp = None
                        self.update_sidebar()
                else:
                    self.log_manager.add_error(f"Failed to delete wallpaper {folder_id}", "GUI")
                    error_dialog = Gtk.MessageDialog(
                        transient_for=self.win,
                        modal=True,
                        message_type=Gtk.MessageType.ERROR,
                        buttons=Gtk.ButtonsType.OK,
                        text="Deletion Failed"
                    )
                    error_dialog.set_property("secondary-text", f"Could not delete wallpaper {folder_id}. Check permissions.")
                    error_dialog.connect("response", lambda d, r: d.destroy())
                    error_dialog.present()

            dialog.destroy()

        dialog.connect("response", on_dialog_response)
        dialog.present()

    def on_feeling_lucky(self, btn):
        """随机挑选并应用一张壁纸"""
        if not self.wp_manager._wallpapers:
            return
        wp_id = random.choice(list(self.wp_manager._wallpapers.keys()))
        self.on_select_wallpaper(wp_id)
        self.controller.apply(wp_id)
        self.active_wp = wp_id
        wp = self.wp_manager._wallpapers.get(wp_id)
        if wp:
            self.active_wp_label.set_label(wp['title'])

    def auto_apply_wallpaper(self, wp_id: str):
        """启动时自动应用上次壁纸"""
        if wp_id in self.wp_manager._wallpapers:
            self.controller.apply(wp_id)
            self.active_wp = wp_id
            wp = self.wp_manager._wallpapers.get(wp_id)
            if wp:
                self.active_wp_label.set_label(wp['title'])
                print(f"[AUTO-APPLY] Wallpaper auto-applied: {wp['title']}")
        return False  # 不重复执行

    def on_apply_clicked(self, btn):
        """应用壁纸"""
        if self.selected_wp:
            self.controller.apply(self.selected_wp)
            self.active_wp = self.selected_wp
            wp = self.wp_manager._wallpapers.get(self.selected_wp)
            if wp:
                self.active_wp_label.set_label(wp['title'])

    def on_workshop_clicked(self, btn):
        """打开 Workshop 页面"""
        if self.selected_wp:
            url = f"steam://url/CommunityFilePage/{self.selected_wp}"
            webbrowser.open(url)

    # ========================================================================
    # 设置页面
    # ========================================================================
    def build_settings_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        page.add_css_class("settings-container")
        self.content_stack.add_named(page, "settings")

        # 左侧导航
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar.add_css_class("settings-sidebar")
        sidebar.set_size_request(280, -1)
        page.append(sidebar)

        # 标题
        header = Gtk.Label(label="Settings")
        header.add_css_class("settings-header")
        header.set_halign(Gtk.Align.START)
        header.set_margin_start(16)
        sidebar.append(header)

        subheader = Gtk.Label(label="Configure your experience")
        subheader.add_css_class("settings-subheader")
        subheader.set_halign(Gtk.Align.START)
        subheader.set_margin_start(16)
        subheader.set_margin_bottom(32)
        sidebar.append(subheader)

        # 导航按钮（先创建但不绑定信号）
        nav_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        nav_box.set_vexpand(True)
        sidebar.append(nav_box)

        sections = [
            ("general", "🖥 General"),
            ("audio", "🔊 Audio"),
            ("advanced", "⚙️ Advanced"),
            ("logs", "📋 Logs"),
        ]

        self.settings_nav_btns = {}
        for section_id, label in sections:
            btn = Gtk.ToggleButton(label=label)
            btn.add_css_class("settings-nav-item")
            # 暂时不绑定信号
            nav_box.append(btn)
            self.settings_nav_btns[section_id] = btn

        # 右侧设置内容（先创建 stack）
        content_scroll = Gtk.ScrolledWindow()
        content_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        content_scroll.set_hexpand(True)
        page.append(content_scroll)

        self.settings_stack = Gtk.Stack()
        self.settings_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        content_scroll.set_child(self.settings_stack)

        # 构建所有设置页面
        self.build_general_settings()
        self.build_audio_settings()
        self.build_advanced_settings()
        self.build_logs_settings()

        # 现在 stack 已经存在，安全绑定信号
        for section_id, _ in sections:
            btn = self.settings_nav_btns[section_id]
            btn.connect("toggled", self.on_settings_nav, section_id)

        # 设置默认选中
        self.settings_nav_btns["general"].set_active(True)

        # 操作按钮
        actions = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        actions.set_margin_top(24)
        sidebar.append(actions)

        save_btn = Gtk.Button(label="Save Changes")
        save_btn.add_css_class("action-btn")
        save_btn.add_css_class("primary")
        save_btn.connect("clicked", self.on_save_settings)
        actions.append(save_btn)

        refresh_btn = Gtk.Button(label="Reload Wallpapers")
        refresh_btn.add_css_class("action-btn")
        refresh_btn.add_css_class("secondary")
        refresh_btn.connect("clicked", self.on_reload_wallpapers)
        actions.append(refresh_btn)

        clear_btn = Gtk.Button(label="Stop Wallpaper")
        clear_btn.add_css_class("action-btn")
        clear_btn.add_css_class("danger")
        clear_btn.connect("clicked", lambda _: self.controller.stop())
        actions.append(clear_btn)

    def on_settings_nav(self, btn, section_id):
        if btn.get_active():
            for sid, b in self.settings_nav_btns.items():
                if sid != section_id:
                    b.set_active(False)
            self.settings_stack.set_visible_child_name(section_id)

    def build_general_settings(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        self.settings_stack.add_named(box, "general")

        title = Gtk.Label(label="General")
        title.add_css_class("settings-section-title")
        title.set_halign(Gtk.Align.START)
        box.append(title)

        desc = Gtk.Label(label="Basic wallpaper engine behavior and performance.")
        desc.add_css_class("settings-section-desc")
        desc.set_halign(Gtk.Align.START)
        box.append(desc)

        # FPS
        fps_row = self.create_setting_row("FPS Limit", "Target frames per second.")
        box.append(fps_row)
        self.fps_spin = Gtk.SpinButton()
        self.fps_spin.set_range(1, 144)
        self.fps_spin.set_increments(1, 10)
        self.fps_spin.set_value(self.config.get("fps", 30))
        fps_row.append(self.fps_spin)

        # Scaling
        scaling_row = self.create_setting_row("Scaling Mode", "How the wallpaper fits.")
        box.append(scaling_row)
        self.scaling_dropdown = Gtk.DropDown.new_from_strings(
            ["default", "stretch", "fit", "fill"]
        )
        current_scaling = self.config.get("scaling", "default")
        scaling_options = ["default", "stretch", "fit", "fill"]
        if current_scaling in scaling_options:
            self.scaling_dropdown.set_selected(scaling_options.index(current_scaling))
        scaling_row.append(self.scaling_dropdown)

        # No Fullscreen Pause
        pause_row = self.create_setting_row("No Fullscreen Pause", "Keep running in fullscreen.")
        box.append(pause_row)
        self.pause_switch = Gtk.Switch()
        self.pause_switch.set_active(self.config.get("noFullscreenPause", False))
        self.pause_switch.set_valign(Gtk.Align.CENTER)
        pause_row.append(self.pause_switch)

        # Disable Mouse
        mouse_row = self.create_setting_row("Disable Mouse", "Ignore mouse interaction.")
        box.append(mouse_row)
        self.mouse_switch = Gtk.Switch()
        self.mouse_switch.set_active(self.config.get("disableMouse", False))
        self.mouse_switch.set_valign(Gtk.Align.CENTER)
        mouse_row.append(self.mouse_switch)

    def build_audio_settings(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        self.settings_stack.add_named(box, "audio")

        title = Gtk.Label(label="Audio")
        title.add_css_class("settings-section-title")
        title.set_halign(Gtk.Align.START)
        box.append(title)

        desc = Gtk.Label(label="Control wallpaper audio.")
        desc.add_css_class("settings-section-desc")
        desc.set_halign(Gtk.Align.START)
        box.append(desc)

        # Silence
        silence_row = self.create_setting_row("Silence Wallpaper", "Mute all audio.")
        box.append(silence_row)
        self.silence_switch = Gtk.Switch()
        self.silence_switch.set_active(self.config.get("silence", True))
        self.silence_switch.set_valign(Gtk.Align.CENTER)
        silence_row.append(self.silence_switch)

        # Volume
        volume_row = self.create_setting_row("Volume", "Master volume (0-100).")
        box.append(volume_row)
        self.volume_spin = Gtk.SpinButton()
        self.volume_spin.set_range(0, 100)
        self.volume_spin.set_increments(5, 10)
        self.volume_spin.set_value(self.config.get("volume", 50))
        volume_row.append(self.volume_spin)

    def build_advanced_settings(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        self.settings_stack.add_named(box, "advanced")

        title = Gtk.Label(label="Advanced")
        title.add_css_class("settings-section-title")
        title.set_halign(Gtk.Align.START)
        box.append(title)

        desc = Gtk.Label(label="Power user options.")
        desc.add_css_class("settings-section-desc")
        desc.set_halign(Gtk.Align.START)
        box.append(desc)

        # Workshop Path
        path_row = self.create_setting_row("Workshop Directory", "Path to Workshop content.")
        path_row.set_orientation(Gtk.Orientation.VERTICAL)
        box.append(path_row)
        self.path_entry = Gtk.Entry()
        self.path_entry.set_text(self.config.get("workshopPath", WORKSHOP_PATH))
        self.path_entry.set_hexpand(True)
        path_row.append(self.path_entry)

        # Screen Root (Multi-monitor support)
        screen_row = self.create_setting_row("Screen Root", "Select a monitor for wallpaper.")
        box.append(screen_row)

        # 获取屏幕列表
        screens = self.screen_manager.get_screens()
        current_screen = self.config.get("lastScreen", "eDP-1")

        # 如果当前屏幕不在列表中，添加它
        if current_screen not in screens:
            screens = screens + [current_screen]

        self.screen_dropdown = Gtk.DropDown.new_from_strings(screens)
        self.screen_dropdown.set_hexpand(True)

        # 设置当前选中的屏幕
        if current_screen in screens:
            self.screen_dropdown.set_selected(screens.index(current_screen))

        screen_row.append(self.screen_dropdown)

        # 刷新屏幕按钮
        refresh_screen_btn = Gtk.Button(label="⟳ Refresh Screens")
        refresh_screen_btn.add_css_class("action-btn")
        refresh_screen_btn.add_css_class("secondary")
        refresh_screen_btn.set_margin_top(8)
        refresh_screen_btn.connect("clicked", self.on_refresh_screens)
        box.append(refresh_screen_btn)

    def build_logs_settings(self):
        """构建日志设置页面"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        self.settings_stack.add_named(box, "logs")

        title = Gtk.Label(label="Logs")
        title.add_css_class("settings-section-title")
        title.set_halign(Gtk.Align.START)
        box.append(title)

        desc = Gtk.Label(label="View application and wallpaper engine logs.")
        desc.add_css_class("settings-section-desc")
        desc.set_halign(Gtk.Align.START)
        box.append(desc)

        # 日志文本视图
        log_scroll = Gtk.ScrolledWindow()
        log_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        log_scroll.set_vexpand(True)
        log_scroll.set_size_request(-1, 500)
        box.append(log_scroll)

        self.log_text_view = Gtk.TextView()
        self.log_text_view.set_editable(False)
        self.log_text_view.set_cursor_visible(False)
        self.log_text_view.set_monospace(True)
        self.log_text_view.set_left_margin(8)
        self.log_text_view.set_right_margin(8)
        self.log_text_view.set_top_margin(8)
        self.log_text_view.set_bottom_margin(8)
        log_scroll.set_child(self.log_text_view)

        self.log_buffer = self.log_text_view.get_buffer()

        # 创建日志文本标签
        tag_table = self.log_buffer.get_tag_table()

        # 时间标签（灰色）
        self.log_tag_timestamp = Gtk.TextTag(name="timestamp")
        self.log_tag_timestamp.set_property("foreground", "#6b7280")
        self.log_tag_timestamp.set_property("size-points", 12)
        tag_table.add(self.log_tag_timestamp)

        # 级别标签（不同颜色）
        self.log_tag_debug = Gtk.TextTag(name="debug")
        self.log_tag_debug.set_property("foreground", "#6b7280")
        self.log_tag_debug.set_property("size-points", 12)
        tag_table.add(self.log_tag_debug)

        self.log_tag_info = Gtk.TextTag(name="info")
        self.log_tag_info.set_property("foreground", "#3b82f6")
        self.log_tag_info.set_property("size-points", 12)
        tag_table.add(self.log_tag_info)

        self.log_tag_warning = Gtk.TextTag(name="warning")
        self.log_tag_warning.set_property("foreground", "#f59e0b")
        self.log_tag_warning.set_property("size-points", 12)
        tag_table.add(self.log_tag_warning)

        self.log_tag_error = Gtk.TextTag(name="error")
        self.log_tag_error.set_property("foreground", "#ef4444")
        self.log_tag_error.set_property("size-points", 12)
        tag_table.add(self.log_tag_error)

        # 来源标签（紫色）
        self.log_tag_source = Gtk.TextTag(name="source")
        self.log_tag_source.set_property("foreground", "#a855f7")
        self.log_tag_source.set_property("size-points", 12)
        tag_table.add(self.log_tag_source)

        # 消息标签（白色，稍大字号）
        self.log_tag_message = Gtk.TextTag(name="message")
        self.log_tag_message.set_property("foreground", "#e5e7eb")
        self.log_tag_message.set_property("size-points", 12)
        tag_table.add(self.log_tag_message)

        # 行间距标签
        self.log_tag_line = Gtk.TextTag(name="line")
        self.log_tag_line.set_property("pixels-above-lines", 8)
        tag_table.add(self.log_tag_line)

        # 操作按钮
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_box.set_halign(Gtk.Align.END)
        box.append(btn_box)

        clear_btn = Gtk.Button(label="Clear Logs")
        clear_btn.add_css_class("action-btn")
        clear_btn.add_css_class("secondary")
        clear_btn.connect("clicked", self.on_clear_logs)
        btn_box.append(clear_btn)

        copy_btn = Gtk.Button(label="Copy Logs")
        copy_btn.add_css_class("action-btn")
        copy_btn.add_css_class("secondary")
        copy_btn.connect("clicked", self.on_copy_logs)
        btn_box.append(copy_btn)

        refresh_btn = Gtk.Button(label="Refresh")
        refresh_btn.add_css_class("action-btn")
        refresh_btn.add_css_class("primary")
        refresh_btn.connect("clicked", self.on_refresh_logs)
        btn_box.append(refresh_btn)

        # 注册日志更新回调
        self.log_manager.register_callback(self.on_log_update)

        # 初始化显示日志
        self.refresh_logs_display()

    def on_log_update(self, log_entry: Dict):
        """日志更新回调"""
        def update_ui():
            self.append_log_entry(log_entry)
        GLib.idle_add(update_ui)

    def append_log_entry(self, log_entry: Dict):
        """添加日志条目到显示区域"""
        timestamp = log_entry.get("timestamp", "")
        level = log_entry.get("level", "")
        source = log_entry.get("source", "")
        message = log_entry.get("message", "")

        # 获取位置标记
        start_iter = self.log_buffer.get_end_iter()

        # 插入时间戳
        self.log_buffer.insert_with_tags(start_iter, f"[{timestamp}] ", self.log_tag_timestamp)

        # 插入级别标签
        level_tags = {
            "DEBUG": self.log_tag_debug,
            "INFO": self.log_tag_info,
            "WARNING": self.log_tag_warning,
            "ERROR": self.log_tag_error
        }
        level_tag = level_tags.get(level, self.log_tag_debug)
        self.log_buffer.insert_with_tags(start_iter, f"[{level}] ", level_tag)

        # 插入来源
        self.log_buffer.insert_with_tags(start_iter, f"[{source}] ", self.log_tag_source)

        # 插入消息
        self.log_buffer.insert_with_tags(start_iter, f"{message}\n", self.log_tag_message, self.log_tag_line)

        # 自动滚动到底部
        self.log_text_view.scroll_to_mark(
            self.log_buffer.create_mark("end", self.log_buffer.get_end_iter(), False),
            0.0, False, 0.0, 0.0
        )

    def refresh_logs_display(self):
        """刷新日志显示"""
        self.log_buffer.set_text("")
        for log_entry in self.log_manager.get_logs():
            self.append_log_entry(log_entry)

    def on_clear_logs(self, btn):
        """清空日志"""
        self.log_manager.clear()
        self.log_buffer.set_text("")

    def on_copy_logs(self, btn):
        """复制日志到剪贴板"""
        start_iter = self.log_buffer.get_start_iter()
        end_iter = self.log_buffer.get_end_iter()
        text = self.log_buffer.get_text(start_iter, end_iter, False)
        
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(text)
        
        # 提示成功
        original_label = "Copy Logs" # Hardcoded or retrieve if needed, but we know it's "Copy Logs"
        btn.set_label("Copied!")
        btn.add_css_class("success")
        
        def restore_button():
            btn.set_label(original_label)
            btn.remove_css_class("success")
            return False

        GLib.timeout_add(2000, restore_button)

    def on_refresh_logs(self, btn):
        """刷新日志显示"""
        self.refresh_logs_display()

    def create_setting_row(self, label: str, description: str) -> Gtk.Box:
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add_css_class("setting-row")

        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info.set_hexpand(True)
        row.append(info)

        lbl = Gtk.Label(label=label)
        lbl.add_css_class("setting-label")
        lbl.set_halign(Gtk.Align.START)
        info.append(lbl)

        d = Gtk.Label(label=description)
        d.add_css_class("setting-desc")
        d.set_halign(Gtk.Align.START)
        info.append(d)

        return row

    def on_save_settings(self, btn):
        """保存设置"""
        self.config.set("fps", int(self.fps_spin.get_value()))
        scaling_options = ["default", "stretch", "fit", "fill"]
        self.config.set("scaling", scaling_options[self.scaling_dropdown.get_selected()])
        self.config.set("noFullscreenPause", self.pause_switch.get_active())
        self.config.set("disableMouse", self.mouse_switch.get_active())
        self.config.set("silence", self.silence_switch.get_active())
        self.config.set("volume", int(self.volume_spin.get_value()))

        # 保存 Workshop 路径
        new_path = self.path_entry.get_text().strip()
        if new_path:
            self.config.set("workshopPath", new_path)

        # 从下拉选择保存屏幕名称
        screens = self.screen_manager.get_screens()
        selected_idx = self.screen_dropdown.get_selected()
        if selected_idx >= 0 and selected_idx < len(screens):
            self.config.set("lastScreen", screens[selected_idx])
        else:
            self.config.set("lastScreen", "eDP-1")

        self.log_manager.add_info("Settings saved", "GUI")

        # 如果当前有正在播放的壁纸，重新应用以应用新设置
        if self.active_wp and self.active_wp in self.wp_manager._wallpapers:
            self.log_manager.add_info(f"Re-applying wallpaper {self.active_wp} with new settings", "GUI")
            self.controller.apply(self.active_wp)

    def on_refresh_screens(self, btn):
        """刷新屏幕列表"""
        screens = self.screen_manager.refresh()
        current_screen = self.config.get("lastScreen", "eDP-1")

        # 如果当前屏幕不在列表中，添加它
        if current_screen not in screens:
            screens = screens + [current_screen]

        # 更新下拉选择
        self.screen_dropdown.set_model(Gtk.StringList.new(screens))

        # 设置当前选中的屏幕
        if current_screen in screens:
            self.screen_dropdown.set_selected(screens.index(current_screen))

    def on_reload_wallpapers(self, btn):
        """重新加载壁纸"""
        self.wp_manager.clear_cache()
        # 如果用户修改了 Workshop 路径，使用新路径进行扫描
        new_path = self.path_entry.get_text().strip()
        if new_path:
            self.wp_manager.workshop_path = new_path
        self.wp_manager.scan()
        self.refresh_wallpaper_grid()


# ============================================================================
# 入口
# ============================================================================
if __name__ == '__main__':
    app = WallpaperApp()
    app.run(sys.argv)
