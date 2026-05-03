import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme

ComboBox {
    id: root

    property bool hasError: false
    property var themeBridge: null
    property var tb: themeBridge || null

    background: Rectangle {
        radius: Theme.radiusMd
        color: root.enabled ? (tb ? tb.cInput : Theme.input) : (tb ? tb.cElevated : Theme.elevated)
        border.width: 1
        border.color: {
            if (!root.enabled) return tb ? tb.cBorder : Theme.border
            if (root.hasError) return tb ? tb.cDestructive : Theme.destructive
            if (root.activeFocus) return tb ? tb.cRing : Theme.ring
            return tb ? tb.cBorder : Theme.border
        }

        Behavior on border.color { ColorAnimation { duration: Theme.animFast } }
    }

    contentItem: Text {
        text: root.displayText
        font.pixelSize: Theme.fontSizeMd
        color: root.enabled ? (tb ? tb.cFg : Theme.fg) : (tb ? tb.cFgSubtle : Theme.fgSubtle)
        leftPadding: Theme.spaceSm
        rightPadding: Theme.spaceSm
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    popup: Popup {
        y: root.height
        width: root.width
        implicitHeight: contentItem.implicitHeight + Theme.spaceMd
        padding: Theme.spaceSm

        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: root.popup.visible ? root.delegateModel : null
            currentIndex: root.highlightedIndex

            ScrollIndicator.vertical: ScrollIndicator {}
        }

        background: Rectangle {
            radius: Theme.radiusXl
            color: tb ? tb.cOverlay : Theme.overlay
            border.width: 1
            border.color: tb ? tb.cBorder : Theme.border
        }
    }

    delegate: ItemDelegate {
        width: root.width
        contentItem: Text {
            text: root.model[index]
            font.pixelSize: Theme.fontSizeMd
            color: highlighted ? (tb ? tb.cAccentFg : Theme.accentFg) : (tb ? tb.cFg : Theme.fg)
            verticalAlignment: Text.AlignVCenter
        }
        highlighted: root.highlightedIndex === index
        background: Rectangle {
            radius: Theme.radiusSm
            color: highlighted ? (tb ? tb.cAccent : Theme.accent) : (hovered ? (tb ? tb.cOverlay : Theme.overlay) : "transparent")
        }
    }
}
