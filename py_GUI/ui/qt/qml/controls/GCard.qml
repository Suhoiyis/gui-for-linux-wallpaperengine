import QtQuick
import "../Theme.js" as Theme
import "../effects" as Effects

Rectangle {
    id: root

    property bool elevated: false
    property real padding: Theme.spaceMd
    default property alias content: _content.children

    color: Theme.surface
    radius: Theme.radiusLg
    border.width: 1
    border.color: Theme.border

    // Improved shadow with better positioning
    Effects.GDropShadow {
        visible: root.elevated
        shadowWidth: root.width
        shadowHeight: root.height
        radius: root.radius
        color: Theme.withAlpha("#000000", 0.15)
        spread: root.elevated ? 6 : 4
        verticalOffset: root.elevated ? 4 : 2
    }

    // Subtle border glow when elevated
    Rectangle {
        visible: root.elevated
        anchors.fill: parent
        radius: root.radius
        color: "transparent"
        border.width: 1
        border.color: Theme.withAlpha(Theme.brand, 0.1)
    }

    Item {
        id: _content
        anchors.fill: parent
        anchors.margins: root.padding
    }
}
