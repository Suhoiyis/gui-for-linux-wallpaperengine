import { useMemo, useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useAppStore } from "@/store/appStore";
import { isTauriEnv } from "@/lib/utils";

// 子组件
import { CompactNavbar } from "@/components/compact/CompactNavbar";
import { CompactPreview } from "@/components/compact/CompactPreview";
import { WallpaperMetadata } from "@/components/library/WallpaperMetadata";
import { CompactCarousel } from "@/components/compact/CompactCarousel";
import { ApplyButton } from "@/components/shared/ApplyButton";

// Tauri API
import { getCurrentWindow, LogicalSize } from "@tauri-apps/api/window";

/**
 * Compact 模式主页面 (Controller)
 * 职责：从 Zustand 获取数据、处理顶层事件、组装子组件
 */
export function CompactMode() {
  const { wallpapers, selectedId, setSelectedId, toggleCompactMode } =
    useAppStore();

  // 动态预览状态：当底部轮播图滑动时实时更新的壁纸 ID
  const [dynamicPreviewId, setDynamicPreviewId] = useState<string | null>(null);

  // 计算当前显示的壁纸（优先显示滑动预览，没有则显示已选中的）
  const displayId = dynamicPreviewId || selectedId;

  // 计算当前壁纸
  const currentWallpaper = useMemo(
    () => wallpapers.find((w) => w.id === displayId) || wallpapers[0],
    [wallpapers, displayId],
  );

  // 计算当前索引 (1-based)
  const currentIndex = useMemo(
    () => wallpapers.findIndex((w) => w.id === displayId) + 1,
    [wallpapers, displayId],
  );

  // 切换到正常窗口模式
  const handleSwitchToNormal = async () => {
    const isTauri = isTauriEnv();
    if (!isTauri) {
      console.warn("Detected non-Tauri environment. Skipping window resize.");
      toggleCompactMode(false);
      return;
    }

    try {
      const appWindow = getCurrentWindow();
      if (appWindow) {
        await appWindow.setSize(new LogicalSize(1200, 800));
      }
      toggleCompactMode(false);
    } catch (err) {
      console.error("Failed to resize window:", err);
      toggleCompactMode(false);
    }
  };

  // 导航到上一张/下一张
  const handleNavigate = (direction: -1 | 1) => {
    const currentIdx = wallpapers.findIndex((w) => w.id === selectedId);
    if (currentIdx === -1) return;
    let newIdx = currentIdx + direction;
    if (newIdx < 0) newIdx = wallpapers.length - 1;
    if (newIdx >= wallpapers.length) newIdx = 0;
    setSelectedId(wallpapers[newIdx].id);
  };

  // 跳转到指定索引 (0-based)
  const handleJumpTo = (index: number) => {
    if (wallpapers[index]) {
      setSelectedId(wallpapers[index].id);
    }
  };

  // 选择壁纸
  const handleSelect = (id: string) => {
    setSelectedId(id);
  };

  return (
    <div className="flex flex-col h-full bg-background text-foreground select-none">
      {/* Navbar */}
      <CompactNavbar onSwitchToNormal={handleSwitchToNormal} />

      {/* Main Content */}
      <ScrollArea className="flex-1">
        <div className="p-4 space-y-4 flex flex-col items-center">
          {/* Preview */}
          <CompactPreview
            wallpaper={currentWallpaper}
            totalCount={wallpapers.length}
            currentIndex={currentIndex}
            onNavigate={handleNavigate}
            onJumpTo={handleJumpTo}
          />

          {/* Apply Button */}
          <ApplyButton
            size="lg"
            className="w-full font-bold bg-brand hover:bg-brand/90 text-brand-foreground shadow-lg shadow-brand/20 transition-all active:scale-95"
          />

          {/* Metadata */}
          <WallpaperMetadata wallpaper={currentWallpaper} />
        </div>
      </ScrollArea>

      {/* Carousel */}
      <CompactCarousel
        wallpapers={wallpapers}
        selectedId={selectedId}
        onSelect={handleSelect}
        onHoverPreview={setDynamicPreviewId}
      />
    </div>
  );
}
