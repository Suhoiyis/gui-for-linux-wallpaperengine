import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/theme/app_theme.dart';
import 'package:lwg_gui/providers/app_provider.dart';
import 'package:lwg_gui/models/wallpaper.dart';

class WallpaperCard extends ConsumerStatefulWidget {
  final Wallpaper wallpaper;

  const WallpaperCard({super.key, required this.wallpaper});

  @override
  ConsumerState<WallpaperCard> createState() => _WallpaperCardState();
}

class _WallpaperCardState extends ConsumerState<WallpaperCard> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(appProvider);
    final notifier = ref.read(appProvider.notifier);
    final isFavorite = state.isFavorite(widget.wallpaper.id);
    final isSelected = state.selectedId == widget.wallpaper.id;

    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      child: GestureDetector(
        onTap: () => notifier.setSelectedId(widget.wallpaper.id),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOutCubic,
          transform: Matrix4.identity()..scale(_isHovered ? 1.02 : 1.0),
          child: Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(16),
              border: isSelected ? Border.all(color: AppTheme.primary, width: 2) : null,
              boxShadow: [
                BoxShadow(
                  color: _typeColor().withValues(alpha: _isHovered ? 0.4 : 0.2),
                  blurRadius: _isHovered ? 20 : 10,
                  spreadRadius: _isHovered ? 2 : 0,
                  offset: const Offset(0, 8),
                ),
              ],
            ),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: Stack(
                fit: StackFit.expand,
                children: [
                  Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [_typeColor().withValues(alpha: 0.8), _typeColor().withValues(alpha: 0.4)],
                      ),
                    ),
                  ),
                  Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                        colors: [Colors.white.withValues(alpha: 0.1), Colors.transparent],
                      ),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.end,
                          children: [
                            AnimatedOpacity(
                              duration: const Duration(milliseconds: 200),
                              opacity: _isHovered ? 1 : 0,
                              child: GestureDetector(
                                onTap: () => notifier.toggleFavorite(widget.wallpaper.id),
                                child: Container(
                                  padding: const EdgeInsets.all(6),
                                  decoration: BoxDecoration(
                                    color: Colors.white.withValues(alpha: 0.2),
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                  child: Icon(
                                    isFavorite ? Icons.favorite : Icons.favorite_border,
                                    color: isFavorite ? AppTheme.error : Colors.white,
                                    size: 16,
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                        const Spacer(),
                        Text(
                          widget.wallpaper.title,
                          style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
                          overflow: TextOverflow.ellipsis,
                          maxLines: 1,
                        ),
                        const SizedBox(height: 2),
                        Row(
                          children: [
                            Flexible(child: Text(
                              widget.wallpaper.size,
                              style: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 11),
                              overflow: TextOverflow.ellipsis,
                            )),
                            const SizedBox(width: 6),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                              decoration: BoxDecoration(
                                color: AppTheme.primary.withValues(alpha: 0.3),
                                borderRadius: BorderRadius.circular(3),
                              ),
                              child: Text(
                                _typeLabel(),
                                style: const TextStyle(color: Colors.white, fontSize: 9),
                              ),
                            ),
                          ],
                        ),
                        if (_isHovered)
                          Padding(
                            padding: const EdgeInsets.only(top: 8),
                            child: GestureDetector(
                              onTap: () => notifier.applyWallpaper(widget.wallpaper.id, null),
                              child: Container(
                                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                decoration: BoxDecoration(
                                  gradient: AppTheme.primaryGradient,
                                  borderRadius: BorderRadius.circular(6),
                                ),
                                child: const Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Icon(Icons.play_arrow, color: Colors.white, size: 14),
                                    SizedBox(width: 4),
                                    Text('应用', style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w600)),
                                  ],
                                ),
                              ),
                            ),
                          ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Color _typeColor() {
    return switch (widget.wallpaper.type) {
      WallpaperType.video => const Color(0xFF3B82F6),
      WallpaperType.scene => const Color(0xFF10B981),
      WallpaperType.web => const Color(0xFFF59E0B),
    };
  }

  String _typeLabel() {
    return switch (widget.wallpaper.type) {
      WallpaperType.video => '视频',
      WallpaperType.scene => '场景',
      WallpaperType.web => '网页',
    };
  }
}