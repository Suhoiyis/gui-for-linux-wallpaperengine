import subprocess
import os
import shutil
from typing import Optional, Callable, List, Tuple, Dict
from py_GUI.core.config import ConfigManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.logger import LogManager

from py_GUI.core.screen import ScreenManager
from py_GUI.core.performance import PerformanceMonitor

class WallpaperController:
    def __init__(self, config: ConfigManager, prop_manager: PropertiesManager, 
                 log_manager: LogManager, screen_manager: ScreenManager):
        self.config = config
        self.prop_manager = prop_manager
        self.log_manager = log_manager
        self.screen_manager = screen_manager
        self.current_proc: Optional[subprocess.Popen] = None
        self.show_toast: Callable[[str], None] = lambda msg: None
        self._last_command: List[str] = []
        self.history_manager = None
        
        self.perf_monitor = PerformanceMonitor(config=config)
        
        if shutil.which("xvfb-run"):
            self.log_manager.add_info("Xvfb detected: Silent screenshots enabled", "Controller")
        else:
            self.log_manager.add_info("Xvfb not found: Screenshots will spawn a window", "Controller")

    def set_toast_callback(self, callback: Callable[[str], None]):
        self.show_toast = callback

    def apply(self, wp_id: str, screen: Optional[str] = None, screens: Optional[List[str]] = None):
        """Apply wallpaper (Multi-monitor support)"""
        
        target_screens = []
        if screens:
            target_screens = screens
        elif screen:
            target_screens = [screen]
        else:
            last = self.config.get("lastScreen")
            if not last or last == "None":
                last = "eDP-1"
            target_screens = [last]

        active_monitors = self.config.get("active_monitors", {})
        
        for s in target_screens:
            active_monitors[s] = wp_id
            
        self.config.set("active_monitors", active_monitors)
        self.config.set("lastWallpaper", wp_id)
        
        if len(target_screens) == 1:
            self.config.set("lastScreen", target_screens[0])

        self.log_manager.add_info(f"Applying wallpaper {wp_id} to {target_screens}", "Controller")
        
        # Record wallpaper in history if HistoryManager is available
        if self.history_manager:
            try:
                wp_details = self.wp_manager.get_wallpaper(wp_id)
                if wp_details:
                    title = wp_details.get('title', 'Unknown')
                    preview = wp_details.get('preview', '')
                    self.history_manager.add(wp_id, title, preview)
            except Exception as e:
                self.log_manager.add_error(f"Failed to record wallpaper in history: {e}", "Controller")
        
        self.restart_wallpapers()

    def stop_screen(self, screen: str):
        """Stop wallpaper on a specific screen"""
        active_monitors = self.config.get("active_monitors", {})
        if screen in active_monitors:
            del active_monitors[screen]
            self.config.set("active_monitors", active_monitors)
            self.log_manager.add_info(f"Stopped wallpaper on {screen}", "Controller")
            
            if not active_monitors:
                self.stop()
            else:
                self.restart_wallpapers()

    def restart_wallpapers(self):
        """Restart the engine with current active_monitors configuration"""
        self.stop()
        
        # Validate screens
        active_monitors = self.config.get("active_monitors", {})
        connected_screens = self.screen_manager.get_screens()
        
        # Filter out disconnected screens
        valid_monitors = {scr: wid for scr, wid in active_monitors.items() if scr in connected_screens}
        
        # If monitors were removed, update config
        if len(valid_monitors) != len(active_monitors):
            self.log_manager.add_info(f"Removing disconnected screens from config. Valid: {list(valid_monitors.keys())}", "Controller")
            self.config.set("active_monitors", valid_monitors)
            active_monitors = valid_monitors

        if not active_monitors:
            self.log_manager.add_info("No active wallpapers for connected screens.", "Controller")
            return

        cmd = ["linux-wallpaperengine"]
        
        # Add screens
        for scr, wid in active_monitors.items():
            cmd.extend(["--screen-root", scr, "--bg", str(wid)])

        # Global args
        cmd.extend(["-f", str(self.config.get("fps", 30))])

        # Strict boolean check with default True for None
        silence_cfg = self.config.get("silence")
        is_silent_mode = True if silence_cfg is None else bool(silence_cfg)
        
        self.log_manager.add_debug(f"Building command. Silence mode: {is_silent_mode} (Raw: {silence_cfg})", "Controller")

        if is_silent_mode:
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

        if self.config.get("noautomute", False):
            cmd.append("--noautomute")

        if self.config.get("noAudioProcessing", False):
            cmd.append("--no-audio-processing")

        if self.config.get("disableParallax", False):
            cmd.append("--disable-parallax")

        if self.config.get("disableParticles", False):
            cmd.append("--disable-particles")

        clamp = self.config.get("clamping", "clamp")
        if clamp != "clamp":
            cmd.extend(["--clamp", clamp])

        if self.config.get("wayland_only_active", False):
            cmd.append("--fullscreen-pause-only-active")
            
        ignore_ids = (self.config.get("wayland_ignore_appids") or "").strip()
        if ignore_ids:
            for appid in ignore_ids.split(','):
                if appid.strip():
                    cmd.extend(["--fullscreen-pause-ignore-appid", appid.strip()])

        assets_path = self.config.get("assetsPath")
        if assets_path:
            cmd.extend(["--assets-dir", assets_path])

        # Properties (Apply for all active wallpapers)
        audio_props = {'musicvolume', 'music', 'bellvolume', 'sound', 'soundsettings', 'volume'}
        
        for wid in set(active_monitors.values()):
            user_props = self.prop_manager._user_properties.get(wid, {})
            for prop_name, prop_value in user_props.items():
                if is_silent_mode and prop_name.lower() in audio_props:
                    continue
                prop_type = self.prop_manager.get_property_type(wid, prop_name)
                formatted_value = self.prop_manager.format_property_value(prop_type, prop_value)
                cmd.extend(["--set-property", f"{prop_name}={formatted_value}"])

        self._last_command = cmd
        self.log_manager.add_debug(f"Executing: {' '.join(cmd)}", "Controller")

        try:
            # Fix potential deadlock by redirecting stdout/stderr to a log file instead of PIPE
            from py_GUI.const import CONFIG_DIR
            log_path = os.path.join(CONFIG_DIR, "engine_last.log")
            self.engine_log = open(log_path, "w")

            self.current_proc = subprocess.Popen(
                cmd,
                stdout=self.engine_log,
                stderr=self.engine_log
            )

            import time
            time.sleep(0.5)
            if self.current_proc.poll() is not None:
                self.engine_log.close()
                with open(log_path, "r") as f:
                    output = f.read()
                
                error_msg = f"Process exited immediately!\nOutput:\n{output}"
                self.log_manager.add_error(error_msg, "Engine")
                self.show_toast("❌ Wallpaper engine failed to start - check logs")
                return

            self.log_manager.add_info("Engine started successfully", "Controller")

            # Start Performance Monitoring
            if self.current_proc and self.current_proc.pid:
                self.perf_monitor.stop_all_backends()
                self.perf_monitor.start_monitoring("backend", self.current_proc.pid)

            colors_script = os.path.expanduser("~/niri/scripts/sync_colors.sh")
            if os.path.exists(colors_script):
                try:
                    subprocess.run(["bash", colors_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                except Exception:
                    pass

        except Exception as e:
            self.log_manager.add_error(f"Failed to start engine: {e}", "Controller")
            self.show_toast(f"❌ Failed to start engine: {e}")

    def take_screenshot(self, wp_id: str, output_path: str, delay: Optional[int] = None):
        """Take a high-resolution screenshot of a specific wallpaper"""
        if delay is None:
            delay = self.config.get("screenshotDelay", 20)
        res = self.config.get("screenshotRes", "3840x2160")
        
        # Check for xvfb-run dynamically and preference
        xvfb_path = shutil.which("xvfb-run")
        prefer_xvfb = self.config.get("preferXvfb", True)
        has_xvfb = (xvfb_path is not None) and prefer_xvfb
        
        # Base command for the engine
        engine_cmd = [
            "linux-wallpaperengine",
            "--screenshot", output_path,
            "--screenshot-delay", str(delay),
            "--silent",
            "-f", "60",
            str(wp_id)
        ]

        assets_path = self.config.get("assetsPath")
        if assets_path:
            engine_cmd.extend(["--assets-dir", assets_path])

        if has_xvfb:
            # Wrap in xvfb-run
            # Important: The server args must be a single string for -s
            xvfb_args = ["-a", "-s", f"-screen 0 {res}x24 +extension GLX"]
            
            # Combine commands
            # Even in Xvfb, we MUST force the engine to create a window of the target resolution
            # Otherwise it might default to 640x480 or 800x600
            cmd = [xvfb_path] + xvfb_args + engine_cmd + ["--window", f"0x0x{res}"]
            mode_msg = f"Silent (Xvfb) at {res}"
        else:
            # Fallback: Force window size
            cmd = engine_cmd + ["--window", f"0x0x{res}"]
            mode_msg = f"Windowed at {res} (Xvfb not found)"
        
        self.log_manager.add_info(f"Starting screenshot: {mode_msg}", "Controller")
        self.log_manager.add_info(f"Raw command: {cmd}", "Controller")
        
        # Prepare environment: Force X11/Xvfb usage by stripping Wayland vars
        env = os.environ.copy()
        if has_xvfb:
            # Aggressively strip Wayland indicators
            env.pop("WAYLAND_DISPLAY", None)
            env["XDG_SESSION_TYPE"] = "x11"
            env["SDL_VIDEODRIVER"] = "x11"
            env["GDK_BACKEND"] = "x11"
            # Ensure software rendering fallback if hardware GL fails in Xvfb
            env["LIBGL_ALWAYS_SOFTWARE"] = "1" 
        
        # Run asynchronously with a new session so we can kill the whole group
        # Redirect stderr to a temp file for debugging crashes
        err_log = open("/tmp/wallpaper_screenshot_error.log", "w")
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=err_log, start_new_session=True, env=env)
        
        tracker = self.perf_monitor.start_task("screenshot", proc.pid)
        return proc, tracker

    def stop(self):
        """Stop wallpaper"""
        self.log_manager.add_info("Stopping wallpaper", "Controller")
        
        self.perf_monitor.stop_all_backends()
        
        if self.current_proc:
            self.current_proc.terminate()
            self.current_proc = None
            
            # Close log file handle if open
            if hasattr(self, 'engine_log') and self.engine_log and not self.engine_log.closed:
                try:
                    self.engine_log.close()
                except:
                    pass
        subprocess.run(
            ["pkill", "-f", "linux-wallpaperengine"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

    def get_current_command(self) -> str:
        if not self._last_command:
            return ""
        return " ".join(self._last_command)
