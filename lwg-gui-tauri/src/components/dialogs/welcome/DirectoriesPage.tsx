import { Button } from "@/components/ui/button";
import { useAppStore } from "@/store/appStore";
import { PathInputField } from "@/components/settings/Shared";

interface DirectoriesPageProps {
  onNext: () => void;
  onSkip: () => void;
}

export function DirectoriesPage({ onNext, onSkip }: DirectoriesPageProps) {
  const settings = useAppStore((s) => s.settings);
  const updateSetting = useAppStore((s) => s.updateSetting);

  if (!settings) return null;

  const handleNext = () => {
    onNext();
  };

  return (
    <div className="py-4">
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Directories</h2>
        <p className="text-sm text-muted-foreground">
          Set up the paths where your Wallpapers and Assets are located.
        </p>
      </div>

      <div className="space-y-6 mb-8">
        <div className="space-y-2">
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
        </div>

        <div className="space-y-2">
            <PathInputField
                label={
                    <div className="flex flex-col mb-1">
                        <span className="font-medium">Assets Path (Optional)</span>
                        <span className="text-xs text-muted-foreground font-normal">
                            Where linux-wallpaperengine assets are installed (usually /usr/share/linux-wallpaperengine/assets).
                        </span>
                    </div>
                }
                value={settings.assetsPath || ""}
                onChange={(val) => updateSetting("assetsPath", val || "")}
                placeholder="/usr/share/linux-wallpaperengine/assets"
            />
        </div>
      </div>

      <div className="flex justify-between">
        <Button variant="ghost" onClick={onSkip}>
            Skip for now
        </Button>
        <Button onClick={handleNext}>
            Next
        </Button>
      </div>
    </div>
  );
}
