import { ReactNode } from "react";

interface LayoutProps {
  navbar: ReactNode;
  sidebar: ReactNode;
  children: ReactNode;
}


export function Layout({ navbar, sidebar, children }: LayoutProps) {
  return (
    <div className="flex flex-col h-screen bg-background text-foreground overflow-hidden">
      {/* 顶部导航 */}
      <div className="h-16 border-b border-border flex-shrink-0 px-4 flex items-center bg-surface z-20">
        {navbar}
      </div>

      {/* 下方主体区域 */}
      <div className="flex flex-1 overflow-hidden min-w-0">
        {/* 左侧主内容：修复核心 - 移除了 flex flex-col 和 h-full */}
        <main className="flex-1 overflow-y-auto p-4 min-w-0 scrollbar-thin relative">
          {children}
        </main>

        {/* 右侧侧边栏 */}
        {sidebar && (
          <aside className="w-80 border-l border-border bg-surface flex-shrink-0 flex flex-col shadow-xl z-10 overflow-y-auto animate-in slide-in-from-right duration-300">
            {sidebar}
          </aside>
        )}
      </div>
    </div>
  );
}
