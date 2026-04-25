import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../Theme.js" as Theme

Frame {
    id: root

    property var backend

    background: Rectangle {
        color: Theme.panelBg
        radius: Theme.radiusXl
        border.width: 1
        border.color: Theme.panelBorder
    }
    padding: Theme.spaceMd

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceSm

        Label {
            text: "Wayland Tweaks"
            color: Theme.textSection
            font.pixelSize: Theme.fontSizeMd
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Pause Only When Active"; color: Theme.textPrimary; Layout.preferredWidth: Theme.spaceXl * 9.5 }
            Ctrl.GSwitch {
                checked: root.backend ? root.backend.waylandOnlyActive : false
                onToggled: if (root.backend) root.backend.setWaylandOnlyActive(checked)
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: Theme.spaceXs
            Label {
                text: "Ignore Application IDs"
                color: Theme.textPrimary
            }
            Ctrl.GTextArea {
                id: appidsArea
                Layout.fillWidth: true
                implicitHeight: Theme.space2xl * 3.75
                wrapMode: TextEdit.WordWrap
                text: root.backend ? root.backend.waylandIgnoreAppids : ""
            }
            RowLayout {
                Layout.fillWidth: true
                Item { Layout.fillWidth: true }
                Ctrl.GPillButton {
                    text: "Save"
                    onClicked: if (root.backend) root.backend.setWaylandIgnoreAppids(appidsArea.text)
                }
            }
        }
    }
}