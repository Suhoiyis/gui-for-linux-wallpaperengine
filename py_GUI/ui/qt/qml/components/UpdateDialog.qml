import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

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

    ColumnLayout {
        anchors.fill: parent
        spacing: 12

        Frame {
            Layout.fillWidth: true
            ColumnLayout {
                anchors.fill: parent
                spacing: 6
                Label { text: "Current: v" + root.currentVersion; color: "#8a90b8" }
                Label { text: "Latest: " + root.latestVersion; color: "#7aa2f7"; font.bold: true }
            }
        }

        Label {
            Layout.fillWidth: true
            text: "A new version is available."
            color: "#a9b1d6"
            wrapMode: Text.WordWrap
        }

        Item { Layout.fillHeight: true }

        RowLayout {
            Layout.alignment: Qt.AlignRight
            Button {
                text: "Later"
                onClicked: root.close()
            }
            Button {
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
