use gtk4::prelude::*;
use gtk4::gdk::{self, Texture};

use lru::LruCache;
use std::num::NonZeroUsize;
use std::sync::Arc;
use std::path::Path;
use tokio::sync::Mutex;
use tracing::{debug, warn};

#[derive(Debug)]
pub struct ThumbnailCache {
    cache: Arc<Mutex<LruCache<String, Texture>>>,
}

impl ThumbnailCache {
    /// 创建新的缩略图缓存（容量 80）
    pub fn new(capacity: usize) -> Self {
        Self {
            cache: Arc::new(Mutex::new(LruCache::new(
                NonZeroUsize::new(capacity).unwrap_or(NonZeroUsize::new(80).unwrap()),
            ))),
        }
    }
    
    /// 获取缩略图
    pub async fn get(&self, key: &str) -> Option<Texture> {
        let mut cache = self.cache.lock().await;
        cache.get(key).cloned()
    }
    
    /// 插入缩略图
    pub async fn insert(&self, key: String, texture: Texture) {
        let mut cache = self.cache.lock().await;
        cache.put(key.clone(), texture);
        debug!("缩略图缓存：{} (当前大小：{})", key, cache.len());

        debug!("缩略图缓存：{} (当前大小：{})", key, cache.len());
    }
    
    /// 从文件加载缩略图（支持 JPG/PNG/GIF）
    pub fn load_from_file(path: &Path) -> Option<Texture> {
        if !path.exists() {
            warn!("缩略图文件不存在：{:?}", path);
            return None;
        }
        
        let extension = path.extension().and_then(|e| e.to_str()).unwrap_or("");
        
        match extension.to_lowercase().as_str() {
            "gif" => Self::load_gif_thumbnail(path),
            "jpg" | "jpeg" | "png" => Self::load_image_thumbnail(path),
            _ => {
                warn!("不支持的缩略图格式：{}", extension);
                None
            }
        }
    }
    
    fn load_image_thumbnail(path: &Path) -> Option<Texture> {
        let file = gtk4::gio::File::for_path(path);
        Texture::from_file(&file).ok()
    }

    
    fn load_gif_thumbnail(path: &Path) -> Option<Texture> {
        // 使用 image crate 读取 GIF
        let file = std::fs::File::open(path).ok()?;
        let mut decoder = gif::Decoder::new(file).ok()?;
        
        // 尝试提取第 15 帧（避免第一帧黑屏）
        let mut frame_num = 0;
        let mut target_frame = None;
        
        while let Ok(Some(frame)) = decoder.next_frame_info() {
            frame_num += 1;
            if frame_num == 15 {
                // 提取第 15 帧
                target_frame = Some(frame.clone());
                break;
            }
        }
        
        // 如果 GIF 少于 15 帧，使用最后一帧
        if target_frame.is_none() && frame_num > 0 {
            let file = std::fs::File::open(path).ok()?;
            let mut decoder = gif::Decoder::new(file).ok()?;
            let mut last_frame = None;
            
            while let Ok(Some(frame)) = decoder.next_frame_info() {
                last_frame = Some(frame.clone());
            }
            target_frame = last_frame;
        }
        
        if let Some(frame) = target_frame {
            // 转换为 RGBA
            let width = frame.width as u32;
            let height = frame.height as u32;
            let data = frame.buffer.to_vec();
            
            // 创建 Gdk::Texture
            let rowstride = width as usize * 4;
            let bytes = glib::Bytes::from(&data);
            
            Some(gdk::MemoryTexture::new(
                width as i32,
                height as i32,
                gdk::MemoryFormat::R8g8b8a8,
                &bytes,
                rowstride,
            ).upcast())
        } else {
            // 回退到直接加载
            let file = gtk4::gio::File::for_path(path);
            Texture::from_file(&file).ok()
        }
    }

    
    /// 清除所有缓存
    pub async fn clear(&self) {
        let mut cache = self.cache.lock().await;
        cache.clear();
        debug!("缩略图缓存已清空");
    }
    
    /// 获取缓存大小
    pub async fn len(&self) -> usize {
        let cache = self.cache.lock().await;
        cache.len()
    }
}

impl Default for ThumbnailCache {
    fn default() -> Self {
        Self::new(80)  // 默认容量 80
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_cache_capacity() {
        let cache = ThumbnailCache::new(80);
        assert_eq!(cache.cache.blocking_lock().capacity(), 80);
    }
}
