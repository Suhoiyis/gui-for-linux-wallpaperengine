import { useState, useRef, useEffect, useCallback } from "react";
import { Plus, ListMusic, List, Star, Pin, PinOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Skeleton } from "@/components/ui/skeleton";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";
import { useAppStore } from "@/store/appStore";
import { PlaylistList } from "./PlaylistList";
import { CreatePlaylistDialog } from "./CreatePlaylistDialog";
import { FAVORITES_PLAYLIST_ID } from "@/lib/constants";

function generateAvatarColor(name: string): string {
  const colors = [
    "bg-rose-500",
    "bg-pink-500",
    "bg-fuchsia-500",
    "bg-violet-500",
    "bg-indigo-500",
    "bg-blue-500",
    "bg-cyan-500",
    "bg-teal-500",
    "bg-emerald-500",
    "bg-lime-500",
    "bg-amber-500",
    "bg-orange-500",
  ];

  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
}

function getInitial(name: string): string {
  return name.charAt(0).toUpperCase();
}

// ===== 图标列（仅最小化模式使用）=====
function IconColumn() {
  const playlists = useAppStore((state) => state.playlists);
  const activePlaylistId = useAppStore((state) => state.activePlaylistId);
  const setActivePlaylist = useAppStore((state) => state.setActivePlaylist);
  const favoriteIds = useAppStore((state) => state.favoriteIds);

  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  return (
    <>
      {/* 占位 Header - 与悬浮/锁定模式 Header 高度对齐 */}
      <div className="shrink-0 h-[52px] border-b border-border/30" />

      <ScrollArea className="flex-1">
        <div className="flex flex-col items-center gap-1 p-2">
          <button
            onClick={() => setActivePlaylist(null)}
            className={cn(
              "w-9 h-9 rounded-md flex items-center justify-center transition-all duration-200",
              !activePlaylistId
                ? "bg-accent text-accent-foreground shadow-sm scale-110"
                : "text-muted-foreground hover:bg-accent/50 hover:text-foreground",
            )}
            title="All Wallpapers"
          >
            <ListMusic className="w-4 h-4" />
          </button>

          <Separator className="w-8" />

          <button
            onClick={() => setActivePlaylist(FAVORITES_PLAYLIST_ID)}
            className={cn(
              "w-9 h-9 rounded-md flex items-center justify-center transition-all duration-200",
              activePlaylistId === FAVORITES_PLAYLIST_ID
                ? "bg-accent shadow-sm scale-110"
                : "text-muted-foreground hover:bg-accent/50 hover:text-foreground",
            )}
            title={`Favorites (${favoriteIds.size})`}
          >
            <Star
              className={cn(
                "w-4 h-4 transition-all duration-200",
                activePlaylistId === FAVORITES_PLAYLIST_ID
                  ? "fill-yellow-400 text-yellow-400"
                  : "",
              )}
            />
          </button>

          {playlists.map((playlist) => (
            <button
              key={playlist.id}
              onClick={() => setActivePlaylist(playlist.id)}
              className={cn(
                "w-9 h-9 rounded-md flex items-center justify-center transition-all duration-200",
                activePlaylistId === playlist.id
                  ? "bg-accent shadow-sm scale-110"
                  : "hover:bg-accent/50",
              )}
              title={playlist.name}
            >
              <span
                className={cn(
                  "w-7 h-7 rounded-md flex items-center justify-center text-xs font-bold text-white transition-transform duration-200",
                  generateAvatarColor(playlist.name),
                  activePlaylistId === playlist.id && "scale-105",
                )}
              >
                {getInitial(playlist.name)}
              </span>
            </button>
          ))}
        </div>
      </ScrollArea>

      <div className="shrink-0 h-[48px] flex items-center justify-center border-t border-border/30">
        <button
          onClick={() => setIsCreateDialogOpen(true)}
          className="w-8 h-8 rounded-md flex items-center justify-center text-muted-foreground hover:bg-accent/50 hover:text-foreground transition-all duration-200"
          title="New Playlist"
        >
          <Plus className="w-4 h-4" />
        </button>
      </div>

      <CreatePlaylistDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
      />
    </>
  );
}

// ===== 展开面板内容（悬浮和锁定模式共用）=====

