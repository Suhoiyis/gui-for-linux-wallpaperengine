# Playlist 功能实现计划 - 后端部分

## 1. 功能概述

为 Playlist 功能提供后端支持：
- Playlist 数据结构定义
- 持久化存储到 `config.json`
- CRUD 命令实现
- 轮换逻辑修改（支持指定列表）

## 2. 数据结构

### 2.1 Playlist 结构体 (`lwg-rs/crates/lwg-core/src/config.rs`)

```rust
/// 播放列表
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Playlist {
    /// 唯一标识符 (UUID)
    pub id: String,
    
    /// 列表名称
    pub name: String,
    
    /// 壁纸 ID 列表（有序）
    pub wallpaper_ids: Vec<String>,
    
    /// 创建时间戳（秒）
    pub created_at: u64,
    
    /// 更新时间戳（秒）
    pub updated_at: u64,
}

impl Playlist {
    /// 创建新播放列表（仅用于测试）
    /// 
    /// ⚠️ 生产环境中 ID 由前端生成，后端 create_playlist 命令接收前端传来的 ID
    /// 此方法仅用于单元测试
    #[cfg(test)]
    pub fn new(name: String, wallpaper_ids: Vec<String>) -> Self {
        let now = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs();
        
        Self {
            id: uuid::Uuid::new_v4().to_string(),
            name,
            wallpaper_ids,
            created_at: now,
            updated_at: now,
        }
    }
}
```

### 2.2 AppConfig 扩展

```rust
// 在 AppConfig 结构体中新增字段
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct AppConfig {
    // ... 现有字段 ...
    
    /// 用户自定义播放列表
    pub playlists: Vec<Playlist>,
    
    /// 轮换使用的列表 ID（None = ALL）
    pub cycle_playlist_id: Option<String>,
    
    /// Playlist 侧边栏显示状态
    pub playlist_sidebar_open: bool,
}

// 更新 Default 实现
impl Default for AppConfig {
    fn default() -> Self {
        Self {
            // ... 现有默认值 ...
            playlists: Vec::new(),
            cycle_playlist_id: None,
            playlist_sidebar_open: true,
        }
    }
}
```

### 2.3 配置文件格式

```json
// ~/.config/linux-wallpaperengine-gui/config.json
{
  "fps": 30,
  "volume": 50,
  // ... 其他配置 ...
  "playlists": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Nature",
      "wallpaperIds": ["2874425843", "2810924556"],
      "createdAt": 1700000000,
      "updatedAt": 1700000000
    }
  ],
  "cyclePlaylistId": "550e8400-e29b-41d4-a716-446655440000",
  "playlistSidebarOpen": true
}
```

## 3. Tauri 命令设计

### 3.1 命令清单

| 命令 | 参数 | 返回值 | 功能 |
|------|------|--------|------|
| `get_playlists` | 无 | `Vec<Playlist>` | 获取所有列表 |
| `create_playlist` | `id: String, name: String, wallpaper_ids: Vec<String>` | `Playlist` | 创建列表（ID 由前端生成） |
| `update_playlist` | `id: String, name: Option<String>, wallpaper_ids: Option<Vec<String>>` | `()` | 更新列表 |
| `delete_playlist` | `id: String` | `()` | 删除列表 |
| `reorder_playlists` | `ordered_ids: Vec<String>` | `()` | 排序列表 |
| `set_cycle_playlist` | `id: Option<String>` | `()` | 设置轮换列表 |
| `get_cycle_playlist` | 无 | `Option<String>` | 获取当前轮换列表 ID |
| `get_playlist_sidebar_open` | 无 | `bool` | 获取侧边栏显示状态 |
| `set_playlist_sidebar_open` | `open: bool` | `()` | 设置侧边栏显示状态 |

### 3.2 命令实现

