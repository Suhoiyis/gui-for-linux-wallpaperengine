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

    implicitWidth: 320
    implicitHeight: 360

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceMd

        // Preview Image - styled like WallpaperCard
        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            width: 200
            height: 200
            radius: Theme.radius2xl
            color: Theme.surface
            border.width: 1
            border.color: Theme.border
            clip: true

            Image {
                id: previewImage
                anchors.fill: parent
                source: root.wallpaper && root.wallpaper.preview ? root.wallpaper.preview : ""
                fillMode: Image.PreserveAspectCrop
                asynchronous: true
                sourceSize.width: 400
                sourceSize.height: 400

                Rectangle {
                    anchors.fill: parent
                    color: Theme.elevated
                    visible: previewImage.status === Image.Error || !previewImage.source

                    Column {
                        anchors.centerIn: parent
                        spacing: Theme.spaceSm

                        Ctrl.GIcon {
                            anchors.horizontalCenter: parent.horizontalCenter
                            name: "image"
                            size: Theme.fontSize2xl
                            color: Theme.fgSubtle
                        }

                        Text {
                            anchors.horizontalCenter: parent.horizontalCenter
                            text: "No Preview"
                            color: Theme.fgSubtle
                            font.pixelSize: Theme.fontSizeSm
                        }
                    }
                }
            }

            // Loading indicator
            BusyIndicator {
                anchors.centerIn: parent
                running: previewImage.status === Image.Loading
                visible: running
            }
        }

        // Title & ID
        ColumnLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: Theme.spaceXs

            Label {
                Layout.alignment: Qt.AlignHCenter
                Layout.maximumWidth: 300
                text: root.wallpaper && root.wallpaper.title ? root.wallpaper.title : "Select Wallpaper"
                color: Theme.fg
                font.pixelSize: Theme.fontSizeLg
                font.bold: true
                elide: Text.ElideRight
                horizontalAlignment: Text.AlignHCenter
                maximumLineCount: 2
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            }

            // ID badge with copy
            Rectangle {
                Layout.alignment: Qt.AlignHCenter
                height: 24
                radius: Theme.radiusPill
                color: Theme.input
                border.width: 1
                border.color: Theme.border

                RowLayout {
                    anchors.centerIn: parent
                    anchors.leftMargin: Theme.spaceSm
                    anchors.rightMargin: Theme.spaceSm
                    spacing: Theme.spaceXs

                    Label {
                        text: root.wallpaper && root.wallpaper.id ? root.wallpaper.id : "---"
                        color: Theme.fgMuted
                        font.pixelSize: Theme.fontSizeXs
                    }

                    Ctrl.GIcon {
                        name: "copy"
                        size: Theme.fontSizeXs
                        color: Theme.fgSubtle
                    }
                }

                implicitWidth: idLayout.implicitWidth + Theme.spaceMd

                RowLayout {
                    id: idLayout
                    visible: false
                    Label {
                        text: root.wallpaper && root.wallpaper.id ? root.wallpaper.id : "---"
                        font.pixelSize: Theme.fontSizeXs
                    }
                    Ctrl.GIcon {
                        name: "copy"
                        size: Theme.fontSizeXs
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.copyIdRequested()
                    onEntered: parent.color = Theme.elevated
                    onExited: parent.color = Theme.input
                }
            }
        }

        // Navigation - rounded buttons like Tauri
        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: Theme.spaceSm

            // Previous button
            Rectangle {
                width: 32
                height: 32
                radius: 16
                color: navLeftMouse.containsMouse ? Theme.elevated : Theme.input
                border.width: 1
                border.color: Theme.border

                Behavior on color { ColorAnimation { duration: Theme.animFast } }

                Ctrl.GIcon {
                    anchors.centerIn: parent
                    name: "chevronRight"
                    size: Theme.fontSizeMd
                    color: Theme.fgMuted
                    rotation: 180
                }

                MouseArea {
                    id: navLeftMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.navigate(-1)
                }
            }

            // Page input
            Rectangle {
                width: 80
                height: 32
                radius: Theme.radiusMd
                color: Theme.input
                border.width: 1
                border.color: Theme.border

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: Theme.spaceXs
                    spacing: 2

                    TextInput {
                        id: pageInput
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: root.currentIndex.toString()
                        color: Theme.fg
                        font.pixelSize: Theme.fontSizeSm
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        selectByMouse: true
                        validator: IntValidator { bottom: 1; top: root.totalCount }

                        onEditingFinished: {
                            var val = parseInt(text)
                            if (!isNaN(val) && val >= 1 && val <= root.totalCount) {
                                root.jumpTo(val - 1)
                            } else {
                                text = root.currentIndex.toString()
                            }
                        }

                        Keys.onReturnPressed: {
                            focus = false
                        }
                    }

                    Label {
                        text: "/ " + root.totalCount
                        color: Theme.fgMuted
                        font.pixelSize: Theme.fontSizeSm
                    }
                }
            }

            // Next button
            Rectangle {
                width: 32
                height: 32
                radius: 16
                color: navRightMouse.containsMouse ? Theme.elevated : Theme.input
                border.width: 1
                border.color: Theme.border

                Behavior on color { ColorAnimation { duration: Theme.animFast } }

                Ctrl.GIcon {
                    anchors.centerIn: parent
                    name: "chevronDown"
                    size: Theme.fontSizeMd
                    color: Theme.fgMuted
                    rotation: -90
                }

                MouseArea {
                    id: navRightMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.navigate(1)
                }
            }
        }
    }
}