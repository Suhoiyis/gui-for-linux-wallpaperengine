// src/components/library/LibraryHeader.tsx
import { memo, useState, useEffect, useRef, useMemo } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { renderInlineMarkdown } from "@/lib/markdown";
import { getDisplayName } from "@/lib/utils";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { ArrowUpDown, CheckSquare } from "lucide-react";
import { useAppStore } from "@/store/appStore";

interface LibraryHeaderProps {
  currentTitle: string;
  activeWallpaperId: string | null;
  onTitleClick: (id: string) => void;
  totalCount: number;
  currentPage: number;
  totalPages: number;
  currentIndex: number;
  onPageChange: (page: number) => void;
}

// 宽度阈值：小于此值切换为紧凑布局
// 这个值大约是"Currently Using" + 排序下拉 + 分页信息 + 合理的壁纸名称宽度
const COMPACT_THRESHOLD = 550;

export const LibraryHeader = memo(
  ({
    currentTitle,
    activeWallpaperId,
    onTitleClick,
    totalCount,
    currentPage,
    totalPages,
    currentIndex,
    onPageChange,
  }: LibraryHeaderProps) => {
    const [isEditing, setIsEditing] = useState(false);
    const [inputValue, setInputValue] = useState(currentPage.toString());
    const inputRef = useRef<HTMLInputElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);
    const [isCompact, setIsCompact] = useState(false);

    useEffect(() => {
      setInputValue(currentPage.toString());
    }, [currentPage]);

    // ✨ 监测组件自身宽度
    useEffect(() => {
      const container = containerRef.current;
      if (!container) return;

      const resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          const width = entry.contentRect.width;
          setIsCompact(width < COMPACT_THRESHOLD);
        }
      });

      resizeObserver.observe(container);
      
      // 初始检查
      const initialWidth = container.clientWidth;
      setIsCompact(initialWidth < COMPACT_THRESHOLD);
      
      return () => resizeObserver.disconnect();
    }, []);

    // ✨ 获取排序状态
    const sortBy = useAppStore((state) => state.sortBy);
    const setSortBy = useAppStore((state) => state.setSortBy);
    
    // ✨ 勾选模式状态
    const isSelectionMode = useAppStore((state) => state.isSelectionMode);
    const enterSelectionMode = useAppStore((state) => state.enterSelectionMode);
    
    // ✨ 获取 nicknames 和 wallpapers 用于显示昵称
    const nicknames = useAppStore((state) => state.nicknames);
    const wallpapers = useAppStore((state) => state.wallpapers);
    
    // 计算带昵称的显示名称
    const displayTitle = useMemo(() => {
      if (!activeWallpaperId) return currentTitle;
      const wp = wallpapers.find((w) => w.id === activeWallpaperId);
      if (!wp) return currentTitle;
      const { displayName } = getDisplayName(nicknames, wp.id, wp.title);
      return displayName;
    }, [activeWallpaperId, wallpapers, nicknames, currentTitle]);

    useEffect(() => {
      if (isEditing && inputRef.current) {
        inputRef.current.focus();
        inputRef.current.select();
      }
    }, [isEditing]);

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Enter") {
        const page = parseInt(inputValue);
        if (!isNaN(page) && page >= 1 && page <= totalPages) {
          onPageChange(page);
          setIsEditing(false);
        } else {
          toast.error("Invalid Page");
          setInputValue(currentPage.toString());
        }
      } else if (e.key === "Escape") {
        setIsEditing(false);
        setInputValue(currentPage.toString());
      }
    };

    const handleBlur = () => {
      setIsEditing(false);
      setInputValue(currentPage.toString());
    };

    // 分页信息（JSX 表达式，非组件函数，避免重渲染丢失焦点）
    const paginationInfo = (
      <span className="flex items-center gap-1 text-xs font-mono text-muted-foreground/50 select-none">
        <span>
          {currentIndex > 0 ? currentIndex : "-"}/{totalCount} wallpapers
        </span>
        {totalPages > 0 && (
          <span className="flex items-center ml-1 text-muted-foreground/40">
            (
            {isEditing ? (
              <Input
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                onBlur={handleBlur}
                className="inline-block h-5 w-8 min-h-0 py-0 px-0 text-center text-xs font-mono border-0 border-b border-primary rounded-none bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 leading-none mx-0.5 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
              />
            ) : (
              <span
                onClick={() => setIsEditing(true)}
                className="inline-block w-8 text-center mx-0.5 text-primary/90 hover:text-primary cursor-pointer transition-colors border-b border-dashed border-primary/30 hover:border-solid"
              >
                {currentPage}
              </span>
            )}
            /{totalPages} Pages)
          </span>
        )}
      </span>
    );

    // 排序选择器（JSX 表达式）
    const sortSelect = (
      <Select
        value={sortBy}
        onValueChange={(value: "name" | "id" | "size") => setSortBy(value)}
      >
        <SelectTrigger className="h-7 w-[130px] text-xs bg-transparent border-dashed shadow-none">
          <div className="flex items-center gap-2 text-muted-foreground">
            <ArrowUpDown className="h-3 w-3" />
            <SelectValue placeholder="Sort by" />
          </div>
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="name">Name (A-Z)</SelectItem>
          <SelectItem value="id">ID (Ascending)</SelectItem>
          <SelectItem value="size">Size (Largest)</SelectItem>
        </SelectContent>
      </Select>
    );

    // 勾选模式按钮（仅图标 + Tooltip）
    const selectButton = (
      <TooltipProvider delayDuration={300}>
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7"
              onClick={enterSelectionMode}
              disabled={isSelectionMode}
            >
              <CheckSquare className="h-4 w-4" />
            </Button>
          </TooltipTrigger>
          <TooltipContent side="bottom">
            <p>Select mode</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    );

    return (
      <div
        ref={containerRef}
        className="bg-muted/20 px-4 py-2 rounded-xl border border-border/50 shrink-0"
      >
        {!isCompact ? (
          /* 宽布局（桌面模式）：单行布局 */
          <div className="flex items-center justify-between gap-4">
            {/* 左侧：Current Using */}
            <div className="flex items-center gap-3 text-xs font-bold text-muted-foreground tracking-widest flex-shrink min-w-0">
              <span className="text-brand uppercase whitespace-nowrap">
                Currently Using
              </span>
              {activeWallpaperId ? (
                <span
                  className="text-foreground truncate flex-1 min-w-0 cursor-pointer hover:text-brand transition-colors underline underline-offset-2 decoration-brand/30 hover:decoration-brand"
                  onClick={() => onTitleClick(activeWallpaperId)}
                >
                  {displayTitle ? renderInlineMarkdown(displayTitle) : "None"}
                </span>
              ) : (
                <span className="text-foreground truncate flex-1 min-w-0">
                  {displayTitle ? renderInlineMarkdown(displayTitle) : "None"}
                </span>
              )}
            </div>

            {/* 右侧：排序 + 分页 */}
            <div className="flex items-center gap-4 flex-shrink-0">
              {selectButton}
              <div className="h-4 w-px bg-border/50"></div>
              {sortSelect}
              <div className="h-4 w-px bg-border/50"></div>
              {paginationInfo}
            </div>
          </div>
        ) : (
          /* 窄布局（紧凑模式）：两行布局 */
          <div>
            {/* 第一行（状态区）：Active 徽章 + 壁纸名称（全宽） */}
            <div className="flex items-center gap-2 text-xs font-bold text-muted-foreground tracking-widest">
              <span className="px-2 py-0.5 rounded-full bg-brand/20 text-brand text-[10px] uppercase whitespace-nowrap">
                Active
              </span>
              {activeWallpaperId ? (
                <span
                  className="text-foreground truncate flex-1 min-w-0 cursor-pointer hover:text-brand transition-colors"
                  onClick={() => onTitleClick(activeWallpaperId)}
                >
                  {displayTitle ? renderInlineMarkdown(displayTitle) : "None"}
                </span>
              ) : (
                <span className="text-foreground truncate flex-1 min-w-0">
                  {displayTitle ? renderInlineMarkdown(displayTitle) : "None"}
                </span>
              )}
            </div>

            {/* 第二行（控制区）：分页 + 排序，整体靠右 */}
            <div className="flex items-center justify-end gap-3 mt-1">
              {selectButton}
              <div className="h-4 w-px bg-border/50"></div>
              {paginationInfo}
              <div className="h-4 w-px bg-border/50"></div>
              {sortSelect}
            </div>
          </div>
        )}
      </div>
    );
  },
);