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

// ── Semantic color system ──
// Layer hierarchy: bg < surface < elevated < overlay

var bg          = "#0f1017"   // deepest — window background
var surface     = "#1a1b26"   // panels, cards default
var elevated    = "#1f2335"   // raised panels, hover cards
var overlay     = "#282a36"   // dropdowns, popovers, tooltips

// Foreground hierarchy
var fg          = "#c0caf5"   // primary text
var fgMuted     = "#8a90b8"   // secondary text
var fgSubtle    = "#565f89"   // disabled / hint text

// Brand identity (matches Tauri --brand: 330 75% 55%)
var brand       = "#d946a0"
var brandFg     = "#ffffff"

// Interactive accent (blue, for focus rings, controls)
var accent      = "#7aa2f7"
var accentFg    = "#0f1017"

// Semantic status
var destructive     = "#f7768e"
var destructiveFg   = "#ffffff"
var success         = "#9ece6a"
var warning         = "#e0af68"

// Border / Input
var border      = "#2f344b"
var borderHover = "#4f5f8f"
var input       = "#16161e"
var ring        = "#7aa2f7"

// ── Opacity variants ──

var brand5          = withAlpha(brand, 0.05)
var brand10         = withAlpha(brand, 0.10)
var brand20         = withAlpha(brand, 0.20)
var brand50         = withAlpha(brand, 0.50)
var surface80       = withAlpha(surface, 0.80)
var overlay95       = withAlpha(overlay, 0.95)
var overlayDim      = withAlpha("#000000", 0.30)
var destructive10   = withAlpha(destructive, 0.10)
var selectionOverlay = withAlpha(accent, 0.20)

// ── Badge / tag semantic colors ──

var typeBlue     = "#93c5fd"
var idOrange     = "#f59e0b"
var sizePink     = "#fda4af"
var favoriteGold = "#e0af68"
var favoriteGoldBg = withAlpha(favoriteGold, 0.25)

// ── Row alternation ──

var rowEven     = "#1f2335"
var rowOdd      = "#1b1f2f"
var rowSelected = "#2c3148"

// ── Shadows ──

var shadowSm      = "0 1px 2px " + withAlpha("#000000", 0.10)
var shadow        = "0 1px 3px " + withAlpha("#000000", 0.12) + ", 0 1px 2px " + withAlpha("#000000", 0.08)
var shadowLg      = "0 4px 6px " + withAlpha("#000000", 0.12) + ", 0 2px 4px " + withAlpha("#000000", 0.08)
var shadowXl      = "0 10px 15px " + withAlpha("#000000", 0.15) + ", 0 4px 6px " + withAlpha("#000000", 0.08)
var shadowBrand20 = "0 8px 24px " + brand20

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

// ── Backward-compat aliases (old token names → new semantic names) ──
// Remove after Phase 3 is complete and all components use new tokens.

var windowBg      = surface
var panelBg       = elevated
var panelBorder   = border
var textPrimary   = fg
var textSecondary = fgMuted
var textMuted     = fgSubtle
var textBody      = "#a9b1d6"
var textSection   = "#9aa5ce"
var statusBarBg   = input
var cardBg        = elevated
var cardBorder    = "#2b2f42"
var cardBorderHover  = borderHover
var cardBorderActive = accent
var cardBorderWidth  = focusRingWidth
var sidebarBg     = "#1b1f2f"
var inputBg       = input
var inputBorder   = border
var divider       = "#292e42"
var errorBg       = "#374151"
var errorText     = "#9ca3af"
var applyNormal   = "#27a1b9"
var applyHover    = accent
var applyPressed  = "#3d59a1"