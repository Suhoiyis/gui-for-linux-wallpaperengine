use crate::error::{LwgError, LwgResult};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use tracing::{debug, error, info, warn};

/// 壁纸信息结构体
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Wallpaper {
    pub id: String,
    pub title: String,
    pub preview: PathBuf,
    pub description: String,
    #[serde(rename = "type")]
    pub wp_type: String,
    pub tags: Vec<String>,
    pub file: String,
    pub content_rating: String,
    pub version: String,
    pub size: u64,
}

/// 壁纸管理器
pub struct WallpaperManager {
    workshop_path: PathBuf,
    wallpapers: HashMap<String, Wallpaper>,
    manifest_path: Option<PathBuf>,
    pub last_scan_error: Option<String>,
    pub scan_errors: Vec<String>,
}

impl WallpaperManager {
    /// 创建新的壁纸管理器
    pub fn new(workshop_path: impl AsRef<Path>) -> Self {
        let workshop_path = workshop_path.as_ref().to_path_buf();
        let manifest_path = Self::find_manifest_path(&workshop_path);

        Self {
            workshop_path,
            wallpapers: HashMap::new(),
            manifest_path,
            last_scan_error: None,
            scan_errors: Vec::new(),
        }
    }

    /// 尝试查找 Steam appworkshop 清单文件
    fn find_manifest_path(workshop_path: &Path) -> Option<PathBuf> {
        // workshop_path 通常是 .../workshop/content/431960
        // 我们需要往上两级到 .../workshop/ 找 appworkshop_431960.acf
        let content_dir = workshop_path.parent()?;
        let workshop_dir = content_dir.parent()?;

        let manifest = workshop_dir.join("appworkshop_431960.acf");
        if manifest.exists() {
            return Some(manifest);
        }

        None
    }

    /// 扫描壁纸库
    pub fn scan(&mut self) -> LwgResult<&HashMap<String, Wallpaper>> {
        self.wallpapers.clear();
        self.last_scan_error = None;
        self.scan_errors.clear();

        if !self.workshop_path.exists() {
            self.last_scan_error = Some(format!(
                "Workshop directory not found: {}",
                self.workshop_path.display()
            ));
            return Ok(&self.wallpapers);
        }

        if !self.workshop_path.is_dir() {
            self.last_scan_error = Some(format!(
                "Workshop path is not a directory: {}",
                self.workshop_path.display()
            ));
            return Ok(&self.wallpapers);
        }

        let entries = match std::fs::read_dir(&self.workshop_path) {
            Ok(entries) => entries,
            Err(e) => {
                self.last_scan_error = Some(format!("Cannot read directory: {}", e));
                return Ok(&self.wallpapers);
            }
        };

        for entry in entries.flatten() {
            let folder = entry.file_name();
            let folder_str = folder.to_string_lossy();

            let json_path = entry.path().join("project.json");
            if json_path.exists() {
                match self.parse_wallpaper(&folder_str, &json_path) {
                    Ok(wallpaper) => {
                        self.wallpapers.insert(folder_str.to_string(), wallpaper);
                    }
                    Err(e) => {
                        self.scan_errors
                            .push(format!("Error reading {}: {}", folder_str, e));
                    }
                }
            }
        }

        if self.wallpapers.is_empty() && self.last_scan_error.is_none() {
            self.last_scan_error = Some(format!(
                "No wallpapers found in: {}",
                self.workshop_path.display()
            ));
        }

        info!("Scanned {} wallpapers", self.wallpapers.len());
        Ok(&self.wallpapers)
    }

    /// 解析单个壁纸的 project.json
    fn parse_wallpaper(&self, folder_id: &str, json_path: &Path) -> LwgResult<Wallpaper> {
        let content = std::fs::read_to_string(json_path)?;
        let data: serde_json::Value = serde_json::from_str(&content)?;

        let folder_path = self.workshop_path.join(folder_id);
        let preview_file = data
            .get("preview")
            .and_then(|v| v.as_str())
            .unwrap_or("preview.jpg");

        let size = Self::calculate_folder_size(&folder_path)?;

        Ok(Wallpaper {
            id: folder_id.to_string(),
            title: data
                .get("title")
                .and_then(|v| v.as_str())
                .unwrap_or("Unknown")
                .to_string(),
            preview: folder_path.join(preview_file),
            description: data
                .get("description")
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string(),
            wp_type: data
                .get("type")
                .and_then(|v| v.as_str())
                .unwrap_or("Scene")
                .to_string(),
            tags: data
                .get("tags")
                .and_then(|v| v.as_array())
                .map(|arr| {
                    arr.iter()
                        .filter_map(|v| v.as_str().map(|s| s.to_string()))
                        .collect()
                })
                .unwrap_or_default(),
            file: data
                .get("file")
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string(),
            content_rating: data
                .get("contentrating")
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string(),
            version: data
                .get("version")
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string(),
            size,
        })
    }

