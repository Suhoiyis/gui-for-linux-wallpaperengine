import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Item {
    id: root

    property var playlists: []
    property string activePlaylistId: ""
    property var favoriteIds: []

    property string panelState: "minimized" // minimized | floating | locked
    property bool createDialogOpen: false
    property bool renameDialogOpen: false
    property bool deleteDialogOpen: false

    property string pendingPlaylistId: ""
    property string pendingPlaylistName: ""

    signal activePlaylistChanged(string playlistId)
    signal activePlaylistCleared()
    signal createPlaylistRequested(string playlistName)
    signal renamePlaylistRequested(string playlistId, string playlistName)
    signal deletePlaylistRequested(string playlistId)

    function generateAvatarColor(name) {
        var colors = [
            "#f43f5e", "#ec4899", "#d946ef", "#a855f7", "#8b5cf6",
            "#6366f1", "#3b82f6", "#06b6d4", "#14b8a6", "#10b981",
            "#84cc16", "#eab308", "#f97316"
        ]
        var hash = 0
        for (var i = 0; i < name.length; i++) {
            hash = name.charCodeAt(i) + ((hash << 5) - hash)
        }
        return colors[Math.abs(hash) % colors.length]
    }

    function getInitial(name) {
        return name.charAt(0).toUpperCase()
    }

    function beginRenameForActivePlaylist() {
        var found = null
        for (var i = 0; i < root.playlists.length; i++) {
            if (root.playlists[i].id === root.activePlaylistId) {
                found = root.playlists[i]
                break
            }
        }
        if (found) {
            root.pendingPlaylistId = found.id
            root.pendingPlaylistName = found.name || ""
            root.renameDialogOpen = true
        }
    }

    function beginDeleteForActivePlaylist() {
        root.pendingPlaylistId = root.activePlaylistId
        root.deleteDialogOpen = true
    }

    width: panelState === "locked" ? 268 : Theme.navButtonSize + Theme.spaceMd

    Timer {
        id: hoverOpenTimer
        interval: Theme.playlistHoverOpen
        repeat: false
        onTriggered: {
            if (root.panelState === "minimized") {
                root.panelState = "floating"
            }
        }
    }

    Timer {
        id: autoCloseTimer
        interval: Theme.playlistAutoClose
        repeat: false
        onTriggered: {
            if (root.panelState === "floating") {
                root.panelState = "minimized"
            }
        }
    }

    Rectangle {
        id: iconColumn
        width: Theme.navButtonSize + Theme.spaceMd
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        color: Theme.surface
        border.width: 1
        border.color: Theme.border

        ColumnLayout {
            anchors.fill: parent
            spacing: Theme.spaceSm

            // Header spacer matching floating/locked panel header height
            Item { Layout.preferredHeight: 52 }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                ColumnLayout {
                    width: parent.width
                    spacing: Theme.spaceXs

                    // All Wallpapers button
                    Rectangle {
                        Layout.alignment: Qt.AlignHCenter
                        width: 36
                        height: 36
                        radius: Theme.radiusMd
                        color: root.activePlaylistId.length === 0 ? Theme.elevated : "transparent"

                        Behavior on color { ColorAnimation { duration: Theme.animFast } }

                        Rectangle {
                            anchors.fill: parent
                            anchors.margins: root.activePlaylistId.length === 0 ? 0 : 4
                            radius: root.activePlaylistId.length === 0 ? Theme.radiusMd : Theme.radiusSm
                            color: root.activePlaylistId.length === 0 ? Theme.brand : "transparent"
                            opacity: root.activePlaylistId.length === 0 ? 1 : 0
                            Behavior on opacity { NumberAnimation { duration: Theme.animFast } }
                        }

                        Ctrl.GIcon {
                            anchors.centerIn: parent
                            name: "list"
                            size: Theme.fontSizeMd
                            color: root.activePlaylistId.length === 0 ? Theme.brandFg : Theme.fgMuted
                        }

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onClicked: root.activePlaylistCleared()
                            onEntered: if (root.activePlaylistId.length > 0) parent.color = Theme.withAlpha(Theme.elevated, 0.5)
                            onExited: if (root.activePlaylistId.length > 0) parent.color = "transparent"
                        }
                    }

                    // Separator
                    Rectangle {
                        Layout.alignment: Qt.AlignHCenter
                        width: 32
                        height: 1
                        color: Theme.border
                    }

                    // Favorites button
                    Rectangle {
                        Layout.alignment: Qt.AlignHCenter
                        width: 36
                        height: 36
                        radius: Theme.radiusMd
                        color: root.activePlaylistId === "favorites" ? Theme.elevated : "transparent"

                        Behavior on color { ColorAnimation { duration: Theme.animFast } }

                        Rectangle {
                            anchors.fill: parent
                            anchors.margins: root.activePlaylistId === "favorites" ? 0 : 4
                            radius: root.activePlaylistId === "favorites" ? Theme.radiusMd : Theme.radiusSm
                            color: root.activePlaylistId === "favorites" ? Theme.brand : "transparent"
                            opacity: root.activePlaylistId === "favorites" ? 1 : 0
                            Behavior on opacity { NumberAnimation { duration: Theme.animFast } }
                        }

                        Ctrl.GIcon {
                            anchors.centerIn: parent
                            name: "star"
                            size: Theme.fontSizeMd
                            color: {
                                if (root.activePlaylistId === "favorites") return Theme.favoriteGold
                                return Theme.fgMuted
                            }
                        }

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onClicked: root.activePlaylistChanged("favorites")
                            onEntered: if (root.activePlaylistId !== "favorites") parent.color = Theme.withAlpha(Theme.elevated, 0.5)
                            onExited: if (root.activePlaylistId !== "favorites") parent.color = "transparent"
                        }
                    }

                    // Playlist avatars
                    Repeater {
                        model: root.playlists.filter(function(p) { return p.id !== "favorites" })
                        delegate: Rectangle {
                            required property var modelData
                            Layout.alignment: Qt.AlignHCenter
                            width: 36
                            height: 36
                            radius: Theme.radiusMd
                            color: root.activePlaylistId === modelData.id ? Theme.elevated : "transparent"

                            Behavior on color { ColorAnimation { duration: Theme.animFast } }

                            Rectangle {
                                anchors.fill: parent
                                anchors.margins: root.activePlaylistId === modelData.id ? 0 : 4
                                radius: root.activePlaylistId === modelData.id ? Theme.radiusMd : Theme.radiusSm
                                color: root.activePlaylistId === modelData.id ? Theme.brand : "transparent"
                                opacity: root.activePlaylistId === modelData.id ? 1 : 0
                                Behavior on opacity { NumberAnimation { duration: Theme.animFast } }
                            }

                            Rectangle {
                                anchors.centerIn: parent
                                width: root.activePlaylistId === modelData.id ? 28 : 24
                                height: root.activePlaylistId === modelData.id ? 28 : 24
                                radius: Theme.radiusSm
                                color: root.generateAvatarColor(modelData.name || "")
                                Behavior on width { NumberAnimation { duration: Theme.animFast } }
                                Behavior on height { NumberAnimation { duration: Theme.animFast } }

                                Text {
                                    anchors.centerIn: parent
                                    text: root.getInitial(modelData.name || "")
                                    color: "white"
                                    font.pixelSize: Theme.fontSizeSm
                                    font.bold: true
                                }
                            }

                            MouseArea {
                                anchors.fill: parent
                                hoverEnabled: true
                                onClicked: root.activePlaylistChanged(modelData.id)
                                onEntered: if (root.activePlaylistId !== modelData.id) parent.color = Theme.withAlpha(Theme.elevated, 0.5)
                                onExited: if (root.activePlaylistId !== modelData.id) parent.color = "transparent"
                            }
                        }
                    }

                    Item { Layout.fillHeight: true }
                }
            }

            // Footer with create button
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 48
                color: Theme.withAlpha(Theme.bg, 0.5)
                border.width: 1
                border.color: Theme.border

                Rectangle {
                    anchors.centerIn: parent
                    width: 32
                    height: 32
                    radius: Theme.radiusMd
                    color: "transparent"

                    Ctrl.GIcon {
                        anchors.centerIn: parent
                        name: "plus"
                        size: Theme.fontSizeMd
                        color: Theme.fgMuted
                    }

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: root.createDialogOpen = true
                        onEntered: parent.color = Theme.elevated
                        onExited: parent.color = "transparent"
                    }
                }
            }
        }

        HoverHandler {
            acceptedDevices: PointerDevice.Mouse
            onHoveredChanged: function() {
                if (hovered) {
                    autoCloseTimer.stop()
                    if (root.panelState === "minimized") {
                        hoverOpenTimer.restart()
                    }
                } else {
                    hoverOpenTimer.stop()
                    if (root.panelState === "floating") {
                        autoCloseTimer.restart()
                    }
                }
            }
        }
    }

    Rectangle {
        id: floatingPanel
        visible: root.panelState === "floating"
        x: Theme.navButtonSize + Theme.spaceMd
        width: 220
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        color: Theme.surface
        border.width: 1
        border.color: Theme.border
        z: 20

        HoverHandler {
            acceptedDevices: PointerDevice.Mouse
            onHoveredChanged: function() {
                if (hovered) {
                    autoCloseTimer.stop()
                } else {
                    autoCloseTimer.restart()
                }
            }
        }

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            // Header
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 52
                color: "transparent"
                border.width: 0
                border.color: Theme.border

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: Theme.spaceSm
                    anchors.rightMargin: Theme.spaceSm
                    spacing: Theme.spaceSm

                    Ctrl.GIcon {
                        name: "list"
                        size: Theme.fontSizeMd
                        color: Theme.fgMuted
                    }

                    Label {
                        text: "Playlists"
                        color: Theme.fg
                        font.pixelSize: Theme.fontSizeSm
                        font.bold: true
                        Layout.fillWidth: true
                    }

                    Ctrl.GIconButton {
                        iconName: "pin"
                        size: Theme.iconButtonSm
                        tooltip: "Pin (locked mode)"
                        onClicked: root.panelState = "locked"
                    }
                }
            }

            // Separator
            Rectangle {
                Layout.fillWidth: true
                height: 1
                color: Theme.border
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                Column {
                    width: parent.width
                    spacing: Theme.spaceXs
                    padding: Theme.spaceSm

                    Ctrl.GButton {
                        width: parent.width - Theme.spaceSm * 2
                        x: Theme.spaceSm
                        text: "All Wallpapers"
                        variant: root.activePlaylistId.length === 0 ? "brand" : "ghost"
                        onClicked: root.activePlaylistCleared()
                    }

                    // Separator
                    Rectangle {
                        width: parent.width - Theme.spaceSm * 2
                        x: Theme.spaceSm
                        height: 1
                        color: Theme.border
                    }

                    Repeater {
                        model: root.playlists
                        delegate: Ctrl.GButton {
                            required property var modelData
                            width: parent.width - Theme.spaceSm * 2
                            x: Theme.spaceSm
                            text: modelData.name || "Unnamed"
                            variant: root.activePlaylistId === modelData.id ? "brand" : "ghost"
                            onClicked: root.activePlaylistChanged(modelData.id)
                        }
                    }
                }
            }

            // Footer
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 48
                color: Theme.withAlpha(Theme.bg, 0.5)
                border.width: 1
                border.color: Theme.border

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: Theme.spaceSm
                    anchors.rightMargin: Theme.spaceSm
                    spacing: Theme.spaceSm

                    Ctrl.GButton {
                        Layout.fillWidth: true
                        text: "New Playlist"
                        iconName: "plus"
                        variant: "outline"
                        onClicked: root.createDialogOpen = true
                    }
                }
            }
        }
    }

    Rectangle {
        id: lockedPanel
        visible: root.panelState === "locked"
        x: Theme.navButtonSize + Theme.spaceMd
        width: 220
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        color: Theme.surface
        border.width: 1
        border.color: Theme.border

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            // Header
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 52
                color: "transparent"
                border.width: 0
                border.color: Theme.border

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: Theme.spaceSm
                    anchors.rightMargin: Theme.spaceSm
                    spacing: Theme.spaceSm

                    Ctrl.GIcon {
                        name: "list"
                        size: Theme.fontSizeMd
                        color: Theme.fgMuted
                    }

                    Label {
                        text: "Playlists"
                        color: Theme.fg
                        font.pixelSize: Theme.fontSizeSm
                        font.bold: true
                        Layout.fillWidth: true
                    }

                    Ctrl.GIconButton {
                        iconName: "pin"
                        size: Theme.iconButtonSm
                        tooltip: "Unpin (floating mode)"
                        onClicked: root.panelState = "minimized"
                    }
                }
            }

            // Separator
            Rectangle {
                Layout.fillWidth: true
                height: 1
                color: Theme.border
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                Column {
                    width: parent.width
                    spacing: Theme.spaceXs
                    padding: Theme.spaceSm

                    Ctrl.GButton {
                        width: parent.width - Theme.spaceSm * 2
                        x: Theme.spaceSm
                        text: "All Wallpapers"
                        variant: root.activePlaylistId.length === 0 ? "brand" : "ghost"
                        onClicked: root.activePlaylistCleared()
                    }

                    // Separator
                    Rectangle {
                        width: parent.width - Theme.spaceSm * 2
                        x: Theme.spaceSm
                        height: 1
                        color: Theme.border
                    }

                    Repeater {
                        model: root.playlists
                        delegate: Ctrl.GButton {
                            required property var modelData
                            width: parent.width - Theme.spaceSm * 2
                            x: Theme.spaceSm
                            text: modelData.name || "Unnamed"
                            variant: root.activePlaylistId === modelData.id ? "brand" : "ghost"
                            onClicked: root.activePlaylistChanged(modelData.id)
                        }
                    }
                }
            }

            // Footer
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 48
                color: Theme.withAlpha(Theme.bg, 0.5)
                border.width: 1
                border.color: Theme.border

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: Theme.spaceSm
                    anchors.rightMargin: Theme.spaceSm
                    spacing: Theme.spaceSm

                    Ctrl.GButton {
                        Layout.fillWidth: true
                        text: "New Playlist"
                        iconName: "plus"
                        variant: "outline"
                        onClicked: root.createDialogOpen = true
                    }
                }
            }
        }
    }

    Dialog {
        id: createDialog
        visible: root.createDialogOpen
        modal: true
        title: "Create Playlist"
        width: 420
        height: 170
        standardButtons: Dialog.Ok | Dialog.Cancel

        background: Rectangle {
            radius: Theme.radiusXl
            color: Theme.elevated
            border.width: 1
            border.color: Theme.border
        }

        readonly property var okButton: standardButton(Dialog.Ok)

        onOpened: {
            nameInput.forceActiveFocus()
            nameInput.selectAll()
        }

        Component.onCompleted: {
            okButton.enabled = Qt.binding(function() {
                return nameInput.text.trim().length > 0
            })
        }

        onAccepted: {
            if (nameInput.text.trim().length > 0) {
                root.createPlaylistRequested(nameInput.text.trim())
                nameInput.text = ""
            }
            root.createDialogOpen = false
        }
        onRejected: {
            root.createDialogOpen = false
        }

        contentItem: ColumnLayout {
            spacing: Theme.spaceSm
            Ctrl.GTextField {
                id: nameInput
                placeholderText: "Playlist name"
                selectByMouse: true
                onAccepted: {
                    if (createDialog.okButton.enabled) createDialog.accept()
                }
            }
        }
    }

    Dialog {
        id: renameDialog
        visible: root.renameDialogOpen
        modal: true
        title: "Rename Playlist"
        width: 420
        height: 170
        standardButtons: Dialog.Ok | Dialog.Cancel

        background: Rectangle {
            radius: Theme.radiusXl
            color: Theme.elevated
            border.width: 1
            border.color: Theme.border
        }

        readonly property var okButton: standardButton(Dialog.Ok)

        onOpened: {
            renameInput.text = root.pendingPlaylistName
            renameInput.forceActiveFocus()
            renameInput.selectAll()
        }

        Component.onCompleted: {
            okButton.enabled = Qt.binding(function() {
                return renameInput.text.trim().length > 0
            })
        }

        onAccepted: {
            if (root.pendingPlaylistId.length > 0 && renameInput.text.trim().length > 0) {
                root.renamePlaylistRequested(root.pendingPlaylistId, renameInput.text.trim())
            }
            root.renameDialogOpen = false
        }
        onRejected: {
            root.renameDialogOpen = false
        }

        contentItem: ColumnLayout {
            spacing: Theme.spaceSm
            Ctrl.GTextField {
                id: renameInput
                placeholderText: "Playlist name"
                selectByMouse: true
                onAccepted: {
                    if (renameDialog.okButton.enabled) renameDialog.accept()
                }
            }
        }
    }

    Dialog {
        id: deleteDialog
        visible: root.deleteDialogOpen
        modal: true
        title: "Delete Playlist"
        width: 360
        height: 150
        standardButtons: Dialog.Ok | Dialog.Cancel

        background: Rectangle {
            radius: Theme.radiusXl
            color: Theme.elevated
            border.width: 1
            border.color: Theme.border
        }

        onAccepted: {
            if (root.pendingPlaylistId.length > 0) {
                root.deletePlaylistRequested(root.pendingPlaylistId)
            }
            root.deleteDialogOpen = false
        }
        onRejected: {
            root.deleteDialogOpen = false
        }

        contentItem: ColumnLayout {
            spacing: Theme.spaceSm
            Label {
                text: "Delete selected playlist?"
            }
        }
    }
}