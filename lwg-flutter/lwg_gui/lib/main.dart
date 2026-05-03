import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/theme/app_theme.dart';
import 'package:lwg_gui/providers/app_provider.dart';
import 'package:lwg_gui/components/sidebar.dart';
import 'package:lwg_gui/pages/library_page.dart';
import 'package:lwg_gui/pages/settings_page.dart';
import 'package:lwg_gui/pages/performance_page.dart';

void main() {
  runApp(const ProviderScope(child: WallpaperApp()));
}

class WallpaperApp extends ConsumerWidget {
  const WallpaperApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final notifier = ref.read(appProvider.notifier);
    notifier.initApp();

    return MaterialApp(
      title: 'Wallpaper Manager',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.themeData,
      home: const MainScreen(),
    );
  }
}

class MainScreen extends ConsumerWidget {
  const MainScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(appProvider);

    return Scaffold(
      body: Row(
        children: [
          const Sidebar(),
          Expanded(
            child: AnimatedSwitcher(
              duration: const Duration(milliseconds: 250),
              switchInCurve: Curves.easeOut,
              switchOutCurve: Curves.easeIn,
              child: switch (state.activeTab) {
                AppTab.wallpapers => const LibraryPage(key: ValueKey('library')),
                AppTab.settings => const SettingsPage(key: ValueKey('settings')),
                AppTab.performance => const PerformancePage(key: ValueKey('performance')),
              },
            ),
          ),
        ],
      ),
    );
  }
}