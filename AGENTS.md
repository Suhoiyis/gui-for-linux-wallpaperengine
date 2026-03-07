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

### Rule 1: Backward Compatibility is Mandatory

- The new Tauri app MUST be fully backward compatible with the Python app's `config.json`.

## 🤖 Instructions for the AI Agent

1. **Never guess config keys**: If asked to implement a new setting, grep `lwg-rs/crates/lwg-core/src/config.rs` and `py_GUI/core/config.py` to find the exact key name.
2. **Verify Tauri Commands**: Before writing `invoke('some_command')` in React, verify that `some_command` is actually defined and registered in `lwg-gui-tauri/src-tauri/src/lib.rs`.
3. **Check standard UI components**: Before building a new form element, check `lwg-gui-tauri/src/components/settings/Shared.tsx` for existing reusable wrappers (like `SliderRow`, `SwitchRow`, `EditableComboboxField`).
