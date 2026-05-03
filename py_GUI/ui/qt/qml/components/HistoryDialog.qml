import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Dialog {
    id: root

    property var backend
    property var themeBridge
    property var tb: themeBridge || null
    modal: true
    title: "Play History"
    standardButtons: Dialog.Close
    width: 520
    height: 480

    background: Rectangle {
        radius: Theme.radiusXl
        color: tb ? tb.cElevated : Theme.elevated
        border.width: 0
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
                color: tb ? tb.cFg : Theme.fg
            }

            ColumnLayout {
                Layout.fillWidth: true
                spacing: 0

                Label {
                    text: "Play History"
                    color: tb ? tb.cFg : Theme.fg
                    font.pixelSize: Theme.fontSizeLg
                    font.bold: true
                }

                Label {
                    text: "Recently played wallpapers. Click Reuse to apply again."
                    color: tb ? tb.cFgMuted : Theme.fgMuted
                    font.pixelSize: Theme.fontSizeXs
                }
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceMd

        // History list
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: Theme.radiusLg
            color: tb ? tb.cSurface : Theme.surface
            border.width: 0

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
                    color: index % 2 === 0 ? (tb ? tb.cSurface : Theme.surface) : Theme.withAlpha(tb ? tb.cElevated : Theme.elevated, 0.5)

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
                            color: tb ? tb.cElevated : Theme.elevated

                            Ctrl.GIcon {
                                name: "image"
                                size: Theme.fontSizeMd
                                color: tb ? tb.cFgMuted : Theme.fgMuted
                                anchors.centerIn: parent
                            }
                        }

                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 0

                            Label {
                                text: modelData.title || "Unknown"
                                color: tb ? tb.cFg : Theme.fg
                                font.pixelSize: Theme.fontSizeSm
                                font.weight: Theme.fontWeightMedium
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                            }

                            Label {
                                text: modelData.id || ""
                                color: tb ? tb.cFgMuted : Theme.fgMuted
                                font.pixelSize: Theme.fontSizeXs
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                            }
                        }

                        Ctrl.GButton {
                            themeBridge: root.themeBridge
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
                        color: tb ? tb.cBorder : Theme.border
                    }
                }

                // Empty state
                Label {
                    anchors.centerIn: parent
                    visible: parent.count === 0
                    text: "No playback history yet"
                    color: tb ? tb.cFgMuted : Theme.fgMuted
                    font.pixelSize: Theme.fontSizeMd
                }
            }
        }

        // Footer buttons
        RowLayout {
            Layout.fillWidth: true
            Item { Layout.fillWidth: true }
            Ctrl.GButton {
                themeBridge: root.themeBridge
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