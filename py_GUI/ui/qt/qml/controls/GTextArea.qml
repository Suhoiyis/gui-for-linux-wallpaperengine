import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

TextArea {
    id: root

    color: Theme.textPrimary
    placeholderTextColor: Theme.textMuted
    font.pixelSize: Theme.fontSizeMd
    padding: Theme.spaceSm

    background: Rectangle {
        radius: Theme.radiusMd
        color: Theme.inputBg
        border.width: 1
        border.color: root.activeFocus ? Theme.accent : Theme.inputBorder

        Behavior on border.color { ColorAnimation { duration: Theme.animNormal } }
    }
}