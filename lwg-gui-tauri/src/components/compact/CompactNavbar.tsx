import { Maximize2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { AppMenu } from "@/components/layout/AppMenu";
import { ScreenSelector } from "@/components/layout/ScreenSelector";

interface CompactNavbarProps {
  /** 切换到正常窗口模式的回调 */
  onSwitchToNormal: () => void;
}

/**
 * Compact 模式顶部导航栏组件
 * 包含：返回正常窗口按钮、屏幕选择器、应用菜单
 */
export function CompactNavbar({ onSwitchToNormal }: CompactNavbarProps) {
  return (
    <div className="flex items-center justify-between p-2 border-b bg-muted/20 drag-region">
      <Button
        variant="ghost"
        size="icon"
        className="h-8 w-8 no-drag"
        onClick={onSwitchToNormal}
      >
        <Maximize2 className="h-4 w-4" />
      </Button>

      <div className="no-drag">
        <ScreenSelector variant="compact" />
      </div>

      <div className="no-drag">
        <AppMenu />
      </div>
    </div>
  );
}
