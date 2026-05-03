import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/theme/app_theme.dart';
import 'package:lwg_gui/providers/app_provider.dart';
import 'package:lwg_gui/models/wallpaper.dart';

class CompactPage extends ConsumerStatefulWidget {
  const CompactPage({super.key});

  @override
  ConsumerState<CompactPage> createState() => _CompactPageState();
}

class _CompactPageState extends ConsumerState<CompactPage> {
  int _currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(appProvider);
    final notifier = ref.read(appProvider.notifier);
    final wallpapers = state.filteredWallpapers;
    if (wallpapers.isEmpty) return _buildEmptyState();

    final current = wallpapers[_currentIndex % wallpapers.length];
    final isPlaying = state.runtimeState.values.any((w) => w.isPlaying);

    return Column(
      children: [
        _buildCompactNavbar(state, notifier),
        Expanded(
          child: SingleChildScrollView(
            child: Column(
              children: [
                _buildPreview(current, isPlaying),
                _buildMetadata(current, notifier),
              ],
            ),
          ),
        ),
        _buildCarousel(wallpapers),
      ],
    );
  }

  Widget _buildCompactNavbar(AppState state, AppNotifier notifier) {
    final isPlaying = state.runtimeState.values.any((w) => w.isPlaying);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(color: AppTheme.surface),
      child: Row(
        children: [
          IconButton(
            icon: Icon(Icons.open_in_full, color: AppTheme.textSecondary, size: 18),
            tooltip: '正常模式',
            onPressed: () => notifier.toggleCompactMode(false),
          ),
          if (isPlaying)
            IconButton(
              icon: Icon(Icons.stop, color: AppTheme.error, size: 18),
              tooltip: '停止',
              onPressed: () => notifier.stopWallpaper(),
            ),
          const Spacer(),
          Text(
            state.selectedWallpaper?.title ?? '壁纸',
            style: const TextStyle(color: Colors.white, fontSize: 14),
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }

  Widget _buildPreview(Wallpaper wallpaper, bool isPlaying) {
    return Container(
      height: 250,
      margin: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [_typeColor(wallpaper).withValues(alpha: 0.6), _typeColor(wallpaper).withValues(alpha: 0.3)],
        ),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Stack(
        children: [
          Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.wallpaper, color: Colors.white.withValues(alpha: 0.5), size: 48),
                const SizedBox(height: 8),
                Text(wallpaper.title, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w600)),
              ],
            ),
          ),
          if (isPlaying)
            Positioned(
              top: 8,
              right: 8,
              child: Container(
                padding: const EdgeInsets.all(6),
                decoration: BoxDecoration(color: AppTheme.success.withValues(alpha: 0.2), borderRadius: BorderRadius.circular(8)),
                child: Icon(Icons.play_circle, color: AppTheme.success, size: 16),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildMetadata(Wallpaper wallpaper, AppNotifier notifier) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(wallpaper.size, style: const TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(color: AppTheme.primary.withValues(alpha: 0.3), borderRadius: BorderRadius.circular(4)),
                child: Text(_typeLabel(wallpaper), style: const TextStyle(color: Colors.white, fontSize: 10)),
              ),
            ],
          ),
          const SizedBox(height: 8),
          ElevatedButton.icon(
            onPressed: () => notifier.applyWallpaper(wallpaper.id, null),
            icon: const Icon(Icons.play_arrow, size: 16),
            label: const Text('应用'),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primary,
              foregroundColor: Colors.white,
              minimumSize: const Size(double.infinity, 36),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCarousel(List<Wallpaper> wallpapers) {
    return Container(
      height: 60,
      margin: const EdgeInsets.only(bottom: 4),
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: wallpapers.length,
        itemBuilder: (context, index) {
          final w = wallpapers[index];
          final isSelected = index == _currentIndex % wallpapers.length;
          return GestureDetector(
            onTap: () {
              setState(() => _currentIndex = index);
              ref.read(appProvider.notifier).setSelectedId(w.id);
            },
            child: Container(
              width: 80,
              margin: const EdgeInsets.symmetric(horizontal: 4),
              decoration: BoxDecoration(
                gradient: LinearGradient(colors: [_typeColor(w).withValues(alpha: isSelected ? 0.8 : 0.4), _typeColor(w).withValues(alpha: isSelected ? 0.5 : 0.2)]),
                borderRadius: BorderRadius.circular(8),
                border: isSelected ? Border.all(color: AppTheme.primary, width: 2) : null,
              ),
              child: Center(
                child: Text(
                  w.title,
                  style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: isSelected ? FontWeight.bold : FontWeight.normal),
                  overflow: TextOverflow.ellipsis,
                  textAlign: TextAlign.center,
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.wallpaper_outlined, size: 48, color: Colors.white24),
          const SizedBox(height: 16),
          const Text('暂无壁纸', style: TextStyle(color: AppTheme.textSecondary)),
        ],
      ),
    );
  }

  Color _typeColor(Wallpaper w) {
    return switch (w.type) {
      WallpaperType.video => const Color(0xFF3B82F6),
      WallpaperType.scene => const Color(0xFF10B981),
      WallpaperType.web => const Color(0xFFF59E0B),
    };
  }

  String _typeLabel(Wallpaper w) {
    return switch (w.type) {
      WallpaperType.video => '视频',
      WallpaperType.scene => '场景',
      WallpaperType.web => '网页',
    };
  }
}