import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Dialog {
    id: root

    property var backend
    modal: true
    title: "Play History"
    standardButtons: Dialog.Close
    width: 520
    height: 480

    background: Rectangle {
        radius: Theme.radiusXl
        color: Theme.elevated
        border.width: 1
        border.color: Theme.border
    }

    // Custom header with icon
    header: Rectangle {
        height: 60
        color: "transparent"

        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: Theme.spaceLg
            anchors.rightMargin: Theme.spaceLg
            spacing: Theme.spaceSm

            Ctrl.GIcon {
                name: "history"
                size: Theme.fontSizeXl
                color: Theme.fg
            }

            ColumnLayout {
                Layout.fillWidth: true
                spacing: 0

                Label {
                    text: "Play History"
                    color: Theme.fg
                    font.pixelSize: Theme.fontSizeLg
                    font.bold: true
                }

                Label {
                    text: "Recently played wallpapers. Click Reuse to apply again."
                    color: Theme.fgMuted
                    font.pixelSize: Theme.fontSizeXs
                }
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceMd

        // History list with rounded border
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: Theme.radiusLg
            color: Theme.surface
            border.width: 1
            border.color: Theme.border

            ListView {
                anchors.fill: parent
                anchors.margins: 1
                clip: true
                model: root.backend ? root.backend.history : []

                delegate: Rectangle {
                    required property var modelData
                    required property int index
                    width: ListView.view.width
                    height: 64
                    color: index % 2 === 0 ? Theme.surface : Theme.withAlpha(Theme.elevated, 0.5)

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: Theme.spaceMd
                        anchors.rightMargin: Theme.spaceMd
                        spacing: Theme.spaceSm

                        // Icon
                        Rectangle {
                            width: 40
                            height: 40
                            radius: Theme.radiusSm
                            color: Theme.elevated

                            Ctrl.GIcon {
                                name: "image"
                                size: Theme.fontSizeMd
                                color: Theme.fgMuted
                                anchors.centerIn: parent
                            }
                        }

                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 0

                            Label {
                                text: modelData.title || "Unknown"
                                color: Theme.fg
                                font.pixelSize: Theme.fontSizeSm
                                font.weight: Theme.fontWeightMedium
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                            }

                            Label {
                                text: modelData.id || ""
                                color: Theme.fgMuted
                                font.pixelSize: Theme.fontSizeXs
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                            }
                        }

                        Ctrl.GButton {
                            text: "Reuse"
                            sizeVariant: "sm"
                            onClicked: {
                                if (root.backend) {
                                    root.backend.selectWallpaper(modelData.id)
                                    root.backend.applyWallpaper(modelData.id)
                                }
                                root.close()
                            }
                        }
                    }

                    // Divider
                    Rectangle {
                        visible: index < ListView.view.count - 1
                        anchors.bottom: parent.bottom
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.leftMargin: Theme.spaceMd
                        height: 1
                        color: Theme.border
                    }
                }

                // Empty state
                Label {
                    anchors.centerIn: parent
                    visible: parent.count === 0
                    text: "No playback history yet"
                    color: Theme.fgMuted
                    font.pixelSize: Theme.fontSizeMd
                }
            }
        }

        // Footer buttons
        RowLayout {
            Layout.fillWidth: true
            Item { Layout.fillWidth: true }
            Ctrl.GButton {
                text: "Clear History"
                variant: "outline"
                enabled: (root.backend ? root.backend.history.length : 0) > 0
                onClicked: {
                    if (root.backend) root.backend.clearHistory()
                }
            }
        }
    }
}