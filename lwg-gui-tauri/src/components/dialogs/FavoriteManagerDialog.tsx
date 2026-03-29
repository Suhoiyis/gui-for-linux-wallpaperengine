import { useState, useEffect, useMemo } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Thumbnail } from "@/components/common/Thumbnail";
import { useAppStore } from "@/store/appStore";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { Star } from "lucide-react";

interface FavoriteManagerDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

interface FavoriteRow {
  wallpaperId: string;
  title: string;
  selected: boolean;
}

export function FavoriteManagerDialog({ open, onOpenChange }: FavoriteManagerDialogProps) {
  const favoriteIds = useAppStore((state) => state.favoriteIds);
  const wallpapers = useAppStore((state) => state.wallpapers);
  const toggleFavorite = useAppStore((state) => state.toggleFavorite);

  const [rows, setRows] = useState<FavoriteRow[]>([]);

  // Load favorites sorted alphabetically by title when dialog opens
  useEffect(() => {
    if (open) {
      const sortedFavorites = Array.from(favoriteIds)
        .map((wallpaperId) => {
          const wp = wallpapers.find((w) => w.id === wallpaperId);
          return {
            wallpaperId,
            title: wp?.title || `ID: ${wallpaperId}`,
            selected: false,
          };
        })
        .sort((a, b) => a.title.toLowerCase().localeCompare(b.title.toLowerCase()));
      setRows(sortedFavorites);
    }
  }, [open, favoriteIds, wallpapers]);

  const handleSelectAll = () => {
    setRows((prev) => prev.map((row) => ({ ...row, selected: true })));
  };

  const handleDeselectAll = () => {
    setRows((prev) => prev.map((row) => ({ ...row, selected: false })));
  };

  const handleRemoveSelected = async () => {
    const selectedRows = rows.filter((r) => r.selected);
    try {
      for (const row of selectedRows) {
        await toggleFavorite(row.wallpaperId);
      }
      toast.success(`Removed ${selectedRows.length} favorites`);
    } catch (error) {
      console.error("Failed to remove favorites:", error);
      toast.error("Failed to remove favorites");
    }
  };

  const handleToggleSelected = (wallpaperId: string) => {
    setRows((prev) =>
      prev.map((row) =>
        row.wallpaperId === wallpaperId ? { ...row, selected: !row.selected } : row
      )
    );
  };

  const selectedCount = useMemo(() => rows.filter((r) => r.selected).length, [rows]);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px] max-h-[80vh] flex flex-col">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Star className="w-4 h-4 text-yellow-500" /> Favorite Manager
          </DialogTitle>
          <DialogDescription>
            Manage your starred wallpapers. {rows.length} favorite{rows.length !== 1 ? "s" : ""}.
          </DialogDescription>
        </DialogHeader>

        {/* Toolbar */}
        <div className="flex items-center gap-2 py-2">
          <Button variant="ghost" size="sm" onClick={handleSelectAll}>
            Select All
          </Button>
          <Button variant="ghost" size="sm" onClick={handleDeselectAll}>
            Deselect All
          </Button>
          <div className="flex-1" />
          <Button
            variant="destructive"
            size="sm"
            onClick={handleRemoveSelected}
            disabled={selectedCount === 0}
          >
            Remove Selected {selectedCount > 0 && `(${selectedCount})`}
          </Button>
        </div>

        {/* List */}
        <ScrollArea className="flex-1 min-h-0">
          {rows.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-muted-foreground gap-2">
              <Star className="w-8 h-8 opacity-50" />
              <p>No favorites yet.</p>
              <p className="text-xs">Star wallpapers in the Library to add them here.</p>
            </div>
          ) : (
            <div className="space-y-2 pr-4">
              {rows.map((row) => (
                <div
                  key={row.wallpaperId}
                  className={cn(
                    "flex items-center gap-3 p-3 rounded-lg border bg-card/50 overflow-hidden",
                    row.selected && "border-yellow-500/50 bg-yellow-500/5"
                  )}
                >
                  {/* Checkbox */}
                  <Checkbox
                    checked={row.selected}
                    onCheckedChange={() => handleToggleSelected(row.wallpaperId)}
                  />

                  {/* Thumbnail */}
                  <Thumbnail wallpaperId={row.wallpaperId} className="w-12 h-12 shrink-0" />

                  {/* Title */}
                  <div className="flex-1 min-w-0 w-0">
                    <p className="text-sm font-medium text-foreground truncate">
                      {row.title}
                    </p>
                    <p className="text-xs text-muted-foreground truncate">
                      ID: {row.wallpaperId}
                    </p>
                  </div>

                  {/* Star indicator */}
                  <Star className="w-4 h-4 text-yellow-500 fill-yellow-500 shrink-0" />
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}