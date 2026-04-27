import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

Slider {
    id: root

    property color trackColor: Theme.brand

    background: Item {
        x: root.leftPadding
        y: root.topPadding + root.availableHeight / 2 - 2
        width: root.availableWidth
        height: 4

        Rectangle {
            width: parent.width
            height: parent.height
            radius: 2
            color: Theme.border
        }

        Rectangle {
            width: root.visualPosition * parent.width
            height: parent.height
            radius: 2
            color: root.trackColor
        }
    }

    handle: Rectangle {
        x: root.leftPadding + root.visualPosition * root.availableWidth - 8
        y: root.topPadding + root.availableHeight / 2 - 8
        width: 16
        height: 16
        radius: 8
        color: root.trackColor
        border.width: 2
        border.color: Theme.bg

        Behavior on x { NumberAnimation { duration: Theme.animNormal } }
        Behavior on scale { NumberAnimation { duration: Theme.animFast; easing.type: Easing.OutCubic } }

        scale: root.hovered ? 1.15 : 1.0
    }
}
