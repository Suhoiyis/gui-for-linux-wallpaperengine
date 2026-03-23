import React, { memo, useMemo, useRef, useEffect, useState } from "react";
import { Camera } from "lucide-react";
import { useAppStore } from "@/store/appStore";
import { invoke } from "@tauri-apps/api/core";
import { cn } from "@/lib/utils";

interface ThumbnailProps {
  wallpaperId: string;
  className?: string;
  fallbackIcon?: React.ReactNode;
}

export const Thumbnail = memo(
  ({ wallpaperId, className, fallbackIcon }: ThumbnailProps) => {
    const wallpapers = useAppStore((state) => state.wallpapers);

    const wallpaper = useMemo(() => {
      return wallpapers.find((w) => w.id === wallpaperId);
    }, [wallpapers, wallpaperId]);

    const [previewUrl, setPreviewUrl] = useState<string | null>(null);

    useEffect(() => {
      if (!wallpaper?.preview) {
        setPreviewUrl(null);
        return;
      }

      // HTTP/HTTPS 链接直接使用
      if (
        wallpaper.preview.startsWith("http://") ||
        wallpaper.preview.startsWith("https://")
      ) {
        setPreviewUrl(wallpaper.preview);
        return;
      }

      // 本地路径：通过 Rust 命令读取并返回 base64
      let cancelled = false;
      invoke<string>("read_preview_image", { path: wallpaper.preview })
        .then((dataUrl) => {
          if (!cancelled) setPreviewUrl(dataUrl);
        })
        .catch(() => {
          if (!cancelled) setPreviewUrl(null);
        });

      return () => {
        cancelled = true;
      };
    }, [wallpaper?.preview]);

    const isGif = useMemo(() => {
      return wallpaper?.preview?.toLowerCase().endsWith(".gif");
    }, [wallpaper?.preview]);

    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
      if (!isGif || !previewUrl || !canvasRef.current) return;

      const img = new Image();
      img.src = previewUrl;
      img.onload = () => {
        const canvas = canvasRef.current;
        const ctx = canvas?.getContext("2d");
        if (ctx && canvas) {
          canvas.width = img.width;
          canvas.height = img.height;
          ctx.drawImage(img, 0, 0);
        }
      };
    }, [previewUrl, isGif]);

    if (!wallpaper || !previewUrl) {
      return (
        <div
          className={cn(
            "bg-muted rounded overflow-hidden border border-white/10 flex items-center justify-center shrink-0",
            className,
          )}
        >
          {fallbackIcon || <Camera className="w-4 h-4 text-muted-foreground" />}
        </div>
      );
    }

    return (
      <div
        className={cn(
          "bg-black/40 rounded overflow-hidden border border-white/10 shrink-0 relative group",
          className,
        )}
      >
        {isGif ? (
          <canvas
            ref={canvasRef}
            className="absolute inset-0 w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          />
        ) : (
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