import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme
import "." as Controls

Button {
    id: root

    property string iconName: ""
    property string variant: "default"
    property string tooltip: ""
    property int size: Theme.iconButtonMd

    width: size
    height: size

    hoverEnabled: true

    ToolTip.visible: root.hovered && root.tooltip !== ""
    ToolTip.text: root.tooltip
    ToolTip.delay: 500

    background: Rectangle {
        radius: Theme.radiusMd
        color: {
            if (!root.enabled) return "transparent"
            if (root.variant === "destructive") {
                if (root.down) return Theme.destructive10
                if (root.hovered) return Theme.destructive10
                return Theme.withAlpha(Theme.destructive, 0.15)
            }
            if (root.down) return Theme.overlay
            if (root.hovered) return Theme.elevated
            return "transparent"
        }
        border.width: root.variant === "destructive" && root.hovered ? 1 : 0
        border.color: root.variant === "destructive" ? Theme.destructive : "transparent"

        Behavior on color { ColorAnimation { duration: Theme.animFast } }
        Behavior on scale { NumberAnimation { duration: Theme.animFast; easing.type: Easing.OutCubic } }

        scale: root.down ? 0.93 : 1.0
    }

    contentItem: Controls.GIcon {
        name: root.iconName
        size: Math.round(root.size * 0.5)
        color: {
            if (!root.enabled) return Theme.fgSubtle
            if (root.variant === "destructive") return root.hovered ? Theme.destructive : Theme.fgMuted
            return root.hovered ? Theme.fg : Theme.fgMuted
        }
    }
}
