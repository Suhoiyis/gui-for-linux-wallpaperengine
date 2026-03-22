"use client";

import { useState, useEffect, useMemo, useCallback } from "react";
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "@/components/ui/command";
import {
  Activity,
  Shuffle,
  Square,
  Camera,
  RefreshCw,
  Star,
  Volume2,
  Gauge,
  FolderOpen,
  ListMusic,
} from "lucide-react";
import { useAppStore } from "@/store/appStore";
import { getHistory } from "@/api/wallpaper";
import { HistoryEntry } from "@/types";
import { getDisplayName } from "@/lib/utils";
import { FAVORITES_PLAYLIST_ID } from "@/lib/constants";
import { Thumbnail } from "@/components/common/Thumbnail";
import { toast } from "sonner";
import {
  computePlaylistMatchedWallpaperCounts,
  mergeAndRankPlaylistsForSearch,
} from "@/lib/commandPaletteSearch";

// Valid settings fields for navigation (type safety)
const VALID_SETTINGS_FIELDS = [
  "volume",
  "fps",
  "scaling",
  "clamping",
  "workshopPath",
  "assetsPath",
  "screenshotDelay",
  "screenshotRes",
  "preferXvfb",
  "cycleEnabled",
  "cycleInterval",
  "cycleOrder",
] as const;

type SettingsField = (typeof VALID_SETTINGS_FIELDS)[number];

function isValidSettingsField(field: string): field is SettingsField {
  return VALID_SETTINGS_FIELDS.includes(field as SettingsField);
}

// Token matching helper for unified search
function matchesTokens(
  tokens: string[],
  fields: Array<string | null | undefined>,
  keywords: string[] = []
): boolean {
  if (tokens.length === 0) return true;
  const haystacks = [
    ...fields.filter((f): f is string => Boolean(f)).map((f) => f.toLowerCase()),
    ...keywords.map((k) => k.toLowerCase()),
  ];
  return tokens.every((tok) => haystacks.some((h) => h.includes(tok)));
}

