// src/components/performance/Chart.tsx
import React, { memo } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { ChartDataPoint } from "@/types/performance";

interface PerformanceChartProps {
  data: ChartDataPoint[];
  color: string;
  unit: string;
  title?: string;
  height?: number;
}

const PerformanceChart: React.FC<PerformanceChartProps> = memo(
  ({ data, color, unit, title, height = 120 }) => {
    return (
      <div style={{ height }} className="w-full">
        {title && (
          <div className="text-[10px] uppercase text-muted-foreground font-semibold mb-1">
            {title}
          </div>
        )}
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id={`grad-${color}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={color} stopOpacity={0.2} />
                <stop offset="95%" stopColor={color} stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
              stroke="hsl(var(--border))"
              opacity={0.4}
            />
            <XAxis dataKey="time" hide axisLine={false} tickLine={false} />
            <YAxis
              hide={false}
              width={30}
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }}
              tickFormatter={(value) => `${value}`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                borderColor: "hsl(var(--border))",
                borderRadius: "6px",
                fontSize: "12px",
                padding: "4px 8px",
              }}
              itemStyle={{ color: "hsl(var(--foreground))" }}
              formatter={(value: number) => [
                `${value.toFixed(1)}${unit}`,
                "Usage",
              ]}
              labelStyle={{ display: "none" }}
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke={color}
              strokeWidth={2}
              fill={`url(#grad-${color})`}
              isAnimationActive={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    );
  },
);

PerformanceChart.displayName = "PerformanceChart";
export default PerformanceChart;
