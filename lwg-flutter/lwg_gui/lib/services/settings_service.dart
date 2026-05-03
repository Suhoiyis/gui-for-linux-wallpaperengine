import 'dart:convert';
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

    // If C++ returned rawJson (config file exists), parse it
    if (map.containsKey('rawJson')) {
      final jsonString = map['rawJson'] as String;
      try {
        final json = jsonDecode(jsonString) as Map<String, dynamic>;
        return AppConfig(
          fps: json['fps'] as int? ?? 30,
          scaling: json['scaling'] as String? ?? 'default',
          clamping: json['clamping'] as String? ?? 'stretch',
          noFullscreenPause: json['noFullscreenPause'] as bool? ?? false,
          disableMouse: json['disableMouse'] as bool? ?? false,
          disableParallax: json['disableParallax'] as bool? ?? false,
          disableParticles: json['disableParticles'] as bool? ?? false,
          volume: (json['volume'] as num?)?.toDouble() ?? 0.5,
          muteAudio: json['muteAudio'] as bool? ?? false,
          noAutomute: json['noAutomute'] as bool? ?? false,
          noAudioProcessing: json['noAudioProcessing'] as bool? ?? false,
          cycleEnabled: json['cycleEnabled'] as bool? ?? false,
          cycleInterval: json['cycleInterval'] as int? ?? 30,
          cycleOrder: json['cycleOrder'] as String? ?? 'random',
          waylandOnlyActive: json['waylandOnlyActive'] as bool? ?? false,
          waylandIgnoreAppids: json['waylandIgnoreAppids'] as String? ?? '',
          assetsPath: json['assetsPath'] as String?,
          workshopPath: json['workshopPath'] as String?,
          startHidden: json['startHidden'] as bool? ?? false,
          screenshotDelay: json['screenshotDelay'] as int? ?? 5,
          screenshotRes: json['screenshotRes'] as String? ?? '1920x1080',
          preferXvfb: json['preferXvfb'] as bool? ?? false,
          wallpaperProperties: json['wallpaperProperties'] as Map<String, dynamic>? ?? {},
          wallpaperNicknames: (json['wallpaperNicknames'] as Map?)?.cast<String, String>() ?? {},
          compactMode: json['compactMode'] as bool? ?? false,
          autoRestore: json['autoRestore'] as bool? ?? false,
          onboardingCompleted: json['onboardingCompleted'] as bool? ?? false,
        );
      } catch (_) {
        return const AppConfig();
      }
    }

    // Otherwise, individual fields (default values from C++)
    return AppConfig(
      fps: map['fps'] as int? ?? 30,
      scaling: map['scaling'] as String? ?? 'default',
      clamping: map['clamping'] as String? ?? 'stretch',
      volume: (map['volume'] as num?)?.toDouble() ?? 0.5,
      muteAudio: map['muteAudio'] as bool? ?? false,
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