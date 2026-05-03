import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/theme/app_theme.dart';
import 'package:lwg_gui/providers/app_provider.dart';

class CommandPalette extends ConsumerStatefulWidget {
  const CommandPalette({super.key});

  @override
  ConsumerState<CommandPalette> createState() => _CommandPaletteState();
}

class _CommandPaletteState extends ConsumerState<CommandPalette> {
  final _searchController = TextEditingController();
  final _focusNode = FocusNode();

  @override
  void initState() {
    super.initState();
    _focusNode.requestFocus();
  }

  @override
  void dispose() {
    _searchController.dispose();
    _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(appProvider);
    final notifier = ref.read(appProvider.notifier);
    final query = _searchController.text.toLowerCase();

    final commands = _buildCommands(state, notifier, query);

    return Material(
      color: Colors.transparent,
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxHeight: 500),
          child: Container(
            width: 600,
            decoration: BoxDecoration(
              color: AppTheme.surface,
              borderRadius: BorderRadius.circular(16),
              boxShadow: [
                BoxShadow(color: Colors.black.withValues(alpha: 0.5), blurRadius: 30),
              ],
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildSearchBar(),
                const Divider(color: AppTheme.border, height: 1),
                Flexible(child: _buildCommandList(commands)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildSearchBar() {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          Icon(Icons.search, color: AppTheme.textSecondary, size: 20),
          const SizedBox(width: 12),
          Expanded(
            child: TextField(
              controller: _searchController,
              focusNode: _focusNode,
              style: const TextStyle(color: Colors.white, fontSize: 16),
              decoration: InputDecoration(
                hintText: '输入命令或搜索壁纸...',
                hintStyle: const TextStyle(color: AppTheme.textSecondary),
                border: InputBorder.none,
              ),
              onChanged: (_) => setState(() {}),
            ),
          ),
          Text('ESC', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
        ],
      ),
    );
  }

  Widget _buildCommandList(List<CommandItem> commands) {
    if (commands.isEmpty) {
      return Padding(
        padding: const EdgeInsets.all(32),
        child: Text('未找到匹配项', style: const TextStyle(color: AppTheme.textSecondary)),
      );
    }

    return ListView.builder(
      shrinkWrap: true,
      itemCount: commands.length,
      itemBuilder: (context, index) {
        final cmd = commands[index];
        return ListTile(
          leading: Icon(cmd.icon, color: cmd.color, size: 20),
          title: Text(cmd.label, style: const TextStyle(color: Colors.white)),
          subtitle: cmd.description != null
              ? Text(cmd.description!, style: const TextStyle(color: AppTheme.textSecondary, fontSize: 12))
              : null,
          trailing: cmd.shortcut != null
              ? Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(cmd.shortcut!, style: const TextStyle(color: AppTheme.textSecondary, fontSize: 11)),
                )
              : null,
          onTap: () {
            cmd.action();
            Navigator.of(context).pop();
          },
        );
      },
    );
  }

  List<CommandItem> _buildCommands(AppState state, AppNotifier notifier, String query) {
    final allCommands = <CommandItem>[
      CommandItem(icon: Icons.dashboard_outlined, label: '打开库', color: AppTheme.primary, action: () => notifier.setActiveTab(AppTab.wallpapers)),
      CommandItem(icon: Icons.settings_outlined, label: '打开设置', color: AppTheme.primary, action: () => notifier.setActiveTab(AppTab.settings)),
      CommandItem(icon: Icons.speed_outlined, label: '打开性能', color: AppTheme.primary, action: () => notifier.setActiveTab(AppTab.performance)),
      CommandItem(icon: Icons.shuffle, label: '随机壁纸', description: '应用随机壁纸', color: AppTheme.secondary, shortcut: 'Ctrl+R', action: () => notifier.applyRandomWallpaper()),
      CommandItem(icon: Icons.stop, label: '停止所有', description: '停止正在播放的壁纸', color: AppTheme.error, shortcut: 'Ctrl+S', action: () => notifier.stopWallpaper()),
      CommandItem(icon: Icons.refresh, label: '重新扫描', description: '重新扫描壁纸库', color: AppTheme.success, action: () => notifier.loadWallpapers()),
      CommandItem(icon: Icons.view_compact_alt_outlined, label: '切换紧凑模式', color: AppTheme.warning, action: () => notifier.toggleCompactMode(!state.isCompactMode)),
    ];

    final wallpaperCommands = state.wallpapers
        .where((w) {
          if (query.isEmpty) return false;
          return w.title.toLowerCase().contains(query) || w.id.contains(query);
        })
        .take(8)
        .map((w) => CommandItem(
              icon: Icons.wallpaper,
              label: w.title,
              description: '${w.type.name} · ${w.size}',
              color: AppTheme.primary,
              action: () => notifier.applyWallpaper(w.id, null),
            ))
        .toList();

    if (query.isEmpty) {
      return allCommands;
    }

    final filteredCommands = allCommands
        .where((c) => c.label.toLowerCase().contains(query) || (c.description?.toLowerCase().contains(query) ?? false))
        .toList();

    return [...filteredCommands, ...wallpaperCommands];
  }
}

class CommandItem {
  final IconData icon;
  final String label;
  final String? description;
  final Color color;
  final String? shortcut;
  final VoidCallback action;

  const CommandItem({
    required this.icon,
    required this.label,
    this.description,
    required this.color,
    this.shortcut,
    required this.action,
  });
}

void showCommandPalette(BuildContext context) {
  showDialog(
    context: context,
    barrierColor: Colors.black.withValues(alpha: 0.5),
    builder: (context) => const CommandPalette(),
  );
}