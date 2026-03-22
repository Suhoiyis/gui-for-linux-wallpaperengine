// src/hooks/useActiveWallpapers.ts
import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import { isTauriEnv } from "@/lib/utils";

export interface ActiveWallpaper {
  screen: string;
  wallpaperId: string;
}

export function useActiveWallpapers() {
  const [activeWallpapers, setActiveWallpapers] = useState<Map<string, string>>(new Map());
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!isTauriEnv()) {
      setIsLoading(false);
      return;
    }

    const fetchActiveWallpapers = async () => {
      try {
        const result = await invoke<Record<string, { wallpaperId: string; isPlaying: boolean }>>("get_active_wallpapers");
        const activeMap = new Map<string, string>();
        for (const [screen, aw] of Object.entries(result)) {
          if (aw.isPlaying) {
            activeMap.set(screen, aw.wallpaperId);
          }
        }
        setActiveWallpapers(activeMap);
        setIsLoading(false);
      } catch (error) {
        console.error("Failed to get active wallpapers:", error);
        setIsLoading(false);
      }
    };

    fetchActiveWallpapers();

    const setupListeners = async () => {
      const unlistenWp = await listen("wallpaper-changed", () => {
        fetchActiveWallpapers();
      });
      return [unlistenWp];
    };

    let unlisteners: (() => void)[] = [];
    setupListeners().then((fns) => {
      unlisteners = fns;
    });

    return () => {
      unlisteners.forEach((fn) => fn());
    };
  }, []);

  return { activeWallpapers, isLoading };
}