# Playlist 功能实现计划 - 前端部分

## 0. 核心依赖

### 0.1 拖拽库（必须安装）

```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

> ⚠️ **禁止手写原生 H5 Drag and Drop API**！必须使用 `@dnd-kit` 实现拖拽排序，确保兼容性和状态管理的可靠性。

## 1. 功能概述

实现用户自定义壁纸播放列表功能，支持：
- 创建、重命名、删除播放列表
- 向列表中添加/移除壁纸
- 拖拽排序列表
- 勾选模式批量创建列表
- 右键菜单快速添加壁纸到列表
- 轮换播放时选择指定列表
- 左侧可隐藏的 PlaylistSidebar（固定宽度 220px）

## 2. UI 布局设计

```
┌──────────────────────────────────────────────────────────────┐
│                        AppNavbar                              │
├────────────┬─────────────────────────────┬──────────────────┤
│ Playlist   │                             │                  │
│ Sidebar    │      WallpaperGrid          │ WallpaperSidebar │
│  220px     │      (自动填充)             │   (可调整)       │
│ (可隐藏)   │                             │                  │
└────────────┴─────────────────────────────┴──────────────────┘
```

## 3. 组件架构

### 3.1 新建组件清单

```
src/components/playlist/
├── PlaylistSidebar.tsx          # 主容器 (220px 固定宽度)
├── PlaylistList.tsx             # 列表项容器 (拖拽排序)
├── PlaylistItem.tsx             # 单个列表项
├── CreatePlaylistDialog.tsx     # 创建弹窗
├── RenamePlaylistDialog.tsx     # 重命名弹窗
├── DeletePlaylistDialog.tsx     # 删除确认弹窗
├── AddToPlaylistMenu.tsx        # 右键菜单
├── SelectionModeBar.tsx         # 勾选模式工具栏
└── CyclePlaylistSelector.tsx    # 轮换源选择器
```

### 3.2 修改现有组件

| 组件 | 修改内容 |
|------|----------|
| `Library.tsx` | 集成 PlaylistSidebar |
| `WallpaperCard.tsx` | 勾选模式下的复选框 |
| `WallpaperGrid.tsx` | 右键菜单添加 "Add to playlist" |
| `WallpaperContextMenu.tsx` | 新增菜单项 |

## 4. 数据结构

### 4.1 类型定义 (`src/types.ts`)

```typescript
export interface Playlist {
  id: string;              // UUID
  name: string;            // 用户命名
  wallpaperIds: string[];  // 有序壁纸ID列表
  createdAt: number;       // 创建时间戳
  updatedAt: number;       // 更新时间戳
}
```

### 4.2 Store 扩展 (`src/store/appStore.ts`)

```typescript
interface AppStoreState {
  // ===== 新增：Playlist 相关 =====
  
  // 列表数据
  playlists: Playlist[];
  
  // 当前浏览的列表 ID (null = ALL)
  activePlaylistId: string | null;
  
  // 轮换使用的列表 ID (null = ALL)
  cyclePlaylistId: string | null;
  
  // 侧边栏状态
  isPlaylistSidebarOpen: boolean;  // 默认 true
  
  // 初始化状态（FOUC 防护）
  isHydrated: boolean;  // 默认 false，后端数据加载完成后置为 true
  
  // 勾选模式
  isSelectionMode: boolean;
  selectedForPlaylist: Set<string>;
  
  // ===== 新增方法 =====
  
  // 列表 CRUD（直接对应后端命令）
  loadPlaylists: () => Promise<void>;
  createPlaylist: (name: string, wallpaperIds: string[]) => Promise<void>;
  renamePlaylist: (id: string, name: string) => Promise<void>;
  deletePlaylist: (id: string) => Promise<void>;
  reorderPlaylists: (orderedIds: string[]) => Promise<void>;
  
  // ⚠️ 合成动作（前端组合逻辑，调用 update_playlist 全量覆盖）
  // 后端没有专门的 add_to_playlist 命令，这些是前端封装
  addToPlaylist: (playlistId: string, wallpaperIds: string[]) => Promise<void>;
  removeFromPlaylist: (playlistId: string, wallpaperId: string) => Promise<void>;
  
  // 状态控制
  setActivePlaylist: (id: string | null) => void;
  setCyclePlaylist: (id: string | null) => Promise<void>;
  togglePlaylistSidebar: () => void;
  
