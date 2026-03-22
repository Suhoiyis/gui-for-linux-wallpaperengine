import {
  Search,
  Settings as SettingsIcon,
  Activity,
  Square,
  Shuffle,
  Camera,
  ImageIcon,
  Minimize2,
  AlertCircle,
  CheckCircle2,
  Clock,
  FolderOpen,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { isTauriEnv } from "@/lib/utils";
import { Button as StatefulButton } from "@/components/common/StatefulButton";
import { Separator } from "@/components/ui/separator";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
  TooltipProvider,
} from "@/components/ui/tooltip";
import { TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { useAppStore } from "@/store/appStore";
import {
  takeScreenshot,
  openFolder,
  openImage,
} from "@/api/wallpaper";
import { notify } from "@/api/system";
import { toast } from "sonner";
import { AppMenu } from "@/components/layout/AppMenu";
import { ScreenSelector } from "@/components/layout/ScreenSelector";

import { getCurrentWindow, LogicalSize } from "@tauri-apps/api/window";

import { useState } from "react";
import { cn } from "@/lib/utils";

interface ScreenshotResult {
  outputPath: string;
  duration: number;
  maxCpu: number;
  maxMem: number;
}

export function AppNavbar() {
  // 1. 获取全局高亮状态
  const screenshotHintActive = useAppStore(
    (state) => state.screenshotHintActive,
  );
  const setScreenshotHintActive = useAppStore(
    (state) => state.setScreenshotHintActive,
  );

  // 2. 维护 Tooltip 自身的 hover 状态
  const [isHovered, setIsHovered] = useState(false);

  const toggleCompactMode = useAppStore((state) => state.toggleCompactMode);
  const selectedScreen = useAppStore((state) => state.selectedScreen);
  
  // ✨ Command Palette 状态
  const setCommandPaletteOpen = useAppStore((state) => state.setCommandPaletteOpen);

  const getFilteredWallpapers = useAppStore(
    (state) => state.getFilteredWallpapers,
  );
  const setSelectedId = useAppStore((state) => state.setSelectedId);
  const filteredWallpapers = getFilteredWallpapers();

  // 截图成功 Dialog 状态
  const [screenshotDialogOpen, setScreenshotDialogOpen] = useState(false);
  const [screenshotResult, setScreenshotResult] =
    useState<ScreenshotResult | null>(null);

  const handleSwitchToCompact = async () => {
    const isTauri = isTauriEnv();

    if (!isTauri) {
      console.warn("[Browser Mode] Skipping window resize, toggling UI only.");
      toggleCompactMode(true);
      return;
    }

    try {
      const appWindow = getCurrentWindow();
      if (appWindow) {
        await appWindow.setSize(new LogicalSize(360, 600));
      }
      toggleCompactMode(true);
    } catch (err) {
      console.error("Resize failed:", err);
      toggleCompactMode(true);
    }
  };

  const handleStop = async () => {
    await useAppStore.getState().stopWallpaper();
  };

  const handleShuffle = async () => {
    if (filteredWallpapers.length === 0) {
      toast.error("No wallpapers available");
      return;
    }
    const randomIndex = Math.floor(Math.random() * filteredWallpapers.length);
    const randomWallpaper = filteredWallpapers[randomIndex];
    const screen = selectedScreen === "all" ? undefined : selectedScreen;
    await useAppStore.getState().applyWallpaper(randomWallpaper.id, screen);
    setSelectedId(randomWallpaper.id);
    // 优先显示 nickname
    const store = useAppStore.getState();
    const displayName = store.getNickname(randomWallpaper.id) || randomWallpaper.title;
    notify("Wallpaper Changed", displayName);
  };


  const handleScreenshot = async (_e?: React.MouseEvent<HTMLButtonElement>): Promise<void> => {
    setScreenshotHintActive(false); // 点击后立刻取消高亮
    const selectedId = useAppStore.getState().selectedId;

    if (!selectedId) {
      toast.error("Screenshot failed", {
        icon: <AlertCircle className="w-5 h-5 text-red-500" />,
        description: "Please select a wallpaper first",
      });
      throw new Error("No wallpaper selected");
    }

    try {
      const result = await takeScreenshot(selectedId);
      setScreenshotResult(result);
      setScreenshotDialogOpen(true);
      notify("Screenshot Saved", `Completed in ${result.duration.toFixed(1)}s`);
    } catch (error) {
      toast.error("Screenshot failed", {
        icon: <AlertCircle className="w-5 h-5 text-red-500" />,
        description: String(error),
      });
      throw error;
    }
  };

  const handleOpenFolder = async () => {
    if (screenshotResult) {
      try {
        await openFolder(screenshotResult.outputPath);
      } catch (error) {
        toast.error("Failed to open folder", {
          description: String(error),
        });
      }
    }
  };

  const handleOpenImage = async () => {
    if (screenshotResult) {
      try {
        await openImage(screenshotResult.outputPath);
      } catch (error) {
        toast.error("Failed to open image", {
          description: String(error),
        });
      }
    }
  };

  return (
    <>
      {/* 截图成功 Dialog */}
      <Dialog
        open={screenshotDialogOpen}
        onOpenChange={setScreenshotDialogOpen}
      >
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-green-600 dark:text-green-400">
              <CheckCircle2 className="w-5 h-5" />
              Screenshot Saved
            </DialogTitle>
            <DialogDescription className="pt-2">
              Your screenshot has been saved successfully.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-3 py-4">
            {/* 文件路径 */}
            <div className="flex items-start gap-3 p-3 rounded-lg bg-muted/50">
              <FolderOpen className="w-4 h-4 mt-0.5 text-muted-foreground shrink-0" />
              <div className="min-w-0 flex-1">
                <p className="text-xs text-muted-foreground mb-1">Path</p>
                <p className="text-sm font-mono break-all text-foreground">
                  {screenshotResult?.outputPath}
                </p>
              </div>
            </div>

            {/* 性能指标 - CPU/MEM 暂时禁用 */}
            <div className="flex justify-center">
              <div className="flex flex-col items-center p-4 rounded-lg bg-muted/50 min-w-32">
                <Clock className="w-5 h-5 text-muted-foreground mb-1" />
                <p className="text-2xl font-bold text-foreground">
                  {screenshotResult?.duration.toFixed(1)}s
                </p>
                <p className="text-xs text-muted-foreground">Duration</p>
              </div>
            </div>
            {/* CPU/MEM 监控暂时禁用，后期修复
            <div className="grid grid-cols-3 gap-3">
              <div className="flex flex-col items-center p-3 rounded-lg bg-muted/50">
                <Cpu className="w-4 h-4 text-orange-500 mb-1" />
                <p className="text-lg font-bold text-orange-500">{screenshotResult?.maxCpu.toFixed(1)}%</p>
                <p className="text-xs text-muted-foreground">Max CPU</p>
              </div>
              <div className="flex flex-col items-center p-3 rounded-lg bg-muted/50">
                <HardDrive className="w-4 h-4 text-blue-500 mb-1" />
                <p className="text-lg font-bold text-blue-500">{screenshotResult?.maxMem.toFixed(1)}</p>
                <p className="text-xs text-muted-foreground">Max Mem (MB)</p>
              </div>
            </div>
            */}
          </div>

          <DialogFooter className="gap-2 sm:gap-0">
            <Button variant="outline" onClick={handleOpenFolder}>
              <FolderOpen className="w-4 h-4 mr-2" />
              Open Folder
            </Button>
            <Button variant="outline" onClick={handleOpenImage}>
              <ImageIcon className="w-4 h-4 mr-2" />
              Open Image
            </Button>
            <Button onClick={() => setScreenshotDialogOpen(false)}>Done</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Navbar */}
      <div className="flex w-full items-center gap-4 py-2 px-4 drag-region select-none">
        <div className="no-drag flex items-center gap-2">
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8 text-primary hover:bg-primary/10"
                  onClick={handleSwitchToCompact}
                >
                  <Minimize2 className="w-4 h-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                <p>Compact Mode</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <TabsList className="bg-muted/40 border border-border h-auto p-1">
            <TabsTrigger
              value="wallpapers"
              className="gap-2 h-8 data-[state=active]:bg-secondary"
            >
              <ImageIcon className="w-4 h-4" /> Library
            </TabsTrigger>
            <TabsTrigger
              value="performance"
              className="gap-2 h-8 data-[state=active]:bg-secondary"
            >
              <Activity className="w-4 h-4" /> Monitor
            </TabsTrigger>
            <TabsTrigger
              value="settings"
              className="gap-2 h-8 data-[state=active]:bg-secondary"
            >
              <SettingsIcon className="w-4 h-4" /> Settings
            </TabsTrigger>
          </TabsList>
        </div>

        <Separator orientation="vertical" className="h-6 mx-2" />

        {/* Command Palette Trigger */}
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <button
                type="button"
                aria-label="Open Command Palette"
                className={cn(
                  "no-drag flex items-center gap-2 px-3 py-1.5 rounded-md border border-input bg-background hover:bg-accent hover:text-accent-foreground transition-colors cursor-pointer",
                  "min-w-[200px] max-w-xs"
                )}
                onClick={() => {
                  const currentState = useAppStore.getState().isCommandPaletteOpen;
                  setCommandPaletteOpen(!currentState);
                }}
              >
                <Search className="h-4 w-4 text-muted-foreground shrink-0" />
                <span className="text-sm text-muted-foreground truncate flex-1 text-left">
                  Search...
                </span>
                <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
                  <span className="text-xs">Ctrl</span>K
                </kbd>
              </button>
            </TooltipTrigger>
            <TooltipContent>
              <p>Open Command Palette (Ctrl+K)</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>

        {/* 这是一个弹簧占位符，会把右侧的图标推到最右边 */}
        <div className="flex-1" />

        <TooltipProvider>
          <div className="flex items-center gap-1 bg-muted/40 p-1 rounded-xl border border-border no-drag">
            <ScreenSelector variant="default" />

            <Separator orientation="vertical" className="h-4 mx-1" />

            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8 text-red-500 hover:bg-red-500/10"
                  onClick={handleStop}
                >
                  <Square className="w-4 h-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                <p>Stop</p>
              </TooltipContent>
            </Tooltip>

            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8"
                  onClick={handleShuffle}
                >
                  <Shuffle className="w-4 h-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                <p>Shuffle</p>
              </TooltipContent>
            </Tooltip>

            <Tooltip
              // 当鼠标悬浮 或者 全局提示激活时，都显示 Tooltip
              open={isHovered || screenshotHintActive}
              onOpenChange={(open) => {
                setIsHovered(open);
                // 如果用户主动移开鼠标，也可以顺便关掉全局提示
                if (!open && screenshotHintActive)
                  setScreenshotHintActive(false);
              }}
            >
              <TooltipTrigger asChild>
                <StatefulButton
                  variant="ghost"
                  size="icon"
                  // 动态添加高亮和呼吸灯动画
                  className={cn(
                    "h-8 w-8 transition-all duration-300",
                    screenshotHintActive &&
                      "ring-2 ring-primary ring-offset-1 bg-primary/20 text-primary animate-pulse",
                  )}
                  onClick={handleScreenshot}
                >
                  <Camera className="w-4 h-4" />
                </StatefulButton>
              </TooltipTrigger>
              <TooltipContent
                // 动态改变 Tooltip 的样式，让它更醒目
                className={cn(
                  "transition-colors",
                  screenshotHintActive &&
                    "bg-primary text-primary-foreground font-bold shadow-lg",
                )}
              >
                <p>
                  {screenshotHintActive
                    ? "Click me to screenshot!!"
                    : "Screenshot"}
                </p>
              </TooltipContent>
            </Tooltip>

            <Separator orientation="vertical" className="h-4 mx-1" />
            <AppMenu />
          </div>
        </TooltipProvider>
      </div>
    </>
  );
}
