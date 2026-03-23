import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAppStore } from "@/store/appStore";
import { toast } from "sonner";

interface EditNicknameDialogProps {
  wallpaperId: string;
  wallpaperTitle: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function EditNicknameDialog({
  wallpaperId,
  wallpaperTitle,
  open,
  onOpenChange,
}: EditNicknameDialogProps) {
  const nicknames = useAppStore((state) => state.nicknames);
  const setNickname = useAppStore((state) => state.setNickname);

  const [nicknameInput, setNicknameInput] = useState("");

  // Load current nickname when dialog opens
  useEffect(() => {
    if (open) {
      const currentNickname = nicknames[wallpaperId] || "";
      setNicknameInput(currentNickname);
    }
  }, [open, nicknames, wallpaperId]);

  const handleSave = async () => {
    await setNickname(wallpaperId, nicknameInput);
    toast.success("Nickname updated", {
      description: nicknameInput || `Cleared for ${wallpaperTitle}`,
    });
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Set Wallpaper Nickname</DialogTitle>
          <DialogDescription>
            Give this wallpaper a custom nickname for easier identification.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="nickname">Nickname</Label>
            <Input
              id="nickname"
              value={nicknameInput}
              onChange={(e) => setNicknameInput(e.target.value)}
              placeholder="Enter a nickname..."
              onKeyDown={(e) => {
                if (e.key === "Enter") handleSave();
              }}
            />
            <p className="text-xs text-muted-foreground">
              Leave empty to remove nickname
            </p>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button onClick={handleSave}>Save</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}