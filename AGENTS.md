# LWG (Linux Wallpaper Engine) GUI & Core Project Rules

## 🎯 Project Overview

This is a complex, multi-module project migrating a Linux Wallpaper Engine GUI from a legacy Python implementation to a modern **Tauri + React (TypeScript) + Rust** architecture.

- **Active Development Zone**: `lwg-gui-tauri/` (The new Tauri desktop app).
- **Core Engine (Source of Truth)**: `lwg-rs/crates/lwg-core/` (The native Rust core logic).
- **Legacy Reference**: `py_GUI/` (The old Python app, used strictly for backward compatibility reference).

## 📂 Directory Structure & Agent Navigation Guide

### 1. The New Frontend & Tauri Backend (`/lwg-gui-tauri/`)

This is where 90% of UI and frontend-to-backend integration tasks happen.

- `src/components/`: Modular React components using Tailwind CSS and shadcn/ui.
- `src/store/appStore.ts`: Zustand state management. Handles optimistic updates and debounced Tauri invokes.
- `src/pages/`: Main route views (Settings, Library, Performance, etc.).
- `src-tauri/src/lib.rs` & `main.rs`: The Tauri Rust backend. Exposes commands (`#[tauri::command]`) to the React frontend.

### 2. The Rust Core & Workspaces (`/lwg-rs/`)

This is the native Rust implementation of the engine.

- `crates/lwg-core/src/`: Contains the actual implementation for config parsing (`config.rs`), performance monitoring (`performance.rs`), and wallpaper control (`wallpaper.rs`).
- **CRITICAL**: When implementing backend logic in `lwg-gui-tauri/src-tauri/`, always check `lwg-rs/crates/lwg-core/` first to see how the engine expects the data to be formatted or handled.

### 3. The Legacy Python App (`/py_GUI/`)

Used strictly as a reference for backward compatibility.

- `ui/pages/`: Check these files to understand the original behavior of complex UI interactions.

## ⚠️ Core Development Rules

### Rule 1: Field Naming Compatibility

- The new Tauri app uses a **JSON file separation scheme** that differs from the Python version:
  - Field naming remains compatible via `#[serde(alias = "old_snake_case")]` in Rust structs
  - But the overall configuration structure has changed (separate `config.json` / `state.json` / `history.json` / `screenshot_history.json`)
- **Naming Conventions**: The React frontend uses `camelCase` (e.g., `waylandOnlyActive`). The legacy Python config and Rust backend use `snake_case` (e.g., `wayland_only_active`).
- **Implementation Strategy**: In Rust (`src-tauri`), use `#[serde(alias = "old_snake_case_name")]` on configuration structs to seamlessly parse legacy configs while outputting camelCase for the frontend.
- **Empty or Missing Fields**: Always use `Option<T>` for optional or frequently missing fields in Rust structs (like `description: Option<String>`) to prevent JSON deserialization panics.

### Rule 2: State Management & Tauri Invokes (Hybrid Save Strategy)

- **Source of Truth**: The React frontend relies on `src/store/appStore.ts` (Zustand) as the immediate source of truth for the UI.
- **Optimistic Updates**: Always update the local Zustand store immediately for snappy UI feedback.
- **Debouncing**: Changes to Sliders (e.g., `volume`, `fps`) and text inputs must be debounced by **500ms** before calling a Tauri `invoke` to save, preventing I/O flooding.
- **Runtime vs. Persistent State**:
  - Settings that represent actual user preferences go to `config.json`.
  - Runtime state (screen → wallpaper mappings) is persisted to `state.json` for multi-monitor wallpaper restoration. This file can be safely deleted - the app will start with an empty state.
- **Error Handling**: Always wrap Tauri `invoke` calls in `try/catch`. If the backend fails, revert the Zustand state to its previous value and show a `toast.error`.

### Rule 3: UI & Styling Guidelines

- **Framework**: Strictly use **Tailwind CSS** and **shadcn/ui** components. Do not introduce new component libraries without permission.
- **Animations**: For conditionally rendered expansion panels (like accordions or settings groups), apply standard Tailwind animation classes: `animate-in fade-in slide-in-from-top-2 duration-300`.
- **Text Rendering**: For long descriptions or backend logs, always use CSS classes like `whitespace-pre-wrap` to preserve line breaks, and `line-clamp-N` to prevent layout overflow.
- **Environment Safety**: Before invoking any Tauri API (`invoke`, `listen`), verify the environment using: `const isTauri = !!(window as any).__TAURI_INTERNALS__;`. Provide mock fallbacks for browser testing.

