import * as ContextMenu from "@radix-ui/react-context-menu";
import { ReactNode } from "react";
import { FolderOpen, Trash2, Info, Play, ListPlus } from "lucide-react";
import { AddToPlaylistMenu } from "@/components/playlist/AddToPlaylistMenu";

interface Props {
  children: ReactNode;
  wallpaperId: string;
  onOpenFolder?: () => void;
  onDelete?: () => void;
  onProperties?: () => void;
}

export function WallpaperContextMenu({
  children,
  wallpaperId,
  onOpenFolder,
  onDelete,
  onProperties,
}: Props) {
  return (
    <ContextMenu.Root>
      <ContextMenu.Trigger asChild>{children}</ContextMenu.Trigger>

      <ContextMenu.Portal>
        <ContextMenu.Content className="min-w-[180px] bg-popover rounded-lg border border-border p-1.5 shadow-xl animate-in fade-in duration-200 z-50">
          <Item
            onClick={onOpenFolder}
            icon={<Play size={14} />}
            label="Apply Wallpaper"
          />
          <ContextMenu.Separator className="h-px bg-border my-1" />

          <Item
            onClick={onOpenFolder}
            icon={<FolderOpen size={14} />}
            label="Open in Explorer"
          />
          <Item
            onClick={onProperties}
            icon={<Info size={14} />}
            label="Properties"
          />

          <ContextMenu.Separator className="h-px bg-border my-1" />
          
          {/* Add to playlist submenu */}
          <ContextMenu.Sub>
            <ContextMenu.SubTrigger className="flex items-center gap-2 px-2 py-1.5 rounded text-sm outline-none cursor-pointer select-none data-[state=open]:bg-accent data-[highlighted]:bg-accent">
              <ListPlus size={14} />
              <span>Add to playlist</span>
            </ContextMenu.SubTrigger>
            <ContextMenu.Portal>
              <ContextMenu.SubContent className="min-w-[160px] bg-popover rounded-lg border border-border p-1.5 shadow-xl animate-in fade-in duration-200 z-50">
                <AddToPlaylistMenu wallpaperId={wallpaperId}>
                  <span className="hidden">trigger</span>
                </AddToPlaylistMenu>
              </ContextMenu.SubContent>
            </ContextMenu.Portal>
          </ContextMenu.Sub>

          <ContextMenu.Separator className="h-px bg-border my-1" />
          <Item
            onClick={onDelete}
            icon={<Trash2 size={14} />}
            label="Delete"
            destructive
          />
        </ContextMenu.Content>
      </ContextMenu.Portal>
    </ContextMenu.Root>
  );
}

// 辅助组件：菜单项
function Item({ icon, label, onClick, destructive }: any) {
  return (
    <ContextMenu.Item
      className={`
        flex items-center gap-2 px-2 py-1.5 rounded text-sm outline-none cursor-pointer select-none
        data-[highlighted]:bg-accent 
        ${destructive ? "text-red-400 data-[highlighted]:text-red-300" : "text-popover-foreground"}
      `}
      onClick={onClick}
    >
      {icon}
      <span>{label}</span>
    </ContextMenu.Item>
  );
}
