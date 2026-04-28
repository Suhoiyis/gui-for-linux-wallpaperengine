from __future__ import annotations

from typing import TypedDict


class ConfigData(TypedDict, total=False):
    fps: int
    volume: int
    scaling: str
    silence: bool
    noFullscreenPause: bool
    disableMouse: bool
    noautomute: bool
    noAudioProcessing: bool
    disableParallax: bool
    disableParticles: bool
    clamping: str
    wallpaperProperties: dict[str, dict[str, object]]
    screenshotDelay: int
    screenshotRes: str
    preferXvfb: bool
    cycleEnabled: bool
    cycleInterval: int
    cycleOrder: str
    assetsPath: str | None
    workshopPath: str | None
    wayland_only_active: bool
    wayland_ignore_appids: str
    compact_mode: bool
    apply_mode: str
    sortMode: str
    sortReverse: bool
    wallpaperNicknames: dict[str, str]
    startHidden: bool
    autoRestore: bool
    playlists: list[dict[str, object]]
    cyclePlaylistId: str | None
    playlistSidebarOpen: bool
    onboarding_completed: bool
    themeMode: str


class StateData(TypedDict, total=False):
    active_monitors: dict[str, str | None]
    lastWallpaper: str | None
    lastScreen: str | None


class ScreenshotRecord(TypedDict, total=False):
    timestamp: float
    wp_id: str
    output_path: str
    duration: float
    max_cpu: float
    max_mem: float
    avg_cpu: float
    avg_mem: float


DEFAULT_CONFIG: ConfigData = {
    "fps": 30,
    "volume": 0,
    "scaling": "default",
    "silence": True,
    "noFullscreenPause": False,
    "disableMouse": False,
    "noautomute": False,
    "noAudioProcessing": False,
    "disableParallax": False,
    "disableParticles": False,
    "clamping": "clamp",
    "wallpaperProperties": {},
    "screenshotDelay": 20,
    "screenshotRes": "3840x2160",
    "preferXvfb": True,
    "cycleEnabled": False,
    "cycleInterval": 15,
    "cycleOrder": "random",
    "assetsPath": None,
    "workshopPath": None,
    "wayland_only_active": False,
    "wayland_ignore_appids": "",
    "compact_mode": False,
    "apply_mode": "diff",
    "sortMode": "title",
    "sortReverse": False,
    "wallpaperNicknames": {},
    "startHidden": False,
    "autoRestore": True,
    "playlists": [],
    "cyclePlaylistId": None,
    "playlistSidebarOpen": True,
    "onboarding_completed": False,
    "themeMode": "dark",
}

for _runtime_key in (
    "lastWallpaper",
    "lastScreen",
    "active_monitors",
    "activeMonitors",
    "screenshot_history",
):
    DEFAULT_CONFIG.pop(_runtime_key, None)


DEFAULT_STATE: StateData = {
    "active_monitors": {},
    "lastWallpaper": None,
    "lastScreen": None,
}


RUNTIME_KEYS = {"active_monitors", "lastWallpaper", "lastScreen", "activeMonitors"}
SCREENSHOT_HISTORY_KEY = "screenshot_history"


CONFIG_INTERNAL_TO_EXTERNAL = {
    "silence": "muteAudio",
    "noautomute": "noAutomute",
    "wayland_only_active": "waylandOnlyActive",
    "wayland_ignore_appids": "waylandIgnoreAppids",
    "compact_mode": "compactMode",
    "apply_mode": "applyMode",
    "onboarding_completed": "onboardingCompleted",
}


CONFIG_ALIASES_TO_INTERNAL = {
    "muteAudio": "silence",
    "silence": "silence",
    "noAutomute": "noautomute",
    "no_auto_mute": "noautomute",
    "noautomute": "noautomute",
    "waylandOnlyActive": "wayland_only_active",
    "wayland_only_active": "wayland_only_active",
    "waylandIgnoreAppids": "wayland_ignore_appids",
    "wayland_ignore_appids": "wayland_ignore_appids",
    "compactMode": "compact_mode",
    "compact_mode": "compact_mode",
    "applyMode": "apply_mode",
    "apply_mode": "apply_mode",
    "onboardingCompleted": "onboarding_completed",
    "onboarding_completed": "onboarding_completed",
}


STATE_INTERNAL_TO_EXTERNAL = {
    "active_monitors": "activeMonitors",
}


STATE_ALIASES_TO_INTERNAL = {
    "activeMonitors": "active_monitors",
    "active_monitors": "active_monitors",
    "lastWallpaper": "lastWallpaper",
    "last_wallpaper": "lastWallpaper",
    "lastScreen": "lastScreen",
    "last_screen": "lastScreen",
}
