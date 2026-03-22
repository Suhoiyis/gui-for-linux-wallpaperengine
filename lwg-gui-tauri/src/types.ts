// src/types.ts
export interface Wallpaper {
  id: string;
  title: string;
  preview: string;
  type: "Video" | "Scene" | "Web";
  path: string;
  description?: string;  // 新增
  tags?: string[];
  size?: string;
}

export interface AppConfig {
  // --- 1. Playback & Performance ---
  fps: number;
  scaling: string;
  clamping: string;

  noFullscreenPause: boolean;
  disableMouse: boolean;
  disableParallax: boolean;
  disableParticles: boolean;

  // --- 2. Audio & Display ---
  volume: number;
  muteAudio: boolean; // silence -> muteAudio
  noAutomute: boolean; // no_auto_mute -> noAutomute
  noAudioProcessing: boolean;

  // --- 3. Automation (Cycling) ---
  cycleEnabled: boolean;
  cycleInterval: number;
  cycleOrder: string;

  // --- 4. Wayland Tweaks ---
  waylandOnlyActive: boolean;
  waylandIgnoreAppids: string;

  // --- 5. System & Storage ---
  assetsPath: string | null;
  workshopPath: string | null;

  startHidden: boolean;
  // --- 6. Screenshot Tools ---
  screenshotDelay: number;
  screenshotRes: string;
  preferXvfb: boolean;

  // --- 7. Wallpaper Properties ---
  wallpaperProperties: Record<string, any>;
  wallpaperNicknames: Record<string, string>;
  compactMode: boolean;
  autoRestore: boolean;
}

// Represents an active wallpaper on a screen
export interface ActiveWallpaper {
  wallpaperId: string;
  isPlaying: boolean;
}

// Runtime state - direct mapping of screen -> active wallpaper
export type AppState = Record<string, ActiveWallpaper>;

// System integration settings (not stored in AppConfig)
export interface SystemIntegration {
  autostart: boolean;
  startHidden: boolean;
}

export interface LogEntry {
  id: number; // 唯一标识，用于 React key
  timestamp: string; // "10:00:01"
  level: "info" | "warn" | "error" | "debug";
  source: "GUI" | "Core" | "Engine" | "Controller";
  message: string;
}

export interface HistoryEntry {
  id: string;
  title: string;
  preview: string;
  timestamp: string;
}

// Playlist for user-defined wallpaper collections
export interface Playlist {
  id: string;              // UUID (generated on frontend)
  name: string;            // User-defined name
  wallpaperIds: string[];  // Ordered list of wallpaper IDs
  createdAt: number;       // Unix timestamp
  updatedAt: number;       // Unix timestamp
}
