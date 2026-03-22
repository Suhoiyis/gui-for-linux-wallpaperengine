// src/lib/linuxPath.ts

export type LinuxPathCrumb = {
  /** Human-friendly label (may include "~") */
  label: string;
  /** Canonical path value to set when navigating to this crumb */
  fullPath: string;
};

export function normalizeLinuxPath(input: string): string {
  const trimmed = input.trim();
  if (trimmed === "") return "";

  // Collapse consecutive slashes (Linux paths only)
  let out = trimmed.replace(/\/+/g, "/");

  // Remove trailing slash except for root
  if (out.length > 1 && out.endsWith("/")) {
    out = out.replace(/\/+$/g, "");
  }

  return out;
}

export function splitLinuxPathSegments(path: string): string[] {
  const normalized = normalizeLinuxPath(path);
  if (normalized === "" || normalized === "/") return [];

  const withoutLeading = normalized.startsWith("/")
    ? normalized.slice(1)
    : normalized;

  return withoutLeading.split("/").filter((s) => s.length > 0);
}

/**
 * Expand a leading "~" or "~/" to the provided homeDir.
 * If homeDir is unavailable, returns normalized input unchanged.
 */
export function expandTildePath(input: string, homeDir: string | null): string {
  const normalized = normalizeLinuxPath(input);
  if (!homeDir) return normalized;

  if (normalized === "~") return normalizeLinuxPath(homeDir);
  if (normalized.startsWith("~/")) {
    const home = normalizeLinuxPath(homeDir);
    return normalizeLinuxPath(home + "/" + normalized.slice(2));
  }
  return normalized;
}

/**
 * Collapse an absolute path under homeDir back to "~" for display.
 * If value is not under homeDir, returns normalized value unchanged.
 */
export function collapseHomeToTilde(
  value: string,
  homeDir: string | null,
): string {
  const v = normalizeLinuxPath(value);
  if (!homeDir) return v;

  const home = normalizeLinuxPath(homeDir);
  if (home === "") return v;

  if (v === home) return "~";
  if (v.startsWith(home + "/")) return "~/" + v.slice(home.length + 1);
  return v;
}

export function buildLinuxPathCrumbs(params: {
  value: string;
  homeDir: string | null;
}): LinuxPathCrumb[] {
  const normalized = normalizeLinuxPath(params.value);
  if (!normalized) return [];

  const home = params.homeDir ? normalizeLinuxPath(params.homeDir) : null;

  // Home-based crumbs (~) only for absolute paths under home
  if (home && (normalized === home || normalized.startsWith(home + "/"))) {
    const rel = normalized === home ? "" : normalized.slice(home.length + 1);
    const segments = rel ? rel.split("/").filter(Boolean) : [];

    const crumbs: LinuxPathCrumb[] = [{ label: "~", fullPath: home }];
    let current = home;
    for (const seg of segments) {
      current = normalizeLinuxPath(current + "/" + seg);
      crumbs.push({ label: seg, fullPath: current });
    }
    return crumbs;
  }

  // Absolute path crumbs
  if (normalized.startsWith("/")) {
    const segments = splitLinuxPathSegments(normalized);
    const crumbs: LinuxPathCrumb[] = [{ label: "/", fullPath: "/" }];
    let current = "";
    for (const seg of segments) {
      current = current ? current + "/" + seg : "/" + seg;
      crumbs.push({ label: seg, fullPath: current });
    }
    return crumbs;
  }

  // Relative / non-standard: show as a single non-root crumb
  const segments = splitLinuxPathSegments(normalized);
  const crumbs: LinuxPathCrumb[] = [];
  let current = "";
  for (const seg of segments) {
    current = current ? current + "/" + seg : seg;
    crumbs.push({ label: seg, fullPath: current });
  }
  return crumbs;
}
