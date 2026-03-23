import { describe, it, expect, beforeEach } from "vitest";
import { useAppStore } from "./appStore";
import { Wallpaper } from "../types";

describe("appStore - getSelectedWallpaper", () => {
  beforeEach(() => {
    // Reset the store state before each test
    // const { wallpapers, selectedId } = useAppStore.getState();
    useAppStore.setState({
      wallpapers: [],
      selectedId: null,
    });
  });

  it("returns wallpaper when selectedId matches a wallpaper id", () => {
    // Setup: Add wallpapers to the store
    const mockWallpapers: Wallpaper[] = [
      {
        id: "wallpaper-1",
        title: "Ocean Wave",
        preview: "ocean.jpg",
        type: "Video",
        path: "/path/to/ocean",
      },
      {
        id: "wallpaper-2",
        title: "Forest Scene",
        preview: "forest.jpg",
        type: "Scene",
        path: "/path/to/forest",
      },
    ];

    useAppStore.setState({
      wallpapers: mockWallpapers,
      selectedId: "wallpaper-1",
    });

    // Act
    const result = useAppStore.getState().getSelectedWallpaper?.();

    // Assert
    expect(result).toBeDefined();
    expect(result).toEqual(mockWallpapers[0]);
    expect(result?.id).toBe("wallpaper-1");
    expect(result?.title).toBe("Ocean Wave");
  });

  it("returns null when selectedId is null", () => {
    // Setup: Add wallpapers but leave selectedId as null
    const mockWallpapers: Wallpaper[] = [
      {
        id: "wallpaper-1",
        title: "Ocean Wave",
        preview: "ocean.jpg",
        type: "Video",
        path: "/path/to/ocean",
      },
    ];

    useAppStore.setState({
      wallpapers: mockWallpapers,
      selectedId: null,
    });

    // Act
    const result = useAppStore.getState().getSelectedWallpaper?.();

    // Assert
    expect(result).toBeNull();
  });

  it("returns null when selectedId does not match any wallpaper", () => {
    // Setup: Add wallpapers with selectedId that doesn't exist
    const mockWallpapers: Wallpaper[] = [
      {
        id: "wallpaper-1",
        title: "Ocean Wave",
        preview: "ocean.jpg",
        type: "Video",
        path: "/path/to/ocean",
      },
      {
        id: "wallpaper-2",
        title: "Forest Scene",
        preview: "forest.jpg",
        type: "Scene",
        path: "/path/to/forest",
      },
    ];

    useAppStore.setState({
      wallpapers: mockWallpapers,
      selectedId: "non-existent-id",
    });

    // Act
    const result = useAppStore.getState().getSelectedWallpaper?.();

    // Assert
    expect(result).toBeNull();
  });
});