export function CommandPalette() {
  // Local state for search query (filtering only)
  const [search, setSearch] = useState("");
  const [recentWallpapers, setRecentWallpapers] = useState<HistoryEntry[]>([]);

  // Global state from Zustand store
  const isCommandPaletteOpen = useAppStore((state) => state.isCommandPaletteOpen);
  const setCommandPaletteOpen = useAppStore((state) => state.setCommandPaletteOpen);
  
  // Store data
  const wallpapers = useAppStore((state) => state.wallpapers);
  const favoriteIds = useAppStore((state) => state.favoriteIds);
  const nicknames = useAppStore((state) => state.nicknames);
  const settings = useAppStore((state) => state.settings);
  const playlists = useAppStore((state) => state.playlists);
  const cyclePlaylistId = useAppStore((state) => state.cyclePlaylistId);
  
  // Store actions
  const applyWallpaper = useAppStore((state) => state.applyWallpaper);
  const stopWallpaper = useAppStore((state) => state.stopWallpaper);
  const applyRandomWallpaper = useAppStore((state) => state.applyRandomWallpaper);
  const loadWallpapers = useAppStore((state) => state.loadWallpapers);
  const setActiveTab = useAppStore((state) => state.setActiveTab);
  const setActivePlaylist = useAppStore((state) => state.setActivePlaylist);
  const setHighlightSettingField = useAppStore((state) => state.setHighlightSettingField);
  const setScreenshotHintActive = useAppStore((state) => state.setScreenshotHintActive);

  // Keyboard shortcut: Cmd+K (Mac) / Ctrl+K (Windows/Linux)
  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault(); // CRITICAL: Prevent browser default search behavior
        // Use getState() to avoid stale closure
        const currentState = useAppStore.getState().isCommandPaletteOpen;
        setCommandPaletteOpen(!currentState);
      }
    };

    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, [setCommandPaletteOpen]);

  // Load recent wallpapers when dialog opens (with race condition protection)
  useEffect(() => {
    let ignore = false; // Prevent stale updates after unmount/close
    
    if (isCommandPaletteOpen) {
      setSearch(""); // Clear search when opening
      
      getHistory()
        .then((data) => {
          if (!ignore) {
            setRecentWallpapers(data);
          }
        })
        .catch((error) => {
          if (!ignore) {
            console.error("Failed to load recent wallpapers:", error);
            toast.error("Failed to load recent wallpapers", {
              description: String(error),
            });
          }
        });
    }
    
    return () => {
      ignore = true; // Cleanup: ignore pending responses
    };
  }, [isCommandPaletteOpen]);

  // ========== Action Handlers ==========

  const handleRandom = useCallback(async () => {
    try {
      await applyRandomWallpaper();
      setCommandPaletteOpen(false);
    } catch (error) {
      console.error("Random wallpaper failed:", error);
      toast.error("Failed to apply random wallpaper", {
        description: String(error),
      });
    }
  }, [applyRandomWallpaper, setCommandPaletteOpen]);

  const handleStop = useCallback(async () => {
    try {
      await stopWallpaper();
      setCommandPaletteOpen(false);
    } catch (error) {
      console.error("Stop wallpaper failed:", error);
      toast.error("Failed to stop wallpaper", {
        description: String(error),
      });
    }
  }, [stopWallpaper, setCommandPaletteOpen]);

  const handleScreenshot = useCallback(() => {
    setActiveTab("wallpapers");
    setScreenshotHintActive(true);
    setCommandPaletteOpen(false);
  }, [setActiveTab, setScreenshotHintActive, setCommandPaletteOpen]);

  const handleRefresh = useCallback(async () => {
    try {
      await loadWallpapers();
      setCommandPaletteOpen(false);
    } catch (error) {
      console.error("Refresh failed:", error);
      toast.error("Failed to refresh library", {
        description: String(error),
      });
    }
  }, [loadWallpapers, setCommandPaletteOpen]);

  const handleSettingsNavigate = (field: string) => {
    if (!isValidSettingsField(field)) {
      console.warn(`Invalid settings field: ${field}`);
      return;
    }
    setActiveTab("settings");
    setHighlightSettingField(field);
    setCommandPaletteOpen(false);
  };

  const handleMonitorNavigate = () => {
    setActiveTab("performance");
    setCommandPaletteOpen(false);
  };

  const handleApplyWallpaper = async (id: string) => {
    try {
      await applyWallpaper(id);
      setCommandPaletteOpen(false);
    } catch (error) {
      console.error("Apply wallpaper failed:", error);
      toast.error("Failed to apply wallpaper", {
        description: String(error),
      });
    }
  };

  const handleViewFavorites = () => {
    setActiveTab("wallpapers");
    setActivePlaylist(FAVORITES_PLAYLIST_ID);
    setCommandPaletteOpen(false);
  };

  const handleViewPlaylist = (playlistId: string) => {
    setActiveTab("wallpapers");
    setActivePlaylist(playlistId);
    setCommandPaletteOpen(false);
  };

  // ========== Computed Data ==========

  // Search tokenization
  const trimmedSearch = search.trim();
  const searchTokens = useMemo(() => {
    if (!trimmedSearch) return [];
    return trimmedSearch
      .toLowerCase()
      .split(/\s+/)
      .map((t) => t.trim())
      .filter(Boolean);
  }, [trimmedSearch]);

  const hasSearch = searchTokens.length > 0;

  // Single-pass wallpaper matching (optimization: avoids duplicate scan)
  const { filteredWallpapers, matchedWallpaperIdsForPlaylists } = useMemo(() => {
    if (!hasSearch) {
      return {
        filteredWallpapers: [] as typeof wallpapers,
        matchedWallpaperIdsForPlaylists: new Set<string>(),
      };
    }

    const filtered: typeof wallpapers = [];
    const ids = new Set<string>();

    for (const w of wallpapers) {
      const hit = matchesTokens(
        searchTokens,
        [w.title || "", w.id, nicknames[w.id] || "", w.type],
        ["wallpaper", "library"]
      );
      if (!hit) continue;

      ids.add(w.id);
      if (filtered.length < 8) filtered.push(w);
    }

    return { filteredWallpapers: filtered, matchedWallpaperIdsForPlaylists: ids };
  }, [hasSearch, searchTokens, wallpapers, nicknames]);

  const playlistMatchedWallpaperCountById = useMemo(() => {
    if (!hasSearch) return new Map<string, number>();
    return computePlaylistMatchedWallpaperCounts(
      playlists,
      matchedWallpaperIdsForPlaylists
    );
  }, [hasSearch, playlists, matchedWallpaperIdsForPlaylists]);

  const nameMatchedPlaylists = useMemo(() => {
    if (!hasSearch) return [];
    return playlists.filter((p) =>
      matchesTokens(
        searchTokens,
        [p.name, p.id],
        ["playlist", cyclePlaylistId === p.id ? "cycle" : ""]
      )
    );
  }, [hasSearch, searchTokens, playlists, cyclePlaylistId]);

  // Filtered playlists for search (Library group) — merged name-match + contains-match
  const filteredPlaylists = useMemo(() => {
    if (!hasSearch) return [];
    return mergeAndRankPlaylistsForSearch({
      playlists,
      nameMatchedPlaylists,
      matchedCountById: playlistMatchedWallpaperCountById,
      cyclePlaylistId,
      limit: 5,
    });
  }, [hasSearch, playlists, nameMatchedPlaylists, playlistMatchedWallpaperCountById, cyclePlaylistId]);

  // Settings nav items with keywords
  const settingsNavItems = useMemo(
    () => [
      {
        id: "settings-volume",
        label: `Volume: ${settings?.volume ?? 50}%`,
        field: "volume" as const,
        keywords: ["audio", "sound", "loudness"],
        icon: <Volume2 className="h-4 w-4 text-blue-500" />,
      },
      {
        id: "settings-fps",
        label: `FPS: ${settings?.fps ?? 30}`,
        field: "fps" as const,
        keywords: ["frame", "framerate", "performance"],
        icon: <Gauge className="h-4 w-4 text-emerald-500" />,
      },
      {
        id: "settings-workshop",
        label: "Workshop Path",
        field: "workshopPath" as const,
        keywords: ["steam", "workshop", "path", "folder", "directory"],
        icon: <FolderOpen className="h-4 w-4 text-amber-500" />,
      },
    ],
    [settings?.volume, settings?.fps]
  );

  // Filtered settings nav items
  const filteredSettingsNavItems = useMemo(() => {
    if (!hasSearch) return settingsNavItems;
    return settingsNavItems.filter((it) =>
      matchesTokens(searchTokens, [it.id, it.label, it.field], it.keywords)
    );
  }, [hasSearch, searchTokens, settingsNavItems]);

  // Monitor matches search
  const monitorMatchesSearch = useMemo(() => {
    if (!hasSearch) return true;
    return matchesTokens(
      searchTokens,
      ["Open Performance Monitor", "monitor", "performance"],
      ["cpu", "memory", "usage", "stats", "activity"]
    );
  }, [hasSearch, searchTokens]);

  // Quick action items with keywords
  const quickActionItems = useMemo(
    () => [
      {
        id: "action-random",
        label: "Random Wallpaper",
        keywords: ["random", "shuffle", "lucky", "dice"],
        icon: <Shuffle className="h-4 w-4 text-pink-500" />,
        shortcut: "Ctrl+R",
        onSelect: handleRandom,
      },
      {
        id: "action-stop",
        label: "Stop All",
        keywords: ["stop", "kill", "terminate", "end"],
        icon: <Square className="h-4 w-4 text-red-500" />,
        shortcut: "Ctrl+S",
        onSelect: handleStop,
      },
      {
        id: "action-screenshot",
        label: "Screenshot",
        keywords: ["screenshot", "capture", "photo", "snap"],
        icon: <Camera className="h-4 w-4 text-cyan-500" />,
        shortcut: "Ctrl+P",
        onSelect: handleScreenshot,
      },
      {
        id: "action-refresh",
        label: "Refresh Library",
        keywords: ["refresh", "reload", "rescan", "scan"],
        icon: <RefreshCw className="h-4 w-4 text-teal-500" />,
        shortcut: "Ctrl+L",
        onSelect: handleRefresh,
      },
    ],
    [handleRandom, handleStop, handleScreenshot, handleRefresh]
  );

  // Filtered quick action items
  const filteredQuickActionItems = useMemo(() => {
    if (!hasSearch) return quickActionItems;
    return quickActionItems.filter((it) =>
      matchesTokens(searchTokens, [it.id, it.label], it.keywords)
    );
  }, [hasSearch, searchTokens, quickActionItems]);

  // Format relative time
  const formatTimeAgo = (timestamp: string): string => {
    const t = new Date(timestamp).getTime();
    if (!Number.isFinite(t)) return "—";

    const diffMs = Date.now() - t;
    if (!Number.isFinite(diffMs)) return "—";

    const minutes = Math.max(0, Math.floor(diffMs / 60000));
    if (minutes < 60) return `${minutes}m ago`;

    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;

    return `${Math.floor(hours / 24)}d ago`;
  };

  // ========== Playlist Display Logic ==========
  
  // Select playlists to display (max 3)
  // Priority: 1) cyclePlaylistId 2) sortBy updatedAt (most recent)
  const displayedPlaylists = useMemo(() => {
    if (playlists.length === 0) return [];
    
    // 1. Find cycle playlist (if set)
    const cyclePlaylist = cyclePlaylistId 
      ? playlists.find(p => p.id === cyclePlaylistId) 
      : null;
    
    // 2. Other playlists sorted by updatedAt (most recent first)
    const otherPlaylists = playlists
      .filter(p => p.id !== cyclePlaylistId)
      .sort((a, b) => b.updatedAt - a.updatedAt);
    
    // 3. Combine: cycle playlist first, then recent ones
    const result: typeof playlists = [];
    
    if (cyclePlaylist) {
      result.push(cyclePlaylist);
    }
    
    // Fill remaining slots (max 3 total)
    const remaining = 3 - result.length;
    result.push(...otherPlaylists.slice(0, remaining));
    
    return result;
  }, [playlists, cyclePlaylistId]);

  // ========== Render ==========

  return (
    <CommandDialog open={isCommandPaletteOpen} onOpenChange={setCommandPaletteOpen}>
      <CommandInput
        placeholder="Search wallpapers, settings, commands..."
        value={search}
        onValueChange={setSearch}
      />
      <CommandList>
        <CommandEmpty>
          {trimmedSearch ? `No results for "${trimmedSearch}"` : "Start typing to search..."}
        </CommandEmpty>

        {/* Library Group - Show when no search */}
        {!hasSearch && (
          <>
            <CommandGroup heading="Library">
              {/* Recent Wallpapers */}
              {recentWallpapers.slice(0, 3).map((entry) => {
                const { displayName } = getDisplayName(nicknames, entry.id, entry.title);
                return (
                  <CommandItem
                    key={entry.id}
                    value={`recent-${entry.id}`}
                    onSelect={() => handleApplyWallpaper(entry.id)}
                  >
                    <Thumbnail wallpaperId={entry.id} className="w-5 h-5 rounded" />
                    <span className="truncate">{displayName}</span>
                    <span className="ml-auto text-xs text-muted-foreground">
                      {formatTimeAgo(entry.timestamp)}
                    </span>
                  </CommandItem>
                );
              })}
              
              {/* User Playlists: Favorites (常驻) + 3 recent playlists */}
              {/* Favorites - always first */}
              {favoriteIds.size > 0 && (
                <CommandItem value="view-favorites" onSelect={handleViewFavorites}>
                  <Star className="h-4 w-4 text-yellow-500" />
                  <span>Favorites</span>
                  <span className="ml-auto text-xs text-muted-foreground">
                    {favoriteIds.size} items
                  </span>
                </CommandItem>
              )}
              
              {/* Recent playlists (max 3, sorted by cycle + recent update) */}
              {displayedPlaylists.map((playlist) => (
                <CommandItem
                  key={playlist.id}
                  value={`playlist-${playlist.id}`}
                  onSelect={() => handleViewPlaylist(playlist.id)}
                >
                  <ListMusic className="h-4 w-4 text-violet-500" />
                  <span className="truncate">{playlist.name}</span>
                  <span className="ml-auto text-xs text-muted-foreground flex items-center gap-1">
                    {cyclePlaylistId === playlist.id && (
                      <span className="text-primary font-medium">cycle</span>
                    )}
                    {playlist.wallpaperIds.length} items
                  </span>
                </CommandItem>
              ))}
            </CommandGroup>
            <CommandSeparator />
          </>
        )}

        {/* Search Mode - Unified Groups */}
        {hasSearch && (() => {
          // Favorites only shown when search matches favorites keywords
          const favoritesVisible =
            favoriteIds.size > 0 &&
            matchesTokens(searchTokens, ["Favorites", "Starred"], [
              "favorite",
              "favorites",
              "favourite",
              "favourites",
              "star",
              "starred",
              "liked",
            ]);

          const libraryVisible =
            filteredWallpapers.length > 0 ||
            filteredPlaylists.length > 0 ||
            favoritesVisible;
          const settingsVisible = filteredSettingsNavItems.length > 0;
          const monitorVisible = monitorMatchesSearch;
          const actionsVisible = filteredQuickActionItems.length > 0;

          return (
            <>
              {/* Library Group (Wallpapers + Playlists + Favorites) */}
              {libraryVisible && (
                <CommandGroup heading="Library">
                  {filteredWallpapers.map((wp) => {
                    const { displayName } = getDisplayName(nicknames, wp.id, wp.title);
                    return (
                      <CommandItem
                        key={`lib-wp-${wp.id}`}
                        value={`${wp.title} ${wp.id} ${nicknames[wp.id] || ""} wallpaper`}
                        onSelect={() => handleApplyWallpaper(wp.id)}
                      >
                        <Thumbnail wallpaperId={wp.id} className="w-5 h-5 rounded" />
                        <span className="truncate">{displayName}</span>
                        <span className="ml-auto text-xs text-muted-foreground">
                          {wp.type}
                        </span>
                      </CommandItem>
                    );
                  })}

                  {filteredWallpapers.length > 0 && (favoritesVisible || filteredPlaylists.length > 0) && (
                    <CommandSeparator />
                  )}

                  {/* Favorites - only shown when search matches keywords */}
                  {favoritesVisible && (
                    <CommandItem value="view-favorites-search" onSelect={handleViewFavorites}>
                      <Star className="h-4 w-4 text-yellow-500" />
                      <span>Favorites</span>
                      <span className="ml-auto text-xs text-muted-foreground">
                        {favoriteIds.size} items
                      </span>
                    </CommandItem>
                  )}

                  {/* Other playlists */}
                  {filteredPlaylists.map((playlist) => {
                    const matchCount =
                      playlistMatchedWallpaperCountById.get(playlist.id) ?? 0;
                    return (
                      <CommandItem
                        key={`lib-pl-${playlist.id}`}
                        value={`${playlist.name} playlist ${cyclePlaylistId === playlist.id ? "cycle" : ""}`}
                        onSelect={() => handleViewPlaylist(playlist.id)}
                      >
                        <ListMusic className="h-4 w-4 text-violet-500" />
                        <span className="truncate">{playlist.name}</span>
                        <span className="ml-auto text-xs text-muted-foreground flex items-center gap-1">
                          {cyclePlaylistId === playlist.id && (
                            <span className="text-primary font-medium">cycle</span>
                          )}
                          {matchCount > 0 && (
                            <span>
                              {matchCount} match{matchCount === 1 ? "" : "es"}
                            </span>
                          )}
                          {playlist.wallpaperIds.length} items
                        </span>
                      </CommandItem>
                    );
                  })}
                </CommandGroup>
              )}

              {libraryVisible && (settingsVisible || monitorVisible || actionsVisible) && (
                <CommandSeparator />
              )}

              {/* Settings Group */}
              {settingsVisible && (
                <CommandGroup heading="Settings">
                  {filteredSettingsNavItems.map((it) => (
                    <CommandItem
                      key={it.id}
                      value={`${it.label} ${it.field} ${it.keywords.join(" ")}`}
                      onSelect={() => handleSettingsNavigate(it.field)}
                    >
                      {it.icon}
                      <span>{it.label}</span>
                    </CommandItem>
                  ))}
                </CommandGroup>
              )}

              {settingsVisible && (monitorVisible || actionsVisible) && (
                <CommandSeparator />
              )}

              {/* Monitor Group */}
              {monitorVisible && (
                <CommandGroup heading="Monitor">
                  <CommandItem value="monitor-open-search" onSelect={handleMonitorNavigate}>
                    <Activity className="h-4 w-4 text-purple-500" />
                    <span>Open Performance Monitor</span>
                  </CommandItem>
                </CommandGroup>
              )}

              {monitorVisible && actionsVisible && <CommandSeparator />}

              {/* Quick Actions Group */}
              {actionsVisible && (
                <CommandGroup heading="Quick Actions">
                  {filteredQuickActionItems.map((it) => (
                    <CommandItem
                      key={it.id}
                      value={`${it.label} ${it.keywords.join(" ")}`}
                      onSelect={it.onSelect}
                    >
                      {it.icon}
                      <span>{it.label}</span>
                      {it.shortcut && (
                        <CommandShortcut>{it.shortcut}</CommandShortcut>
                      )}
                    </CommandItem>
                  ))}
                </CommandGroup>
              )}
            </>
          );
        })()}

        {/* Non-search mode: Settings/Monitor/Quick Actions */}
        {!hasSearch && (
          <>
            {/* Settings Group */}
            <CommandGroup heading="Settings">
              {settingsNavItems.map((it) => (
                <CommandItem
                  key={it.id}
                  value={it.id}
                  onSelect={() => handleSettingsNavigate(it.field)}
                >
                  {it.icon}
                  <span>{it.label}</span>
                </CommandItem>
              ))}
            </CommandGroup>

            <CommandSeparator />

            {/* Monitor Group */}
            <CommandGroup heading="Monitor">
              <CommandItem value="monitor-open" onSelect={handleMonitorNavigate}>
                <Activity className="h-4 w-4 text-purple-500" />
                <span>Open Performance Monitor</span>
              </CommandItem>
            </CommandGroup>

            <CommandSeparator />

            {/* Quick Actions Group */}
            <CommandGroup heading="Quick Actions">
              {quickActionItems.map((it) => (
                <CommandItem
                  key={it.id}
                  value={it.id}
                  onSelect={it.onSelect}
                >
                  {it.icon}
                  <span>{it.label}</span>
                  {it.shortcut && (
                    <CommandShortcut>{it.shortcut}</CommandShortcut>
                  )}
                </CommandItem>
              ))}
            </CommandGroup>
          </>
        )}
      </CommandList>
    </CommandDialog>
  );
}
