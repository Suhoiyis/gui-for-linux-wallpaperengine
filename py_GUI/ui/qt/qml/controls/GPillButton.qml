import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

Button {
    id: root

    background: Rectangle {
        radius: Theme.radiusPill
        color: root.down ? Theme.applyPressed :
               (root.hovered ? Theme.applyHover : Theme.accent)

        Behavior on color { ColorAnimation { duration: Theme.animNormal } }
    }

    contentItem: Text {
        text: root.text
        font.bold: true
        font.pixelSize: Theme.fontSizeMd
        color: Theme.windowBg
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}