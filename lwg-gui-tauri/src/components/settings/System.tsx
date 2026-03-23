// src/components/settings/System.tsx
import { useState, useEffect, useCallback } from "react";
import { isTauriEnv } from "@/lib/utils";
import { invoke } from "@tauri-apps/api/core";
import { useAppStore } from "@/store/appStore";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import {
  Power,
  EyeOff,
  FileImage,
  FolderOpen,
  AlertTriangle,
  Info,
  Database,
  Star,
} from "lucide-react";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import {
  Header,
  SwitchRow,
  PathInputField,
  EditableComboboxField,
  RESOLUTION_OPTIONS,
} from "./Shared";
import { NicknameManagerDialog } from "@/components/dialogs/NicknameManagerDialog";
import { FavoriteManagerDialog } from "@/components/dialogs/FavoriteManagerDialog";
import { Button } from "@/components/ui/button";
import { setAutostart, getAutostartStatus } from "@/api/system";

export function SystemSettings() {
  const { settings, updateSetting, highlightSettingField } = useAppStore();
  const [autostart, setAutostartState] = useState(false);
  const [hasXvfb, setHasXvfb] = useState<boolean | null>(null);
  const [nicknameDialogOpen, setNicknameDialogOpen] = useState(false);
  const [favoriteDialogOpen, setFavoriteDialogOpen] = useState(false);

  useEffect(() => {
    getAutostartStatus()
      .then(setAutostartState)
      .catch(() => {});
  }, []);

  useEffect(() => {
    // 检测 Xvfb 是否安装
    const isTauri = isTauriEnv();
    if (isTauri) {
      invoke<boolean>("check_xvfb_available")
        .then((available) => {
          setHasXvfb(available);
          // 如果没有安装 Xvfb，清除配置
          if (!available && settings?.preferXvfb) {
            updateSetting("preferXvfb", false);
          }
        })
        .catch(() => setHasXvfb(false));
    } else {
      setHasXvfb(false);
    }
  }, [settings, updateSetting]);

  const handleAutostartChange = useCallback(
    async (enabled: boolean) => {
      try {
        await setAutostart(enabled);
        setAutostartState(enabled);
        toast.success(enabled ? "Autostart enabled" : "Autostart disabled");
      } catch {
        toast.error("Failed to change autostart");
      }
    },
    [],
  );

  // ✨ Scroll highlighted field into view
  useEffect(() => {
    if (highlightSettingField === "workshopPath") {
      // Small delay to ensure DOM is ready
      const timer = setTimeout(() => {
        const inputElement = document.querySelector(
          'input[value*="workshopPath"], input[placeholder*="Steam"]',
        );
        if (inputElement) {
          inputElement.scrollIntoView({ behavior: "smooth", block: "center" });
        }
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [highlightSettingField]);
  if (!settings) return <div>Loading...</div>;

  return (
    <div className="space-y-6">
      {/* Header 保持在最上面，跨越整行 */}
      <Header
        title="System & Tools"
        desc="Manage directories and screenshot utilities."
      />

      {/* ✨ 新增：响应式网格容器 */}
      {/* 在窄屏(默认)下单列，在宽屏(xl/1280px以上)下变为双列 */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 items-start">
        {/* Directories Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FolderOpen className="w-4 h-4 text-yellow-500" /> Directories
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <PathInputField
              label="Steam Workshop Path"
              value={settings.workshopPath || ""}
              onChange={(v) => updateSetting("workshopPath", v)}
              placeholder="/home/user/.local/share/Steam/steamapps/workshop/content/431960"
              className={
                highlightSettingField === "workshopPath"
                  ? "ring-2 ring-primary animate-pulse"
                  : ""
              }
            />
            <PathInputField
              label={
                <div className="flex items-center gap-1.5">
                  Assets Directory
                  <HoverCard>
                    <HoverCardTrigger asChild>
                      <Info className="w-4 h-4 text-muted-foreground hover:text-foreground cursor-help transition-colors outline-none" />
                    </HoverCardTrigger>
                    {/* 设置 max-w-fit 并且给稍微宽一点的尺寸，确保路径能在一行内尽量展示 */}
                    <HoverCardContent
                      className="w-fit max-w-[450px] text-sm"
                      side="top"
                    >
                      <p className="mb-2 font-medium">Auto-detected paths:</p>
                      <ul className="list-disc pl-4 space-y-1 text-muted-foreground font-mono text-[11px] break-all">
                        <li>~/.steam/steam/steamapps/common</li>
                        <li>~/.local/share/Steam/steamapps/common</li>
                        <li>
                          ~/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/common
                        </li>
                        <li>
                          ~/snap/steam/common/.local/share/Steam/steamapps/common
                        </li>
                      </ul>
                    </HoverCardContent>
                  </HoverCard>
                </div>
              }
              value={settings.assetsPath || ""}
              onChange={(v) => updateSetting("assetsPath", v)}
              placeholder="Leave empty to auto-detect"
            />
          </CardContent>
        </Card>

        {/* Startup & Integration Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Power className="w-4 h-4 text-red-500" /> Startup & Integration
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <SwitchRow
              label="Run on Startup"
              description="Launch automatically on login"
              checked={autostart}
              onCheckedChange={handleAutostartChange}
            />

            <SwitchRow
              label="Start Hidden"
              description="Minimize to tray on launch"
              checked={settings.startHidden ?? false}
              onCheckedChange={(v) => updateSetting("startHidden", v)}
              icon={<EyeOff className="w-4 h-4 text-muted-foreground" />}
            />

            <SwitchRow
              label="Auto Restore"
              description="Restore last wallpapers on launch"
              checked={settings.autoRestore ?? false}
              onCheckedChange={(v) => updateSetting("autoRestore", v)}
            />
          </CardContent>
        </Card>

        {/* Screenshot Tools Card */}
        <Card
          className={
            hasXvfb === true
              ? "border-pink-500/20"
              : "border-amber-500/20 bg-amber-500/5"
          }
        >
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span className="flex items-center gap-2">
                <FileImage className="w-4 h-4 text-pink-500" /> Screenshot Tools
              </span>
              <Badge
                variant="outline"
                className={
                  "text-xs font-normal " +
                  (hasXvfb === true
                    ? "border-green-500/30 text-green-500"
                    : "border-amber-500/30 text-amber-500")
                }
              >
                {hasXvfb === null
                  ? "Checking..."
                  : hasXvfb
                    ? "Xvfb Installed"
                    : "Xvfb Not Found"}
              </Badge>
            </CardTitle>
            {hasXvfb === false && (
              <p className="text-xs text-amber-600 flex items-center gap-1">
                <AlertTriangle className="w-3 h-3" />
                Install xvfb-run for silent background capture.
              </p>
            )}
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Target Resolution */}
            <div className="max-w-md">
              <EditableComboboxField
                label="Target Resolution"
                value={settings.screenshotRes}
                onChange={(v) => updateSetting("screenshotRes", v)}
                options={RESOLUTION_OPTIONS}
                placeholder="Select or type..."
              />
            </div>

            <Separator />

            <SwitchRow
              label="Prefer Silent Capture (Xvfb)"
              description="Capture in background without visible window"
              checked={settings.preferXvfb}
              onCheckedChange={(v) => updateSetting("preferXvfb", v)}
              disabled={hasXvfb === false}
            />
          </CardContent>
        </Card>

        {/* Wallpaper Data Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Database className="w-4 h-4 text-brand" /> Wallpaper Data
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Nicknames */}
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <p className="text-sm font-medium">Nicknames</p>
                <p className="text-xs text-muted-foreground">
                  Custom names for your wallpapers.
                </p>
              </div>
              <Button variant="outline" onClick={() => setNicknameDialogOpen(true)}>
                Manage
              </Button>
            </div>

            <Separator />

            {/* Favorites */}
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <p className="text-sm font-medium flex items-center gap-1.5">
                  <Star className="w-3.5 h-3.5 text-yellow-500" /> Favorites
                </p>
                <p className="text-xs text-muted-foreground">
                  Your starred wallpapers.
                </p>
              </div>
              <Button variant="outline" onClick={() => setFavoriteDialogOpen(true)}>
                Manage
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Nickname Manager Dialog */}
      <NicknameManagerDialog
        open={nicknameDialogOpen}
        onOpenChange={setNicknameDialogOpen}
      />

      {/* Favorite Manager Dialog */}
      <FavoriteManagerDialog
        open={favoriteDialogOpen}
        onOpenChange={setFavoriteDialogOpen}
      />
    </div>
  );
}
