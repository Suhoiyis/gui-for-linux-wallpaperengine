import sys
import os
import platform
import shutil
import html
import gi

import socket
import threading

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, Gdk, GLib

from py_GUI.const import CSS_STYLE, APP_ID, WORKSHOP_PATH, VERSION
from py_GUI.core.config import ConfigManager
from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.screen import ScreenManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.logger import LogManager
from py_GUI.core.nickname import NicknameManager
from py_GUI.core.history import HistoryManager
from py_GUI.utils import markdown_to_pango

from py_GUI.ui.components.navbar import NavBar
from py_GUI.ui.components.history_dialog import HistoryDialog
from py_GUI.ui.components.welcome_dialog import WelcomeDialog
from py_GUI.ui.components.command_palette import CommandPalette
from py_GUI.ui.components.dialogs import show_update_dialog
from py_GUI.ui.pages.wallpapers import WallpapersPage
from py_GUI.ui.pages.settings import SettingsPage
from py_GUI.ui.pages.performance import PerformancePage
from py_GUI.ui.tray import TrayIcon
from py_GUI.ui.compact_window import CompactWindow
from py_GUI.core.updater import UpdateChecker
from py_GUI.core.integrations import AppIntegrator
from py_GUI.core.state import AppStateBus, StateManager
from py_GUI.core.migration import StorageMigrationManager
from py_GUI.core.playlists import PlaylistService, FAVORITES_PLAYLIST_ID


def get_debug_info():
    import platform, sys, shutil, os
    from gi.repository import Gtk, Adw

    info = []
    info.append("System Environment")
    info.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    try:
        os_info = f"{platform.system()} {platform.release()}"
        info.append(f"OS: {os_info}")
    except Exception:
        info.append("OS: Unknown")

    try:
        py_version = sys.version.split()[0]
        info.append(f"Python: {py_version}")
    except Exception:
        info.append("Python: Unknown")

    try:
        gtk_version = f"{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}"
        info.append(f"GTK: {gtk_version}")
    except Exception:
        info.append("GTK: Unknown")

    try:
        adw_version = f"{Adw.get_major_version()}.{Adw.get_minor_version()}.{Adw.get_micro_version()}"
        info.append(f"Libadwaita: {adw_version}")
    except Exception:
        info.append("Libadwaita: Unknown")

    try:
        display_server = os.environ.get("XDG_SESSION_TYPE", "unknown").capitalize()
        info.append(f"Display Server: {display_server}")
    except Exception:
        info.append("Display Server: Unknown")

    try:
        backend_found = shutil.which("linux-wallpaperengine") is not None
        backend_status = "✓ Found" if backend_found else "✗ Not found"
        info.append(f"Backend (linux-wallpaperengine): {backend_status}")
    except Exception:
        info.append("Backend: Unknown")

    return "\n".join(info)


def get_latest_changelog():
    import os
    import re

    changelog_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs/CHANGELOG.md"
    )
    if not os.path.exists(changelog_path):
        return "<p>No changelog found.</p>"

    try:
        with open(changelog_path, "r", encoding="utf-8") as f:
            content = f.read()

        sections = re.split(r"\n## ", content)
        for section in sections:
            section = section.strip()
            if not section:
                continue

            is_version = section.startswith("v")
            is_latest = "最新更新" in section

            if is_version or is_latest:
                lines = section.split("\n")
                header = lines[0].strip()
                body_lines = lines[1:]

                processed_lines = []
                in_list = False

                for line in body_lines:
                    line = line.strip()
                    if line.startswith("---"):
                        break

                    if not line:
                        continue

                    if line.startswith("###"):
                        if in_list:
                            processed_lines.append("</ul>")
                            in_list = False
                        # Escape the text content before wrapping in tags
                        section_title = html.escape(line.replace("###", "").strip())
                        processed_lines.append(f"<p><em>{section_title}</em></p>")
                    elif line.startswith("-"):
                        if not in_list:
                            processed_lines.append("<ul>")
                            in_list = True
                        item_text = line.replace("-", "", 1).strip()
                        # Escape raw text first, then apply formatting
                        item_text = html.escape(item_text)
                        item_text = item_text.replace("**", "<em>", 1).replace(
                            "**", "</em>", 1
                        )
                        processed_lines.append(f"  <li>{item_text}</li>")
                    else:
                        if in_list:
                            processed_lines.append("</ul>")
                            in_list = False
                        # Escape the paragraph text
                        escaped_line = html.escape(line)
                        processed_lines.append(f"<p>{escaped_line}</p>")

                if in_list:
                    processed_lines.append("</ul>")

                content_html = "\n".join(processed_lines)
                if not content_html.strip() or content_html.strip() == "(暂无)":
                    continue

                # Escape header before wrapping in tags
                escaped_header = html.escape(header)
                return f"<p><em>{escaped_header}</em></p>" + content_html
    except Exception as e:
        return f"<p>Error reading changelog: {str(e)}</p>"

    return "<p>Check CHANGELOG.md for details.</p>"


class WallpaperApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id=APP_ID, flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        )
        self.config = ConfigManager()
        self.log_manager = LogManager()
        self.state_bus = AppStateBus()
        self.state_manager = StateManager(self.state_bus)
        self.migration_manager = StorageMigrationManager(
            log_info=self.log_manager.add_info,
            log_error=self.log_manager.add_error,
        )
        self.migration_manager.migrate_if_needed()
        self.history_manager = HistoryManager(self.config)

        workshop_path = self.config.get("workshopPath", WORKSHOP_PATH)
        self.wp_manager = WallpaperManager(workshop_path)
        self.prop_manager = PropertiesManager(self.config)
        self.screen_manager = ScreenManager()
        self.nickname_manager = NicknameManager(self.config)
        self.controller = WallpaperController(
            self.config,
            self.prop_manager,
            self.log_manager,
            self.screen_manager,
            state_manager=self.state_manager,
            signal_bus=self.state_bus,
        )
        self.controller.wp_manager = self.wp_manager
        self.controller.nickname_manager = self.nickname_manager
        self.controller.history_manager = self.history_manager
        self.playlists = PlaylistService(self.config, self.state_bus)

        self.start_hidden = False
        self.cli_actions = []
        self.initialized = False
        self._is_first_activation = True
        self.cycle_timer_id = None
        self.command_palette = None

        self.app_integrator = AppIntegrator()
        self.update_checker = UpdateChecker()

        self.tray = TrayIcon(self)

        self.state_bus.connect("state-changed", self._on_state_changed)
        self.state_bus.connect(
            "screenshot-history-changed", self._on_screenshot_history_changed
        )

    def _on_state_changed(self, *_):
        if hasattr(self, "wallpapers_page"):
            self.wallpapers_page.update_active_wallpaper_label()
        if hasattr(self, "performance_page"):
            self.performance_page.refresh_screenshot_history_safe()
        GLib.timeout_add(200, self.update_tray_status)

    def _on_screenshot_history_changed(self, *_):
        if hasattr(self, "performance_page"):
            self.performance_page.refresh_screenshot_history_safe()

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
            elif arg == "--stop":
                self.cli_actions.append("stop")
            elif arg == "--random":
                self.cli_actions.append("random")
            elif arg == "--quit":
                self.cli_actions.append("quit")

        self.activate()
        return 0

    def do_activate(self):
        if self.initialized:
            if self._is_first_activation and not self.start_hidden:
                self.show_window()
            self._is_first_activation = False
            self.start_hidden = False
            self.consume_cli_actions()

            GLib.timeout_add(1500, self.update_tray_status)
            return

        # Load CSS
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS_STYLE.encode("utf-8"))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Setup Icon Theme
        display = Gdk.Display.get_default()
        icon_theme = Gtk.IconTheme.get_for_display(display)

        # Add 'pic' directory to icon search path
        # py_GUI/ui/app.py -> .../linux-wallpaperengine-gui/
        base_path = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        pic_path = os.path.join(base_path, "pic/icons")

        if os.path.exists(pic_path):
            icon_theme.add_search_path(pic_path)

        self.win = Gtk.ApplicationWindow(application=self)
        self.win.set_title("Linux Wallpaper Engine GUI")
        self.win.set_icon_name(APP_ID)  # Matches GUI_rounded.png in pic/icons/
        self.win.set_default_size(1200, 800)
        self.win.set_size_request(1000, 700)
        self.win.connect("close-request", self.on_window_close)

        key_ctrl = Gtk.EventControllerKey.new()
        key_ctrl.connect("key-pressed", self._on_global_key_pressed)
        self.win.add_controller(key_ctrl)

        # Setup Actions
        self.setup_actions()

        self.toast_overlay = Adw.ToastOverlay()
        self.win.set_child(self.toast_overlay)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.toast_overlay.set_child(main_box)

        # Stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_vexpand(True)

        # Navbar
        screens = self.screen_manager.get_screens()
        selected_screen = (
            self.state_manager.get_last_screen()
            or self.screen_manager.get_primary_screen()
            or "eDP-1"
        )
        initial_link_state = self.config.get("apply_mode") == "same"
        initial_compact_state = bool(self.config.get("compact_mode"))

        self.navbar = NavBar(
            self.stack,
            screens=screens,
            selected_screen=selected_screen,
            on_home_enter=self.on_home_enter,
            on_screen_changed=self.on_navbar_screen_changed,
            on_link_toggled=self.on_navbar_link_toggled,
            on_restart_app=self.restart_app,
            on_compact_mode_toggled=self.on_compact_mode_toggled,
            initial_link_state=initial_link_state,
            initial_compact_state=initial_compact_state,
        )
        main_box.append(self.navbar)
        main_box.append(self.stack)

        # Pages
        self.wallpapers_page = WallpapersPage(
            self.win,
            self.config,
            self.wp_manager,
            self.prop_manager,
            self.controller,
            self.log_manager,
            self.screen_manager,
            self.nickname_manager,
            self.playlists,
            self.show_toast,
        )
        self.stack.add_named(self.wallpapers_page, "wallpapers")

        # Performance Page
        self.performance_page = PerformancePage(self.controller)
        self.stack.add_named(self.performance_page, "performance")

        self.settings_page = SettingsPage(
            self.win,
            self.config,
            self.screen_manager,
            self.log_manager,
            self.controller,
            self.wp_manager,
            self.nickname_manager,
            self.playlists,
            on_cycle_changed=self.setup_cycle_timer,
            show_toast=self.show_toast,
        )
        self.stack.add_named(self.settings_page, "settings")

        self.controller.set_toast_callback(self.show_toast)

        self.compact_win = CompactWindow(
            app=self,
            wp_manager=self.wp_manager,
            controller=self.controller,
            config=self.config,
            log_manager=self.log_manager,
            screen_manager=self.screen_manager,
            nickname_manager=self.nickname_manager,
            show_toast=self.show_toast,
            on_compact_mode_toggled=self.on_compact_mode_toggled,
            on_restart_app=self.restart_app,
        )
        self.compact_win.set_icon_name("GUI")

        self.wp_manager.scan()
        self.nickname_manager.cleanup(list(self.wp_manager._wallpapers.keys()))
        self.wallpapers_page.refresh_wallpaper_grid()

        if self.wp_manager.last_scan_error:
            GLib.timeout_add(
                500,
                lambda: (
                    self.show_toast(f"⚠️ {self.wp_manager.last_scan_error}") or False
                ),
            )

        # Restore last session wallpapers
        active_monitors = self.state_manager.get_active_monitors()
        screens = self.screen_manager.get_screens()

        # Ensure lastScreen always points to a connected screen (fallback to first/primary)
        last_screen = self.state_manager.get_last_screen()
        if not last_screen or last_screen not in screens:
            last_screen = self.screen_manager.get_primary_screen() or (
                screens[0] if screens else "eDP-1"
            )
            self.state_manager.set_last_screen(last_screen)

        if active_monitors:
            # Fill in missing lastWallpaper for CLI/apply-last correctness
            if not self.state_manager.get_last_wallpaper():
                if last_screen in active_monitors:
                    self.state_manager.set_last_wallpaper(active_monitors[last_screen])
                elif active_monitors:
                    self.state_manager.set_last_wallpaper(
                        next(iter(active_monitors.values()))
                    )

            # Re-launch wallpapers using saved mapping
            self.controller.restart_wallpapers()
            GLib.timeout_add(300, self.wallpapers_page.update_active_wallpaper_label)
            # Do not override user selection; only select current if none
            GLib.timeout_add(
                350,
                lambda: self.wallpapers_page.show_current_wallpaper_in_sidebar(False),
            )
        else:
            # Legacy fallback: apply last single wallpaper
            last_wp = self.state_manager.get_last_wallpaper()
            if last_wp:
                self.wallpapers_page.select_wallpaper(last_wp)
                GLib.timeout_add(500, lambda: self.auto_apply(last_wp))

        if self.start_hidden:
            self.win.set_visible(False)
            self.compact_win.set_visible(False)
        elif initial_compact_state:
            self.win.set_visible(False)
            wp_ids = self.wallpapers_page._current_wp_ids
            self.compact_win.sync_from_main(wp_ids, None)
            self.compact_win.set_visible(True)
            self.compact_win.present()
            GLib.timeout_add(100, lambda: self.compact_win.present() or False)
        else:
            self.win.set_visible(True)
            self.win.present()
            GLib.timeout_add(100, lambda: self.win.present() or False)
        self.start_hidden = False

        self.initialized = True
        self._is_first_activation = False
        self.check_onboarding()
        self._check_shortcut_updates()
        self.setup_cycle_timer()

        self.start_ipc_server()

        self.tray.start()

        if self.tray.process and self.tray.process.pid:
            self.controller.perf_monitor.start_monitoring("tray", self.tray.process.pid)

        self.consume_cli_actions()

        # 1. 延迟 1.5 秒发送初始状态
        GLib.timeout_add(1500, self.update_tray_status)

        # 2. 开启 1 秒一次的智能心跳守护线程 (通过 or True 强制保持循环)
        # 无论用户通过什么刁钻的方式在内部换了壁纸，托盘绝对会在 1 秒内发现并跟上！
        if not hasattr(self, "_tray_loop_started"):
            self._tray_loop_started = True
            GLib.timeout_add_seconds(1, lambda: self.update_tray_status() or True)

    def start_ipc_server(self):
        """监听来自 Rust 托盘的极速 Abstract Socket 指令 (0 文件残留)"""
        socket_name = os.getenv("LWG_IPC_SOCKET", f"lwg-ipc-{os.getuid()}")
        abstract_addr = f"\x00{socket_name}"

        def _server_thread():
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as srv:
                try:
                    # 🛡️ Copilot 建议的保护罩：防止多开应用时因地址被占用导致线程脏崩溃
                    srv.bind(abstract_addr)
                    srv.listen(5)
                except OSError as e:
                    # 将错误安全地抛给主线程的日志管理器，然后体面地结束这个冗余线程
                    GLib.idle_add(
                        lambda: self.log_manager.add_info(
                            f"IPC Server 绑定失败 (可能已有一个实例正在运行): {e}",
                            "App",
                        )
                    )
                    return

                while True:
                    try:
                        conn, _ = srv.accept()
                        with conn:
                            data = conn.recv(1024).decode().strip()
                            if not data:
                                continue

                            if data == "--show":
                                GLib.idle_add(self.show_window)
                            elif data == "--toggle":
                                GLib.idle_add(self.toggle_window)
                            elif data == "--stop":
                                GLib.idle_add(self.stop_wallpaper)
                            elif data == "--apply-last":
                                GLib.idle_add(self.apply_last_from_cli)
                            elif data == "--random":
                                GLib.idle_add(self.random_wallpaper)
                            elif data == "--quit":
                                GLib.idle_add(self.quit_app)
                    except Exception:
                        pass

        t = threading.Thread(target=_server_thread, daemon=True)
        t.start()

    def auto_apply(self, wp_id):
        if wp_id:
            self.controller.apply(wp_id)
            # Update UI state
            self.wallpapers_page.active_wp = wp_id
            wp = self.wp_manager._wallpapers.get(wp_id)
            if wp:
                self.wallpapers_page.active_wp_label.set_markup(
                    markdown_to_pango(wp["title"])
                )

            # 【新增】确保自动应用壁纸时激活计时器
            self.setup_cycle_timer()
        GLib.timeout_add(500, self.update_tray_status)
        return False

    def on_window_close(self, win):
        self.hide_window()
        return True

    def show_window(self):
        is_compact = self.config.get("compact_mode", False)
        if is_compact:
            self.compact_win.set_visible(True)
            self.compact_win.present()
            # 加上这句：给 WM 100ms 的反应时间后，再强行夺取一次焦点
            GLib.timeout_add(100, lambda: self.compact_win.present() or False)
        else:
            self.win.set_visible(True)
            self.win.present()
            # 加上这句：给 WM 100ms 的反应时间后，再强行夺取一次焦点
            GLib.timeout_add(100, lambda: self.win.present() or False)

    def show_toast(self, message: str, timeout: int = 3):
        if hasattr(self, "toast_overlay"):
            toast = Adw.Toast.new(message)
            toast.set_timeout(timeout)
            self.toast_overlay.add_toast(toast)

    def hide_window(self):
        self.win.set_visible(False)
        if hasattr(self, "compact_win"):
            self.compact_win.set_visible(False)

    def toggle_window(self):
        """智能 Toggle 逻辑 (Smart Toggle)"""
        is_compact = self.config.get("compact_mode", False)

        # 确定当前应该操作哪个窗口
        target_win = getattr(self, "compact_win", None) if is_compact else self.win

        if not target_win:
            self.show_window()
            return

        # 核心逻辑：
        # is_active() 能够判断该窗口是否是当前桌面系统里“正在被聚焦/置顶”的活跃窗口
        if target_win.get_visible() and target_win.is_active():
            # 状态 1：窗口已打开，并且就在最前面（拥有焦点） -> 隐藏它
            self.hide_window()
        else:
            # 状态 2：窗口被关了，或者被别的窗口挡住了，或者在别的工作区 -> 唤醒并置顶！
            self.show_window()

    def on_home_enter(self):
        try:
            self.wallpapers_page.update_active_wallpaper_label()
            self.wallpapers_page.show_current_wallpaper_in_sidebar(False)
        except Exception:
            pass

    def _on_global_key_pressed(self, controller, keyval, keycode, state):
        ctrl = bool(state & Gdk.ModifierType.CONTROL_MASK)
        meta = bool(state & Gdk.ModifierType.META_MASK)
        if keyval in (Gdk.KEY_k, Gdk.KEY_K) and (ctrl or meta):
            self.open_command_palette()
            return True
        return False

    def _build_palette_items(self):
        items = []

        items.append(
            {
                "label": "Stop All",
                "group": "Action",
                "keywords": "stop end",
                "action": "stop",
            }
        )
        items.append(
            {
                "label": "Random Wallpaper",
                "group": "Action",
                "keywords": "random lucky",
                "action": "random",
            }
        )
        items.append(
            {
                "label": "Open Settings",
                "group": "Action",
                "keywords": "settings preferences",
                "action": "open_settings",
            }
        )
        items.append(
            {
                "label": "Open Performance",
                "group": "Action",
                "keywords": "performance monitor",
                "action": "open_performance",
            }
        )

        for pid, wp in self.wp_manager._wallpapers.items():
            title = str(wp.get("title", pid))
            nickname = ""
            if self.nickname_manager:
                nickname = self.nickname_manager.get(pid) or ""
            tags = wp.get("tags", [])
            tags_text = (
                " ".join([str(t) for t in tags])
                if isinstance(tags, list)
                else str(tags or "")
            )
            items.append(
                {
                    "label": f"Apply: {title}",
                    "group": "Wallpaper",
                    "keywords": f"{title} {pid} {nickname} {tags_text}",
                    "action": "apply_wallpaper",
                    "wallpaper_id": pid,
                }
            )

        for p in self.playlists.get_playlists():
            pid = str(p.get("id", ""))
            name = str(p.get("name", ""))
            if not pid or not name:
                continue
            items.append(
                {
                    "label": f"Filter Playlist: {name}",
                    "group": "Playlist",
                    "keywords": f"playlist {name} {pid}",
                    "action": "filter_playlist",
                    "playlist_id": pid,
                }
            )

        try:
            entries = self.history_manager.get_all()[:20]
            for entry in entries:
                wid = str(entry.get("id", ""))
                title = str(entry.get("title", wid))
                if not wid:
                    continue
                items.append(
                    {
                        "label": f"History: {title}",
                        "group": "History",
                        "keywords": f"history {title} {wid}",
                        "action": "apply_wallpaper",
                        "wallpaper_id": wid,
                    }
                )
        except Exception:
            pass

        return items

    def _execute_palette_item(self, item):
        action = item.get("action")
        if action == "stop":
            self.stop_wallpaper()
            return
        if action == "random":
            self.random_wallpaper()
            return
        if action == "open_settings":
            self.stack.set_visible_child_name("settings")
            self.navbar.btn_settings.set_active(True)
            return
        if action == "open_performance":
            self.stack.set_visible_child_name("performance")
            self.navbar.btn_performance.set_active(True)
            return
        if action == "filter_playlist":
            pid = item.get("playlist_id")
            if hasattr(self, "wallpapers_page") and pid is not None:
                self.stack.set_visible_child_name("wallpapers")
                self.navbar.btn_home.set_active(True)
                self.wallpapers_page.selected_playlist_filter = str(pid)
                self.wallpapers_page.on_playlists_changed("palette-filter")
            return
        if action == "apply_wallpaper":
            wid = item.get("wallpaper_id")
            if wid and str(wid) in self.wp_manager._wallpapers:
                self.wallpapers_page.select_wallpaper(str(wid))
                self.wallpapers_page.apply_wallpaper(str(wid))
                self.setup_cycle_timer()

    def open_command_palette(self):
        if self.command_palette and self.command_palette.get_visible():
            self.command_palette.present_with_focus()
            return
        self.command_palette = CommandPalette(
            self.win, self._build_palette_items, self._execute_palette_item
        )
        self.command_palette.connect(
            "destroy", lambda *_: setattr(self, "command_palette", None)
        )
        self.command_palette.present_with_focus()

    def on_navbar_screen_changed(self, screen: str):
        self.state_manager.set_last_screen(screen)
        if hasattr(self, "wallpapers_page"):
            self.wallpapers_page.selected_screen = screen
            self.wallpapers_page.update_active_wallpaper_label()

    def on_navbar_link_toggled(self, is_linked: bool):
        mode = "same" if is_linked else "diff"
        self.config.set("apply_mode", mode)
        if hasattr(self, "wallpapers_page"):
            self.wallpapers_page.apply_mode = mode
            self.log_manager.add_info(f"Apply mode changed to: {mode}", "App")

    def on_compact_mode_toggled(self, is_compact: bool):
        self.config.set("compact_mode", is_compact)

        if is_compact:
            self.win.set_visible(False)
            wp_ids = self.wallpapers_page._current_wp_ids
            selected_wp = self.wallpapers_page.selected_wp
            self.compact_win.sync_from_main(wp_ids, selected_wp)
            self.compact_win.set_visible(True)
            self.compact_win.present()
        else:
            self.compact_win.set_visible(False)
            self.win.set_visible(True)
            self.win.present()
            self.navbar.set_compact_active(False)

        self.log_manager.add_info(
            f"Compact mode: {'enabled' if is_compact else 'disabled'}", "App"
        )

    def refresh_from_cli(self):
        self.wallpapers_page.on_reload_wallpapers(None)

    def apply_last_from_cli(self):
        last_wp = self.state_manager.get_last_wallpaper()
        if last_wp:
            self.auto_apply(last_wp)

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
            elif action == "stop":
                self.stop_wallpaper()
            elif action == "random":
                self.random_wallpaper()
            elif action == "quit":
                self.quit_app()

    def stop_wallpaper(self):
        # Tray stop means STOP ALL
        self.controller.stop()
        self.state_manager.clear_active_monitors()
        self.wallpapers_page.update_active_wallpaper_label()

        # 【新增】停止播放时，顺便把轮换计时器也停掉
        self.setup_cycle_timer()

        GLib.timeout_add(500, self.update_tray_status)

    def update_tray_status(self):
        """利用 Pango Markup 增强多屏 ToolTip，并附带状态 Flag 让 Rust 切换图标"""
        import html

        try:
            active = self.state_manager.get_active_monitors()
            text = "Stopped"
            state_flag = "STOPPED"  # 👈 默认状态为停止

            if active:
                state_flag = "ACTIVE"  # 👈 如果有壁纸，状态改为运行
                if len(active) == 1:
                    ui_name = self.wallpapers_page.active_wp_label.get_text()
                    if not ui_name or ui_name in ["-", "None"]:
                        ui_name = "Loading..."
                    safe_name = html.escape(ui_name)
                    text = f"<b>Running:</b> <i>{safe_name}</i>"
                else:
                    # ... (这里的多屏遍历拼接逻辑保持完全不变) ...
                    names = []
                    for screen_name, wp_id in active.items():
                        display_name = wp_id
                        wp = getattr(
                            self, "wp_manager", None
                        ) and self.wp_manager._wallpapers.get(wp_id)
                        if wp:
                            try:
                                res = self.nickname_manager.get_display_name(wp)
                                display_name = res[0] if isinstance(res, tuple) else res
                            except Exception:
                                display_name = wp.get("title", wp_id)

                        if len(display_name) > 18:
                            display_name = display_name[:17] + "…"

                        safe_screen = html.escape(screen_name)
                        safe_display = html.escape(display_name)
                        names.append(f"  • <b>{safe_screen}</b>: <i>{safe_display}</i>")

                    joined_names = "\n".join(names)
                    text = f"<b>Running:</b>\n{joined_names}"

            # ✨ 核心改动：把状态和文本用 "|" 拼起来一起发过去
            payload = f"{state_flag}|{text}"

            if getattr(self, "_last_tray_text", None) != payload:
                self.tray.update_tooltip(payload)
                self._last_tray_text = payload

        except Exception as e:
            from py_GUI.ui.tray import log_main

            log_main(f"Error computing tray status: {e}")

        return False

    def random_wallpaper(self):
        # Triggered by cycle timer or CLI or Menu
        # Cycle order logic
        cycle_order = self.config.get("cycleOrder") or "random"
        active_monitors = self.state_manager.get_active_monitors()

        screens = self.screen_manager.get_screens()

        # If no monitors active, activate on the last used screen or first available
        if not active_monitors:
            target = (
                self.state_manager.get_last_screen()
                or self.screen_manager.get_primary_screen()
                or (screens[0] if screens else "eDP-1")
            )
            active_monitors[target] = None  # Placeholder

        all_wps = list(self.wp_manager._wallpapers.keys())
        if not all_wps:
            return

        cycle_playlist_id = self.config.get("cyclePlaylistId")
        candidate_wps = list(all_wps)
        if cycle_playlist_id:
            playlist = self.playlists.get_playlist(str(cycle_playlist_id))
            if playlist:
                selected_ids = [
                    wid
                    for wid in playlist.get("wallpaper_ids", [])
                    if wid in set(all_wps)
                ]
                if selected_ids:
                    candidate_wps = selected_ids

        import random

        new_monitors = {}

        # Get sorted list if needed
        sorted_ids = []
        if cycle_order != "random":
            sorted_ids = self.wp_manager.get_sorted_wallpapers(cycle_order)
            allowed = set(candidate_wps)
            sorted_ids = [wid for wid in sorted_ids if wid in allowed]
            # Fallback to random if sort fails or empty
            if not sorted_ids:
                sorted_ids = candidate_wps
                cycle_order = "random"

        for scr in active_monitors.keys():
            if scr in screens:
                if cycle_order == "random":
                    wp_id = random.choice(candidate_wps)
                else:
                    # Sequential logic
                    current_wp = active_monitors.get(scr)
                    next_index = 0
                    if current_wp and current_wp in sorted_ids:
                        current_index = sorted_ids.index(current_wp)
                        next_index = (current_index + 1) % len(sorted_ids)
                    else:
                        # If current not found or None, start from 0
                        next_index = 0

                    wp_id = sorted_ids[next_index]

                new_monitors[scr] = wp_id

        if new_monitors:
            self.state_manager.set_active_monitors(new_monitors)
            # Update lastScreen/lastWallpaper for proper restore & tray apply-last
            primary_screen = self.state_manager.get_last_screen()
            if primary_screen not in new_monitors:
                primary_screen = next(iter(new_monitors.keys()))
                self.state_manager.set_last_screen(primary_screen)

            self.state_manager.set_last_wallpaper(new_monitors.get(primary_screen))

            self.controller.restart_wallpapers()
            self.wallpapers_page.update_active_wallpaper_label()

            self.log_manager.add_info(f"Cycled wallpaper ({cycle_order})", "App")

            # 【新增】每次切完随机壁纸，重置/启动一轮新的倒计时
            self.setup_cycle_timer()

        GLib.timeout_add(500, self.update_tray_status)

    def on_cycle_trigger(self):
        self.log_manager.add_info("Cycling wallpaper...", "App")
        self.random_wallpaper()

        # 【终极修复】必须返回 False！
        # 因为 random_wallpaper 内部会调用 setup_cycle_timer 创建全新的计时器。
        # 如果这里返回 True，旧计时器就会被 GLib 强行复活，变成无法被 stop 杀掉的幽灵！
        return False

    def setup_cycle_timer(self):
        if self.cycle_timer_id:
            GLib.source_remove(self.cycle_timer_id)
            self.cycle_timer_id = None

        # 获取当前正在播放的显示器字典
        active_monitors = self.state_manager.get_active_monitors()

        # 只有在设置开启，且当前确有壁纸在播放时，才启动计时器
        if self.config.get("cycleEnabled") and active_monitors:
            interval_mins = self.config.get("cycleInterval") or 15
            # Minimum 1 minute safety
            interval_mins = max(1, interval_mins)
            self.cycle_timer_id = GLib.timeout_add_seconds(
                interval_mins * 60, self.on_cycle_trigger
            )
            self.log_manager.add_info(
                f"Wallpaper cycling enabled (every {interval_mins} mins)", "App"
            )
        else:
            # 打印更精准的日志状态
            state = (
                "disabled"
                if not self.config.get("cycleEnabled")
                else "paused (no active wallpaper)"
            )
            self.log_manager.add_info(f"Wallpaper cycling {state}", "App")

    def check_onboarding(self):
        needs_onboarding = not self.config.get("onboardingCompleted", False)
        if needs_onboarding:
            self.show_welcome_wizard()

    def _check_shortcut_updates(self):
        try:
            self.app_integrator.check_and_update_shortcut()
            self.log_manager.add_info("App shortcuts updated", "App")
        except Exception as e:
            self.log_manager.add_info(f"Shortcut update check skipped: {str(e)}", "App")

    def quit_app(self):
        self.controller.stop()
        self.tray.stop()
        self.quit()

    def restart_app(self):
        self.log_manager.add_info("Restarting application...", "App")
        self.controller.stop()
        self.tray.stop()

        import os
        import sys
        import subprocess

        # 提取去掉首位脚本名和隐藏参数后的干净参数
        args = [arg for arg in sys.argv[1:] if arg not in ("--hidden", "--minimized")]

        appimage_path = os.environ.get("APPIMAGE")
        if appimage_path:
            # 【AppImage 环境重启】
            # 使用外部文件的绝对路径，启动一个完全独立的新会话 (start_new_session=True)
            # 这样新进程就不会受当前进程 FUSE 销毁的影响
            cmd = [appimage_path] + args
            subprocess.Popen(cmd, start_new_session=True, cwd=os.path.expanduser("~"))
            self.quit()
            sys.exit(0)
        else:
            # 【源码环境重启】
            # 传统的进程替换方式
            cmd = [sys.executable, sys.argv[0]] + args
            os.execv(sys.executable, cmd)

    def setup_actions(self):
        action_apply = Gio.SimpleAction.new("apply", GLib.VariantType.new("s"))
        action_apply.connect("activate", self.on_action_apply)
        self.win.add_action(action_apply)

        action_stop = Gio.SimpleAction.new("stop", None)
        action_stop.connect("activate", self.on_action_stop)
        self.win.add_action(action_stop)

        action_delete = Gio.SimpleAction.new("delete", GLib.VariantType.new("s"))
        action_delete.connect("activate", self.on_action_delete)
        self.win.add_action(action_delete)

        action_open_folder = Gio.SimpleAction.new(
            "open_folder", GLib.VariantType.new("s")
        )
        action_open_folder.connect("activate", self.on_action_open_folder)
        self.win.add_action(action_open_folder)

        action_refresh = Gio.SimpleAction.new("refresh", None)
        action_refresh.connect("activate", self.on_action_refresh)
        self.win.add_action(action_refresh)

        action_restart = Gio.SimpleAction.new("restart", None)
        action_restart.connect("activate", self.on_action_restart)
        self.win.add_action(action_restart)

        action_about = Gio.SimpleAction.new("about", None)
        action_about.connect("activate", self.on_action_about)
        self.win.add_action(action_about)

        action_quit_app = Gio.SimpleAction.new("quit_app", None)
        action_quit_app.connect("activate", self.on_action_quit_request)
        self.win.add_action(action_quit_app)

        action_show_history = Gio.SimpleAction.new("show_history", None)
        action_show_history.connect("activate", self.on_action_show_history)
        self.win.add_action(action_show_history)

        action_welcome = Gio.SimpleAction.new("welcome", None)
        action_welcome.connect("activate", self.on_action_welcome)
        self.win.add_action(action_welcome)

        action_check_update = Gio.SimpleAction.new("check_update", None)
        action_check_update.connect("activate", self.on_action_check_update)
        self.win.add_action(action_check_update)

        action_toggle_favorite = Gio.SimpleAction.new(
            "toggle_favorite", GLib.VariantType.new("s")
        )
        action_toggle_favorite.connect("activate", self.on_action_toggle_favorite)
        self.win.add_action(action_toggle_favorite)

        action_add_to_playlist = Gio.SimpleAction.new(
            "add_to_playlist", GLib.VariantType.new("(ss)")
        )
        action_add_to_playlist.connect("activate", self.on_action_add_to_playlist)
        self.win.add_action(action_add_to_playlist)

        action_remove_from_playlist = Gio.SimpleAction.new(
            "remove_from_playlist", GLib.VariantType.new("(ss)")
        )
        action_remove_from_playlist.connect(
            "activate", self.on_action_remove_from_playlist
        )
        self.win.add_action(action_remove_from_playlist)

    def on_action_apply(self, action, param):
        wp_id = param.get_string()
        if wp_id:
            self.wallpapers_page.select_wallpaper(wp_id)
            self.wallpapers_page.apply_wallpaper(wp_id)
            self.setup_cycle_timer()

            GLib.timeout_add(500, self.update_tray_status)

    def on_action_stop(self, action, param):
        self.stop_wallpaper()

    def on_action_delete(self, action, param):
        wp_id = param.get_string()
        if wp_id:
            self.wallpapers_page.delete_wallpaper(wp_id)

    def on_action_open_folder(self, action, param):
        wp_id = param.get_string()
        if wp_id:
            self.wallpapers_page.open_wallpaper_folder(wp_id)

    def on_action_refresh(self, action, param):
        self.refresh_from_cli()

    def on_action_restart(self, action, param):
        self.restart_app()

    def on_action_about(self, action, param):
        try:
            dialog = Adw.AboutDialog(
                application_name="Linux Wallpaper Engine GUI",
                application_icon=APP_ID,
                version=VERSION,
                developer_name="Suhoiyis",
                comments="A modern GTK4 GUI for managing dynamic wallpapers from Steam Workshop on Linux, based on linux-wallpaperengine.",
                license_type=Gtk.License.GPL_3_0,
                website="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine",
                issue_url="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues",
                copyright="© 2026 Suhoiyis",
                release_notes=get_latest_changelog(),
                debug_info=get_debug_info(),
                debug_info_filename="wallpaperengine-gui-debug.txt",
            )
            dialog.present(self.win)
        except Exception as e:
            self.show_toast(f"Error opening About dialog: {str(e)}")

    def on_action_show_history(self, action, param):
        try:
            dialog = HistoryDialog(
                self.win,
                self.history_manager,
                self.wp_manager,
                self.controller,
                self.nickname_manager,
            )
            dialog.present()
        except Exception as e:
            self.show_toast(f"Error opening history: {str(e)}")

    def on_action_welcome(self, action, param):
        try:
            required = not self.config.get("onboardingCompleted", False)
            dialog = WelcomeDialog(
                self.win, self.config, self.app_integrator, is_required=required
            )
            dialog.present()
        except Exception as e:
            self.show_toast(f"Error opening welcome dialog: {str(e)}")

    def on_action_check_update(self, action, param):
        try:

            def on_update_callback(latest_version, release_url, has_update):
                GLib.idle_add(
                    lambda: self._handle_update_result(
                        latest_version, release_url, has_update
                    )
                )

            self.update_checker.check_update(VERSION, on_update_callback)
            self.show_toast("Checking for updates...")
        except Exception as e:
            self.show_toast(f"Error checking for updates: {str(e)}")

    def _handle_update_result(self, latest_version, release_url, has_update):
        show_update_dialog(self.win, VERSION, latest_version, release_url, has_update)

    def on_action_toggle_favorite(self, action, param):
        wp_id = param.get_string()
        if not wp_id:
            return
        now_fav = self.playlists.toggle_favorite(wp_id)
        if hasattr(self, "wallpapers_page"):
            self.wallpapers_page.on_playlists_changed("favorite-toggle")
        self.show_toast("Added to favorites" if now_fav else "Removed from favorites")

    def on_action_add_to_playlist(self, action, param):
        playlist_id, wp_id = param.unpack()
        if not playlist_id or not wp_id:
            return
        try:
            self.playlists.add_wallpaper(str(playlist_id), str(wp_id))
            if hasattr(self, "wallpapers_page"):
                self.wallpapers_page.on_playlists_changed("playlist-item-added")
            self.show_toast("Added to playlist")
        except Exception as e:
            self.show_toast(f"Failed to add to playlist: {e}")

    def on_action_remove_from_playlist(self, action, param):
        playlist_id, wp_id = param.unpack()
        if not playlist_id or not wp_id:
            return
        try:
            self.playlists.remove_wallpaper(str(playlist_id), str(wp_id))
            if hasattr(self, "wallpapers_page"):
                self.wallpapers_page.on_playlists_changed("playlist-item-removed")
            self.show_toast("Removed from playlist")
        except Exception as e:
            self.show_toast(f"Failed to remove from playlist: {e}")

    def show_welcome_wizard(self):
        self.on_action_welcome(None, None)

    def on_action_quit_request(self, action, param):
        dialog = Adw.MessageDialog.new(self.win)
        dialog.set_heading("Quit Application?")
        dialog.set_body(
            "This will stop all running wallpapers and exit the application."
        )
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("quit", "Quit")
        dialog.set_response_appearance("quit", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.connect("response", self.on_quit_dialog_response)
        dialog.present()

    def on_quit_dialog_response(self, dialog, response):
        if response == "quit":
            self.quit_app()


def main():
    # Set program name for WM class matching - must match the .desktop filename
    GLib.set_prgname(APP_ID)
    app = WallpaperApp()
    app.run(sys.argv)
