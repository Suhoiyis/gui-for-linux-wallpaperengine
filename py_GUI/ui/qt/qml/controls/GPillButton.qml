import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme
import "." as Controls

Button {
    id: root

    property string iconName: ""
    property bool loading: false

    implicitHeight: 34

    hoverEnabled: true

    background: Rectangle {
        radius: Theme.radiusPill
        color: {
            if (!root.enabled) return Theme.elevated
            if (root.down) return Theme.brand50
            if (root.hovered) return Theme.brand
            return Theme.brand
        }

        Behavior on color { ColorAnimation { duration: Theme.animFast } }
        Behavior on scale { NumberAnimation { duration: Theme.animFast; easing.type: Easing.OutCubic } }

        scale: root.down ? 0.97 : (root.hovered ? 1.02 : 1.0)
    }

    contentItem: Row {
        id: _contentRow
        spacing: root.iconName ? Theme.spaceXs : 0
        anchors.centerIn: parent

        Controls.GIcon {
            visible: root.iconName !== "" && !root.loading
            name: root.iconName
            size: Theme.fontSizeLg
            color: Theme.brandFg
            anchors.verticalCenter: parent.verticalCenter
        }

        BusyIndicator {
            visible: root.loading
            running: root.loading
            width: Theme.fontSizeLg
            height: width
            anchors.verticalCenter: parent.verticalCenter
        }

        Text {
            text: root.text
            font.pixelSize: Theme.fontSizeMd
            font.weight: Theme.fontWeightBold
            font.letterSpacing: Theme.trackingWide
            color: root.enabled ? Theme.brandFg : Theme.fgSubtle
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
}
