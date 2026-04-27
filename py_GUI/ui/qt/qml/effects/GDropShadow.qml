import QtQuick
import "../Theme.js" as Theme

// Drop shadow using layered semi-transparent rectangles.
// No Qt5Compat dependency — works with core Qt Quick only.
// Apply by placing this as a sibling BEFORE the target item in the layout,
// or use the convenience GShadowFrame wrapper.
Item {
    id: root

    // Shadow appearance
    property real radius: 8
    property color color: Theme.withAlpha("#000000", 0.15)
    property real horizontalOffset: 0
    property real verticalOffset: 2
    property real spread: 2

    // Target dimensions — bind to the shadowed item
    property real shadowWidth: 0
    property real shadowHeight: 0

    x: horizontalOffset - spread
    y: verticalOffset - spread
    width: shadowWidth + spread * 2
    height: shadowHeight + spread * 2

    // Three shadow layers for soft-edge appearance
    Rectangle {
        anchors.fill: parent
        anchors.margins: root.spread * 2
        radius: root.radius + root.spread * 2
        color: Theme.withAlpha(root.color, 0.03)
    }
    Rectangle {
        anchors.fill: parent
        anchors.margins: root.spread
        radius: root.radius + root.spread
        color: Theme.withAlpha(root.color, 0.06)
    }
    Rectangle {
        anchors.fill: parent
        radius: root.radius
        color: root.color
    }
}
