import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { useAppStore } from "@/store/appStore";
import { SwitchRow, SliderRow } from "@/components/settings/Shared";
import { setAutostart, getAutostartStatus } from "@/api/system";

interface QuickSettingsPageProps {
  onNext: () => void;
  onSkip: () => void;
}

export function QuickSettingsPage({ onNext, onSkip }: QuickSettingsPageProps) {
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
      // Revert if failed
      setAutostartState(!checked);
    } finally {
      setIsSettingAutostart(false);
    }
  };

  if (!settings) return null;

  return (
    <div className="py-4">
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Quick Settings</h2>
        <p className="text-sm text-muted-foreground">
          A few basics to get you started. You can change these later.
        </p>
      </div>

      <div className="space-y-6 mb-8 bg-muted/20 p-4 rounded-xl border border-border/50">
        <SwitchRow
            label="Mute Audio"
            description="Mute wallpaper audio globally"
            checked={settings.muteAudio ?? false}
            onCheckedChange={(val) => updateSetting("muteAudio", val)}
        />
        
        <div className="pt-2">
            <SliderRow
                label="Volume"
                value={settings.volume ?? 50}
                onValueChange={(val) => updateSetting("volume", val)}
                min={0}
                max={100}
                suffix="%"
            />
        </div>

        <div className="pt-2">
            <SliderRow
                label="FPS Limit"
                value={settings.fps ?? 30}
                onValueChange={(val) => updateSetting("fps", val)}
                min={15}
                max={144}
                suffix="fps"
            />
        </div>

        <SwitchRow
            label="Launch on Startup"
            description="Automatically start the app when you log in"
            checked={autostart}
            onCheckedChange={handleAutostartChange}
            disabled={isSettingAutostart}
        />
        
        <SwitchRow
            label="Auto Restore"
            description="Restore previous wallpapers on startup"
            checked={settings.autoRestore ?? true}
            onCheckedChange={(val) => updateSetting("autoRestore", val)}
        />
      </div>

      <div className="flex justify-between">
        <Button variant="ghost" onClick={onSkip}>
            Skip for now
        </Button>
        <Button onClick={onNext}>
            Save & Continue
        </Button>
      </div>
    </div>
  );
}
