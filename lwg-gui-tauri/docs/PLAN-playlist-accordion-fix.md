# Playlist Accordion UI Fix Plan

## TL;DR

> **Quick Summary**: Fix 5 issues with the playlist accordion UI: separate selection from toggle, allow multiple accordions open, fix thumbnail overflow logic, add right-aligned layout, and add remove wallpaper functionality.
> 
> **Deliverables**:
> - Fixed `PlaylistList.tsx` with `type="multiple"` accordion
> - Fixed `PlaylistItem.tsx` with proper layout and thumbnail logic
> - Remove wallpaper from playlist UI added
> 
> **Estimated Effort**: Quick
> **Parallel Execution**: NO - sequential changes to related files
> **Critical Path**: PlaylistList.tsx → PlaylistItem.tsx → Verification

---

## Context

### Original Request
User reported 5 issues with the playlist accordion UI:
1. Opening accordion should NOT change playlist selection
2. Accordions should allow multiple open (currently mutually exclusive)
3. Thumbnail overflow logic is broken (shows only +X with 2 thumbnails)
4. Missing remove wallpaper from playlist functionality
5. Badge count, accordion arrow, and 3-dot menu should be right-aligned

### Interview Summary
**Key Discussions**:
- User wants playlist name click to select, accordion arrow to just toggle
- Thumbnail strip should show N normal thumbnails, last one with +X overlay when overflow
- Need hover-to-reveal remove button on each thumbnail
- Layout: drag handle (left) | name | right side: badge + arrow + menu

**Research Findings**:
- `removeFromPlaylist` method already exists in `appStore.ts` (line 1099)
- Accordion component supports `type="multiple"` for non-exclusive behavior
- Thumbnail component accepts `className` for sizing

---

## Work Objectives

### Core Objective
Fix the playlist accordion UI to match user's expected behavior.

### Concrete Deliverables
- `PlaylistList.tsx`: Change `type="single"` to `type="multiple"`
- `PlaylistItem.tsx`: Complete refactor with all 5 fixes

### Definition of Done
- [ ] Multiple accordions can be open simultaneously
- [ ] Clicking playlist name selects it, clicking arrow only toggles expand
- [ ] Thumbnails show correctly with proper overflow logic
- [ ] Hover on thumbnail reveals remove button
- [ ] Badge, arrow, and menu are right-aligned
- [ ] `npx vitest run` passes
- [ ] No new TypeScript errors in playlist files

### Must Have
- Separate playlist selection from accordion toggle
- Fix thumbnail overflow calculation
- Right-aligned layout
- Remove wallpaper functionality

### Must NOT Have (Guardrails)
- Do not break existing drag-and-drop functionality
- Do not break rename/delete dialogs
- Do not modify store methods (already have `removeFromPlaylist`)

---

## TODOs

- [ ] 1. Fix PlaylistList.tsx - Change Accordion to type="multiple"

  **What to do**:
  - Change `<Accordion type="single" collapsible>` to `<Accordion type="multiple">`
  - This allows multiple accordions to be open simultaneously

  **Note (from review)**: When changing to `type="multiple"`, Radix UI expects `value`/`defaultValue` to be a string array. However, since our current code does NOT pass `value` or `defaultValue` (uncontrolled mode), this change is safe — just change the type attribute.

  **Must NOT do**:
  - Do not change the DndContext or SortableContext wrappers

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single line change
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 2
  - **Blocked By**: None

  **References**:
  - `lwg-gui-tauri/src/components/playlist/PlaylistList.tsx:71` - Current accordion implementation
  - `lwg-gui-tauri/src/components/ui/accordion.tsx` - Accordion component API

  **Acceptance Criteria**:
  - [ ] Multiple playlists can be expanded at the same time
  - [ ] No TypeScript errors

  **QA Scenarios**:
  ```
  Scenario: Multiple accordions open
    Tool: Browser dev at port 1420
    Steps:
      1. Create 3 playlists with wallpapers
      2. Expand first playlist
      3. Expand second playlist
      4. Verify first playlist is still expanded
    Expected Result: Both playlists show their thumbnail strips
  ```

