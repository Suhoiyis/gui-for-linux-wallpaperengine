import os
import shutil
import gi

gi.require_version("Gtk", "4.0")
try:
    gi.require_version("Adw", "1")
except ValueError:
    pass
from gi.repository import Gtk, GLib


class WelcomeDialog(Gtk.Window):
    STEP_TITLES = [
        "Welcome",
        "Requirements Check",
        "Directories",
        "Quick Settings",
        "All Set!",
    ]

    def __init__(self, parent, config, integrator, is_required=False):
        super().__init__(transient_for=parent, modal=True)
        self.config = config
        self.integrator = integrator
        self.is_required = bool(is_required)
        self.current_step = 0

        self.set_title("Welcome")
        self.set_default_size(600, 480)
        self.set_resizable(False)
        self.connect("close-request", self.on_close_request)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_child(root)

        header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        header.set_margin_top(14)
        header.set_margin_bottom(10)
        header.set_margin_start(16)
        header.set_margin_end(16)
        root.append(header)

        self.step_dots = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.step_dots.set_halign(Gtk.Align.CENTER)
        header.append(self.step_dots)

        self.step_title = Gtk.Label(label="")
        self.step_title.add_css_class("dim-label")
        header.append(self.step_title)

        sep_top = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        root.append(sep_top)

        self.stack = Gtk.Stack()
        self.stack.set_hexpand(True)
        self.stack.set_vexpand(True)
        root.append(self.stack)

        self._build_step_0_welcome()
        self._build_step_1_requirements()
        self._build_step_2_directories()
        self._build_step_3_quick_settings()
        self._build_step_4_all_set()

        sep_bottom = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        root.append(sep_bottom)

        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        footer.set_margin_top(10)
        footer.set_margin_bottom(10)
        footer.set_margin_start(16)
        footer.set_margin_end(16)
        root.append(footer)

        self.btn_back = Gtk.Button(label="Back")
        self.btn_back.connect("clicked", self.on_back_clicked)
        footer.append(self.btn_back)

        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        footer.append(spacer)

        self.btn_next = Gtk.Button(label="Continue")
        self.btn_next.add_css_class("suggested-action")
        self.btn_next.connect("clicked", self.on_next_clicked)
        footer.append(self.btn_next)

        self.refresh_step_ui()

    def _mk_page_box(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(24)
        box.set_margin_end(24)
        return box

    def _build_step_0_welcome(self):
        box = self._mk_page_box()
        box.set_valign(Gtk.Align.CENTER)

        logo_path = self._resolve_logo_path()
        if logo_path:
            icon = Gtk.Image.new_from_file(logo_path)
        else:
            icon = Gtk.Image.new_from_icon_name("preferences-desktop-wallpaper")
        icon.set_pixel_size(96)
        icon.set_halign(Gtk.Align.CENTER)
        box.append(icon)

        title = Gtk.Label(label="Linux Wallpaper Engine GUI")
        title.add_css_class("title-2")
        box.append(title)

        desc = Gtk.Label(
            label="A modern GUI for applying Steam Workshop live wallpapers on Linux."
        )
        desc.set_wrap(True)
        desc.set_justify(Gtk.Justification.CENTER)
        desc.add_css_class("dim-label")
        box.append(desc)

        self.stack.add_named(box, "step-0")

    def _build_step_1_requirements(self):
        box = self._mk_page_box()

        self.req_rows = []
        checks = [
            ("linux-wallpaperengine", self._check_backend),
            ("Xvfb (Recommended)", self._check_xvfb),
            ("Wayland Session", self._check_wayland),
        ]
        for name, checker in checks:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            row.add_css_class("card")
            row.set_margin_top(2)
            row.set_margin_bottom(2)
            icon = Gtk.Label(label="⏳")
            icon.set_width_chars(2)
            row.append(icon)
            text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            title = Gtk.Label(label=name)
            title.set_halign(Gtk.Align.START)
            title.add_css_class("heading")
            msg = Gtk.Label(label="Checking...")
            msg.set_halign(Gtk.Align.START)
            msg.add_css_class("dim-label")
            text_box.append(title)
            text_box.append(msg)
            row.append(text_box)
            box.append(row)
            self.req_rows.append((icon, msg, checker))

        self.stack.add_named(box, "step-1")

    def _build_step_2_directories(self):
        box = self._mk_page_box()

        t1 = Gtk.Label(label="Workshop Path (Required)")
        t1.set_halign(Gtk.Align.START)
        t1.add_css_class("heading")
        box.append(t1)

        path_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.path_entry = Gtk.Entry()
        self.path_entry.set_hexpand(True)
        self.path_entry.set_placeholder_text(
            "/home/user/.steam/steam/steamapps/workshop/content/431960"
        )
        current_path = self.config.get("workshopPath", "")
        if current_path:
            self.path_entry.set_text(str(current_path))
        path_box.append(self.path_entry)

        btn_browse = Gtk.Button(icon_name="folder-open-symbolic")
        btn_browse.connect("clicked", self.on_browse_clicked)
        path_box.append(btn_browse)
        box.append(path_box)

        t2 = Gtk.Label(label="Assets Path (Optional)")
        t2.set_halign(Gtk.Align.START)
        t2.add_css_class("heading")
        box.append(t2)

        self.assets_entry = Gtk.Entry()
        self.assets_entry.set_placeholder_text("Leave empty to auto-detect")
        assets_path = self.config.get("assetsPath", "")
        if assets_path:
            self.assets_entry.set_text(str(assets_path))
        box.append(self.assets_entry)

        self.stack.add_named(box, "step-2")

    def _build_step_3_quick_settings(self):
        box = self._mk_page_box()

        row_audio = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row_audio.append(Gtk.Label(label="Mute Audio"))
        row_audio_spacer = Gtk.Box()
        row_audio_spacer.set_hexpand(True)
        row_audio.append(row_audio_spacer)
        self.switch_mute = Gtk.Switch()
        self.switch_mute.set_active(bool(self.config.get("muteAudio", False)))
        row_audio.append(self.switch_mute)
        box.append(row_audio)

        row_autostart = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row_autostart.append(Gtk.Label(label="Launch on Startup"))
        row_autostart_spacer = Gtk.Box()
        row_autostart_spacer.set_hexpand(True)
        row_autostart.append(row_autostart_spacer)
        self.switch_auto = Gtk.Switch()
        self.switch_auto.set_active(bool(self.integrator.is_autostart_enabled()))
        row_autostart.append(self.switch_auto)
        box.append(row_autostart)

        row_restore = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row_restore.append(Gtk.Label(label="Auto Restore"))
        row_restore_spacer = Gtk.Box()
        row_restore_spacer.set_hexpand(True)
        row_restore.append(row_restore_spacer)
        self.switch_restore = Gtk.Switch()
        self.switch_restore.set_active(bool(self.config.get("autoRestore", True)))
        row_restore.append(self.switch_restore)
        box.append(row_restore)

        vol_label = Gtk.Label(label="Volume")
        vol_label.set_halign(Gtk.Align.START)
        box.append(vol_label)
        self.spin_volume = Gtk.SpinButton.new_with_range(0, 100, 1)
        self.spin_volume.set_value(float(self.config.get("volume", 50) or 50))
        box.append(self.spin_volume)

        fps_label = Gtk.Label(label="FPS Limit")
        fps_label.set_halign(Gtk.Align.START)
        box.append(fps_label)
        self.spin_fps = Gtk.SpinButton.new_with_range(15, 144, 1)
        self.spin_fps.set_value(float(self.config.get("fps", 30) or 30))
        box.append(self.spin_fps)

        self.stack.add_named(box, "step-3")

    def _build_step_4_all_set(self):
        box = self._mk_page_box()
        box.set_valign(Gtk.Align.CENTER)

        emoji = Gtk.Label(label="🎉")
        emoji.add_css_class("title-1")
        box.append(emoji)

        title = Gtk.Label(label="All Set!")
        title.add_css_class("title-2")
        box.append(title)

        desc = Gtk.Label(
            label="Your preferences have been saved. You can change them anytime in Settings."
        )
        desc.set_wrap(True)
        desc.set_justify(Gtk.Justification.CENTER)
        desc.add_css_class("dim-label")
        box.append(desc)

        self.stack.add_named(box, "step-4")

    def _resolve_logo_path(self):
        """
        智能查找 Logo 图片路径，兼容源码、AppImage 和系统安装包
        """
        candidates = []
        filename = "pic/icons/GUI_rounded.png"

        # 1. AppImage 环境优先 (检测 APPDIR 环境变量)
        appdir = os.getenv("APPDIR")
        if appdir:
            # 对应 build 脚本中的安装路径
            candidates.append(
                os.path.join(appdir, "usr/share/linux-wallpaperengine-gui", filename)
            )

        # 2. 系统/Arch 包安装路径
        candidates.append(
            os.path.join("/usr/share/linux-wallpaperengine-gui", filename)
        )

        # 3. 源码开发环境 (相对于当前文件的位置)
        # 当前文件在 py_GUI/ui/welcome_dialog.py
        # 项目根目录是往上推 3 级
        try:
            base_path = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            candidates.append(os.path.join(base_path, filename))
        except Exception:
            pass

        # 遍历检查，返回第一个存在的路径
        for path in candidates:
            if os.path.exists(path):
                return path
        return None

    def _check_backend(self):
        return shutil.which(
            "linux-wallpaperengine"
        ) is not None, "Found" if shutil.which(
            "linux-wallpaperengine"
        ) else "Not found — app may not work correctly"

    def _check_xvfb(self):
        ok = shutil.which("Xvfb") is not None
        return ok, "Available" if ok else "Not found — screenshots may not work"

    def _check_wayland(self):
        session = os.environ.get("XDG_SESSION_TYPE", "unknown").lower()
        ok = session == "wayland"
        return ok, "Detected" if ok else f"Running on {session}"

    def run_requirements_check(self):
        for icon, msg, checker in self.req_rows:
            try:
                ok, text = checker()
                icon.set_label("✅" if ok else "⚠️")
                msg.set_label(str(text))
            except Exception:
                icon.set_label("⚠️")
                msg.set_label("Check failed")

    def refresh_step_ui(self):
        while True:
            child = self.step_dots.get_first_child()
            if child is None:
                break
            self.step_dots.remove(child)
        for i in range(5):
            dot = Gtk.Label(label="●" if i == self.current_step else "○")
            if i != self.current_step:
                dot.add_css_class("dim-label")
            self.step_dots.append(dot)

        self.step_title.set_label(self.STEP_TITLES[self.current_step])
        self.stack.set_visible_child_name(f"step-{self.current_step}")
        self.btn_back.set_sensitive(self.current_step > 0)

        if self.current_step == 0:
            self.btn_next.set_label("Get Started")
        elif self.current_step < 4:
            self.btn_next.set_label("Continue")
        else:
            self.btn_next.set_label("Start Using App")

        if self.current_step == 1:
            GLib.idle_add(lambda: (self.run_requirements_check(), False)[1])

    def on_back_clicked(self, button):
        if self.current_step > 0:
            self.current_step -= 1
            self.refresh_step_ui()

    def on_next_clicked(self, button):
        if self.current_step < 4:
            self._persist_step_data()
            self.current_step += 1
            self.refresh_step_ui()
            return
        self._persist_step_data()
        self.config.set("onboardingCompleted", True)
        self.destroy()

    def _persist_step_data(self):
        if hasattr(self, "path_entry"):
            path = self.path_entry.get_text().strip()
            if path:
                self.config.set("workshopPath", path)
        if hasattr(self, "assets_entry"):
            self.config.set("assetsPath", self.assets_entry.get_text().strip())
        if hasattr(self, "switch_mute"):
            self.config.set("muteAudio", bool(self.switch_mute.get_active()))
        if hasattr(self, "switch_restore"):
            self.config.set("autoRestore", bool(self.switch_restore.get_active()))
        if hasattr(self, "spin_volume"):
            self.config.set("volume", int(self.spin_volume.get_value()))
        if hasattr(self, "spin_fps"):
            self.config.set("fps", int(self.spin_fps.get_value()))
        if hasattr(self, "switch_auto"):
            try:
                self.integrator.set_autostart(bool(self.switch_auto.get_active()))
            except Exception:
                pass

    def on_close_request(self, window):
        if self.is_required and not self.config.get("onboardingCompleted", False):
            return True
        return False

    def on_browse_clicked(self, button):
        dialog = Gtk.FileChooserNative(
            title="Select Workshop Folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )

        dialog.set_modal(True)

        def on_response(d, response):
            if response == Gtk.ResponseType.ACCEPT:
                file = d.get_file()
                path = file.get_path()
                if path:
                    self.path_entry.set_text(path)
            d.destroy()

        dialog.connect("response", on_response)
        dialog.show()