  // 勾选模式
  enterSelectionMode: () => void;
  exitSelectionMode: () => void;
  toggleSelectForPlaylist: (wallpaperId: string) => void;
  selectAllForPlaylist: () => void;
  deselectAllForPlaylist: () => void;
  createPlaylistFromSelection: (name: string) => Promise<void>;
  
  // 过滤逻辑修改
  getFilteredWallpapers: () => Wallpaper[];  // 需要考虑 activePlaylistId
}

### 4.3 addToPlaylist / removeFromPlaylist 实现细节

> ⚠️ **关键设计**：后端没有专门的 `add_to_playlist` 命令！这两个方法是前端的合成动作。

```typescript
// appStore.ts 中的合成动作实现

// 添加壁纸到列表（合成动作）
addToPlaylist: async (playlistId: string, newWallpaperIds: string[]) => {
  const state = get();
  const playlist = state.playlists.find(p => p.id === playlistId);
  if (!playlist) {
    throw new Error(`Playlist not found: ${playlistId}`);
  }
  
  // 🚨 关键：合并后必须去重！防止 React key 重复和 dnd-kit 崩溃
  const mergedIds = [...playlist.wallpaperIds, ...newWallpaperIds];
  const dedupedIds = Array.from(new Set(mergedIds));
  
  // 更新前端状态
  const updatedPlaylists = state.playlists.map(p =>
    p.id === playlistId
      ? { ...p, wallpaperIds: dedupedIds, updatedAt: Math.floor(Date.now() / 1000) }
      : p
  );
  set({ playlists: updatedPlaylists });
  
  // 调用后端 update_playlist 全量覆盖
  if (isTauri) {
    await invoke('update_playlist', {
      id: playlistId,
      wallpaperIds: dedupedIds
    });
  } else {
    persistPlaylists(updatedPlaylists);
  }
},

// 从列表移除壁纸（合成动作）
removeFromPlaylist: async (playlistId: string, wallpaperId: string) => {
  const state = get();
  const playlist = state.playlists.find(p => p.id === playlistId);
  if (!playlist) {
    throw new Error(`Playlist not found: ${playlistId}`);
  }
  
  const newWallpaperIds = playlist.wallpaperIds.filter(id => id !== wallpaperId);
  
  // 更新前端状态
  const updatedPlaylists = state.playlists.map(p =>
    p.id === playlistId
      ? { ...p, wallpaperIds: newWallpaperIds, updatedAt: Math.floor(Date.now() / 1000) }
      : p
  );
  set({ playlists: updatedPlaylists });
  
  // 调用后端 update_playlist 全量覆盖
  if (isTauri) {
    await invoke('update_playlist', {
      id: playlistId,
      wallpaperIds: newWallpaperIds
    });
  } else {
    persistPlaylists(updatedPlaylists);
  }
}
```

### 4.4 getFilteredWallpapers 核心逻辑（⚠️ 关键）

> **性能与排序约束**：当用户查看某个 Playlist 时，必须使用 `map` 而非 `filter`，以保留用户自定义的顺序！

> **⚠️ 过滤 Pipeline 顺序（严格遵守！）**：
> 1. **域过滤（Domain Filter）**：如果 `activePlaylistId` 存在，先基于该 Playlist 的 `wallpaperIds` 映射出基础数组
> 2. **搜索过滤（Search Filter）**：在第 1 步的基础数组上，再去匹配用户的搜索关键字
> 3. **最终输出**
> 
> **绝对不能把顺序搞反或并列！** 错误的顺序会导致搜索结果显示不在当前 Playlist 中的壁纸。

