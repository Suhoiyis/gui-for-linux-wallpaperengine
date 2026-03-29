import { Monitor, Volume2, Moon, Sun, Speaker } from "lucide-react";
import { useAppStore } from "@/store/appStore";
import { useTheme } from "@/components/providers/ThemeProvider";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Header, SliderRow, SwitchRow, SwitchCard } from "./Shared";

export function DisplaySettings() {
  const { theme, setTheme } = useTheme();
  const { settings, updateSetting } = useAppStore();

  if (!settings) return <div>Loading...</div>;

  return (
    <div className="space-y-6">
      <Header
        title="Audio & Display"
        desc="Manage audio processing and interface theme."
      />
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 items-start">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Volume2 className="w-4 h-4 text-green-500" /> Audio Control
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Mute Audio */}
            <SwitchRow
              label="Mute Audio"
              description="Mute all audio output and processing"
              checked={settings.muteAudio}
              onCheckedChange={(v) => updateSetting("muteAudio", v)}
              icon={<Speaker className="w-4 h-4 text-muted-foreground" />}
            />

            {/* ✨ 折叠区域：包含音量、分割线以及两个高级音频选项 */}
            {!settings.muteAudio && (
              <div className="space-y-6 pt-2 animate-in fade-in slide-in-from-top-2 duration-300">
                <SliderRow
                  label="Master Volume"
                  value={settings.volume}
                  onValueChange={(v) => updateSetting("volume", v)}
                  max={100}
                  step={1}
                  suffix="%"
                />

                <Separator />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <SwitchCard
                    label="Disable Auto Mute"
                    description="Prevent muting when other apps play sound"
                    checked={settings.noAutomute}
                    onCheckedChange={(v) => updateSetting("noAutomute", v)}
                  />
                  <SwitchCard
                    label="No Audio Processing"
                    description="Disable spectrum analysis for performance"
                    checked={settings.noAudioProcessing}
                    onCheckedChange={(v) =>
                      updateSetting("noAudioProcessing", v)
                    }
                  />
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              {theme === "dark" ? (
                <Moon className="w-4 h-4" />
              ) : (
                <Sun className="w-4 h-4" />
              )}{" "}
              Interface Theme
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between space-x-4">
              <div className="flex flex-col space-y-1">
                <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                  App Appearance
                </label>
                <p className="text-xs text-muted-foreground">
                  Light or Dark mode
                </p>
              </div>

              {/* ✨ 替换后的丝滑三向切换开关 */}
              <div className="relative grid grid-cols-3 w-[260px] items-center rounded-xl bg-muted/50 p-1 border border-border/50">
                {/* ✨ 核心：滑动的背景高亮块 */}
                <div
                  className="absolute left-1 top-1 bottom-1 w-[calc((100%-8px)/3)] rounded-lg bg-background shadow-sm border border-border/50 transition-transform duration-300 ease-out"
                  style={{
                    transform: `translateX(${
                      theme === "system"
                        ? "0"
                        : theme === "dark"
                          ? "100%"
                          : "200%"
                    })`,
                  }}
                />

                {/* 三个选项按钮 */}
                {(["system", "dark", "light"] as const).map((t) => (
                  <button
                    key={t}
                    onClick={() => setTheme(t)}
                    className={`relative z-10 py-1.5 text-xs font-medium capitalize transition-colors flex items-center justify-center gap-1.5 ${
                      theme === t
                        ? "text-foreground"
                        : "text-muted-foreground hover:text-foreground"
                    }`}
                  >
                    {t === "system" && <Monitor className="w-3.5 h-3.5" />}
                    {t === "dark" && <Moon className="w-3.5 h-3.5" />}
                    {t === "light" && <Sun className="w-3.5 h-3.5" />}
                    {t}
                  </button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
