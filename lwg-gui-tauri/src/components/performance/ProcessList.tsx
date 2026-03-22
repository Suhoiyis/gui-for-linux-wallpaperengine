// src/components/performance/ProcessList.tsx
import React, { useState, memo, useMemo } from "react";
import {
  Activity,
  Monitor,
  Layers,
  Image as ImageIcon,
  Server,
  MonitorIcon,
  BrickWall,
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Thumbnail } from "@/components/common/Thumbnail";
import { Collapsible, CollapsibleContent } from "@/components/ui/collapsible";
import { ChevronDown, ChevronRight } from "lucide-react";
import { ProcessStats, SystemStats } from "@/types/performance";
import { Wallpaper } from "@/types";
import PerformanceChart from "./Chart";
import { useActiveWallpapers } from "@/hooks/useActiveWallpapers";
import { useAppStore } from "@/store/appStore";
import { renderInlineMarkdown } from "@/lib/markdown";

interface ProcessRowProps {
  type: string;
  data: ProcessStats;
  icon: React.ReactNode;
}

// Small preview component for wallpaper
const WallpaperPreview = memo(
  ({ wallpaper }: { wallpaper: Wallpaper | null }) => {
    if (!wallpaper) {
      return (
        <div className="w-20 h-20 bg-muted/60 rounded-md overflow-hidden border border-border/50 shrink-0 relative">
          <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-gray-500/20 to-gray-600/20">
            <ImageIcon className="w-6 h-6 text-muted-foreground" />
          </div>
          <div className="absolute bottom-0 inset-x-0 bg-muted/80 text-[10px] text-foreground p-1 text-center truncate">
            No Wallpaper
          </div>
        </div>
      );
    }

    return (
      <div className="relative group rounded-md overflow-hidden">
        {/* 1. 直接复用通用缩略图组件，并在这里传入外壳的尺寸 w-20 h-20 */}
        <Thumbnail
          wallpaperId={wallpaper?.id || ""}
          className="w-20 h-20 rounded-md"
        />

        <div className="absolute bottom-0 inset-x-0 bg-black/60 text-[10px] text-white p-1 text-center truncate">
          {wallpaper?.type || "No Wallpaper"}
        </div>
      </div>
    );
  },
);
WallpaperPreview.displayName = "WallpaperPreview";

