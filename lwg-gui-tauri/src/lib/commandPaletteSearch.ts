import type { Playlist } from "@/types";

export function computePlaylistMatchedWallpaperCounts(
  playlists: Playlist[],
  matchedWallpaperIds: Set<string>
): Map<string, number> {
  const counts = new Map<string, number>();
  if (matchedWallpaperIds.size === 0) return counts;

  for (const p of playlists) {
    let count = 0;

    // Guard against malformed wallpaperIds
    const rawIds: unknown = (p as unknown as { wallpaperIds?: unknown }).wallpaperIds;
    const wallpaperIds = Array.isArray(rawIds) ? rawIds : [];

    for (const wid of wallpaperIds) {
      if (typeof wid !== "string") continue;
      if (matchedWallpaperIds.has(wid)) count += 1;
    }

    if (count > 0) counts.set(p.id, count);
  }

  return counts;
}

export interface MergeAndRankPlaylistsForSearchParams {
  playlists: Playlist[];
  nameMatchedPlaylists: Playlist[];
  matchedCountById: Map<string, number>;
  cyclePlaylistId: string | null;
  limit: number;
}

/**
 * Merge and rank playlists for CommandPalette search.
 *
 * Rules:
 * - dedupe by playlist.id
 * - cycle playlist first (if present)
 * - name/id-matched playlists before contains-only playlists
 * - contains-only playlists ordered by matchedCount desc then updatedAt desc
 * - final fallback: updatedAt desc, then id asc for determinism
 * - return capped by `limit`
 */
export function mergeAndRankPlaylistsForSearch({
  playlists,
  nameMatchedPlaylists,
  matchedCountById,
  cyclePlaylistId,
  limit,
}: MergeAndRankPlaylistsForSearchParams): Playlist[] {
  if (limit <= 0) return [];

  const nameMatchedIds = new Set(nameMatchedPlaylists.map((p) => p.id));

  // merged candidates: anything name-matched OR contains-matched
  const byId = new Map<string, Playlist>();
  for (const p of nameMatchedPlaylists) byId.set(p.id, p);
  for (const p of playlists) {
    if ((matchedCountById.get(p.id) ?? 0) > 0) byId.set(p.id, p);
  }

  const merged = Array.from(byId.values());
  merged.sort((a, b) => {
    const aCycle = cyclePlaylistId != null && a.id === cyclePlaylistId ? 1 : 0;
    const bCycle = cyclePlaylistId != null && b.id === cyclePlaylistId ? 1 : 0;
    if (aCycle !== bCycle) return bCycle - aCycle;

    const aName = nameMatchedIds.has(a.id) ? 1 : 0;
    const bName = nameMatchedIds.has(b.id) ? 1 : 0;
    if (aName !== bName) return bName - aName;

    // contains-only ordering by match count
    if (aName === 0 && bName === 0) {
      const ac = matchedCountById.get(a.id) ?? 0;
      const bc = matchedCountById.get(b.id) ?? 0;
      if (ac !== bc) return bc - ac;
    }

    // updatedAt descending
    const updatedAtDiff = b.updatedAt - a.updatedAt;
    if (updatedAtDiff !== 0) return updatedAtDiff;

    // Final tie-breaker: id ascending for deterministic sort
    return a.id.localeCompare(b.id);
  });

  return merged.slice(0, limit);
}
