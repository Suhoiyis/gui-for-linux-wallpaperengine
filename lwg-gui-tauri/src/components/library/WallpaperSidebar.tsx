import React from "react";
import { Star, Edit3, Copy, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { WallpaperCard } from "@/components/library/WallpaperCard";
import { ApplyButton } from "@/components/shared/ApplyButton";
import { EditNicknameDialog } from "@/components/dialogs/EditNicknameDialog";
import { useAppStore } from "@/store/appStore";
import { toast } from "sonner";
import { cn, getDisplayName, getColorForTag } from "@/lib/utils";
import { renderInlineMarkdown } from "@/lib/markdown";

function cleanDescription(text: string): string {
  return (
    text
      // 1. 移除 BBCode 标签 [tag]...[/tag] 和 [tag=...]
      .replace(/\[\/?[a-zA-Z0-9_]+\s*[^\]]*\]/g, "")
      // 2. 移除裸露的 URL（BBCode 移除后剩下的）
      .replace(/https?:\/\/\S+/g, "")
      // 3. Trim 每行的开头和结尾空格（杀死用于居中对齐的大量空格）
      .split("\n")
      .map((line) => line.trim())
      .join("\n")
      // 4. 压缩多余空行
      .replace(/\n{3,}/g, "\n\n")
      .trim()
  );
}
export function WallpaperSidebar() {
  const nicknames = useAppStore((state) => state.nicknames);
  const selectedWallpaper = useAppStore((state) =>
    state.getSelectedWallpaper(),
  );
  const getFilteredWallpapers = useAppStore((state) => state.getFilteredWallpapers);
  
  // Calculate position in sorted list
  const filteredWallpapers = getFilteredWallpapers();
  const wallpaperIndex = selectedWallpaper
    ? filteredWallpapers.findIndex((w) => w.id === selectedWallpaper.id) + 1
    : 0;
  
  // Get display name with nickname support
  const { displayName, originalTitle } = selectedWallpaper
    ? getDisplayName(nicknames, selectedWallpaper.id, selectedWallpaper.title)
    : { displayName: '', originalTitle: null };
  const isNickname = originalTitle !== null;
  
  const isFavorite = useAppStore((state) =>
    selectedWallpaper ? state.isFavorite(selectedWallpaper.id) : false,
  );
  const toggleFavorite = useAppStore((state) => state.toggleFavorite);

  const [isDialogOpen, setIsDialogOpen] = React.useState(false);
  const [isIdCopied, setIsIdCopied] = React.useState(false);

  const handleToggleFavorite = () => {
    if (selectedWallpaper) {
      toggleFavorite(selectedWallpaper.id);
      toast.success(
        isFavorite ? "Removed from favorites" : "Added to favorites",
        { description: displayName },
      );
    }
  };

  const handleCopyId = () => {
    if (!selectedWallpaper) return;
    navigator.clipboard.writeText(selectedWallpaper.id);
    setIsIdCopied(true);
    toast.success("ID copied to clipboard", { description: selectedWallpaper.id });
    setTimeout(() => setIsIdCopied(false), 1500);
  };

  return (
    <div className="h-full flex flex-col bg-card/30">
      <ScrollArea className="flex-1 p-4">
        {selectedWallpaper ? (
          <div className="space-y-3 animate-in fade-in zoom-in-95 duration-300">
            {/* 1. 预览图 */}
            <WallpaperCard
              wp={selectedWallpaper}
              isSelected={false}
              onSelect={() => {}}
              showTitle={false}
              showIcons={false}
              className="w-full aspect-square shadow-xl"
            />

            {/* 2. 标题行：标题 + 图标按钮 inline */}
            <div className="space-y-1.5">
              <div className="flex flex-wrap items-start gap-x-1 gap-y-0">
                <h1 className={cn(
                  "text-lg font-bold leading-tight",
                  isNickname && "nickname-text"
                )}>
                  {renderInlineMarkdown(displayName)}
                </h1>
                <div className="flex items-center gap-0.5 shrink-0">
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={() => setIsDialogOpen(true)}
                      >
                        <Edit3 className="w-3.5 h-3.5 text-muted-foreground" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent side="top">Edit Nickname</TooltipContent>
                  </Tooltip>

                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={handleToggleFavorite}
                      >
                        <Star className={cn(
                          "w-3.5 h-3.5",
                          isFavorite ? "fill-yellow-500 text-yellow-500" : "text-muted-foreground"
                        )} />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent side="top">
                      {isFavorite ? "Remove from favorites" : "Add to favorites"}
                    </TooltipContent>
                  </Tooltip>
                </div>
              </div>

              {/* 原标题 */}
              {isNickname && (
                <p className="original-name-text text-xs">
                  {renderInlineMarkdown(originalTitle || "")}
                </p>
              )}

              {/* Badge 行 - 中性色区分（避开 Tags 颜色） */}
              <div className="flex flex-wrap gap-1.5 pt-1">
                <Badge className="bg-slate-500/20 text-slate-600 dark:text-slate-400 border-slate-500/20 hover:bg-slate-500/30 text-[10px] px-1.5 h-5">
                  {selectedWallpaper.type || "unknown"}
                </Badge>
                <Badge 
                  className="bg-amber-500/20 text-amber-600 dark:text-amber-400 border-amber-500/20 hover:bg-amber-500/30 text-[10px] px-1.5 h-5 font-mono cursor-pointer"
                  onClick={handleCopyId}
                >
                  {selectedWallpaper.id}
                  {isIdCopied ? (
                    <Check className="w-3 h-3 ml-1 text-green-500" />
                  ) : (
                    <Copy className="w-3 h-3 ml-1 opacity-50" />
                  )}
                </Badge>
                <Badge className="bg-rose-500/20 text-rose-600 dark:text-rose-400 border-rose-500/20 hover:bg-rose-500/30 text-[10px] px-1.5 h-5">
                  {selectedWallpaper.size || "0 MB"}
                </Badge>
                {wallpaperIndex > 0 && (
                  <Badge className="bg-sky-500/20 text-sky-600 dark:text-sky-400 border-sky-500/20 hover:bg-sky-500/30 text-[10px] px-1.5 h-5">
                    {wallpaperIndex}/{filteredWallpapers.length}
                  </Badge>
                )}
              </div>

              {/* Tags - 带标题 */}
              {selectedWallpaper.tags && selectedWallpaper.tags.length > 0 && (
                <div className="space-y-1.5 pt-2">
                  <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">
                    Tags
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {selectedWallpaper.tags.slice(0, 8).map((tag) => (
                      <Badge
                        key={tag}
                        variant="outline"
                        className={cn(
                          "text-[10px] px-1.5 h-5 font-normal",
                          getColorForTag(tag)
                        )}
                      >
                        {tag}
                      </Badge>
                    ))}
                    {selectedWallpaper.tags.length > 8 && (
                      <span className="text-[10px] text-muted-foreground">
                        +{selectedWallpaper.tags.length - 8}
                      </span>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* 4. Description - 可折叠 */}
            {selectedWallpaper.description && cleanDescription(selectedWallpaper.description) && (
              <Accordion type="single" collapsible>
                <AccordionItem value="description" className="border-0">
                  <AccordionTrigger className="text-[11px] font-bold text-muted-foreground uppercase tracking-widest py-2 hover:no-underline">
                    Description
                  </AccordionTrigger>
                  <AccordionContent className="text-sm text-muted-foreground/80 leading-relaxed break-words pt-0 whitespace-pre-wrap overflow-wrap-anywhere">
                    {cleanDescription(selectedWallpaper.description)}
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            )}
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-muted-foreground/50 space-y-4">
            <div className="w-16 h-16 rounded-xl bg-muted/50 border-2 border-dashed border-muted-foreground/20" />
            <p className="text-sm">Select a wallpaper to view details</p>
          </div>
        )}
      </ScrollArea>

      {/* 底部 Apply 按钮 */}
      <div className="p-4 bg-background/50 border-t">
        <ApplyButton className="w-full h-11 bg-brand hover:bg-brand/90 text-brand-foreground font-bold rounded-xl" />
      </div>

      {/* Edit Nickname Dialog */}
      {selectedWallpaper && (
        <EditNicknameDialog
          wallpaperId={selectedWallpaper.id}
          wallpaperTitle={selectedWallpaper.title}
          open={isDialogOpen}
          onOpenChange={setIsDialogOpen}
        />
      )}
    </div>
  );
}