```typescript
// appStore.ts 中的实现
getFilteredWallpapers: () => {
  const state = get();
  const { wallpapers, searchQuery, sortBy, nicknames, activePlaylistId, playlists } = state;
  
  // ===== 情况 1：查看特定 Playlist =====
  if (activePlaylistId && activePlaylistId !== 'ALL') {
    const activePlaylist = playlists.find(p => p.id === activePlaylistId);
    if (!activePlaylist) return [];
    
    // 【步骤 1：域过滤】必须使用 map 保留用户自定义顺序！
    // 按照 playlist.wallpaperIds 的顺序映射到壁纸对象
    const playlistWallpapers = activePlaylist.wallpaperIds
      .map(id => wallpapers.find(w => w.id === id))
      .filter((w): w is Wallpaper => w !== undefined); // 过滤掉已物理删除的残影壁纸
    
    // 【步骤 2：搜索过滤】在域过滤结果上进行搜索
    // ⚠️ 关键：搜索只作用于 playlistWallpapers，不会跳出当前 Playlist
    if (searchQuery) {
      const lowerQ = searchQuery.toLowerCase();
      return playlistWallpapers.filter(w => 
        w.title.toLowerCase().includes(lowerQ) ||
        w.id.includes(lowerQ) ||
        (nicknames[w.id] || '').toLowerCase().includes(lowerQ)
      );
    }
    
    // 【步骤 3：最终输出】
    return playlistWallpapers;
  }
  
  // ===== 情况 2：ALL 视图（原有逻辑） =====
  let filtered = wallpapers;
  
  // 搜索过滤
  if (searchQuery) {
    const lowerQ = searchQuery.toLowerCase();
    filtered = wallpapers.filter(w => {
      const title = w.title.toLowerCase();
      const id = w.id.toLowerCase();
      const nick = (nicknames[w.id] || '').toLowerCase();
      return title.includes(lowerQ) || id.includes(lowerQ) || nick.includes(lowerQ);
    });
  }
  
  // 排序
  return [...filtered].sort((a, b) => {
    const titleA = nicknames[a.id] || a.title;
    const titleB = nicknames[b.id] || b.title;
    
    switch (sortBy) {
      case 'name':
        return titleA.localeCompare(titleB);
      case 'id':
        return a.id.localeCompare(b.id);
      case 'size':
        const sizeA = parseFloat(a.size || '0');
        const sizeB = parseFloat(b.size || '0');
        return sizeB - sizeA;
      default:
        return 0;
    }
  });
}
```

### 4.5 勾选模式性能保护（⚠️ 关键）

> **性能约束**：全选操作可能导致大量组件重渲染，必须限制范围和数量！

```typescript
// appStore.ts 中的勾选模式实现

// ⚠️ 性能保护：最大可选数量限制
const MAX_SELECTION_COUNT = 100;

// 进入勾选模式
enterSelectionMode: () => {
  set({ isSelectionMode: true, selectedForPlaylist: new Set() });
},

// 退出勾选模式
exitSelectionMode: () => {
  set({ isSelectionMode: false, selectedForPlaylist: new Set() });
},

// 切换单个壁纸选中状态
toggleSelectForPlaylist: (wallpaperId: string) => {
  const state = get();
  const newSet = new Set(state.selectedForPlaylist);
  
  if (newSet.has(wallpaperId)) {
    newSet.delete(wallpaperId);
  } else {
    // 🚨 检查是否超过上限
    if (newSet.size >= MAX_SELECTION_COUNT) {
      toast.warning(`Maximum ${MAX_SELECTION_COUNT} wallpapers can be selected at once`);
      return;
    }
    newSet.add(wallpaperId);
  }
  
  set({ selectedForPlaylist: newSet });
},

// 全选（⚠️ 性能保护：只选当前过滤后的可见壁纸）
selectAllForPlaylist: () => {
  const state = get();
  
  // 🚨 关键：只全选当前过滤后的可见壁纸，不是全局库
  const visibleWallpapers = state.getFilteredWallpapers();
  
  // 🚨 数量限制保护
  if (visibleWallpapers.length > MAX_SELECTION_COUNT) {
    toast.warning(`Too many wallpapers (${visibleWallpapers.length}). Only first ${MAX_SELECTION_COUNT} will be selected.`);
    const limited = visibleWallpapers.slice(0, MAX_SELECTION_COUNT);
    set({ selectedForPlaylist: new Set(limited.map(w => w.id)) });
  } else {
    set({ selectedForPlaylist: new Set(visibleWallpapers.map(w => w.id)) });
  }
},

// 取消全选
deselectAllForPlaylist: () => {
  set({ selectedForPlaylist: new Set() });
},
```

## 5. 组件详细设计

### 5.1 PlaylistSidebar.tsx

```tsx
// 主容器，固定宽度 220px，可隐藏
interface PlaylistSidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

// 结构：
// - Header: 标题 + 折叠按钮
// - Content: 列表项 + ALL 项
// - Footer: + New 按钮 + 轮换选择器

// 样式：
// - 宽度: isOpen ? 220px : 0
// - 过渡: transition-all duration-200
// - 隐藏时: overflow-hidden
```

### 5.2 PlaylistItem.tsx

```tsx
interface PlaylistItemProps {
  playlist: Playlist;
  isActive: boolean;
  onSelect: () => void;
  onRename: () => void;
  onDelete: () => void;
}

// 功能：
// - 显示列表名称 + 壁纸数量
// - 右键菜单：重命名、删除
// - 拖拽排序
// - 点击切换 activePlaylistId
```

