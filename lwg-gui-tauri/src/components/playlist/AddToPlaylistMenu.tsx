import { useState } from "react";
import { Plus, ListMusic } from "lucide-react";
import { useAppStore } from "@/store/appStore";
import {
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import { CreatePlaylistDialog } from "./CreatePlaylistDialog";

interface AddToPlaylistMenuProps {
  wallpaperId: string;
  children: React.ReactNode;
}

export function AddToPlaylistMenu({
  wallpaperId,
  children,
}: AddToPlaylistMenuProps) {
  const playlists = useAppStore((state) => state.playlists);
  const addToPlaylist = useAppStore((state) => state.addToPlaylist);

  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  const handleAddToPlaylist = async (playlistId: string) => {
    await addToPlaylist(playlistId, [wallpaperId]);
  };

  return (
    <>
      <DropdownMenuSub>
        <DropdownMenuSubTrigger>{children}</DropdownMenuSubTrigger>
        <DropdownMenuSubContent className="w-48">
          {playlists.length > 0 ? (
            <>
              {playlists.map((playlist) => (
                <DropdownMenuItem
                  key={playlist.id}
                  onClick={() => handleAddToPlaylist(playlist.id)}
                >
                  <ListMusic className="w-4 h-4 mr-2" />
                  <span className="truncate">{playlist.name}</span>
                </DropdownMenuItem>
              ))}
              <DropdownMenuSeparator />
            </>
          ) : null}
          <DropdownMenuItem onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Create new playlist...
          </DropdownMenuItem>
        </DropdownMenuSubContent>
      </DropdownMenuSub>

      <CreatePlaylistDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
        initialWallpaperIds={[wallpaperId]}
      />
    </>
  );
}