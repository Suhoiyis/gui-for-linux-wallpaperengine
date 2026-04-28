import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../effects" as Effects
import "../Theme.js" as Theme

Rectangle {
    id: root

    property var backend
    property var wallpaper: ({})
    property bool hasWallpaper: !!(wallpaper && wallpaper.id && String(wallpaper.id).length > 0)
    property string originalTitle: ""

    property bool nicknameDialogOpen: false
    property bool descriptionExpanded: false

    function stripBBCode(text) {
        if (!text) return ""
        var out = text
        out = out.replace(/\[url=([^\]]*)\]([^\[]*)\[\/url\]/gi, "$2 ($1)")
        out = out.replace(/\[url\]([^\[]*)\[\/url\]/gi, "$1")
        out = out.replace(/\[b\]([^]*?)\[\/b\]/gi, "$1")
        out = out.replace(/\[i\]([^]*?)\[\/i\]/gi, "$1")
        out = out.replace(/\[u\]([^]*?)\[\/u\]/gi, "$1")
        out = out.replace(/\[s\]([^]*?)\[\/s\]/gi, "$1")
        out = out.replace(/\[h[1-6]\]([^]*?)\[\/h[1-6]\]/gi, "$1")
        out = out.replace(/\[color=[^\]]*\]([^]*?)\[\/color\]/gi, "$1")
        out = out.replace(/\[size=[^\]]*\]([^]*?)\[\/size\]/gi, "$1")
        out = out.replace(/\[img\][^\[]*\[\/img\]/gi, "")
        out = out.replace(/\[\/?(?:b|i|u|s|url|img|h[1-6]|color|size|list|li|code|quote|spoiler|table|tr|td|hr)[^\]]*\]/gi, "")
        out = out.replace(/\n{3,}/g, "\n\n")
        return out.trim()
    }

    signal applyRequested(string wallpaperId)
    signal favoriteToggled(string wallpaperId)
    signal nicknameEditRequested(string wallpaperId, string nickname)

    color: Theme.surface
    border.width: 1
    border.color: Theme.border

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true

            Item {
                width: parent ? parent.width : Theme.sidebarWidth
                implicitHeight: contentColumn.implicitHeight + Theme.spaceXl

                ColumnLayout {
                    id: contentColumn
                    width: parent.width - Theme.spaceLg * 2
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: Theme.spaceLg
                    spacing: Theme.spaceMd

                    // Preview image - styled like WallpaperCard
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: width
                        radius: Theme.radius2xl
                        color: Theme.surface
                        border.width: 1
                        border.color: Theme.border
                        clip: true

                        Image {
                            anchors.fill: parent
                            source: root.hasWallpaper ? (root.wallpaper.preview || "") : ""
                            fillMode: Image.PreserveAspectCrop
                            asynchronous: true
                        }

                        // Empty state with dashed border
                        Rectangle {
                            anchors.fill: parent
                            color: Theme.elevated
                            visible: !root.hasWallpaper
                            border.width: 2
                            border.color: Theme.border

                            Column {
                                anchors.centerIn: parent
                                spacing: Theme.spaceSm

                                Rectangle {
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    width: 64
                                    height: 64
                                    radius: Theme.radiusLg
                                    color: "transparent"
                                    border.width: 2
                                    border.color: Theme.fgSubtle
                                }

                                Text {
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    text: "Select a wallpaper to view details"
                                    color: Theme.fgSubtle
                                    font.pixelSize: Theme.fontSizeSm
                                }
                            }
                        }
                    }

                    // Title + action buttons row
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: Theme.spaceXs

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: Theme.spaceXs

                            Text {
                                text: root.hasWallpaper ? (root.wallpaper.title || "Unknown") : "None"
                                color: Theme.fg
                                font.pixelSize: Theme.fontSizeLg
                                font.bold: true
                                elide: Text.ElideRight
                                Layout.fillWidth: true
                                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                                maximumLineCount: 2
                            }

                            Ctrl.GIconButton {
                                enabled: root.hasWallpaper
                                iconName: "edit3"
                                size: 24
                                tooltip: "Edit Nickname"
                                onClicked: root.nicknameDialogOpen = true
                            }

                            Ctrl.GIconButton {
                                enabled: root.hasWallpaper
                                iconName: "star"
                                size: 24
                                tooltip: "Toggle Favorite"
                                onClicked: if (root.hasWallpaper) root.favoriteToggled(root.wallpaper.id)
                            }
                        }

                        // Original title (if nickname differs)
                        Text {
                            visible: root.hasWallpaper && root.originalTitle.length > 0 && root.originalTitle !== (root.wallpaper.title || "")
                            text: root.originalTitle
                            color: Theme.fgSubtle
                            font.pixelSize: Theme.fontSizeSm
                            elide: Text.ElideRight
                            Layout.fillWidth: true
                        }

                        // Badges row - styled like Tauri (slate/amber/rose/sky)
                        Flow {
                            Layout.fillWidth: true
                            spacing: Theme.spaceXs

                            Rectangle {
                                height: 20
                                radius: Theme.radiusSm
                                color: Theme.withAlpha("#64748b", 0.2)
                                border.width: 1
                                border.color: Theme.withAlpha("#64748b", 0.3)

                                Text {
                                    anchors.centerIn: parent
                                    anchors.leftMargin: Theme.spaceSm
                                    anchors.rightMargin: Theme.spaceSm
                                    text: root.hasWallpaper ? (root.wallpaper.type || "unknown") : "unknown"
                                    color: "#94a3b8"
                                    font.pixelSize: Theme.fontSizeXs
                                }

                                implicitWidth: typeText.implicitWidth + Theme.spaceSm * 2
                                Text {
                                    id: typeText
                                    visible: false
                                    text: parent.children[0].text
                                    font.pixelSize: Theme.fontSizeXs
                                }
                            }

                            Rectangle {
                                height: 20
                                radius: Theme.radiusSm
                                color: Theme.withAlpha(Theme.favoriteGold, 0.2)
                                border.width: 1
                                border.color: Theme.withAlpha(Theme.favoriteGold, 0.3)

                                Text {
                                    anchors.centerIn: parent
                                    anchors.leftMargin: Theme.spaceSm
                                    anchors.rightMargin: Theme.spaceSm
                                    text: root.hasWallpaper ? (root.wallpaper.id || "") : ""
                                    color: Theme.favoriteGold
                                    font.pixelSize: Theme.fontSizeXs
                                    font.family: "monospace"
                                }

                                implicitWidth: idText.implicitWidth + Theme.spaceSm * 2
                                Text {
                                    id: idText
                                    visible: false
                                    text: parent.children[0].text
                                    font.pixelSize: Theme.fontSizeXs
                                    font.family: "monospace"
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: {
                                        if (root.backend && root.hasWallpaper) {
                                            root.backend.copyTextToClipboard(root.wallpaper.id || "")
                                        }
                                    }
                                }
                            }

                            Rectangle {
                                height: 20
                                radius: Theme.radiusSm
                                color: Theme.withAlpha(Theme.destructive, 0.2)
                                border.width: 1
                                border.color: Theme.withAlpha(Theme.destructive, 0.3)

                                Text {
                                    anchors.centerIn: parent
                                    anchors.leftMargin: Theme.spaceSm
                                    anchors.rightMargin: Theme.spaceSm
                                    text: root.hasWallpaper ? (root.wallpaper.size || "0 MB") : "0 MB"
                                    color: Theme.destructive
                                    font.pixelSize: Theme.fontSizeXs
                                }

                                implicitWidth: sizeText.implicitWidth + Theme.spaceSm * 2
                                Text {
                                    id: sizeText
                                    visible: false
                                    text: parent.children[0].text
                                    font.pixelSize: Theme.fontSizeXs
                                }
                            }
                        }

                        // Tags section
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: Theme.spaceXs
                            visible: root.hasWallpaper && (root.wallpaper.tags || "").length > 0

                            Text {
                                text: "Tags"
                                color: Theme.fgMuted
                                font.pixelSize: Theme.fontSizeXs
                                font.bold: true
                                font.letterSpacing: Theme.trackingWide
                            }

                            Flow {
                                Layout.fillWidth: true
                                spacing: Theme.spaceXs

                                Repeater {
                                    model: {
                                        if (!root.hasWallpaper) return []
                                        var tags = (root.wallpaper.tags || "").split(",").filter(function(t) { return t.trim().length > 0 })
                                        return tags.slice(0, 8)
                                    }
                                    delegate: Rectangle {
                                        required property var modelData
                                        height: 20
                                        radius: Theme.radiusSm
                                        color: "transparent"
                                        border.width: 1
                                        border.color: Theme.border

                                        Text {
                                            anchors.centerIn: parent
                                            anchors.leftMargin: Theme.spaceSm
                                            anchors.rightMargin: Theme.spaceSm
                                            text: modelData.trim()
                                            color: Theme.fgMuted
                                            font.pixelSize: Theme.fontSizeXs
                                        }

                                        implicitWidth: tagText.implicitWidth + Theme.spaceSm * 2
                                        Text {
                                            id: tagText
                                            visible: false
                                            text: modelData.trim()
                                            font.pixelSize: Theme.fontSizeXs
                                        }
                                    }
                                }
                            }
                        }

                        // Description accordion
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: Theme.spaceXs
                            visible: root.hasWallpaper && root.stripBBCode(root.wallpaper.description || "").length > 0

                            Rectangle {
                                Layout.fillWidth: true
                                height: 32
                                color: "transparent"

                                RowLayout {
                                    anchors.fill: parent
                                    spacing: Theme.spaceSm

                                    Text {
                                        text: "Description"
                                        color: Theme.fgMuted
                                        font.pixelSize: Theme.fontSizeXs
                                        font.bold: true
                                        font.letterSpacing: Theme.trackingWide
                                        Layout.fillWidth: true
                                    }

                                    Ctrl.GIcon {
                                        name: root.descriptionExpanded ? "chevronDown" : "chevronRight"
                                        size: Theme.fontSizeMd
                                        color: Theme.fgMuted
                                    }
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: root.descriptionExpanded = !root.descriptionExpanded
                                }
                            }

                            Rectangle {
                                Layout.fillWidth: true
                                visible: root.descriptionExpanded
                                color: "transparent"
                                implicitHeight: descText.implicitHeight + Theme.spaceSm

                                Text {
                                    id: descText
                                    anchors.fill: parent
                                    anchors.margins: Theme.spaceSm
                                    text: root.hasWallpaper ? root.stripBBCode(root.wallpaper.description || "") : "No description"
                                    color: Theme.fgMuted
                                    font.pixelSize: Theme.fontSizeSm
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }
                    }
                }
            }
        }

        // Apply footer
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 64
            color: Theme.withAlpha(Theme.bg, 0.8)
            border.width: 1
            border.color: Theme.border

            RowLayout {
                anchors.fill: parent
                anchors.margins: Theme.spaceMd

                Ctrl.GButton {
                    Layout.fillWidth: true
                    enabled: root.hasWallpaper
                    text: "Apply Wallpaper"
                    iconName: "play"
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
            color: Theme.elevated
            border.width: 1
            border.color: Theme.border
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