### 5.3 CreatePlaylistDialog.tsx

```tsx
interface CreatePlaylistDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  initialWallpaperIds?: string[];  // 预选的壁纸
}

// 结构：
// - 输入框：列表名称
// - 网格：显示所有壁纸供选择
// - 底部：全选/反选按钮 + 创建按钮
```

### 5.4 SelectionModeBar.tsx

```tsx
// 勾选模式下的顶部工具栏
// 显示在 LibraryHeader 下方

// 功能：
// - 显示已选数量
// - 全选/反选按钮
// - 创建列表按钮
// - 取消按钮（退出勾选模式）
```

### 5.5 AddToPlaylistMenu.tsx

```tsx
// 右键菜单的子菜单

// 结构：
// - 现有列表列表（可点击添加）
// - 分隔线
// - "Create new playlist..." 选项
```

### 5.6 CyclePlaylistSelector.tsx

```tsx
// 轮换源选择下拉框
// 用于 PlaylistSidebar Footer 和 Settings > Playback

// 选项：
// - ALL (所有壁纸)
// - 各个自定义列表名称
```

> ⚠️ **UI 健壮性约束**：如果当前的 `cyclePlaylistId` 不为 null，且在现有的 `playlists` 数组中找不到对应的 ID（意味着列表已被删除），Selector 必须自动回退（Fallback）显示为 "ALL" 选项，并悄悄触发一次 `setCyclePlaylist(null)` 修正状态。

```tsx
// CyclePlaylistSelector.tsx 实现示例
function CyclePlaylistSelector() {
  const playlists = useAppStore(s => s.playlists);
  const cyclePlaylistId = useAppStore(s => s.cyclePlaylistId);
  const setCyclePlaylist = useAppStore(s => s.setCyclePlaylist);
  
  // 🚨 健壮性检查：如果 cyclePlaylistId 对应的列表已不存在，自动回退到 ALL
  React.useEffect(() => {
    if (cyclePlaylistId) {
      const exists = playlists.some(p => p.id === cyclePlaylistId);
      if (!exists) {
        // 静默修正状态
        setCyclePlaylist(null);
      }
    }
  }, [cyclePlaylistId, playlists, setCyclePlaylist]);
  
  // 确定当前选中值（如果列表已删除，显示 ALL）
  const effectiveValue = React.useMemo(() => {
    if (!cyclePlaylistId) return 'ALL';
    const exists = playlists.some(p => p.id === cyclePlaylistId);
    return exists ? cyclePlaylistId : 'ALL';
  }, [cyclePlaylistId, playlists]);
  
  // ... 渲染 Select 组件
}
```

## 6. 交互流程

### 6.1 创建列表

```
方式 1: 侧边栏 +New 按钮
┌─────────────────────────────────────────────────┐
│ Create New Playlist                         [X] │
├─────────────────────────────────────────────────┤
│ Name: [____________________]                    │
│                                                 │
│ Select wallpapers:                              │
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐               │
│ │ ☐  │ │ ☑  │ │ ☐  │ │ ☑  │               │
│ │ 🖼️ │ │ 🖼️ │ │ 🖼️ │ │ 🖼️ │               │
│ └─────┘ └─────┘ └─────┘ └─────┘               │
│                                                 │
│ [Select All] [Deselect All]                     │
├─────────────────────────────────────────────────┤
│                           [Cancel] [Create]     │
└─────────────────────────────────────────────────┘
```

### 6.2 勾选模式

```
1. 在 ALL 列表下点击 "Select" 按钮进入勾选模式
2. 壁纸卡片左上角出现复选框
3. 用户勾选壁纸
4. 顶部工具栏显示已选数量 + "Create Playlist" 按钮
5. 点击创建，输入名称，完成
```

### 6.3 右键添加

```
1. 在壁纸卡片上右键
2. 选择 "Add to playlist"
3. 展开子菜单，显示所有列表
4. 点击列表名称，添加完成
5. 或点击 "Create new..." 创建新列表
```

### 6.4 列表切换

```
1. 点击侧边栏中的列表项
2. WallpaperGrid 显示该列表中的壁纸
3. activePlaylistId 更新
4. getFilteredWallpapers() 返回过滤后的结果
```

## 7. 状态持久化与前后端同步

### 7.1 架构原则

> ⚠️ **关键约束**：前后端数据必须保持同步，严禁在 Tauri 环境下使用 localStorage 存储业务数据！

