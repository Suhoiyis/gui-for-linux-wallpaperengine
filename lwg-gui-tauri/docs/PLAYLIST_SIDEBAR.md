# Playlist Sidebar 架构文档

## 概述

Playlist Sidebar 是一个三状态侧栏组件，支持最小化、悬浮、锁定三种模式，在不同模式下提供不同的交互体验。

## 三种模式

### 1. 最小化模式 (Minimized) - 48px

```
┌────────┐
│   ◀    │  ← 展开/收起切换按钮
├────────┤
│   ♫    │  ← All Wallpapers
│   ★    │  ← Favorites
│   A    │  ← Playlist avatar
│   B    │
│   +    │  ← New Playlist
└────────┘
   48px
```

**特点：**
- 仅显示图标列
- 独立 `ScrollArea`
- 点击 `▶` 打开悬浮模式

### 2. 悬浮模式 (Floating) - 220px

```
┌─────────────────────────────┐
│  Playlists        📌 ✕     │  ← Header
├─────────────────────────────┤
│  ♫ All Wallpapers           │
│  ─────────────────────────  │  ← Separator
│  ★ Favorites           5    │  ← 可展开缩略图
│  A Playlist 1          3    │
│  B Playlist 2          7    │  ← 可拖拽排序
├─────────────────────────────┤
│  + New Playlist             │  ← Footer
└─────────────────────────────┘
          220px
```

**特点：**
- 独立浮层，覆盖在内容上方
- 鼠标离开后 500ms 自动关闭
- 使用 `PlaylistList` 原始布局
- **不需要与图标列对齐**（单列结构，无漂移问题）

### 3. 锁定模式 (Locked) - 268px (48px + 220px)

```
┌────────┬─────────────────────────┐
│   ◀    │  Playlists      📌 ✕   │  ← Header (跨两列)
├────────┼─────────────────────────┤
│   ♫    │  ♫ All Wallpapers      │  ← 同一行：图标 + 文字
│   ─    │  ─────────────────────  │  ← Separator 对齐
│   ★    │  ★ Favorites       5   │  ← 可展开缩略图
│   A    │  A Playlist 1      3   │  ← 可拖拽排序
│   B    │  B Playlist 2      7   │
├────────┼─────────────────────────┤
│   +    │  + New Playlist        │  ← Footer (跨两列)
└────────┴─────────────────────────┘
  48px          220px
```

**特点：**
- 固定停靠，推开内容区域
- **单一 ScrollArea** - 每行同时渲染图标和文字
- 完整功能：拖拽排序、Accordion、缩略图、重命名/删除
- 图标和文字永远对齐

---

## 核心问题：为什么锁定模式需要特殊处理？

### 问题根源

最初实现中，锁定模式使用两个独立的 `ScrollArea`：

```
┌──────────────┐  ┌─────────────────┐
│ ScrollArea A │  │  ScrollArea B   │  ← 两个独立滚动容器
│  icon list   │  │   text list     │
└──────────────┘  └─────────────────┘
```

**问题：** 两个 `ScrollArea` 是完全独立的滚动容器，它们的内部高度计算由各自的内容决定。只要 item 高度差 1px，乘以 N 条后就会累积漂移。

### 解决方案

使用**单一 ScrollArea**，每一行同时包含图标和文字：

```tsx
<div className="flex items-center">
  {/* 左侧图标槽 - 固定 48px */}
  <div className="w-12 shrink-0 flex items-center justify-center">
    {/* Icon */}
  </div>
  {/* 右侧内容槽 - flex-1 */}
  <div className="flex-1 pr-2">
    {/* Text + Accordion + Thumbnails */}
  </div>
</div>
```

**结果：** 图标和文字在同一行 DOM 节点中，永远不会错位。

---

## 组件结构

```
PlaylistSidebar.tsx
├── IconColumn              # 最小化模式专用
│   ├── Header (切换按钮)
│   ├── ScrollArea (图标列表)
│   └── Footer (新建按钮)
│
├── LockedSidebarLayout     # 锁定模式专用
│   ├── Header (跨两列)
│   ├── ScrollArea
│   │   ├── All Wallpapers 行
│   │   ├── Separator 行
│   │   └── PlaylistList variant="locked"
│   │       ├── FavoritesItem variant="locked"
│   │       └── PlaylistItem variant="locked" (带拖拽)
│   └── Footer (跨两列)
│
└── ExpandedSidebarContent  # 悬浮模式专用
    ├── Header
    ├── ScrollArea
    │   ├── All Wallpapers
    │   ├── Separator
    │   └── PlaylistList variant="floating"
    │       ├── FavoritesItem variant="floating"
    │       └── PlaylistItem variant="floating" (带拖拽)
    └── Footer

PlaylistList.tsx
├── variant prop: "floating" | "locked"
├── DndContext (拖拽上下文)
├── SortableContext (排序上下文)
├── FavoritesItem
└── PlaylistItem[]

FavoritesItem.tsx
├── variant prop: "floating" | "locked"
├── locked: 带图标槽的对齐布局
└── floating: 原始布局

PlaylistItem.tsx
├── variant prop: "floating" | "locked"
├── useSortable (拖拽功能)
├── AccordionItem (展开/折叠)
├── 缩略图预览
└── 重命名/删除菜单
```

---

## 关键实现细节

### 1. variant prop 模式切换

所有播放列表相关组件都支持 `variant` prop：

