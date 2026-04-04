import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

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
        spacing: 16

        // Preview Image
        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            width: 200
            height: 200
            radius: 16
            color: "#1f2335"
            border.width: 2
            border.color: "#2b2f42"
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
                    color: "#374151"
                    visible: previewImage.status === Image.Error || !previewImage.source
                    Text {
                        anchors.centerIn: parent
                        text: "No Preview"
                        color: "#9ca3af"
                        font.pixelSize: 12
                    }
                }
            }
        }

        // Title & ID
        ColumnLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 4

            Label {
                Layout.alignment: Qt.AlignHCenter
                Layout.maximumWidth: 280
                text: root.wallpaper && root.wallpaper.title ? root.wallpaper.title : "Select Wallpaper"
                color: "#c0caf5"
                font.pixelSize: 16
                font.bold: true
                elide: Text.ElideRight
                horizontalAlignment: Text.AlignHCenter
            }

            Rectangle {
                Layout.alignment: Qt.AlignHCenter
                width: idRow.implicitWidth + 16
                height: 24
                radius: 12
                color: "#16161e"
                border.width: 1
                border.color: "#2f344b"

                RowLayout {
                    id: idRow
                    anchors.centerIn: parent
                    spacing: 4

                    Label {
                        text: root.wallpaper && root.wallpaper.id ? root.wallpaper.id : "---"
                        color: "#565f89"
                        font.pixelSize: 10
                    }

                    Label {
                        text: "📋"
                        color: "#565f89"
                        font.pixelSize: 10
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
            spacing: 12

            Button {
                text: "◀"
                width: 32
                height: 32
                onClicked: root.navigate(-1)
            }

            Rectangle {
                width: 80
                height: 32
                radius: 6
                color: "#16161e"
                border.width: 1
                border.color: "#2f344b"

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 4
                    spacing: 2

                    TextField {
                        id: pageInput
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: root.currentIndex.toString()
                        color: "#c0caf5"
                        font.pixelSize: 12
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
                        color: "#565f89"
                        font.pixelSize: 12
                    }
                }
            }

            Button {
                text: "▶"
                width: 32
                height: 32
                onClicked: root.navigate(1)
            }
        }

        // Apply Button
        Button {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 200
            Layout.preferredHeight: 40
            text: "Apply Wallpaper"
            font.bold: true
            onClicked: root.applyRequested()
            background: Rectangle {
                radius: 8
                color: parent.down ? "#3d59a1" : (parent.hovered ? "#7aa2f7" : "#27a1b9")
            }
            contentItem: Text {
                text: parent.text
                font: parent.font
                color: "#1a1b26"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}
