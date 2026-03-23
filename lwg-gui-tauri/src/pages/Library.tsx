// src/pages/Library.tsx
import { useMemo, useCallback, useState, useRef, useEffect } from "react";
import { AlertTriangle } from "lucide-react";
import { toast } from "sonner";

// Layout & UI Components
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  EmptyState,
  PlaylistEmptyState,
  SearchEmptyState,
  FavoritesEmptyState,
} from "@/components/common/Empty";
import { FAVORITES_PLAYLIST_ID } from "@/lib/constants";
import { TooltipProvider } from "@/components/ui/tooltip";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

// Custom Components
import { LibraryHeader } from "@/components/library/LibraryHeader";
import { WallpaperSidebar } from "@/components/library/WallpaperSidebar";
import { WallpaperGrid } from "@/components/library/WallpaperGrid";
import { LibraryPagination } from "@/components/library/LibraryPagination";
import { PlaylistSidebar } from "@/components/playlist/PlaylistSidebar";
import { SelectionModeBar } from "@/components/playlist/SelectionModeBar";

// State & API
import { useAppStore } from "@/store/appStore";
import { openFolder } from "@/api/wallpaper";
import { useActiveWallpapers } from "@/hooks/useActiveWallpapers";

const ITEMS_PER_PAGE = 24;

