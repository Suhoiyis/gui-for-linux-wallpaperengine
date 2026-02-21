import os
import sys
import stat
import shutil
import base64
import subprocess

from py_GUI.const import APP_ID

# 【神级优化】：在程序刚启动、虚拟文件系统(FUSE)绝对健康的时候，就把图标吃进内存！
# 坚决不在运行时去读文件。
try:
    from py_GUI.embedded_icon import ICON_DATA
    RAM_ICON_CACHE = ICON_DATA
    print("✅ Start loading: Successfully retrieved Base64 icon from memory.")
except Exception as e:
    print(f"⚠️ Startup prompt: Embedded icon module not found (source code development environment is normal): {e}")
    RAM_ICON_CACHE = None


class AppIntegrator:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(os.path.dirname(current_dir))
        
        self.script_path = os.path.join(self.project_root, "run_gui.py")
        self.icon_path = os.path.join(self.project_root, "pic/icons/GUI_rounded.png")
        self.python_exe = sys.executable
        
        self.app_dir = os.path.expanduser("~/.local/share/applications")
        self.autostart_dir = os.path.expanduser("~/.config/autostart")
        self.desktop_filename = f"{APP_ID}.desktop"

    def _generate_content(self, hidden=False):
        appimage_path = os.environ.get("APPIMAGE")
        
        if appimage_path:
            exec_cmd = f"\"{appimage_path}\""
            path_str = ""
        elif self.project_root.startswith("/usr/share/"):
            exec_cmd = "linux-wallpaperengine-gui"
            path_str = ""
        else:
            exec_cmd = f"{self.python_exe} \"{self.script_path}\""
            path_str = f"Path={self.project_root}\n"
        
        icon_str = APP_ID
        
        if hidden:
            exec_cmd += " --hidden"
            
        return f"""[Desktop Entry]
Type=Application
Name=Linux Wallpaper Engine
Comment=Wallpaper Engine for Linux (GUI)
Exec={exec_cmd}
Icon={icon_str}
{path_str}Terminal=false
Categories=Utility;Graphics;
StartupNotify=true
StartupWMClass={APP_ID}
X-GNOME-Autostart-enabled=true
"""

    def _install_icon(self):
        """完全从内存写入，与物理磁盘 100% 解耦"""
        dest_dir = os.path.expanduser("~/.local/share/icons/hicolor/512x512/apps")
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, f"{APP_ID}.png")
        
        icon_installed = False

        # ── 策略 A：内存直接吐出 (AppImage 专属，极速且无视 FUSE) ──
        if RAM_ICON_CACHE:
            try:
                with open(dest_path, "wb") as f:
                    f.write(base64.b64decode(RAM_ICON_CACHE))
                print(f"✅ SUCCESS: Icon materialized from RAM to {dest_path}")
                icon_installed = True
            except Exception as e:
                print(f"❌ ERROR writing RAM icon: {e}")

        # ── 策略 B：传统复制 (源码环境备用) ──
        if not icon_installed:
            candidates = [
                self.icon_path,
                os.path.join(self.project_root, "pic/icons/GUI_rounded.png"),
                os.path.join(self.project_root, "pic/icons/gui_tray_rounded.png")
            ]
            for src in candidates:
                if os.path.exists(src):
                    try:
                        shutil.copy(src, dest_path)
                        print(f"✅ SUCCESS: Icon copied from local file to {dest_path}")
                        icon_installed = True
                        break
                    except Exception as e:
                        print(f"❌ ERROR copying {src}: {e}")

        # ── 刷新缓存 ──
        if icon_installed:
            try:
                # 【终极修复】不使用 os.getcwd() 和 os.chdir()！
                # 直接通过 cwd 参数，让子进程在安全的用户主目录下运行，彻底隔离 FUSE
                subprocess.run(
                    ["/usr/bin/gtk-update-icon-cache", "-f", "-t", os.path.expanduser("~/.local/share/icons/hicolor")],
                    stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=False,
                    cwd=os.path.expanduser("~")  # <--- 让子进程降落在这里
                )
                print("✅ SUCCESS: Icon cache officially updated.")
            except Exception as e:
                print(f"⚠️ Refresh icon cache skip (non-fatal): {e}")
        else:
            print("⚠️ CRITICAL: All icon extraction strategies failed!")

    def create_menu_shortcut(self):
        self._install_icon()
        os.makedirs(self.app_dir, exist_ok=True)
        path = os.path.join(self.app_dir, self.desktop_filename)
        self._write_file(path, self._generate_content(hidden=False))
        return path

    def create_desktop_entry(self):
        try:
            path = self.create_menu_shortcut()
            return True, f"Desktop entry created at: {path}"
        except Exception as e:
            return False, f"Failed to create desktop entry: {str(e)}"

    def set_autostart(self, enabled: bool, hidden: bool = True):
        os.makedirs(self.autostart_dir, exist_ok=True)
        path = os.path.join(self.autostart_dir, self.desktop_filename)
        if enabled:
            self._install_icon()
            self._write_file(path, self._generate_content(hidden=hidden))
        else:
            if os.path.exists(path):
                os.remove(path)

    def is_autostart_enabled(self) -> bool:
        path = os.path.join(self.autostart_dir, self.desktop_filename)
        return os.path.exists(path)

    def check_and_update_shortcut(self):
        path = os.path.join(self.app_dir, self.desktop_filename)
        if not os.path.exists(path):
            return False
        try:
            with open(path, "r") as f:
                existing_content = f.read()
        except Exception:
            return False
        
        expected_content = self._generate_content(hidden=False)
        if existing_content == expected_content:
            return False
        
        try:
            self._install_icon()
            self._write_file(path, expected_content)
            return True
        except Exception:
            return False

    def _write_file(self, path, content):
        with open(path, "w") as f:
            f.write(content)
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)