```rust
// src-tauri/src/lib.rs

/// 获取所有播放列表
#[tauri::command]
async fn get_playlists(
    state: State<'_, TauriState>,
) -> Result<Vec<Playlist>, String> {
    let cm = state.config_manager.lock().await;
    Ok(cm.config().playlists.clone())
}

/// 创建播放列表
/// 
/// ⚠️ ID 由前端生成：前端使用 crypto.randomUUID() 生成 UUID，
/// 以支持乐观更新（Optimistic Update）
/// 
/// ⚠️ 去重保护：wallpaper_ids 会自动去重
#[tauri::command]
async fn create_playlist(
    id: String,  // 前端生成的 UUID
    name: String,
    mut wallpaper_ids: Vec<String>,
    state: State<'_, TauriState>,
) -> Result<Playlist, String> {
    // 验证名称非空
    let name = name.trim();
    if name.is_empty() {
        return Err("Playlist name cannot be empty".to_string());
    }
    
    // 验证 ID 格式（简单的 UUID 格式检查）
    if id.is_empty() || id.len() != 36 {
        return Err("Invalid playlist ID format".to_string());
    }
    
    // 检查 ID 是否已存在
    {
        let cm = state.config_manager.lock().await;
        if cm.config().playlists.iter().any(|p| p.id == id) {
            return Err(format!("Playlist with ID {} already exists", id));
        }
    }
    
    // 🚨 去重保护：完全去重但保留顺序（防止重复 ID 导致前端崩溃）
    // 注意：dedup() 只去除连续重复，这里需要完全去重
    let mut seen = std::collections::HashSet::new();
    let deduped_ids: Vec<String> = wallpaper_ids
        .into_iter()
        .filter(|id| seen.insert(id.clone()))
        .collect();
    
    // 创建新列表（使用前端传来的 ID）
    let now = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_secs();
    
    let playlist = Playlist {
        id,
        name: name.to_string(),
        wallpaper_ids: deduped_ids,
        created_at: now,
        updated_at: now,
    };
    
    let result = playlist.clone();
    
    // 更新配置
    {
        let mut cm = state.config_manager.lock().await;
        cm.config_mut().playlists.push(playlist);
        cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
    }
    
    Ok(result)
}

/// 更新播放列表
/// 
/// ⚠️ 去重保护：wallpaper_ids 会自动去重，防止前端重复添加导致 React/dnd-kit 崩溃
#[tauri::command]
async fn update_playlist(
    id: String,
    name: Option<String>,
    mut wallpaper_ids: Option<Vec<String>>,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    let mut cm = state.config_manager.lock().await;
    
    // 查找列表
    let playlist = cm.config_mut()
        .playlists
        .iter_mut()
        .find(|p| p.id == id)
        .ok_or_else(|| format!("Playlist not found: {}", id))?;
    
    // 更新字段
    if let Some(n) = name {
        let n = n.trim();
        if n.is_empty() {
            return Err("Playlist name cannot be empty".to_string());
        }
        playlist.name = n.to_string();
    }
    
    if let Some(ids) = wallpaper_ids {
        // 🚨 去重保护：完全去重但保留顺序
        let mut seen = std::collections::HashSet::new();
        let deduped_ids: Vec<String> = ids
            .into_iter()
            .filter(|id| seen.insert(id.clone()))
            .collect();
        playlist.wallpaper_ids = deduped_ids;
    }
    
    // 更新时间戳
    playlist.updated_at = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_secs();
    
    cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
    
    Ok(())
}

/// 删除播放列表
#[tauri::command]
async fn delete_playlist(
    id: String,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    let mut cm = state.config_manager.lock().await;
    
    // 查找并移除
    let index = cm.config()
        .playlists
        .iter()
        .position(|p| p.id == id)
        .ok_or_else(|| format!("Playlist not found: {}", id))?;
    
    cm.config_mut().playlists.remove(index);
    
    // 如果删除的是轮换列表，清除设置
    if cm.config().cycle_playlist_id.as_ref() == Some(&id) {
        cm.config_mut().cycle_playlist_id = None;
    }
    
    cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
    
    Ok(())
}

/// 重排序播放列表
/// 
/// ⚠️ 竞态安全：使用安全合并策略，避免因并发创建新列表导致排序失败
/// 
/// 逻辑：
/// 1. 按照 ordered_ids 的顺序重建列表（已存在的）
/// 2. 将未出现在 ordered_ids 中的新列表（竞态产生的）追加到末尾
#[tauri::command]
async fn reorder_playlists(
    ordered_ids: Vec<String>,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    let mut cm = state.config_manager.lock().await;
    
    // 创建 ID 到 Playlist 的映射
    let id_to_playlist: std::collections::HashMap<String, Playlist> = cm.config()
        .playlists
        .iter()
        .map(|p| (p.id.clone(), p.clone()))
        .collect();
    
    let mut new_playlists: Vec<Playlist> = Vec::new();
    let mut processed_ids: std::collections::HashSet<String> = std::collections::HashSet::new();
    
    // 1. 按照 ordered_ids 的顺序插入已存在的列表
    for id in &ordered_ids {
        if let Some(playlist) = id_to_playlist.get(id) {
            new_playlists.push(playlist.clone());
            processed_ids.insert(id.clone());
        }
        // 如果 ID 不存在，静默忽略（可能是已删除的列表）
    }
    
    // 2. 将未在 ordered_ids 中的列表（竞态产生的新列表）追加到末尾
    for playlist in &cm.config().playlists {
        if !processed_ids.contains(&playlist.id) {
            new_playlists.push(playlist.clone());
        }
    }
    
    cm.config_mut().playlists = new_playlists;
    cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
    
    Ok(())
}

/// 设置轮换播放列表
#[tauri::command]
async fn set_cycle_playlist(
    id: Option<String>,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    let mut cm = state.config_manager.lock().await;
    
    // 验证 ID 存在（如果提供）
    if let Some(ref playlist_id) = id {
        let exists = cm.config()
            .playlists
            .iter()
            .any(|p| &p.id == playlist_id);
        
        if !exists {
            return Err(format!("Playlist not found: {}", playlist_id));
        }
    }
    
    cm.config_mut().cycle_playlist_id = id;
    cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
    
    Ok(())
}

/// 获取当前轮换播放列表 ID
#[tauri::command]
async fn get_cycle_playlist(
    state: State<'_, TauriState>,
) -> Result<Option<String>, String> {
    let cm = state.config_manager.lock().await;
    Ok(cm.config().cycle_playlist_id.clone())
}

/// 获取侧边栏显示状态
#[tauri::command]
async fn get_playlist_sidebar_open(
    state: State<'_, TauriState>,
) -> Result<bool, String> {
    let cm = state.config_manager.lock().await;
    Ok(cm.config().playlist_sidebar_open)
}

/// 设置侧边栏状态
#[tauri::command]
async fn set_playlist_sidebar_open(
    open: bool,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    let mut cm = state.config_manager.lock().await;
    cm.config_mut().playlist_sidebar_open = open;
    cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
    Ok(())
}
```

