import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

Switch {
    id: root

    property color checkedColor: Theme.brand

    indicator: Rectangle {
        x: root.leftPadding
        y: root.topPadding + root.availableHeight / 2 - 10
        width: 36
        height: 20
        radius: 10
        color: {
            if (!root.enabled) return Theme.overlay
            return root.checked ? root.checkedColor : Theme.border
        }

        Behavior on color { ColorAnimation { duration: Theme.animNormal } }

        Rectangle {
            x: root.checked ? parent.width - 18 : 2
            y: 2
            width: 16
            height: 16
            radius: 8
            color: root.checked ? Theme.brandFg : Theme.fgMuted

            Behavior on x { NumberAnimation { duration: Theme.animNormal; easing.type: Easing.OutCubic } }
            Behavior on color { ColorAnimation { duration: Theme.animNormal } }
        }
    }

    contentItem: Text {
        text: root.text
        font.pixelSize: Theme.fontSizeMd
        color: root.enabled ? Theme.fg : Theme.fgSubtle
        verticalAlignment: Text.AlignVCenter
        leftPadding: root.indicator.width + root.rightPadding
    }
}
