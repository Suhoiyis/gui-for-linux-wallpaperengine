import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Rectangle {
    id: root

    property var backend
    property var wallpaper: ({})
    property bool hasWallpaper: !!(wallpaper && wallpaper.id && String(wallpaper.id).length > 0)
    property string originalTitle: ""

    property bool nicknameDialogOpen: false

    signal applyRequested(string wallpaperId)
    signal favoriteToggled(string wallpaperId)
    signal nicknameEditRequested(string wallpaperId, string nickname)

    color: Theme.sidebarBg
    border.width: 1
    border.color: Theme.panelBorder

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Item {
                width: parent ? parent.width : Theme.sidebarWidth
                implicitHeight: contentColumn.implicitHeight + Theme.spaceXl

                ColumnLayout {
                    id: contentColumn
                    width: parent.width - Theme.space2xl
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: Theme.spaceMd
                    spacing: Theme.spaceSm

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: width
                        radius: Theme.radius2xl
                        color: Theme.cardBg
                        border.width: 1
                        border.color: Theme.panelBorder
                        clip: true

                        Image {
                            anchors.fill: parent
                            source: root.hasWallpaper ? (root.wallpaper.preview || "") : ""
                            fillMode: Image.PreserveAspectCrop
                            asynchronous: true
                        }

                        Rectangle {
                            anchors.fill: parent
                            color: Theme.cardBg
                            visible: !root.hasWallpaper
                            Label {
                                anchors.centerIn: parent
                                text: "Select a wallpaper"
                                color: Theme.textSecondary
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: Theme.spaceXs

                        RowLayout {
                            Layout.fillWidth: true

                            Label {
                                text: root.hasWallpaper ? (root.wallpaper.title || "Unknown") : "None"
                                color: Theme.textPrimary
                                font.pixelSize: Theme.fontSizeXl
                                font.bold: true
                                elide: Text.ElideRight
                                Layout.fillWidth: true
                            }

                            Ctrl.GIconButton {
                                enabled: root.hasWallpaper
                                text: "✎"
                                size: Theme.iconButtonSm
                                onClicked: root.nicknameDialogOpen = true
                            }

                            Ctrl.GIconButton {
                                enabled: root.hasWallpaper
                                text: (root.backend && root.hasWallpaper && root.backend.isFavorite(root.wallpaper.id)) ? "★" : "☆"
                                size: Theme.iconButtonSm
                                onClicked: if (root.hasWallpaper) root.favoriteToggled(root.wallpaper.id)
                            }
                        }

                        Label {
                            visible: root.hasWallpaper && root.originalTitle.length > 0 && root.originalTitle !== (root.wallpaper.title || "")
                            text: root.originalTitle
                            color: Theme.textSecondary
                            font.pixelSize: Theme.fontSizeSm
                            elide: Text.ElideRight
                            Layout.fillWidth: true
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: Theme.spaceXs

                            Rectangle {
                                radius: Theme.radiusMd
                                color: Theme.cardBg
                                border.width: 1
                                border.color: Theme.cardBorder
                                implicitHeight: Theme.space2xl
                                implicitWidth: typeLabel.implicitWidth + Theme.spaceMd

                                Label {
                                    id: typeLabel
                                    anchors.centerIn: parent
                                    text: root.hasWallpaper ? (root.wallpaper.type || "unknown") : "unknown"
                                    color: Theme.typeBlue
                                    font.pixelSize: Theme.fontSizeXs
                                }
                            }

                            Rectangle {
                                radius: Theme.radiusMd
                                color: Theme.favoriteGoldBg
                                border.width: 1
                                border.color: Theme.cardBorder
                                implicitHeight: Theme.space2xl
                                implicitWidth: idLabel.implicitWidth + Theme.spaceMd

                                Label {
                                    id: idLabel
                                    anchors.centerIn: parent
                                    text: root.hasWallpaper ? (root.wallpaper.id || "") : ""
                                    color: Theme.idOrange
                                    font.pixelSize: Theme.fontSizeXs
                                }
                            }

                            Rectangle {
                                radius: Theme.radiusMd
                                color: Theme.cardBg
                                border.width: 1
                                border.color: Theme.cardBorder
                                implicitHeight: Theme.space2xl
                                implicitWidth: sizeLabel.implicitWidth + Theme.spaceMd

                                Label {
                                    id: sizeLabel
                                    anchors.centerIn: parent
                                    text: root.hasWallpaper ? (root.wallpaper.size || "0 MB") : "0 MB"
                                    color: Theme.sizePink
                                    font.pixelSize: Theme.fontSizeXs
                                }
                            }
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: Theme.spaceSm

                            Ctrl.GButton {
                                Layout.fillWidth: true
                                enabled: root.hasWallpaper
                                text: "Copy ID"
                                onClicked: {
                                    if (root.backend) root.backend.copyTextToClipboard(root.wallpaper.id || "")
                                }
                            }

                            Ctrl.GButton {
                                Layout.fillWidth: true
                                enabled: root.hasWallpaper
                                text: "Workshop"
                                onClicked: {
                                    if (root.backend) root.backend.openWorkshopForWallpaper(root.wallpaper.id || "")
                                }
                            }
                        }

                        Label {
                            text: "Description"
                            color: Theme.textSection
                            font.pixelSize: Theme.fontSizeMd
                            font.bold: true
                            Layout.fillWidth: true
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            radius: Theme.radiusMd
                            color: Theme.inputBg
                            border.width: 1
                            border.color: Theme.panelBorder
                            implicitHeight: Math.max(72, descriptionText.implicitHeight + Theme.spaceLg)

                            Label {
                                id: descriptionText
                                anchors.fill: parent
                                anchors.margins: Theme.spaceSm
                                text: root.hasWallpaper
                                    ? ((root.wallpaper.description || "").trim().length > 0
                                       ? root.wallpaper.description
                                       : "No description")
                                    : "No description"
                                color: Theme.textSecondary
                                wrapMode: Text.WordWrap
                                elide: Text.ElideRight
                                maximumLineCount: 6
                                verticalAlignment: Text.AlignTop
                            }
                        }

                        Label {
                            text: "Tags"
                            color: Theme.textSection
                            font.pixelSize: Theme.fontSizeMd
                            font.bold: true
                            Layout.fillWidth: true
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            radius: Theme.radiusMd
                            color: Theme.inputBg
                            border.width: 1
                            border.color: Theme.panelBorder
                            implicitHeight: Math.max(48, tagsText.implicitHeight + Theme.spaceLg)

                            Label {
                                id: tagsText
                                anchors.fill: parent
                                anchors.margins: Theme.spaceSm
                                text: root.hasWallpaper
                                    ? ((root.wallpaper.tags || "").trim().length > 0
                                       ? root.wallpaper.tags
                                       : "No tags")
                                    : "No tags"
                                color: Theme.textSecondary
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
            Layout.preferredHeight: Theme.navHeight + Theme.spaceLg
            color: Theme.inputBg
            border.width: 1
            border.color: Theme.panelBorder

            RowLayout {
                anchors.fill: parent
                anchors.margins: Theme.spaceMd

                Ctrl.GPillButton {
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

        background: Rectangle {
            radius: Theme.radiusXl
            color: Theme.panelBg
            border.width: 1
            border.color: Theme.panelBorder
        }

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
            spacing: Theme.spaceSm
            Ctrl.GTextField {
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