### 3.3 注册命令

```rust
.invoke_handler(tauri::generate_handler![
    // ... 现有命令 ...
    get_playlists,
    create_playlist,
    update_playlist,
    delete_playlist,
    reorder_playlists,
    set_cycle_playlist,
    get_cycle_playlist,
    get_playlist_sidebar_open,
    set_playlist_sidebar_open,
])
```

## 4. 轮换逻辑修改

### 4.1 修改 `select_next_wallpaper` 函数

```rust
/// 选择下一张壁纸
/// 
/// 新增参数：
/// - `cycle_playlist_id`: 指定的播放列表 ID
/// - `playlists`: 所有播放列表
/// 
/// ⚠️ 空列表处理：如果指定的播放列表为空，优雅降级到全局库随机选择
fn select_next_wallpaper(
    order: &str,
    current_id: Option<&str>,
    all_ids: &[String],
    cycle_playlist_id: Option<&str>,
    playlists: &[Playlist],
) -> String {
    // 确定候选壁纸 ID 列表
    let candidate_ids: Vec<String> = if let Some(playlist_id) = cycle_playlist_id {
        // 从指定列表获取壁纸
        let playlist_wallpapers = playlists
            .iter()
            .find(|p| p.id == playlist_id)
            .map(|p| p.wallpaper_ids.clone());
        
        match playlist_wallpapers {
            Some(ids) if !ids.is_empty() => ids,
            _ => {
                // ⚠️ 空列表或列表不存在：优雅降级到全局库
                all_ids.to_vec()
            }
        }
    } else {
        // 使用所有壁纸
        all_ids.to_vec()
    };
    
    // 🚨 如果全局库也为空，返回空字符串（调用方需要处理）
    if candidate_ids.is_empty() {
        return String::new();
    }
    
    match order {
        "random" => {
            use rand::seq::SliceRandom;
            candidate_ids
                .choose(&mut rand::thread_rng())
                .unwrap()
                .clone()
        }
        "title" | "size" | "type" | "id" => {
            // 顺序模式：在候选列表中找当前壁纸，取下一个
            let next_index = if let Some(current) = current_id {
                let current_index = candidate_ids
                    .iter()
                    .position(|id| id == current)
                    .unwrap_or(0);
                (current_index + 1) % candidate_ids.len()
            } else {
                0
            };
            candidate_ids[next_index].clone()
        }
        _ => {
            use rand::seq::SliceRandom;
            candidate_ids
                .choose(&mut rand::thread_rng())
                .unwrap()
                .clone()
        }
    }
}
```

