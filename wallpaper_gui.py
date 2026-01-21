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
    text-align: left;
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
        """清理纹理缓存"""
        self._texture_cache.clear()
        gc.collect()


# ============================================================================
# 壁纸控制器
# ============================================================================
class WallpaperController:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.current_proc: Optional[subprocess.Popen] = None

    def apply(self, wp_id: str, screen: Optional[str] = None):
        """应用壁纸"""
        self.stop()
        # 确保screen是有效字符串，避免None被转成字符串"None"
        if not screen:
            screen = self.config.get("lastScreen")
        if not screen or screen == "None":
            screen = "eDP-1"

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

        # 【调试输出】
        print(f"[DEBUG] Executing: {' '.join(cmd)}")

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
                print(f"[ERROR] Process exited!")
                print(f"[STDOUT] {stdout.decode()}")
                print(f"[STDERR] {stderr.decode()}")
                return

            self.config.set("lastWallpaper", wp_id)
            self.config.set("lastScreen", screen)
            print(f"[SUCCESS] Wallpaper applied: {wp_id}")

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
            print(f"[EXCEPTION] Failed: {e}")

    def stop(self):
        """停止壁纸"""
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
        self.wp_manager = WallpaperManager()
        self.controller = WallpaperController(self.config)

        self.view_mode = "grid"  # grid, list
        self.selected_wp: Optional[str] = None
        self.active_wp: Optional[str] = None

        # CLI 控制：支持 --minimized/--hidden、--show/--hide/--toggle 等
        self.start_hidden = False
        self.cli_actions: List[str] = []
        self.initialized = False

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
            if not self.start_hidden:
                self.show_window()
            self.start_hidden = False
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

        # 最小化按钮（隐藏到托盘）
        minimize_btn = Gtk.Button(label="⌄ Minimize")
        minimize_btn.add_css_class("nav-btn")
        minimize_btn.connect("clicked", lambda _: self.hide_window())
        nav_container.append(minimize_btn)

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

        # 工具栏
        self.build_toolbar(page)

        # 主内容区（左右布局）
        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        content_box.set_vexpand(True)
        page.append(content_box)

        # 左侧壁纸区
        workspace = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        workspace.set_hexpand(True)
        content_box.append(workspace)

        # 壁纸容器
        self.wallpaper_scroll = Gtk.ScrolledWindow()
        self.wallpaper_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.wallpaper_scroll.set_vexpand(True)
        workspace.append(self.wallpaper_scroll)

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

        # 右侧侧边栏
        self.build_sidebar(content_box)

    def build_toolbar(self, parent: Gtk.Box):
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        toolbar.add_css_class("toolbar")

        # 左侧空白
        left_space = Gtk.Box()
        left_space.set_hexpand(True)
        toolbar.append(left_space)

        # 状态信息
        status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        toolbar.append(status_box)

        # 当前壁纸
        using_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        using_label = Gtk.Label(label="CURRENTLY USING :")
        using_label.add_css_class("status-label")
        using_box.append(using_label)
        self.active_wp_label = Gtk.Label(label="-")
        self.active_wp_label.add_css_class("status-value")
        self.active_wp_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.active_wp_label.set_max_width_chars(32)
        using_box.append(self.active_wp_label)
        status_box.append(using_box)

        # 分隔
        status_box.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))

        # 停止按钮
        stop_btn = Gtk.Button(label="⏹ Stop")
        stop_btn.add_css_class("mode-btn")
        stop_btn.connect("clicked", lambda _: self.controller.stop())
        status_box.append(stop_btn)

        # 刷新壁纸列表（无需重启应用即可加载新壁纸）
        refresh_btn = Gtk.Button(label="⟳ Refresh")
        refresh_btn.add_css_class("mode-btn")
        refresh_btn.connect("clicked", self.on_reload_wallpapers)
        status_box.append(refresh_btn)

        # 随机挑选一张壁纸
        lucky_btn = Gtk.Button(label="🎲 I'm feeling lucky")
        lucky_btn.add_css_class("mode-btn")
        lucky_btn.connect("clicked", self.on_feeling_lucky)
        status_box.append(lucky_btn)

        # 右侧空白
        right_space = Gtk.Box()
        right_space.set_hexpand(True)
        toolbar.append(right_space)

        # 视图切换
        view_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.append(view_box)

        self.btn_grid = Gtk.ToggleButton(label="⊞ Grid")
        self.btn_grid.add_css_class("mode-btn")
        self.btn_grid.set_active(True)
        self.btn_grid.connect("toggled", self.on_view_grid)
        view_box.append(self.btn_grid)

        self.btn_list = Gtk.ToggleButton(label="☰ List")
        self.btn_list.add_css_class("mode-btn")
        self.btn_list.connect("toggled", self.on_view_list)
        view_box.append(self.btn_list)

        parent.append(toolbar)

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
        self.sidebar.append(sidebar_scroll)

        sidebar_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
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

        self.sidebar_tags = Gtk.FlowBox()
        self.sidebar_tags.set_selection_mode(Gtk.SelectionMode.NONE)
        self.sidebar_tags.set_max_children_per_line(4)
        self.sidebar_tags.set_margin_start(20)
        self.sidebar_tags.set_margin_end(20)
        sidebar_content.append(self.sidebar_tags)

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

        for folder_id, wp in self.wp_manager._wallpapers.items():
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

        for folder_id, wp in self.wp_manager._wallpapers.items():
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
        self.path_entry.set_text(WORKSHOP_PATH)
        self.path_entry.set_hexpand(True)
        path_row.append(self.path_entry)

        # Screen Root (Multi-monitor support)
        screen_row = self.create_setting_row("Screen Root", "XRandR/Wayland screen name, e.g. eDP-1.")
        screen_row.set_orientation(Gtk.Orientation.VERTICAL)
        box.append(screen_row)
        self.screen_entry = Gtk.Entry()
        self.screen_entry.set_text(str(self.config.get("lastScreen", "eDP-1")))
        self.screen_entry.set_hexpand(True)
        screen_row.append(self.screen_entry)

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
        # 确保保存有效的屏幕名称
        screen_input = self.screen_entry.get_text().strip()
        self.config.set("lastScreen", screen_input if screen_input else "eDP-1")

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
