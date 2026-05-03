import 'dart:async';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/models/wallpaper.dart';
import 'package:lwg_gui/models/app_config.dart';
import 'package:lwg_gui/models/playlist.dart';
import 'package:lwg_gui/models/active_wallpaper.dart';
import 'package:lwg_gui/models/log_entry.dart';
import 'package:lwg_gui/services/wallpaper_service.dart';
import 'package:lwg_gui/services/settings_service.dart';

enum AppTab { wallpapers, settings, performance }
enum SortBy { name, id, size }

class AppState {
  final String appVersion;
  final List<Wallpaper> wallpapers;
  final String? selectedId;
  final String searchQuery;
  final AppTab activeTab;
  final SortBy sortBy;
  final Set<String> favoriteIds;
  final Map<String, String> nicknames;
  final AppConfig? settings;
  final bool settingsLoading;
  final List<String> monitors;
  final bool monitorsLoading;
  final String selectedScreen;
  final Map<String, ActiveWallpaper> runtimeState;
  final List<Playlist> playlists;
  final String? activePlaylistId;
  final String? cyclePlaylistId;
  final bool isPlaylistSidebarOpen;
  final bool isPlaylistSidebarPinned;
  final bool isHydrated;
  final bool isSelectionMode;
  final Set<String> selectedForPlaylist;
  final bool isCommandPaletteOpen;
  final bool welcomeDialogOpen;
  final bool welcomeDialogRequired;
  final bool isCompactMode;
  final List<LogEntry> logs;

  const AppState({
    this.appVersion = '0.0.0',
    this.wallpapers = const [],
    this.selectedId,
    this.searchQuery = '',
    this.activeTab = AppTab.wallpapers,
    this.sortBy = SortBy.name,
    this.favoriteIds = const {},
    this.nicknames = const {},
    this.settings,
    this.settingsLoading = false,
    this.monitors = const [],
    this.monitorsLoading = false,
    this.selectedScreen = 'all',
    this.runtimeState = const {},
    this.playlists = const [],
    this.activePlaylistId,
    this.cyclePlaylistId,
    this.isPlaylistSidebarOpen = true,
    this.isPlaylistSidebarPinned = true,
    this.isHydrated = false,
    this.isSelectionMode = false,
    this.selectedForPlaylist = const {},
    this.isCommandPaletteOpen = false,
    this.welcomeDialogOpen = false,
    this.welcomeDialogRequired = false,
    this.isCompactMode = false,
    this.logs = const [],
  });

  List<Wallpaper> get filteredWallpapers {
    var filtered = wallpapers;

    if (searchQuery.isNotEmpty) {
      final q = searchQuery.toLowerCase();
      filtered = filtered
          .where(
            (w) =>
                w.title.toLowerCase().contains(q) ||
                w.id.contains(q) ||
                w.tags.any((t) => t.toLowerCase().contains(q)),
          )
          .toList();
    }

    if (activePlaylistId != null) {
      final playlist = playlists.firstWhere(
        (p) => p.id == activePlaylistId,
        orElse: () => Playlist(
          id: '',
          name: '',
          createdAt: 0,
          updatedAt: 0,
        ),
      );
      if (playlist.id.isNotEmpty) {
        filtered = filtered
            .where((w) => playlist.wallpaperIds.contains(w.id))
            .toList();
      }
    }

    filtered.sort((a, b) {
      return switch (sortBy) {
        SortBy.name => a.title.compareTo(b.title),
        SortBy.id => a.id.compareTo(b.id),
        SortBy.size => a.size.compareTo(b.size),
      };
    });

    return filtered;
  }

  Wallpaper? get selectedWallpaper {
    if (selectedId == null) return null;
    try {
      return wallpapers.firstWhere((w) => w.id == selectedId);
    } catch (_) {
      return null;
    }
  }

  bool isFavorite(String id) => favoriteIds.contains(id);

