// src/hooks/useSystemStats.ts
import { useState, useEffect, useRef, useCallback } from "react";
import { listen } from "@tauri-apps/api/event";
import { invoke } from "@tauri-apps/api/core";
import { isTauriEnv } from "@/lib/utils";
import {
  SystemStats,
  ProcessStats,
  ChartDataPoint,
} from "@/types/performance";
import { ScreenshotRecord } from "@/api/wallpaper";

interface RawPerformanceEvent {
  total_cpu: number;
  total_memory_mb: number;
  total_threads: number;
  processes?: {
    [key: string]: RawProcessStats;
  };
  timestamp?: number;
  cpu_cores?: number;
  total_memory_gb?: number;
  process_count?: number;
}

interface RawProcessStats {
  pid: number;
  name: string;
  cmd: string;
  status: string;
  cpu: number;
  memory_mb: number;
  threads: number;
  cpu_history?: number[];
  mem_history?: number[];
  thread_names?: string[];
}

const HISTORY_SIZE = 30;
const UPDATE_INTERVAL_MS = 2000;
const GC_INTERVAL_MS = 60000;

function mapEventToStats(raw: RawPerformanceEvent): SystemStats {
  const createDefaultProcess = (name: string): ProcessStats => ({
    pid: 0,
    name,
    cmd: "N/A",
    status: "Sleeping",
    cpu: 0,
    mem: 0,
    cpuHistory: [],
    memHistory: [],
    threads: [],
  });

  const toChartData = (values: number[] | undefined): ChartDataPoint[] => {
    if (!values) return [];

    const result: ChartDataPoint[] = [];
    const dataLen = values.length;

    for (let i = 0; i < HISTORY_SIZE - dataLen; i++) {
      result.push({ time: "", value: 0 });
    }

    for (let i = 0; i < dataLen; i++) {
      result.push({
        time: `${dataLen - i}s`,
        value: values[i],
      });
    }

    return result;
  };

  const mapProcess = (
    raw: RawProcessStats | undefined,
    name: string,
  ): ProcessStats => {
    if (!raw) return createDefaultProcess(name);
    return {
      pid: raw.pid,
      name: raw.name || name,
      cmd: raw.cmd,
      status: (raw.status || "Sleeping") as "Running" | "Sleeping" | "Idle",
      cpu: raw.cpu,
      mem: raw.memory_mb,
      cpuHistory: toChartData(raw.cpu_history),
      memHistory: toChartData(raw.mem_history),
      threads: raw.thread_names || [],
    };
  };

  const allProcesses = raw.processes || {};
  const processValues = Object.values(allProcesses);

  const cpuHistory: ChartDataPoint[] = [];
  const memHistory: ChartDataPoint[] = [];

  let maxDataLen = 0;
  for (const p of processValues) {
    if (p?.cpu_history) {
      maxDataLen = Math.max(maxDataLen, p.cpu_history.length);
    }
  }
  maxDataLen = Math.min(maxDataLen, HISTORY_SIZE);

  for (let i = 0; i < HISTORY_SIZE - maxDataLen; i++) {
    cpuHistory.push({ time: "", value: 0 });
    memHistory.push({ time: "", value: 0 });
  }

  for (let i = 0; i < maxDataLen; i++) {
    let totalCpu = 0;
    let totalMem = 0;
    for (const p of processValues) {
      const processLen = p?.cpu_history?.length || 0;
      const idx = i - (maxDataLen - processLen);
      if (idx >= 0 && idx < processLen) {
        totalCpu += p.cpu_history?.[idx] || 0;
        totalMem += p.mem_history?.[idx] || 0;
      }
    }
    cpuHistory.push({ time: `${maxDataLen - i}s`, value: totalCpu });
    memHistory.push({ time: `${maxDataLen - i}s`, value: totalMem });
  }

  return {
    totalCpu: raw.total_cpu ?? 0,
    totalMem: raw.total_memory_mb ?? 0,
    activeThreads: raw.total_threads ?? 0,
    cpuHistory,
    memHistory,
    processes: {
      backend: mapProcess(raw.processes?.backend, "Backend"),
      frontend: mapProcess(raw.processes?.frontend, "Frontend"),
      webkit_web: raw.processes?.webkit_web
        ? mapProcess(raw.processes.webkit_web, "WebKit Web")
        : undefined,
      webkit_net: raw.processes?.webkit_net
        ? mapProcess(raw.processes.webkit_net, "WebKit Network")
        : undefined,
      webkit_gpu: raw.processes?.webkit_gpu
        ? mapProcess(raw.processes.webkit_gpu, "WebKit GPU")
        : undefined,
    },
    cpuCores: raw.cpu_cores ?? 1,
    totalMemoryGb: raw.total_memory_gb ?? 16,
    processCount: raw.process_count ?? 1,
  };
}