| 环境 | 存储方式 | 说明 |
|------|----------|------|
| **Tauri 环境** | `invoke()` 调用后端命令 | 数据持久化到 `config.json` |
| **浏览器开发** | `localStorage` 仅作为 fallback | 仅用于前端开发测试 |

### 7.2 环境检测与分支

```typescript
// appStore.ts 中的环境检测
const isTauri = !!(window as any).__TAURI_INTERNALS__;

// 统一的数据持久化入口
const persistPlaylists = async (playlists: Playlist[]) => {
  if (isTauri) {
    // Tauri 环境：数据已在后端命令中持久化，无需额外操作
    return;
  }
  // 浏览器开发环境：使用 localStorage 作为 fallback
  localStorage.setItem('lwg_playlists', JSON.stringify(playlists));
};

const persistCyclePlaylist = async (id: string | null) => {
  if (isTauri) {
    await invoke('set_cycle_playlist', { id });
    return;
  }
  if (id) {
    localStorage.setItem('lwg_cycle_playlist', id);
  } else {
    localStorage.removeItem('lwg_cycle_playlist');
  }
};
```

### 7.3 初始化加载

```typescript
// appStore.ts 初始化
loadPlaylists: async () => {
  if (isTauri) {
    // 从后端加载
    const playlists = await invoke<Playlist[]>('get_playlists');
    const cyclePlaylistId = await invoke<string | null>('get_cycle_playlist');
    set({ playlists, cyclePlaylistId });
  } else {
    // 浏览器开发环境：从 localStorage 加载
    const playlists = JSON.parse(localStorage.getItem('lwg_playlists') || '[]');
    const cyclePlaylistId = localStorage.getItem('lwg_cycle_playlist') || null;
    set({ playlists, cyclePlaylistId });
  }
}
```

### 7.4 UUID 生成（前端负责）

> ⚠️ **关键设计**：UUID 由前端生成，以支持乐观更新（Optimistic Update）！

```typescript
// 前端生成 UUID
const generateUUID = (): string => {
  // 使用 Web Crypto API
  return crypto.randomUUID();
};

// createPlaylist 实现（乐观更新）
createPlaylist: async (name: string, wallpaperIds: string[]) => {
  const id = generateUUID(); // 前端生成 ID
  const now = Math.floor(Date.now() / 1000);
  
  const newPlaylist: Playlist = {
    id,
    name,
    wallpaperIds,
    createdAt: now,
    updatedAt: now,
  };
  
  // 1. 乐观更新：立即更新 UI
  set(state => ({
    playlists: [...state.playlists, newPlaylist]
  }));
  
  // 2. 持久化
  if (isTauri) {
    try {
      // 后端接收前端生成的 ID
      await invoke('create_playlist', { id, name, wallpaperIds });
    } catch (error) {
      // 回滚乐观更新
      set(state => ({
        playlists: state.playlists.filter(p => p.id !== id)
      }));
      throw error;
    }
  } else {
    persistPlaylists(get().playlists);
  }
}
```

### 7.5 deletePlaylist 防御代码

> ⚠️ **关键约束**：删除列表时必须检查是否为当前活跃列表或轮换列表！

```typescript
deletePlaylist: async (id: string) => {
  const state = get();
  
  // 🚨 防御 1：如果删除的是当前正在查看的列表，退回到 ALL
  if (state.activePlaylistId === id) {
    set({ activePlaylistId: null });
  }
  
  // 🚨 防御 2：如果删除的是轮换列表，清除轮换设置
  if (state.cyclePlaylistId === id) {
    if (isTauri) {
      await invoke('set_cycle_playlist', { id: null });
    }
    set({ cyclePlaylistId: null });
  }
  
  // 3. 从列表中移除
  const newPlaylists = state.playlists.filter(p => p.id !== id);
  set({ playlists: newPlaylists });
  
  // 4. 持久化
  if (isTauri) {
    await invoke('delete_playlist', { id });
  } else {
    persistPlaylists(newPlaylists);
  }
}
```

## 8. 拖拽排序实现

### 8.1 依赖

```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

### 8.2 实现要点

> **⚠️ 性能约束**：拖拽过程中禁止频繁调用后端！必须采用"乐观更新优先，onDragEnd 时持久化"策略。

```tsx
// PlaylistList.tsx
import { DndContext, closestCenter, DragEndEvent } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';

