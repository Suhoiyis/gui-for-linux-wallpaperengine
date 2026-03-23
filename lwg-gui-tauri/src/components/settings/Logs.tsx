import { useState, useEffect, useMemo, useCallback } from "react";
import { Filter, Copy, Check, Trash2 } from "lucide-react";
import { invoke } from "@tauri-apps/api/core";
import { listen, UnlistenFn } from "@tauri-apps/api/event";
import { LogEntry } from "@/types";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Header,
  LOG_FILTER_OPTIONS,
  getLevelColor,
  formatLogEntry,
} from "./Shared";

export function LogViewer() {
  const [filter, setFilter] = useState<string>("All");
  const [isCopied, setIsCopied] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);

  useEffect(() => {
    // Fetch initial logs from backend
    invoke<LogEntry[]>("get_logs")
      .then((data) => setLogs(data))
      .catch((err) => console.error("Failed to fetch logs:", err));

    // Listen for real-time log entries
    let unlisten: UnlistenFn | undefined;
    const setupListener = async () => {
      unlisten = await listen<LogEntry>("log-entry", (event) => {
        setLogs((prev) => [...prev, event.payload]);
      });
    };
    setupListener().catch(console.error);

    return () => {
      if (unlisten) unlisten();
    };
  }, []);

  const filteredLogs = useMemo(
    () => logs.filter((log) => filter === "All" || log.source === filter),
    [logs, filter],
  );

  const handleCopy = useCallback(() => {
    navigator.clipboard.writeText(filteredLogs.map(formatLogEntry).join("\n"));
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  }, [filteredLogs]);

  const handleClear = useCallback(() => {
    invoke("clear_logs")
      .then(() => setLogs([]))
      .catch((err) => console.error("Failed to clear logs:", err));
  }, []);

  return (
    <div className="space-y-6 h-full flex flex-col">
      <div className="flex items-center justify-between">
        <Header title="Log Monitor" desc="Real-time debug information." />
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-muted-foreground" />
          <Select value={filter} onValueChange={setFilter}>
            <SelectTrigger className="w-[140px] h-8 text-xs">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {LOG_FILTER_OPTIONS.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="flex-1 rounded-lg border bg-muted font-mono text-xs overflow-hidden flex flex-col">
        <ScrollArea className="flex-1 p-4">
          {filteredLogs.map((log) => (
            <div key={log.id} className="flex gap-4 py-0.5">
              <span className="text-muted-foreground w-16">{log.timestamp}</span>
              <span className={`w-10 font-bold ${getLevelColor(log.level)}`}>
                {log.level.toUpperCase()}
              </span>
              <span className="text-purple-500 w-20">[{log.source}]</span>
              <span className="text-foreground flex-1">{log.message}</span>
            </div>
          ))}
        </ScrollArea>
      </div>

      <div className="flex justify-between items-center pt-2">
        <span className="text-[10px] text-muted-foreground">
          {filteredLogs.length} entries
        </span>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleClear}
            className="h-8 gap-2 text-xs"
          >
            <Trash2 className="w-3 h-3" />
            Clear
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleCopy}
            className="h-8 gap-2 text-xs"
          >
            {isCopied ? (
              <Check className="w-3 h-3 text-green-500" />
            ) : (
              <Copy className="w-3 h-3" />
            )}
            {isCopied ? "Copied!" : "Copy"}
          </Button>
        </div>
      </div>
    </div>
  );
}