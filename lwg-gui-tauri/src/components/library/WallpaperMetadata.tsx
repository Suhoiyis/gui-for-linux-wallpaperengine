// src/components/WallpaperMetadata.tsx
import { Badge } from "@/components/ui/badge";
import { Wallpaper } from "@/types";
import { cn, getColorForTag } from "@/lib/utils";

interface WallpaperMetadataProps {
  wallpaper: Wallpaper | null;
  className?: string; // 允许外部传入样式（比如 border-t pt-4）
}

export function WallpaperMetadata({
  wallpaper,
  className,
}: WallpaperMetadataProps) {
  return (
    <div className={cn("w-full grid grid-cols-2 gap-4", className)}>
      {/* 左侧：Tags */}
      <div className="space-y-2">
        <div className="text-xs font-bold text-muted-foreground uppercase tracking-widest">
          Tags
        </div>
        <div className="flex flex-wrap gap-1.5 content-start">
          {wallpaper?.tags?.map((tag) => (
            <Badge
              key={tag}
              variant="outline"
              className={cn(
                "text-[10px] px-1.5 h-5 font-normal border shadow-sm",
                getColorForTag(tag),
              )}
            >
              {tag}
            </Badge>
          ))}
          {!wallpaper?.tags?.length && (
            <span className="text-[10px] text-muted-foreground italic">
              No tags
            </span>
          )}
        </div>
      </div>

      {/* 右侧：Type */}
      <div className="space-y-2">
        <div className="text-xs font-bold text-muted-foreground uppercase tracking-widest">
          Type
        </div>
        <div className="flex flex-wrap content-start">
          <Badge
            variant="secondary"
            className="text-[10px] h-5 px-1.5 font-mono font-normal bg-slate-100 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700"
          >
            {wallpaper?.type || "Unknown"}
          </Badge>
        </div>
      </div>
    </div>
  );
}