// 🚨 关键：拖拽结束才保存，拖拽过程中只更新 UI
const handleDragEnd = (event: DragEndEvent) => {
  const { active, over } = event;
  if (over && active.id !== over.id) {
    const oldIndex = playlists.findIndex(p => p.id === active.id);
    const newIndex = playlists.findIndex(p => p.id === over.id);
    
    // 1. 乐观更新：立即更新 UI（Zustand state）
    const newOrder = arrayMove(playlists, oldIndex, newIndex);
    set({ playlists: newOrder });  // 本地状态立即响应
    
    // 2. 持久化：只在 onDragEnd 时发送一次请求
    reorderPlaylists(newOrder.map(p => p.id));
  }
};

// Store 中的 reorderPlaylists 实现
reorderPlaylists: async (orderedIds: string[]) => {
  // 不再更新本地状态（已在 handleDragEnd 中乐观更新）
  // 只发送持久化请求
  if (isTauri) {
    try {
      await invoke('reorder_playlists', { orderedIds });
    } catch (error) {
      // 持久化失败，回滚乐观更新（可以从后端重新加载）
      console.error('Failed to persist reorder:', error);
      toast.error('Failed to save playlist order');
      // 可选：重新加载 playlists 恢复状态
      await get().loadPlaylists();
    }
  } else {
    persistPlaylists(get().playlists);
  }
}
```

### 8.3 初始化闪烁防护（FOUC Prevention）

> **⚠️ 用户体验约束**：侧边栏宽度状态在从后端加载完成前，应保持骨架屏或隐藏，避免闪烁。

```tsx
// appStore.ts 中的初始化逻辑

// 状态：是否已完成 hydration（注水）
isHydrated: boolean;  // 默认 false

// 初始化加载
loadPlaylists: async () => {
  try {
    if (isTauri) {
      // 从后端加载所有设置（包括 playlistSidebarOpen）
      const [playlists, cyclePlaylistId, sidebarOpen] = await Promise.all([
        invoke<Playlist[]>('get_playlists'),
        invoke<string | null>('get_cycle_playlist'),
        invoke<boolean>('get_playlist_sidebar_open'),
      ]);
      
      set({
        playlists,
        cyclePlaylistId,
        isPlaylistSidebarOpen: sidebarOpen,
        isHydrated: true,  // 标记注水完成
      });
    } else {
      // 浏览器环境从 localStorage 加载
      set({
        playlists: JSON.parse(localStorage.getItem('lwg_playlists') || '[]'),
        cyclePlaylistId: localStorage.getItem('lwg_cycle_playlist') || null,
        isPlaylistSidebarOpen: localStorage.getItem('lwg_sidebar_open') !== 'false',
        isHydrated: true,
      });
    }
  } catch (error) {
    console.error('Failed to load playlists:', error);
    set({ isHydrated: true });  // 即使失败也标记完成，避免永久卡住
  }
}

