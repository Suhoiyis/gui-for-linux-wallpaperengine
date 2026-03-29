import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";

export function usePreviewUrl(preview: string | undefined): string | null {
  const [url, setUrl] = useState<string | null>(null);

  useEffect(() => {
    if (!preview) {
      setUrl(null);
      return;
    }

    if (preview.startsWith("http://") || preview.startsWith("https://")) {
      setUrl(preview);
      return;
    }

    let cancelled = false;
    
    invoke<string>("read_preview_image", { path: preview })
      .then((dataUrl) => {
        if (!cancelled) {
          setUrl(dataUrl);
        }
      })
      .catch(() => {
        if (!cancelled) setUrl(null);
      });

    return () => {
      cancelled = true;
    };
  }, [preview]);

  return url;
}