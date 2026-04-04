"""Python Backend - 暴露给 QML 的服务层（类似 Zustand Store）"""

import json
from typing import Optional
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl


class Backend(QObject):
    """Qt Quick 后端服务，提供状态管理和业务逻辑"""

    wallpapersChanged = Signal()
    selectedIdChanged = Signal()
    favoriteIdsChanged = Signal()

    def __init__(self):
        super().__init__()
        self._wallpapers = []
        self._selected_id: Optional[str] = None
        self._favorite_ids: set = set()
        self._load_mock_data()

    def _load_mock_data(self):
        """加载测试数据（PoC 阶段使用）"""
        self._wallpapers = [
            {
                "id": "2874425843",
                "title": "Cyberpunk City",
                "preview": "https://picsum.photos/seed/cyber/400/400",
                "type": "Web",
                "path": "/path/to/cyberpunk",
                "size": "45.2 MB",
            },
            {
                "id": "2810924556",
                "title": "Mountain Sunset",
                "preview": "https://picsum.photos/seed/mountain/400/400",
                "type": "Video",
                "path": "/path/to/mountain",
                "size": "128.5 MB",
            },
            {
                "id": "2915945682",
                "title": "Space Station",
                "preview": "https://picsum.photos/seed/space/400/400",
                "type": "Scene",
                "path": "/path/to/space",
                "size": "256.8 MB",
            },
            {
                "id": "2857246391",
                "title": "Rainy Tokyo",
                "preview": "https://picsum.photos/seed/tokyo/400/400",
                "type": "Web",
                "path": "/path/to/tokyo",
                "size": "67.3 MB",
            },
            {
                "id": "2893651874",
                "title": "Ocean Waves",
                "preview": "https://picsum.photos/seed/ocean/400/400",
                "type": "Video",
                "path": "/path/to/ocean",
                "size": "189.1 MB",
            },
            {
                "id": "2826519483",
                "title": "Fireplace",
                "preview": "https://picsum.photos/seed/fire/400/400",
                "type": "Video",
                "path": "/path/to/fireplace",
                "size": "52.4 MB",
            },
        ]
        self.wallpapersChanged.emit()

    @Property(list, notify=wallpapersChanged)
    def wallpapers(self):
        return self._wallpapers

    @Property(str, notify=selectedIdChanged)
    def selectedId(self):
        return self._selected_id or ""

    @Property(list, notify=favoriteIdsChanged)
    def favoriteIds(self):
        return list(self._favorite_ids)

    @Slot(str)
    def selectWallpaper(self, wp_id: str):
        self._selected_id = wp_id
        self.selectedIdChanged.emit()
        print(f"[Backend] Selected: {wp_id}")

    @Slot(str)
    def applyWallpaper(self, wp_id: str):
        print(f"[Backend] Apply wallpaper: {wp_id}")

    @Slot(str)
    def toggleFavorite(self, wp_id: str):
        if wp_id in self._favorite_ids:
            self._favorite_ids.remove(wp_id)
            print(f"[Backend] Removed from favorites: {wp_id}")
        else:
            self._favorite_ids.add(wp_id)
            print(f"[Backend] Added to favorites: {wp_id}")
        self.favoriteIdsChanged.emit()

    @Slot(str, result=bool)
    def isFavorite(self, wp_id: str) -> bool:
        return wp_id in self._favorite_ids

    @Slot(None)
    def refresh(self):
        self._load_mock_data()
        print("[Backend] Refreshed wallpapers")
