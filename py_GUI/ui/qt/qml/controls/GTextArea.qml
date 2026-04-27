import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

TextArea {
    id: root

    property bool hasError: false
    property string errorText: ""

    color: root.enabled ? Theme.fg : Theme.fgSubtle
    placeholderTextColor: Theme.fgSubtle
    font.pixelSize: Theme.fontSizeMd
    padding: Theme.spaceSm

    background: Rectangle {
        radius: Theme.radiusMd
        color: root.enabled ? Theme.input : Theme.elevated
        border.width: 1
        border.color: {
            if (!root.enabled) return Theme.border
            if (root.hasError) return Theme.destructive
            if (root.activeFocus) return Theme.ring
            return Theme.border
        }

        Behavior on border.color { ColorAnimation { duration: Theme.animFast } }
    }
}
