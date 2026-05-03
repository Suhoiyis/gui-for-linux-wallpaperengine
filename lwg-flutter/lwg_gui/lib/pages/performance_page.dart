import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/theme/app_theme.dart';
import 'package:lwg_gui/providers/app_provider.dart';

class SystemStats {
  final double cpuUsage;
  final double memoryUsage;
  final int threads;
  final double processCpu;
  final double processMemory;
  final String processName;

  const SystemStats({
    this.cpuUsage = 0,
    this.memoryUsage = 0,
    this.threads = 0,
    this.processCpu = 0,
    this.processMemory = 0,
    this.processName = '',
  });
}

final systemStatsProvider = StreamProvider<SystemStats>((ref) {
  return Stream.periodic(
    const Duration(seconds: 2),
    (count) => SystemStats(
      cpuUsage: 15 + (count % 30) * 0.8,
      memoryUsage: 45 + (count % 20) * 0.5,
      threads: 8 + count % 4,
      processCpu: 3 + count % 10 * 0.3,
      processMemory: 250 + count % 100,
      processName: 'linux-wallpaperengine',
    ),
  );
});

class PerformancePage extends ConsumerWidget {
  const PerformancePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final statsAsync = ref.watch(systemStatsProvider);
    final appState = ref.watch(appProvider);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('系统监控', style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          Row(
            children: [
              _buildOverviewCard('CPU', '${statsAsync.value?.cpuUsage.toStringAsFixed(1) ?? '--'}%', Icons.processor, AppTheme.primary),
              const SizedBox(width: 16),
              _buildOverviewCard('内存', '${statsAsync.value?.memoryUsage.toStringAsFixed(1) ?? '--'}%', Icons.memory, AppTheme.secondary),
              const SizedBox(width: 16),
              _buildOverviewCard('线程', '${statsAsync.value?.threads ?? '--'}', Icons.account_tree_outlined, AppTheme.success),
            ],
          ),
          const SizedBox(height: 32),
          const Text('壁纸引擎进程', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          _buildProcessTable(statsAsync.value, appState),
          const SizedBox(height: 32),
          if (appState.runtimeState.values.any((w) => w.isPlaying))
            ElevatedButton.icon(
              onPressed: () => ref.read(appProvider.notifier).stopWallpaper(),
              icon: const Icon(Icons.stop, size: 16),
              label: const Text('停止壁纸'),
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

  Widget _buildOverviewCard(String title, String value, IconData icon, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: AppTheme.surface,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: color.withValues(alpha: 0.3)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 12),
            Text(title, style: const TextStyle(color: AppTheme.textSecondary, fontSize: 14)),
            const SizedBox(height: 4),
            Text(value, style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }

  Widget _buildProcessTable(SystemStats? stats, AppState appState) {
    final isPlaying = appState.runtimeState.values.any((w) => w.isPlaying);
    if (!isPlaying) {
      return Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(color: AppTheme.surface, borderRadius: BorderRadius.circular(16)),
        child: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.info_outline, color: AppTheme.textSecondary, size: 32),
              const SizedBox(height: 8),
              const Text('壁纸引擎未运行', style: TextStyle(color: AppTheme.textSecondary)),
            ],
          ),
        ),
      );
    }
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: AppTheme.surface, borderRadius: BorderRadius.circular(16)),
      child: Column(
        children: [
          _buildTableHeader(),
          const SizedBox(height: 12),
          _buildTableRow(
            stats?.processName ?? 'linux-wallpaperengine',
            '${stats?.processCpu.toStringAsFixed(1) ?? '--'}%',
            '${stats?.processMemory.toStringAsFixed(0) ?? '--'}MB',
          ),
        ],
      ),
    );
  }

  Widget _buildTableHeader() {
    return Row(
      children: [
        const Expanded(child: Text('进程名', style: TextStyle(color: AppTheme.textSecondary, fontWeight: FontWeight.w600))),
        SizedBox(width: 120, child: Text('CPU', style: TextStyle(color: AppTheme.textSecondary, fontWeight: FontWeight.w600), textAlign: TextAlign.right)),
        SizedBox(width: 120, child: Text('内存', style: TextStyle(color: AppTheme.textSecondary, fontWeight: FontWeight.w600), textAlign: TextAlign.right)),
      ],
    );
  }

  Widget _buildTableRow(String name, String cpu, String mem) {
    return Row(
      children: [
        Expanded(child: Text(name, style: const TextStyle(color: Colors.white))),
        SizedBox(width: 120, child: Text(cpu, style: const TextStyle(color: Colors.white70), textAlign: TextAlign.right)),
        SizedBox(width: 120, child: Text(mem, style: const TextStyle(color: Colors.white70), textAlign: TextAlign.right)),
      ],
    );
  }
}