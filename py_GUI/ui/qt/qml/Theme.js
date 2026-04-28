.pragma library

// ── Utility ──

function withAlpha(hexColor, alpha) {
    var hex = hexColor.toString()
    if (hex.length === 9) hex = "#" + hex.slice(3, 9) // strip #AA from #AARRGGBB
    var r = parseInt(hex.slice(1, 3), 16)
    var g = parseInt(hex.slice(3, 5), 16)
    var b = parseInt(hex.slice(5, 7), 16)
    var a = Math.round(alpha * 255)
    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b + a).toString(16).slice(1)
}

// ── Color palettes ──

var dark = {
    bg:          "#0f1017",
    surface:     "#1a1b26",
    elevated:    "#1f2335",
    overlay:     "#282a36",
    fg:          "#c0caf5",
    fgMuted:     "#8a90b8",
    fgSubtle:    "#565f89",
    brand:       "#d946a0",
    brandFg:     "#ffffff",
    accent:      "#7aa2f7",
    accentFg:    "#0f1017",
    destructive: "#f7768e",
    destructiveFg: "#ffffff",
    success:     "#9ece6a",
    warning:     "#e0af68",
    border:      "#2f344b",
    borderHover: "#4f5f8f",
    input:       "#16161e",
    ring:        "#7aa2f7",
    rowEven:     "#1f2335",
    rowOdd:      "#1b1f2f",
    rowSelected: "#2c3148",
}

var light = {
    bg:          "#f8f9fc",
    surface:     "#f0f1f5",
    elevated:    "#e8eaf0",
    overlay:     "#dde0e8",
    fg:          "#1a1b2e",
    fgMuted:     "#5c6370",
    fgSubtle:    "#9ca3af",
    brand:       "#c9388a",
    brandFg:     "#ffffff",
    accent:      "#3b82f6",
    accentFg:    "#ffffff",
    destructive: "#dc2626",
    destructiveFg: "#ffffff",
    success:     "#16a34a",
    warning:     "#d97706",
    border:      "#d1d5db",
    borderHover: "#9ca3af",
    input:       "#e5e7eb",
    ring:        "#3b82f6",
    rowEven:     "#f0f1f5",
    rowOdd:      "#e8eaf0",
    rowSelected: "#dbeafe",
}

// ── Derived opacity variants (computed from palette) ──

function _derived(palette) {
    return {
        brand5:           withAlpha(palette.brand, 0.05),
        brand10:          withAlpha(palette.brand, 0.10),
        brand20:          withAlpha(palette.brand, 0.20),
        brand50:          withAlpha(palette.brand, 0.50),
        surface80:        withAlpha(palette.surface, 0.80),
        overlay95:        withAlpha(palette.overlay, 0.95),
        overlayDim:       withAlpha("#000000", 0.30),
        destructive10:    withAlpha(palette.destructive, 0.10),
        selectionOverlay: withAlpha(palette.accent, 0.20),
    }
}

// ── Badge / tag semantic colors (shared across themes) ──

var typeBlue     = "#93c5fd"
var idOrange     = "#f59e0b"
var sizePink     = "#fda4af"
var favoriteGold = "#e0af68"
var favoriteGoldBg_light = withAlpha(favoriteGold, 0.20)
var favoriteGoldBg_dark  = withAlpha(favoriteGold, 0.25)

// ── Shadows ──

var shadowSm_dark  = "0 1px 2px " + withAlpha("#000000", 0.10)
var shadow_dark    = "0 1px 3px " + withAlpha("#000000", 0.12) + ", 0 1px 2px " + withAlpha("#000000", 0.08)
var shadowLg_dark  = "0 4px 6px " + withAlpha("#000000", 0.12) + ", 0 2px 4px " + withAlpha("#000000", 0.08)
var shadowXl_dark  = "0 10px 15px " + withAlpha("#000000", 0.15) + ", 0 4px 6px " + withAlpha("#000000", 0.08)
var shadowBrand20_dark = "0 8px 24px " + withAlpha(dark.brand, 0.20)

