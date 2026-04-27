import QtQuick
import "../Theme.js" as Theme

Item {
    id: root

    property Item target: null
    property color ringColor: Theme.brand
    property int ringWidth: Theme.focusRingWidth
    property int ringOffset: Theme.focusRingOffset

    visible: target ? target.activeFocus : false

    anchors.fill: target
    anchors.margins: -ringOffset
    z: target ? target.z - 1 : 0

    Rectangle {
        anchors.fill: parent
        radius: Theme.radiusMd + root.ringOffset
        color: "transparent"
        border.width: root.ringWidth
        border.color: root.ringColor
        visible: root.visible

        Behavior on border.color {
            ColorAnimation { duration: Theme.animFast }
        }
    }
}
