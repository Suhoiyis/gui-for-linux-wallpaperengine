import { create } from "zustand";
import { invoke } from "@tauri-apps/api/core";
import { toast } from "sonner";

import { Wallpaper, AppConfig, AppState, Playlist } from "../types";
import { scanWallpapers } from "../api/wallpaper";
import { parseSize, normalizeType, isTauriEnv } from "../lib/utils";
import { startCycleTimer, stopCycleTimer, setCycleScreen } from "../api/cycle";
import { FAVORITES_PLAYLIST_ID } from "../lib/constants";

// Runtime settings: require explicit Save button (backend restart needed)
const RUNTIME_SETTINGS = new Set<keyof AppConfig>([
  "fps",
  "volume",
  "muteAudio",
  "scaling",
  "clamping",
  "disableParallax",
  "disableParticles",
  "noFullscreenPause",
  "disableMouse",
  "noAutomute",
  "noAudioProcessing",
  "assetsPath",
  "waylandOnlyActive",
  "waylandIgnoreAppids",
]);

// Non-runtime settings: immediate save with debounce
const NON_RUNTIME_SETTINGS = new Set<keyof AppConfig>([
  "workshopPath",
  "screenshotRes",
  "preferXvfb",
  "screenshotDelay",
  "cycleEnabled",
  "cycleInterval",
  "cycleOrder",
]);


const saveTimeouts: Record<string, ReturnType<typeof setTimeout>> = {};

// Highlight timeout for settings field focus
let highlightTimeout: ReturnType<typeof setTimeout> | undefined;

// Maximum selection count for playlist creation (performance protection)
const MAX_SELECTION_COUNT = 100;

const isSliderOrInput = (key: keyof AppConfig): boolean => {
  const sliderInputKeys: Array<keyof AppConfig> = [
    "volume",
    "fps",
    "screenshotDelay",
    "cycleInterval",
    "waylandIgnoreAppids",
  ];
  return sliderInputKeys.includes(key);
};

interface AppStoreState {
  // App version
  appVersion: string;

  // Wallpaper data
  wallpapers: Wallpaper[];
  selectedId: string | null;
  searchQuery: string;
  activeTab: "wallpapers" | "settings" | "performance";

  // ✨ 新增：排序状态
  sortBy: "name" | "id" | "size";

  // Favorites & nicknames
  favoriteIds: Set<string>;
  nicknames: Record<string, string>;

  // Settings data
  settings: AppConfig | null;
  settingsLoading: boolean;

  // Monitor detection
  monitors: string[];
  monitorsLoading: boolean;

  // Screen selection
  selectedScreen: string;

  // ✨✨ 新增：截图引导状态 ✨✨
  screenshotHintActive: boolean;

  // ✨✨ 新增：设置字段高亮状态（用于跨组件通信）✨✨
  highlightSettingField: string | null;
  // Runtime state (loaded from separate state endpoint)
  runtimeState: import('../types').AppState;

  // ===== Playlist 相关状态 =====
  
  // Playlist data
  playlists: Playlist[];
  
  // Currently browsing playlist ID (null = ALL)
  activePlaylistId: string | null;
  
  // Playlist used for cycling (null = ALL)
  cyclePlaylistId: string | null;
  
  // Sidebar visibility
  isPlaylistSidebarOpen: boolean;
  isPlaylistSidebarPinned: boolean; // true = locked (pushes content), false = floating (overlays content)
  
  // Hydration state (FOUC prevention)
  isHydrated: boolean;
  
  // Selection mode for batch operations
  isSelectionMode: boolean;
  selectedForPlaylist: Set<string>;

  // ✨✨ Command Palette 状态 ✨✨
  isCommandPaletteOpen: boolean;




  // Actions
  fetchAppVersion: () => Promise<void>;
  loadWallpapers: () => Promise<void>;
  setSelectedId: (id: string | null) => void;
  setSearchQuery: (query: string) => void;
  setActiveTab: (tab: "wallpapers" | "settings" | "performance") => void;

  // ✨ 新增：设置排序方式的方法
  setSortBy: (sort: "name" | "id" | "size") => void;

  // ✨✨ 新增：设置截图引导状态的方法 ✨✨
  setScreenshotHintActive: (active: boolean) => void;

  // ✨✨ 新增：设置字段高亮方法 ✨✨
  setHighlightSettingField: (field: string | null) => void;

  // ✨✨ Command Palette 方法 ✨✨
  setCommandPaletteOpen: (open: boolean) => void;

  toggleFavorite: (id: string) => void;
  addToFavorites: (id: string) => void;
  removeFromFavorites: (id: string) => void;
  isFavorite: (id: string) => boolean;
  setNickname: (id: string, nickname: string) => Promise<void>;
  getNickname: (id: string) => string | undefined;

  fetchSettings: () => Promise<void>;
  initializeSettings: () => Promise<void>;
  getState: () => Promise<AppState>;
  saveRuntimeState: (state: AppState) => Promise<void>;
  fetchMonitors: () => Promise<void>;
  updateSetting: <K extends keyof AppConfig>(
    key: K,
    value: AppConfig[K],
  ) => void;
  saveSettings: () => Promise<void>;
  restartWallpapers: () => Promise<void>;

  // ✨✨ 新增全局壁纸控制方法（供托盘和快捷键调用）✨✨
  applyWallpaper: (id: string, screen?: string) => Promise<void>;
  stopWallpaper: () => Promise<void>;
  applyRandomWallpaper: () => Promise<void>;


  // Delete wallpaper
  removeWallpaper: (id: string, path: string) => Promise<void>;

  setSelectedScreen: (screen: string) => void;
  flushPendingUpdates: () => void;

  // Computed properties
  getFilteredWallpapers: () => Wallpaper[];
  getSelectedWallpaper: () => Wallpaper | null;

