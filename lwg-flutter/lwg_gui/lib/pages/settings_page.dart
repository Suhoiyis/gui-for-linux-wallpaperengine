import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/theme/app_theme.dart';
import 'package:lwg_gui/providers/app_provider.dart';
import 'package:lwg_gui/models/app_config.dart';

class SettingsPage extends ConsumerWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(appProvider);
    final notifier = ref.read(appProvider.notifier);
    final settings = state.settings ?? const AppConfig();

    return Row(
      children: [
        _buildSettingsSidebar(state),
        Expanded(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(32),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildSectionTitle('播放与性能'),
                _buildPlaybackSettings(settings, notifier),
                const SizedBox(height: 32),
                _buildSectionTitle('音频与显示'),
                _buildDisplaySettings(settings, notifier),
                const SizedBox(height: 32),
                _buildSectionTitle('系统与工具'),
                _buildSystemSettings(settings, notifier),
                const SizedBox(height: 32),
                Row(
                  children: [
                    ElevatedButton(
                      onPressed: () => notifier.saveSettings(),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppTheme.primary,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      child: const Text('保存设置'),
                    ),
                    const SizedBox(width: 12),
                    OutlinedButton(
                      onPressed: () => notifier.fetchSettings(),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: AppTheme.textSecondary,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      child: const Text('重新加载'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSettingsSidebar(AppState state) {
    final isPlaying = state.runtimeState.values.any((w) => w.isPlaying);
    return Container(
      width: 240,
      decoration: BoxDecoration(
        color: AppTheme.surface,
        border: Border(right: BorderSide(color: AppTheme.border)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: 24),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: isPlaying ? AppTheme.success.withValues(alpha: 0.1) : Colors.grey.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  Icon(isPlaying ? Icons.play_circle : Icons.stop_circle, color: isPlaying ? AppTheme.success : Colors.grey, size: 20),
                  const SizedBox(width: 8),
                  Text(isPlaying ? '正在播放' : '已停止', style: TextStyle(color: isPlaying ? AppTheme.success : Colors.grey, fontSize: 13)),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          _buildSidebarItem(Icons.speed_outlined, 'FPS: ${state.settings?.fps ?? 30}'),
          _buildSidebarItem(Icons.volume_up_outlined, '音量: ${(state.settings?.volume ?? 0.5 * 100).round()}%'),
        ],
      ),
    );
  }

  Widget _buildSidebarItem(IconData icon, String text) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      child: Row(
        children: [
          Icon(icon, color: AppTheme.textSecondary, size: 18),
          const SizedBox(width: 8),
          Text(text, style: const TextStyle(color: AppTheme.textSecondary, fontSize: 13)),
        ],
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Text(title, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w600));
  }

  Widget _buildPlaybackSettings(AppConfig settings, AppNotifier notifier) {
    return Column(
      children: [
        _buildSliderSetting('FPS', settings.fps, 1, 144, (v) => notifier.updateSettings(settings.copyWith(fps: v.round()))),
        _buildDropdownSetting('缩放模式', settings.scaling, ['default', 'fit', 'fill', 'stretch'], (v) => notifier.updateSettings(settings.copyWith(scaling: v))),
        _buildDropdownSetting('裁剪模式', settings.clamping, ['stretch', 'clamp', 'crop'], (v) => notifier.updateSettings(settings.copyWith(clamping: v))),
        _buildSwitchSetting('暂停全屏应用时停止播放', settings.noFullscreenPause, (v) => notifier.updateSettings(settings.copyWith(noFullscreenPause: v))),
        _buildSwitchSetting('禁用鼠标交互', settings.disableMouse, (v) => notifier.updateSettings(settings.copyWith(disableMouse: v))),
        _buildSwitchSetting('禁用视差效果', settings.disableParallax, (v) => notifier.updateSettings(settings.copyWith(disableParallax: v))),
        _buildSwitchSetting('禁用粒子效果', settings.disableParticles, (v) => notifier.updateSettings(settings.copyWith(disableParticles: v))),
      ],
    );
  }

  Widget _buildDisplaySettings(AppConfig settings, AppNotifier notifier) {
    return Column(
      children: [
        _buildSliderSetting('音量', settings.volume, 0, 1, (v) => notifier.updateSettings(settings.copyWith(volume: v))),
        _buildSwitchSetting('静音', settings.muteAudio, (v) => notifier.updateSettings(settings.copyWith(muteAudio: v))),
        _buildSwitchSetting('禁用自动静音', settings.noAutomute, (v) => notifier.updateSettings(settings.copyWith(noAutomute: v))),
        _buildSwitchSetting('禁用音频处理', settings.noAudioProcessing, (v) => notifier.updateSettings(settings.copyWith(noAudioProcessing: v))),
        _buildSwitchSetting('壁纸轮播', settings.cycleEnabled, (v) => notifier.updateSettings(settings.copyWith(cycleEnabled: v))),
        if (settings.cycleEnabled)
          _buildSliderSetting('轮播间隔(秒)', settings.cycleInterval, 5, 3600, (v) => notifier.updateSettings(settings.copyWith(cycleInterval: v.round()))),
        _buildDropdownSetting('轮播顺序', settings.cycleOrder, ['random', 'sequential'], (v) => notifier.updateSettings(settings.copyWith(cycleOrder: v))),
      ],
    );
  }

  Widget _buildSystemSettings(AppConfig settings, AppNotifier notifier) {
    return Column(
      children: [
        _buildSwitchSetting('Wayland仅激活窗口渲染', settings.waylandOnlyActive, (v) => notifier.updateSettings(settings.copyWith(waylandOnlyActive: v))),
        _buildSwitchSetting('启动时隐藏窗口', settings.startHidden, (v) => notifier.updateSettings(settings.copyWith(startHidden: v))),
        _buildSwitchSetting('自动恢复壁纸', settings.autoRestore, (v) => notifier.updateSettings(settings.copyWith(autoRestore: v))),
        _buildSwitchSetting('紧凑模式', settings.compactMode, (v) => notifier.updateSettings(settings.copyWith(compactMode: v))),
        _buildSwitchSetting('使用Xvfb截图', settings.preferXvfb, (v) => notifier.updateSettings(settings.copyWith(preferXvfb: v))),
        _buildSliderSetting('截图延迟(秒)', settings.screenshotDelay, 1, 30, (v) => notifier.updateSettings(settings.copyWith(screenshotDelay: v.round()))),
      ],
    );
  }

  Widget _buildSliderSetting(String label, double value, double min, double max, ValueChanged<double> onChanged) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Expanded(child: Text(label, style: const TextStyle(color: Colors.white70))),
          SizedBox(width: 200, child: Slider(value: value, min: min, max: max, onChanged: onChanged)),
          SizedBox(
            width: 60,
            child: Text(max <= 1 ? '${(value * 100).round()}%' : value.round().toString(), style: const TextStyle(color: AppTheme.textSecondary), textAlign: TextAlign.right),
          ),
        ],
      ),
    );
  }

  Widget _buildSwitchSetting(String label, bool value, ValueChanged<bool> onChanged) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Expanded(child: Text(label, style: const TextStyle(color: Colors.white70))),
          Switch(value: value, onChanged: onChanged),
        ],
      ),
    );
  }

  Widget _buildDropdownSetting(String label, String value, List<String> options, ValueChanged<String> onChanged) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Expanded(child: Text(label, style: const TextStyle(color: Colors.white70))),
          SizedBox(
            width: 200,
            child: DropdownButton<String>(
              value: value,
              isDense: true,
              dropdownColor: AppTheme.surface,
              style: const TextStyle(color: Colors.white),
              underline: Container(height: 1, color: AppTheme.border),
              items: options.map((o) => DropdownMenuItem(value: o, child: Text(o))).toList(),
              onChanged: (v) => onChanged(v!),
            ),
          ),
        ],
      ),
    );
  }
}