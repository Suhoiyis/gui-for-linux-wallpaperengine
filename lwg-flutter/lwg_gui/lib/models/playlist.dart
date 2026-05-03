class Playlist {
  final String id;
  final String name;
  final List<String> wallpaperIds;
  final int createdAt;
  final int updatedAt;

  const Playlist({
    required this.id,
    required this.name,
    this.wallpaperIds = const [],
    required this.createdAt,
    required this.updatedAt,
  });

  Playlist copyWith({
    String? id,
    String? name,
    List<String>? wallpaperIds,
    int? createdAt,
    int? updatedAt,
  }) {
    return Playlist(
      id: id ?? this.id,
      name: name ?? this.name,
      wallpaperIds: wallpaperIds ?? this.wallpaperIds,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) || other is Playlist && id == other.id;

  @override
  int get hashCode => id.hashCode;
}