  AppState copyWith({
    String? appVersion,
    List<Wallpaper>? wallpapers,
    String? selectedId,
    bool clearSelectedId = false,
    String? searchQuery,
    AppTab? activeTab,
    SortBy? sortBy,
    Set<String>? favoriteIds,
    Map<String, String>? nicknames,
    AppConfig? settings,
    bool clearSettings = false,
    bool? settingsLoading,
    List<String>? monitors,
    bool? monitorsLoading,
    String? selectedScreen,
    Map<String, ActiveWallpaper>? runtimeState,
    List<Playlist>? playlists,
    String? activePlaylistId,
    bool clearActivePlaylistId = false,
    String? cyclePlaylistId,
    bool clearCyclePlaylistId = false,
    bool? isPlaylistSidebarOpen,
    bool? isPlaylistSidebarPinned,
    bool? isHydrated,
    bool? isSelectionMode,
    Set<String>? selectedForPlaylist,
    bool? isCommandPaletteOpen,
    bool? welcomeDialogOpen,
    bool? welcomeDialogRequired,
    bool? isCompactMode,
    List<LogEntry>? logs,
  }) {
    return AppState(
      appVersion: appVersion ?? this.appVersion,
      wallpapers: wallpapers ?? this.wallpapers,
      selectedId: clearSelectedId ? null : (selectedId ?? this.selectedId),
      searchQuery: searchQuery ?? this.searchQuery,
      activeTab: activeTab ?? this.activeTab,
      sortBy: sortBy ?? this.sortBy,
      favoriteIds: favoriteIds ?? this.favoriteIds,
      nicknames: nicknames ?? this.nicknames,
      settings: clearSettings ? null : (settings ?? this.settings),
      settingsLoading: settingsLoading ?? this.settingsLoading,
      monitors: monitors ?? this.monitors,
      monitorsLoading: monitorsLoading ?? this.monitorsLoading,
      selectedScreen: selectedScreen ?? this.selectedScreen,
      runtimeState: runtimeState ?? this.runtimeState,
      playlists: playlists ?? this.playlists,
      activePlaylistId: clearActivePlaylistId
          ? null
          : (activePlaylistId ?? this.activePlaylistId),
      cyclePlaylistId: clearCyclePlaylistId
          ? null
          : (cyclePlaylistId ?? this.cyclePlaylistId),
      isPlaylistSidebarOpen:
          isPlaylistSidebarOpen ?? this.isPlaylistSidebarOpen,
      isPlaylistSidebarPinned:
          isPlaylistSidebarPinned ?? this.isPlaylistSidebarPinned,
      isHydrated: isHydrated ?? this.isHydrated,
      isSelectionMode: isSelectionMode ?? this.isSelectionMode,
      selectedForPlaylist: selectedForPlaylist ?? this.selectedForPlaylist,
      isCommandPaletteOpen:
          isCommandPaletteOpen ?? this.isCommandPaletteOpen,
      welcomeDialogOpen: welcomeDialogOpen ?? this.welcomeDialogOpen,
      welcomeDialogRequired:
          welcomeDialogRequired ?? this.welcomeDialogRequired,
      isCompactMode: isCompactMode ?? this.isCompactMode,
      logs: logs ?? this.logs,
    );
  }
}

class AppNotifier extends Notifier<AppState> {
  @override
  AppState build() => const AppState();

  Future<void> initApp() async {
    await Future.wait([
      loadWallpapers(),
      fetchSettings(),
      loadPlaylists(),
      fetchMonitors(),
    ]);
    initializeSelectedWallpaper();
    state = state.copyWith(isHydrated: true);
  }

  Future<void> loadWallpapers() async {
    final service = ref.read(wallpaperServiceProvider);
    final wallpapers = await service.scanWallpapers();
    state = state.copyWith(wallpapers: wallpapers);
  }

  void setSelectedId(String? id) {
    state = state.copyWith(selectedId: id, clearSelectedId: id == null);
  }

  void initializeSelectedWallpaper() {
    if (state.wallpapers.isEmpty) return;
    final runtime = state.runtimeState;
    if (runtime.isNotEmpty) {
      final firstActive = runtime.values.first;
      if (state.wallpapers.any((w) => w.id == firstActive.wallpaperId)) {
        state = state.copyWith(selectedId: firstActive.wallpaperId);
        return;
      }
    }
    state = state.copyWith(selectedId: state.wallpapers.first.id);
  }

  Future<void> applyWallpaper(String id, String? screen) async {
    final service = ref.read(wallpaperServiceProvider);
    await service.applyWallpaper(id, screen ?? state.selectedScreen);
    final screenKey = screen ?? 'all';
    state = state.copyWith(
      runtimeState: {
        ...state.runtimeState,
        screenKey: ActiveWallpaper(wallpaperId: id, isPlaying: true),
      },
    );
  }

