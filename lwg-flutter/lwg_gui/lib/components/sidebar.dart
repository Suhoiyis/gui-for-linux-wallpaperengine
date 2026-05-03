import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/theme/app_theme.dart';
import 'package:lwg_gui/providers/app_provider.dart';

class Sidebar extends ConsumerWidget {
  const Sidebar({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(appProvider);
    final notifier = ref.read(appProvider.notifier);

    final navItems = [
      NavItem(icon: Icons.dashboard_outlined, label: '库', tab: AppTab.wallpapers),
      NavItem(icon: Icons.settings_outlined, label: '设置', tab: AppTab.settings),
      NavItem(icon: Icons.speed_outlined, label: '性能', tab: AppTab.performance),
    ];

    return Container(
      width: 240,
      decoration: BoxDecoration(
        gradient: AppTheme.surfaceGradient,
        borderRadius: const BorderRadius.horizontal(right: Radius.circular(24)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.3),
            blurRadius: 20,
            offset: const Offset(4, 0),
          ),
        ],
      ),
      child: Column(
        children: [
          const SizedBox(height: 40),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: AppTheme.primaryGradient,
              boxShadow: [
                BoxShadow(
                  color: AppTheme.primary.withValues(alpha: 0.4),
                  blurRadius: 20,
                  spreadRadius: 5,
                ),
              ],
            ),
            child: const Icon(Icons.wallpaper, size: 40, color: Colors.white),
          ),
          const SizedBox(height: 16),
          const Text(
            'Wallpaper Engine',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
          ),
          const SizedBox(height: 40),
          ...navItems.map((item) => _buildNavItem(item, state, notifier)),
          const Spacer(),
          _buildStatusIndicator(state),
        ],
      ),
    );
  }

  Widget _buildNavItem(NavItem item, AppState state, AppNotifier notifier) {
    final isSelected = state.activeTab == item.tab;
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => notifier.setActiveTab(item.tab),
          borderRadius: BorderRadius.circular(12),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              gradient: isSelected
                  ? LinearGradient(colors: [
                      AppTheme.primary.withValues(alpha: 0.3),
                      AppTheme.secondary.withValues(alpha: 0.1),
                    ])
                  : null,
              borderRadius: BorderRadius.circular(12),
              border: isSelected ? Border.all(color: AppTheme.primary.withValues(alpha: 0.5)) : null,
            ),
            child: Row(
              children: [
                Icon(item.icon, color: isSelected ? AppTheme.primary : Colors.white54, size: 22),
                const SizedBox(width: 12),
                Text(
                  item.label,
                  style: TextStyle(
                    color: isSelected ? Colors.white : Colors.white54,
                    fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildStatusIndicator(AppState state) {
    final isPlaying = state.runtimeState.values.any((w) => w.isPlaying);
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.white.withValues(alpha: 0.05),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
        ),
        child: Row(
          children: [
            Container(
              width: 8,
              height: 8,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isPlaying ? AppTheme.success : Colors.grey,
              ),
            ),
            const SizedBox(width: 8),
            Text(
              isPlaying ? '运行中' : '已停止',
              style: const TextStyle(fontSize: 12, color: AppTheme.textSecondary),
            ),
          ],
        ),
      ),
    );
  }
}

class NavItem {
  final IconData icon;
  final String label;
  final AppTab tab;

  const NavItem({required this.icon, required this.label, required this.tab});
}