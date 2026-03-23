import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import {
  Home,
  Settings,
  Activity,
  Play,
  Image as ImageIcon,
} from "lucide-react";
import { useAppStore } from "@/store/appStore";

import { Button } from "@/components/ui/button";


// 菜单项配置
const items = [
  { title: "Library", tab: "wallpapers", icon: Home },
  { title: "Performance", tab: "performance", icon: Activity },
  { title: "Settings", tab: "settings", icon: Settings },
] as const;

export function AppSidebar() {
  // 1. 获取当前选中的壁纸
  const selectedWallpaper = useAppStore((state) =>
    state.getSelectedWallpaper(),
  );

  // 2. 处理应用壁纸逻辑
  const handleApply = async () => {
    if (!selectedWallpaper) return;
    const selectedScreen = useAppStore.getState().selectedScreen;
    const screen = selectedScreen === "all" ? undefined : selectedScreen;
    await useAppStore.getState().applyWallpaper(selectedWallpaper.id, screen);
  };

  // 3. 获取 setActiveTab
  const setActiveTab = useAppStore((state) => state.setActiveTab);
  const activeTab = useAppStore((state) => state.activeTab);

  return (
    <Sidebar>
      <SidebarHeader className="p-4 border-b">
        <div className="flex items-center gap-2 font-bold text-xl">
          <ImageIcon className="w-6 h-6 text-pink-500" />
          <span>Wallpaper Engine</span>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Menu</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton
                    onClick={() => setActiveTab(item.tab)}
                    isActive={activeTab === item.tab}
                  >
                    <item.icon />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      {/* 🔥 核心区域：底部详情与应用按钮 */}
      <SidebarFooter className="p-4 border-t bg-sidebar-accent/10">
        {selectedWallpaper ? (
          <div className="flex flex-col gap-3 animate-in slide-in-from-bottom-2">
            {/* 选中的壁纸预览信息 */}
            <div className="space-y-1">
              <div className="font-medium truncate text-sm">
                {selectedWallpaper.title}
              </div>
              <div className="text-xs text-muted-foreground flex justify-between">
                <span>{selectedWallpaper.type}</span>
                <span>{selectedWallpaper.size}</span>
              </div>
            </div>

            {/* 应用按钮 */}
            <Button
              onClick={handleApply}
              className="w-full bg-pink-600 hover:bg-pink-700 text-white shadow-lg"
            >
              <Play className="w-4 h-4 mr-2 fill-current" />
              Apply
            </Button>
          </div>
        ) : (
          <div className="text-sm text-muted-foreground text-center py-2">
            Select a wallpaper to apply
          </div>
        )}
      </SidebarFooter>
    </Sidebar>
  );
}
