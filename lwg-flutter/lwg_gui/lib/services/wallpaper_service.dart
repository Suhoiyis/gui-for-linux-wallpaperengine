import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/models/wallpaper.dart';
import 'package:lwg_gui/models/playlist.dart';
import 'package:lwg_gui/services/platform_service.dart';

class WallpaperService {
  final PlatformService _platform;

  WallpaperService(this._platform);

  Future<List<Wallpaper>> scanWallpapers() async {
    final raw = await _platform.invoke('get_wallpapers');
    if (raw == null) return _mockWallpapers();
    final list = raw as List;
    return list.map((item) {
      final map = item as Map;
      return Wallpaper(
        id: map['id'] as String,
        title: map['title'] as String,
        preview: map['preview'] as String,
        path: map['path'] as String,
        type: _parseType(map['type'] as String),
        tags: (map['tags'] as List?)?.cast<String>() ?? [],
        size: map['size'] as String? ?? '',
        description: map['description'] as String?,
      );
    }).toList();
  }

  Future<void> applyWallpaper(String id, String screen) async {
    await _platform.invoke('apply_wallpaper', {'id': id, 'screen': screen});
  }

  Future<void> stopWallpaper() async {
    await _platform.invoke('stop_wallpaper');
  }

  Future<void> deleteWallpaper(String id, String path) async {
    await _platform.invoke('delete_wallpaper', {'id': id, 'path': path});
  }

  Future<List<String>> getMonitors() async {
    final result = await _platform.invoke('get_connected_monitors');
    if (result == null) return ['HDMI-1', 'DP-1'];
    return (result as List).cast<String>();
  }

  Future<List<Playlist>> getPlaylists() async {
    final result = await _platform.invoke('get_playlists');
    if (result == null) return [];
    final list = result as List;
    return list.map((item) {
      final map = item as Map;
      return Playlist(
        id: map['id'] as String,
        name: map['name'] as String,
        wallpaperIds: (map['wallpaperIds'] as List?)?.cast<String>() ?? [],
        createdAt: map['createdAt'] as int,
        updatedAt: map['updatedAt'] as int,
      );
    }).toList();
  }

  WallpaperType _parseType(String type) {
    return switch (type.toLowerCase()) {
      'video' => WallpaperType.video,
      'scene' => WallpaperType.scene,
      'web' => WallpaperType.web,
      _ => WallpaperType.video,
    };
  }

  List<Wallpaper> _mockWallpapers() {
    final types = ['风景', '动漫', '游戏', '抽象', '城市', '自然'];
    final typeEnums = [
      WallpaperType.scene,
      WallpaperType.video,
      WallpaperType.web,
      WallpaperType.scene,
      WallpaperType.video,
      WallpaperType.scene,
    ];
    return List.generate(20, (i) {
      final catIndex = i % types.length;
      return Wallpaper(
        id: '${1000 + i}',
        title: '${types[catIndex]}壁纸 ${i + 1}',
        preview: '',
        path: '/tmp/wallpaper_${i + 1}',
        type: typeEnums[catIndex],
        tags: [types[catIndex], 'popular'],
        size: '${(i + 1) * 5}MB',
        description: '这是一张${types[catIndex]}类型的壁纸',
      );
    });
  }
}

final wallpaperServiceProvider = Provider<WallpaperService>((ref) {
  return WallpaperService(ref.read(platformServiceProvider));
});