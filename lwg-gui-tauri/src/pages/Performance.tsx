// src/pages/Performance.tsx

import { Cpu, MemoryStick } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

// Hooks
import { useSystemStats } from "@/hooks/useSystemStats";

// Components
import {
  OverviewCard,
  ThreadsCard,
} from "@/components/performance/OverviewCard";
import ProcessList from "@/components/performance/ProcessList";
import ScreenshotHistory from "@/components/performance/ScreenshotHistory";

export function Performance() {
  const { stats, history, clearHistory, isLoading } = useSystemStats();

  if (isLoading) {
    return (
      <div className="flex flex-col h-full items-center justify-center">
        <div className="text-center space-y-4">
          <div className="text-base text-muted-foreground">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
          <p className="text-muted-foreground">
            Initializing Performance Monitor...
          </p>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="flex flex-col h-full items-center justify-center">
        <div className="text-center space-y-2">
          <p className="text-muted-foreground">
            Unable to load performance data
          </p>
          <p className="text-sm text-muted-foreground/70">
            Please check if the backend is running
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full space-y-6 overflow-hidden">
      <div className="flex flex-col space-y-1">
        <h1 className="text-2xl font-bold tracking-tight">System Monitor</h1>
        <p className="text-sm text-muted-foreground">
          Real-time resource usage of Wallpaper Engine components.
        </p>
      </div>

      <ScrollArea className="flex-1 -mx-6 px-6">
        <div className="space-y-8 pb-20">
          {/* 1. 总览卡片 */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <OverviewCard
              title="Total CPU"
              value={`${stats.totalCpu.toFixed(1)}%`}
              sub={`${stats.cpuCores} Cores Active`}
              icon={<Cpu className="text-purple-500" />}
              data={stats.cpuHistory}
              color="#a855f7"
              unit="%"
            />

            <OverviewCard
              title="Total Memory"
              value={`${stats.totalMem.toFixed(0)} MB`}
              sub={`of ${stats.totalMemoryGb.toFixed(1)} GB`}
              icon={<MemoryStick className="text-cyan-500" />}
              data={stats.memHistory}
              color="#06b6d4"
              unit=" MB"
            />
            <ThreadsCard
              count={stats.activeThreads}
              processCount={stats.processCount}
            />
          </div>

          <Separator />

          {/* 2. 进程详情 */}
          <ProcessList processes={stats.processes} />

          <Separator />

          {/* 3. 截图历史 */}
          <ScreenshotHistory items={history} onClear={clearHistory} />
        </div>
      </ScrollArea>
    </div>
  );
}
