// src/components/ui/thumbnail.tsx
import React, { memo, useMemo, useRef, useEffect } from "react";
import { Camera } from "lucide-react";
import { useAppStore } from "@/store/appStore";
import { convertFileSrc } from "@tauri-apps/api/core";
import { cn } from "@/lib/utils";

interface ThumbnailProps {
  wallpaperId: string;
  // ✨ 这里是关键：允许父组件传入样式（尤其是宽度和高度）
  className?: string;
  // 允许父组件自定义找不到壁纸时的占位图标
  fallbackIcon?: React.ReactNode;
}

export const Thumbnail = memo(
  ({ wallpaperId, className, fallbackIcon }: ThumbnailProps) => {
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

    // 判断是否为 GIF 动图
    const isGif = useMemo(() => {
      return wallpaper?.preview?.toLowerCase().endsWith(".gif");
    }, [wallpaper?.preview]);

    const canvasRef = useRef<HTMLCanvasElement>(null);

    // ✨ 性能核心：如果是 GIF，用 Canvas 绘制静态的第一帧来冻结动画，节省 GPU 资源
    useEffect(() => {
      if (!isGif || !previewUrl || !canvasRef.current) return;

      const img = new Image();
      img.src = previewUrl;
      img.crossOrigin = "anonymous";
      img.onload = () => {
        const canvas = canvasRef.current;
        const ctx = canvas?.getContext("2d");
        if (ctx && canvas) {
          // 画布尺寸匹配真实图片尺寸以保证清晰度
          canvas.width = img.width;
          canvas.height = img.height;
          ctx.drawImage(img, 0, 0);
        }
      };
    }, [previewUrl, isGif]);

    // 1. 找不到壁纸时的 fallback UI
    if (!wallpaper || !previewUrl) {
      return (
        <div
          className={cn(
            "bg-muted rounded overflow-hidden border border-white/10 flex items-center justify-center shrink-0",
            className, // 由父组件决定 w 和 h
          )}
        >
          {fallbackIcon || <Camera className="w-4 h-4 text-muted-foreground" />}
        </div>
      );
    }

    // 2. 正常渲染 UI
    return (
      <div
        className={cn(
          "bg-black/40 rounded overflow-hidden border border-white/10 shrink-0 relative group",
          className, // ✨ 由父组件决定 w 和 h，组件自身不包含任何固定尺寸！
        )}
      >
        {isGif ? (
          // 渲染静态画布
          <canvas
            ref={canvasRef}
            className="absolute inset-0 w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          />
        ) : (
          // 渲染普通图片
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

Thumbnail.displayName = "Thumbnail";
