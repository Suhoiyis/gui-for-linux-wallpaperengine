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
import { Checkbox } from "@/components/ui/checkbox";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Thumbnail } from "@/components/common/Thumbnail";
import { useAppStore } from "@/store/appStore";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

interface NicknameManagerDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

interface NicknameRow {
  wallpaperId: string;
  title: string;
  nickname: string;
  selected: boolean;
}

export function NicknameManagerDialog({ open, onOpenChange }: NicknameManagerDialogProps) {
  const nicknames = useAppStore((state) => state.nicknames);
  const wallpapers = useAppStore((state) => state.wallpapers);
  const setNickname = useAppStore((state) => state.setNickname);

  const [rows, setRows] = useState<NicknameRow[]>([]);

  // Load nicknames sorted alphabetically when dialog opens
  useEffect(() => {
    if (open) {
      const sortedNicknames = Object.entries(nicknames)
        .sort((a, b) => a[1].toLowerCase().localeCompare(b[1].toLowerCase()))
        .map(([wallpaperId, nickname]) => {
          const wp = wallpapers.find((w) => w.id === wallpaperId);
          return {
            wallpaperId,
            title: wp?.title || `ID: ${wallpaperId}`,
            nickname,
            selected: false,
          };
        });
      setRows(sortedNicknames);
    }
  }, [open, nicknames, wallpapers]);

  const handleSelectAll = () => {
    setRows((prev) => prev.map((row) => ({ ...row, selected: true })));
  };

  const handleDeselectAll = () => {
    setRows((prev) => prev.map((row) => ({ ...row, selected: false })));
  };

  const handleDeleteSelected = () => {
    setRows((prev) =>
      prev.map((row) => (row.selected ? { ...row, nickname: "" } : row))
    );
  };

  const handleToggleSelected = (wallpaperId: string) => {
    setRows((prev) =>
      prev.map((row) =>
        row.wallpaperId === wallpaperId ? { ...row, selected: !row.selected } : row
      )
    );
  };

  const handleNicknameChange = (wallpaperId: string, newNickname: string) => {
    setRows((prev) =>
      prev.map((row) =>
        row.wallpaperId === wallpaperId ? { ...row, nickname: newNickname } : row
      )
    );
  };

  const handleSave = async () => {
    try {
      // Update all nicknames
      for (const row of rows) {
        await setNickname(row.wallpaperId, row.nickname);
      }
      toast.success("Nicknames saved");
      onOpenChange(false);
    } catch (error) {
      console.error("Failed to save nicknames:", error);
      toast.error("Failed to save nicknames");
    }
  };

  const selectedCount = useMemo(() => rows.filter((r) => r.selected).length, [rows]);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px] max-h-[80vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>Nickname Manager</DialogTitle>
          <DialogDescription>
            Manage custom names for your wallpapers.
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
            onClick={handleDeleteSelected}
            disabled={selectedCount === 0}
          >
            Delete Selected {selectedCount > 0 && `(${selectedCount})`}
          </Button>
        </div>

        {/* List */}
        <ScrollArea className="flex-1 min-h-0">
          {rows.length === 0 ? (
            <div className="flex items-center justify-center py-8 text-muted-foreground">
              No nicknames set.
            </div>
          ) : (
            <div className="space-y-2 pr-4">
              {rows.map((row) => (
                <div
                  key={row.wallpaperId}
                  className={cn(
                    "flex items-center gap-3 p-3 rounded-lg border bg-card/50 overflow-hidden",
                    row.selected && "border-brand/50 bg-brand/5"
                  )}
                >
                  {/* Checkbox */}
                  <Checkbox
                    checked={row.selected}
                    onCheckedChange={() => handleToggleSelected(row.wallpaperId)}
                  />

                  {/* Thumbnail */}
                  <Thumbnail wallpaperId={row.wallpaperId} className="w-12 h-12 shrink-0" />

                  {/* Title & Input */}
                  <div className="flex-1 min-w-0 w-0">
                    <p className="text-xs text-muted-foreground truncate mb-1">
                      {row.title}
                    </p>
                    <Input
                      value={row.nickname}
                      onChange={(e) => handleNicknameChange(row.wallpaperId, e.target.value)}
                      placeholder="Nickname"
                      className="h-8"
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button onClick={handleSave}>Save Changes</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}