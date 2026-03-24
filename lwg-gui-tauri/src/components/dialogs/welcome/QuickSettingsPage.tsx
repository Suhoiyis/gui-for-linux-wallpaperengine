import { useState, useEffect } from "react";
import { useAppStore } from "@/store/appStore";
import { SwitchRow, SliderRow } from "@/components/settings/Shared";
import { setAutostart, getAutostartStatus } from "@/api/system";

export function QuickSettingsPage() {
  const settings = useAppStore((s) => s.settings);
  const updateSetting = useAppStore((s) => s.updateSetting);
  
  const [autostart, setAutostartState] = useState(false);
  const [isSettingAutostart, setIsSettingAutostart] = useState(false);

  useEffect(() => {
    async function loadAutostart() {
      try {
        const status = await getAutostartStatus();
        setAutostartState(status);
      } catch (error) {
        console.error("Failed to get autostart status:", error);
      }
    }
    loadAutostart();
  }, []);

  const handleAutostartChange = async (checked: boolean) => {
    setAutostartState(checked);
    setIsSettingAutostart(true);
    try {
      await setAutostart(checked);
    } catch (error) {
      console.error("Failed to set autostart:", error);
      setAutostartState(!checked);
    } finally {
      setIsSettingAutostart(false);
    }
  };

  if (!settings) return null;

  return (
    <div className="flex flex-col justify-center h-full py-2">
      <div className="grid grid-cols-2 gap-x-6 gap-y-4">
        <SwitchRow
            label="Mute Audio"
            description="Mute wallpaper audio"
            checked={settings.muteAudio ?? false}
            onCheckedChange={(val) => updateSetting("muteAudio", val)}
        />

        <SwitchRow
            label="Launch on Startup"
            description="Start on login"
            checked={autostart}
            onCheckedChange={handleAutostartChange}
            disabled={isSettingAutostart}
        />
        
        <SliderRow
            label="Volume"
            value={settings.volume ?? 50}
            onValueChange={(val) => updateSetting("volume", val)}
            min={0}
            max={100}
            suffix="%"
        />

        <SliderRow
            label="FPS Limit"
            value={settings.fps ?? 30}
            onValueChange={(val) => updateSetting("fps", val)}
            min={15}
            max={144}
            suffix="fps"
        />

        <SwitchRow
            label="Auto Restore"
            description="Restore on startup"
            checked={settings.autoRestore ?? true}
            onCheckedChange={(val) => updateSetting("autoRestore", val)}
        />
      </div>
    </div>
  );
}