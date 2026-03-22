import { cva, type VariantProps } from "class-variance-authority";
import { Ghost, Settings, ListPlus, Search, Star } from "lucide-react";

import { cn } from "@/lib/utils";
import { useAppStore } from "@/store/appStore";
import { Button } from "@/components/ui/button";

function Empty({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="empty"
      className={cn(
        "flex min-w-0 flex-1 flex-col items-center justify-center gap-6 text-balance rounded-lg border-dashed p-6 text-center md:p-12",
        className,
      )}
      {...props}
    />
  );
}

function EmptyHeader({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="empty-header"
      className={cn(
        "flex max-w-sm flex-col items-center gap-2 text-center",
        className,
      )}
      {...props}
    />
  );
}

const emptyMediaVariants = cva(
  "mb-2 flex shrink-0 items-center justify-center [&_svg]:pointer-events-none [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-transparent",
        icon: "bg-muted text-foreground flex size-10 shrink-0 items-center justify-center rounded-lg [&_svg:not([class*='size-'])]:size-6",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
);

function EmptyMedia({
  className,
  variant = "default",
  ...props
}: React.ComponentProps<"div"> & VariantProps<typeof emptyMediaVariants>) {
  return (
    <div
      data-slot="empty-icon"
      data-variant={variant}
      className={cn(emptyMediaVariants({ variant, className }))}
      {...props}
    />
  );
}

function EmptyTitle({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="empty-title"
      className={cn("text-lg font-medium tracking-tight text-foreground", className)}
      {...props}
    />
  );
}

function EmptyDescription({ className, ...props }: React.ComponentProps<"p">) {
  return (
    <div
      data-slot="empty-description"
      className={cn(
        "text-muted-foreground [&>a:hover]:text-primary text-sm/relaxed [&>a]:underline [&>a]:underline-offset-4",
        className,
      )}
      {...props}
    />
  );
}

function EmptyContent({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="empty-content"
      className={cn(
        "flex w-full min-w-0 max-w-sm flex-col items-center gap-4 text-balance text-sm",
        className,
      )}
      {...props}
    />
  );
}

export {
  Empty,
  EmptyHeader,
  EmptyTitle,
  EmptyDescription,
  EmptyContent,
  EmptyMedia,
};

/**
 * EmptyState - All Wallpapers 场景，空库时显示
 */
export function EmptyState() {
  const workshopPath = useAppStore((state) => state.settings?.workshopPath);
  const setActiveTab = useAppStore((state) => state.setActiveTab);
  const setHighlightSettingField = useAppStore(
    (state) => state.setHighlightSettingField,
  );

  const handleConfigurePath = () => {
    setActiveTab("settings");
    setHighlightSettingField("workshopPath");
  };

  return (
    <Empty>
      <EmptyMedia>
        <Ghost className="size-12 text-muted-foreground/50" />
      </EmptyMedia>
      <EmptyHeader>
        <EmptyTitle>No Wallpapers Found</EmptyTitle>
        <EmptyDescription>
          The wallpaper library appears to be empty.
        </EmptyDescription>
      </EmptyHeader>
      <EmptyContent>
        {/* Display current path */}
        <div className="text-sm text-muted-foreground space-y-2">
          <span className="font-medium">Current Library Path:</span>
          <code className="block px-3 py-2 bg-muted rounded text-xs break-all">
            {workshopPath || "Not configured"}
          </code>
        </div>

        {/* Configure button */}
        <Button
          onClick={handleConfigurePath}
          size="sm"
          className="bg-brand text-brand-foreground hover:bg-brand/90"
        >
          <Settings className="w-4 h-4 mr-2" />
          Configure Library Path
        </Button>
      </EmptyContent>
    </Empty>
  );
}

/**
 * PlaylistEmptyState - 播放列表为空时显示
 */
