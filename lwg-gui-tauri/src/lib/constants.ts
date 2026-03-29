/**
 * 特殊播放列表 ID 常量
 */

/**
 * Favorites 播放列表 ID
 * 这是一个虚拟播放列表，不在 playlists 数组中，由 favoriteIds 驱动
 */
export const FAVORITES_PLAYLIST_ID = "__favorites__";

/**
 * 检查是否为特殊播放列表 ID
 */
export function isSpecialPlaylistId(id: string | null): boolean {
  return id === FAVORITES_PLAYLIST_ID;
}