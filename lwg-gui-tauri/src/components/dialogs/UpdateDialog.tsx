import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Download, ExternalLink } from "lucide-react";
import { openUrl } from "@tauri-apps/plugin-opener";
import { isTauriEnv } from "@/lib/utils";

interface UpdateDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  currentVersion: string;
  latestVersion: string;
  downloadUrl: string;
}

export function UpdateDialog({
  open,
  onOpenChange,
  currentVersion,
  latestVersion,
  downloadUrl,
}: UpdateDialogProps) {
  const handleOpenUrl = async () => {
    try {
      if (isTauriEnv()) {
        await openUrl(downloadUrl);
      } else {
        window.open(downloadUrl, "_blank");
      }
    } catch (error) {
      console.error("Failed to open URL:", error);
      // Fallback to window.open
      window.open(downloadUrl, "_blank");
    }
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Download className="h-5 w-5 text-primary" />
            发现新版本
          </DialogTitle>
          <DialogDescription>
            有新版本可供下载
          </DialogDescription>
        </DialogHeader>

        <div className="py-4 space-y-3">
          <div className="flex justify-between items-center p-3 bg-muted/50 rounded-lg">
            <div>
              <p className="text-sm text-muted-foreground">当前版本</p>
              <p className="font-mono font-medium">v{currentVersion}</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-muted-foreground">最新版本</p>
              <p className="font-mono font-medium text-primary">{latestVersion}</p>
            </div>
          </div>

          <p className="text-sm text-muted-foreground">
            建议更新到最新版本以获得更好的体验和 bug 修复。
          </p>
        </div>

        <DialogFooter className="gap-2 sm:gap-0">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            稍后提醒
          </Button>
          <Button onClick={handleOpenUrl}>
            <ExternalLink className="h-4 w-4 mr-2" />
            前往下载
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}