const ProcessRow: React.FC<ProcessRowProps> = memo(({ type, data, icon }) => {
  const [isOpen, setIsOpen] = useState(false);
  const { activeWallpapers } = useActiveWallpapers();
  const wallpapers = useAppStore((state) => state.wallpapers);

  const cpuColor =
    data.cpu < 20 ? "#22c55e" : data.cpu < 40 ? "#f97316" : "#ef4444";

  // Get active wallpaper info for backend
  const activeEntries = Array.from(activeWallpapers.entries());
  const hasActiveWallpaper = activeEntries.length > 0;

  // Find wallpaper details from store
  const firstWallpaperInfo = useMemo(() => {
    if (!hasActiveWallpaper || activeEntries.length === 0) return null;
    const wallpaperId = activeEntries[0][1];
    const screen = activeEntries[0][0];
    const wallpaper = wallpapers.find((w) => w.id === wallpaperId);
    return {
      screen,
      id: wallpaperId,
      wallpaper,
    };
  }, [hasActiveWallpaper, activeEntries, wallpapers]);

  return (
    <Card className="overflow-hidden transition-all hover:border-primary/50">
      <div className="p-4 flex flex-col gap-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-muted rounded-xl flex items-center justify-center shrink-0">
            {icon}
          </div>

          <div className="flex-1 min-w-0 grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
            <div className="col-span-3">
              <div className="font-bold text-base flex items-center gap-2">
                {data.name}
                <Badge
                  variant="outline"
                  className="text-[10px] h-5 px-1 font-mono text-muted-foreground"
                >
                  PID: {data.pid}
                </Badge>
              </div>
              <div
                className="text-xs text-muted-foreground truncate"
                title={data.cmd}
              >
                {data.cmd}
              </div>
            </div>

            <div className="col-span-3 flex gap-6">
              <div>
                <div
                  className={`font-mono font-bold ${data.cpu > 20 ? "text-orange-500" : "text-green-500"}`}
                >
                  {data.cpu.toFixed(1)}%
                </div>
                <div className="text-[10px] text-muted-foreground uppercase">
                  CPU
                </div>
              </div>
              <div>
                <div className="font-mono font-bold text-blue-500">
                  {data.mem.toFixed(0)} MB
                </div>
                <div className="text-[10px] text-muted-foreground uppercase">
                  Mem
                </div>
              </div>
              <div>
                <div className="font-mono text-muted-foreground">
                  {data.status}
                </div>
                <div className="text-[10px] text-muted-foreground uppercase">
                  Status
                </div>
              </div>
            </div>

            <div className="col-span-4 hidden md:flex gap-4 items-center">
              <div className="flex-1">
                <PerformanceChart
                  data={data.cpuHistory}
                  color={cpuColor}
                  unit="%"
                  height={60}
                  title="CPU Trend"
                />
              </div>
              <div className="flex-1">
                <PerformanceChart
                  data={data.memHistory}
                  color="#3b82f6"
                  unit=" MB"
                  height={60}
                  title="Mem Trend"
                />
              </div>
            </div>

            <div className="col-span-2 flex justify-end">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsOpen(!isOpen)}
              >
                {isOpen ? "Hide" : "Details"}
                {isOpen ? (
                  <ChevronDown className="ml-2 w-4 h-4" />
                ) : (
                  <ChevronRight className="ml-2 w-4 h-4" />
                )}
              </Button>
            </div>
          </div>
        </div>

        <Collapsible open={isOpen} className="space-y-2">
          <CollapsibleContent>
            <div className="pt-2 pl-[64px] pr-4 space-y-4">
              {/* Backend Specific Info - Now shows real data with wallpaper preview */}
              {type === "backend" &&
                hasActiveWallpaper &&
                firstWallpaperInfo && (
                  <div className="rounded-lg bg-secondary/30 border p-4 flex gap-4">
                    <WallpaperPreview
                      wallpaper={firstWallpaperInfo.wallpaper || null}
                    />
                    <div className="flex flex-col justify-center space-y-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <Badge className="bg-blue-500/20 text-blue-500 border-blue-500/20 hover:bg-blue-500/30 shrink-0">
                          Wallpaper
                        </Badge>
                        <span className="text-sm font-bold truncate" title={firstWallpaperInfo.wallpaper?.title || undefined}>
                          {firstWallpaperInfo.wallpaper?.title
                            ? renderInlineMarkdown(
                                firstWallpaperInfo.wallpaper.title,
                              )
                            : "Unknown"}
                        </span>
                      </div>
                      <div className="text-xs text-muted-foreground flex items-center gap-4">
                        <span className="flex items-center gap-1">
                          <Monitor className="w-3 h-3" />{" "}
                          {firstWallpaperInfo.screen}
                        </span>
                        <span className="flex items-center gap-1">
                          <Layers className="w-3 h-3" /> ID:{" "}
                          {firstWallpaperInfo.id}
                        </span>
                      </div>
                      <div className="text-xs text-muted-foreground pt-1">
                        Running • {data.threads.length} threads active
                      </div>
                    </div>
                  </div>
                )}

              {/* Thread Details */}
              <div className="rounded-lg bg-muted/30 border p-4">
                <h4 className="text-xs font-bold uppercase text-muted-foreground mb-3 flex items-center gap-2">
                  <Activity className="w-3 h-3" /> Active Threads (
                  {data.threads.length})
                </h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                  {data.threads.map((t, i) => (
                    <div
                      key={i}
                      className="text-xs font-mono text-muted-foreground flex items-center gap-2 hover:text-foreground transition-colors cursor-default"
                    >
                      <div className="w-1.5 h-1.5 rounded-full bg-muted-foreground/50" />
                      {t}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CollapsibleContent>
        </Collapsible>
      </div>
    </Card>
  );
});

ProcessRow.displayName = "ProcessRow";

export default function ProcessList({
  processes,
}: {
  processes: SystemStats["processes"];
}) {
  // const { activeWallpapers } = useActiveWallpapers();

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold flex items-center gap-2">
        <Server className="w-5 h-5" /> Process Details
      </h2>

      <ProcessRow
        type="backend"
        data={processes.backend}
        icon={<BrickWall className="text-yellow-500" />}
      />

      <ProcessRow
        type="frontend"
        data={processes.frontend}
        icon={<MonitorIcon className="text-pink-500" />}
      />

      {/* <ProcessRow
        type="tray"
        data={processes.tray}
        icon={<ArrowDownToLine className="text-purple-500" />}
      /> */}
    </div>
  );
}
