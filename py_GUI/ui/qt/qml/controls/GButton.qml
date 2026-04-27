import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme
import "." as Controls

Button {
    id: root

    property string variant: "default"
    property string sizeVariant: "default"
    property string iconName: ""
    property bool loading: false

    readonly property real _h: sizeVariant === "sm" ? 28 :
                               sizeVariant === "lg" ? 40 : 34
    readonly property real _fontSize: sizeVariant === "sm" ? Theme.fontSizeSm :
                                      sizeVariant === "lg" ? Theme.fontSizeLg : Theme.fontSizeMd
    readonly property real _padH: sizeVariant === "sm" ? Theme.spaceSm :
                                  sizeVariant === "lg" ? Theme.spaceLg : Theme.spaceMd

    implicitWidth: Math.max(_h, _contentRow.implicitWidth + _padH * 2)
    implicitHeight: _h

    hoverEnabled: true

    background: Rectangle {
        radius: Theme.radiusMd
        color: {
            if (!root.enabled) return Theme.elevated
            if (root.down) {
                if (root.variant === "destructive") return Theme.destructive
                if (root.variant === "outline" || root.variant === "ghost") return Theme.overlay
                return Theme.brand  // Changed from accent to brand for primary
            }
            if (root.hovered) {
                if (root.variant === "destructive") return Theme.destructive
                if (root.variant === "outline" || root.variant === "ghost") return Theme.overlay
                return Theme.brand  // Changed from accent to brand for primary
            }
            if (root.variant === "destructive") return Theme.destructive
            if (root.variant === "outline" || root.variant === "ghost") return "transparent"
            return Theme.brand  // Changed from accent to brand for primary
        }
        border.width: root.variant === "outline" ? 1 : 0
        border.color: root.variant === "outline" ? Theme.border : "transparent"

        Behavior on color { ColorAnimation { duration: Theme.animFast } }
        Behavior on scale { NumberAnimation { duration: Theme.animFast; easing.type: Easing.OutCubic } }

        scale: root.down ? 0.97 : 1.0
    }

    contentItem: Row {
        id: _contentRow
        spacing: root.iconName ? Theme.spaceXs : 0
        anchors.centerIn: parent

        Controls.GIcon {
            visible: root.iconName !== "" && !root.loading
            name: root.iconName
            size: root._fontSize + 2
            color: root.variant === "default" || root.variant === "destructive" ? Theme.accentFg : Theme.fg
            anchors.verticalCenter: parent.verticalCenter
        }

        BusyIndicator {
            visible: root.loading
            running: root.loading
            width: root._fontSize + 2
            height: width
            anchors.verticalCenter: parent.verticalCenter
        }

        Text {
            text: root.text
            font.pixelSize: root._fontSize
            font.weight: Theme.fontWeightMedium
            color: {
                if (!root.enabled) return Theme.fgSubtle
                if (root.variant === "default" || root.variant === "destructive") return Theme.brandFg
                return Theme.fg
            }
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
}
