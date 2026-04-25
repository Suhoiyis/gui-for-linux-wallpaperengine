import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

Button {
    id: root

    property int size: Theme.iconButtonMd

    width: size
    height: size

    background: Rectangle {
        radius: Theme.radiusMd
        color: root.hovered ? Theme.cardBorderHover : "transparent"

        Behavior on color { ColorAnimation { duration: Theme.animNormal } }
    }

    contentItem: Text {
        text: root.text
        font.pixelSize: Theme.fontSizeLg
        color: root.highlighted ? Theme.windowBg : Theme.textPrimary
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}