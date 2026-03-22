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

interface RenamePlaylistDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  playlistId: string;
  currentName: string;
}

export function RenamePlaylistDialog({
  open,
  onOpenChange,
  playlistId,
  currentName,
}: RenamePlaylistDialogProps) {
  const renamePlaylist = useAppStore((state) => state.renamePlaylist);
  const playlists = useAppStore((state) => state.playlists);

  const [name, setName] = useState(currentName);
  const [isLoading, setIsLoading] = useState(false);

  const MAX_NAME_LENGTH = 15;

  useEffect(() => {
    if (open) {
      setName(currentName);
    }
  }, [open, currentName]);

  const isDuplicateName = useMemo(() => {
    const trimmedName = name.trim().toLowerCase();
    if (trimmedName === currentName.toLowerCase()) return false;
    return playlists.some(p => p.name.toLowerCase() === trimmedName);
  }, [name, playlists, currentName]);

  const handleRename = async () => {
    if (!name.trim() || name === currentName || isDuplicateName) {
      return;
    }

    setIsLoading(true);
    try {
      await renamePlaylist(playlistId, name.trim());
      onOpenChange(false);
    } catch (error) {
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Rename Playlist</DialogTitle>
          <DialogDescription>
            Enter a new name for this playlist.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="playlist-rename">Name</Label>
            <Input
              id="playlist-rename"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Playlist name"
              maxLength={MAX_NAME_LENGTH}
              onKeyDown={(e) => {
                if (e.key === "Enter" && name.trim() && !isDuplicateName) {
                  handleRename();
                }
              }}
            />
            <div className="flex justify-between items-center">
              {isDuplicateName ? (
                <p className="text-xs text-amber-500">A playlist with this name already exists</p>
              ) : (
                <span />
              )}
              <p className="text-xs text-muted-foreground shrink-0">
                {name.length}/{MAX_NAME_LENGTH}
              </p>
            </div>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button onClick={handleRename} disabled={!name.trim() || isLoading || isDuplicateName || name === currentName}>
            {isLoading ? "Saving..." : "Rename"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}