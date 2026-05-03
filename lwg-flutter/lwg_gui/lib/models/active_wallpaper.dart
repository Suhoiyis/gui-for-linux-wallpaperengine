class ActiveWallpaper {
  final String wallpaperId;
  final bool isPlaying;

  const ActiveWallpaper({
    required this.wallpaperId,
    this.isPlaying = false,
  });

  ActiveWallpaper copyWith({
    String? wallpaperId,
    bool? isPlaying,
  }) {
    return ActiveWallpaper(
      wallpaperId: wallpaperId ?? this.wallpaperId,
      isPlaying: isPlaying ?? this.isPlaying,
    );
  }
}