// ===== 悬浮面板内容 =====
function ExpandedSidebarContent({
  onTogglePin,
  isPinned,
}: {
  onTogglePin: () => void;
  isPinned: boolean;
}) {
  const activePlaylistId = useAppStore((state) => state.activePlaylistId);
  const setActivePlaylist = useAppStore((state) => state.setActivePlaylist);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  return (
    <>
      <div className="h-[52px] flex items-center justify-between px-3 border-b border-border/30 shrink-0">
        <div className="flex items-center gap-2">
          <List className="w-4 h-4 text-muted-foreground" />
          <span className="font-semibold text-sm">Playlists</span>
        </div>
        <div className="flex items-center gap-0.5">
          <Button
            variant="ghost"
            size="icon"
            className="h-7 w-7 transition-transform duration-200 hover:scale-110"
            onClick={onTogglePin}
            title={isPinned ? "Unpin (floating mode)" : "Pin (locked mode)"}
          >
            {isPinned ? (
              <PinOff className="w-4 h-4" />
            ) : (
              <Pin className="w-4 h-4" />
            )}
          </Button>
        </div>
      </div>

      <ScrollArea className="flex-1">
        <div className="p-2 space-y-1">
          <button
            onClick={() => setActivePlaylist(null)}
            className={cn(
              "w-full flex items-center gap-2 px-3 h-9 rounded-md text-sm transition-all duration-200",
              !activePlaylistId
                ? "bg-accent text-accent-foreground shadow-sm"
                : "text-muted-foreground hover:bg-accent/50 hover:text-foreground",
            )}
          >
            <span>All Wallpapers</span>
          </button>

          <Separator />

          <PlaylistList />
        </div>
      </ScrollArea>

      <div className="h-[48px] flex items-center px-2 border-t border-border/30 shrink-0">
        <Button
          variant="outline"
          size="sm"
          className="w-full justify-start gap-2 transition-all duration-200 hover:translate-x-0.5"
          onClick={() => setIsCreateDialogOpen(true)}
        >
          <Plus className="w-4 h-4" />
          <span>New Playlist</span>
        </Button>
      </div>

      <CreatePlaylistDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
      />
    </>
  );
}

// ===== 锁定面板（in-flow 定位，推开壁纸区域，和悬浮面板外观一致）=====
function LockedPanel({
  isClosingFromLocked,
  onTogglePin,
}: {
  isClosingFromLocked: boolean;
  onTogglePin: () => void;
}) {
  return (
    <div
      className={cn(
        "h-full bg-sidebar border-r border-border/30 shrink-0 overflow-hidden",
        "transition-[width] duration-300 ease-in-out",
        isClosingFromLocked ? "w-0" : "w-[220px]",
      )}
    >
      {/* 内部固定宽度，避免内容被挤压变形 */}
      <div className="w-[220px] h-full flex flex-col">
        <ExpandedSidebarContent onTogglePin={onTogglePin} isPinned={true} />
      </div>
    </div>
  );
}

// ===== 悬浮面板（absolute 定位，不推内容区域）=====
function FloatingPanel({
  isClosingToMinimized,
  isPinning,
  isFloating,
  onMouseEnter,
  onMouseLeave,
  onTogglePin,
}: {
  isClosingToMinimized: boolean;
  isPinning: boolean;
  isFloating: boolean;
  onMouseEnter?: () => void;
  onMouseLeave?: () => void;
  onTogglePin: () => void;
}) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    const raf1 = requestAnimationFrame(() => {
      const raf2 = requestAnimationFrame(() => setIsMounted(true));
      return () => cancelAnimationFrame(raf2);
    });
    return () => cancelAnimationFrame(raf1);
  }, []);

  const isOpen = isMounted && !isClosingToMinimized && !isPinning;

  return (
    <div
      className={cn(
        "absolute left-12 top-0 h-full w-[220px] z-30",
        "flex flex-col bg-sidebar border-r border-border/30",
        "transition-[transform,opacity] duration-300 ease-out",
        isOpen
          ? "translate-x-0 opacity-100 shadow-2xl"
          : "-translate-x-3 opacity-0 shadow-none",
        isPinning && "pointer-events-none",
      )}
      onMouseEnter={isFloating ? onMouseEnter : undefined}
      onMouseLeave={isFloating ? onMouseLeave : undefined}
    >
      <ExpandedSidebarContent onTogglePin={onTogglePin} isPinned={false} />
    </div>
  );
}

