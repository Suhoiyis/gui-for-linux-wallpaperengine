import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root

    property var wallpaper: ({})
    property bool hasWallpaper: wallpaper && wallpaper.id
    property string originalTitle: ""

    property bool nicknameDialogOpen: false

    signal applyRequested(string wallpaperId)
    signal favoriteToggled(string wallpaperId)
    signal nicknameEditRequested(string wallpaperId, string nickname)

    color: "#1b1f2f"
    border.width: 1
    border.color: "#2f344b"

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Item {
                width: parent ? parent.width : 320
                implicitHeight: contentColumn.implicitHeight + 20

                ColumnLayout {
                    id: contentColumn
                    width: parent.width - 24
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 12
                    spacing: 10

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: width
                        radius: 14
                        color: "#24283b"
                        border.width: 1
                        border.color: "#353d57"
                        clip: true

                        Image {
                            anchors.fill: parent
                            source: root.hasWallpaper ? (root.wallpaper.preview || "") : ""
                            fillMode: Image.PreserveAspectCrop
                            asynchronous: true
                        }

                        Rectangle {
                            anchors.fill: parent
                            color: "#24283b"
                            visible: !root.hasWallpaper
                            Label {
                                anchors.centerIn: parent
                                text: "Select a wallpaper"
                                color: "#8a90b8"
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 6

                        RowLayout {
                            Layout.fillWidth: true

                            Label {
                                text: root.hasWallpaper ? (root.wallpaper.title || "Unknown") : "None"
                                color: "#c0caf5"
                                font.pixelSize: 16
                                font.bold: true
                                elide: Text.ElideRight
                                Layout.fillWidth: true
                            }

                            ToolButton {
                                enabled: root.hasWallpaper
                                text: "✎"
                                onClicked: root.nicknameDialogOpen = true
                            }

                            ToolButton {
                                enabled: root.hasWallpaper
                                text: Backend.isFavorite(root.wallpaper.id) ? "★" : "☆"
                                onClicked: root.favoriteToggled(root.wallpaper.id)
                            }
                        }

                        Label {
                            visible: root.hasWallpaper && root.originalTitle.length > 0 && root.originalTitle !== (root.wallpaper.title || "")
                            text: root.originalTitle
                            color: "#8a90b8"
                            font.pixelSize: 11
                            elide: Text.ElideRight
                            Layout.fillWidth: true
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 6

                            Rectangle {
                                radius: 8
                                color: "#33415566"
                                border.width: 1
                                border.color: "#334155"
                                implicitHeight: 24
                                implicitWidth: typeLabel.implicitWidth + 12

                                Label {
                                    id: typeLabel
                                    anchors.centerIn: parent
                                    text: root.hasWallpaper ? (root.wallpaper.type || "unknown") : "unknown"
                                    color: "#93c5fd"
                                    font.pixelSize: 10
                                }
                            }

                            Rectangle {
                                radius: 8
                                color: "#7c2d1266"
                                border.width: 1
                                border.color: "#b45309"
                                implicitHeight: 24
                                implicitWidth: idLabel.implicitWidth + 12

                                Label {
                                    id: idLabel
                                    anchors.centerIn: parent
                                    text: root.hasWallpaper ? (root.wallpaper.id || "") : ""
                                    color: "#f59e0b"
                                    font.pixelSize: 10
                                }
                            }

                            Rectangle {
                                radius: 8
                                color: "#9f123966"
                                border.width: 1
                                border.color: "#be185d"
                                implicitHeight: 24
                                implicitWidth: sizeLabel.implicitWidth + 12

                                Label {
                                    id: sizeLabel
                                    anchors.centerIn: parent
                                    text: root.hasWallpaper ? (root.wallpaper.size || "0 MB") : "0 MB"
                                    color: "#fda4af"
                                    font.pixelSize: 10
                                }
                            }
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 8

                            Button {
                                Layout.fillWidth: true
                                enabled: root.hasWallpaper
                                text: "Copy ID"
                                onClicked: {
                                    Backend.copyTextToClipboard(root.wallpaper.id || "")
                                }
                            }

                            Button {
                                Layout.fillWidth: true
                                enabled: root.hasWallpaper
                                text: "Workshop"
                                onClicked: {
                                    Backend.openWorkshopForWallpaper(root.wallpaper.id || "")
                                }
                            }
                        }

                        Label {
                            text: "Description"
                            color: "#9aa5ce"
                            font.pixelSize: 12
                            font.bold: true
                            Layout.fillWidth: true
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            radius: 8
                            color: "#161926"
                            border.width: 1
                            border.color: "#2f344b"
                            implicitHeight: Math.max(72, descriptionText.implicitHeight + 16)

                            Label {
                                id: descriptionText
                                anchors.fill: parent
                                anchors.margins: 8
                                text: root.hasWallpaper
                                    ? ((root.wallpaper.description || "").trim().length > 0
                                       ? root.wallpaper.description
                                       : "No description")
                                    : "No description"
                                color: "#8a90b8"
                                wrapMode: Text.WordWrap
                                elide: Text.ElideRight
                                maximumLineCount: 6
                                verticalAlignment: Text.AlignTop
                            }
                        }

                        Label {
                            text: "Tags"
                            color: "#9aa5ce"
                            font.pixelSize: 12
                            font.bold: true
                            Layout.fillWidth: true
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            radius: 8
                            color: "#161926"
                            border.width: 1
                            border.color: "#2f344b"
                            implicitHeight: Math.max(48, tagsText.implicitHeight + 16)

                            Label {
                                id: tagsText
                                anchors.fill: parent
                                anchors.margins: 8
                                text: root.hasWallpaper
                                    ? ((root.wallpaper.tags || "").trim().length > 0
                                       ? root.wallpaper.tags
                                       : "No tags")
                                    : "No tags"
                                color: "#8a90b8"
                                wrapMode: Text.WordWrap
                                maximumLineCount: 3
                                elide: Text.ElideRight
                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 66
            color: "#161926"
            border.width: 1
            border.color: "#2f344b"

            RowLayout {
                anchors.fill: parent
                anchors.margins: 12

                Button {
                    Layout.fillWidth: true
                    enabled: root.hasWallpaper
                    text: "Apply Wallpaper"
                    onClicked: root.applyRequested(root.wallpaper.id)
                }
            }
        }
    }

    Dialog {
        id: nicknameDialog
        visible: root.nicknameDialogOpen
        modal: true
        title: "Edit Nickname"
        standardButtons: Dialog.Ok | Dialog.Cancel

        readonly property var okButton: standardButton(Dialog.Ok)

        onOpened: {
            nicknameInput.text = root.hasWallpaper ? (root.wallpaper.title || "") : ""
            nicknameInput.forceActiveFocus()
            nicknameInput.selectAll()
        }

        Component.onCompleted: {
            okButton.enabled = Qt.binding(function() {
                return root.hasWallpaper
            })
        }

        onAccepted: {
            if (root.hasWallpaper) {
                root.nicknameEditRequested(root.wallpaper.id, nicknameInput.text)
            }
            root.nicknameDialogOpen = false
        }

        onRejected: {
            root.nicknameDialogOpen = false
        }

        contentItem: ColumnLayout {
            spacing: 8
            TextField {
                id: nicknameInput
                placeholderText: "Nickname"
                selectByMouse: true
                onAccepted: {
                    if (nicknameDialog.okButton.enabled) nicknameDialog.accept()
                }
            }
        }
    }
}