> ⚠️ **关键变更**：当指定的播放列表为空时，不再返回空字符串（会导致引擎崩溃），而是优雅降级到全局库随机选择。
```

### 4.2 修改 `trigger_cycle_internal` 函数

```rust
async fn trigger_cycle_internal(app: &AppHandle) -> Result<(), String> {
    let state = app.state::<TauriState>();
    
    // 获取配置（包括 playlists）
    let (cycle_order, cycle_screen, cycle_playlist_id, playlists) = {
        let cm = state.config_manager.lock().await;
        (
            cm.config().cycle_order.clone(),
            state.cycle_screen.lock().await.clone(),
            cm.config().cycle_playlist_id.clone(),
            cm.config().playlists.clone(),
        )
    };
    
    // 获取所有壁纸 ID 缓存
    let all_wallpaper_ids = {
        let cache = state.cached_wallpaper_ids.read()
            .map_err(|e| format!("Cache read error: {}", e))?;
        cache.clone()
    };
    
    // ... 其他逻辑 ...
    
    // 选择下一张壁纸时传入 playlist 信息
    let new_wp_id = select_next_wallpaper(
        &cycle_order,
        current_id,
        &all_wallpaper_ids,
        cycle_playlist_id.as_deref(),
        &playlists,
    );
    
    // ... 其余逻辑不变 ...
}
```

## 5. 配置迁移

### 5.1 向后兼容

旧版本 `config.json` 没有 `playlists` 字段，需要确保默认值正确：

```rust
// 在 ConfigManager::new() 中
let config = if config_path.exists() {
    let content = std::fs::read_to_string(&config_path)?;
    let user_config: serde_json::Value = serde_json::from_str(&content)?;
    AppConfig::merge_with_default(user_config)
} else {
    AppConfig::default()
};

