import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

Button {
    id: root

    property bool transparentBg: false

    background: Rectangle {
        radius: Theme.radiusMd
        color: root.highlighted ? Theme.accent :
               (root.hovered ? Theme.cardBorderHover :
                (root.transparentBg ? "transparent" : Theme.panelBg))
        border.width: root.transparentBg && !root.highlighted ? 0 : 1
        border.color: root.highlighted ? Theme.accent : Theme.panelBorder

        Behavior on color { ColorAnimation { duration: Theme.animNormal } }
    }

    contentItem: Text {
        text: root.text
        color: root.highlighted ? Theme.windowBg : Theme.textPrimary
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
}