// PlaylistSidebar.tsx 中使用
function PlaylistSidebar() {
  const isHydrated = useAppStore(s => s.isHydrated);
  const isOpen = useAppStore(s => s.isPlaylistSidebarOpen);
  
  // 注水完成前显示骨架屏或保持隐藏
  if (!isHydrated) {
    return (
      <div className="w-[220px] h-full bg-muted animate-pulse">
        {/* 骨架屏 */}
      </div>
    );
  }
  
  // 注水完成后正常渲染
  return (
    <div className={cn(
      "h-full flex flex-col bg-sidebar border-r transition-all duration-200",
      isOpen ? "w-[220px]" : "w-0 overflow-hidden"
    )}>
      {/* ... */}
    </div>
  );
}
```

## 9. 文件修改清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `src/types.ts` | 修改 | 新增 `Playlist` 类型 |
| `src/store/appStore.ts` | 修改 | 新增 playlist 状态和方法 |
| `src/pages/Library.tsx` | 修改 | 集成 PlaylistSidebar |
| `src/components/playlist/PlaylistSidebar.tsx` | **新建** | 主容器 |
| `src/components/playlist/PlaylistList.tsx` | **新建** | 列表项容器（拖拽） |
| `src/components/playlist/PlaylistItem.tsx` | **新建** | 单个列表项 |
| `src/components/playlist/CreatePlaylistDialog.tsx` | **新建** | 创建弹窗 |
| `src/components/playlist/RenamePlaylistDialog.tsx` | **新建** | 重命名弹窗 |
| `src/components/playlist/DeletePlaylistDialog.tsx` | **新建** | 删除确认 |
| `src/components/playlist/AddToPlaylistMenu.tsx` | **新建** | 右键菜单 |
| `src/components/playlist/SelectionModeBar.tsx` | **新建** | 勾选模式工具栏 |
| `src/components/playlist/CyclePlaylistSelector.tsx` | **新建** | 轮换源选择器 |
| `src/components/library/WallpaperCard.tsx` | 修改 | 勾选模式复选框 |
| `src/components/library/WallpaperGrid.tsx` | 修改 | 右键菜单扩展 |
| `src/components/layout/AppSidebar.tsx` | **删除** | 废弃文件 |

## 10. 开发阶段

| 阶段 | 任务 | 预估时间 |
|------|------|----------|
| **Phase 1** | 类型定义 + Store 扩展 | 30 分钟 |
| **Phase 2** | PlaylistSidebar 基础 UI（空壳） | 45 分钟 |
| **Phase 3** | 集成到 Library.tsx | 30 分钟 |
| **Phase 4** | PlaylistItem + 列表渲染 | 45 分钟 |
| **Phase 5** | CreatePlaylistDialog | 1 小时 |
| **Phase 6** | 重命名 + 删除对话框 | 30 分钟 |
| **Phase 7** | 右键菜单添加 | 30 分钟 |
| **Phase 8** | 勾选模式 | 1 小时 |
| **Phase 9** | 拖拽排序 | 1 小时 |
| **Phase 10** | 轮换选择器 | 30 分钟 |
| **Phase 11** | 本地存储持久化 | 30 分钟 |
| **Phase 12** | 测试 + 边缘情况 | 1 小时 |
| **总计** | | **约 8 小时** |

## 11. 测试要点

### 11.1 功能测试

- [ ] 创建列表：输入名称，选择壁纸，创建成功
- [ ] 重命名列表：右键菜单，输入新名称，更新成功
- [ ] 删除列表：确认对话框，删除成功
- [ ] 添加壁纸到列表：右键菜单，添加成功
- [ ] 从列表移除壁纸：移除成功，列表为空时提示删除
- [ ] 拖拽排序：拖动列表项，顺序更新
- [ ] 勾选模式：进入/退出，全选/反选，创建列表
- [ ] 列表切换：点击列表，Grid 显示对应壁纸
- [ ] 轮换源选择：选择列表，设置成功
- [ ] 侧边栏隐藏/显示：切换正常
- [ ] 数据持久化（Tauri）：刷新页面，数据从后端加载正确
- [ ] 数据持久化（浏览器）：刷新页面，localStorage 数据保持

### 11.2 边缘情况

- [ ] 创建空名称列表：显示错误提示
- [ ] 创建重复名称列表：允许（ID 不同）
- [ ] 列表内壁纸全部移除：提示删除列表
- [ ] **删除当前查看的列表**：自动退回到 ALL 视图
- [ ] **删除轮换中的列表**：自动切换到 ALL
- [ ] **删除壁纸后清理 Playlist**：物理删除壁纸后，所有 Playlist 中的该 ID 被移除
- [ ] **轮换列表被删除后 Selector 回退**：CyclePlaylistSelector 自动显示 ALL 并修正状态
- [ ] **Playlist 视图下壁纸顺序**：确认显示顺序与用户在列表中编排的顺序一致
- [ ] **乐观更新回滚**：后端创建失败时，前端状态回滚
- [ ] **重复添加同一壁纸**：自动去重，不会导致 React key 冲突或拖拽崩溃
- [ ] **过滤 Pipeline 顺序**：在 Playlist 视图下搜索，只显示当前列表中的匹配结果
- [ ] **全选数量限制**：超过 100 张时显示警告并只选前 100 张
- [ ] **拖拽性能**：拖拽过程中 UI 跟手响应，只在释放时调用一次后端
- [ ] **初始化无闪烁**：侧边栏状态从后端加载后正确显示，无宽度跳变

## 12. 注意事项

### 12.1 环境适配

| 环境 | 数据持久化 | 说明 |
|------|-----------|------|
| **Tauri 环境** | `invoke()` 调用后端命令 | 数据持久化到 `config.json` |
| **浏览器开发** | `localStorage` fallback | 仅用于前端开发测试 |

```typescript
const isTauri = !!(window as any).__TAURI_INTERNALS__;

