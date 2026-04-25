import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Dialog {
    id: root

    property string currentVersion: "unknown"
    property string latestVersion: "unknown"
    property string downloadUrl: ""
    property var backend

    modal: true
    title: "Update Available"
    width: 430
    height: 290

    background: Rectangle {
        radius: Theme.radiusXl
        color: Theme.panelBg
        border.width: 1
        border.color: Theme.panelBorder
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceMd

        Frame {
            Layout.fillWidth: true
            ColumnLayout {
                anchors.fill: parent
                spacing: Theme.spaceXs
                Label { text: "Current: v" + root.currentVersion; color: Theme.textSecondary }
                Label { text: "Latest: " + root.latestVersion; color: Theme.accent; font.bold: true }
            }
        }

        Label {
            Layout.fillWidth: true
            text: "A new version is available."
            color: Theme.textBody
            wrapMode: Text.WordWrap
        }

        Item { Layout.fillHeight: true }

        RowLayout {
            Layout.alignment: Qt.AlignRight
            Ctrl.GButton {
                text: "Later"
                onClicked: root.close()
            }
            Ctrl.GPillButton {
                text: "Download"
                onClicked: {
                    if (root.backend && root.downloadUrl.length > 0) {
                        root.backend.openExternalUrl(root.downloadUrl)
                    }
                    root.close()
                }
            }
        }
    }
}