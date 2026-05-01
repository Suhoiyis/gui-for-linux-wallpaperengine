import { useState, useEffect } from "react";

// Convert local file path to Tauri v2 asset protocol URL.
// This lets WebKit load and manage images natively — no base64 IPC,
// no data-URL decoding overhead, and WebKit can discard decoded bitmaps
// under memory pressure.
function toAssetUrl(filePath: string): string {
  if (filePath.startsWith("http://") || filePath.startsWith("https://")) {
    return filePath;
  }
  if (filePath.startsWith("/")) {
    return `http://asset.localhost${filePath}`;
  }
  return "";
}

export function usePreviewUrl(preview: string | undefined): string | null {
  const [url, setUrl] = useState<string | null>(() => {
    if (!preview) return null;
    return toAssetUrl(preview) || null;
  });

  useEffect(() => {
    if (!preview) {
      setUrl(null);
      return;
    }

    const assetUrl = toAssetUrl(preview);
    if (assetUrl) {
      setUrl(assetUrl);
      return;
    }

    // Relative path — fall back to base64 IPC (rare in production)
    let cancelled = false;
    import("@tauri-apps/api/core").then(({ invoke }) => {
      invoke<string>("read_preview_image", { path: preview })
        .then((dataUrl) => {
          if (!cancelled) setUrl(dataUrl);
        })
        .catch(() => {
          if (!cancelled) setUrl(null);
        });
    });

    return () => {
      cancelled = true;
    };
  }, [preview]);

  return url;
}
