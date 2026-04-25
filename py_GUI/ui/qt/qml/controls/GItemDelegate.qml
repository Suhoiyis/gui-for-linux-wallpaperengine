import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

ItemDelegate {
    id: root

    contentItem: Text {
        text: root.text
        font.pixelSize: Theme.fontSizeMd
        color: root.highlighted ? Theme.windowBg : Theme.textPrimary
        verticalAlignment: Text.AlignVCenter
    }

    background: Rectangle {
        radius: Theme.radiusSm
        color: root.highlighted ? Theme.accent :
               (root.hovered ? Theme.cardBorderHover : "transparent")

        Behavior on color { ColorAnimation { duration: Theme.animNormal } }
    }
}