import { invoke } from "@tauri-apps/api/core";

export interface WebKitProcessSnapshot {
  timestamp: number;
  processes: WebKitProcessInfo[];
  totalMemoryMB: number;
}

export interface WebKitProcessInfo {
  pid: number;
  name: string;
  memory_mb: number;
  cpu_percent: number;
}

class MemoryProfiler {
  private snapshots: WebKitProcessSnapshot[] = [];
  private snapshotIntervalId: number | null = null;
  private logIntervalId: number | null = null;
  private readonly maxSnapshots = 180;

  startProfiling(intervalMs = 10000) {
    if (this.snapshotIntervalId) return;

    console.log("[MemoryProfiler] Starting WebKit process memory profiling...");

    this.snapshotIntervalId = window.setInterval(() => {
      this.takeSnapshot();
    }, intervalMs);

    // Log stats every minute — now properly tracked for cleanup
    this.logIntervalId = window.setInterval(() => {
      this.logStats();
    }, 60000);

    this.takeSnapshot();
  }

  stopProfiling() {
    if (this.snapshotIntervalId) {
      clearInterval(this.snapshotIntervalId);
      this.snapshotIntervalId = null;
    }
    if (this.logIntervalId) {
      clearInterval(this.logIntervalId);
      this.logIntervalId = null;
    }
    // Clear accumulated data to free memory
    this.snapshots = [];
    delete (window as any).__MEMORY_PROFILE__;
    console.log("[MemoryProfiler] Stopped and cleared data");
  }

  private async takeSnapshot() {
    try {
      const processes = await invoke<WebKitProcessInfo[]>("get_webkit_process_memory");
      const totalMemoryMB = processes.reduce((sum, p) => sum + p.memory_mb, 0);

      const snapshot: WebKitProcessSnapshot = {
        timestamp: Date.now(),
        processes,
        totalMemoryMB,
      };

      this.snapshots.push(snapshot);

      if (this.snapshots.length > this.maxSnapshots) {
        this.snapshots.shift();
      }

      if (this.snapshots.length % 10 === 0) {
        this.analyzeGrowth();
      }

      // Only export on demand (downloadReport), not every snapshot
    } catch (error) {
      console.error("[MemoryProfiler] Failed to take snapshot:", error);
    }
  }

  private analyzeGrowth() {
    if (this.snapshots.length < 10) return;

    const recent = this.snapshots.slice(-10);
    const first = recent[0];
    const last = recent[recent.length - 1];
    const timeDiff = (last.timestamp - first.timestamp) / 1000 / 60;
    const memDiffMB = last.totalMemoryMB - first.totalMemoryMB;
    const growthRate = memDiffMB / timeDiff;

    console.log(`[MemoryProfiler] Last ${recent.length} snapshots:`);
    console.log(`  Time span: ${timeDiff.toFixed(1)} min`);
    console.log(`  Memory growth: ${memDiffMB.toFixed(2)} MB`);
    console.log(`  Growth rate: ${growthRate.toFixed(2)} MB/min`);

    console.log("  WebKit processes:");
    last.processes.forEach((p) => {
      console.log(`    ${p.name} (PID ${p.pid}): ${p.memory_mb.toFixed(2)} MB, CPU: ${p.cpu_percent.toFixed(1)}%`);
    });

    if (growthRate > 20) {
      console.warn(
        `[MemoryProfiler] HIGH GROWTH RATE: ${growthRate.toFixed(2)} MB/min`,
      );
    } else if (growthRate > 10) {
      console.warn(
        `[MemoryProfiler] MODERATE GROWTH RATE: ${growthRate.toFixed(2)} MB/min`,
      );
    } else {
      console.log(
        `[MemoryProfiler] NORMAL GROWTH RATE: ${growthRate.toFixed(2)} MB/min`,
      );
    }
  }

  private logStats() {
    if (this.snapshots.length === 0) return;

    const latest = this.snapshots[this.snapshots.length - 1];
    const totalMB = latest.totalMemoryMB.toFixed(2);
    const processCount = latest.processes.length;

    console.log(
      `[MemoryProfiler] Current: ${totalMB} MB total (${processCount} WebKit processes)`,
    );
  }

  getSummary() {
    if (this.snapshots.length < 2) return null;

    const first = this.snapshots[0];
    const last = this.snapshots[this.snapshots.length - 1];
    const totalTime = (last.timestamp - first.timestamp) / 1000 / 60;
    const totalGrowth = last.totalMemoryMB - first.totalMemoryMB;

    return {
      totalSnapshots: this.snapshots.length,
      totalTimeMinutes: totalTime,
      totalGrowthMB: totalGrowth,
      averageGrowthRateMBperMin: totalTime > 0 ? totalGrowth / totalTime : 0,
      currentMemoryMB: last.totalMemoryMB,
      webkitProcessCount: last.processes.length,
    };
  }

  downloadReport() {
    const data = {
      userAgent: navigator.userAgent,
      snapshots: this.snapshots,
      summary: this.getSummary(),
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `webkit-memory-profile-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);

    console.log("[MemoryProfiler] Report downloaded");
  }
}

export const memoryProfiler = new MemoryProfiler();

if (import.meta.env.DEV) {
  memoryProfiler.startProfiling();

  (window as any).memoryProfiler = memoryProfiler;
  console.log("[MemoryProfiler] Available as window.memoryProfiler");
  console.log("Commands:");
  console.log("  window.memoryProfiler.stopProfiling()");
  console.log("  window.memoryProfiler.downloadReport()");
}
