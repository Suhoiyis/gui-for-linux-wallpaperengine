use gtk4::gdk::Texture;
use lru::LruCache;
use std::num::NonZeroUsize;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct ThumbnailCache {
    cache: Arc<Mutex<LruCache<String, Texture>>>,
}

impl ThumbnailCache {
    pub fn new(capacity: usize) -> Self {
        Self {
            cache: Arc::new(Mutex::new(LruCache::new(
                NonZeroUsize::new(capacity).unwrap_or(NonZeroUsize::new(200).unwrap()),
            ))),
        }
    }

    pub async fn get(&self, key: &str) -> Option<Texture> {
        let mut cache = self.cache.lock().await;
        cache.get(key).cloned()
    }

    pub async fn insert(&self, key: String, texture: Texture) {
        let mut cache = self.cache.lock().await;
        cache.put(key, texture);
    }
}

impl Default for ThumbnailCache {
    fn default() -> Self {
        Self::new(200)
    }
}