var shadowSm_light  = "0 1px 2px " + withAlpha("#000000", 0.04)
var shadow_light    = "0 1px 3px " + withAlpha("#000000", 0.06) + ", 0 1px 2px " + withAlpha("#000000", 0.03)
var shadowLg_light  = "0 4px 6px " + withAlpha("#000000", 0.06) + ", 0 2px 4px " + withAlpha("#000000", 0.03)
var shadowXl_light  = "0 10px 15px " + withAlpha("#000000", 0.08) + ", 0 4px 6px " + withAlpha("#000000", 0.03)
var shadowBrand20_light = "0 8px 24px " + withAlpha(light.brand, 0.15)

// ── Resolve palette by mode ──

function resolvePalette(mode) {
    var palette = mode === "light" ? light : dark
    var derived = _derived(palette)
    var shadows = mode === "light"
        ? { shadowSm: shadowSm_light, shadow: shadow_light, shadowLg: shadowLg_light, shadowXl: shadowXl_light, shadowBrand20: shadowBrand20_light }
        : { shadowSm: shadowSm_dark, shadow: shadow_dark, shadowLg: shadowLg_dark, shadowXl: shadowXl_dark, shadowBrand20: shadowBrand20_dark }
    var badges = mode === "light"
        ? { typeBlue: typeBlue, idOrange: idOrange, sizePink: sizePink, favoriteGold: favoriteGold, favoriteGoldBg: favoriteGoldBg_light }
        : { typeBlue: typeBlue, idOrange: idOrange, sizePink: sizePink, favoriteGold: favoriteGold, favoriteGoldBg: favoriteGoldBg_dark }

    // Merge base + derived + shadows + badges
    var result = {}
    for (var k in palette) result[k] = palette[k]
    for (var k in derived) result[k] = derived[k]
    for (var k in shadows) result[k] = shadows[k]
    for (var k in badges) result[k] = badges[k]

    // Backward-compat aliases
    result.windowBg      = palette.surface
    result.panelBg       = palette.elevated
    result.panelBorder   = palette.border
    result.textPrimary   = palette.fg
    result.textSecondary = palette.fgMuted
    result.textMuted     = palette.fgSubtle
    result.textBody      = mode === "light" ? "#4b5563" : "#a9b1d6"
    result.textSection   = mode === "light" ? "#6b7280" : "#9aa5ce"
    result.statusBarBg   = palette.input
    result.cardBg        = palette.elevated
    result.cardBorder    = mode === "light" ? "#d1d5db" : "#2b2f42"
    result.cardBorderHover  = palette.borderHover
    result.cardBorderActive = palette.accent
    result.cardBorderWidth  = focusRingWidth
    result.sidebarBg     = mode === "light" ? "#eef0f6" : "#1b1f2f"
    result.inputBg       = palette.input
    result.inputBorder   = palette.border
    result.divider       = mode === "light" ? "#e5e7eb" : "#292e42"
    result.errorBg       = mode === "light" ? "#fef2f2" : "#374151"
    result.errorText     = mode === "light" ? "#dc2626" : "#9ca3af"
    result.applyNormal   = mode === "light" ? "#0e7490" : "#27a1b9"
    result.applyHover    = palette.accent
    result.applyPressed  = mode === "light" ? "#1d4ed8" : "#3d59a1"

    return result
}

// ── Typography ──

var fontSizeXs    = 10
var fontSizeSm    = 11
var fontSizeMd    = 12
var fontSizeLg    = 14
var fontSizeXl    = 16
var fontSize2xl   = 18
var fontSize3xl   = 20

// Font weight constants (QML Font enum values)
var fontWeightLight  = 25   // Font.Light
var fontWeightNormal = 50   // Font.Normal
var fontWeightMedium = 75   // Font.Medium
var fontWeightBold   = 100  // Font.Bold

// Letter spacing (fraction of em)
var trackingNormal = 0
var trackingWide   = 0.02
var trackingWider  = 0.05

// Line height multipliers
var lineHeightTight   = 1.25
var lineHeightNormal  = 1.5
var lineHeightRelaxed = 1.75

