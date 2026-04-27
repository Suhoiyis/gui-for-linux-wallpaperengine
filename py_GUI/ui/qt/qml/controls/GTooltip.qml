import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

ToolTip {
    id: root

    delay: 500
    timeout: 3000

    contentItem: Text {
        text: root.text
        font.pixelSize: Theme.fontSizeSm
        color: Theme.fg
    }

    background: Rectangle {
        radius: Theme.radiusSm
        color: Theme.overlay
        border.width: 1
        border.color: Theme.border
    }
}
