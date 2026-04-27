import QtQuick
import "../Theme.js" as Theme
import "." as Controls

Column {
    id: root

    property string title: ""
    property bool expanded: false

    spacing: 0

    Rectangle {
        width: root.width
        height: 32
        radius: Theme.radiusSm
        color: titleArea.containsMouse ? Theme.overlay : "transparent"

        MouseArea {
            id: titleArea
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: root.expanded = !root.expanded
        }

        Row {
            anchors.fill: parent
            anchors.leftMargin: Theme.spaceXs
            anchors.rightMargin: Theme.spaceXs
            spacing: Theme.spaceXs

            Controls.GIcon {
                name: root.expanded ? "chevronDown" : "chevronRight"
                size: 14
                color: Theme.fgMuted
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                text: root.title
                font.pixelSize: Theme.fontSizeMd
                font.weight: Theme.fontWeightMedium
                color: Theme.fg
                verticalAlignment: Text.AlignVCenter
            }
        }
    }

    Item {
        width: root.width
        height: root.expanded ? _content.implicitHeight : 0
        clip: true

        Behavior on height { NumberAnimation { duration: Theme.animNormal; easing.type: Easing.OutCubic } }

        default property alias content: _content.children
        Item {
            id: _content
            width: parent.width
            implicitHeight: childrenRect.height
        }
    }
}
