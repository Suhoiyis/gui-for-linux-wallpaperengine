import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Frame {
    id: root

    property var backend

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        Label {
            text: "Wayland Tweaks"
            color: "#9aa5ce"
            font.pixelSize: 12
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Pause Only When Active"; color: "#c0caf5"; Layout.preferredWidth: 190 }
            Switch {
                checked: root.backend ? root.backend.waylandOnlyActive : false
                onToggled: if (root.backend) root.backend.setWaylandOnlyActive(checked)
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 4
            Label {
                text: "Ignore Application IDs"
                color: "#c0caf5"
            }
            TextArea {
                id: appidsArea
                Layout.fillWidth: true
                implicitHeight: 90
                wrapMode: TextEdit.WordWrap
                text: root.backend ? root.backend.waylandIgnoreAppids : ""
            }
            RowLayout {
                Layout.fillWidth: true
                Item { Layout.fillWidth: true }
                Button {
                    text: "Save"
                    onClicked: if (root.backend) root.backend.setWaylandIgnoreAppids(appidsArea.text)
                }
            }
        }
    }
}
