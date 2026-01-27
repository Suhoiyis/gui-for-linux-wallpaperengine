# Wallpaper Engine Linux Projects Analysis

> Analysis Date: Jan 27, 2026

## Overview

Two reverse-engineering projects that enable running **Wallpaper Engine** content on Linux:

| Project | Language | Maturity | Repository |
|---------|----------|----------|------------|
| **linux-wallpaperengine** (Almamu) | C++20 | Production-ready | `wallpaper_C++/` |
| **linux-wallpaperengine** (AzPepoze) | Go | Early development | `wallpaper_go/` |

---

## Project Comparison

### Code Structure

| Aspect | C++ | Go |
|--------|-----|-----|
| Source files | ~570+ | ~30 |
| Build system | CMake | Go modules |
| Rendering | Native OpenGL 3.3 | Raylib wrapper |
| Windowing | GLFW/GLEW | Raylib |
| Texture loading | Direct GPU upload | PNG conversion → Raylib |
| Shader support | HLSL→GLSL transpilation | Not implemented |
| Web wallpapers | Full CEF (Chromium) | Not implemented |
| Video wallpapers | MPV integration | Not implemented |

### Feature Support

| Feature | C++ | Go |
|---------|-----|-----|
| Scene wallpapers | ✅ Full | ⚠️ Basic |
| Video wallpapers | ✅ Full | ❌ |
| Web wallpapers | ✅ Full | ❌ |
| .pkg unpacking | ✅ | ✅ |
| .tex decoding | ✅ | ✅ |
| Particle systems | ✅ Complete | ⚠️ Basic emitters |
| Shader effects | ✅ Full | ❌ |
| Audio visualization | ✅ | ❌ |
| X11 support | ✅ | ✅ |
| Wayland support | ✅ wlr-layer-shell | ❌ |

### Dependencies

**C++ Project:**
- OpenGL 3.3, GLFW, GLEW
- SDL2, SDL2_mixer
- MPV (video playback)
- PulseAudio (audio capture)
- FFmpeg, LZ4
- CEF (Chromium Embedded Framework)
- FreeImage, nlohmann/json

**Go Project:**
- raylib-go
- pierrec/lz4
- iamGreedy/dxt (texture decompression)

---

## File Format Specifications

### 1. Package Container (`.pkg`)

**Header:** `PKGV0005` (8 bytes)

```
Offset  Size    Description
0x00    8       Magic "PKGV0005"
0x08    4       File count (uint32 LE)

For each file entry:
+0x00   4       Filename length (uint32 LE)
+0x04   N       Filename (N bytes, null-terminated)
+N      4       Data offset (uint32 LE)
+N+4    4       Data length (uint32 LE)

[Raw file data follows at specified offsets]
```

**Parsing (Go):**
```go
// From wallpaper_go/internal/convert/unpacker.go
type PkgEntry struct {
    Name   string
    Offset uint32
    Length uint32
}
```

### 2. Texture Format (`.tex`)

**Container Header:** `TEXV0005` (8 bytes)

**Image Header:** `TEXI0001` (8 bytes) followed by:

```
Offset  Size    Description
0x00    8       Magic "TEXI0001"
0x08    4       Format (uint32 LE)
0x0C    4       Flags (uint32 LE)
0x10    4       Texture width
0x14    4       Texture height
0x18    4       Image width
0x1C    4       Image height
```

**Supported Formats:**

| Format ID | Name | Description |
|-----------|------|-------------|
| 0 | ARGB8888 | 32-bit RGBA |
| 4 | DXT1 | BC1 compression (no alpha) |
| 6 | DXT3 | BC2 compression (sharp alpha) |
| 8 | DXT5 | BC3 compression (smooth alpha) |
| 17 | R8 | 8-bit grayscale |
| 18 | RG88 | 16-bit RG |

**Flags:**

