import { useState, useEffect, memo, useMemo } from "react";
import { invoke } from "@tauri-apps/api/core";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from "@/components/common/Empty";
import { Thumbnail } from "@/components/common/Thumbnail";
import { useAppStore } from "@/store/appStore";
import { toast } from "sonner";
import { History, Play, Trash2, Clock, Hash, CircleQuestionMark } from "lucide-react";
import { HistoryEntry } from "@/types";
import { getDisplayName, cn } from "@/lib/utils";

interface HistoryDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const HistoryRow = memo(({ entry, onReuse }: { entry: HistoryEntry; onReuse: (id: string) => void }) => {
  const nicknames = useAppStore((state) => state.nicknames);
  const wallpapers = useAppStore((state) => state.wallpapers);

  const wallpaper = useMemo(() => {
    return wallpapers.find((w) => w.id === entry.id);
  }, [wallpapers, entry.id]);
  
  // Get display name with nickname support
  const title = wallpaper?.title || entry.title || "Unknown Wallpaper";
  const { displayName, originalTitle } = getDisplayName(nicknames, entry.id, title);
  const isNickname = originalTitle !== null;

  const formattedTime = useMemo(() => {
    try {
      const date = new Date(entry.timestamp);
      return date.toLocaleString();
    } catch {
      return entry.timestamp;
    }
  }, [entry.timestamp]);

  return (
    <div className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors group">
      <div className="flex items-center gap-4 flex-1 min-w-0">
        <Thumbnail wallpaperId={entry.id} className="w-12 h-12 shrink-0" />
        <div className="flex-1 min-w-0">
          <div 
            className={cn(
              "font-medium truncate text-foreground",
              isNickname && "nickname-text"
            )}
            title={isNickname ? `Original: ${originalTitle}` : undefined}
          >
            {displayName}
          </div>
          <div className="flex items-center gap-3 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <Hash className="w-3 h-3" />
              {entry.id}
            </span>
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {formattedTime}
            </span>
          </div>
        </div>
      </div>

      <Button
        variant="ghost"
        size="sm"
        className="opacity-0 group-hover:opacity-100 transition-opacity shrink-0"
        onClick={() => onReuse(entry.id)}
      >
        <Play className="w-4 h-4 mr-1" />
        Reuse
      </Button>
    </div>
  );
});

HistoryRow.displayName = "HistoryRow";

export function HistoryDialog({ open, onOpenChange }: HistoryDialogProps) {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const applyWallpaper = useAppStore((state) => state.applyWallpaper);
  const setSelectedId = useAppStore((state) => state.setSelectedId);
  const selectedScreen = useAppStore((state) => state.selectedScreen);

  useEffect(() => {
    if (open) {
      loadHistory();
    }
  }, [open]);

  const loadHistory = async () => {
    setIsLoading(true);
    try {
      const result = await invoke<HistoryEntry[]>("get_history");
      setHistory(result);
    } catch (error) {
      console.error("Failed to load history:", error);
      toast.error("Failed to load history");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReuse = async (id: string) => {
    const screen = selectedScreen === "all" ? undefined : selectedScreen;
    await applyWallpaper(id, screen);
    setSelectedId(id);
    onOpenChange(false);
    toast.success("Wallpaper applied");
  };

  const handleClear = async () => {
    try {
      await invoke("clear_history");
      setHistory([]);
      toast.success("History cleared");
    } catch (error) {
      console.error("Failed to clear history:", error);
      toast.error("Failed to clear history");
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <History className="w-5 h-5" />
            Play History
          </DialogTitle>
          <DialogDescription>
            Recently played wallpapers. Click Reuse to apply again.
          </DialogDescription>
        </DialogHeader>

        <div className="rounded-xl border bg-card/50 overflow-hidden max-h-[400px] overflow-y-auto">
          {isLoading ? (
            <div className="flex items-center justify-center py-8 text-muted-foreground">
              Loading...
            </div>
          ) : history.length === 0 ? (
            <Empty>
              <EmptyHeader>
                <EmptyMedia variant="icon">
                  <CircleQuestionMark />
                </EmptyMedia>
                <EmptyTitle>No Playback History</EmptyTitle>
                <EmptyDescription>
                  You haven't played any wallpapers yet.
                </EmptyDescription>
              </EmptyHeader>
            </Empty>
          ) : (
            <div className="divide-y">
              {history.map((entry) => (
                <HistoryRow
                  key={entry.id + "-" + entry.timestamp}
                  entry={entry}
                  onReuse={handleReuse}
                />
              ))}
            </div>
          )}
        </div>

        <DialogFooter>
          <Button
            variant="outline"
            size="sm"
            onClick={handleClear}
            disabled={history.length === 0}
          >
            <Trash2 className="w-4 h-4 mr-2" />
            Clear History
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}