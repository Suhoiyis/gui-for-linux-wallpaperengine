# LWG (Linux Wallpaper Engine) GUI Project

## 项目概述

这是一个 Linux Wallpaper Engine 的图形用户界面项目，正在从旧的 Python 实现迁移到现代的 **Tauri + React + Rust** 架构。

### 核心目标

1. **向后兼容**：与旧版 Python 实现的 `config.json` 完全兼容
2. **现代化架构**：使用 Tauri 提供原生性能，React 提供流畅 UI
3. **跨平台潜力**：虽然主要面向 Linux，架构设计考虑了跨平台扩展

---

## 目录结构

```
suw/
├── lwg-gui-tauri/          # 🎯 主要开发区域 - Tauri 桌面应用
│   ├── src/                 # React 前端代码
│   │   ├── components/      # UI 组件
│   │   │   ├── ui/          # shadcn/ui 基础组件
│   │   │   ├── library/     # 壁纸库相关组件
│   │   │   ├── settings/    # 设置页面组件
│   │   │   └── ...
│   │   ├── pages/           # 页面组件 (Settings, Library, Performance)
│   │   ├── store/           # Zustand 状态管理
│   │   ├── api/             # Tauri API 封装
│   │   └── types.ts         # TypeScript 类型定义
│   │
│   ├── src-tauri/           # Tauri Rust 后端
│   │   ├── src/lib.rs       # 主要 Tauri 命令定义
│   │   ├── src/main.rs      # 入口点
│   │   └── Cargo.toml
│   │
│   └── public/README.md     # linux-wallpaperengine 使用说明
│
├── lwg-rs/                  # Rust 核心引擎
│   ├── crates/
│   │   ├── lwg-core/        # 🎯 核心逻辑实现
│   │   │   ├── src/config.rs      # 配置解析
│   │   │   ├── src/controller.rs  # 壁纸控制器
│   │   │   ├── src/wallpaper.rs   # 壁纸管理器
│   │   │   └── ...
│   │   ├── lwg-ipc/         # IPC 通信
│   │   ├── lwg-tray/        # 系统托盘
│   │   └── lwg-ui/          # GTK UI (备用前端)
│   └── Cargo.toml
│
├── py_GUI/                  # 📦 Legacy Python 实现 (仅供参考)
│   └── ...
│
└── .sisyphus/               # Agent 工作文件
    └── plans/               # 工作计划存储
```

---

## 技术栈

| 层级         | 技术                     | 用途                |
| ------------ | ------------------------ | ------------------- |
| **前端 UI**  | React 18 + TypeScript    | 组件化界面          |
| **样式**     | Tailwind CSS + shadcn/ui | 现代 UI 组件库      |
| **状态管理** | Zustand                  | 轻量级全局状态      |
| **桌面框架** | Tauri v2                 | 原生桌面应用        |
| **后端**     | Rust                     | 高性能原生逻辑      |
| **核心引擎** | linux-wallpaperengine    | 壁纸渲染引擎 (外部) |

---

## 关键数据流

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  React Frontend │────▶│   Tauri API     │────▶│   lwg-core      │
│  (Zustand Store)│     │   (lib.rs)      │     │   (Rust)        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                      │
                                                      ▼
                                              ┌─────────────────┐
                                              │ linux-wallpaper │
                                              │ engine (外部)    │
                                              └─────────────────┘
