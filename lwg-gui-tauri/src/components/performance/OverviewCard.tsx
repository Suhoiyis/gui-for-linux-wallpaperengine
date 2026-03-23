// src/components/performance/OverviewCard.tsx
import React, { memo } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Activity } from "lucide-react";
import PerformanceChart from "./Chart";
import { ChartDataPoint } from "@/types/performance";

interface OverviewCardProps {
  title: string;
  value: string;
  sub: string;
  icon: React.ReactNode;
  data: ChartDataPoint[];
  color: string;
  unit: string;
}

export const OverviewCard: React.FC<OverviewCardProps> = memo(
  ({ title, value, sub, icon, data, color, unit }) => {
    return (
      <Card className="overflow-hidden">
        <CardContent className="p-0">
          <div className="p-6 pb-2">
            <div className="flex justify-between items-start mb-2">
              <span className="text-sm font-medium text-muted-foreground">
                {title}
              </span>
              <div className="p-2 bg-muted/50 rounded-lg">{icon}</div>
            </div>
            <div className="text-2xl font-bold">{value}</div>
            <div className="text-xs text-muted-foreground">{sub}</div>
          </div>
          <div className="h-[100px] w-full mt-2 pr-4">
            <PerformanceChart
              data={data}
              color={color}
              unit={unit}
              height={100}
            />
          </div>
        </CardContent>
      </Card>
    );
  },
);
OverviewCard.displayName = "OverviewCard";

export const ThreadsCard = memo(
  ({ count, processCount = 1 }: { count: number; processCount?: number }) => {
    return (
      <Card>
        <CardContent className="p-6 flex flex-col justify-between h-full">
          <div className="flex justify-between items-start">
            <span className="text-sm font-medium text-muted-foreground">
              Active Threads
            </span>
            <div className="p-2 bg-muted/50 rounded-lg">
              {/* 修改为 emerald-500 */}
              <Activity className="w-4 h-4 text-emerald-500" />
            </div>
          </div>
          <div>
            <div className="text-3xl font-bold">{count}</div>
            <div className="text-xs text-muted-foreground mt-1">
              Across {processCount} process{processCount !== 1 ? "es" : ""}
            </div>
          </div>
          <div className="h-[100px] flex items-end gap-1 mt-2 opacity-30">
            {[40, 60, 30, 80, 50, 90, 20, 60].map((h, i) => (
              <div
                key={i}
                className="flex-1 bg-emerald-500 rounded-t-sm" // 修改为 emerald-500
                style={{ height: `${h}%` }}
              ></div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  },
);
ThreadsCard.displayName = "ThreadsCard";
