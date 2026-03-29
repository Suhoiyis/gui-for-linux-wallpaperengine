import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { useAppStore } from "@/store/appStore";
import { PlaylistItem } from "./PlaylistItem";
import { FavoritesItem } from "./FavoritesItem";
import { Accordion } from "@/components/ui/accordion";

interface PlaylistListProps {
  variant?: "floating" | "locked";
}

export function PlaylistList({ variant = "floating" }: PlaylistListProps) {
  const playlists = useAppStore((state) => state.playlists);
  const reorderPlaylists = useAppStore((state) => state.reorderPlaylists);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8, // Require 8px movement before starting drag
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      const oldIndex = playlists.findIndex((p) => p.id === active.id);
      const newIndex = playlists.findIndex((p) => p.id === over.id);

      // Optimistic update - reorder locally first
      const newOrder = arrayMove(playlists, oldIndex, newIndex);

      // Persist to backend
      reorderPlaylists(newOrder.map((p) => p.id));
    }
  };

  return (
    <Accordion type="multiple" className="space-y-1">
      {/* Favorites - 固定在最上面，不可拖动 */}
      <FavoritesItem variant={variant} />

      {/* 用户创建的播放列表 - 可拖动排序 */}
      {playlists.length > 0 && (
        <DndContext
          sensors={sensors}
          collisionDetection={closestCenter}
          onDragEnd={handleDragEnd}
        >
          <SortableContext
            items={playlists.map((p) => p.id)}
            strategy={verticalListSortingStrategy}
          >
            {playlists.map((playlist) => (
              <PlaylistItem key={playlist.id} playlist={playlist} variant={variant} />
            ))}
          </SortableContext>
        </DndContext>
      )}
    </Accordion>
  );
}