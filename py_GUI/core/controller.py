import subprocess
import os
import shutil
from typing import Optional
from py_GUI.core.config import ConfigManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.logger import LogManager

class WallpaperController:
    def __init__(self, config: ConfigManager, prop_manager: PropertiesManager, log_manager: LogManager):
        self.config = config
        self.prop_manager = prop_manager
        self.log_manager = log_manager
        self.current_proc: Optional[subprocess.Popen] = None
        
        # Log Xvfb status on startup
        if shutil.which("xvfb-run"):
            self.log_manager.add_info("Xvfb detected: Silent screenshots enabled", "Controller")
        else:
            self.log_manager.add_info("Xvfb not found: Screenshots will spawn a window", "Controller")

    def apply(self, wp_id: str, screen: Optional[str] = None):
        """Apply wallpaper"""
        self.stop()
        
        if not screen:
            screen = self.config.get("lastScreen")
        if not screen or screen == "None":
            screen = "eDP-1"

        self.log_manager.add_info(f"Applying wallpaper {wp_id} to screen {screen}", "Controller")

        cmd = [
            "linux-wallpaperengine",
            str(wp_id),
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

        # User properties
        is_silent = self.config.get("silence", True)
        audio_props = {'musicvolume', 'music', 'bellvolume', 'sound', 'soundsettings', 'volume'}

        user_props = self.prop_manager._user_properties.get(wp_id, {})
        self.log_manager.add_debug(f"User properties for {wp_id}: {user_props}", "Controller")
        
        for prop_name, prop_value in user_props.items():
            if is_silent and prop_name.lower() in audio_props:
                continue

            prop_type = self.prop_manager.get_property_type(wp_id, prop_name)
            formatted_value = self.prop_manager.format_property_value(prop_type, prop_value)
            cmd.extend(["--set-property", f"{prop_name}={formatted_value}"])
            self.log_manager.add_debug(f"Adding property: {prop_name}={formatted_value} (type: {prop_type})", "Controller")

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
                # Process exited immediately
                # Read log file to get error
                self.engine_log.close() # Flush and close handle
                with open(log_path, "r") as f:
                    output = f.read()
                
                error_msg = f"Process exited immediately!\nOutput:\n{output}"
                self.log_manager.add_error(error_msg, "Engine")
                return

            self.config.set("lastWallpaper", wp_id)
            self.config.set("lastScreen", screen)
            self.log_manager.add_info(f"Wallpaper applied: {wp_id}", "Controller")

            # Niri color sync script support
            colors_script = os.path.expanduser("~/niri/scripts/sync_colors.sh")
            if os.path.exists(colors_script):
                try:
                    subprocess.run(["bash", colors_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                except Exception:
                    pass

        except Exception as e:
            self.log_manager.add_error(f"Failed to apply wallpaper: {e}", "Controller")

    def take_screenshot(self, wp_id: str, output_path: str):
        """Take a high-resolution screenshot of a specific wallpaper"""
        delay = self.config.get("screenshotDelay", 20)
        res = self.config.get("screenshotRes", "3840x2160")
        
        # Check for xvfb-run dynamically
        xvfb_path = shutil.which("xvfb-run")
        has_xvfb = xvfb_path is not None
        
        # Base command for the engine
        engine_cmd = [
            "linux-wallpaperengine",
            "--screenshot", output_path,
            "--screenshot-delay", str(delay),
            "--silent",
            "-f", "60",
            str(wp_id)
        ]

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
        return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=err_log, start_new_session=True, env=env)

    def stop(self):
        """Stop wallpaper"""
        self.log_manager.add_info("Stopping wallpaper", "Controller")
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