  Future<void> stopWallpaper() async {
    final service = ref.read(wallpaperServiceProvider);
    await service.stopWallpaper();
    final updated = Map<String, ActiveWallpaper>.from(state.runtimeState);
    for (final key in updated.keys) {
      updated[key] = updated[key]!.copyWith(isPlaying: false);
    }
    state = state.copyWith(runtimeState: updated);
  }

  Future<void> applyRandomWallpaper() async {
    if (state.wallpapers.isEmpty) return;
    final random = state.wallpapers[
        (DateTime.now().millisecondsSinceEpoch) % state.wallpapers.length];
    await applyWallpaper(random.id, null);
  }

  void toggleFavorite(String id) {
    final favorites = Set<String>.from(state.favoriteIds);
    if (favorites.contains(id)) {
      favorites.remove(id);
    } else {
      favorites.add(id);
    }
    state = state.copyWith(favoriteIds: favorites);
  }

  void setSearchQuery(String query) {
    state = state.copyWith(searchQuery: query);
  }

  void setActiveTab(AppTab tab) {
    state = state.copyWith(activeTab: tab);
  }

  void setSortBy(SortBy sort) {
    state = state.copyWith(sortBy: sort);
  }

  void setSelectedScreen(String screen) {
    state = state.copyWith(selectedScreen: screen);
  }

  void toggleCompactMode(bool enabled) {
    state = state.copyWith(isCompactMode: enabled);
  }

  void setNickname(String id, String nickname) {
    final updated = Map<String, String>.from(state.nicknames);
    final trimmed = nickname.trim();
    if (trimmed.isEmpty || trimmed.length > 100) return;
    updated[id] = trimmed;
    state = state.copyWith(nicknames: updated);
  }

  String? getNickname(String id) => state.nicknames[id];

  Future<void> fetchSettings() async {
    state = state.copyWith(settingsLoading: true);
    final service = ref.read(settingsServiceProvider);
    final settings = await service.fetchSettings();
    state = state.copyWith(
      settings: settings,
      settingsLoading: false,
    );
  }

  Future<void> saveSettings() async {
    if (state.settings == null) return;
    final service = ref.read(settingsServiceProvider);
    await service.saveSettings(state.settings!);
  }

  void updateSettings(AppConfig settings) {
    state = state.copyWith(settings: settings);
  }

  Future<void> fetchMonitors() async {
    state = state.copyWith(monitorsLoading: true);
    final service = ref.read(wallpaperServiceProvider);
    final monitors = await service.getMonitors();
    state = state.copyWith(monitors: monitors, monitorsLoading: false);
  }

  Future<void> loadPlaylists() async {
    final service = ref.read(wallpaperServiceProvider);
    final playlists = await service.getPlaylists();
    state = state.copyWith(playlists: playlists);
  }

  Future<void> createPlaylist(String name, List<String> wallpaperIds) async {
    final now = DateTime.now().millisecondsSinceEpoch;
    final playlist = Playlist(
      id: 'playlist_$now',
      name: name,
      wallpaperIds: wallpaperIds,
      createdAt: now,
      updatedAt: now,
    );
    state = state.copyWith(playlists: [...state.playlists, playlist]);
  }

  Future<void> deletePlaylist(String id) async {
    final playlists = state.playlists.where((p) => p.id != id).toList();
    state = state.copyWith(
      playlists: playlists,
      clearActivePlaylistId: state.activePlaylistId == id,
      clearCyclePlaylistId: state.cyclePlaylistId == id,
    );
  }

  void setActivePlaylist(String? id) {
    state = state.copyWith(
      activePlaylistId: id,
      clearActivePlaylistId: id == null,
    );
  }

  void togglePlaylistSidebar() {
    state = state.copyWith(isPlaylistSidebarOpen: !state.isPlaylistSidebarOpen);
  }

  void enterSelectionMode() {
    state = state.copyWith(isSelectionMode: true, selectedForPlaylist: {});
  }

  void exitSelectionMode() {
    state = state.copyWith(isSelectionMode: false, selectedForPlaylist: {});
  }

  void toggleSelectForPlaylist(String wallpaperId) {
    final selected = Set<String>.from(state.selectedForPlaylist);
    if (selected.contains(wallpaperId)) {
      selected.remove(wallpaperId);
    } else if (selected.length < 100) {
      selected.add(wallpaperId);
    }
    state = state.copyWith(selectedForPlaylist: selected);
  }

  void addLog(LogEntry entry) {
    state = state.copyWith(logs: [...state.logs, entry]);
  }
}

final appProvider = NotifierProvider<AppNotifier, AppState>(() => AppNotifier());