```

---

## 配置文件格式

配置文件位于 `/home/yua/.config/linux-wallpaperengine-gui/config.json`，与 Python 版本**完全兼容**。

### 关键配置字段

```json
{
  "fps": 30,
  "volume": 15,
  "muteAudio": false,
  "scaling": "default",
  "clamping": "clamp",
  "workshopPath": "/home/user/.local/share/Steam/steamapps/workshop/content/431960",
  "wallpaperProperties": {},
  "wallpaperNicknames": {},
  "activeMonitors": { "HDMI-1": "12345678" }
}
```

---

## 重要开发规则

### 1. 后端引擎参数传递

在 `lwg-rs/crates/lwg-core/src/controller.rs` 中，参数按以下优先级传递给引擎：

| 参数             | 引擎标志    | 说明                                            |
| ---------------- | ----------- | ----------------------------------------------- |
| `muteAudio=true` | `--silent`  | **最高优先级**，静音时不传其他音频参数          |
| `volume`         | `--volume`  | 仅非静音时传递                                  |
| `fps`            | `-f`        | 帧率限制                                        |
| `scaling`        | `--scaling` | 缩放模式                                        |
| `clamping`       | `--clamp`   | ⚠️ 注意：引擎参数是 `--clamp` 不是 `--clamping` |

### 2. 前后端字段映射

某些字段在前后端命名不同：

| 前端 (TypeScript) | 后端 (Rust)         | 说明              |
| ----------------- | ------------------- | ----------------- |
| `type`            | `wp_type` / `wtype` | 壁纸类型          |
| `muteAudio`       | `silence`           | 静音设置          |
| `description`     | 可选字段            | 需要在 API 层映射 |

### 3. 壁纸路径结构

```
{workshopPath}/{wallpaperId}/
├── project.json    # 壁纸元数据
├── preview.jpg     # 预览图
└── scene.json      # 场景文件 (或 index.html, video.mp4)
```

### 4. 壁纸 description 处理

壁纸的 `description` 字段可能包含：

- **BBCode 标签** (`[img]`, `[url]`, `[h1]` 等)
- **长 URL**
- **大量空格**（原作者用于"居中对齐"）

显示前需要清理，参考 `WallpaperSidebar.tsx` 中的 `cleanDescription` 函数。

---

## 常见任务

### 添加新的设置项

1. **前端类型**: 更新 `lwg-gui-tauri/src/types.ts`
2. **后端类型**: 更新 `lwg-rs/crates/lwg-core/src/config.rs`
3. **Tauri 映射**: 更新 `lwg-gui-tauri/src-tauri/src/lib.rs`
4. **参数传递**: 更新 `lwg-rs/crates/lwg-core/src/controller.rs`

### 添加新的 Tauri 命令

1. 在 `lib.rs` 中定义 `#[tauri::command]` 函数
2. 在 `lib.rs` 的 `invoke_handler` 中注册
3. 在前端 `src/api/` 中封装调用

### 运行项目

```bash
# 开发模式
cd lwg-gui-tauri
npm run tauri dev

# 构建
npm run tauri build

# 测试 Rust 核心
cd lwg-rs && cargo test
```

---

## 注意事项

### ⚠️ 引擎 README 与实际参数不符

`lwg-gui-tauri/public/README.md` 是 linux-wallpaperengine 的文档，但存在以下错误：

- 文档写 `--clamping`，实际参数是 `--clamp`
- 文档遗漏了 `--disable-particles` 参数

**开发时应以引擎源代码为准**，参考 `lwg-rs/crates/lwg-core/src/controller.rs` 中的实现。

### ⚠️ 不要随意修改 config.json 结构

配置文件需要与 Python 版本兼容，修改前请检查：

- `py_GUI/core/config.py` 中的字段定义
- `lwg-rs/crates/lwg-core/src/config.rs` 中的字段定义

### ⚠️ 前端 API 层需要手动映射

`src/api/wallpaper.ts` 中有字段映射逻辑，添加新字段时记得更新。

### 修改版本号：只需编辑 tauri.conf.json 的 version 字段

#### 手动同步版本号

```
npm run sync-version
```

#### 开发/构建时自动同步

```
npm run dev # predev 钩子自动同步
npm run build # prebuild 钩子自动同步
```

---

## 外部依赖

### linux-wallpaperengine

这是实际的壁纸渲染引擎，GUI 只是其前端。

- **安装路径**: `/opt/linux-wallpaperengine/linux-wallpaperengine`
- **官方仓库**: https://github.com/Almamu/linux-wallpaperengine
- **支持的参数**: 参见 `controller.rs` 或引擎源码 `ApplicationContext.cpp`

### Steam Workshop

壁纸默认存储在 Steam Workshop 目录：

```
~/.local/share/Steam/steamapps/workshop/content/431960/{wallpaperId}/
```

---

## 调试技巧

1. **Tauri 日志**: 查看 DevTools (Ctrl+Shift+I) 和终端输出
2. **Rust 日志**: 使用 `tracing` crate，日志级别在 `logger.rs` 中配置
3. **配置文件**: 手动编辑 `~/.config/lwg/config.json` 测试
4. **引擎测试**: 直接运行 `linux-wallpaperengine` 命令测试参数

---

## 联系信息

- 项目路径: `/home/yua/suw`
- 主要开发分支: `feature/tauri`
