import { Zap, MousePointer2, Clock, AlertTriangle, ListMusic } from "lucide-react";
import { useState, useEffect } from "react";
import { isTauriEnv } from "@/lib/utils";
import { invoke } from "@tauri-apps/api/core";
import { useAppStore } from "@/store/appStore";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Label } from "@/components/ui/label";
// 引入公共组件
import {
  Header,
  SliderRow,
  SwitchRow,
  SelectField,
  InputField,
  SCALING_OPTIONS,
  CLAMPING_OPTIONS,
  CYCLE_ORDER_OPTIONS,
  TextareaField,
} from "./Shared";
import { CyclePlaylistSelector } from "@/components/playlist/CyclePlaylistSelector";

export function PlaybackSettings() {
  const { settings, updateSetting } = useAppStore();
  const [isWayland, setIsWayland] = useState<boolean | null>(null);

  useEffect(() => {
    const isTauri = isTauriEnv();
    if (isTauri) {
      invoke<string>("get_display_server")
        .then((result) => {
          const wayland = result === "wayland";
          setIsWayland(wayland);
          // X11 环境下清除 Wayland 相关配置
          if (!wayland && settings) {
            if (settings.waylandOnlyActive) {
              updateSetting("waylandOnlyActive", false);
            }
            if (settings.waylandIgnoreAppids) {
              updateSetting("waylandIgnoreAppids", "");
            }
          }
        })
        .catch(() => setIsWayland(false));
    } else {
      setIsWayland(false);
    }
  }, [settings, updateSetting]);

  if (!settings) return <div>Loading...</div>;

  return (
    <div className="space-y-6">
      <Header
        title="Playback & Performance"
        desc="Fine-tune rendering quality, automation, and system integration."
      />

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 items-start">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-orange-500" /> Rendering Quality
            </CardTitle>
            <CardDescription>
              Optimize for battery life or visual fidelity.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <SliderRow
              label="Target FPS Limit"
              value={settings.fps}
              onValueChange={(v) => updateSetting("fps", v)}
              max={144}
              min={10}
              step={1}
              suffix=" FPS"
            />
            <Separator />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <SwitchRow
                label="Disable Parallax"
                description="Stop mouse movement effects"
                checked={settings.disableParallax}
                onCheckedChange={(v) => updateSetting("disableParallax", v)}
              />
              <SwitchRow
                label="Disable Particles"
                description="Turn off rain/fire effects"
                checked={settings.disableParticles}
                onCheckedChange={(v) => updateSetting("disableParticles", v)}
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Display Behavior</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <SelectField
                label="Scaling Mode"
                value={settings.scaling}
                onValueChange={(v) => updateSetting("scaling", v)}
                options={SCALING_OPTIONS}
              />
              <SelectField
                label="Texture Clamping"
                value={settings.clamping}
                onValueChange={(v) => updateSetting("clamping", v)}
                options={CLAMPING_OPTIONS}
              />
            </div>
            <Separator />
            <SwitchRow
              label="No Fullscreen Pause"
              description="Keep playing when games open"
              checked={settings.noFullscreenPause}
              onCheckedChange={(v) => updateSetting("noFullscreenPause", v)}
            />
            <SwitchRow
              label="Disable Mouse Interaction"
              description="Ignore mouse clicks"
              checked={settings.disableMouse}
              onCheckedChange={(v) => updateSetting("disableMouse", v)}
              icon={<MousePointer2 className="w-4 h-4 text-muted-foreground" />}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-blue-500" /> Playlist Automation
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <SwitchRow
              label="Enable Auto-Cycle"
              description="Automatically switch wallpapers"
              checked={settings.cycleEnabled}
              onCheckedChange={(v) => updateSetting("cycleEnabled", v)}
            />
            {settings.cycleEnabled && (
              // animate-in 和相关的动画类名
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2 animate-in fade-in slide-in-from-top-2 duration-300">
                <InputField
                  label="Cycle Interval (minutes)"
                  value={settings.cycleInterval}
                  onChange={(v) =>
                    updateSetting("cycleInterval", parseInt(v) || 15)
                  }
                  type="number"
                  min={1}
                />
                <SelectField
                  label="Cycle Order"
                  value={settings.cycleOrder}
                  onValueChange={(v) => updateSetting("cycleOrder", v)}
                  options={CYCLE_ORDER_OPTIONS}
                />
              </div>
            )}
            {settings.cycleEnabled && (
              <div className="space-y-2 pt-2 animate-in fade-in slide-in-from-top-2 duration-300">
                <Label className="flex items-center gap-2 text-sm font-medium">
                  <ListMusic className="w-4 h-4 text-muted-foreground" />
                  Cycle Source
                </Label>
                <CyclePlaylistSelector className="w-full" />
                <p className="text-xs text-muted-foreground">
                  Choose which playlist to use for automatic cycling. Select "All Wallpapers" to cycle through your entire library.
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Wayland Tweaks - only relevant on Wayland */}
        <Card
          className={
            isWayland === true
              ? "border-blue-500/20 bg-blue-500/5"
              : "border-amber-500/20 bg-amber-500/5"
          }
        >
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Wayland Tweaks</span>
              <Badge
                variant="outline"
                className={
                  "text-xs font-normal " +
                  (isWayland === true
                    ? "border-blue-500/30 text-blue-500"
                    : "border-amber-500/30 text-amber-500")
                }
              >
                {isWayland === null
                  ? "Detecting..."
                  : isWayland
                    ? "Wayland"
                    : "X11"}
              </Badge>
            </CardTitle>
            {isWayland === false && (
              <p className="text-xs text-amber-600 flex items-center gap-1">
                <AlertTriangle className="w-3 h-3" />
                These settings only work on Wayland. Your session is X11.
              </p>
            )}
          </CardHeader>
          <CardContent className="space-y-6">
            <SwitchRow
              label="Pause Only When Active"
              description="Only pause if app is focused"
              checked={settings.waylandOnlyActive}
              onCheckedChange={(v) => updateSetting("waylandOnlyActive", v)}
              disabled={isWayland === false}
            />
            <TextareaField
              label="Ignore Application IDs"
              description="Comma-separated list of app IDs to ignore when auto-pausing (e.g., steam, firefox, discord)"
              value={settings.waylandIgnoreAppids}
              onChange={(v) => updateSetting("waylandIgnoreAppids", v)}
              placeholder="dock, bar, launcher..."
              disabled={isWayland === false}
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
