import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/theme/app_theme.dart';
import 'package:lwg_gui/providers/app_provider.dart';
import 'package:lwg_gui/models/wallpaper.dart';
import 'package:lwg_gui/components/wallpaper_card.dart';

class LibraryPage extends ConsumerWidget {
  const LibraryPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(appProvider);
    final notifier = ref.read(appProvider.notifier);
    final filtered = state.filteredWallpapers;

    return Column(
      children: [
        _buildHeader(context, state, notifier),
        _buildCategoryTabs(state, notifier),
        Expanded(
          child: state.wallpapers.isEmpty
              ? _buildEmptyState()
              : _buildWallpaperGrid(filtered),
        ),
      ],
    );
  }

  Widget _buildHeader(BuildContext context, AppState state, AppNotifier notifier) {
    return Container(
      padding: const EdgeInsets.all(24),
      child: Row(
        children: [
          Expanded(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              decoration: BoxDecoration(
                color: Colors.white.withValues(alpha: 0.05),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
              ),
              child: Row(
                children: [
                  Icon(Icons.search, color: Colors.white.withValues(alpha: 0.5)),
                  const SizedBox(width: 12),
                  Expanded(
                    child: TextField(
                      style: const TextStyle(color: Colors.white),
                      decoration: InputDecoration(
                        hintText: '搜索壁纸...',
                        hintStyle: TextStyle(color: Colors.white.withValues(alpha: 0.5)),
                        border: InputBorder.none,
                        contentPadding: const EdgeInsets.symmetric(vertical: 16),
                      ),
                      onChanged: (value) => notifier.setSearchQuery(value),
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(width: 16),
          _buildActionButton(Icons.filter_list, '筛选'),
          const SizedBox(width: 12),
          PopupMenuButton<SortBy>(
            icon: _buildActionButton(Icons.sort, '排序'),
            onSelected: (sort) => notifier.setSortBy(sort),
            itemBuilder: (context) => [
              const PopupMenuItem(value: SortBy.name, child: Text('按名称')),
              const PopupMenuItem(value: SortBy.id, child: Text('按ID')),
              const PopupMenuItem(value: SortBy.size, child: Text('按大小')),
            ],
          ),
          const SizedBox(width: 12),
          if (state.runtimeState.values.any((w) => w.isPlaying))
            ElevatedButton.icon(
              onPressed: () => notifier.stopWallpaper(),
              icon: const Icon(Icons.stop, size: 16),
              label: const Text('停止'),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppTheme.error.withValues(alpha: 0.2),
                foregroundColor: AppTheme.error,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildActionButton(IconData icon, String tooltip) {
    return Tooltip(
      message: tooltip,
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.white.withValues(alpha: 0.05),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
        ),
        child: Icon(icon, color: Colors.white70, size: 20),
      ),
    );
  }

  Widget _buildCategoryTabs(AppState state, AppNotifier notifier) {
    final categories = ['全部', '视频', '场景', '网页'];

    return Container(
      height: 50,
      padding: const EdgeInsets.symmetric(horizontal: 24),
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: categories.length + state.playlists.length,
        itemBuilder: (context, index) {
          if (index < categories.length) {
            final isSelected = state.activePlaylistId == null && index == 0;
            return Padding(
              padding: const EdgeInsets.only(right: 12),
              child: Material(
                color: Colors.transparent,
                child: InkWell(
                  onTap: () {
                    if (index == 0) notifier.setActivePlaylist(null);
                  },
                  borderRadius: BorderRadius.circular(20),
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                    decoration: BoxDecoration(
                      gradient: isSelected ? AppTheme.primaryGradient : null,
                      color: isSelected ? null : Colors.white.withValues(alpha: 0.05),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      categories[index],
                      style: TextStyle(
                        color: isSelected ? Colors.white : Colors.white70,
                        fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
                      ),
                    ),
                  ),
                ),
              ),
            );
          }
          final playlistIndex = index - categories.length;
          final playlist = state.playlists[playlistIndex];
          final isSelected = state.activePlaylistId == playlist.id;
          return Padding(
            padding: const EdgeInsets.only(right: 12),
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: () => notifier.setActivePlaylist(playlist.id),
                borderRadius: BorderRadius.circular(20),
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                  decoration: BoxDecoration(
                    gradient: isSelected ? AppTheme.primaryGradient : null,
                    color: isSelected ? null : Colors.white.withValues(alpha: 0.05),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.playlist_play, size: 16, color: isSelected ? Colors.white : Colors.white54),
                      const SizedBox(width: 4),
                      Text(
                        playlist.name,
                        style: TextStyle(
                          color: isSelected ? Colors.white : Colors.white70,
                          fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
                        ),
                      ),
                    ],
                  ),
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
          Icon(Icons.wallpaper_outlined, size: 64, color: Colors.white24),
          const SizedBox(height: 16),
          const Text('暂无壁纸', style: TextStyle(color: AppTheme.textSecondary, fontSize: 16)),
        ],
      ),
    );
  }

  Widget _buildWallpaperGrid(List<Wallpaper> wallpapers) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: GridView.builder(
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 4,
          childAspectRatio: 16 / 10,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
        ),
        itemCount: wallpapers.length,
        itemBuilder: (context, index) {
          return WallpaperCard(wallpaper: wallpapers[index]);
        },
      ),
    );
  }
}