// src/components/library/WallpaperCard.tsx
import { memo, useMemo } from "react";
import { Star, Video, Monitor, Globe, Image as ImageIcon, Check } from "lucide-react";
import { Wallpaper } from "@/types";
import { renderInlineMarkdown } from "@/lib/markdown";
import { convertFileSrc } from "@tauri-apps/api/core";
import { useAppStore } from "@/store/appStore";
import { toast } from "sonner";
import { Toggle } from "@/components/ui/toggle";
import { cn, getDisplayName } from "@/lib/utils";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

interface WallpaperCardProps {
  wp: Wallpaper;
  isSelected: boolean;
  onSelect: () => void;

  // ✨ 细粒度显示控制
  showTitle?: boolean;
  showIcons?: boolean;
  className?: string;
  children?: React.ReactNode;
}

function getPreviewUrl(preview: string): string {
  if (preview.startsWith("http://") || preview.startsWith("https://")) {
    return preview;
  }
  return convertFileSrc(preview);
}

export const WallpaperCard = memo(function WallpaperCard({
  wp,
  isSelected,
  onSelect,
  showTitle = true,
  showIcons = true,
  className,
  children,
}: WallpaperCardProps) {
  const nicknames = useAppStore((state) => state.nicknames);
  const isFavorite = useAppStore((state) => state.isFavorite(wp.id));
  const toggleFavorite = useAppStore((state) => state.toggleFavorite);
  
  // Selection mode state
  const isSelectionMode = useAppStore((state) => state.isSelectionMode);
  const selectedForPlaylist = useAppStore((state) => state.selectedForPlaylist);
  const toggleSelectForPlaylist = useAppStore((state) => state.toggleSelectForPlaylist);
  const isInSelection = selectedForPlaylist.has(wp.id);
  
  // Get display name with nickname support
  const { displayName, originalTitle } = getDisplayName(nicknames, wp.id, wp.title);
  const isNickname = originalTitle !== null;

  const handleToggleFavorite = () => {
    toggleFavorite(wp.id);
    toast.success(
      isFavorite ? "Removed from favorites" : "Added to favorites",
      { description: displayName },
    );
  };

  const handleClick = () => {
    if (isSelectionMode) {
      toggleSelectForPlaylist(wp.id);
    } else {
      onSelect();
    }
  };

  const previewUrl = useMemo(() => getPreviewUrl(wp.preview), [wp.preview]);

  const TypeIcon = useMemo(() => {
    const type = wp.type?.toLowerCase() ?? "";
    switch (type) {
      case "video":
        return <Video className="w-3.5 h-3.5 text-pink-400" />;
      case "web":
        return <Globe className="w-3.5 h-3.5 text-blue-400" />;
      case "scene":
        return <Monitor className="w-3.5 h-3.5 text-emerald-400" />;
      default:
        return <ImageIcon className="w-3.5 h-3.5 text-muted-foreground" />;
    }
  }, [wp.type]);

  return (
    // 1. 最外层容器：负责响应点击、布局位置和传入的 className
    <div
      onClick={handleClick}
      className={cn(
        "group relative cursor-pointer select-none",
        "aspect-square",
        className,
      )}
    >
      {/* 2. 视觉容器：负责圆角、边框、阴影和 hover 效果 */}
      <div
        className={cn(
          "relative w-full h-full overflow-hidden rounded-2xl border-2 bg-muted transition-all duration-300",
          isSelected
            ? "border-brand ring-2 ring-brand ring-offset-4 ring-offset-background shadow-lg shadow-brand/20"
            : "border-border/50 hover:border-brand/50 hover:shadow-xl hover:shadow-brand/10",
          isInSelection && "border-brand ring-2 ring-brand/50",
        )}
      >
        {/* 3. 内容层：图片和叠加元素 */}

        {/* 图片 */}
        <img
          src={previewUrl}
          className="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          alt={wp.title}
          loading="lazy"
          draggable={false}
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.src =
              'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23374151" width="100" height="100"/><text x="50" y="55" text-anchor="middle" fill="%239ca3af" font-size="12">No Preview</text></svg>';
          }}
        />

        {/* 收藏按钮 (左上) - 选择模式下隐藏 */}
        {showIcons && !isSelectionMode && (
          <Tooltip>
            <TooltipTrigger asChild>
              <div
                className="absolute top-2 left-2 z-20"
                onClick={(e) => e.stopPropagation()} // 再次确保阻断点击
              >
                <Toggle
                  pressed={isFavorite}
                  onPressedChange={handleToggleFavorite}
                  size="sm"
                  className={cn(
                    "h-7 w-7 p-0 rounded-full border border-border/50 backdrop-blur-sm transition-all",
                    // 未选中时半透明黑底，选中时淡黄底
                    isFavorite
                      ? "bg-yellow-500/20 border-yellow-500/50 opacity-100"
                      : "bg-muted/60 hover:bg-muted/80 opacity-0 group-hover:opacity-100",
                  )}
                >
                  <Star
                    className={cn(
                      "h-3.5 w-3.5 transition-colors",
                      isFavorite
                        ? "fill-yellow-400 text-yellow-400"
                        : "fill-transparent text-foreground/90",
                    )}
                  />
                </Toggle>
              </div>
            </TooltipTrigger>
            <TooltipContent side="top">
              <p>{isFavorite ? "Remove from favorites" : "Add to favorites"}</p>
            </TooltipContent>
          </Tooltip>
        )}

        {/* 类型图标 (右上) - 选择模式下隐藏 */}
        {showIcons && !isSelectionMode && (
          <div className="absolute top-2 right-2 z-20 bg-muted/70 backdrop-blur-md p-1.5 rounded-lg border border-border/30 shadow-sm flex items-center justify-center pointer-events-none">
            {TypeIcon}
          </div>
        )}

        {/* Selection mode checkbox (center overlay) */}
        {isSelectionMode && (
          <div className="absolute inset-0 z-25 flex items-center justify-center bg-muted/30 transition-opacity">
            <div
              className={cn(
                "w-8 h-8 rounded-full border-2 flex items-center justify-center transition-all",
                isInSelection
                  ? "bg-brand border-brand"
                  : "bg-muted/80 border-border/50"
              )}
            >
              {isInSelection && <Check className="w-5 h-5 text-brand-foreground" />}
            </div>
          </div>
        )}

        {/* 底部标题 (渐变层) */}
        {showTitle && (
          <Tooltip>
            <TooltipTrigger asChild>
              <div className="absolute inset-x-0 bottom-0 z-10 bg-gradient-to-t from-muted/90 via-muted/50 to-transparent p-3 pt-8 pointer-events-none">
                <p className={cn(
                  "text-[11px] font-bold text-foreground truncate",
                  isNickname && "nickname-text"
                )}>
                  {renderInlineMarkdown(displayName)}
                </p>
              </div>
            </TooltipTrigger>
            {isNickname && (
              <TooltipContent side="top">
                <p className="text-xs">Original: {originalTitle}</p>
              </TooltipContent>
            )}
          </Tooltip>
        )}

        {/* 子元素插槽 (覆盖在最上层) */}
        {children && (
          <div className="absolute inset-0 z-30 pointer-events-none">
            {children}
          </div>
        )}
      </div>
    </div>
  );
});