  isCompactMode: boolean;
  toggleCompactMode: (enabled: boolean) => void;

  // 初始化
  initApp: () => Promise<void>;
  initializeSelectedWallpaper: () => void;
  
  // ===== Playlist 相关方法 =====
  
  // Playlist CRUD
  loadPlaylists: () => Promise<void>;
  createPlaylist: (name: string, wallpaperIds: string[]) => Promise<void>;
  renamePlaylist: (id: string, name: string) => Promise<void>;
  deletePlaylist: (id: string) => Promise<void>;
  reorderPlaylists: (orderedIds: string[]) => Promise<void>;
  
  // Synthetic actions (frontend composition, calls update_playlist)
  addToPlaylist: (playlistId: string, wallpaperIds: string[]) => Promise<void>;
  removeFromPlaylist: (playlistId: string, wallpaperId: string) => Promise<void>;
  
  // State control
  setActivePlaylist: (id: string | null) => void;
  setCyclePlaylist: (id: string | null) => Promise<void>;
  togglePlaylistSidebar: () => void;
  togglePlaylistSidebarPin: () => void;
  openPlaylistSidebarFloating: () => void;
  
  // Selection mode
  enterSelectionMode: () => void;
  exitSelectionMode: () => void;
  toggleSelectForPlaylist: (wallpaperId: string) => void;
  selectAllForPlaylist: () => void;
  deselectAllForPlaylist: () => void;
  createPlaylistFromSelection: (name: string) => Promise<void>;
}