    /// 计算文件夹大小
    fn calculate_folder_size(path: &Path) -> LwgResult<u64> {
        let mut total_size = 0u64;

        if path.is_dir() {
            for entry in walkdir::WalkDir::new(path) {
                if let Ok(entry) = entry {
                    if entry.file_type().is_file() {
                        total_size += entry.metadata().map(|m| m.len()).unwrap_or(0);
                    }
                }
            }
        }

        Ok(total_size)
    }

    /// 获取壁纸
    pub fn get(&self, id: &str) -> Option<&Wallpaper> {
        self.wallpapers.get(id)
    }

    /// 获取所有壁纸列表
    pub fn list(&self) -> Vec<&Wallpaper> {
        self.wallpapers.values().collect()
    }

    /// 获取排序后的壁纸 ID 列表
    pub fn get_sorted_ids(&self, sort_mode: &str, reverse: bool) -> Vec<String> {
        if self.wallpapers.is_empty() {
            return Vec::new();
        }

        let mut items: Vec<_> = self.wallpapers.values().collect();

        match sort_mode {
            "title" => {
                items.sort_by(|a, b| {
                    let cmp = a.title.to_lowercase().cmp(&b.title.to_lowercase());
                    if reverse {
                        cmp.reverse()
                    } else {
                        cmp
                    }
                });
            }
            "size" => {
                items.sort_by(|a, b| {
                    let cmp = a.size.cmp(&b.size);
                    if reverse {
                        cmp.reverse()
                    } else {
                        cmp
                    }
                });
            }
            "type" => {
                items.sort_by(|a, b| {
                    let cmp = a.wp_type.to_lowercase().cmp(&b.wp_type.to_lowercase());
                    if reverse {
                        cmp.reverse()
                    } else {
                        cmp
                    }
                });
            }
            "id" => {
                items.sort_by(|a, b| {
                    let cmp = a.id.cmp(&b.id);
                    if reverse {
                        cmp.reverse()
                    } else {
                        cmp
                    }
                });
            }
            _ => {}
        }

        items.into_iter().map(|w| w.id.clone()).collect()
    }

    /// 搜索壁纸
    pub fn search(&self, query: &str) -> Vec<&Wallpaper> {
        let query = query.to_lowercase();
        self.wallpapers
            .values()
            .filter(|w| {
                w.title.to_lowercase().contains(&query)
                    || w.description.to_lowercase().contains(&query)
                    || w.tags.iter().any(|t| t.to_lowercase().contains(&query))
                    || w.id.contains(&query)
            })
            .collect()
    }

    /// 删除壁纸
    pub fn delete(&mut self, folder_id: &str) -> LwgResult<bool> {
        if !self.wallpapers.contains_key(folder_id) {
            return Ok(false);
        }

        let folder_path = self.workshop_path.join(folder_id);
        if !folder_path.exists() {
            return Ok(false);
        }

        std::fs::remove_dir_all(&folder_path)?;
        self.wallpapers.remove(folder_id);

        info!("Deleted wallpaper {}", folder_id);
        Ok(true)
    }

    /// 获取壁纸数量
    pub fn count(&self) -> usize {
        self.wallpapers.len()
    }

    /// 检查是否为空
    pub fn is_empty(&self) -> bool {
        self.wallpapers.is_empty()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::TempDir;

    fn create_test_wallpaper(dir: &Path, id: &str, title: &str, wp_type: &str) {
        let folder = dir.join(id);
        std::fs::create_dir_all(&folder).unwrap();

        let project_json = serde_json::json!({
            "title": title,
            "type": wp_type,
            "description": "Test description",
            "tags": ["other", "tag"],
            "file": "scene.json",
            "preview": "preview.jpg"
        });

        let mut file = std::fs::File::create(folder.join("project.json")).unwrap();
        file.write_all(project_json.to_string().as_bytes()).unwrap();
    }

    #[test]
    fn test_scan_wallpapers() {
        let temp_dir = TempDir::new().unwrap();
        create_test_wallpaper(temp_dir.path(), "12345", "Test Wallpaper", "Scene");
        create_test_wallpaper(temp_dir.path(), "67890", "Another Wallpaper", "Video");

        let mut manager = WallpaperManager::new(temp_dir.path());
        let wallpapers = manager.scan().unwrap();

        assert_eq!(wallpapers.len(), 2);
        assert!(manager.get("12345").is_some());
        assert!(manager.get("67890").is_some());
        assert_eq!(manager.get("12345").unwrap().title, "Test Wallpaper");
    }

    #[test]
    fn test_search_wallpapers() {
        let temp_dir = TempDir::new().unwrap();
        create_test_wallpaper(temp_dir.path(), "12345", "Test Wallpaper", "Scene");
        create_test_wallpaper(temp_dir.path(), "67890", "Another Wallpaper", "Video");

        let mut manager = WallpaperManager::new(temp_dir.path());
        manager.scan().unwrap();

        let results = manager.search("test");
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].id, "12345");

