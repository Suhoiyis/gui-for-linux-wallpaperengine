// src/types/performance.ts

export interface ChartDataPoint {
  time: string;
  value: number;
}

export interface ProcessStats {
  pid: number;
  name: string;
  cmd: string;
  status: "Running" | "Sleeping" | "Idle";
  cpu: number;
  mem: number;
  cpuHistory: ChartDataPoint[];
  memHistory: ChartDataPoint[];
  threads: string[];
}

export interface SystemStats {
  totalCpu: number;
  totalMem: number;
  activeThreads: number;
  cpuHistory: ChartDataPoint[];
  memHistory: ChartDataPoint[];
  processes: {
    backend: ProcessStats;
    frontend: ProcessStats;
    tray: ProcessStats;
  };
  // System info
  cpuCores: number;
  totalMemoryGb: number;
  processCount: number;
}
