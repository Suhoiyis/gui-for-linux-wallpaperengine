import { useAppStore } from "@/store/appStore";
import { PathInputField } from "@/components/settings/Shared";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { Info } from "lucide-react";

export function DirectoriesPage() {
  const settings = useAppStore((s) => s.settings);
  const updateSetting = useAppStore((s) => s.updateSetting);

  if (!settings) return null;

  return (
    <div className="flex flex-col justify-center h-full py-4">
      <div className="space-y-5">
        <PathInputField
            label={
                <div className="flex flex-col mb-1">
                    <span className="font-medium">Workshop Path (Required)</span>
                    <span className="text-xs text-muted-foreground font-normal">
                        Where Steam downloads Wallpaper Engine content.
                    </span>
                </div>
            }
            value={settings.workshopPath || ""}
            onChange={(val) => updateSetting("workshopPath", val || "")}
            placeholder="/home/user/.steam/steam/steamapps/workshop/content/431960"
        />

        <PathInputField
            label={
                <div className="flex flex-col mb-1">
                    <div className="flex items-center gap-1.5">
                        <span className="font-medium">Assets Path (Optional)</span>
                        <HoverCard>
                            <HoverCardTrigger asChild>
                                <Info className="w-3.5 h-3.5 text-muted-foreground hover:text-foreground cursor-help transition-colors outline-none" />
                            </HoverCardTrigger>
                            <HoverCardContent className="w-fit max-w-[400px] text-sm" side="top">
                                <p className="mb-2 font-medium">Auto-detected paths:</p>
                                <ul className="list-disc pl-4 space-y-1 text-muted-foreground font-mono text-[11px] break-all">
                                    <li>~/.steam/steam/steamapps/common</li>
                                    <li>~/.local/share/Steam/steamapps/common</li>
                                    <li>~/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/common</li>
                                    <li>~/snap/steam/common/.local/share/Steam/steamapps/common</li>
                                </ul>
                            </HoverCardContent>
                        </HoverCard>
                    </div>
                    <span className="text-xs text-muted-foreground font-normal">
                        Where linux-wallpaperengine assets are installed.
                    </span>
                </div>
            }
            value={settings.assetsPath || ""}
            onChange={(val) => updateSetting("assetsPath", val || "")}
            placeholder="Leave empty to auto-detect"
        />
      </div>
    </div>
  );
}