// merge_with_default 中处理新字段
impl AppConfig {
    pub fn merge_with_default(user_config: serde_json::Value) -> Self {
        let mut config = Self::default();
        
        // ... 现有字段处理 ...
        
        // 新增字段处理
        if let Some(v) = user_config.get("playlists") {
            if let Ok(playlists) = serde_json::from_value(v.clone()) {
                config.playlists = playlists;
            }
        }
        
        if let Some(v) = user_config.get("cyclePlaylistId").and_then(|v| v.as_str()) {
            config.cycle_playlist_id = Some(v.to_string());
        }
        
        if let Some(v) = user_config.get("playlistSidebarOpen").and_then(|v| v.as_bool()) {
            config.playlist_sidebar_open = v;
        }
        
        config
    }
}
```

## 6. 文件修改清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `lwg-rs/crates/lwg-core/src/config.rs` | 修改 | 新增 `Playlist` 结构体，扩展 `AppConfig` |
| `lwg-gui-tauri/src-tauri/src/lib.rs` | 修改 | 新增 CRUD 命令，修改轮换逻辑 |
| `lwg-gui-tauri/src-tauri/Cargo.toml` | 修改 | 添加 `uuid` 依赖 |

## 7. 依赖项

### 7.1 Cargo 依赖

```toml
# lwg-rs/crates/lwg-core/Cargo.toml 或 src-tauri/Cargo.toml
[dependencies]
uuid = { version = "1.0", features = ["v4", "serde"] }
```

### 7.2 已有依赖（无需新增）

- `serde`, `serde_json`: JSON 序列化
- `tokio`: 异步运行时
- `rand`: 随机选择

## 8. 测试计划

### 8.1 单元测试

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_playlist_creation() {
        let playlist = Playlist::new("Test".to_string(), vec!["1".to_string(), "2".to_string()]);
        assert!(!playlist.id.is_empty());
        assert_eq!(playlist.name, "Test");
        assert_eq!(playlist.wallpaper_ids.len(), 2);
    }
    
    #[test]
    fn test_select_next_wallpaper_with_playlist() {
        let playlists = vec![
            Playlist::new("Nature".to_string(), vec!["1".to_string(), "2".to_string(), "3".to_string()]),
        ];
        
        // 随机模式
        let result = select_next_wallpaper("random", None, &["1", "2", "3", "4", "5"], Some(&playlists[0].id), &playlists);
        assert!(["1", "2", "3"].contains(&result.as_str()));
        
        // 顺序模式
        let result1 = select_next_wallpaper("title", Some("1"), &["1", "2", "3", "4", "5"], Some(&playlists[0].id), &playlists);
        assert_eq!(result1, "2");
    }
    
    #[test]
    fn test_config_serialization() {
        let mut config = AppConfig::default();
        config.playlists.push(Playlist::new("Test".to_string(), vec!["1".to_string()]));
        
        let json = serde_json::to_string(&config).unwrap();
        assert!(json.contains("\"playlists\""));
        assert!(json.contains("\"wallpaperIds\""));  // camelCase
    }
    
    #[test]
    fn test_reorder_playlists_race_condition() {
        // 模拟竞态条件：后端有 [A, B, C, D]，但前端只发送 [A, B, C]
        let mut config = AppConfig::default();
        let p1 = Playlist::new("A".to_string(), vec![]);
        let p2 = Playlist::new("B".to_string(), vec![]);
        let p3 = Playlist::new("C".to_string(), vec![]);
        let p4 = Playlist::new("D".to_string(), vec![]);
        
        config.playlists = vec![p1.clone(), p2.clone(), p3.clone(), p4.clone()];
        
        // 模拟 reorder_playlists 逻辑
        let ordered_ids = vec![p3.id.clone(), p1.id.clone(), p2.id.clone()]; // 只包含 A, B, C
        let id_to_playlist: std::collections::HashMap<String, Playlist> = config.playlists
            .iter()
            .map(|p| (p.id.clone(), p.clone()))
            .collect();
        
        let mut new_playlists: Vec<Playlist> = Vec::new();
        let mut processed_ids: std::collections::HashSet<String> = std::collections::HashSet::new();
        
        for id in &ordered_ids {
            if let Some(playlist) = id_to_playlist.get(id) {
                new_playlists.push(playlist.clone());
                processed_ids.insert(id.clone());
            }
        }
        
        for playlist in &config.playlists {
            if !processed_ids.contains(&playlist.id) {
                new_playlists.push(playlist.clone());
            }
        }
        
        // 验证：D 应该被追加到末尾
        assert_eq!(new_playlists.len(), 4);
        assert_eq!(new_playlists[0].name, "C");
        assert_eq!(new_playlists[1].name, "A");
        assert_eq!(new_playlists[2].name, "B");
        assert_eq!(new_playlists[3].name, "D"); // 竞态产生的新列表被保留
    }
    
    #[test]
    fn test_dedup_wallpaper_ids_preserve_order() {
        // 测试完全去重但保留原始顺序
        let ids = vec!["1".to_string(), "2".to_string(), "1".to_string(), "3".to_string(), "2".to_string()];
        
        // 使用 HashSet 去重但保留顺序
        let mut seen = std::collections::HashSet::new();
        let deduped: Vec<String> = ids
            .into_iter()
            .filter(|id| seen.insert(id.clone()))
            .collect();
        
        // 验证：去重后保留首次出现的顺序
        assert_eq!(deduped, vec!["1", "2", "3"]);
    }
}
```

> ⚠️ **去重策略**：使用 `HashSet` 进行完全去重，同时保留元素首次出现的顺序。前端使用 `Array.from(new Set(...))`，后端使用 `HashSet` 过滤。

### 8.2 集成测试

- [ ] 创建列表后，`config.json` 包含正确数据
- [ ] 删除列表后，`config.json` 更新正确
- [ ] 重排序后，顺序保持
- [ ] 轮换指定列表时，只从列表中选择
- [ ] 删除轮换中的列表后，`cycle_playlist_id` 被清除
- [ ] **重复 ID 去重**：创建列表时传入重复 ID，后端自动去重
- [ ] **删除壁纸清理 Playlist**：删除壁纸后，所有 Playlist 中的该 ID 被移除

## 9. API 文档

### 9.1 get_playlists

```
GET /api/playlists

Response:
[
  {
    "id": "uuid",
    "name": "Nature",
    "wallpaperIds": ["2874425843", "2810924556"],
    "createdAt": 1700000000,
    "updatedAt": 1700000000
  }
]
```

### 9.2 create_playlist

```
POST /api/playlists

Request:
{
  "name": "Nature",
  "wallpaperIds": ["2874425843"]
}

Response:
{
  "id": "new-uuid",
  "name": "Nature",
  "wallpaperIds": ["2874425843"],
  "createdAt": 1700000000,
  "updatedAt": 1700000000
}
```

