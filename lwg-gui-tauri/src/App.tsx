import { useEffect } from "react";

import { motion, AnimatePresence } from "framer-motion";
import { listen } from "@tauri-apps/api/event";
import { toast } from "sonner";

// Shadcn UI 组件
import { Tabs } from "@/components/ui/tabs";
import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";

// 项目自定义组件
import { Layout } from "./components/layout/Layout";
import { AppNavbar } from "./components/layout/AppNavbar";
import { CommandPalette } from "./components/layout/CommandPalette";

// 页面组件
import { Library } from "./pages/Library";
import { Settings } from "./pages/Settings";
import { Performance } from "./pages/Performance";
import { CompactMode } from "./pages/Compact";

import { useAppStore } from "./store/appStore";

// 页面切换动画配置
const pageVariants = {
  initial: { opacity: 0, y: 10, scale: 0.99 },
  in: { opacity: 1, y: 0, scale: 1 },
  out: { opacity: 0, y: -10, scale: 0.99 },
};

const pageTransition = {
  type: "tween",
  ease: "circOut",
  duration: 0.25,
} as const;

export function App() {
  const activeTab = useAppStore((state) => state.activeTab);
  const setActiveTab = useAppStore((state) => state.setActiveTab);

  const isCompactMode = useAppStore((s) => s.isCompactMode);
  const toggleCompactMode = useAppStore((s) => s.toggleCompactMode);

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      const THRESHOLD = 500;
      if (width < THRESHOLD && !isCompactMode) {
        // 只有当不是 Compact Mode 时才切换，避免死循环
        toggleCompactMode(true);
      } else if (width >= THRESHOLD && isCompactMode) {
        // 只有当是 Compact Mode 时才切换回大窗
        toggleCompactMode(false);
      }
    };
    // 初始化时先检查一次
    handleResize();

    // 监听窗口变化
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [isCompactMode, toggleCompactMode]); // 依赖项

  // 初始化应用
  useEffect(() => {
    useAppStore.getState().initApp();
  }, []);

  // 监听 Tauri System Tray 事件和壁纸轮换事件
  useEffect(() => {
    // 挂载状态锁 - 防止异步操作完成时组件已卸载
    let mounted = true;
    let unlistenRandom: (() => void) | undefined;
    let unlistenStop: (() => void) | undefined;
    let unlistenApplyLast: (() => void) | undefined;
    let unlistenQuit: (() => void) | undefined;
    let unlistenWallpaperCycled: (() => void) | undefined;

    const setupListeners = async () => {
      const unlisten1 = await listen("tray-random-wallpaper", () => {
        useAppStore.getState().applyRandomWallpaper();
      });

      if (!mounted) {
        unlisten1();
        return;
      }
      unlistenRandom = unlisten1;

      const unlisten2 = await listen("tray-stop-wallpaper", () => {
        useAppStore.getState().stopWallpaper();
      });

      if (!mounted) {
        unlisten2();
        unlistenRandom?.();
        return;
      }
      unlistenStop = unlisten2;

      const unlisten3 = await listen("tray-apply-last", () => {
        const state = useAppStore.getState();
        const activeMonitors = state.runtimeState || {};
        for (const [screen, aw] of Object.entries(activeMonitors)) {
          if (aw.wallpaperId) {
            state.applyWallpaper(aw.wallpaperId, screen);
          }
        }
      });

      if (!mounted) {
        unlisten3();
        unlistenRandom?.();
        unlistenStop?.();
        return;
      }
      unlistenApplyLast = unlisten3;

      const unlisten4 = await listen("tray-quit-request", () => {
        // Import invoke dynamically to avoid circular dependency
        import("@tauri-apps/api/core").then(({ invoke }) => {
          invoke("quit_app");
        });
      });

      if (!mounted) {
        unlisten4();
        unlistenRandom?.();
        unlistenStop?.();
        unlistenApplyLast?.();
        return;
      }
      unlistenQuit = unlisten4;

      // 监听壁纸轮换完成事件
      const unlisten5 = await listen<string>("wallpaper-cycled", (event) => {
        const wallpaperId = event.payload;
        console.log("[App] Wallpaper cycled:", wallpaperId);
        useAppStore.getState().getState();
        
        // 发送系统通知和应用内 toast
        const store = useAppStore.getState();
        const wallpaper = store.wallpapers.find(w => w.id === wallpaperId);
        if (wallpaper) {
          // 优先显示 nickname，否则显示原标题
          const displayName = store.getNickname(wallpaperId) || wallpaper.title;
          // 应用内 toast
          toast.success("Wallpaper Changed", { description: displayName });
          // 系统通知
          import("@/api/system").then(({ notify }) => {
            notify("Wallpaper Changed", displayName);
          });
        }
      });

      if (!mounted) {
        unlisten5();
        unlistenRandom?.();
        unlistenStop?.();
        unlistenApplyLast?.();
        unlistenQuit?.();
        return;
      }
      unlistenWallpaperCycled = unlisten5;
    };

    setupListeners();

    return () => {
      mounted = false;
      unlistenRandom?.();
      unlistenStop?.();
      unlistenApplyLast?.();
      unlistenQuit?.();
      unlistenWallpaperCycled?.();
    };
  }, []);



  // --- 渲染逻辑 ---

  // 1. 如果是 Compact Mode
  if (isCompactMode) {
    return (
      // ✨ 2. 包裹 TooltipProvider
      <TooltipProvider delayDuration={300}>
        <motion.div
          key="compact"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="h-screen w-screen bg-background"
        >
          <CompactMode />
          <Toaster />
        </motion.div>
        {/* CommandPalette rendered once outside conditional to prevent remounting */}
        <CommandPalette />
      </TooltipProvider>
    );
  }

  // 2. 正常大窗口模式
  return (
    // ✨ 2. 包裹 TooltipProvider (这里的 <> 也可以删掉直接包 Provider)
    <TooltipProvider delayDuration={300}>
      <Tabs
        value={activeTab}
        onValueChange={(value) =>
          setActiveTab(value as "wallpapers" | "settings" | "performance")
        }
      >
        <Layout navbar={<AppNavbar />} sidebar={null}>
          <AnimatePresence mode="wait">
            {activeTab === "wallpapers" && (
              <motion.div
                key="wallpapers"
                initial="initial"
                animate="in"
                exit="out"
                variants={pageVariants}
                transition={pageTransition}
                className="h-full"
              >
                <Library />
              </motion.div>
            )}

            {activeTab === "settings" && (
              <motion.div
                key="settings"
                initial="initial"
                animate="in"
                exit="out"
                variants={pageVariants}
                transition={pageTransition}
                className="h-full"
              >
                <Settings />
              </motion.div>
            )}

            {activeTab === "performance" && (
              <motion.div
                key="performance"
                initial="initial"
                animate="in"
                exit="out"
                variants={pageVariants}
                transition={pageTransition}
                className="h-full"
              >
                <Performance />
              </motion.div>
            )}
          </AnimatePresence>
        </Layout>
      </Tabs>
      <Toaster />
      {/* CommandPalette rendered once outside conditional to prevent remounting */}
      <CommandPalette />
    </TooltipProvider>
  );
}