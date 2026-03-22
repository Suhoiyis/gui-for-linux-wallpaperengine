import { useState, useEffect, useMemo } from "react";
import { ChevronLeft, ChevronRight, Copy, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { WallpaperCard } from "@/components/library/WallpaperCard";
import { Wallpaper } from "@/types";
import { renderInlineMarkdown } from "@/lib/markdown";
import { getDisplayName } from "@/lib/utils";
import { useAppStore } from "@/store/appStore";

interface CompactPreviewProps {
  /** 当前壁纸 */
  wallpaper: Wallpaper | null;
  /** 壁纸总数 */
  totalCount: number;
  /** 当前索引 (1-based) */
  currentIndex: number;
  /** 导航回调 (上一张/下一张) */
  onNavigate: (direction: -1 | 1) => void;
  /** 跳转到指定索引回调 (0-based) */
  onJumpTo: (index: number) => void;
}

/**
 * Compact 模式主图预览组件
 * 包含：壁纸预览卡片、标题与 ID 复制、分页控制器
 */
export function CompactPreview({
  wallpaper,
  totalCount,
  currentIndex,
  onNavigate,
  onJumpTo,
}: CompactPreviewProps) {
  const [isCopied, setIsCopied] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const nicknames = useAppStore((state) => state.nicknames);
  
  // 计算带昵称的显示名称
  const displayTitle = useMemo(() => {
    if (!wallpaper) return "Select Wallpaper";
    const { displayName } = getDisplayName(nicknames, wallpaper.id, wallpaper.title);
    return displayName;
  }, [wallpaper, nicknames]);

  // 同步当前索引到输入框
  useEffect(() => {
    setInputValue(currentIndex.toString());
  }, [currentIndex]);

  // 复制 ID 到剪贴板
  const handleCopyId = () => {
    navigator.clipboard.writeText(wallpaper?.id || "");
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 1500);
  };

  // 跳转到指定页码
  const handleJumpToPage = () => {
    const targetPage = parseInt(inputValue);
    if (!isNaN(targetPage) && targetPage >= 1 && targetPage <= totalCount) {
      const targetIndex = targetPage - 1;
      onJumpTo(targetIndex);
    } else {
      setInputValue(currentIndex.toString());
    }
  };

  // 键盘事件处理
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleJumpToPage();
      e.currentTarget.blur();
    }
  };

  return (
    <div className="p-4 space-y-4 flex flex-col items-center">
      {/* Preview Image */}
      {wallpaper && (
        <WallpaperCard
          wp={wallpaper}
          isSelected={false}
          onSelect={() => {}}
          showTitle={false}
          showIcons={true}
          className="w-[200px] h-[200px] shadow-sm"
        />
      )}

      {/* Title & ID */}
      <div className="w-full text-center space-y-1">
        <h3 className="font-bold text-lg leading-tight line-clamp-2 px-4">
          {displayTitle ? renderInlineMarkdown(displayTitle) : "Select Wallpaper"}
        </h3>
        <div
          className="inline-flex items-center gap-1 text-[10px] bg-muted px-2 py-0.5 rounded-full text-muted-foreground cursor-pointer hover:bg-muted/80 transition-colors"
          onClick={handleCopyId}
        >
          <span>{wallpaper?.id || "---"}</span>
          {isCopied ? (
            <Check className="h-3 w-3 text-green-500" />
          ) : (
            <Copy className="h-3 w-3" />
          )}
        </div>
      </div>

      {/* Navigation */}
      <div className="flex items-center gap-2 w-full px-4 justify-center">
        <Button
          variant="outline"
          size="icon"
          className="h-8 w-8 rounded-full"
          onClick={() => onNavigate(-1)}
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>

        {/* 可编辑的页码输入框 */}
        <div className="flex items-center gap-1 bg-muted rounded-md px-2 h-8 font-mono">
          <Input
            className="h-6 w-10 p-0 text-center border-none bg-transparent focus-visible:ring-0 text-xs [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onBlur={handleJumpToPage}
            onKeyDown={handleKeyDown}
          />
          <span className="text-xs text-muted-foreground">/ {totalCount}</span>
        </div>

        <Button
          variant="outline"
          size="icon"
          className="h-8 w-8 rounded-full"
          onClick={() => onNavigate(1)}
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
