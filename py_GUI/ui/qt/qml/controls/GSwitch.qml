import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

Switch {
    id: root

    indicator: Rectangle {
        x: root.leftPadding
        y: root.topPadding + root.availableHeight / 2 - 10
        width: 36
        height: 20
        radius: 10
        color: root.checked ? Theme.accent : Theme.inputBorder

        Behavior on color { ColorAnimation { duration: Theme.animNormal } }

        Rectangle {
            x: root.checked ? parent.width - 18 : 2
            y: 2
            width: 16
            height: 16
            radius: 8
            color: root.checked ? Theme.windowBg : Theme.textSecondary
            border.width: 0

            Behavior on x { NumberAnimation { duration: Theme.animNormal; easing.type: Easing.OutCubic } }
            Behavior on color { ColorAnimation { duration: Theme.animNormal } }
        }
    }

    contentItem: Text {
        text: root.text
        font.pixelSize: Theme.fontSizeMd
        color: Theme.textPrimary
        verticalAlignment: Text.AlignVCenter
        leftPadding: root.indicator.width + root.rightPadding
    }
}