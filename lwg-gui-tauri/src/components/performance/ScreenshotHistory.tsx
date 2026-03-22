// src/components/performance/ScreenshotHistory.tsx
import React, { memo, useMemo } from "react";
import {
  Camera,
  FolderOpen,
  Image as ImageIcon,
  Trash2,
  CircleQuestionMark,
  Clock,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScreenshotRecord } from "@/api/wallpaper";
import { useAppStore } from "@/store/appStore";
import { convertFileSrc } from "@tauri-apps/api/core";
import { openFolder, openImage } from "@/api/wallpaper";
import { toast } from "sonner";
import { Thumbnail } from "@/components/common/Thumbnail";
import { getDisplayName } from "@/lib/utils";
import { renderInlineMarkdown } from "@/lib/markdown";
import {
  Empty,
  EmptyContent,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from "@/components/common/Empty";

interface ScreenshotRowProps {
  record: ScreenshotRecord;
}

// 缩略图预览组件
const ScreenshotThumbnail: React.FC<{ wallpaperId: string }> = memo(
  ({ wallpaperId }) => {
    const wallpapers = useAppStore((state) => state.wallpapers);

    const wallpaper = useMemo(() => {
      return wallpapers.find((w) => w.id === wallpaperId);
    }, [wallpapers, wallpaperId]);

    const previewUrl = useMemo(() => {
      if (!wallpaper?.preview) return null;
      if (
        wallpaper.preview.startsWith("http://") ||
        wallpaper.preview.startsWith("https://")
      ) {
        return wallpaper.preview;
      }
      return convertFileSrc(wallpaper.preview);
    }, [wallpaper?.preview]);

    if (!wallpaper) {
      return (
        <div className="w-16 h-10 bg-muted rounded overflow-hidden border border-border/50 flex items-center justify-center shrink-0">
          <Camera className="w-4 h-4 text-muted-foreground" />
        </div>
      );
    }

    return (
      <div className="w-16 h-10 bg-muted/60 rounded overflow-hidden border border-border/50 shrink-0 relative group">
        {previewUrl && (
          <img
            src={previewUrl}
            className="absolute inset-0 w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
            alt={wallpaper.title}
            loading="lazy"
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.style.display = "none";
            }}
          />
        )}
      </div>
    );
  },
);
ScreenshotThumbnail.displayName = "ScreenshotThumbnail";

const ScreenshotRow: React.FC<ScreenshotRowProps> = memo(({ record }) => {
  const wallpapers = useAppStore((state) => state.wallpapers);
  const nicknames = useAppStore((state) => state.nicknames);

  const wallpaper = useMemo(() => {
    return wallpapers.find((w) => w.id === record.wpId);
  }, [wallpapers, record.wpId]);
  
  // 计算带昵称的显示名称
  const displayTitle = useMemo(() => {
    if (!wallpaper) return "Unknown Wallpaper";
    const { displayName } = getDisplayName(nicknames, wallpaper.id, wallpaper.title);
    return displayName;
  }, [wallpaper, nicknames]);

  const handleOpenFolder = async () => {
    try {
      await openFolder(record.outputPath);
    } catch (error) {
      toast.error("Failed to open folder", { description: String(error) });
    }
  };

  const handleOpenImage = async () => {
    try {
      await openImage(record.outputPath);
    } catch (error) {
      toast.error("Failed to open image", { description: String(error) });
    }
  };

  return (
    <div className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors group">
      {/* 左侧：缩略图 + 壁纸信息 */}
      <div className="flex items-center gap-4">
        <Thumbnail wallpaperId={record.wpId} className="w-12 h-12" />

        <div className="min-w-0">
          <div className="text-base font-bold max-w-[200px] truncate" title={displayTitle}>
            {renderInlineMarkdown(displayTitle)}
          </div>
        </div>
      </div>

      {/* 中间：Duration */}
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Clock className="w-4 h-4" />
        <span className="font-mono">{record.duration.toFixed(1)}s</span>
      </div>

      {/* 右侧：操作按钮 */}
      <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8"
          onClick={handleOpenFolder}
          title="Open Folder"
        >
          <FolderOpen className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8"
          onClick={handleOpenImage}
          title="Open Image"
        >
          <ImageIcon className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
});

ScreenshotRow.displayName = "ScreenshotRow";

interface ScreenshotHistoryProps {
  items: ScreenshotRecord[];
  onClear: () => void;
}

export default function ScreenshotHistory({
  items,
  onClear,
}: ScreenshotHistoryProps) {
  // ✨ 新增：获取 appStore 的 setter 和 activeTab 控制
  const setScreenshotHintActive = useAppStore(
    (state) => state.setScreenshotHintActive,
  );
  const setActiveTab = useAppStore((state) => state.setActiveTab);

  // ✨ 新增：处理点击跳转和高亮的逻辑
  const handleGoScreenshot = () => {
    // 1. 跳转回 Library Tab
    setActiveTab("wallpapers");

    // 2. 激活高亮提示
    setScreenshotHintActive(true);

    // 3. 3秒后自动移除高亮
    setTimeout(() => {
      setScreenshotHintActive(false);
    }, 3000);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Camera className="w-5 h-5" /> Screenshot History
          </h2>
          <p className="text-xs text-muted-foreground">
            Recent screenshot captures.
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={onClear}
          disabled={items.length === 0}
        >
          <Trash2 className="w-4 h-4 mr-2" /> Clear
        </Button>
      </div>

      <div className="rounded-xl border bg-card/50 overflow-hidden">
        {items.length === 0 ? (
          <Empty>
            <EmptyHeader>
              <EmptyMedia variant="icon">
                <CircleQuestionMark />
              </EmptyMedia>
              <EmptyTitle>No Screenshot Records</EmptyTitle>
              <EmptyDescription>
                You have no screenshot records to display.
              </EmptyDescription>
            </EmptyHeader>
            <EmptyContent className="flex-row justify-center gap-2">
              {/* ✨ 修改：绑定 onClick 事件 */}
              <Button onClick={handleGoScreenshot}>Go Screenshot!!</Button>
            </EmptyContent>
          </Empty>
        ) : (
          <div className="divide-y">
            {items.map((record, index) => (
              <ScreenshotRow
                key={record.wpId + "-" + record.timestamp + "-" + index}
                record={record}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
