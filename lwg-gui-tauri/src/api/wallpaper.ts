import { invoke } from "@tauri-apps/api/core";
import { Wallpaper, HistoryEntry } from "@/types";

// ================= Screenshot Types =================
export interface ScreenshotRecord {
  timestamp: number;
  wpId: string;
  outputPath: string;
  duration: number;
  maxCpu: number;
  maxMem: number;
}

// ================= Mock Data =================
const BASE_MOCK_TEMPLATES: Wallpaper[] = [
  {
    id: "base_2",
    title: "Anime Landscape",
    preview:
      "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=500&q=80",
    path: "mock/path/2.jpg",
    type: "Scene",
    tags: ["Anime", "Scenery"],
    size: "5 MB",
  },
  {
    id: "base_3",
    title: "Neon Car",
    preview:
      "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=500&q=80",
    path: "mock/path/3.jpg",
    type: "Scene",
    tags: ["Cars", "Neon"],
    size: "8 MB",
  },
  {
    id: "base_4",
    title: "Abstract Waves",
    preview:
      "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=500&q=80",
    path: "mock/path/4.mp4",
    type: "Video",
    tags: ["Abstract", "4K"],
    size: "125 MB",
  },
  {
    id: "base_6",
    title: "Mountain Mist",
    preview:
      "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=500&q=80",
    path: "mock/path/6.jpg",
    type: "Scene",
    tags: ["Nature", "Mountain", "Mist"],
    size: "6 MB",
  },
  {
    id: "base_7",
    title: "Galaxy Starry",
    preview:
      "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=500&q=80",
    path: "mock/path/7.jpg",
    type: "Scene",
    tags: ["Space", "Stars", "Dark"],
    size: "7 MB",
  },
  {
    id: "base_8",
    title: "Minimalist Geometry",
    preview:
      "https://images.unsplash.com/photo-1507608869274-d3177c8bb4c7?w=500&q=80",
    path: "mock/path/8.mp4",
    type: "Video",
    tags: ["Minimal", "Geometry", "Art"],
    size: "94 MB",
  },
  {
    id: "base_9",
    title: "Ocean Sunset",
    preview:
      "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=500&q=80",
    path: "mock/path/9.jpg",
    type: "Scene",
    tags: ["Ocean", "Sunset", "Warm"],
    size: "5 MB",
  },
  {
    id: "base_10",
    title: "Tokyo Night Rain",
    preview:
      "https://images.unsplash.com/photo-1542051841857-5f90071e7989?w=500&q=80",
    path: "mock/path/10.mp4",
    type: "Video",
    tags: ["City", "Rain", "Japan"],
    size: "157 MB",
  },
  {
    id: "base_11",
    title: "Desert Dunes",
    preview:
      "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=500&q=80",
    path: "mock/path/11.jpg",
    type: "Scene",
    tags: ["Desert", "Sand", "Hot"],
    size: "4 MB",
  },
  {
    id: "base_12",
    title: "Northern Lights",
    preview:
      "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=500&q=80",
    path: "mock/path/12.jpg",
    type: "Scene",
    tags: ["Aurora", "Night", "Green"],
    size: "8 MB",
  },
];

// Generate expanded mock data
const EXPANDED_MOCK_WALLPAPERS = Array.from({ length: 1500 }).map((_, i) => {
  const template = BASE_MOCK_TEMPLATES[i % BASE_MOCK_TEMPLATES.length];
  return {
    ...template,
    id: `mock_wp_${i}`,
    title: `${template.title} #${i + 1}`,
  };
});

// ================= API Functions =================

export async function scanWallpapers(): Promise<Wallpaper[]> {
  try {
    const data = await invoke<any[]>("get_wallpapers");

    return data.map((item) => ({
      id: item.id,
      title: item.title,
      preview: item.preview,
      path: item.path || "",
      type: item.wtype === "video" ? "Video" : item.wtype === "web" ? "Web" : "Scene",
      description: item.description || undefined,
      tags: item.tags || [],
      size: item.size || "0 MB",
    }));
  } catch (error) {
    console.warn("⚠️ 环境检测：无法连接 Rust 后端，已切换至 Mock 数据模式。");
    await new Promise((resolve) => setTimeout(resolve, 600));
    return EXPANDED_MOCK_WALLPAPERS;
  }
}

export async function applyWallpaper(
  id: string,
  screen?: string,
): Promise<void> {
  try {
    await invoke("apply_wallpaper", { id, screen });
  } catch (e) {
    console.log(
      `[Mock] 假装应用了壁纸 ID: ${id}${screen ? ` 到屏幕 ${screen}` : ""}`,
    );
  }
}

export async function stopWallpaper(): Promise<void> {
  try {
    await invoke("stop_wallpaper");
  } catch (e) {
    console.log(`[Mock] 假装停止了壁纸`);
  }
}

export async function deleteWallpaper(
  id: string,
  path: string,
): Promise<void> {
  try {
    await invoke("delete_wallpaper", { wallpaperId: id, path });
  } catch (e) {
    console.warn(`[Mock] 假装删除了壁纸 ID: ${id}, 路径: ${path}`);
  }
}

export async function takeScreenshot(
  wallpaperId: string,
  outputPath?: string,
): Promise<ScreenshotRecord> {
  return await invoke("take_screenshot", { wallpaperId, outputPath });
}

export async function getScreenshotHistory(): Promise<ScreenshotRecord[]> {
  return await invoke("get_screenshot_history");
}

export async function openFolder(path: string): Promise<void> {
  await invoke("open_folder", { path });
}

export async function openImage(path: string): Promise<void> {
  await invoke("open_image", { path });
}

// ================= History =================

const MOCK_HISTORY: HistoryEntry[] = [
  {
    id: "2874425843",
    title: "Cyberpunk City Night",
    preview:
      "https://images.unsplash.com/photo-1605218427306-635ba2439af2?w=500&q=80",
    timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
  },
  {
    id: "2810924556",
    title: "Anime Landscape",
    preview:
      "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=500&q=80",
    timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
  },
];

let mockHistoryStore = [...MOCK_HISTORY];

export async function getHistory(): Promise<HistoryEntry[]> {
  try {
    return await invoke("get_history");
  } catch (e) {
    console.warn("⚠️ [Mock] 使用假的播放历史数据");
    await new Promise((resolve) => setTimeout(resolve, 300));
    return [...mockHistoryStore];
  }
}

export async function clearHistory(): Promise<void> {
  try {
    await invoke("clear_history");
  } catch (e) {
    console.warn("⚠️ [Mock] 清空假的播放历史数据");
    mockHistoryStore = [];
  }
}