export const useAppStore = create<AppStoreState>((set, get) => ({
  // Initial state
  appVersion: "0.0.0",
  wallpapers: [],
  selectedId: null,
  searchQuery: "",
  activeTab: "wallpapers",
  sortBy: "name", // ✨ 默认按名称排序
  favoriteIds: new Set<string>(),
  nicknames: {},
  settings: null,
  settingsLoading: false,
  monitors: [],
  monitorsLoading: false,
  selectedScreen: "all",
  isCompactMode: false,

  // ✨✨ 截图引导提示默认关闭 ✨✨
  screenshotHintActive: false,

  // ✨✨ 设置字段高亮默认为 null ✨✨
  highlightSettingField: null,

  // Runtime state from separate API endpoint
  runtimeState: {},

  // ===== Playlist 初始状态 =====
  playlists: [],
  activePlaylistId: null,
  cyclePlaylistId: null,
  isPlaylistSidebarOpen: true,
  isPlaylistSidebarPinned: true, // 默认锁定模式
  isHydrated: false,
  isSelectionMode: false,
  selectedForPlaylist: new Set<string>(),

  // ✨✨ Command Palette 默认关闭 ✨✨
  isCommandPaletteOpen: false,


  // App version action
  fetchAppVersion: async () => {
    try {
      const isTauri = isTauriEnv();
      if (isTauri) {
        const version = await invoke<string>("get_app_version");
        set({ appVersion: version });
      }
    } catch (error) {
      console.error("Failed to fetch app version:", error);
    }
  },

  // Wallpaper actions
  loadWallpapers: async () => {
    const data = await scanWallpapers();

    // 🛠️ 解决 TS 报错：
    const mappedWallpapers = data.map((w: any) => ({
      ...w,
      type: normalizeType(w.type || w.wtype),
    })) as Wallpaper[];

    set({ wallpapers: mappedWallpapers });
    // 不再自动选中，等待 initApp -> initializeSelectedWallpaper() 处理
  },

  setSelectedId: (id) => set({ selectedId: id }),
  setSearchQuery: (q) => set({ searchQuery: q }),
  setActiveTab: (tab) => set({ activeTab: tab }),

  // ✨ 新增
  setSortBy: (sortBy) => set({ sortBy }),

  // ✨✨ 新增截图动作 ✨✨
  setScreenshotHintActive: (active) => set({ screenshotHintActive: active }),

  // ✨✨ 新增设置字段高亮动作 ✨✨
  setHighlightSettingField: (field) => {
    // Clear previous timeout BEFORE setting new one (prevents race conditions)
    if (highlightTimeout) {
      clearTimeout(highlightTimeout);
    }

    set({ highlightSettingField: field });

    // Auto-clear highlight after 3 seconds
    if (field) {
      highlightTimeout = setTimeout(() => {
        set({ highlightSettingField: null });
      }, 3000);
    }
  },

  // ✨✨ Command Palette 开关 ✨✨
  setCommandPaletteOpen: (open) => set({ isCommandPaletteOpen: open }),

  // Favorites & nicknames actions
  toggleFavorite: async (id: string) => {
    const isTauri = isTauriEnv();
    
    // Store previous state for rollback on error
    const previousFavorites = get().favoriteIds;
    
    // Optimistic update - MUST create new Set for React re-render
    const next = new Set(previousFavorites);
    if (next.has(id)) {
      next.delete(id);
    } else {
      next.add(id);
    }
    set({ favoriteIds: next });
    
    // Save to backend
    if (isTauri) {
      try {
        await invoke("toggle_favorite", { id });
      } catch (error) {
        console.error("Failed to toggle favorite:", error);
        toast.error("Failed to save favorite");
        // Revert on error
        set({ favoriteIds: previousFavorites });
      }
    }
  },
  
  // 幂等添加到收藏（已收藏则无操作）
  addToFavorites: async (id: string) => {
    const isTauri = isTauriEnv();
    const currentFavorites = get().favoriteIds;
    
    // 已收藏则无操作
    if (currentFavorites.has(id)) return;
    
    // 乐观更新
    const next = new Set(currentFavorites);
    next.add(id);
    set({ favoriteIds: next });
    
    // 保存到后端
    if (isTauri) {
      try {
        await invoke("toggle_favorite", { id });
      } catch (error) {
        console.error("Failed to add favorite:", error);
        toast.error("Failed to add to favorites");
        set({ favoriteIds: currentFavorites });
      }
    }
  },
  
  // 幂等从收藏移除（未收藏则无操作）
  removeFromFavorites: async (id: string) => {
    const isTauri = isTauriEnv();
    const currentFavorites = get().favoriteIds;
    
    // 未收藏则无操作
    if (!currentFavorites.has(id)) return;
    
    // 乐观更新
    const next = new Set(currentFavorites);
    next.delete(id);
    set({ favoriteIds: next });
    
    // 保存到后端
    if (isTauri) {
      try {
        await invoke("toggle_favorite", { id });
      } catch (error) {
        console.error("Failed to remove favorite:", error);
        toast.error("Failed to remove from favorites");
        set({ favoriteIds: currentFavorites });
      }
    }
  },
  
  isFavorite: (id: string) => get().favoriteIds.has(id),
  setNickname: async (id: string, nickname: string) => {
    const isTauri = isTauriEnv();
    const previousNicknames = get().nicknames;
    const trimmed = nickname.trim().slice(0, 100);
    const newNicknames = { ...previousNicknames };
    if (trimmed === "") {
      delete newNicknames[id];
    } else {
      newNicknames[id] = trimmed;
    }
    set({ nicknames: newNicknames });
    
    // Save to backend
    if (isTauri) {
      try {
        await invoke("set_nickname", { id, nickname: trimmed });
      } catch (error) {
        console.error("Failed to save nickname:", error);
        toast.error("Failed to save nickname");
        set({ nicknames: previousNicknames });
      }
    }
  },
  getNickname: (id: string) => get().nicknames[id],

  // Monitor detection
  fetchMonitors: async () => {
    set({ monitorsLoading: true });
    try {
      const isTauri = isTauriEnv();
      if (!isTauri) {
        // Browser mode - return empty array
        set({ monitors: [], monitorsLoading: false });
        return;
      }

      // Use Rust backend command to get real monitor names via xrandr
      const monitors = await invoke<string[]>("get_connected_monitors");
      set({ monitors, monitorsLoading: false });
    } catch (error) {
      console.error("Failed to fetch monitors:", error);
      set({ monitors: [], monitorsLoading: false });
    }
  },

  // Settings actions
  fetchSettings: async () => {
    set({ settingsLoading: true });
    try {
      // ✨ 1. 检查是否在 Tauri 环境中
      const isTauri = isTauriEnv();

      let settings;
      if (isTauri) {
        // 如果是 Tauri 客户端，正常调用 Rust 后端
        settings = await invoke<AppConfig>("get_settings");
      } else {
        // ✨ 2. 如果是纯浏览器环境，返回 Mock 数据
        console.warn("[Browser Mode] Fetching Mock Settings...");
        // 模拟一点网络延迟，更真实
        await new Promise((resolve) => setTimeout(resolve, 500));
        settings = {
          fps: 60,
          volume: 50,
          scaling: "fill",
          muteAudio: false, // 对应 Rust 侧的 #[serde(rename = "muteAudio")] pub silence: bool
          noFullscreenPause: false, // 驼峰命名
          disableMouse: false,
          noAutomute: false, // 对应 Rust 侧的 #[serde(rename = "noAutomute")] pub no_auto_mute: bool
          noAudioProcessing: false,
          disableParallax: false,
          disableParticles: false,
          clamping: "clamp",
          wallpaperProperties: {},
          screenshotDelay: 2,
          screenshotRes: "1920x1080",
          preferXvfb: true,
          cycleEnabled: true,
          cycleInterval: 30,
          cycleOrder: "random",
          assetsPath: "/mock/assets/path",
          workshopPath: "/mock/workshop/path",
          waylandOnlyActive: false,
          waylandIgnoreAppids: "firefox,steam",
          compactMode: false,
          wallpaperNicknames: {},
        } as unknown as AppConfig;
      }

      set({ settings, settingsLoading: false });
    } catch (error) {
      console.error("Failed to fetch settings:", error);
      set({ settingsLoading: false });
      throw error;
    }
  },

  initializeSettings: async () => {
    set({ settingsLoading: true });
    try {
      const isTauri = isTauriEnv();
      if (isTauri) {
        const settings = await invoke<AppConfig>("get_settings");
        set({ settings, settingsLoading: false });
        console.log("[App] Settings initialized from backend");
        // Also load runtime state
        const state = await invoke<AppState>("get_state");
        set({ runtimeState: state });
        
        // Load nicknames from backend
        try {
          const nicknames = await invoke<Record<string, string>>("get_nicknames");
          set({ nicknames });
          console.log("[App] Nicknames loaded:", Object.keys(nicknames).length);
        } catch (error) {
          console.error("[App] Failed to load nicknames:", error);
        }
        
        // Load favorites from backend
        try {
          const favoriteIds = await invoke<string[]>("get_favorites");
          set({ favoriteIds: new Set(favoriteIds) });
          console.log("[App] Favorites loaded:", favoriteIds.length);
        } catch (error) {
          console.error("[App] Failed to load favorites:", error);
        }

      } else {
        // Mock mode - use default settings
        const defaultSettings: AppConfig = {
          fps: 30,
          volume: 50,
          scaling: "default",
          clamping: "clamp",
          muteAudio: false,
          noFullscreenPause: false,
          disableMouse: false,
          noAutomute: false,
          noAudioProcessing: false,
          disableParallax: false,
          disableParticles: false,
          wallpaperProperties: {},
          screenshotDelay: 20,
          screenshotRes: "3840x2160",
          preferXvfb: true,
          cycleEnabled: false,
          cycleInterval: 15,
          cycleOrder: "random",
          assetsPath: null,
          workshopPath: null,
          waylandOnlyActive: false,
          waylandIgnoreAppids: "",
          wallpaperNicknames: {},
          compactMode: false,
          startHidden: false,
          autoRestore: false,
        };
        set({ settings: defaultSettings, settingsLoading: false });
        // Mock runtime state
        set({ runtimeState: {} });
        console.log("[App] Settings initialized with defaults (mock mode)");

      }
    } catch (error) {
      console.error("[App] Failed to initialize settings:", error);
      set({ settingsLoading: false });
      // Don't throw - app should still work with defaults
    }
  },

  updateSetting: <K extends keyof AppConfig>(key: K, value: AppConfig[K]) => {
    const currentSettings = get().settings;
    if (!currentSettings) return;

    const newSettings = { ...currentSettings, [key]: value };
    set({ settings: newSettings });

    const isTauri = isTauriEnv();
    if (!isTauri) {
      console.log(`[Mock Mode] Updated ${String(key)}:`, value);
      return;
    }

    if (RUNTIME_SETTINGS.has(key)) {
      console.log(
        `[Runtime] ${String(key)} updated locally, waiting for Save button`,
      );
      return;
    }

    if (!NON_RUNTIME_SETTINGS.has(key)) {
      return;
    }

    if (saveTimeouts[key as string]) {
      clearTimeout(saveTimeouts[key as string]);
    }

    const debounceMs = isSliderOrInput(key) ? 500 : 0;

    saveTimeouts[key as string] = setTimeout(async () => {
      try {
        console.log(`[Non-Runtime] Saving ${String(key)} to backend...`);
        const result = await invoke<AppConfig>("update_config_value", {
          key: key as string,
          value: value,
        });
        set({ settings: result });
        console.log(`[Non-Runtime] ${String(key)} saved successfully`);
        
        // Handle cycleEnabled changes
        if (key === "cycleEnabled") {
          if (value) {
            await startCycleTimer();
            toast.success("Wallpaper cycling enabled");
          } else {
            await stopCycleTimer();
            toast.success("Wallpaper cycling disabled");
          }
        }
        
        toast.success("Setting saved", {
          description: `${String(key)} has been updated`,
          duration: 2000,
        });
      } catch (error) {
        console.error(`[Non-Runtime] Failed to save ${String(key)}:`, error);
        set({ settings: currentSettings });
        toast.error(`Failed to save ${String(key)}`, {
          description: String(error),
        });
      }
    }, debounceMs);
  },

  saveSettings: async () => {
    const settings = get().settings;
    if (!settings) {
      throw new Error("No settings to save");
    }
    try {
      const isTauri = isTauriEnv();
      if (isTauri) {
        await invoke("save_settings", { config: settings });
      } else {
        console.warn("[Browser Mode] Mock saving settings:", settings);
        await new Promise((resolve) => setTimeout(resolve, 500));
        // 在浏览器里，数据实际上已经在 store 里更新了，所以不需要做什么，直接成功即可
      }
    } catch (error) {
      console.error("Failed to save settings:", error);
      throw error;
    }
  },

  getState: async () => {
    try {
      const isTauri = isTauriEnv();
      if (!isTauri) {
        return {};
      }
      const state = await invoke<AppState>("get_state");
      set({ runtimeState: state });

      return state;
    } catch (error) {
      console.error("Failed to fetch state:", error);
      throw error;
    }
  },


  saveRuntimeState: async (state: AppState) => {
    try {
      const isTauri = isTauriEnv();
      if (!isTauri) {
        set({ runtimeState: state });
        return;
      }
      await invoke("save_state", { appState: state });
      set({ runtimeState: state });
    } catch (error) {
      console.error("Failed to save runtime state:", error);
      throw error;
    }
  },



  flushPendingUpdates: () => {
    // Clear all pending timeouts
    Object.values(saveTimeouts).forEach(clearTimeout);
    // Clear the timeouts object
    Object.keys(saveTimeouts).forEach((k) => delete saveTimeouts[k]);
  },

  restartWallpapers: async () => {
    try {
      await invoke("restart_wallpapers");
    } catch (error) {
      console.error("Failed to restart wallpapers:", error);
      throw error;
    }
  },

  applyWallpaper: async (id: string, screen?: string) => {
    const previousRuntimeState = get().runtimeState;
    
    try {
      // Trigger backend to apply wallpaper
      const targetScreen = screen || (get().selectedScreen === "all" ? undefined : get().selectedScreen);
      await invoke("apply_wallpaper", { id, screen: targetScreen });

      // Update runtime state (not config) - optimistic update
      const monitors = get().monitors;
      
      let newRuntimeState: typeof previousRuntimeState;
      
      if (targetScreen) {
        // Update specific screen
        newRuntimeState = {
          ...previousRuntimeState,
          [targetScreen]: { wallpaperId: id, isPlaying: true },
        };
      } else {
        // Update all monitors (when screen is undefined/"all")
        const updates: Record<string, { wallpaperId: string; isPlaying: boolean }> = {};
        monitors.forEach(monitor => {
          updates[monitor] = { wallpaperId: id, isPlaying: true };
        });
        newRuntimeState = {
          ...previousRuntimeState,
          ...updates,
        };
      }

      set({ runtimeState: newRuntimeState });
      
      // Persist runtime state to backend
      try {
        await get().saveRuntimeState(newRuntimeState);
      } catch (saveError) {
        console.error("Failed to save runtime state:", saveError);
        // 状态已更新但持久化失败，只记录警告不回滚（本地状态更可靠）
        toast.warning("State saved locally but sync failed");
      }

      const wallpaper = get().wallpapers.find((w) => w.id === id);
      if (wallpaper) {
        try {
          await invoke("add_history", {
            id: wallpaper.id,
            title: wallpaper.title,
            preview: wallpaper.preview,
          });
        } catch (historyError) {
          console.error("Failed to add history:", historyError);
          toast.warning("Wallpaper applied, but failed to save history");
        }
      }
    } catch (error) {
      // 回滚到之前的状态
      set({ runtimeState: previousRuntimeState });
      console.error("Failed to apply wallpaper:", error);
      toast.error("Failed to apply wallpaper", { description: String(error) });
    }
  },





  stopWallpaper: async () => {
    try {
      await invoke("stop_wallpaper");
      
      // 更新 runtimeState：设置所有 isPlaying = false
      const currentRuntimeState = get().runtimeState;
      const newRuntimeState = Object.fromEntries(
        Object.entries(currentRuntimeState).map(([screen, aw]) => [
          screen,
          { ...aw, isPlaying: false }
        ])
      );
      set({ runtimeState: newRuntimeState });
      await get().saveRuntimeState(newRuntimeState);
      
      toast.success("Wallpaper stopped");
    } catch (error) {
      console.error("Failed to stop wallpaper:", error);
      toast.error("Failed to stop wallpaper", { description: String(error) });
    }
  },


  applyRandomWallpaper: async () => {
    const { wallpapers, applyWallpaper } = get();
    if (wallpapers.length === 0) {
      toast.warning("No wallpapers available");
      return;
    }
    const randomIndex = Math.floor(Math.random() * wallpapers.length);
    const randomWp = wallpapers[randomIndex];
    await applyWallpaper(randomWp.id);
  },




  removeWallpaper: async (id: string, path: string) => {
    const isTauri = isTauriEnv();
    
    // Store previous state for rollback
    const previousWallpapers = get().wallpapers;
    const previousFavorites = get().favoriteIds;
    const previousNicknames = get().nicknames;
    const previousSelectedId = get().selectedId;
    const previousRuntimeState = get().runtimeState;
    
    // Optimistic update
    const newWallpapers = previousWallpapers.filter((w) => w.id !== id);
    const newFavorites = new Set(previousFavorites);
    newFavorites.delete(id);
    const newNicknames = { ...previousNicknames };
    delete newNicknames[id];
    const newSelectedId = previousSelectedId === id ? null : previousSelectedId;
    const newRuntimeState = Object.fromEntries(
      Object.entries(previousRuntimeState).filter(
        ([, aw]) => aw.wallpaperId !== id,
      ),
    ) as AppState;
    
    set({
      wallpapers: newWallpapers,
      favoriteIds: newFavorites,
      nicknames: newNicknames,
      selectedId: newSelectedId,
      runtimeState: newRuntimeState,
    });
    
    // Call backend
    if (isTauri) {
      try {
        const { deleteWallpaper } = await import("../api/wallpaper");
        await deleteWallpaper(id, path);
        toast.success("Wallpaper deleted", { description: "Removed from disk" });
      } catch (error) {
        console.error("Failed to delete wallpaper:", error);
        toast.error("Failed to delete wallpaper", { description: String(error) });
        // Rollback
        set({
          wallpapers: previousWallpapers,
          favoriteIds: previousFavorites,
          nicknames: previousNicknames,
          selectedId: previousSelectedId,
          runtimeState: previousRuntimeState,
        });
      }
    } else {
      toast.success("Wallpaper deleted (mock)");
    }
  },

  setSelectedScreen: (screen: string) => {
    set({ selectedScreen: screen });
    setCycleScreen(screen).catch(console.error);
  },

getFilteredWallpapers: () => {
    const { wallpapers, searchQuery, sortBy, nicknames, activePlaylistId, playlists, favoriteIds } = get();

    // ===== 情况 1：Favorites 视图 =====
    if (activePlaylistId === FAVORITES_PLAYLIST_ID) {
      // 从 favoriteIds 生成壁纸列表
      const favoriteWallpapers = Array.from(favoriteIds)
        .map(id => wallpapers.find(w => w.id === id))
        .filter((w): w is Wallpaper => w !== undefined);
      
      // 搜索过滤
      if (searchQuery) {
        const lowerQ = searchQuery.toLowerCase();
        return favoriteWallpapers.filter(w => 
          (w.title || "").toLowerCase().includes(lowerQ) ||
          w.id.includes(lowerQ) ||
          (nicknames[w.id] || '').toLowerCase().includes(lowerQ)
        );
      }
      
      return favoriteWallpapers;
    }

    // ===== 情况 2：查看特定 Playlist =====
    if (activePlaylistId) {
      const activePlaylist = playlists.find(p => p.id === activePlaylistId);
      if (!activePlaylist) return [];
      
      // 【步骤 1：域过滤】使用 map 保留用户自定义顺序
      const playlistWallpapers = activePlaylist.wallpaperIds
        .map(id => wallpapers.find(w => w.id === id))
        .filter((w): w is Wallpaper => w !== undefined);
      
      // 【步骤 2：搜索过滤】在域过滤结果上进行搜索
      if (searchQuery) {
        const lowerQ = searchQuery.toLowerCase();
        return playlistWallpapers.filter(w => 
          (w.title || "").toLowerCase().includes(lowerQ) ||
          w.id.includes(lowerQ) ||
          (nicknames[w.id] || '').toLowerCase().includes(lowerQ)
        );
      }
      
      // 【步骤 3：最终输出】
      return playlistWallpapers;
    }
    
    // ===== 情况 3：ALL 视图 =====
    let filtered = wallpapers;
    if (searchQuery) {
      const lowerQ = searchQuery.toLowerCase();
      filtered = wallpapers.filter(
        (w) => {
          const title = (w.title || "").toLowerCase();
          const nick = (nicknames[w.id] || "").toLowerCase();
          return title.includes(lowerQ) || w.id.includes(lowerQ) || nick.includes(lowerQ);
        },
      );
    }

    // 排序 (浅拷贝防止修改原数组)
    return [...filtered].sort((a, b) => {
      if (sortBy === "name") {
        return (a.title || "").localeCompare(b.title || "");
      } else if (sortBy === "id") {
        const aNum = parseInt(a.id, 10);
        const bNum = parseInt(b.id, 10);
        if (!isNaN(aNum) && !isNaN(bNum)) {
          return aNum - bNum;
        }
        return (a.id || "").localeCompare(b.id || "");
      } else if (sortBy === "size") {
        return parseSize(b.size) - parseSize(a.size);
      }
      return 0;
    });
  },

  getSelectedWallpaper: () => {
    const { wallpapers, selectedId } = get();
    return wallpapers.find((w) => w.id === selectedId) || null;
  },

  toggleCompactMode: (enabled) => {
    const previous = get().isCompactMode;
    set({ isCompactMode: enabled });

    const isTauri = isTauriEnv();
    if (isTauri) {
      const currentSettings = get().settings;
      if (currentSettings) {
        const nextSettings = { ...currentSettings, compactMode: enabled };
        set({ settings: nextSettings });

        invoke<AppConfig>("update_config_value", {
          key: "compactMode",
          value: enabled,
        })
          .then((result) => {
            set({ settings: result });
          })
          .catch((error) => {
            set({ isCompactMode: previous, settings: currentSettings });
            console.error("Failed to save compact mode:", error);
            toast.error("Failed to save compact mode", {
              description: String(error),
            });
          });
      }
    } else {
      localStorage.setItem("lwg_compact_mode", String(enabled));
    }
  },

  initializeSelectedWallpaper: () => {
    const { wallpapers, selectedId, selectedScreen, runtimeState } = get();

    // 如果已有选中，跳过
    if (selectedId) return;

    // 如果没有壁纸，跳过
    if (wallpapers.length === 0) return;

    // 1. 尝试从 runtimeState 恢复
    let initialId: string | null = null;

    if (Object.keys(runtimeState).length > 0) {
      // 优先找当前选中屏幕的壁纸
      if (selectedScreen !== "all" && runtimeState[selectedScreen]?.wallpaperId) {
        initialId = runtimeState[selectedScreen].wallpaperId;
      }
      // 否则找任一屏幕的壁纸
      if (!initialId) {
        for (const screen of Object.keys(runtimeState)) {
          if (runtimeState[screen]?.wallpaperId) {
            initialId = runtimeState[screen].wallpaperId;
            break;
          }
        }
      }
    }

    // 2. 验证找到的壁纸是否在当前列表中（防御性编程）
    if (initialId && wallpapers.find(w => w.id === initialId)) {
      set({ selectedId: initialId });
      return;
    }

    // 3. 默认选中排序后的第一个
    const sorted = get().getFilteredWallpapers();
    if (sorted.length > 0) {
      set({ selectedId: sorted[0].id });
    }
  },

  // ===== Playlist 方法实现 =====

  loadPlaylists: async () => {
    const isTauri = isTauriEnv();
    
    try {
      if (isTauri) {
        // 从后端加载
        const playlists = await invoke<Playlist[]>('get_playlists');
        const cyclePlaylistId = await invoke<string | null>('get_cycle_playlist');
        const sidebarOpen = await invoke<boolean>('get_playlist_sidebar_open');
        set({ playlists, cyclePlaylistId, isPlaylistSidebarOpen: sidebarOpen, isHydrated: true });
      } else {
        // 浏览器开发环境：从 localStorage 加载
        const stored = localStorage.getItem('lwg_playlists');
        const playlists = stored ? JSON.parse(stored) : [];
        const cyclePlaylistId = localStorage.getItem('lwg_cycle_playlist') || null;
        const sidebarOpen = localStorage.getItem('lwg_sidebar_open') !== 'false';
        set({ playlists, cyclePlaylistId, isPlaylistSidebarOpen: sidebarOpen, isHydrated: true });
      }
    } catch (error) {
      console.error('Failed to load playlists:', error);
      set({ isHydrated: true }); // 即使失败也标记完成
    }
  },

  createPlaylist: async (name: string, wallpaperIds: string[]) => {
    const isTauri = isTauriEnv();
    const state = get();
    
    // 检查空名称
    const trimmedName = name.trim().slice(0, 100);
    if (trimmedName.length === 0) {
      toast.error('Invalid playlist name', {
        description: 'Playlist name cannot be empty.'
      });
      throw new Error('Empty playlist name');
    }
    
    // 检查同名
    const existingPlaylist = state.playlists.find(
      p => p.name.toLowerCase() === trimmedName.toLowerCase()
    );
    if (existingPlaylist) {
      toast.error('Playlist name already exists', {
        description: `A playlist named "${trimmedName}" already exists.`
      });
      throw new Error('Duplicate playlist name');
    }
    
    // 前端生成 UUID
    const id = crypto.randomUUID();
    const now = Math.floor(Date.now() / 1000);
    
    const newPlaylist: Playlist = {
      id,
      name: trimmedName,
      wallpaperIds: Array.from(new Set(wallpaperIds)), // 去重
      createdAt: now,
      updatedAt: now,
    };
    
    // 乐观更新
    const previousPlaylists = state.playlists;
    set({ playlists: [...previousPlaylists, newPlaylist] });
    
    // 持久化
    if (isTauri) {
      try {
        await invoke('create_playlist', { id, name: newPlaylist.name, wallpaperIds: newPlaylist.wallpaperIds });
        toast.success('Playlist created');
      } catch (error) {
        // 回滚
        set({ playlists: previousPlaylists });
        console.error('Failed to create playlist:', error);
        toast.error('Failed to create playlist', { description: String(error) });
        throw error;
      }
    } else {
      localStorage.setItem('lwg_playlists', JSON.stringify(get().playlists));
      toast.success('Playlist created');
    }
  },

  renamePlaylist: async (id: string, name: string) => {
    const isTauri = isTauriEnv();
    
    const trimmedName = name.trim().slice(0, 100);
    
    // 检查空名称
    if (trimmedName.length === 0) {
      toast.error('Invalid playlist name', {
        description: 'Playlist name cannot be empty.'
      });
      throw new Error('Empty playlist name');
    }
    
    // 检查重名（排除自己）
    const currentPlaylists = get().playlists;
    const duplicate = currentPlaylists.find(
      p => p.id !== id && p.name.toLowerCase() === trimmedName.toLowerCase()
    );
    if (duplicate) {
      toast.error('Playlist name already exists', {
        description: `A playlist named "${trimmedName}" already exists.`
      });
      throw new Error('Duplicate playlist name');
    }
    
    const previousPlaylists = currentPlaylists;
    
    // 乐观更新
    const updatedPlaylists = previousPlaylists.map(p =>
      p.id === id ? { ...p, name: trimmedName, updatedAt: Math.floor(Date.now() / 1000) } : p
    );
    set({ playlists: updatedPlaylists });
    
    // 持久化
    if (isTauri) {
      try {
        await invoke('update_playlist', { id, name: trimmedName });
        toast.success('Playlist renamed');
      } catch (error) {
        set({ playlists: previousPlaylists });
        console.error('Failed to rename playlist:', error);
        toast.error('Failed to rename playlist', { description: String(error) });
        throw error;
      }
    } else {
      localStorage.setItem('lwg_playlists', JSON.stringify(updatedPlaylists));
      toast.success('Playlist renamed');
    }
  },

  deletePlaylist: async (id: string) => {
    const isTauri = isTauriEnv();
    const state = get();
    
    // 保存状态以便回滚
    const previousPlaylists = state.playlists;
    const previousActivePlaylistId = state.activePlaylistId;
    const previousCyclePlaylistId = state.cyclePlaylistId;
    
    // 防御 1：如果删除的是当前正在查看的列表，退回到 ALL
    if (state.activePlaylistId === id) {
      set({ activePlaylistId: null });
    }
    
    // 防御 2：如果删除的是轮换列表，清除轮换设置
    if (state.cyclePlaylistId === id) {
      if (isTauri) {
        try {
          await invoke('set_cycle_playlist', { id: null });
        } catch (e) {
          console.error('Failed to clear cycle playlist:', e);
        }
      }
      set({ cyclePlaylistId: null });
    }
    
    // 从列表中移除
    const newPlaylists = previousPlaylists.filter(p => p.id !== id);
    set({ playlists: newPlaylists });
    
    // 持久化
    if (isTauri) {
      try {
        await invoke('delete_playlist', { id });
        toast.success('Playlist deleted');
      } catch (error) {
        // 完整回滚：恢复 playlists, activePlaylistId, cyclePlaylistId
        set({ 
          playlists: previousPlaylists,
          activePlaylistId: previousActivePlaylistId,
          cyclePlaylistId: previousCyclePlaylistId
        });
        // 如果之前有 cycle playlist，尝试恢复后端状态
        if (previousCyclePlaylistId === id) {
          try {
            await invoke('set_cycle_playlist', { id: previousCyclePlaylistId });
          } catch (e) {
            console.error('Failed to restore cycle playlist:', e);
          }
        }
        console.error('Failed to delete playlist:', error);
        toast.error('Failed to delete playlist', { description: String(error) });
        throw error;
      }
    } else {
      localStorage.setItem('lwg_playlists', JSON.stringify(newPlaylists));
      toast.success('Playlist deleted');
    }
  },

  reorderPlaylists: async (orderedIds: string[]) => {
    const isTauri = isTauriEnv();
    const state = get();
    
    // 根据 orderedIds 重新排序 playlists
    const playlistMap = new Map(state.playlists.map(p => [p.id, p]));
    const reorderedPlaylists = orderedIds
      .map(id => playlistMap.get(id))
      .filter((p): p is Playlist => p !== undefined);
    
    // 乐观更新
    set({ playlists: reorderedPlaylists });
    
    // 持久化
    if (isTauri) {
      try {
        await invoke('reorder_playlists', { orderedIds });
      } catch (error) {
        console.error('Failed to persist reorder:', error);
        toast.error('Failed to save playlist order');
        // 可选：重新加载恢复状态
        await get().loadPlaylists();
      }
    } else {
      localStorage.setItem('lwg_playlists', JSON.stringify(reorderedPlaylists));
    }
  },

  addToPlaylist: async (playlistId: string, newWallpaperIds: string[]) => {
    const isTauri = isTauriEnv();
    const state = get();
    const playlist = state.playlists.find(p => p.id === playlistId);
    
    if (!playlist) {
      toast.error('Playlist not found');
      return;
    }
    
    // 过滤出真正新增的 ID
    const existingIds = new Set(playlist.wallpaperIds);
    const actuallyNewIds = newWallpaperIds.filter(id => !existingIds.has(id));
    
    // 如果没有新增，直接返回
    if (actuallyNewIds.length === 0) {
      toast.info('All selected wallpapers are already in this playlist');
      return;
    }
    
    // 合并后去重
    const dedupedIds = [...playlist.wallpaperIds, ...actuallyNewIds];
    
    // 乐观更新
    const previousPlaylists = state.playlists;
    const updatedPlaylists = previousPlaylists.map(p =>
      p.id === playlistId
        ? { ...p, wallpaperIds: dedupedIds, updatedAt: Math.floor(Date.now() / 1000) }
        : p
    );
    set({ playlists: updatedPlaylists });
    
    // 持久化
    if (isTauri) {
      try {
        await invoke('update_playlist', { id: playlistId, wallpaperIds: dedupedIds });
        toast.success(`Added ${actuallyNewIds.length} wallpaper(s) to playlist`);
      } catch (error) {
        set({ playlists: previousPlaylists });
        console.error('Failed to add to playlist:', error);
        toast.error('Failed to add to playlist', { description: String(error) });
        throw error;
      }
    } else {
      localStorage.setItem('lwg_playlists', JSON.stringify(updatedPlaylists));
      toast.success(`Added ${actuallyNewIds.length} wallpaper(s) to playlist`);
    }
  },

  removeFromPlaylist: async (playlistId: string, wallpaperId: string) => {
    const isTauri = isTauriEnv();
    const state = get();
    const playlist = state.playlists.find(p => p.id === playlistId);
    
    if (!playlist) {
      toast.error('Playlist not found');
      return;
    }
    
    const newWallpaperIds = playlist.wallpaperIds.filter(id => id !== wallpaperId);
    
    // 乐观更新
    const previousPlaylists = state.playlists;
    const updatedPlaylists = previousPlaylists.map(p =>
      p.id === playlistId
        ? { ...p, wallpaperIds: newWallpaperIds, updatedAt: Math.floor(Date.now() / 1000) }
        : p
    );
    set({ playlists: updatedPlaylists });
    
    // 持久化
    if (isTauri) {
      try {
        await invoke('update_playlist', { id: playlistId, wallpaperIds: newWallpaperIds });
      } catch (error) {
        set({ playlists: previousPlaylists });
        console.error('Failed to remove from playlist:', error);
        toast.error('Failed to remove from playlist', { description: String(error) });
        throw error;
      }
    } else {
      localStorage.setItem('lwg_playlists', JSON.stringify(updatedPlaylists));
    }
  },

  setActivePlaylist: (id: string | null) => {
    set({ activePlaylistId: id });
  },

  setCyclePlaylist: async (id: string | null) => {
    const isTauri = isTauriEnv();
    const previousCyclePlaylistId = get().cyclePlaylistId;

    set({ cyclePlaylistId: id });
    
    if (isTauri) {
      try {
        await invoke('set_cycle_playlist', { id });
      } catch (error) {
        set({ cyclePlaylistId: previousCyclePlaylistId });
        console.error('Failed to set cycle playlist:', error);
        toast.error('Failed to set cycle playlist', { description: String(error) });
      }
    } else {
      if (id) {
        localStorage.setItem('lwg_cycle_playlist', id);
      } else {
        localStorage.removeItem('lwg_cycle_playlist');
      }
    }
  },

  togglePlaylistSidebar: () => {
    const isTauri = isTauriEnv();
    const previousOpen = get().isPlaylistSidebarOpen;
    const newOpen = !get().isPlaylistSidebarOpen;
    set({ isPlaylistSidebarOpen: newOpen });
    
    if (isTauri) {
      invoke('set_playlist_sidebar_open', { open: newOpen }).catch((error) => {
        set({ isPlaylistSidebarOpen: previousOpen });
        console.error('Failed to set playlist sidebar open:', error);
        toast.error('Failed to toggle sidebar', { description: String(error) });
      });
    } else {
      localStorage.setItem('lwg_sidebar_open', String(newOpen));
    }
  },

  togglePlaylistSidebarPin: () => {
    const newPinned = !get().isPlaylistSidebarPinned;
    set({ isPlaylistSidebarPinned: newPinned });
  },

  openPlaylistSidebarFloating: () => {
    // 打开悬浮模式（不锁定）
    set({ isPlaylistSidebarOpen: true, isPlaylistSidebarPinned: false });
  },

  enterSelectionMode: () => {
    set({ isSelectionMode: true, selectedForPlaylist: new Set() });
  },

  exitSelectionMode: () => {
    set({ isSelectionMode: false, selectedForPlaylist: new Set() });
  },

  toggleSelectForPlaylist: (wallpaperId: string) => {
    const state = get();
    const newSet = new Set(state.selectedForPlaylist);
    
    if (newSet.has(wallpaperId)) {
      newSet.delete(wallpaperId);
    } else {
      // 检查是否超过上限
      if (newSet.size >= MAX_SELECTION_COUNT) {
        toast.warning(`Maximum ${MAX_SELECTION_COUNT} wallpapers can be selected at once`);
        return;
      }
      newSet.add(wallpaperId);
    }
    
    set({ selectedForPlaylist: newSet });
  },

  selectAllForPlaylist: () => {
    const state = get();
    const visibleWallpapers = state.getFilteredWallpapers();
    
    // 数量限制保护
    if (visibleWallpapers.length > MAX_SELECTION_COUNT) {
      toast.warning(`Too many wallpapers (${visibleWallpapers.length}). Only first ${MAX_SELECTION_COUNT} will be selected.`);
      const limited = visibleWallpapers.slice(0, MAX_SELECTION_COUNT);
      set({ selectedForPlaylist: new Set(limited.map(w => w.id)) });
    } else {
      set({ selectedForPlaylist: new Set(visibleWallpapers.map(w => w.id)) });
    }
  },

  deselectAllForPlaylist: () => {
    set({ selectedForPlaylist: new Set() });
  },

  createPlaylistFromSelection: async (name: string) => {
    const state = get();
    const selectedIds = Array.from(state.selectedForPlaylist);
    
    if (selectedIds.length === 0) {
      toast.warning('No wallpapers selected');
      return;
    }
    
    await get().createPlaylist(name, selectedIds);
    
    // 创建成功后退出选择模式
    set({ isSelectionMode: false, selectedForPlaylist: new Set() });
  },

  initApp: async () => {
    // 1. 并发加载基础数据（互不依赖，提升启动速度）
    await Promise.all([
      get().loadWallpapers(),
      get().initializeSettings(),
      get().loadPlaylists(),
    ]);

    // 2. 数据就绪后，执行初始选中逻辑
    get().initializeSelectedWallpaper();

    // 3. 其他启动任务
    get().fetchMonitors();
    get().fetchAppVersion();
  },
}));
