from __future__ import annotations

from pathlib import Path


WallpaperData = dict[str, str | int | float | bool | None | list[str]]


def to_file_uri(path_value: str | None) -> str:
    if not path_value:
        return ""
    try:
        return Path(path_value).resolve().as_uri()
    except (OSError, ValueError):
        return ""


def format_size_text(size_value: str | int | float | None) -> str:
    if isinstance(size_value, str):
        return size_value
    if size_value is None:
        return "0.0 MB"
    try:
        size_mb = float(size_value) / (1024.0 * 1024.0)
    except (TypeError, ValueError):
        return "0.0 MB"
    return f"{size_mb:.1f} MB"


def to_qt_wallpaper_item(
    wp_id: str, wallpaper: WallpaperData, workshop_path: str
) -> dict[str, str]:
    raw_size = wallpaper.get("size")
    parsed_size: str | int | float | None
    if isinstance(raw_size, bool):
        parsed_size = None
    elif isinstance(raw_size, (str, int, float)):
        parsed_size = raw_size
    else:
        parsed_size = None

    return {
        "id": wp_id,
        "title": str(wallpaper.get("title", "Unknown")),
        "preview": to_file_uri(str(wallpaper.get("preview", ""))),
        "type": str(wallpaper.get("type", "Scene")),
        "path": str(Path(workshop_path) / wp_id),
        "size": format_size_text(parsed_size),
    }


def to_qt_wallpaper_list(
    wallpapers: dict[str, WallpaperData], workshop_path: str
) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for wp_id, wallpaper in wallpapers.items():
        items.append(to_qt_wallpaper_item(str(wp_id), wallpaper, workshop_path))
    return items
