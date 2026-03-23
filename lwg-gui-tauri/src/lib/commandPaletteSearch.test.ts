import { describe, it, expect } from "vitest";
import type { Playlist } from "@/types";
import {
  computePlaylistMatchedWallpaperCounts,
  mergeAndRankPlaylistsForSearch,
} from "./commandPaletteSearch";

function pl(
  id: string,
  name: string,
  wallpaperIds: string[],
  updatedAt: number
): Playlist {
  return {
    id,
    name,
    wallpaperIds,
    createdAt: 0,
    updatedAt,
  };
}

describe("commandPaletteSearch", () => {
  it("computes matched wallpaper counts per playlist", () => {
    const playlists: Playlist[] = [
      pl("p1", "One", ["w1", "w2"], 10),
      pl("p2", "Two", ["w2", "w3", "w4"], 20),
      pl("p3", "Three", [], 30),
    ];
    const matched = new Set<string>(["w2", "w4", "wX"]);

    const counts = computePlaylistMatchedWallpaperCounts(playlists, matched);

    expect(counts.get("p1")).toBe(1);
    expect(counts.get("p2")).toBe(2);
    expect(counts.has("p3")).toBe(false);
  });

  it("dedupes playlists present in both name-match and contains-match", () => {
    const playlists: Playlist[] = [
      pl("cycle", "Cycle", ["w1"], 50),
      pl("p1", "Alpha", ["w2"], 10),
      pl("p2", "Beta", ["w3"], 20),
    ];
    const nameMatchedPlaylists: Playlist[] = [playlists[1]]; // p1
    const counts = new Map<string, number>([
      ["p1", 1],
      ["p2", 1],
    ]);

    const result = mergeAndRankPlaylistsForSearch({
      playlists,
      nameMatchedPlaylists,
      matchedCountById: counts,
      cyclePlaylistId: null,
      limit: 10,
    });

    const ids = result.map((p) => p.id);
    expect(ids.filter((id) => id === "p1")).toHaveLength(1);
  });

  it("orders: cycle first, then name-match, then contains-only by matchCount then updatedAt", () => {
    const playlists: Playlist[] = [
      pl("cycle", "Cycle", ["w9"], 1),
      pl("name", "NameMatch", ["w1"], 10),
      pl("c2", "Contains2", ["w1", "w2"], 5),
      pl("c1new", "Contains1New", ["w2"], 100),
      pl("c1old", "Contains1Old", ["w2"], 50),
    ];
    const nameMatchedPlaylists: Playlist[] = [playlists[1]]; // name
    const counts = new Map<string, number>([
      ["cycle", 1],
      ["c2", 2],
      ["c1new", 1],
      ["c1old", 1],
    ]);

    const result = mergeAndRankPlaylistsForSearch({
      playlists,
      nameMatchedPlaylists,
      matchedCountById: counts,
      cyclePlaylistId: "cycle",
      limit: 10,
    });

    expect(result.map((p) => p.id)).toEqual([
      "cycle",
      "name",
      "c2",
      "c1new",
      "c1old",
    ]);
  });

  it("enforces limit", () => {
    const playlists: Playlist[] = [
      pl("p1", "One", ["w1"], 1),
      pl("p2", "Two", ["w2"], 2),
      pl("p3", "Three", ["w3"], 3),
    ];
    const nameMatchedPlaylists: Playlist[] = [playlists[0]];
    const counts = new Map<string, number>([
      ["p2", 1],
      ["p3", 1],
    ]);

    const result = mergeAndRankPlaylistsForSearch({
      playlists,
      nameMatchedPlaylists,
      matchedCountById: counts,
      cyclePlaylistId: null,
      limit: 2,
    });

    expect(result).toHaveLength(2);
  });

  it("does not throw if playlist.wallpaperIds is malformed", () => {
    const playlists = [
      { ...pl("bad", "Bad", ["w1"], 10), wallpaperIds: null as unknown as string[] },
      pl("ok", "Ok", ["w2"], 20),
    ] as Playlist[];

    const matched = new Set<string>(["w2"]);

    expect(() => computePlaylistMatchedWallpaperCounts(playlists, matched)).not.toThrow();

    const counts = computePlaylistMatchedWallpaperCounts(playlists, matched);
    expect(counts.get("ok")).toBe(1);
    expect(counts.has("bad")).toBe(false);
  });

  it("uses playlist id as final tie-breaker for deterministic sort", () => {
    const playlists: Playlist[] = [
      pl("b", "B", ["w1"], 100),
      pl("a", "A", ["w1"], 100),
    ];

    const result = mergeAndRankPlaylistsForSearch({
      playlists,
      nameMatchedPlaylists: [],
      matchedCountById: new Map<string, number>([
        ["a", 1],
        ["b", 1],
      ]),
      cyclePlaylistId: null,
      limit: 10,
    });

    expect(result.map((p) => p.id)).toEqual(["a", "b"]);
  });
});
