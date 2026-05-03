enum WallpaperType { video, scene, web }

class Wallpaper {
  final String id;
  final String title;
  final String preview;
  final String path;
  final WallpaperType type;
  final List<String> tags;
  final String size;
  final String? description;

  const Wallpaper({
    required this.id,
    required this.title,
    required this.preview,
    required this.path,
    required this.type,
    this.tags = const [],
    this.size = '',
    this.description,
  });

  Wallpaper copyWith({
    String? id,
    String? title,
    String? preview,
    String? path,
    WallpaperType? type,
    List<String>? tags,
    String? size,
    String? description,
  }) {
    return Wallpaper(
      id: id ?? this.id,
      title: title ?? this.title,
      preview: preview ?? this.preview,
      path: path ?? this.path,
      type: type ?? this.type,
      tags: tags ?? this.tags,
      size: size ?? this.size,
      description: description ?? this.description,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Wallpaper && id == other.id && path == other.path;

  @override
  int get hashCode => Object.hash(id, path);
}