// ThemeBridge.qml — Dynamic color proxy that resolves Theme.js palette based on mode
import QtQuick
import "../Theme.js" as Theme

QtObject {
    id: bridge

    // Mode: "dark", "light", or "system"
    property string mode: "dark"

    // Resolved effective mode (system → dark or light based on OS preference)
    property string resolvedMode: {
        if (mode === "system") {
            // Qt 6.5+ provides Application.styleHints.colorScheme
            var scheme = Application.styleHints ? Application.styleHints.colorScheme : 0
            // ColorScheme.Dark = 2, ColorScheme.Light = 1, ColorScheme.Unknown = 0
            if (scheme === 1) return "light"
            return "dark" // default dark for unknown/system-dark
        }
        return mode
    }

    // Resolved color palette (re-evaluated when resolvedMode changes)
    readonly property var colors: Theme.resolvePalette(resolvedMode)

    // Convenience: expose individual color properties for QML binding
    // (QML can't bind to var object properties reliably, so we flatten)
    readonly property color cBg:              colors.bg
    readonly property color cSurface:         colors.surface
    readonly property color cElevated:        colors.elevated
    readonly property color cOverlay:         colors.overlay
    readonly property color cFg:              colors.fg
    readonly property color cFgMuted:         colors.fgMuted
    readonly property color cFgSubtle:        colors.fgSubtle
    readonly property color cBrand:           colors.brand
    readonly property color cBrandFg:         colors.brandFg
    readonly property color cAccent:          colors.accent
    readonly property color cAccentFg:        colors.accentFg
    readonly property color cDestructive:     colors.destructive
    readonly property color cDestructiveFg:   colors.destructiveFg
    readonly property color cSuccess:         colors.success
    readonly property color cWarning:         colors.warning
    readonly property color cBorder:          colors.border
    readonly property color cBorderHover:     colors.borderHover
    readonly property color cInput:           colors.input
    readonly property color cRing:            colors.ring
    readonly property color cRowEven:         colors.rowEven
    readonly property color cRowOdd:          colors.rowOdd
    readonly property color cRowSelected:     colors.rowSelected
    readonly property color cBrand5:          colors.brand5
    readonly property color cBrand10:         colors.brand10
    readonly property color cBrand20:         colors.brand20
    readonly property color cBrand50:         colors.brand50
    readonly property color cSurface80:       colors.surface80
    readonly property color cOverlay95:       colors.overlay95
    readonly property color cOverlayDim:      colors.overlayDim
    readonly property color cDestructive10:   colors.destructive10
    readonly property color cSelectionOverlay: colors.selectionOverlay
    readonly property string cShadowSm:       colors.shadowSm
    readonly property string cShadow:         colors.shadow
    readonly property string cShadowLg:       colors.shadowLg
    readonly property string cShadowXl:       colors.shadowXl
    readonly property string cShadowBrand20:  colors.shadowBrand20

    // Backward-compat aliases
    readonly property color cWindowBg:      colors.windowBg
    readonly property color cPanelBg:       colors.panelBg
    readonly property color cPanelBorder:   colors.panelBorder
    readonly property color cTextPrimary:   colors.textPrimary
    readonly property color cTextSecondary: colors.textSecondary
    readonly property color cTextMuted:     colors.textMuted
    readonly property color cTextBody:      colors.textBody
    readonly property color cTextSection:   colors.textSection
    readonly property color cStatusBarBg:   colors.statusBarBg
    readonly property color cCardBg:        colors.cardBg
    readonly property color cCardBorder:    colors.cardBorder
    readonly property color cCardBorderHover:  colors.cardBorderHover
    readonly property color cCardBorderActive: colors.cardBorderActive
    readonly property int   cCardBorderWidth:  Theme.focusRingWidth
    readonly property color cSidebarBg:     colors.sidebarBg
    readonly property color cInputBg:       colors.inputBg
    readonly property color cInputBorder:   colors.inputBorder
    readonly property color cDivider:       colors.divider
    readonly property color cErrorBg:       colors.errorBg
    readonly property color cErrorText:     colors.errorText
    readonly property color cApplyNormal:   colors.applyNormal
    readonly property color cApplyHover:    colors.applyHover
    readonly property color cApplyPressed:  colors.applyPressed
    readonly property color cFavoriteGoldBg: colors.favoriteGoldBg

    // Alpha-based tokens for no-border visual hierarchy
    readonly property color cDividerAlpha:    colors.dividerAlpha
    readonly property color cNavBgAlpha:      colors.navBgAlpha
    readonly property color cSidebarBgAlpha:  colors.sidebarBgAlpha
    readonly property color cCardHoverBorder: colors.cardHoverBorder
    readonly property color cBorderSubtle:    colors.borderSubtle

    // Badge colors (shared across themes)
    readonly property color cTypeBlue:      Theme.typeBlue
    readonly property color cIdOrange:      Theme.idOrange
    readonly property color cSizePink:      Theme.sizePink
    readonly property color cFavoriteGold:  Theme.favoriteGold
}