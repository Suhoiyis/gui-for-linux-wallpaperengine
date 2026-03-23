import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Github } from "lucide-react";
import { useAppStore } from "@/store/appStore";

interface AboutDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function AboutDialog({ open, onOpenChange }: AboutDialogProps) {
  const appVersion = useAppStore((state) => state.appVersion);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px] flex flex-col items-center text-center">
        {/* 1. Logo 区域：彻底去除内边距，让图片成为视觉主体 */}
        <div className="flex items-center justify-center mb-6">
          <div
            // ✨ 移除 p-3 (内边距) 和 bg-primary/5 (背景色)
            // 加上 shadow-xl 让你的圆角图标看起来更有立体感，像浮在纸面上
            className="h-24 w-24 rounded-[22%] overflow-hidden shadow-xl border border-border/40"
          >
            <img
              src="/GUI_rounded.png"
              alt="LWG GUI Logo"
              // ✨ 关键：使用 object-cover 确保图片填满每一寸空间
              className="w-full h-full object-cover"
            />
          </div>
        </div>

        <DialogHeader className="flex flex-col items-center">
          <DialogTitle className="text-2xl font-bold">
            LINUX WALLPAPER ENGINE GUI
          </DialogTitle>
          <DialogDescription className="text-sm">v{appVersion}</DialogDescription>
        </DialogHeader>

        {/* 2. 描述文本 */}
        <div className="py-4 text-sm text-muted-foreground">
          <p>
            A modern, high-performance wallpaper manager for{" "}
            <a
              href="https://github.com/Almamu/linux-wallpaperengine"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline"
            >
              Almamu/linux-wallpaperengine
            </a>{" "}
            built with Tauri, React, and Rust.
            <br />
            Designed for simplicity and efficiency.
          </p>
        </div>

        {/* 3. 链接按钮组 */}
        <div className="flex gap-2 justify-center w-full">
          <Button
            variant="outline"
            size="sm"
            className="gap-2"
            onClick={() =>
              window.open(
                "https://github.com/Suhoiyis/gui-for-linux-wallpaperengine",
                "_blank",
              )
            }
          >
            <Github className="h-4 w-4" /> GitHub
          </Button>
          {/* <Button
            variant="outline"
            size="sm"
            className="gap-2"
            onClick={() => window.open("https://tauri.app", "_blank")}
          >
            <Globe className="h-4 w-4" /> Website
          </Button> */}
        </div>

        {/* 4. 底部版权信息 */}
        <div className="mt-4 text-[10px] text-muted-foreground">
          <p>© 2026 Suhoiyis.</p>
          <p>Licensed under GPL-3.0 License.</p>
        </div>
      </DialogContent>
    </Dialog>
  );
}
