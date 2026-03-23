import { useState, useCallback, useEffect } from "react";
import {
  PlayCircle,
  Monitor,
  Settings2,
  FileText,
  Zap,
  RotateCw,
  Save,
  Square,
} from "lucide-react";

import { useAppStore } from "@/store/appStore";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { toast } from "sonner";


// 引入拆分后的子组件
import { PlaybackSettings } from "@/components/settings/Playback";
import { DisplaySettings } from "@/components/settings/Display";
import { SystemSettings } from "@/components/settings/System";
import { LogViewer } from "@/components/settings/Logs";

type SettingsTab = "playback" | "display" | "system" | "logs";

export function Settings() {
  const [activeTab, setActiveTab] = useState<SettingsTab>("playback");
  const {
    // settings,
    saveSettings,
    flushPendingUpdates,
    restartWallpapers,
    settingsLoading,
    highlightSettingField,
  } = useAppStore();
  const handleSave = useCallback(async () => {
    try {
      // Flush any pending debounced updates before bulk save
      flushPendingUpdates();
      await saveSettings();
      toast.success("Settings saved successfully");
    } catch {
      toast.error("Failed to save settings");
    }
  }, [saveSettings, flushPendingUpdates]);

  const handleReload = useCallback(async () => {
    try {
      await restartWallpapers();
      toast.success("Wallpapers reloaded");
    } catch {
      toast.error("Failed to reload wallpapers");
    }
  }, [restartWallpapers]);

  const handleStop = useCallback(async () => {
    await useAppStore.getState().stopWallpaper();
  }, []);

  // ✨ Auto-switch to appropriate tab when highlight is triggered
  useEffect(() => {
    if (highlightSettingField) {
      // Map field names to their corresponding tabs
      const fieldToTabMap: Record<string, SettingsTab> = {
        workshopPath: "system",
        assetsPath: "system",
        volume: "display",
        muteAudio: "display",
        fps: "playback",
        scaling: "playback",
        clamping: "playback",
      };

      const targetTab = fieldToTabMap[highlightSettingField];
      if (targetTab && activeTab !== targetTab) {
        setActiveTab(targetTab);
      }
    }
  }, [highlightSettingField, activeTab]);
  return (
    <div className="flex h-full w-full bg-background text-foreground rounded-xl overflow-hidden border">
      {/* Sidebar Navigation */}
      <aside className="w-64 border-r bg-muted/30 flex flex-col">
        <div className="p-6">
          <h2 className="text-2xl font-bold tracking-tight flex items-center gap-2">
            <Settings2 className="w-6 h-6" /> Settings
          </h2>
        </div>

        <div className="px-3 space-y-1 flex-1">
          <NavButton
            active={activeTab === "playback"}
            onClick={() => setActiveTab("playback")}
            icon={<PlayCircle className="w-4 h-4" />}
            label="Playback & Perf"
            desc="FPS, Cycling, Interaction"
          />
          <NavButton
            active={activeTab === "display"}
            onClick={() => setActiveTab("display")}
            icon={<Monitor className="w-4 h-4" />}
            label="Audio & Display"
            desc="Monitor, Theme, Volume"
          />
          <NavButton
            active={activeTab === "system"}
            onClick={() => setActiveTab("system")}
            icon={<Zap className="w-4 h-4" />}
            label="System & Tools"
            desc="Paths, Root, Autostart"
          />
          <NavButton
            active={activeTab === "logs"}
            onClick={() => setActiveTab("logs")}
            icon={<FileText className="w-4 h-4" />}
            label="Log Monitor"
            desc="Debug & Filters"
          />
        </div>

        <div className="p-4 border-t bg-background/50 space-y-3 backdrop-blur-sm">
          <Button
            className="w-full gap-2 font-bold shadow-lg shadow-primary/20"
            onClick={handleSave}
            disabled={settingsLoading}
          >
            <Save className="w-4 h-4" /> Save Changes
          </Button>
          <div className="grid grid-cols-2 gap-2">
            <Button
              variant="outline"
              size="sm"
              className="gap-2"
              onClick={handleReload}
            >
              <RotateCw className="w-3 h-3" /> Reload
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="gap-2 text-red-500 hover:text-red-600 hover:bg-red-500/10"
              onClick={handleStop}
            >
              <Square className="w-3 h-3 fill-current" /> Stop
            </Button>
          </div>
        </div>
      </aside>

      <ScrollArea className="flex-1 bg-card/10">
        <div className="p-8 max-w-7xl mx-auto space-y-8 pb-20">
          {activeTab === "playback" && <PlaybackSettings />}
          {activeTab === "display" && <DisplaySettings />}
          {activeTab === "system" && <SystemSettings />}
          {activeTab === "logs" && <LogViewer />}
        </div>
      </ScrollArea>
    </div>
  );
}

// NavButton 是布局专用组件，保留在主文件中
function NavButton({
  active,
  onClick,
  icon,
  label,
  desc,
}: {
  active: boolean;
  onClick: () => void;
  icon: React.ReactNode;
  label: string;
  desc: string;
}) {
  return (
    <Button
      variant={active ? "secondary" : "ghost"}
      className={`w-full justify-start h-auto py-3 px-4 mb-1 ${active ? "bg-secondary shadow-sm" : ""}`}
      onClick={onClick}
    >
      <div
        className={`mr-3 p-2 rounded-md ${active ? "bg-background text-primary" : "bg-muted text-muted-foreground"}`}
      >
        {icon}
      </div>
      <div className="text-left flex-1 min-w-0">
        <div
          className={`font-medium ${active ? "text-foreground" : "text-muted-foreground"}`}
        >
          {label}
        </div>
        <div className="text-xs text-muted-foreground truncate opacity-70">
          {desc}
        </div>
      </div>
    </Button>
  );
}
