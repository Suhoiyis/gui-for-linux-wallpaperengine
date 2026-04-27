import QtQuick
import "../Theme.js" as Theme

Rectangle {
    id: root

    property real blurRadius: 16
    property color tintColor: Theme.surface
    property real tintOpacity: 0.80

    color: Theme.withAlpha(root.tintColor, tintOpacity)
    radius: Theme.radiusMd
}