if (isTauri) {
  // Tauri 环境：调用后端
  await invoke('create_playlist', { id, name, wallpaperIds });
} else {
  // 浏览器开发环境：使用 localStorage fallback
  localStorage.setItem('lwg_playlists', JSON.stringify(playlists));
}
```

### 12.2 状态同步

- `activePlaylistId` 变化时，重新计算 `getFilteredWallpapers()`
- `playlists` 变化时，调用后端命令持久化（localStorage 仅作为浏览器开发 fallback）
- 轮换设置同步到 Settings 页面

### 12.3 UI 细节

- 列表项 hover 时显示操作按钮
- 拖拽时显示拖拽指示器
- 删除确认弹窗防止误操作
- 空列表显示提示信息

---

## ⚠️ 执行约束

1. **优先完成基础功能**：先实现创建/删除/切换列表，再做高级功能
2. **前后端同步开发**：在 Tauri 环境下必须通过 invoke 调用后端命令，localStorage 仅作为浏览器开发 fallback
3. **保持 UI 一致性**：使用现有的 Tailwind 样式和 shadcn 组件
4. **渐进式开发**：每个阶段完成后验证，再进入下一阶段
5. **🚨 禁止使用 filter 过滤 Playlist**：在 Playlist 视图下必须使用 `map` 以保留用户自定义顺序
6. **🚨 禁止手写原生拖拽**：必须使用 `@dnd-kit` 库实现拖拽排序
7. **🚨 CyclePlaylistSelector 必须健壮**：当列表被删除后自动回退到 ALL
8. **🚨 UUID 前端生成**：createPlaylist 必须使用 `crypto.randomUUID()` 生成 ID，支持乐观更新
9. **🚨 deletePlaylist 必须防御**：删除列表时检查是否为当前活跃列表或轮换列表，自动回退
10. **🚨 去重保护**：addToPlaylist 合并数组后必须 `Array.from(new Set(...))` 去重，防止 React key 冲突和 dnd-kit 崩溃
11. **🚨 合成动作**：addToPlaylist 和 removeFromPlaylist 是前端封装，调用 `update_playlist` 全量覆盖，后端没有专门的命令
12. **🚨 过滤 Pipeline 顺序**：必须先域过滤（Playlist），再搜索过滤，顺序不能颠倒
13. **🚨 全选性能保护**：selectAllForPlaylist 只选当前过滤后的可见壁纸，且最多 100 张
14. **🚨 拖拽性能优化**：拖拽过程中只更新 UI（乐观更新），onDragEnd 时才调用后端持久化，禁止拖拽中频繁 IPC
15. **🚨 初始化闪烁防护**：使用 `isHydrated` 状态，后端数据加载完成前显示骨架屏，避免侧边栏宽度闪烁

## ⚠️ 跨模块联动警告

> **关键**：Playlist 功能与现有的"删除壁纸"功能存在跨模块依赖！

### 删除壁纸时必须清理 Playlist 残留

当用户物理删除一张壁纸时，必须同步清理所有 Playlist 中该壁纸的 ID，否则会形成"死链（Dead ID）"：

- **问题**：如果 Playlist 中残留被删除壁纸的 ID，轮换时会导致壁纸引擎找不到文件而崩溃
- **解决方案**：修改 `removeWallpaper` 方法，删除壁纸后遍历所有 Playlist，移除该 ID

```typescript
// appStore.ts 中修改 removeWallpaper 方法
removeWallpaper: async (id: string, path: string) => {
  // ... 现有删除逻辑 ...
  
  // 🚨 跨模块联动：清理所有 Playlist 中的死链 ID
  const state = get();
  const updatedPlaylists = state.playlists.map(playlist => ({
    ...playlist,
    wallpaperIds: playlist.wallpaperIds.filter(wid => wid !== id)
  })).filter(playlist => {
    // 如果列表为空，提示用户删除或保留
    return playlist.wallpaperIds.length > 0;
  });
  
  set({ playlists: updatedPlaylists });
  
  // 持久化
  if (isTauri) {
    // 后端也需要同步修改 remove_wallpaper 命令
    // 遍历所有 playlists，移除该 ID
  }
}
```

### 后端联动修改

修改 `src-tauri/src/lib.rs` 中的 `remove_wallpaper` 命令：

```rust
// 在 remove_wallpaper 命令中添加
// 清理所有 Playlist 中的该壁纸 ID
for playlist in cm.config_mut().playlists.iter_mut() {
    playlist.wallpaper_ids.retain(|wid| wid != &id);
}
// 移除空列表（可选，或提示用户）
cm.config_mut().playlists.retain(|p| !p.wallpaper_ids.is_empty());
cm.save()?;
```