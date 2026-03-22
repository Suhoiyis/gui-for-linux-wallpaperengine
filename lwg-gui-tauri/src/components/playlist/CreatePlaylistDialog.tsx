import { useState, useEffect, useMemo } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAppStore } from "@/store/appStore";

interface CreatePlaylistDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  initialWallpaperIds?: string[];
}

// Helper function to generate next available playlist name
function getNextPlaylistName(playlists: { name: string }[]): string {
  // Find all existing "Playlist X" names
  const existingNumbers = new Set<number>();
  let hasDefaultName = false;
  
  for (const p of playlists) {
    const match = p.name.match(/^Playlist\s*(\d+)$/i);
    if (match) {
      existingNumbers.add(parseInt(match[1], 10));
    }
    if (p.name.toLowerCase() === "playlist") {
      hasDefaultName = true;
    }
  }
  
  // Find the smallest unused number starting from 1
  let num = 1;
  if (!hasDefaultName && !existingNumbers.has(1)) {
    // If "Playlist 1" doesn't exist, use "Playlist 1"
    // But also check if any playlist is named exactly "Playlist"
    const hasExactPlaylist = playlists.some(p => p.name === "Playlist");
    if (!hasExactPlaylist) {
      return "Playlist 1";
    }
  }
  
  while (existingNumbers.has(num)) {
    num++;
  }
  
  return `Playlist ${num}`;
}

export function CreatePlaylistDialog({
  open,
  onOpenChange,
  initialWallpaperIds = [],
}: CreatePlaylistDialogProps) {
  const createPlaylist = useAppStore((state) => state.createPlaylist);
  const playlists = useAppStore((state) => state.playlists);

  const [name, setName] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const MAX_NAME_LENGTH = 15;

  // Generate default name when dialog opens
  const defaultName = useMemo(() => getNextPlaylistName(playlists), [playlists]);

  // Reset name when dialog opens
  useEffect(() => {
    if (open) {
      setName(defaultName);
      setError(null);
    }
  }, [open, defaultName]);

  // Check for duplicate name
  const isDuplicateName = useMemo(() => {
    const trimmedName = name.trim().toLowerCase();
    return playlists.some(p => p.name.toLowerCase() === trimmedName);
  }, [name, playlists]);

  const handleCreate = async () => {
    const trimmedName = name.trim();
    if (!trimmedName) return;

    // Check for duplicate
    if (isDuplicateName) {
      setError("A playlist with this name already exists");
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      await createPlaylist(trimmedName, initialWallpaperIds);
      onOpenChange(false);
    } catch (error) {
      // Error handling is done in the store
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create New Playlist</DialogTitle>
          <DialogDescription>
            Give your playlist a name. You can add wallpapers to it later.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="playlist-name">Name</Label>
            <Input
              id="playlist-name"
              value={name}
              onChange={(e) => {
                setName(e.target.value);
                setError(null);
              }}
              placeholder="My Playlist"
              maxLength={MAX_NAME_LENGTH}
              className={error ? "border-red-500 focus-visible:ring-red-500" : ""}
              onKeyDown={(e) => {
                if (e.key === "Enter" && name.trim() && !isDuplicateName) {
                  handleCreate();
                }
              }}
            />
            <div className="flex justify-between items-center">
              {error ? (
                <p className="text-xs text-red-500">{error}</p>
              ) : isDuplicateName ? (
                <p className="text-xs text-amber-500">A playlist with this name already exists</p>
              ) : (
                <span />
              )}
              <p className="text-xs text-muted-foreground shrink-0">
                {name.length}/{MAX_NAME_LENGTH}
              </p>
            </div>
            <p className="text-xs text-muted-foreground">
              {initialWallpaperIds.length > 0 && (
                <span>
                  {initialWallpaperIds.length} wallpaper(s) will be added to this
                  playlist.
                </span>
              )}
            </p>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleCreate} 
            disabled={!name.trim() || isLoading || isDuplicateName}
          >
            {isLoading ? "Creating..." : "Create"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}