import { describe, it, expect } from "vitest";
import {
  normalizeLinuxPath,
  splitLinuxPathSegments,
  expandTildePath,
  collapseHomeToTilde,
  buildLinuxPathCrumbs,
} from "./linuxPath";

describe("linuxPath", () => {
  it("normalizes linux paths (trim, collapse slashes, strip trailing)", () => {
    expect(normalizeLinuxPath("  /a//b///  ")).toBe("/a/b");
    expect(normalizeLinuxPath("/")).toBe("/");
    expect(normalizeLinuxPath("")).toBe("");
  });

  it("splits segments correctly", () => {
    expect(splitLinuxPathSegments("/")).toEqual([]);
    expect(splitLinuxPathSegments("/a/b/")).toEqual(["a", "b"]);
    expect(splitLinuxPathSegments("a/b")).toEqual(["a", "b"]);
  });

  it("expands leading ~ when homeDir is available", () => {
    expect(expandTildePath("~", "/home/u")).toBe("/home/u");
    expect(expandTildePath("~/x", "/home/u/")).toBe("/home/u/x");
    expect(expandTildePath("~user/x", "/home/u")).toBe("~user/x");
  });

  it("collapses home prefixes to ~ safely", () => {
    expect(collapseHomeToTilde("/home/u", "/home/u")).toBe("~");
    expect(collapseHomeToTilde("/home/u/x", "/home/u")).toBe("~/x");
    expect(collapseHomeToTilde("/home/uu/x", "/home/u")).toBe("/home/uu/x");
  });

  it("builds crumbs for absolute paths", () => {
    expect(buildLinuxPathCrumbs({ value: "/a/b", homeDir: null })).toEqual([
      { label: "/", fullPath: "/" },
      { label: "a", fullPath: "/a" },
      { label: "b", fullPath: "/a/b" },
    ]);
  });

  it("builds crumbs for home paths using ~", () => {
    expect(buildLinuxPathCrumbs({ value: "/home/u/.local", homeDir: "/home/u" })).toEqual([
      { label: "~", fullPath: "/home/u" },
      { label: ".local", fullPath: "/home/u/.local" },
    ]);
    expect(buildLinuxPathCrumbs({ value: "/home/u", homeDir: "/home/u" })).toEqual([
      { label: "~", fullPath: "/home/u" },
    ]);
  });
});
