import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Item {
    id: root

    required property var playlistData
    required property string activePlaylistId
    required property var wallpapers
    required property var generateAvatarColor
    required property var getInitialFn
    required property bool isSpecial
    property bool draggable: false

    property bool isActive: !isSpecial && activePlaylistId === playlistData.id
    property bool expanded: isActive
    property var wpIds: isSpecial ? [] : (playlistData.wallpaper_ids || [])
    property int rowH: 36
    readonly property int maxThumbs: 5
    readonly property bool thumbsVisible: expanded && wpIds.length > 0
    readonly property int totalHeight: rowH + (thumbsVisible ? 36 + Theme.spaceXs : 0) + (expanded && wpIds.length === 0 ? 20 : 0)

    signal activePlaylistChanged(string playlistId)

    // Special "All Wallpapers" button
    Rectangle {
        visible: root.isSpecial
        anchors.fill: parent
        radius: Theme.radiusMd
        color: activePlaylistId.length === 0 ? Theme.brand : "transparent"

        Behavior on color { ColorAnimation { duration: Theme.animFast } }

        Text {
            anchors.centerIn: parent
            text: "All Wallpapers"
            color: activePlaylistId.length === 0 ? Theme.brandFg : Theme.fgMuted
            font.pixelSize: Theme.fontSizeSm
            font.weight: activePlaylistId.length === 0 ? Theme.fontWeightMedium : Theme.fontWeightNormal
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onClicked: root.activePlaylistChanged("")
            onEntered: if (activePlaylistId.length > 0) parent.color = Theme.withAlpha(Theme.brand, 0.3)
            onExited: if (activePlaylistId.length > 0) parent.color = "transparent"
        }
    }

    // Playlist item with thumbnails
    ColumnLayout {
        visible: !root.isSpecial
        anchors.fill: parent
        spacing: Theme.spaceXs

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: root.rowH
            radius: Theme.radiusMd
            color: isActive ? Theme.elevated : "transparent"
            Behavior on color { ColorAnimation { duration: Theme.animFast } }

            Drag.active: dragMouse.drag.active && root.draggable
            Drag.source: root
            Drag.hotSpot.x: width / 2
            Drag.hotSpot.y: root.rowH / 2

            MouseArea {
                id: dragMouse
                anchors.fill: parent
                hoverEnabled: true
                onClicked: root.activePlaylistChanged(playlistData.id)
                onEntered: if (!isActive) parent.color = Theme.withAlpha(Theme.elevated, 0.5)
                onExited: if (!isActive) parent.color = "transparent"
                drag.target: root.draggable ? parent : undefined
                drag.axis: Drag.YAxis
            }

            states: State {
                when: dragMouse.drag.active && root.draggable
                PropertyChanges { target: root; opacity: 0.5 }
                AnchorChanges { target: parent; anchors.horizontalCenter: undefined; anchors.verticalCenter: undefined }
            }

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: Theme.spaceSm
                anchors.rightMargin: Theme.spaceSm
                spacing: Theme.spaceSm

                Rectangle {
                    width: 28
                    height: 28
                    radius: Theme.radiusSm
                    color: root.generateAvatarColor(playlistData.name || "")

                    Text {
                        anchors.centerIn: parent
                        text: root.getInitialFn(playlistData.name || "")
                        color: "white"
                        font.pixelSize: Theme.fontSizeXs
                        font.bold: true
                    }
                }

                Text {
                    Layout.fillWidth: true
                    text: playlistData.name || "Unnamed"
                    color: isActive ? Theme.fg : Theme.fgMuted
                    font.pixelSize: Theme.fontSizeSm
                    font.weight: isActive ? Theme.fontWeightMedium : Theme.fontWeightNormal
                    elide: Text.ElideRight
                }

                Rectangle {
                    width: badgeText.width + 8
                    height: 18
                    radius: Theme.radiusSm
                    color: Theme.overlay

                    Text {
                        id: badgeText
                        anchors.centerIn: parent
                        text: wpIds.length
                        color: Theme.fgMuted
                        font.pixelSize: Theme.fontSizeXs
                    }
                }

                Ctrl.GIconButton {
                    iconName: expanded ? "chevronDown" : "chevronRight"
                    size: Theme.iconButtonSm
                    onClicked: expanded = !expanded
                }
            }
        }

        Row {
            id: plThumbRow
            Layout.fillWidth: true
            visible: expanded && wpIds.length > 0
            spacing: 2
            clip: true

            Repeater {
                model: {
                    var ids = wpIds
                    var shown = ids.length <= root.maxThumbs ? ids : ids.slice(0, root.maxThumbs - 1)
                    return shown
                }
                delegate: Rectangle {
                    required property var modelData
                    width: 32
                    height: 32
                    radius: Theme.radiusSm
                    color: Theme.overlay
                    clip: true

                    property string previewUrl: {
                        for (var i = 0; i < root.wallpapers.length; i++) {
                            if (root.wallpapers[i].id === modelData) {
                                return root.wallpapers[i].preview || ""
                            }
                        }
                        return ""
                    }

                    Image {
                        anchors.fill: parent
                        source: previewUrl
                        fillMode: Image.PreserveAspectCrop
                        asynchronous: true
                        cache: true
                        visible: status === Image.Ready
                    }

                    Text {
                        anchors.centerIn: parent
                        visible: previewUrl.length === 0
                        text: root.getInitialFn(modelData)
                        color: Theme.fgSubtle
                        font.pixelSize: Theme.fontSizeXs
                    }
                }
            }

            Rectangle {
                id: overflowRect
                visible: wpIds.length > root.maxThumbs
                width: 32
                height: 32
                radius: Theme.radiusSm
                color: Theme.withAlpha(Theme.overlay, 0.8)

                property string overflowThumbUrl: {
                    var ids = wpIds
                    var idx = root.maxThumbs - 1
                    if (idx < ids.length) {
                        for (var i = 0; i < root.wallpapers.length; i++) {
                            if (root.wallpapers[i].id === ids[idx]) {
                                return root.wallpapers[i].preview || ""
                            }
                        }
                    }
                    return ""
                }

                Image {
                    anchors.fill: parent
                    source: overflowRect.overflowThumbUrl
                    fillMode: Image.PreserveAspectCrop
                    asynchronous: true
                    cache: true
                    visible: status === Image.Ready
                    opacity: 0.6
                }

                Rectangle {
                    anchors.fill: parent
                    radius: Theme.radiusSm
                    color: Theme.withAlpha(Theme.bg, 0.6)

                    Text {
                        anchors.centerIn: parent
                        text: "+" + (wpIds.length - root.maxThumbs + 1)
                        color: "white"
                        font.pixelSize: Theme.fontSizeXs
                        font.bold: true
                    }
                }
            }
        }

        Text {
            visible: expanded && wpIds.length === 0
            text: "No wallpapers in this playlist"
            color: Theme.fgSubtle
            font.pixelSize: Theme.fontSizeXs
        }
    }
}