// ── Spacing tokens (4px base grid) ──

var spaceXs   = 4
var spaceSm   = 8
var spaceMd   = 12
var spaceLg   = 16
var spaceXl   = 20
var space2xl  = 24

// ── Sizing tokens ──

var navHeight         = 50
var navButtonSize     = 36
var iconButtonSm      = 28
var iconButtonMd      = 34
var sidebarWidth      = 360
var sidebarPreviewSize = 280

// ── Radius tokens ──

var radiusSm    = 6
var radiusMd    = 8
var radiusLg    = 10
var radiusXl    = 12
var radius2xl   = 14
var radius3xl   = 16
var radiusPill  = 25

// ── Focus ring ──

var focusRingWidth  = 2
var focusRingOffset = 4

// ── Animation tokens (ms) ──

var animFast   = 120
var animNormal = 180
var animSlow   = 420
var animToast  = 150
var pageTransitionMs = 250

// ── Responsive breakpoints ──

var breakpointCompact = 800
var breakpointNormal  = 1100
var breakpointWide    = 1400

// ── Timers (ms) ──

var playlistHoverOpen = 400
var playlistAutoClose = 300
var toastDuration     = 3000

// ── Legacy: direct dark-mode values for backward compat during migration ──
// Components that haven't been migrated yet still read Theme.bg etc. directly.
// These are the dark-mode defaults and will be removed once all components
// use ThemeBridge colors.

var bg          = dark.bg
var surface     = dark.surface
var elevated    = dark.elevated
var overlay     = dark.overlay
var fg          = dark.fg
var fgMuted     = dark.fgMuted
var fgSubtle    = dark.fgSubtle
var brand       = dark.brand
var brandFg     = dark.brandFg
var accent      = dark.accent
var accentFg    = dark.accentFg
var destructive     = dark.destructive
var destructiveFg   = dark.destructiveFg
var success         = dark.success
var warning         = dark.warning
var border      = dark.border
var borderHover = dark.borderHover
var input       = dark.input
var ring        = dark.ring

var brand5          = withAlpha(dark.brand, 0.05)
var brand10         = withAlpha(dark.brand, 0.10)
var brand20         = withAlpha(dark.brand, 0.20)
var brand50         = withAlpha(dark.brand, 0.50)
var surface80       = withAlpha(dark.surface, 0.80)
var overlay95       = withAlpha(dark.overlay, 0.95)
var overlayDim      = withAlpha("#000000", 0.30)
var destructive10   = withAlpha(dark.destructive, 0.10)
var selectionOverlay = withAlpha(dark.accent, 0.20)

var favoriteGoldBg = favoriteGoldBg_dark

var rowEven     = dark.rowEven
var rowOdd      = dark.rowOdd
var rowSelected = dark.rowSelected

var shadowSm      = shadowSm_dark
var shadow        = shadow_dark
var shadowLg      = shadowLg_dark
var shadowXl      = shadowXl_dark
var shadowBrand20 = shadowBrand20_dark

// Backward-compat aliases (old token names → new semantic names)
// Remove after Phase 3 is complete and all components use new tokens.

var windowBg      = dark.surface
var panelBg       = dark.elevated
var panelBorder   = dark.border
var textPrimary   = dark.fg
var textSecondary = dark.fgMuted
var textMuted     = dark.fgSubtle
var textBody      = "#a9b1d6"
var textSection   = "#9aa5ce"
var statusBarBg   = dark.input
var cardBg        = dark.elevated
var cardBorder    = "#2b2f42"
var cardBorderHover  = dark.borderHover
var cardBorderActive = dark.accent
var cardBorderWidth  = focusRingWidth
var sidebarBg     = "#1b1f2f"
var inputBg       = dark.input
var inputBorder   = dark.border
var divider       = "#292e42"
var errorBg       = "#374151"
var errorText     = "#9ca3af"
var applyNormal   = "#27a1b9"
var applyHover    = dark.accent
var applyPressed  = "#3d59a1"