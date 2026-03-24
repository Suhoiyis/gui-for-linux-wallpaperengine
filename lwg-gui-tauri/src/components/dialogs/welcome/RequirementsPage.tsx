import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import { CheckCircle2, AlertTriangle, ExternalLink, Loader2 } from "lucide-react";
import { cn, isTauriEnv } from "@/lib/utils";

interface CheckResult {
  name: string;
  status: "ok" | "warning" | "unknown" | "checking";
  message: string;
}

export function RequirementsPage() {
  const [checks, setChecks] = useState<CheckResult[]>([
    { name: "linux-wallpaperengine", status: "checking", message: "Checking..." },
    { name: "Xvfb", status: "checking", message: "Checking..." },
    { name: "Wayland", status: "checking", message: "Checking..." },
  ]);

  useEffect(() => {
    async function runChecks() {
      if (!isTauriEnv()) {
        setTimeout(() => {
            setChecks([
            { name: "linux-wallpaperengine", status: "ok", message: "Mock mode" },
            { name: "Xvfb (Recommended)", status: "ok", message: "Mock mode" },
            { name: "Wayland Session", status: "ok", message: "Mock mode" },
            ]);
        }, 1000);
        return;
      }

      try {
        const wpInstalled = await invoke<boolean>("check_wallpaperengine_installed").catch(() => false);
        const xvfbAvailable = await invoke<boolean>("check_xvfb_available").catch(() => false);
        const displayServer = await invoke<string>("get_display_server").catch(() => "unknown");

        setChecks([
          {
            name: "linux-wallpaperengine",
            status: wpInstalled ? "ok" : "warning",
            message: wpInstalled ? "Found" : "Not found — app may not work correctly",
          },
          {
            name: "Xvfb (Recommended)",
            status: xvfbAvailable ? "ok" : "warning",
            message: xvfbAvailable ? "Available" : "Not found — screenshots may not work",
          },
          {
            name: "Wayland Session",
            status: displayServer === "wayland" ? "ok" : "warning",
            message: displayServer === "wayland" ? "Detected" : `Running on ${displayServer}`,
          },
        ]);
      } catch (err) {
        console.error("Failed to run system checks:", err);
      }
    }

    runChecks();
  }, []);

  return (
    <div className="flex flex-col justify-center h-full py-4">
      <div className="space-y-3">
        {checks.map((check) => (
          <div
            key={check.name}
            className={cn(
              "flex items-start gap-3 p-3 rounded-lg border",
              check.status === "ok" ? "border-green-500/30 bg-green-500/5" : 
              check.status === "checking" ? "border-border bg-muted/20" :
              "border-yellow-500/30 bg-yellow-500/5"
            )}
          >
            {check.status === "ok" ? (
              <CheckCircle2 className="h-5 w-5 text-green-500 shrink-0" />
            ) : check.status === "checking" ? (
                <Loader2 className="h-5 w-5 text-muted-foreground shrink-0 animate-spin" />
            ) : (
              <AlertTriangle className="h-5 w-5 text-yellow-500 shrink-0" />
            )}
            <div className="flex-1">
              <p className="font-medium text-sm">{check.name}</p>
              <p className="text-xs text-muted-foreground">{check.message}</p>
              {check.name === "Xvfb (Recommended)" && check.status === "warning" && (
                <a
                  href="https://github.com/Almamu/linux-wallpaperengine/wiki/Installation"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-primary hover:underline flex items-center gap-1 mt-1"
                >
                  How to install <ExternalLink className="h-3 w-3" />
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}