| Flag | Value | Description |
|------|-------|-------------|
| NoInterpolation | 0x01 | Disable texture filtering |
| ClampUVs | 0x02 | Clamp instead of repeat |
| IsGif | 0x04 | Animated GIF data |
| LZ4Compression | 0x08 | LZ4 compressed |

**Mipmap Structure:**
```
For each mipmap level (TEXB0003 header):
- Magic "TEXB0003" (8 bytes)
- Width, Height (4 bytes each)
- Pixel count (4 bytes, may be compressed size)
- Reserved (24 bytes)
- Pixel data
```

### 3. Project Metadata (`project.json`)

```json
{
  "file": "scene.json",
  "general": {
    "properties": {
      "schemecolor": {
        "order": 0,
        "text": "ui_browse_properties_scheme_color",
        "type": "color",
        "value": "0.5 0.5 0.5"
      }
    }
  },
  "preview": "preview.jpg",
  "tags": ["Abstract", "Relaxing"],
  "title": "Wallpaper Title",
  "type": "scene",
  "visibility": "public",
  "workshopid": "123456789"
}
```

**Type Values:**
- `scene` - 2D/3D scene with effects
- `video` - Video file playback
- `web` - HTML/JS web content

### 4. Scene Definition (`scene.json`)

```json
{
  "camera": {
    "center": [0, 0, 0],
    "eye": [0, 0, 1],
    "up": [0, 1, 0]
  },
  "general": {
    "ambientcolor": "1 1 1",
    "bloom": false,
    "clearcolor": "0 0 0",
    "orthogonalprojection": {
      "auto": true,
      "height": 1080,
      "width": 1920
    },
    "skylightcolor": "1 1 1"
  },
  "objects": [
    {
      "image": "materials/texture.tex",
      "name": "Background",
      "origin": "0 0 0",
      "scale": "1 1 1",
      "angles": "0 0 0",
      "visible": true,
      "effects": [],
      "id": 1
    }
  ]
}
```

**Object Types:**
- **image** - Static/animated textures with effects
- **sound** - Audio sources
- **particle** - Particle emitter systems
- **light** - Light sources (scene 3D)

---

## Key Source Files

### C++ Project (`wallpaper_C++/`)

| File | Purpose |
|------|---------|
| `src/WallpaperEngine/Data/Parsers/ProjectParser.cpp` | project.json parsing |
| `src/WallpaperEngine/Data/Parsers/WallpaperParser.cpp` | scene.json parsing |
| `src/WallpaperEngine/Data/Parsers/PackageParser.cpp` | .pkg file extraction |
| `src/WallpaperEngine/Data/Parsers/TextureParser.cpp` | .tex format decoding |
| `src/WallpaperEngine/Data/Parsers/ObjectParser.cpp` | Scene object loading (~847 lines) |
| `src/WallpaperEngine/Render/` | OpenGL rendering pipeline |
| `src/WallpaperEngine/WebBrowser/` | CEF integration |

### Go Project (`wallpaper_go/`)

| File | Purpose |
|------|---------|
| `cmd/linux-wallpaperengine/main.go` | Entry point, CLI |
| `cmd/linux-wallpaperengine/loader.go` | Model/particle loading |
| `internal/convert/unpacker.go` | .pkg extraction |
| `internal/convert/texture.go` | .tex → PNG conversion |
| `internal/wallpaper/types.go` | Data structures |
| `internal/wallpaper/scene.go` | JSON unmarshaling |

---

## Implementation Notes

### Texture Loading Difference

**C++ (Direct OpenGL):**
```cpp
// Direct GPU texture creation from decoded data
glTexImage2D(GL_TEXTURE_2D, 0, internalFormat, 
             width, height, 0, format, type, data);
```

**Go (PNG Intermediate):**
```go
// Convert to PNG, then load via Raylib
img := image.NewRGBA(image.Rect(0, 0, width, height))
// ... decode texture data into img ...
png.Encode(buffer, img)
return rl.LoadTextureFromImage(rl.LoadImageFromMemory(".png", data))
```

