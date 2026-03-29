import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { convertFileSrc } from "@tauri-apps/api/core";

/**
 * Tauri window 接口，用于类型安全的环境检测
 */
interface TauriWindow extends Window {
  __TAURI_INTERNALS__?: unknown;
}

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * 检测是否在 Tauri 环境中运行
 */
export const isTauriEnv = (): boolean => {
  return !!(window as TauriWindow).__TAURI_INTERNALS__;
};

/**
 * 获取壁纸预览 URL
 * 处理本地路径和远程 URL
 */
export const getPreviewUrl = (preview: string): string => {
  if (preview.startsWith("http://") || preview.startsWith("https://")) {
    return preview;
  }
  return convertFileSrc(preview);
};

/**
 * 解析文件大小字符串为 MB 数值
 */
export const parseSize = (rawSize?: string | number | null): number => {
  if (rawSize === null || rawSize === undefined) return 0;
  if (typeof rawSize === "number") return rawSize;

  const sizeStr = String(rawSize).toUpperCase();
  const num = parseFloat(sizeStr);
  if (isNaN(num)) return 0;

  if (sizeStr.includes("GB")) return num * 1024;
  if (sizeStr.includes("KB")) return num / 1024;
  return num; // MB
};

/**
 * 标准化壁纸类型
 * 将后端返回的 wtype 转换为前端统一类型
 */
export const normalizeType = (wtype: string | undefined): "Video" | "Scene" | "Web" => {
  const map: Record<string, "Video" | "Scene" | "Web"> = {
    video: "Video",
    scene: "Scene",
    web: "Web",
  };
  return map[wtype?.toLowerCase() || ""] || "Scene";
};

/**
 * 根据标签内容生成固定的颜色类名
 * 使用简单的哈希算法确保同一标签始终显示相同颜色
 */
export const getColorForTag = (tag: string) => {
  const colors = [
    "bg-blue-100 text-blue-700 hover:bg-blue-100/80 border-blue-200 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800",
    "bg-green-100 text-green-700 hover:bg-green-100/80 border-green-200 dark:bg-green-900/30 dark:text-green-300 dark:border-green-800",
    "bg-purple-100 text-purple-700 hover:bg-purple-100/80 border-purple-200 dark:bg-purple-900/30 dark:text-purple-300 dark:border-purple-800",
    "bg-pink-100 text-pink-700 hover:bg-pink-100/80 border-pink-200 dark:bg-pink-900/30 dark:text-pink-300 dark:border-pink-800",
    "bg-yellow-100 text-yellow-700 hover:bg-yellow-100/80 border-yellow-200 dark:bg-yellow-900/30 dark:text-yellow-300 dark:border-yellow-800",
    "bg-indigo-100 text-indigo-700 hover:bg-indigo-100/80 border-indigo-200 dark:bg-indigo-900/30 dark:text-indigo-300 dark:border-indigo-800",
    "bg-red-100 text-red-700 hover:bg-red-100/80 border-red-200 dark:bg-red-900/30 dark:text-red-300 dark:border-red-800",
    "bg-orange-100 text-orange-700 hover:bg-orange-100/80 border-orange-200 dark:bg-orange-900/30 dark:text-orange-300 dark:border-orange-800",
    "bg-teal-100 text-teal-700 hover:bg-teal-100/80 border-teal-200 dark:bg-teal-900/30 dark:text-teal-300 dark:border-teal-800",
  ];

  // 简单的哈希算法：计算字符串 ASCII 码之和
  let hash = 0;
  for (let i = 0; i < tag.length; i++) {
    hash += tag.charCodeAt(i);
  }

  return colors[hash % colors.length];
};
export interface DisplayNameResult {
  displayName: string;
  originalTitle: string | null;
}

/**
 * Get display name for a wallpaper, considering nickname
 * Returns both the display name and original title (if nickname exists)
 * 
 * IMPORTANT: This is a PURE FUNCTION - components must subscribe to nicknames
 * state via selector for React reactivity:
 * 
 * const nicknames = useAppStore((state) => state.nicknames);
 * const { displayName, originalTitle } = getDisplayName(nicknames, wp.id, wp.title);
 */
export function getDisplayName(
  nicknames: Record<string, string>,
  wallpaperId: string,
  fallbackTitle: string
): DisplayNameResult {
  const nickname = nicknames[wallpaperId];
  if (nickname) {
    return { displayName: nickname, originalTitle: fallbackTitle };
  }
  return { displayName: fallbackTitle, originalTitle: null };
}