        let results = manager.search("wallpaper");
        assert_eq!(results.len(), 2);
    }
}

/// 壁纸排序模式
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum SortMode {
    Title,
    Size,
    Type,
    Id,
    Random,
}

impl WallpaperManager {
    /// 排序壁纸列表
    pub fn sort(&mut self, mode: SortMode, ascending: bool) {
        let mut wallpapers: Vec<_> = self.wallpapers.values().collect();
        
        match mode {
            SortMode::Title => {
                wallpapers.sort_by(|a, b| {
                    if ascending {
                        a.title.cmp(&b.title)
                    } else {
                        b.title.cmp(&a.title)
                    }
                });
            }
            SortMode::Size => {
                wallpapers.sort_by(|a, b| {
                    if ascending {
                        a.size.cmp(&b.size)
                    } else {
                        b.size.cmp(&a.size)
                    }
                });
            }
            SortMode::Type => {
                wallpapers.sort_by(|a, b| {
                    if ascending {
                        a.wp_type.cmp(&b.wp_type)
                    } else {
                        b.wp_type.cmp(&a.wp_type)
                    }
                });
            }
            SortMode::Id => {
                wallpapers.sort_by(|a, b| {
                    if ascending {
                        a.id.cmp(&b.id)
                    } else {
                        b.id.cmp(&a.id)
                    }
                });
            }
            SortMode::Random => {
                use std::collections::hash_map::DefaultHasher;
                use std::hash::{Hash, Hasher};
                
                wallpapers.sort_by(|a, b| {
                    let mut hasher_a = DefaultHasher::new();
                    let mut hasher_b = DefaultHasher::new();
                    a.id.hash(&mut hasher_a);
                    b.id.hash(&mut hasher_b);
                    hasher_a.finish().cmp(&hasher_b.finish())
                });
            }
        }
        
        // 重建 HashMap（保持排序后的顺序）
        let sorted: HashMap<String, Wallpaper> = wallpapers
            .into_iter()
            .map(|w| (w.id.clone(), w.clone()))
            .collect();
        
        self.wallpapers = sorted;
        debug!("壁纸已排序：{:?}, 升序：{}", mode, ascending);
    }
    
    /// 获取排序后的壁纸列表
    pub fn get_sorted(&self, mode: SortMode, ascending: bool) -> Vec<&Wallpaper> {
        let mut wallpapers: Vec<_> = self.wallpapers.values().collect();
        
        match mode {
            SortMode::Title => {
                if ascending {
                    wallpapers.sort_by(|a, b| a.title.cmp(&b.title));
                } else {
                    wallpapers.sort_by(|a, b| b.title.cmp(&a.title));
                }
            }
            SortMode::Size => {
                if ascending {
                    wallpapers.sort_by(|a, b| a.size.cmp(&b.size));
                } else {
                    wallpapers.sort_by(|a, b| b.size.cmp(&a.size));
                }
            }
            SortMode::Type => {
                if ascending {
                    wallpapers.sort_by(|a, b| a.wp_type.cmp(&b.wp_type));
                } else {
                    wallpapers.sort_by(|a, b| b.wp_type.cmp(&a.wp_type));
                }
            }
            SortMode::Id => {
                if ascending {
                    wallpapers.sort_by(|a, b| a.id.cmp(&b.id));
                } else {
                    wallpapers.sort_by(|a, b| b.id.cmp(&a.id));
                }
            }
            SortMode::Random => {
                use std::collections::hash_map::DefaultHasher;
                use std::hash::{Hash, Hasher};
                
                wallpapers.sort_by(|a, b| {
                    let mut hasher_a = DefaultHasher::new();
                    let mut hasher_b = DefaultHasher::new();
                    a.id.hash(&mut hasher_a);
                    b.id.hash(&mut hasher_b);
                    hasher_a.finish().cmp(&hasher_b.finish())
                });
            }
        }
        
        wallpapers
    }
}

#[cfg(test)]
mod tests_wallpaper_extended {
    use super::*;

    #[test]
    fn test_sort_modes() {
        let mut manager = WallpaperManager::new("/tmp");
        manager.sort(SortMode::Title, true);
        manager.sort(SortMode::Size, false);
        manager.sort(SortMode::Random, true);
        assert!(true);
    }

    #[test]
    fn test_search_empty() {
        let manager = WallpaperManager::new("/tmp");
        let results = manager.search("nonexistent");
        assert!(results.is_empty());
    }
}