### Shader Transpilation (C++ only)

The C++ version transpiles Wallpaper Engine's HLSL shaders to GLSL:
- Custom preprocessor for includes
- Type/function mapping (float4 → vec4, etc.)
- Semantic handling (TEXCOORD0 → varying)

### Particle System Complexity

C++ implementation handles:
- Initializers (lifetime, velocity, color, size, rotation)
- Operators (movement, gravity, color fade, size change)
- Emitters (box, sphere, line)
- Rendering modes (rope, oriented, billboard)

Go currently only has basic emitter support.

---

## Parent Project Context

The workspace root (`/home/yua/suw/`) contains:
- `py_GUI/` - Python GTK4 GUI for the C++ backend
- `linux-wallpaperengine-gui/` - Related GUI component

The user is building a frontend that wraps Almamu's C++ implementation.

---

## Potential Next Steps

1. **Improve Go implementation**
   - Add shader compilation/transpilation
   - Implement video playback (possibly via go-mpv)
   - Add web wallpaper support (webview?)

2. **Improve Python GUI**
   - Wallpaper preview thumbnails
   - Settings/properties editor
   - Multi-monitor configuration

3. **Format documentation**
   - Complete .tex format with all edge cases
   - Particle system JSON schema
   - Effect/material definitions

4. **Performance optimization**
   - Go: Direct OpenGL instead of PNG intermediates
   - GUI: Async wallpaper loading


不，我若想要自己移植呢？github上有一个比较成熟的移植项目Almamu/linux-wallpaperengine，我能否像他一样自己开发一个

这是一个非常硬核且令人兴奋的想法！如果你打算像 Almamu 那样“自己开发一个”，你实际上不是在做“移植”（Porting），而是在做逆向工程（Reverse Engineering）和运行时重实现（Runtime Re-implementation）。

因为 Wallpaper Engine 是闭源软件，你拿不到它的 C++ 源代码。你要做的事情本质上和 Wine 或者是游戏模拟器（Emulator）的开发者一样：解析它的资源文件，并写一个新的引擎把它们画出来。

如果你决心走这条路，以下是你需要攻克的技术架构和具体要求：

1. 核心技术难点拆解
要从零开发一个兼容 Linux 的 Wallpaper Engine 播放器，你需要分别实现以下四大模块：

A. 资源解析层 (The Asset Loader)
Wallpaper Engine 不直接使用 PNG/JPG，它会将资源打包。

.pkg 文件解包： 这是 Wallpaper Engine 的核心打包格式。你需要逆向分析其二进制结构，提取出里面的图片、JSON 配置文件和着色器代码。

.tex 纹理转换： 它通常不直接用标准图片格式，而是转换成了专门针对显卡优化的 .tex 格式（类似 DDS）。你需要写一个解析器，将这些二进制数据转换成 OpenGL/Vulkan 能读取的纹理。

参考工具： 这一步你可以参考 GitHub 上的 RePKG 项目，它是目前解析该格式的鼻祖。

B. 渲染引擎层 (The Rendering Engine)
这是最难的部分。Wallpaper Engine 的壁纸主要分三类，你的引擎需要分别处理：

Scene (场景类 - 3D/2D)：

这是最复杂的。你需要解析 scene.json 来构建场景图（Scene Graph）。

你需要处理 Shaders (着色器)。原版使用的是 DirectX (HLSL)，而 Linux 需要 OpenGL (GLSL) 或 Vulkan (SPIR-V)。你需要写一个转换层（Transpiler）或者手动重写一套兼容的 Shader 库来模拟原版的水波纹、粒子特效、光照效果。

Web (网页类)：

这相对简单，你需要在这个程序里嵌入一个浏览器内核（通常是 CEF - Chromium Embedded Framework）。

你需要通过 IPC（进程间通信）把你的配置参数注入到这个浏览器实例的 JavaScript 中。

