class AppConfig {
  final int fps;
  final String scaling;
  final String clamping;
  final bool noFullscreenPause;
  final bool disableMouse;
  final bool disableParallax;
  final bool disableParticles;
  final double volume;
  final bool muteAudio;
  final bool noAutomute;
  final bool noAudioProcessing;
  final bool cycleEnabled;
  final int cycleInterval;
  final String cycleOrder;
  final bool waylandOnlyActive;
  final String waylandIgnoreAppids;
  final String? assetsPath;
  final String? workshopPath;
  final bool startHidden;
  final int screenshotDelay;
  final String screenshotRes;
  final bool preferXvfb;
  final Map<String, dynamic> wallpaperProperties;
  final Map<String, String> wallpaperNicknames;
  final bool compactMode;
  final bool autoRestore;
  final bool onboardingCompleted;

  const AppConfig({
    this.fps = 30,
    this.scaling = 'default',
    this.clamping = 'stretch',
    this.noFullscreenPause = false,
    this.disableMouse = false,
    this.disableParallax = false,
    this.disableParticles = false,
    this.volume = 0.5,
    this.muteAudio = false,
    this.noAutomute = false,
    this.noAudioProcessing = false,
    this.cycleEnabled = false,
    this.cycleInterval = 30,
    this.cycleOrder = 'random',
    this.waylandOnlyActive = false,
    this.waylandIgnoreAppids = '',
    this.assetsPath,
    this.workshopPath,
    this.startHidden = false,
    this.screenshotDelay = 5,
    this.screenshotRes = '1920x1080',
    this.preferXvfb = false,
    this.wallpaperProperties = const {},
    this.wallpaperNicknames = const {},
    this.compactMode = false,
    this.autoRestore = false,
    this.onboardingCompleted = false,
  });

  AppConfig copyWith({
    int? fps,
    String? scaling,
    String? clamping,
    bool? noFullscreenPause,
    bool? disableMouse,
    bool? disableParallax,
    bool? disableParticles,
    double? volume,
    bool? muteAudio,
    bool? noAutomute,
    bool? noAudioProcessing,
    bool? cycleEnabled,
    int? cycleInterval,
    String? cycleOrder,
    bool? waylandOnlyActive,
    String? waylandIgnoreAppids,
    String? assetsPath,
    String? workshopPath,
    bool? startHidden,
    int? screenshotDelay,
    String? screenshotRes,
    bool? preferXvfb,
    Map<String, dynamic>? wallpaperProperties,
    Map<String, String>? wallpaperNicknames,
    bool? compactMode,
    bool? autoRestore,
    bool? onboardingCompleted,
  }) {
    return AppConfig(
      fps: fps ?? this.fps,
      scaling: scaling ?? this.scaling,
      clamping: clamping ?? this.clamping,
      noFullscreenPause: noFullscreenPause ?? this.noFullscreenPause,
      disableMouse: disableMouse ?? this.disableMouse,
      disableParallax: disableParallax ?? this.disableParallax,
      disableParticles: disableParticles ?? this.disableParticles,
      volume: volume ?? this.volume,
      muteAudio: muteAudio ?? this.muteAudio,
      noAutomute: noAutomute ?? this.noAutomute,
      noAudioProcessing: noAudioProcessing ?? this.noAudioProcessing,
      cycleEnabled: cycleEnabled ?? this.cycleEnabled,
      cycleInterval: cycleInterval ?? this.cycleInterval,
      cycleOrder: cycleOrder ?? this.cycleOrder,
      waylandOnlyActive: waylandOnlyActive ?? this.waylandOnlyActive,
      waylandIgnoreAppids:
          waylandIgnoreAppids ?? this.waylandIgnoreAppids,
      assetsPath: assetsPath ?? this.assetsPath,
      workshopPath: workshopPath ?? this.workshopPath,
      startHidden: startHidden ?? this.startHidden,
      screenshotDelay: screenshotDelay ?? this.screenshotDelay,
      screenshotRes: screenshotRes ?? this.screenshotRes,
      preferXvfb: preferXvfb ?? this.preferXvfb,
      wallpaperProperties:
          wallpaperProperties ?? this.wallpaperProperties,
      wallpaperNicknames:
          wallpaperNicknames ?? this.wallpaperNicknames,
      compactMode: compactMode ?? this.compactMode,
      autoRestore: autoRestore ?? this.autoRestore,
      onboardingCompleted:
          onboardingCompleted ?? this.onboardingCompleted,
    );
  }
}