- [ ] 2. Refactor PlaylistItem.tsx - Separate selection from toggle

  **What to do**:
  - Remove `onClick` from `AccordionTrigger`
  - Add a separate clickable element (the playlist name area) that triggers `setActivePlaylist`
  - The accordion arrow should only toggle expand/collapse
  - Keep the trigger for keyboard accessibility

  **Implementation approach**:
  ```tsx
  // Structure:
  <div class="flex items-center gap-1">
    {/* Drag handle */}
    <button {...attributes} {...listeners}>...</button>
    
    {/* Clickable name area - selects playlist */}
    <button 
      class="flex-1 text-left truncate"
      onClick={() => setActivePlaylist(playlist.id)}
    >
      {playlist.name}
    </button>
    
    {/* Right side: badge + accordion toggle + menu */}
    <Badge>{count}</Badge>
    {/* Empty AccordionTrigger renders only the chevron (auto-appended by Radix) */}
    <AccordionTrigger class="p-0.5 hover:bg-accent/50 rounded" />
    <DropdownMenu>...</DropdownMenu>
  </div>
  ```

  **Guardrail (from review)**: Our `AccordionTrigger` implementation (see `accordion.tsx`) automatically appends a `ChevronDown` icon after `{children}`. By passing NO children, the trigger will render ONLY the chevron. This is the correct approach — it preserves accessibility (keyboard navigation works) while separating selection from toggle behavior.

  **Must NOT do**:
  - Do not remove AccordionTrigger entirely (needed for accessibility)
  - Do not break the drag handle functionality

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: UI layout restructuring
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 3
  - **Blocked By**: Task 1

  **References**:
  - `lwg-gui-tauri/src/components/playlist/PlaylistItem.tsx:141-154` - Current trigger with onClick
  - `lwg-gui-tauri/src/components/ui/accordion.tsx` - Accordion component API

  **Acceptance Criteria**:
  - [ ] Clicking playlist name selects it (changes activePlaylistId)
  - [ ] Clicking accordion arrow only toggles expand/collapse
  - [ ] Keyboard navigation still works

- [ ] 3. Fix thumbnail overflow logic in PlaylistItem.tsx

  **What to do**:
  - The issue is `stripWidth` starts at 0, causing incorrect calculation
  - Use a reasonable default/fallback width or wait for real measurement
  - Logic should be:
    - Calculate how many thumbnails fit in the available width
    - If `total <= fitCount`, show all thumbnails
    - If `total > fitCount`, show `(fitCount - 1)` normal thumbnails + 1 with +X overlay
    - The +X overlay should be ON the last thumbnail, not replace all

  **Implementation fix**:
  ```tsx
  const SIDEBAR_WIDTH = 200; // Approximate sidebar width
  const THUMBNAIL_SIZE = 32;
  const GAP = 6;
  const PADDING = 16; // px-2 * 2
  
  const { shownIds, overflow, overflowThumbnailId } = useMemo(() => {
    // Use measured width or fall back to estimated
    const availableWidth = stripWidth > 0 ? stripWidth : SIDEBAR_WIDTH - PADDING;
    const fitCount = Math.max(1, Math.floor((availableWidth + GAP) / (THUMBNAIL_SIZE + GAP)));
    
    if (total === 0) {
      return { shownIds: [], overflow: 0, overflowThumbnailId: null };
    }
    
    if (total <= fitCount) {
      return { shownIds: thumbnailIds, overflow: 0, overflowThumbnailId: null };
    }
    
    // Show (fitCount - 1) normal + 1 with overlay
    // CRITICAL: Math.max(0, ...) to prevent negative slice indices
    const showCount = Math.max(0, fitCount - 1);
    const remainingCount = total - showCount;
    const overflowThumb = thumbnailIds[showCount] ?? thumbnailIds[0];
    
    return {
      shownIds: thumbnailIds.slice(0, showCount),
      overflow: remainingCount,
      overflowThumbnailId: overflowThumb,
    };
  }, [stripWidth, thumbnailIds, total]);
  ```

  **Guardrail (from review)**: Always use `Math.max(0, fitCount - 1)` to prevent negative slice indices when sidebar is extremely narrow.

  **Must NOT do**:
  - Do not show only the +X thumbnail when there's overflow
  - Do not hide all thumbnails when width is 0

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Logic fix
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 4
  - **Blocked By**: Task 2

  **Acceptance Criteria**:
  - [ ] With 2 wallpapers and sufficient width, show 2 thumbnails (no +X)
  - [ ] With many wallpapers, show N-1 normal + 1 with +X
  - [ ] No flickering on initial render

