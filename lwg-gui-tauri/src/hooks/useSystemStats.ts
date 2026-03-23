// src/hooks/useSystemStats.ts
import { useState, useEffect } from "react";
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

const HISTORY_SIZE = 60;

// ... (mapEventToStats 函数完全保持原样)
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
      tray: mapProcess(raw.processes?.tray, "Tray"),
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

  useEffect(() => {
    const isTauri = isTauriEnv();
    let unlistenPerformance: (() => void) | null = null;
    let mockInterval: NodeJS.Timeout | null = null;

    if (isTauri) {
      // ==========================================
      // 真实环境：Tauri 后端通信
      // ==========================================
      const setupMonitoring = async () => {
        try {
          await invoke("start_performance_monitor");

          unlistenPerformance = await listen<RawPerformanceEvent>(
            "performance-update",
            (event) => {
              const mappedStats = mapEventToStats(event.payload);
              setStats(mappedStats);
              setIsLoading(false);
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
      // ==========================================
      // 浏览器环境：生成动态 Mock 数据
      // ==========================================
      console.warn("[Browser Mode] Starting Mock Performance Monitor...");

      // 初始化一段平缓的历史数据（60个点）
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

      // 模拟截图历史
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
        // 生成这一秒的新数据
        const newBackendCpu = Math.random() * 15 + 5;
        const newBackendMem = Math.random() * 50 + 400;
        const newFrontendCpu = Math.random() * 5 + 1;
        const newFrontendMem = Math.random() * 20 + 150;

        // 推进数组（去掉最老的，加入最新的）
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

        // 组装符合你定义的 Raw 事件结构
        const fakeEvent: RawPerformanceEvent = {
          total_cpu: newBackendCpu + newFrontendCpu,
          total_memory_mb: newBackendMem + newFrontendMem,
          total_threads: 145,
          cpu_cores: 16,
          total_memory_gb: 32,
          process_count: 3,
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
          },
        };

        // 经过你原来的 map 函数转换并更新状态
        setStats(mapEventToStats(fakeEvent));
        setIsLoading(false);
      }, 1000); // 1秒更新一次图表
    }

    return () => {
      // 清理逻辑：销毁监听或清除定时器
      if (isTauri) {
        if (unlistenPerformance) unlistenPerformance();
        invoke("stop_performance_monitor").catch(console.error);
      } else if (mockInterval) {
        clearInterval(mockInterval);
      }
    };
  }, []);

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
      setHistory([]); // 浏览器端直接清空状态
    }
  };

  return { stats, history, clearHistory, isLoading };
}
