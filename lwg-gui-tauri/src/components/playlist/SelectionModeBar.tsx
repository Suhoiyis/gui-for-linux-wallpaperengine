import { X, Check, CheckCheck, Plus, Trash2, ListPlus, Star } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAppStore } from "@/store/appStore";
import { useState, useMemo } from "react";
import { CreatePlaylistDialog } from "./CreatePlaylistDialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import { toast } from "sonner";
import { FAVORITES_PLAYLIST_ID } from "@/lib/constants";
import { cn } from "@/lib/utils";

export function SelectionModeBar() {
  const selectedForPlaylist = useAppStore((state) => state.selectedForPlaylist);
  const exitSelectionMode = useAppStore((state) => state.exitSelectionMode);
  const selectAllForPlaylist = useAppStore((state) => state.selectAllForPlaylist);
  const deselectAllForPlaylist = useAppStore((state) => state.deselectAllForPlaylist);
  
  // 播放列表相关状态
  const playlists = useAppStore((state) => state.playlists);
  const activePlaylistId = useAppStore((state) => state.activePlaylistId);
  const favoriteIds = useAppStore((state) => state.favoriteIds);
  const addToPlaylist = useAppStore((state) => state.addToPlaylist);
  const removeFromPlaylist = useAppStore((state) => state.removeFromPlaylist);
  const addToFavorites = useAppStore((state) => state.addToFavorites);
  const removeFromFavorites = useAppStore((state) => state.removeFromFavorites);

  // 获取当前播放列表名称（包括 Favorites）
  const activePlaylistName = activePlaylistId === FAVORITES_PLAYLIST_ID
    ? "Favorites"
    : playlists.find((p) => p.id === activePlaylistId)?.name;

  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  const selectedCount = selectedForPlaylist.size;
  const selectedIds = Array.from(selectedForPlaylist);

  // 计算已收藏的数量
  const favoritesAlreadyCount = useMemo(() => {
    return selectedIds.filter(id => favoriteIds.has(id)).length;
  }, [selectedIds, favoriteIds]);
  const allInFavorites = favoritesAlreadyCount === selectedCount;

  // 计算每个播放列表中已加入的数量
  const getPlaylistAlreadyCount = (playlistId: string) => {
    const playlist = playlists.find(p => p.id === playlistId);
    if (!playlist) return 0;
    return selectedIds.filter(id => playlist.wallpaperIds.includes(id)).length;
  };

  // 从当前播放列表移除（支持 Favorites）
  const handleRemoveFromPlaylist = async () => {
    if (!activePlaylistId || selectedCount === 0) return;
    
    try {
      if (activePlaylistId === FAVORITES_PLAYLIST_ID) {
        // 从 Favorites 移除 = 使用幂等的 removeFromFavorites
        for (const wallpaperId of selectedIds) {
          await removeFromFavorites(wallpaperId);
        }
        toast.success(`Removed ${selectedCount} wallpaper(s) from Favorites`);
      } else {
        // 从普通播放列表移除
        for (const wallpaperId of selectedIds) {
          await removeFromPlaylist(activePlaylistId, wallpaperId);
        }
        toast.success(`Removed ${selectedCount} wallpaper(s) from playlist`);
      }
      exitSelectionMode();
    } catch (error) {
      // 错误已在 store 中处理
    }
  };

  return (
    <div className="flex items-center gap-2 px-4 py-2 bg-accent/50 border-b animate-in fade-in slide-in-from-top-2 duration-300">
      <Badge variant="secondary" className="font-normal">
        {selectedCount} selected
      </Badge>

      <div className="flex-1" />

      <Button
        variant="outline"
        size="sm"
        onClick={selectAllForPlaylist}
        className="gap-1"
      >
        <CheckCheck className="w-4 h-4" />
        Select All
      </Button>

      <Button
        variant="outline"
        size="sm"
        onClick={deselectAllForPlaylist}
        className="gap-1"
      >
        <Check className="w-4 h-4" />
        Deselect
      </Button>

      {/* Add to Playlist 下拉菜单 */}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="outline"
            size="sm"
            disabled={selectedCount === 0}
            className="gap-1"
          >
            <ListPlus className="w-4 h-4" />
            Add to Playlist
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-48">
          {/* Favorites 选项 */}
          {(() => {
            return (
              <DropdownMenuItem
                disabled={allInFavorites}
                onClick={async () => {
                  // 只添加未收藏的
                  const toAdd = selectedIds.filter(id => !favoriteIds.has(id));
                  for (const id of toAdd) {
                    await addToFavorites(id);
                  }
                  if (toAdd.length > 0) {
                    toast.success(`Added ${toAdd.length} wallpaper(s) to Favorites`);
                  }
                  exitSelectionMode();
                }}
              >
                <Star className={cn(
                  "mr-2 h-4 w-4",
                  allInFavorites && "fill-yellow-400 text-yellow-400"
                )} />
                <span className={allInFavorites ? "text-muted-foreground" : ""}>Favorites</span>
                {/* 只在部分已收藏时显示 Badge，全部已收藏时只显示 Check */}
                {!allInFavorites && favoritesAlreadyCount > 0 && (
                  <Badge variant="secondary" className="ml-auto text-[10px] px-1">
                    {favoritesAlreadyCount}/{selectedCount}
                  </Badge>
                )}
                {allInFavorites && (
                  <Check className="ml-auto h-4 w-4 text-muted-foreground" />
                )}
              </DropdownMenuItem>
            );
          })()}
          
          {playlists.length > 0 && <DropdownMenuSeparator />}
          
          {playlists.map((playlist) => {
            const alreadyCount = getPlaylistAlreadyCount(playlist.id);
            const allInThisPlaylist = alreadyCount === selectedCount;
            
            return (
              <DropdownMenuItem
                key={playlist.id}
                disabled={allInThisPlaylist}
                onClick={async () => {
                  // 只添加未加入的
                  const toAdd = selectedIds.filter(id => !playlist.wallpaperIds.includes(id));
                  if (toAdd.length > 0) {
                    await addToPlaylist(playlist.id, toAdd);
                  }
                  exitSelectionMode();
                }}
              >
                <span className={allInThisPlaylist ? "text-muted-foreground" : ""}>
                  {playlist.name}
                </span>
                {/* 只在部分已加入时显示 X/Y badge，全部已加入时只显示 Check */}
                {!allInThisPlaylist && alreadyCount > 0 && (
                  <Badge variant="secondary" className="ml-auto text-[10px] px-1">
                    {alreadyCount}/{selectedCount}
                  </Badge>
                )}
                {!allInThisPlaylist && alreadyCount === 0 && (
                  <Badge variant="secondary" className="ml-auto text-[10px] px-1">
                    {playlist.wallpaperIds.length}
                  </Badge>
                )}
                {allInThisPlaylist && (
                  <Check className="ml-auto h-4 w-4 text-muted-foreground" />
                )}
              </DropdownMenuItem>
            );
          })}
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Remove from Playlist - 仅当 activePlaylistId 存在时显示 */}
      {activePlaylistId && (
        <Button
          variant="outline"
          size="sm"
          onClick={handleRemoveFromPlaylist}
          disabled={selectedCount === 0}
          className="gap-1 text-red-600 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-950"
        >
          <Trash2 className="w-4 h-4" />
          Remove from "{activePlaylistName}"
        </Button>
      )}

      <Button
        size="sm"
        onClick={() => setIsCreateDialogOpen(true)}
        disabled={selectedCount === 0}
        className="gap-1 bg-brand text-brand-foreground hover:bg-brand/90"
      >
        <Plus className="w-4 h-4" />
        Create Playlist
      </Button>

      <Button
        variant="ghost"
        size="sm"
        onClick={exitSelectionMode}
        className="gap-1"
      >
        <X className="w-4 h-4" />
        Cancel
      </Button>

      <CreatePlaylistDialog
        open={isCreateDialogOpen}
        onOpenChange={(open) => {
          setIsCreateDialogOpen(open);
          if (!open) {
            exitSelectionMode();
          }
        }}
        initialWallpaperIds={selectedIds}
      />
    </div>
  );
}