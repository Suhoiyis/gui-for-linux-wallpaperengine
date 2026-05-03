import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../Theme.js" as Theme

Frame {
    id: root

    property var backend
    property var themeBridge
    property var tb: themeBridge || null

    background: Rectangle {
        color: tb ? tb.cElevated : Theme.elevated
        radius: Theme.radiusXl
        border.width: 0
    }
    padding: Theme.spaceMd

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceSm

        Label {
            text: "Wayland Tweaks"
            color: tb ? tb.cTextSection : Theme.textSection
            font.pixelSize: Theme.fontSizeMd
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Pause Only When Active"; color: tb ? tb.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 9.5 }
            Ctrl.GSwitch {
                themeBridge: root.themeBridge
                checked: root.backend ? root.backend.waylandOnlyActive : false
                onToggled: {
                    if (root.backend) root.backend.setWaylandOnlyActive(checked)
                    if (root.backend) root.backend.saveSettings()
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: Theme.spaceXs
            Label {
                text: "Ignore Application IDs"
                color: tb ? tb.cFg : Theme.fg
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