## 🤖 Instructions for the AI Agent

1. **Never guess config keys**: If asked to implement a new setting, grep `lwg-rs/crates/lwg-core/src/config.rs` and `py_GUI/core/config.py` to find the exact key name.
2. **Verify Tauri Commands**: Before writing `invoke('some_command')` in React, verify that `some_command` is actually defined and registered in `lwg-gui-tauri/src-tauri/src/lib.rs`.
3. **Check standard UI components**: Before building a new form element, check `lwg-gui-tauri/src/components/settings/Shared.tsx` for existing reusable wrappers (like `SliderRow`, `SwitchRow`, `EditableComboboxField`).
4. **Prefer Tauri Native APIs**: When interacting with the OS (e.g., fetching monitors, dialogs, clipboard), prefer `@tauri-apps/api` over executing shell commands (`std::process::Command`), UNLESS the backend core engine strictly requires native output (like `xrandr` connector names).
5. **Listen to Events**: Favor Tauri's event-driven architecture. For things like logs or wallpaper status changes, the Rust backend should use `app.emit()`, and the frontend should use `listen()` in a `useEffect` with proper cleanup, rather than polling the backend.

---

## 📦 Version Management

Version numbers must be kept in sync across these files:

| File | Field | Example |
|------|-------|---------|
| `src-tauri/Cargo.toml` | `version = "0.1.0"` | Rust crate version |
| `src-tauri/tauri.conf.json` | `"version": "0.1.0"` | Tauri app version |
| `package.json` | `"version": "0.1.0"` | NPM package version |

**Sync Commands**:
- Manual: `npm run sync-version`
- Auto: Runs in `predev` and `prebuild` hooks

---

## 🔌 Tauri Plugin Status

| Plugin | Status | Usage |
|--------|--------|-------|
| single-instance | ✅ Active | Prevents multiple instances, focuses main window on second launch |
| window-state | ✅ Active | Persists window position and size across sessions |
| autostart | ✅ Used | Settings page toggle for auto-start on login |
| notification | ✅ Used | Random wallpaper switch, screenshot completion notifications |
| opener | ✅ Used | Open GitHub releases, Steam Workshop URLs |
| dialog | ✅ Used | Folder path selection in Settings page |
| fs | ⚠️ Registered | File operations done in Rust backend, frontend not using |
| shell | ⚠️ Registered | Command execution done in Rust backend, frontend not using |

**Status Legend**:
- ✅ Active: Plugin registered and automatically working
- ✅ Used: Plugin registered and actively used in business logic
- ⚠️ Registered: Plugin added but not currently used

---

## 📝 Logging System

Log sources and their content:

| Source | Definition | Content |
|--------|------------|---------|
| **Engine** | linux-wallpaperengine process stdout/stderr | Engine status, video decoding, hardware acceleration, errors |
| **GUI** | Tauri app frontend/backend operations | User interactions, UI events, state changes |
| **Controller** | WallpaperController | Wallpaper apply/stop, process management, screen operations |
| **Core** | lwg-core library | Config parsing, internal utilities |

**Implementation**: See `lwg-rs/crates/lwg-core/src/logger.rs`

---

## 🖼️ System Tray Implementation

**Decision**: Use Tauri built-in Tray (not tray_rs sidecar)

| Feature | Tauri Built-in | tray_rs |
|---------|----------------|---------|
| Tray icon | ✅ Supported | ✅ Supported |
| Context menu | ✅ Supported | ✅ Supported |
| Left/right click events | ✅ Supported | ✅ Supported |
| Dynamic icon switching | ✅ Supported | ✅ Supported |
| Tooltip (Linux) | ❌ Not supported | ✅ Supported |
| Pango markup formatting | ❌ Not supported | ✅ Supported |

**Trade-off**: Tooltip not supported on Linux, but simpler architecture (same process, no IPC, no separate process management).

**Alternative**: Use dynamic menu items to display multi-monitor status instead of tooltip.

---

## ⚠️ App Restart Known Issue

**Symptom**: In `npm run tauri dev` mode, clicking restart shows white screen or connection refused.

**Cause**: Dev mode webview connects to Vite dev server (`localhost:1420`). Restarting the binary doesn't reconnect properly.

**Workaround**: Manually restart (Ctrl+C and re-run) during development. Production builds work correctly.
