import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/models/app_config.dart';
import 'package:lwg_gui/services/platform_service.dart';

class SettingsService {
  final PlatformService _platform;

  SettingsService(this._platform);

  Future<AppConfig?> fetchSettings() async {
    final raw = await _platform.invoke('get_settings');
    if (raw == null) return const AppConfig();
    final map = raw as Map;
    return AppConfig(
      fps: map['fps'] as int? ?? 30,
      scaling: map['scaling'] as String? ?? 'default',
      clamping: map['clamping'] as String? ?? 'stretch',
      noFullscreenPause: map['noFullscreenPause'] as bool? ?? false,
      disableMouse: map['disableMouse'] as bool? ?? false,
      disableParallax: map['disableParallax'] as bool? ?? false,
      disableParticles: map['disableParticles'] as bool? ?? false,
      volume: (map['volume'] as num?)?.toDouble() ?? 0.5,
      muteAudio: map['muteAudio'] as bool? ?? false,
      noAutomute: map['noAutomute'] as bool? ?? false,
      noAudioProcessing: map['noAudioProcessing'] as bool? ?? false,
      cycleEnabled: map['cycleEnabled'] as bool? ?? false,
      cycleInterval: map['cycleInterval'] as int? ?? 30,
      cycleOrder: map['cycleOrder'] as String? ?? 'random',
      waylandOnlyActive: map['waylandOnlyActive'] as bool? ?? false,
      waylandIgnoreAppids:
          map['waylandIgnoreAppids'] as String? ?? '',
      assetsPath: map['assetsPath'] as String?,
      workshopPath: map['workshopPath'] as String?,
      startHidden: map['startHidden'] as bool? ?? false,
      screenshotDelay: map['screenshotDelay'] as int? ?? 5,
      screenshotRes: map['screenshotRes'] as String? ?? '1920x1080',
      preferXvfb: map['preferXvfb'] as bool? ?? false,
      wallpaperProperties:
          map['wallpaperProperties'] as Map<String, dynamic>? ?? {},
      wallpaperNicknames:
          (map['wallpaperNicknames'] as Map?)?.cast<String, String>() ?? {},
      compactMode: map['compactMode'] as bool? ?? false,
      autoRestore: map['autoRestore'] as bool? ?? false,
      onboardingCompleted:
          map['onboardingCompleted'] as bool? ?? false,
    );
  }

  Future<void> saveSettings(AppConfig config) async {
    await _platform.invoke('save_settings', {
      'fps': config.fps,
      'scaling': config.scaling,
      'clamping': config.clamping,
      'noFullscreenPause': config.noFullscreenPause,
      'disableMouse': config.disableMouse,
      'disableParallax': config.disableParallax,
      'disableParticles': config.disableParticles,
      'volume': config.volume,
      'muteAudio': config.muteAudio,
      'noAutomute': config.noAutomute,
      'noAudioProcessing': config.noAudioProcessing,
      'cycleEnabled': config.cycleEnabled,
      'cycleInterval': config.cycleInterval,
      'cycleOrder': config.cycleOrder,
      'waylandOnlyActive': config.waylandOnlyActive,
      'waylandIgnoreAppids': config.waylandIgnoreAppids,
      'assetsPath': config.assetsPath,
      'workshopPath': config.workshopPath,
      'startHidden': config.startHidden,
      'screenshotDelay': config.screenshotDelay,
      'screenshotRes': config.screenshotRes,
      'preferXvfb': config.preferXvfb,
      'compactMode': config.compactMode,
      'autoRestore': config.autoRestore,
      'onboardingCompleted': config.onboardingCompleted,
    });
  }
}

final settingsServiceProvider = Provider<SettingsService>((ref) {
  return SettingsService(ref.read(platformServiceProvider));
});