```tsx
// PlaylistList.tsx
interface PlaylistListProps {
  variant?: "floating" | "locked";
}

// FavoritesItem.tsx
interface FavoritesItemProps {
  variant?: "floating" | "locked";
}

// PlaylistItem.tsx
interface PlaylistItemProps {
  playlist: Playlist;
  variant?: "floating" | "locked";
}
```

### 2. locked 模式的对齐布局

```tsx
// PlaylistItem locked 模式核心结构
<AccordionItem ref={setNodeRef} style={style} value={playlist.id}>
  {/* 外层行容器：整行可拖动 */}
  <div className="flex items-start" {...attributes} {...listeners}>
    {/* 左侧图标槽 - 48px */}
    <div className="w-12 shrink-0 flex items-center justify-center pt-1.5">
      <button onClick={() => setActivePlaylist(playlist.id)}>
        <span className={generateAvatarColor(playlist.name)}>
          {getInitial(playlist.name)}
        </span>
      </button>
    </div>
    
    {/* 右侧内容槽 */}
    <div className="flex-1 pr-2 min-w-0">
      {/* Header: name + badge + chevron + menu */}
      <div className="group flex items-center gap-1 py-1.5 rounded-md">
        <span className="truncate">{playlist.name}</span>
        <Badge>{playlist.wallpaperIds.length}</Badge>
        <AccordionTrigger />
        <DropdownMenu>{/* rename/delete */}</DropdownMenu>
      </div>
      
      {/* Accordion Content: 缩略图预览 */}
      <AccordionContent>
        <div className="flex items-center gap-1.5">
          {thumbnails}
        </div>
      </AccordionContent>
    </div>
  </div>
</AccordionItem>
```

### 3. 拖拽功能保持

拖拽监听器挂在**整行容器**上（不是仅文字区域）：

```tsx
const { attributes, listeners, setNodeRef, transform, transition, isDragging } = 
  useSortable({ id: playlist.id });

// 拖拽监听在整行
<div className="flex items-start" {...attributes} {...listeners}>
  {/* 图标槽 + 内容槽 */}
</div>
```

限制为垂直方向拖动：

```tsx
const style = {
  transform: CSS.Transform.toString(
    transform ? { ...transform, x: 0 } : null  // x: 0 限制水平
  ),
  transition,
};
```

### 4. 状态管理

```tsx
// appStore.ts
isPlaylistSidebarOpen: boolean;        // 是否打开
isPlaylistSidebarPinned: boolean;      // 是否锁定

// 派生状态
const isFloating = isOpen && !isPinned;  // 悬浮模式
const isLocked = isOpen && isPinned;     // 锁定模式
```

### 5. 动画过渡

- **最小化 → 悬浮**：`animate-in slide-in-from-left fade-in`
- **悬浮 → 最小化**：`-translate-x-full opacity-0`
- **悬浮 → 锁定**：主容器变宽 + 浮层淡出
- **锁定 → 悬浮**：立即切换，无动画

---

## 功能清单

| 功能 | 最小化 | 悬浮 | 锁定 |
|------|--------|------|------|
| 图标显示 | ✅ | ✅ | ✅ |
| 文字显示 | ❌ | ✅ | ✅ |
| 图标-文字对齐 | N/A | ❌ 不需要 | ✅ |
| 拖拽排序 | ❌ | ✅ | ✅ |
| Accordion 展开/折叠 | ❌ | ✅ | ✅ |
| 缩略图预览 | ❌ | ✅ | ✅ |
| 重命名/删除菜单 | ❌ | ✅ | ✅ |
| Badge 数量 | ❌ | ✅ | ✅ |
| 新建播放列表 | ✅ (dialog) | ✅ | ✅ |
| 鼠标离开自动关闭 | N/A | ✅ 500ms | N/A |

---

## 文件清单

```
src/components/playlist/
├── PlaylistSidebar.tsx      # 主组件，三种布局
├── PlaylistList.tsx         # 播放列表容器，DndContext
├── PlaylistItem.tsx         # 单个播放列表项
├── FavoritesItem.tsx        # Favorites 特殊项
├── CreatePlaylistDialog.tsx # 新建对话框
├── RenamePlaylistDialog.tsx # 重命名对话框
└── DeletePlaylistDialog.tsx # 删除确认对话框
```

---

## 注意事项

### 1. 为什么悬浮模式不对齐？

悬浮模式是**独立浮层**（220px），只有单列文本结构，不存在双滚动列漂移问题。保持原始 `PlaylistList` 布局即可。

### 2. 维护一致性

修改 `PlaylistItem` 或 `FavoritesItem` 时，需要同时更新 `floating` 和 `locked` 两种变体的布局。避免只改一个。

### 3. 拖拽边界

锁定模式下，拖拽监听器在整行容器上，但需要确保：
- 三点菜单 `onPointerDown={(e) => e.stopPropagation()}` 阻止拖拽
- 点击 playlist name 不触发拖拽

### 4. Accordion 在 locked 模式下的位置

Accordion 展开内容放在**右侧内容槽**内（`flex-1 pr-2`），确保缩略图与文字列对齐。

---

## 未来优化方向

1. **拖拽手柄**：可为 locked 模式添加显式拖拽手柄，替代整行可拖动
2. **键盘导航**：支持键盘快捷键在三种模式间切换
3. **响应式宽度**：根据播放列表名称长度动态调整锁定模式宽度