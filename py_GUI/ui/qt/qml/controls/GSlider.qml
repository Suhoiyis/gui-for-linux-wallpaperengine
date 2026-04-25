import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

Slider {
    id: root

    background: Item {
        x: root.leftPadding
        y: root.topPadding + root.availableHeight / 2 - 2
        width: root.availableWidth
        height: 4

        Rectangle {
            width: parent.width
            height: parent.height
            radius: 2
            color: Theme.inputBorder
        }

        Rectangle {
            width: root.visualPosition * parent.width
            height: parent.height
            radius: 2
            color: Theme.accent
        }
    }

    handle: Rectangle {
        x: root.leftPadding + root.visualPosition * root.availableWidth - 8
        y: root.topPadding + root.availableHeight / 2 - 8
        width: 16
        height: 16
        radius: 8
        color: Theme.accent
        border.width: 2
        border.color: Theme.windowBg

        Behavior on x { NumberAnimation { duration: Theme.animNormal } }
    }
}