- [ ] 4. Right-align Badge, arrow, and menu in PlaylistItem.tsx

  **What to do**:
  - Restructure the layout so Badge, AccordionTrigger (arrow), and DropdownMenu are on the right
  - Use flexbox with `justify-between` or similar
  - The accordion arrow should be minimal (just the chevron)

  **Layout structure**:
  ```tsx
  <div class="flex items-center gap-1 w-full px-2 py-1.5 rounded-md transition-colors
              {isActive ? 'bg-accent text-accent-foreground' : 'hover:bg-accent/50 text-muted-foreground'}">
    {/* Left: Drag handle */}
    <button class="shrink-0 cursor-grab opacity-0 group-hover:opacity-100" {...attributes} {...listeners}>
      <GripVertical class="w-3.5 h-3.5" />
    </button>
    
    {/* Left-Middle: Clickable name (selects playlist) */}
    <button 
      class="flex-1 min-w-0 text-left truncate text-sm"
      onClick={() => setActivePlaylist(playlist.id)}
    >
      {playlist.name}
    </button>
    
    {/* Right: Badge + Arrow + Menu */}
    <div class="flex items-center gap-1 shrink-0">
      <Badge class="text-[10px] px-1.5 h-4">{playlist.wallpaperIds.length}</Badge>
      {/* Empty AccordionTrigger = only chevron */}
      <AccordionTrigger class="p-0.5 hover:bg-accent/50 rounded" />
      <DropdownMenu>...</DropdownMenu>
    </div>
  </div>
  ```

  **Key insight**: The `AccordionTrigger` with no children will only render the chevron icon (auto-appended by Radix UI). This gives us the exact behavior we want: name click → select, chevron click → toggle expand.

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: UI layout
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 5
  - **Blocked By**: Task 3

- [ ] 5. Add remove wallpaper from playlist functionality

  **What to do**:
  - Add a hover-to-reveal remove button on each thumbnail in the expanded content
  - Call `removeFromPlaylist(playlistId, wallpaperId)` on click
  - Show confirmation toast on success

  **Implementation**:
  ```tsx
  // In AccordionContent thumbnail strip:
  {shownIds.map((id) => (
    <div class="relative group/thumbnail w-8 h-8">
      <Thumbnail wallpaperId={id} className="w-8 h-8" />
      <button
        class="absolute top-0 right-0 w-3.5 h-3.5 rounded-full bg-red-500 text-white 
               opacity-0 group-hover/thumbnail:opacity-100 transition-opacity
               flex items-center justify-center text-[10px] font-bold"
        onClick={(e) => {
          e.stopPropagation();
          removeFromPlaylist(playlist.id, id);
        }}
      >
        ×
      </button>
    </div>
  ))}
  ```

  **Guardrail (from review)**: Position the remove button at `top-0 right-0` INSIDE the thumbnail bounds, NOT with negative margins (`-top-1 -right-1`), to prevent clipping by AccordionContent's `overflow-hidden` during animations.

  **Must NOT do**:
  - Do not show remove button on the +X overlay thumbnail
  - Do not require confirmation dialog (just toast)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: UI with interaction
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 6
  - **Blocked By**: Task 4

  **References**:
  - `lwg-gui-tauri/src/store/appStore.ts:1099` - `removeFromPlaylist` method
  - `lwg-gui-tauri/src/components/common/Thumbnail.tsx` - Thumbnail component

  **Acceptance Criteria**:
  - [ ] Hover on thumbnail reveals small X button
  - [ ] Click X removes wallpaper from playlist
  - [ ] Toast shows success/error

- [ ] 6. Verification - Run tests and typecheck

  **What to do**:
  - Run `npx vitest run` to ensure no test failures
  - Run `npx tsc --noEmit` to check for new TypeScript errors in playlist files
  - Manual browser test at port 1420

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Verification
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: None
  - **Blocked By**: Task 5

  **QA Scenarios**:
  ```
  Scenario: All fixes verified
    Tool: Browser dev at port 1420
    Preconditions: Multiple playlists with various wallpaper counts
    Steps:
      1. Expand multiple playlists - verify all stay open
      2. Click playlist name - verify grid filters to that playlist
      3. Click accordion arrow - verify it only toggles expand, doesn't change selection
      4. Check thumbnail strip with 2 wallpapers - verify both show
      5. Check thumbnail strip with 10+ wallpapers - verify N-1 normal + 1 with +X
      6. Hover thumbnail - verify X button appears
      7. Click X - verify wallpaper removed from playlist
    Expected Result: All behaviors match requirements
  ```

---

## Commit Strategy

- **Commit 1**: `fix(playlist): allow multiple accordions to be open simultaneously`
  - Files: `PlaylistList.tsx`
- **Commit 2**: `fix(playlist): separate selection from accordion toggle and fix thumbnail overflow`
  - Files: `PlaylistItem.tsx`

---

## Success Criteria

### Verification Commands
```bash
npx vitest run  # Expected: 3 tests pass
npx tsc --noEmit 2>&1 | grep -i playlist  # Expected: no errors (pre-existing errors in other files OK)
```

### Final Checklist
- [ ] Multiple accordions can be open
- [ ] Playlist name click selects, arrow click toggles
- [ ] Thumbnails show correctly with overflow
- [ ] Remove button on thumbnail hover
- [ ] Right-aligned layout
- [ ] All tests pass