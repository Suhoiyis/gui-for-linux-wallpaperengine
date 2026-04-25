import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme

ComboBox {
    id: root

    background: Rectangle {
        radius: Theme.radiusMd
        color: Theme.inputBg
        border.width: 1
        border.color: root.activeFocus ? Theme.accent : Theme.inputBorder

        Behavior on border.color { ColorAnimation { duration: Theme.animNormal } }
    }

    contentItem: Text {
        text: root.displayText
        font.pixelSize: Theme.fontSizeMd
        color: Theme.textPrimary
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
            color: Theme.panelBg
            border.width: 1
            border.color: Theme.panelBorder
        }
    }

    delegate: ItemDelegate {
        width: root.width
        contentItem: Text {
            text: root.model[index]
            font.pixelSize: Theme.fontSizeMd
            color: highlighted ? Theme.windowBg : Theme.textPrimary
            verticalAlignment: Text.AlignVCenter
        }
        highlighted: root.highlightedIndex === index
        background: Rectangle {
            radius: Theme.radiusSm
            color: highlighted ? Theme.accent : (hovered ? Theme.cardBorderHover : "transparent")
        }
    }
}