export function useSystemStats() {
  const [stats, setStats] = useState<SystemStats | null>(null);
  const [history, setHistory] = useState<ScreenshotRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const lastWebkitWeb = useRef<ProcessStats | undefined>(undefined);
  const lastWebkitNet = useRef<ProcessStats | undefined>(undefined);
  const lastWebkitGpu = useRef<ProcessStats | undefined>(undefined);
  const pendingEvent = useRef<RawPerformanceEvent | null>(null);
  const isPaused = useRef(false);
  const lastUpdateTime = useRef(0);

  const processEvent = useCallback((event: RawPerformanceEvent) => {
    const now = Date.now();
    if (now - lastUpdateTime.current < UPDATE_INTERVAL_MS) {
      pendingEvent.current = event;
      return;
    }
    lastUpdateTime.current = now;
    pendingEvent.current = null;

    const mappedStats = mapEventToStats(event);

    if ((mappedStats.processes.webkit_web?.pid ?? 0) > 0) {
      lastWebkitWeb.current = mappedStats.processes.webkit_web;
    }
    if ((mappedStats.processes.webkit_net?.pid ?? 0) > 0) {
      lastWebkitNet.current = mappedStats.processes.webkit_net;
    }
    if ((mappedStats.processes.webkit_gpu?.pid ?? 0) > 0) {
      lastWebkitGpu.current = mappedStats.processes.webkit_gpu;
    }

    const statsWithPersistentWebkit: SystemStats = {
      ...mappedStats,
      processes: {
        ...mappedStats.processes,
        webkit_web: mappedStats.processes.webkit_web || lastWebkitWeb.current,
        webkit_net: mappedStats.processes.webkit_net || lastWebkitNet.current,
        webkit_gpu: mappedStats.processes.webkit_gpu || lastWebkitGpu.current,
      },
    };

    setStats(statsWithPersistentWebkit);
    setIsLoading(false);
  }, []);

  useEffect(() => {
    const isTauri = isTauriEnv();
    let unlistenPerformance: (() => void) | null = null;
    let mockInterval: NodeJS.Timeout | null = null;
    let gcInterval: NodeJS.Timeout | null = null;
    let flushInterval: NodeJS.Timeout | null = null;

    const handleVisibilityChange = () => {
      isPaused.current = document.hidden;
      if (document.hidden) {
        const gcFn = (window as unknown as { gc?: () => void }).gc;
        if (typeof gcFn === "function") {
          gcFn();
        }
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);

    const gcFn = (window as unknown as { gc?: () => void }).gc;
    if (typeof gcFn === "function") {
      gcInterval = setInterval(() => {
        if (!isPaused.current) {
          gcFn();
        }
      }, GC_INTERVAL_MS);
    }

    flushInterval = setInterval(() => {
      if (pendingEvent.current && !isPaused.current) {
        processEvent(pendingEvent.current);
      }
    }, UPDATE_INTERVAL_MS);

    if (isTauri) {
      const setupMonitoring = async () => {
        try {
          await invoke("start_performance_monitor");

          unlistenPerformance = await listen<RawPerformanceEvent>(
            "performance-update",
            (event) => {
              if (!isPaused.current) {
                processEvent(event.payload);
              }
            },
          );

          const screenshotHistory = await invoke<ScreenshotRecord[]>(
            "get_screenshot_history",
          );
          setHistory(screenshotHistory);
        } catch (error) {
          console.error("Failed to setup performance monitoring:", error);
          setIsLoading(false);
        }
      };

      setupMonitoring();
    } else {
      console.warn("[Browser Mode] Starting Mock Performance Monitor...");

      let mockCpuHistoryBackend = Array(60)
        .fill(0)
        .map(() => Math.random() * 5 + 5);
      let mockMemHistoryBackend = Array(60)
        .fill(0)
        .map(() => Math.random() * 20 + 300);
      let mockCpuHistoryFrontend = Array(60)
        .fill(0)
        .map(() => Math.random() * 2 + 1);
      let mockMemHistoryFrontend = Array(60)
        .fill(0)
        .map(() => Math.random() * 10 + 100);

      setHistory([
        {
          timestamp: Math.floor(Date.now() / 1000) - 3600,
          wpId: "cyberpunk_01",
          outputPath: "/home/user/Pictures/shot1.png",
          duration: 1.2,
          maxCpu: 24.5,
          maxMem: 450.2,
        },
        {
          timestamp: Math.floor(Date.now() / 1000) - 7200,
          wpId: "nature_02",
          outputPath: "/home/user/Pictures/shot2.png",
          duration: 0.8,
          maxCpu: 15.1,
          maxMem: 310.5,
        },
      ]);

      mockInterval = setInterval(() => {
        if (isPaused.current) return;

        const newBackendCpu = Math.random() * 15 + 5;
        const newBackendMem = Math.random() * 50 + 400;
        const newFrontendCpu = Math.random() * 5 + 1;
        const newFrontendMem = Math.random() * 20 + 150;

        mockCpuHistoryBackend = [
          ...mockCpuHistoryBackend.slice(1),
          newBackendCpu,
        ];
        mockMemHistoryBackend = [
          ...mockMemHistoryBackend.slice(1),
          newBackendMem,
        ];
        mockCpuHistoryFrontend = [
          ...mockCpuHistoryFrontend.slice(1),
          newFrontendCpu,
        ];
        mockMemHistoryFrontend = [
          ...mockMemHistoryFrontend.slice(1),
          newFrontendMem,
        ];

        const fakeEvent: RawPerformanceEvent = {
          total_cpu: newBackendCpu + newFrontendCpu,
          total_memory_mb: newBackendMem + newFrontendMem,
          total_threads: 145,
          cpu_cores: 16,
          total_memory_gb: 32,
          process_count: 4,
          timestamp: Date.now(),
          processes: {
            backend: {
              pid: 10425,
              name: "linux-wallpaperengine",
              cmd: "/opt/linux-wallpaperengine",
              status: "Running",
              cpu: newBackendCpu,
              memory_mb: newBackendMem,
              threads: 45,
              cpu_history: mockCpuHistoryBackend,
              mem_history: mockMemHistoryBackend,
              thread_names: ["main", "render", "audio_decode"],
            },
            frontend: {
              pid: 10426,
              name: "lwg-gui",
              cmd: "/usr/bin/lwg-gui",
              status: "Running",
              cpu: newFrontendCpu,
              memory_mb: newFrontendMem,
              threads: 24,
              cpu_history: mockCpuHistoryFrontend,
              mem_history: mockMemHistoryFrontend,
              thread_names: ["ui_thread", "ipc_worker"],
            },
            webkit_gpu: {
              pid: 10428,
              name: "WebKit GPU",
              cmd: "/usr/lib/webkit2gtk-4.1/WebKitGPUProcess",
              status: "Sleeping",
              cpu: 0.3,
              memory_mb: 82.4,
              threads: 8,
              cpu_history: Array(60).fill(0).map((_, i) => (i % 10 === 0 ? 0.8 : 0.3)),
              mem_history: Array(60).fill(82.4),
              thread_names: ["gpu_main", "compositor", "render"],
            },
          },
        };

        setStats(mapEventToStats(fakeEvent));
        setIsLoading(false);
      }, UPDATE_INTERVAL_MS);
    }

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      if (unlistenPerformance) unlistenPerformance();
      if (mockInterval) clearInterval(mockInterval);
      if (gcInterval) clearInterval(gcInterval);
      if (flushInterval) clearInterval(flushInterval);
      if (isTauri) {
        invoke("stop_performance_monitor").catch(console.error);
      }
    };
  }, [processEvent]);

  const clearHistory = async () => {
    const isTauri = isTauriEnv();
    if (isTauri) {
      try {
        await invoke("clear_screenshot_history");
        setHistory([]);
      } catch (error) {
        console.error("Failed to clear history:", error);
      }
    } else {
      console.warn("[Browser Mode] Clearing mock history");
      setHistory([]);
    }
  };

  return { stats, history, clearHistory, isLoading };
}