### 9.3 update_playlist

```
PATCH /api/playlists/:id

Request:
{
  "name": "New Name",
  "wallpaperIds": ["1", "2", "3"]
}

Response: null
```

### 9.4 delete_playlist

```
DELETE /api/playlists/:id

Response: null
```

### 9.5 reorder_playlists

```
POST /api/playlists/reorder

Request:
{
  "orderedIds": ["uuid-3", "uuid-1", "uuid-2"]
}

Response: null
```

### 9.6 set_cycle_playlist

```
POST /api/cycle-playlist

Request:
{
  "id": "uuid" | null
}

Response: null
```

## 10. 风险与注意事项

### 10.1 并发安全

- 使用 `tokio::sync::Mutex` 保护 `ConfigManager`
- 避免在 `.await` 时持有锁

### 10.2 数据验证

- 列表名称不能为空
- 壁纸 ID 列表可以为空（但会提示删除）
- UUID 格式验证

### 10.3 错误处理

- 列表不存在时返回友好错误
- 保存失败时回滚内存状态

## 11. 时间估算

| 任务 | 预估时间 |
|------|----------|
| 数据结构定义 | 30 分钟 |
| AppConfig 扩展 | 30 分钟 |
| CRUD 命令实现 | 1.5 小时 |
| 轮换逻辑修改 | 1 小时 |
| 配置迁移处理 | 30 分钟 |
| 测试编写 | 1 小时 |
| **总计** | **约 5 小时** |

---

## ⚠️ 执行约束

1. **前后端同步开发**：前端 appStore.ts 必须通过 invoke 调用后端命令，localStorage 仅作为浏览器开发 fallback
2. **保持向后兼容**：旧配置文件应能正常加载
3. **原子写入**：使用临时文件 + rename 确保配置文件完整性
4. **命令注册**：新增命令必须在 `invoke_handler` 中注册
5. **🚨 reorder_playlists 竞态安全**：必须使用安全合并策略，将未包含在排序请求中的新列表追加到末尾，而不是报错拒绝
6. **🚨 UUID 前端生成**：create_playlist 接收前端传来的 id，不在此命令内部生成
7. **🚨 空列表轮换安全**：select_next_wallpaper 必须处理空列表，优雅降级到全局库
8. **🚨 去重保护**：create_playlist 和 update_playlist 必须对 wallpaper_ids 使用 HashSet 完全去重，保留顺序

---

## ⚠️ 跨模块联动警告

> **关键**：Playlist 功能与现有的 `remove_wallpaper` 命令存在跨模块依赖！

### 删除壁纸时必须清理 Playlist 死链

当用户物理删除一张壁纸时，如果不清理 Playlist 中的残留 ID，会导致：
- 轮换时壁纸引擎找不到文件而崩溃
- 前端渲染时出现"残影壁纸"

### 修改 `remove_wallpaper` 命令

在 `src-tauri/src/lib.rs` 的 `remove_wallpaper` 命令中添加清理逻辑：

```rust
/// 删除壁纸（修改现有命令）
#[tauri::command]
async fn remove_wallpaper(
    id: String,
    path: String,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    // ... 现有删除逻辑 ...
    
    // 🚨 跨模块联动：清理所有 Playlist 中的死链 ID
    {
        let mut cm = state.config_manager.lock().await;
        let mut should_save = false;
        
        for playlist in cm.config_mut().playlists.iter_mut() {
            let original_len = playlist.wallpaper_ids.len();
            playlist.wallpaper_ids.retain(|wid| wid != &id);
            if playlist.wallpaper_ids.len() != original_len {
                should_save = true;
            }
        }
        
        if should_save {
            cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
        }
    }
    
    // ... 其余逻辑 ...
}
```

### 新增测试用例

```rust
#[test]
fn test_remove_wallpaper_cleans_playlists() {
    // 创建配置，包含一个 Playlist
    let mut config = AppConfig::default();
    let p1 = Playlist::new("Test".to_string(), vec!["wp-1".to_string(), "wp-2".to_string(), "wp-3".to_string()]);
    config.playlists = vec![p1];
    
    // 模拟删除 wp-2
    for playlist in config.playlists.iter_mut() {
        playlist.wallpaper_ids.retain(|id| id != "wp-2");
    }
    
    // 验证：wp-2 已从 Playlist 中移除
    assert_eq!(config.playlists[0].wallpaper_ids, vec!["wp-1", "wp-3"]);
}
```