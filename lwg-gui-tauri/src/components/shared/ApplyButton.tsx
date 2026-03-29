import { Play } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAppStore } from "@/store/appStore";

interface ApplyButtonProps {
  className?: string;
  size?: "default" | "sm" | "lg" | "icon";
}

export function ApplyButton({ className, size = "default" }: ApplyButtonProps) {
  const selectedWallpaper = useAppStore((state) => state.getSelectedWallpaper());

  const handleApply = async () => {
    if (!selectedWallpaper) return;
    const selectedScreen = useAppStore.getState().selectedScreen;
    const screen = selectedScreen === "all" ? undefined : selectedScreen;
    await useAppStore.getState().applyWallpaper(selectedWallpaper.id, screen);
  };

  return (
    <Button
      onClick={handleApply}
      disabled={!selectedWallpaper}
      size={size}
      className={className}
    >
      <Play className="w-5 h-5 fill-current" /> Apply Wallpaper
    </Button>
  );
}