export function Library() {
  // Store State
  const wallpapers = useAppStore((state) => state.wallpapers);
  const searchQuery = useAppStore((state) => state.searchQuery);
  const selectedId = useAppStore((state) => state.selectedId);
  const setSelectedId = useAppStore((state) => state.setSelectedId);
  const sortBy = useAppStore((state) => state.sortBy);
  const selectedScreen = useAppStore((state) => state.selectedScreen);
  const isSelectionMode = useAppStore((state) => state.isSelectionMode);
  const activePlaylistId = useAppStore((state) => state.activePlaylistId);
  const playlists = useAppStore((state) => state.playlists);
  // 订阅 favoriteIds 和 nicknames 以确保 memo 正确响应
  const favoriteIds = useAppStore((state) => state.favoriteIds);
  const nicknames = useAppStore((state) => state.nicknames);
  const activePlaylist = playlists.find((p) => p.id === activePlaylistId);
  const { activeWallpapers } = useActiveWallpapers();

  // Local State
  const [wallpaperToDelete, setWallpaperToDelete] = useState<{
    id: string;
    title: string;
    path: string;
  } | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const scrollTopRef = useRef<HTMLDivElement>(null);

  // --- Logic Layers ---

  const filteredWallpapers = useMemo(() => {
    return useAppStore.getState().getFilteredWallpapers();
  }, [
    wallpapers,
    searchQuery,
    sortBy,
    activePlaylistId,
    playlists,
    favoriteIds,
    nicknames,
  ]);

  useEffect(() => {
    setCurrentPage(1);
  }, [searchQuery, sortBy, activePlaylistId]);

  // Pagination
  const totalItems = filteredWallpapers.length;
  const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);

  const paginatedWallpapers = useMemo(() => {
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    return filteredWallpapers.slice(startIndex, startIndex + ITEMS_PER_PAGE);
  }, [filteredWallpapers, currentPage]);

  const handlePageChange = useCallback(
    (page: number) => {
      if (page < 1 || page > totalPages) return;
      setCurrentPage(page);
      setTimeout(() => {
        scrollTopRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 10);
    },
    [totalPages],
  );

  // Selection & Metadata
  // const selectedWallpaper = useMemo(() => {
  //   return filteredWallpapers.find((w) => w.id === selectedId) || null;
  // }, [filteredWallpapers, selectedId]);

  const currentIndex = useMemo(() => {
    if (!selectedId) return 0;
    const index = filteredWallpapers.findIndex((w) => w.id === selectedId);
    return index !== -1 ? index + 1 : 0;
  }, [filteredWallpapers, selectedId]);

  // Active wallpaper title
  const activeTitle = useMemo(() => {
    if (selectedScreen !== "all") {
      const wallpaperId = activeWallpapers.get(selectedScreen);
      if (!wallpaperId) return "None";
      const wallpaper = wallpapers.find((w) => w.id === wallpaperId);
      return wallpaper?.title || "None";
    }

    const allPlayingIds = Array.from(activeWallpapers.values());
    const uniqueIds = new Set(allPlayingIds);

    if (uniqueIds.size === 0) return "None";
    if (uniqueIds.size === 1) {
      const wallpaper = wallpapers.find((w) => w.id === allPlayingIds[0]);
      return wallpaper?.title || "None";
    }

    return `${uniqueIds.size} wallpapers playing`;
  }, [activeWallpapers, selectedScreen, wallpapers]);

  // Active wallpaper ID
  const activeWallpaperId = useMemo(() => {
    if (selectedScreen !== "all") {
      return activeWallpapers.get(selectedScreen) || null;
    }
    const allPlayingIds = Array.from(activeWallpapers.values());
    const uniqueIds = new Set(allPlayingIds);
    return uniqueIds.size === 1 ? allPlayingIds[0] : null;
  }, [activeWallpapers, selectedScreen]);

  // --- Event Handlers ---

  const handleSelect = useCallback(
    (id: string) => setSelectedId(id),
    [setSelectedId],
  );

  const handleApply = async (id: string, _title: string) => {
    const selectedScreen = useAppStore.getState().selectedScreen;
    const screen = selectedScreen === "all" ? undefined : selectedScreen;
    await useAppStore.getState().applyWallpaper(id, screen);
    setSelectedId(id);
  };

  const handleStop = async () => {
    await useAppStore.getState().stopWallpaper();
  };

  const handleOpenFolder = async (path: string) => {
    if (!path) {
      toast.error("Cannot open folder", {
        description: "Path is unknown",
      });
      return;
    }

    try {
      await openFolder(path);
    } catch (error) {
      toast.error("Failed to open folder", {
        description: String(error),
      });
    }
  };

  const handleDeleteRequest = (id: string, title: string, path: string) => {
    setWallpaperToDelete({ id, title, path });
  };

  const handleDeleteConfirm = async () => {
    if (!wallpaperToDelete) return;
    const { id, path } = wallpaperToDelete;
    await useAppStore.getState().removeWallpaper(id, path);
    setWallpaperToDelete(null);
  };

  return (
    <div className="h-full w-full overflow-hidden relative">
      <div className="flex h-full">
        {/* Playlist Sidebar - handles minimized/floating/locked states internally */}
        <PlaylistSidebar />

        {/* Main Content Area */}
        <div className="flex-1 h-full overflow-hidden">
          <ResizablePanelGroup
            orientation="horizontal"
            className="h-full w-full rounded-lg"
          >
            {/* Left Panel: Main Content */}
            <ResizablePanel defaultSize="75%" minSize="30%">
              <div className="flex flex-col h-full overflow-hidden">
                {/* Header */}
                <div className="px-6 pt-6 pb-4 shrink-0">
                  <LibraryHeader
                    currentTitle={activeTitle}
                    activeWallpaperId={activeWallpaperId}
                    onTitleClick={handleSelect}
                    totalCount={filteredWallpapers.length}
                    currentPage={currentPage}
                    totalPages={totalPages}
                    currentIndex={currentIndex}
                    onPageChange={handlePageChange}
                  />
                </div>

                {/* Selection Mode Bar */}
                {isSelectionMode && <SelectionModeBar />}

                {/* Content Area */}
                <TooltipProvider>
                  <ScrollArea className="flex-1 w-full h-full">
                    {filteredWallpapers.length === 0 ? (
                      <div className="flex h-full min-h-[50vh] items-center justify-center">
                        {searchQuery ? (
                          <SearchEmptyState query={searchQuery} />
                        ) : activePlaylistId === FAVORITES_PLAYLIST_ID ? (
                          <FavoritesEmptyState />
                        ) : activePlaylistId ? (
                          <PlaylistEmptyState
                            playlistName={activePlaylist?.name}
                          />
                        ) : (
                          <EmptyState />
                        )}
                      </div>
                    ) : (
                      <div className="px-6 pb-10">
                        <div ref={scrollTopRef} />

                        {/* Grid Component */}
                        <WallpaperGrid
                          wallpapers={paginatedWallpapers}
                          selectedId={selectedId}
                          onSelect={handleSelect}
                          onApply={handleApply}
                          onStop={handleStop}
                          onOpenFolder={handleOpenFolder}
                          onDelete={handleDeleteRequest}
                        />

                        {/* Pagination Component */}
                        <LibraryPagination
                          currentPage={currentPage}
                          totalPages={totalPages}
                          onPageChange={handlePageChange}
                        />
                      </div>
                    )}
                  </ScrollArea>
                </TooltipProvider>
              </div>
            </ResizablePanel>

            {/* Handle */}
            <ResizableHandle
              withHandle={false}
              className="relative w-2 bg-transparent z-10 -ml-1 cursor-col-resize group outline-none"
            >
              <div className="h-full w-[1px] bg-border/40 mx-auto group-hover:bg-border transition-colors duration-300" />
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-1 h-8 rounded-full bg-border opacity-0 group-hover:opacity-100 group-hover:bg-primary group-active:bg-primary/80 transition-all duration-300 ease-in-out shadow-sm" />
            </ResizableHandle>

            {/* Right Panel: Sidebar */}
            <ResizablePanel
              defaultSize="20%"
              minSize={300}
              maxSize={350}
              className="bg-muted/30 min-w-[300px] max-w-[450px]"
            >
              <WallpaperSidebar />
            </ResizablePanel>
          </ResizablePanelGroup>
        </div>
      </div>

      {/* Delete Dialog */}
      <AlertDialog
        open={!!wallpaperToDelete}
        onOpenChange={(open) => !open && setWallpaperToDelete(null)}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <div className="flex flex-col items-center gap-2 sm:flex-row sm:gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10 dark:bg-red-900/20">
                <AlertTriangle className="h-6 w-6 text-red-600 dark:text-red-400" />
              </div>
              <div className="space-y-1 text-center sm:text-left">
                <AlertDialogTitle>Delete this wallpaper?</AlertDialogTitle>
                <AlertDialogDescription>
                  This action cannot be undone. This will permanently delete
                  <span className="font-bold text-foreground">
                    {" "}
                    "{wallpaperToDelete?.title}"{" "}
                  </span>
                  and remove it from your disk.
                </AlertDialogDescription>
              </div>
            </div>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDeleteConfirm}
              className="bg-red-600 hover:bg-red-700 text-white focus:ring-red-600"
            >
              Delete Wallpaper
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
