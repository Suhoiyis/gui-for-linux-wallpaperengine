import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme

ComboBox {
    id: root

    property bool hasError: false

    background: Rectangle {
        radius: Theme.radiusMd
        color: root.enabled ? Theme.input : Theme.elevated
        border.width: 1
        border.color: {
            if (!root.enabled) return Theme.border
            if (root.hasError) return Theme.destructive
            if (root.activeFocus) return Theme.ring
            return Theme.border
        }

        Behavior on border.color { ColorAnimation { duration: Theme.animFast } }
    }

    contentItem: Text {
        text: root.displayText
        font.pixelSize: Theme.fontSizeMd
        color: root.enabled ? Theme.fg : Theme.fgSubtle
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
            color: Theme.overlay
            border.width: 1
            border.color: Theme.border
        }
    }

    delegate: ItemDelegate {
        width: root.width
        contentItem: Text {
            text: root.model[index]
            font.pixelSize: Theme.fontSizeMd
            color: highlighted ? Theme.accentFg : Theme.fg
            verticalAlignment: Text.AlignVCenter
        }
        highlighted: root.highlightedIndex === index
        background: Rectangle {
            radius: Theme.radiusSm
            color: highlighted ? Theme.accent : (hovered ? Theme.overlay : "transparent")
        }
    }
}