export function PlaylistEmptyState({ playlistName }: { playlistName?: string }) {
  const enterSelectionMode = useAppStore((state) => state.enterSelectionMode);
  const setActivePlaylist = useAppStore((state) => state.setActivePlaylist);

  const handleAddWallpapers = () => {
    // 先切换到 All Wallpapers，再进入选择模式
    setActivePlaylist(null);
    enterSelectionMode();
  };

  return (
    <Empty>
      <EmptyMedia>
        <ListPlus className="size-12 text-muted-foreground/50" />
      </EmptyMedia>
      <EmptyHeader>
        <EmptyTitle>This Playlist is Empty</EmptyTitle>
        <EmptyDescription>
          {playlistName 
            ? `"${playlistName}" doesn't have any wallpapers yet.`
            : "This playlist doesn't have any wallpapers yet."}
        </EmptyDescription>
      </EmptyHeader>
      <EmptyContent>
        {/* Instructions */}
        <div className="text-sm text-muted-foreground space-y-1.5 text-left">
          <p className="font-medium text-foreground">Add wallpapers by:</p>
          <ol className="list-decimal list-inside space-y-1">
            <li>Click the button below to browse all wallpapers</li>
            <li>Select wallpapers you want to add</li>
            <li>Click "Add to Playlist" in the toolbar</li>
          </ol>
        </div>

        {/* Browse & Add button */}
        <Button
          onClick={handleAddWallpapers}
          size="sm"
          className="bg-brand text-brand-foreground hover:bg-brand/90"
        >
          <ListPlus className="w-4 h-4 mr-2" />
          Browse & Add Wallpapers
        </Button>
      </EmptyContent>
    </Empty>
  );
}

/**
 * SearchEmptyState - 搜索无结果时显示
 */
export function SearchEmptyState({ query }: { query: string }) {
  return (
    <Empty>
      <EmptyMedia>
        <Search className="size-12 text-muted-foreground/50" />
      </EmptyMedia>
      <EmptyHeader>
        <EmptyTitle>No Results Found</EmptyTitle>
        <EmptyDescription>
          No wallpapers match your search.
        </EmptyDescription>
      </EmptyHeader>
      <EmptyContent>
        {/* Search query display */}
        <div className="text-sm text-muted-foreground space-y-2">
          <span className="font-medium">Search query:</span>
          <code className="block px-3 py-2 bg-muted rounded text-xs break-all">
            "{query}"
          </code>
        </div>

        {/* Tips */}
        <div className="text-xs text-muted-foreground text-left space-y-1">
          <p className="font-medium">Tips:</p>
          <ul className="list-disc list-inside space-y-0.5">
            <li>Try different keywords</li>
            <li>Check your spelling</li>
            <li>Use fewer or more general terms</li>
          </ul>
        </div>
      </EmptyContent>
    </Empty>
  );
}

/**
 * FavoritesEmptyState - 收藏列表为空时显示
 */
export function FavoritesEmptyState() {
  const setActivePlaylist = useAppStore((state) => state.setActivePlaylist);

  const handleBrowseWallpapers = () => {
    setActivePlaylist(null);
  };

  return (
    <Empty>
      <EmptyMedia>
        <Star className="size-12 text-muted-foreground/50" />
      </EmptyMedia>
      <EmptyHeader>
        <EmptyTitle>No Favorites Yet</EmptyTitle>
        <EmptyDescription>
          You haven't added any wallpapers to your favorites.
        </EmptyDescription>
      </EmptyHeader>
      <EmptyContent>
        {/* Instructions */}
        <div className="text-sm text-muted-foreground space-y-1.5 text-left">
          <p className="font-medium text-foreground">Add favorites by:</p>
          <ol className="list-decimal list-inside space-y-1">
            <li>Browse wallpapers in the library</li>
            <li>Click the star icon on any wallpaper</li>
            <li>Find them here in your favorites</li>
          </ol>
        </div>

        {/* Browse button */}
        <Button
          onClick={handleBrowseWallpapers}
          size="sm"
          className="bg-brand text-brand-foreground hover:bg-brand/90"
        >
          <Star className="w-4 h-4 mr-2" />
          Browse Wallpapers
        </Button>
      </EmptyContent>
    </Empty>
  );
}