Video (视频类)：

集成 libmpv 或 ffmpeg 库来解码视频流并在纹理上播放。

C. 逻辑交互层 (SceneScript Implementation)
Wallpaper Engine 使用一种叫 SceneScript 的语言（基于 JavaScript）来控制壁纸逻辑（比如鼠标移动时粒子的反应、点击事件）。

你需要集成一个 JS 引擎（如 Google V8 或 QuickJS）。

关键点： 你必须模拟 Wallpaper Engine 暴露给 JS 的 API（例如 engine.audio.getSpectrum()）。如果你的 API 名字或行为和原版不一致，创意工坊里的壁纸运行就会报错。

D. 窗口管理层 (Window Management - X11 vs Wayland)
在 Linux 上“把窗口画在图标后面”是一门黑魔法。

X11： 你需要获取 Root Window ID，并设法在这个窗口上绘制，或者创建一个无边框全屏窗口并强制将其层级设为最底层（Below）。

Wayland： 这是噩梦模式。Wayland 的安全性设计禁止普通程序随便往背景画图。你可能需要使用特定的 Wayland 协议（如 wlr-layer-shell）才能在 Hyprland 或 Sway 等合成器上实现。

2. 开发所需的技能树
如果你想单枪匹马完成这个项目，你需要点亮以下技能点：

编程语言： C++ (首选，性能最高，Almamu 用的就是 C++ 配合 Qt) 或 Rust。

图形编程： 熟练掌握 OpenGL 或 Vulkan。你需要懂得如何手动管理顶点缓冲（VBO）、纹理单元和帧缓冲（FBO）。

逆向工程： 会使用 Hex Editor (如 010 Editor) 分析二进制文件结构；能看懂基本的汇编，甚至使用 Ghidra/IDA 分析原版软件的某些逻辑。

Linux 系统编程： 理解 XLib/XCB (X11) 或 Wayland 协议。

3. 如何起步？(Roadmap)
如果你真的想动手，不要一开始就想做一个完整的播放器。建议按以下步骤进行：

Step 1: 搞定文件格式 (File Format) 写一个小工具，能够读取 Wallpaper Engine 的 project.json 和 .pkg 文件，并把里面的图片提取出来保存为 PNG。如果能做到这一步，说明你已经破解了它的文件系统。

提示：研究 RePKG 的源码。

Step 2: 渲染静态场景 (Static Rendering) 尝试用 C++ 和 OpenGL 写一个窗口，读取解包后的数据，仅仅把壁纸的背景图显示出来。然后尝试解析 .tex 文件直接渲染，不转存 PNG。

Step 3: 攻克 Shader (The Shader Challenge) 这是最大的难关。找一个简单的带特效的壁纸（比如有简单的呼吸灯效果），提取它的 Shader 代码。尝试手动将其从 HLSL 改写为 GLSL，并在你的程序中让它动起来。

Step 4: 嵌入窗口 (Root Window Drawing) 研究如何在 Linux 下把你的渲染窗口“钉”在桌面上，不被其他窗口遮挡，也不遮挡桌面图标。

4. 为什么这是一件很难的事？
Almamu/linux-wallpaperengine 之所以被称为“成熟”，是因为开发者花费了数年时间去猜测和模拟原版引擎的行为。

最大的挑战不是写代码，而是兼容性。Steam 创意工坊里有成千上万个壁纸，每个壁纸可能使用了不同的 Shader 组合、不同的粒子系统参数。原版 Wallpaper Engine 更新一个新功能（比如新的 HDR 支持），你的移植版就会立刻失效，直到你逆向出这个新功能是如何实现的。

你可以为我做的下一步： 如果你想从“解析文件”这一步开始尝试，你需要了解 .pkg 的具体数据结构吗？或者你想先了解一下 Linux 下如何通过 X11 获取桌面窗口句柄（Handle）的代码示例？