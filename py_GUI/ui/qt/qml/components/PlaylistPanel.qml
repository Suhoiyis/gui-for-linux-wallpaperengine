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
        color: Theme.sidebarBg
        border.width: 1
        border.color: Theme.panelBorder

        ColumnLayout {
            anchors.fill: parent
            spacing: Theme.spaceSm

            Item { Layout.preferredHeight: Theme.navHeight - Theme.spaceXs }

            Ctrl.GIconButton {
                Layout.alignment: Qt.AlignHCenter
                text: "≡"
                size: Theme.navButtonSize
                highlighted: root.activePlaylistId.length === 0
                onClicked: root.activePlaylistCleared()
            }

            Ctrl.GIconButton {
                Layout.alignment: Qt.AlignHCenter
                text: "★"
                size: Theme.navButtonSize
                highlighted: root.activePlaylistId === "favorites"
                onClicked: root.activePlaylistChanged("favorites")
            }

            Repeater {
                model: root.playlists.filter(function(p) { return p.id !== "favorites" })
                delegate: Ctrl.GIconButton {
                    required property var modelData
                    Layout.alignment: Qt.AlignHCenter
                    text: (modelData.name || "?").charAt(0).toUpperCase()
                    size: Theme.navButtonSize
                    highlighted: root.activePlaylistId === modelData.id
                    onClicked: root.activePlaylistChanged(modelData.id)
                }
            }

            Item { Layout.fillHeight: true }

            Ctrl.GIconButton {
                Layout.alignment: Qt.AlignHCenter
                text: "+"
                size: Theme.navButtonSize
                onClicked: root.createDialogOpen = true
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
        color: Theme.sidebarBg
        border.width: 1
        border.color: Theme.panelBorder
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

            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: Theme.navHeight + Theme.spaceXs
                Layout.leftMargin: Theme.spaceSm
                Layout.rightMargin: Theme.spaceSm
                Label {
                    text: "Playlists"
                    color: Theme.textPrimary
                    font.bold: true
                    Layout.fillWidth: true
                }
                Ctrl.GIconButton {
                    text: "📌"
                    size: Theme.iconButtonSm
                    onClicked: root.panelState = "locked"
                }
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Column {
                    width: parent.width
                    spacing: Theme.spaceXs

                    Ctrl.GButton {
                        width: parent.width
                        text: "All Wallpapers"
                        highlighted: root.activePlaylistId.length === 0
                        onClicked: root.activePlaylistCleared()
                    }

                    Repeater {
                        model: root.playlists
                        delegate: Ctrl.GButton {
                            required property var modelData
                            width: parent.width
                            text: modelData.name || "Unnamed"
                            highlighted: root.activePlaylistId === modelData.id
                            onClicked: root.activePlaylistChanged(modelData.id)
                        }
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: Theme.navButtonSize + Theme.spaceSm
                Layout.leftMargin: Theme.spaceSm
                Layout.rightMargin: Theme.spaceSm
                Ctrl.GButton {
                    Layout.fillWidth: true
                    text: "New Playlist"
                    onClicked: root.createDialogOpen = true
                }
                Ctrl.GButton {
                    Layout.preferredWidth: 74
                    text: "Rename"
                    enabled: root.activePlaylistId.length > 0 && root.activePlaylistId !== "favorites"
                    onClicked: root.beginRenameForActivePlaylist()
                }
                Ctrl.GButton {
                    Layout.preferredWidth: 66
                    text: "Delete"
                    enabled: root.activePlaylistId.length > 0 && root.activePlaylistId !== "favorites"
                    onClicked: root.beginDeleteForActivePlaylist()
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
        color: Theme.sidebarBg
        border.width: 1
        border.color: Theme.panelBorder

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: Theme.navHeight + Theme.spaceXs
                Layout.leftMargin: Theme.spaceSm
                Layout.rightMargin: Theme.spaceSm
                Label {
                    text: "Playlists"
                    color: Theme.textPrimary
                    font.bold: true
                    Layout.fillWidth: true
                }
                Ctrl.GIconButton {
                    text: "📍"
                    size: Theme.iconButtonSm
                    onClicked: root.panelState = "minimized"
                }
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Column {
                    width: parent.width
                    spacing: Theme.spaceXs

                    Ctrl.GButton {
                        width: parent.width
                        text: "All Wallpapers"
                        highlighted: root.activePlaylistId.length === 0
                        onClicked: root.activePlaylistCleared()
                    }

                    Repeater {
                        model: root.playlists
                        delegate: Ctrl.GButton {
                            required property var modelData
                            width: parent.width
                            text: modelData.name || "Unnamed"
                            highlighted: root.activePlaylistId === modelData.id
                            onClicked: root.activePlaylistChanged(modelData.id)
                        }
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: Theme.navButtonSize + Theme.spaceSm
                Layout.leftMargin: Theme.spaceSm
                Layout.rightMargin: Theme.spaceSm
                Ctrl.GButton {
                    Layout.fillWidth: true
                    text: "New Playlist"
                    onClicked: root.createDialogOpen = true
                }
                Ctrl.GButton {
                    Layout.preferredWidth: 74
                    text: "Rename"
                    enabled: root.activePlaylistId.length > 0 && root.activePlaylistId !== "favorites"
                    onClicked: root.beginRenameForActivePlaylist()
                }
                Ctrl.GButton {
                    Layout.preferredWidth: 66
                    text: "Delete"
                    enabled: root.activePlaylistId.length > 0 && root.activePlaylistId !== "favorites"
                    onClicked: root.beginDeleteForActivePlaylist()
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
            color: Theme.panelBg
            border.width: 1
            border.color: Theme.panelBorder
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
            color: Theme.panelBg
            border.width: 1
            border.color: Theme.panelBorder
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
            color: Theme.panelBg
            border.width: 1
            border.color: Theme.panelBorder
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