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
import { useAppStore } from "@/store/appStore";
import { AlertTriangle } from "lucide-react";

interface DeletePlaylistDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  playlistId: string;
  playlistName: string;
}

export function DeletePlaylistDialog({
  open,
  onOpenChange,
  playlistId,
  playlistName,
}: DeletePlaylistDialogProps) {
  const deletePlaylist = useAppStore((state) => state.deletePlaylist);

  const handleDelete = async () => {
    try {
      await deletePlaylist(playlistId);
      onOpenChange(false);
    } catch (error) {
      // Error handling is done in the store
    }
  };

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <div className="flex flex-col items-center gap-2 sm:flex-row sm:gap-4">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10 dark:bg-red-900/20">
              <AlertTriangle className="h-6 w-6 text-red-600 dark:text-red-400" />
            </div>
            <div className="space-y-1 text-center sm:text-left">
              <AlertDialogTitle>Delete playlist?</AlertDialogTitle>
              <AlertDialogDescription>
                This will permanently delete{" "}
                <span className="font-bold text-foreground">
                  "{playlistName}"
                </span>{" "}
                and cannot be undone. The wallpapers themselves will not be
                deleted.
              </AlertDialogDescription>
            </div>
          </div>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={handleDelete}
            className="bg-red-600 hover:bg-red-700 text-white focus:ring-red-600"
          >
            Delete Playlist
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}