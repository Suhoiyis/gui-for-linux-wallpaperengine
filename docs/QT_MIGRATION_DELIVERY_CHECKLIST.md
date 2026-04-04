# Qt Quick Migration Delivery Checklist

This checklist captures the current migration delivery state for the new Qt Quick UI (`py_GUI/ui/qt`).

## Completed Scope

- App shell and page container are implemented with `StackLayout`:
  - Library page
  - Performance page
  - Settings page
- Library flow is implemented and wired to Python core modules:
  - Wallpaper grid/card selection
  - Apply wallpaper (single screen + linked all-screen mode)
  - Favorite toggle
  - Search and sort
  - Sidebar details with description and tags
  - Copy wallpaper ID and open Workshop URL actions
- Playlist flow is implemented:
  - Three-state panel (`minimized` / `floating` / `locked`)
  - Create / rename / delete playlists
  - Active playlist filtering in grid
- Nickname flow is implemented:
  - Edit nickname dialog
  - Display nickname with original title as secondary text
- Settings flow is implemented for core keys:
  - `fps`, `volume`, `silence`, `scaling`, `clamping`, `workshopPath`, `apply_mode`
  - Backend writes are persisted through existing config manager
- Performance flow is implemented:
  - Total CPU / memory / thread overview
  - Process details list from performance monitor bridge

## Hardening Included

- Dialog validation hardening:
  - Disabled invalid accept states where applicable
  - Enter-to-accept behavior gated by validity
- Playlist duplicate-name guard in backend create/rename operations
- Settings controls now synchronize with backend updates
- Runtime-safe clipboard action handling (graceful fallback if unavailable)

## Known Limits (Current Stage)

- Performance page currently focuses on textual/card metrics and process rows (no sparkline chart parity yet)
- Settings page currently targets core controls only; advanced/secondary options are not fully ported
- Some Tauri-specific visual nuances are approximated in QML styling rather than pixel-identical
- Local runtime may print GTK theme parser warnings in this environment; Qt feature behavior remains functional

## Quick Regression Steps

Run:

```bash
python3 py_GUI/ui/qt/main.py
```

Expected smoke results:

1. Library page
   - Grid renders wallpapers
   - Selecting card updates sidebar
   - Apply button works
   - Favorite toggle works
   - Search/sort change visible ordering

2. Sidebar utilities
   - Copy ID triggers status update
   - Workshop button attempts external open
   - Description/tags visible (or fallback text)

3. Playlist panel
   - Panel transitions between minimized/floating/locked
   - Create/rename/delete dialogs operate
   - Active playlist filters grid

4. Settings page
   - FPS/volume/silence/scaling/clamping/workshopPath/apply mode update backend state

5. Performance page
   - Total CPU/memory/threads visible
   - Process rows visible when monitor has data

## Acceptance Status

- Current status: **Ready for daily trial usage** in development environment
- Next recommended stage: visual polish + advanced settings parity + optional chart parity
