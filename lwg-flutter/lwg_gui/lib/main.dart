import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/theme/app_theme.dart';
import 'package:lwg_gui/providers/app_provider.dart';
import 'package:lwg_gui/components/sidebar.dart';
import 'package:lwg_gui/components/command_palette.dart';
import 'package:lwg_gui/components/welcome_dialog.dart';
import 'package:lwg_gui/pages/library_page.dart';
import 'package:lwg_gui/pages/settings_page.dart';
import 'package:lwg_gui/pages/performance_page.dart';
import 'package:lwg_gui/pages/compact_page.dart';

void main() {
  runApp(const ProviderScope(child: WallpaperApp()));
}

class WallpaperApp extends ConsumerStatefulWidget {
  const WallpaperApp({super.key});

  @override
  ConsumerState<WallpaperApp> createState() => _WallpaperAppState();
}

class _WallpaperAppState extends ConsumerState<WallpaperApp> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(appProvider.notifier).initApp();
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Wallpaper Manager',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.themeData,
      home: const MainScreen(),
    );
  }
}

class MainScreen extends ConsumerStatefulWidget {
  const MainScreen({super.key});

  @override
  ConsumerState<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends ConsumerState<MainScreen> {
  final _keyboardFocusNode = FocusNode();

  @override
  void dispose() {
    _keyboardFocusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(appProvider);
    final notifier = ref.read(appProvider.notifier);

    // Show welcome dialog if onboarding not completed
    if (state.isHydrated && state.settings != null && !state.settings!.onboardingCompleted) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        showWelcomeDialog(context);
      });
    }

    return KeyboardListener(
      focusNode: _keyboardFocusNode,
      onKeyEvent: (event) {
        if (event is KeyDownEvent && event.logicalKey == LogicalKeyboardKey.keyK) {
          final isCtrl = HardwareKeyboard.instance.isLogicalKeyPressed(LogicalKeyboardKey.controlLeft) ||
              HardwareKeyboard.instance.isLogicalKeyPressed(LogicalKeyboardKey.controlRight);
          if (isCtrl) {
            showCommandPalette(context);
          }
        }
      },
      child: Scaffold(
        body: state.isCompactMode
            ? const CompactPage()
            : Row(
                crossAxisAlignment: CrossAxisAlignment.stretch,
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
      ),
    );
  }
}