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
    width: 400
    height: 280

    background: Rectangle {
        radius: Theme.radiusXl
        color: Theme.elevated
        border.width: 1
        border.color: Theme.border
    }

    // Custom header
    header: Rectangle {
        height: 60
        color: "transparent"

        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: Theme.spaceLg
            anchors.rightMargin: Theme.spaceLg
            spacing: Theme.spaceSm

            Ctrl.GIcon {
                name: "download"
                size: Theme.fontSizeXl
                color: Theme.brand
            }

            Label {
                text: "Update Available"
                color: Theme.fg
                font.pixelSize: Theme.fontSizeLg
                font.bold: true
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceLg

        // Version info card
        Rectangle {
            Layout.fillWidth: true
            height: 80
            radius: Theme.radiusLg
            color: Theme.surface
            border.width: 1
            border.color: Theme.border

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Theme.spaceMd
                spacing: Theme.spaceXs

                RowLayout {
                    spacing: Theme.spaceSm
                    Label {
                        text: "Current:"
                        color: Theme.fgMuted
                        font.pixelSize: Theme.fontSizeSm
                    }
                    Label {
                        text: "v" + root.currentVersion
                        color: Theme.fg
                        font.pixelSize: Theme.fontSizeSm
                    }
                }

                RowLayout {
                    spacing: Theme.spaceSm
                    Label {
                        text: "Latest:"
                        color: Theme.fgMuted
                        font.pixelSize: Theme.fontSizeSm
                    }
                    Label {
                        text: "v" + root.latestVersion
                        color: Theme.brand
                        font.pixelSize: Theme.fontSizeSm
                        font.bold: true
                    }
                }
            }
        }

        Label {
            Layout.fillWidth: true
            text: "A new version is available. Download the latest release for new features and bug fixes."
            color: Theme.fg
            font.pixelSize: Theme.fontSizeSm
            wrapMode: Text.WordWrap
        }

        Item { Layout.fillHeight: true }

        // Footer buttons
        RowLayout {
            Layout.fillWidth: true
            Item { Layout.fillWidth: true }
            Ctrl.GButton {
                text: "Later"
                variant: "outline"
                onClicked: root.close()
            }
            Ctrl.GButton {
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