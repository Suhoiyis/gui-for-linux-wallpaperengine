import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { isTauriEnv } from "@/lib/utils";
import {
  Menu,
  RefreshCw,
  Rocket,
  Info,
  RotateCcw,
  LogOut,
  History,
  Download,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { AboutDialog } from "@/components/dialogs/AboutDialog";
import { UpdateDialog } from "@/components/dialogs/UpdateDialog";
import { HistoryDialog } from "@/components/dialogs/HistoryDialog";
import { useAppStore } from "@/store/appStore";
import { toast } from "sonner";

interface UpdateInfo {
  latest_version: string;
  download_url: string;
}

export function AppMenu() {
  const loadWallpapers = useAppStore((state) => state.loadWallpapers);
  // const appVersion = useAppStore((state) => state.appVersion);
  const [showAbout, setShowAbout] = useState(false);
  const [showUpdate, setShowUpdate] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [showQuitConfirm, setShowQuitConfirm] = useState(false);
  const [updateInfo, setUpdateInfo] = useState<UpdateInfo | null>(null);
  const [currentVersion, setCurrentVersion] = useState("");

  const handleRefresh = () => {
    loadWallpapers();
    toast.info("Refreshing library...");
  };

  const handleHistory = () => setShowHistory(true);
  const handleGetStarted = () =>
    toast.info("Show Welcome Screen (Coming soon)");

  const handleCheckUpdate = async () => {
    // Guard: Only run in Tauri environment
    if (!isTauriEnv()) {
      toast.error("Update check is only available in the desktop app");
      return;
    }

    const toastId = toast.loading("Checking for updates...");

    try {
      const result = await invoke<{
        has_update: boolean;
        current_version: string;
        latest_version: string | null;
        download_url: string | null;
      }>("check_for_updates");

      toast.dismiss(toastId);

      if (result.has_update) {
        setCurrentVersion(result.current_version);
        setUpdateInfo({
          latest_version: result.latest_version!,
          download_url: result.download_url!,
        });
        setShowUpdate(true);
      } else {
        toast.success(`Already up to date (v${result.current_version})`);
      }
    } catch (err) {
      toast.dismiss(toastId);
      toast.error(`Update check failed: ${err}`);
    }
  };


  const handleRestart = async () => {
    if (!isTauriEnv()) {
      toast.error("Restart is only available in the desktop app");
      return;
    }
    try {
      await invoke("restart_app");
    } catch (err) {
      toast.error(`Restart failed: ${err}`);
    }
  };

  const handleQuitClick = () => {
    setShowQuitConfirm(true);
  };

  const handleConfirmQuit = async () => {
    if (!isTauriEnv()) {
      toast.error("Quit is only available in the desktop app");
      return;
    }
    try {
      await invoke("quit_app");
    } catch (err) {
      toast.error(`Quit failed: ${err}`);
    }
  };

  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8 hover:bg-muted-foreground/10"
          >
            <Menu className="w-4 h-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-56">
          <DropdownMenuLabel>Application</DropdownMenuLabel>
          <DropdownMenuSeparator />

          <DropdownMenuItem onClick={handleRefresh}>
            <RefreshCw className="mr-2 h-4 w-4" /> Refresh Library
          </DropdownMenuItem>

          <DropdownMenuItem onClick={handleHistory}>
            <History className="mr-2 h-4 w-4" /> Play History
          </DropdownMenuItem>

          <DropdownMenuItem onClick={handleGetStarted}>
            <Rocket className="mr-2 h-4 w-4" /> Get Started
          </DropdownMenuItem>

          <DropdownMenuSeparator />

          <DropdownMenuItem onClick={handleCheckUpdate}>
            <Download className="mr-2 h-4 w-4" /> Check for Update
          </DropdownMenuItem>

          <DropdownMenuItem onClick={() => setShowAbout(true)}>
            <Info className="mr-2 h-4 w-4" /> About
          </DropdownMenuItem>

          <DropdownMenuSeparator />

          <DropdownMenuItem onClick={handleRestart}>
            <RotateCcw className="mr-2 h-4 w-4" /> Restart
          </DropdownMenuItem>
          <DropdownMenuItem
            onSelect={(e) => {
              e.preventDefault();
              handleQuitClick();
            }}
            className="text-red-600 focus:text-red-600 focus:bg-red-100 dark:focus:bg-red-900/30"
          >
            <LogOut className="mr-2 h-4 w-4" /> Quit
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Dialogs - placed outside DropdownMenu */}
      <AboutDialog open={showAbout} onOpenChange={setShowAbout} />
      {updateInfo && (
        <UpdateDialog
          open={showUpdate}
          onOpenChange={setShowUpdate}
          currentVersion={currentVersion}
          latestVersion={updateInfo.latest_version}
          downloadUrl={updateInfo.download_url}
        />
      )}
      <HistoryDialog open={showHistory} onOpenChange={setShowHistory} />

      {/* Quit Confirmation Dialog */}
      <AlertDialog open={showQuitConfirm} onOpenChange={setShowQuitConfirm}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Quit Application?</AlertDialogTitle>
            <AlertDialogDescription>
              This will stop all running wallpapers and exit the application.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleConfirmQuit}
              className="bg-red-600 hover:bg-red-700"
            >
              Quit
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