// ===== 主组件 =====
export function PlaylistSidebar() {
  const isHydrated = useAppStore((state) => state.isHydrated);
  const isOpen = useAppStore((state) => state.isPlaylistSidebarOpen);
  const isPinned = useAppStore((state) => state.isPlaylistSidebarPinned);
  const togglePlaylistSidebar = useAppStore(
    (state) => state.togglePlaylistSidebar,
  );
  const togglePlaylistSidebarPin = useAppStore(
    (state) => state.togglePlaylistSidebarPin,
  );
  const openPlaylistSidebarFloating = useAppStore(
    (state) => state.openPlaylistSidebarFloating,
  );

  const [isMouseInside, setIsMouseInside] = useState(false);
  const [closeTimer, setCloseTimer] = useState<NodeJS.Timeout | null>(null);
  const hoverExpandTimerRef = useRef<NodeJS.Timeout | null>(null);

  // Transition states
  const [isClosingToMinimized, setIsClosingToMinimized] = useState(false);
  const [isClosingFromLocked, setIsClosingFromLocked] = useState(false);
  const [isPinning, setIsPinning] = useState(false);

  // 用 ref 追踪上一个状态，不触发 useEffect cleanup
  const wasFloatingRef = useRef(isOpen && !isPinned);
  const wasLockedRef = useRef(isOpen && isPinned);

  // 单一 effect 处理所有过渡，只用 [isOpen, isPinned] 作为依赖
  // ⚠️ ref 必须在 if 判断之前更新，否则 early return 会导致 ref 停留在 stale 值
  useEffect(() => {
    const wasFloating = wasFloatingRef.current;
    const wasLocked = wasLockedRef.current;

    // 先更新 ref，再做判断
    wasFloatingRef.current = isOpen && !isPinned;
    wasLockedRef.current = isOpen && isPinned;

    // Floating -> Locked
    if (wasFloating && isOpen && isPinned) {
      setIsPinning(true);
      const timer = setTimeout(() => setIsPinning(false), 300);
      return () => clearTimeout(timer);
    }

    // Locked -> Minimized
    if (wasLocked && !isOpen) {
      setIsClosingFromLocked(true);
      const timer = setTimeout(() => setIsClosingFromLocked(false), 300);
      return () => clearTimeout(timer);
    }
  }, [isOpen, isPinned]); // eslint-disable-line react-hooks/exhaustive-deps

  const closeFloatingToMinimized = useCallback(() => {
    setIsClosingToMinimized(true);
    setTimeout(() => {
      togglePlaylistSidebar();
      setIsClosingToMinimized(false);
    }, 300);
  }, [togglePlaylistSidebar]);

  useEffect(() => {
    if (isOpen && !isPinned) {
      if (!isMouseInside) {
        const timer = setTimeout(() => closeFloatingToMinimized(), 500);
        setCloseTimer(timer);
        return () => clearTimeout(timer);
      }
    }
  }, [isOpen, isPinned, isMouseInside, closeFloatingToMinimized]);

  useEffect(() => {
    if (isMouseInside && closeTimer) {
      clearTimeout(closeTimer);
      setCloseTimer(null);
    }
  }, [isMouseInside, closeTimer]);

  const handleMouseEnter = useCallback(() => setIsMouseInside(true), []);
  const handleMouseLeave = useCallback(() => setIsMouseInside(false), []);

  const handleHoverExpand = useCallback(() => {
    if (!isOpen) {
      openPlaylistSidebarFloating();
      setIsMouseInside(true);
    }
  }, [isOpen, openPlaylistSidebarFloating]);

  const handleIconColumnMouseEnter = useCallback(() => {
    if (!isOpen) {
      hoverExpandTimerRef.current = setTimeout(handleHoverExpand, 300);
    }
  }, [isOpen, handleHoverExpand]);

  const handleIconColumnMouseLeave = useCallback(() => {
    if (hoverExpandTimerRef.current) {
      clearTimeout(hoverExpandTimerRef.current);
      hoverExpandTimerRef.current = null;
    }
  }, []);

  const handleTogglePin = useCallback(() => {
    if (isPinned) {
      setIsMouseInside(true);
    }
    togglePlaylistSidebarPin();
  }, [isPinned, togglePlaylistSidebarPin]);

  if (!isHydrated) {
    return (
      <div className="w-12 h-full bg-sidebar border-r border-border/30 flex">
        <div className="w-12 shrink-0 flex flex-col items-center py-4 gap-2">
          <Skeleton className="w-9 h-9 rounded-md" />
          <Skeleton className="w-9 h-9 rounded-md" />
          <Skeleton className="w-9 h-9 rounded-md" />
        </div>
      </div>
    );
  }

  const isFloating = isOpen && !isPinned;
  const isLocked = isOpen && isPinned;

  return (
    <>
      {/* 图标列 - 始终 48px，三种模式下都可见 */}
      <div
        className="w-12 h-full bg-sidebar border-r border-border/30 shrink-0 flex flex-col"
        onMouseEnter={handleIconColumnMouseEnter}
        onMouseLeave={handleIconColumnMouseLeave}
      >
        <IconColumn />
      </div>

      {/* 锁定面板 - in-flow 定位，会推开壁纸内容区域 */}
      {(isLocked || isPinning || isClosingFromLocked) && (
        <LockedPanel
          isClosingFromLocked={isClosingFromLocked}
          onTogglePin={handleTogglePin}
        />
      )}

      {/* 悬浮面板 - absolute 定位，浮在内容上方 */}
      {(isFloating || isPinning) && (
        <FloatingPanel
          isClosingToMinimized={isClosingToMinimized}
          isPinning={isPinning}
          isFloating={isFloating}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          onTogglePin={handleTogglePin}
        />
      )}

      {/* 悬浮模式背景遮罩 */}
      {isFloating && (
        <div
          className={cn(
            "absolute left-12 top-0 bottom-0 right-0 z-20 bg-black/5",
            "transition-opacity duration-300",
            isClosingToMinimized ? "opacity-0" : "opacity-100",
          )}
          onClick={closeFloatingToMinimized}
        />
      )}
    </>
  );
}
