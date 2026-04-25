import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Item {
    id: root

    property var wallpaper: ({})
    property int totalCount: 0
    property int currentIndex: 0

    signal navigate(int direction)
    signal jumpTo(int index)
    signal applyRequested()
    signal copyIdRequested()

    implicitWidth: 300
    implicitHeight: 400

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceLg

        // Preview Image
        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            width: 200
            height: 200
            radius: Theme.radius3xl
            color: Theme.cardBg
            border.width: Theme.cardBorderWidth
            border.color: Theme.cardBorder
            clip: true

            Image {
                id: previewImage
                anchors.fill: parent
                source: root.wallpaper && root.wallpaper.preview ? root.wallpaper.preview : ""
                fillMode: Image.PreserveAspectCrop
                asynchronous: true

                sourceSize.width: 320
                sourceSize.height: 320

                BusyIndicator {
                    anchors.centerIn: parent
                    running: previewImage.status === Image.Loading
                }

                Rectangle {
                    anchors.fill: parent
                    color: Theme.errorBg
                    visible: previewImage.status === Image.Error || !previewImage.source
                    Text {
                        anchors.centerIn: parent
                        text: "No Preview"
                        color: Theme.errorText
                        font.pixelSize: Theme.fontSizeMd
                    }
                }
            }
        }

        // Title & ID
        ColumnLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: Theme.spaceXs

            Label {
                Layout.alignment: Qt.AlignHCenter
                Layout.maximumWidth: 280
                text: root.wallpaper && root.wallpaper.title ? root.wallpaper.title : "Select Wallpaper"
                color: Theme.textPrimary
                font.pixelSize: Theme.fontSizeXl
                font.bold: true
                elide: Text.ElideRight
                horizontalAlignment: Text.AlignHCenter
            }

            Rectangle {
                Layout.alignment: Qt.AlignHCenter
                width: idRow.implicitWidth + Theme.spaceLg
                height: Theme.space2xl
                radius: Theme.radiusXl
                color: Theme.inputBg
                border.width: 1
                border.color: Theme.panelBorder

                RowLayout {
                    id: idRow
                    anchors.centerIn: parent
                    spacing: Theme.spaceXs

                    Label {
                        text: root.wallpaper && root.wallpaper.id ? root.wallpaper.id : "---"
                        color: Theme.textSecondary
                        font.pixelSize: Theme.fontSizeXs
                    }

                    Label {
                        text: "📋"
                        color: Theme.textSecondary
                        font.pixelSize: Theme.fontSizeXs
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.copyIdRequested()
                }
            }
        }

        // Navigation
        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: Theme.spaceMd

            Ctrl.GIconButton {
                text: "◀"
                size: Theme.iconButtonSm
                onClicked: root.navigate(-1)
            }

            Rectangle {
                width: 80
                height: Theme.iconButtonSm
                radius: Theme.radiusSm
                color: Theme.inputBg
                border.width: 1
                border.color: Theme.panelBorder

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: Theme.spaceXs
                    spacing: 2

                    Ctrl.GTextField {
                        id: pageInput
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: root.currentIndex.toString()
                        color: Theme.textPrimary
                        font.pixelSize: Theme.fontSizeMd
                        horizontalAlignment: Text.AlignHCenter
                        background: Item {}
                        onEditingFinished: {
                            var val = parseInt(text)
                            if (!isNaN(val) && val >= 1 && val <= root.totalCount) {
                                root.jumpTo(val - 1)
                            } else {
                                text = root.currentIndex.toString()
                            }
                        }
                    }

                    Label {
                        text: "/ " + root.totalCount
                        color: Theme.textSecondary
                        font.pixelSize: Theme.fontSizeMd
                    }
                }
            }

            Ctrl.GIconButton {
                text: "▶"
                size: Theme.iconButtonSm
                onClicked: root.navigate(1)
            }
        }

        // Apply Button
        Ctrl.GPillButton {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: Theme.spaceXl * 10
            Layout.preferredHeight: Theme.navHeight - Theme.spaceXs
            text: "Apply Wallpaper"
            onClicked: root.applyRequested()
        }
    }
}