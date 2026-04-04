import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root

    property var playlists: []
    property string activePlaylistId: ""
    property var favoriteIds: []

    property string panelState: "minimized" // minimized | floating | locked
    property bool createDialogOpen: false

    signal activePlaylistChanged(string playlistId)
    signal activePlaylistCleared()
    signal createPlaylistRequested(string playlistName)

    width: panelState === "locked" ? 268 : 48

    Timer {
        id: hoverOpenTimer
        interval: 300
        repeat: false
        onTriggered: {
            if (root.panelState === "minimized") {
                root.panelState = "floating"
            }
        }
    }

    Timer {
        id: autoCloseTimer
        interval: 500
        repeat: false
        onTriggered: {
            if (root.panelState === "floating") {
                root.panelState = "minimized"
            }
        }
    }

    Rectangle {
        id: iconColumn
        width: 48
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        color: "#181b28"
        border.width: 1
        border.color: "#2f344b"

        ColumnLayout {
            anchors.fill: parent
            spacing: 6

            Item { Layout.preferredHeight: 44 }

            Button {
                Layout.alignment: Qt.AlignHCenter
                text: "≡"
                width: 36
                height: 36
                highlighted: root.activePlaylistId.length === 0
                onClicked: root.activePlaylistCleared()
            }

            Button {
                Layout.alignment: Qt.AlignHCenter
                text: "★"
                width: 36
                height: 36
                highlighted: root.activePlaylistId === "favorites"
                onClicked: root.activePlaylistChanged("favorites")
            }

            Repeater {
                model: root.playlists.filter(function(p) { return p.id !== "favorites" })
                delegate: Button {
                    required property var modelData
                    Layout.alignment: Qt.AlignHCenter
                    text: (modelData.name || "?").charAt(0).toUpperCase()
                    width: 36
                    height: 36
                    highlighted: root.activePlaylistId === modelData.id
                    onClicked: root.activePlaylistChanged(modelData.id)
                }
            }

            Item { Layout.fillHeight: true }

            Button {
                Layout.alignment: Qt.AlignHCenter
                text: "+"
                width: 36
                height: 36
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
        x: 48
        width: 220
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        color: "#1b1f2f"
        border.width: 1
        border.color: "#2f344b"
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
                Layout.preferredHeight: 52
                Layout.leftMargin: 8
                Layout.rightMargin: 8
                Label {
                    text: "Playlists"
                    color: "#c0caf5"
                    font.bold: true
                    Layout.fillWidth: true
                }
                Button {
                    text: "📌"
                    width: 28
                    height: 28
                    onClicked: root.panelState = "locked"
                }
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Column {
                    width: parent.width
                    spacing: 4

                    Button {
                        width: parent.width
                        text: "All Wallpapers"
                        highlighted: root.activePlaylistId.length === 0
                        onClicked: root.activePlaylistCleared()
                    }

                    Repeater {
                        model: root.playlists
                        delegate: Button {
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
                Layout.preferredHeight: 48
                Layout.leftMargin: 8
                Layout.rightMargin: 8
                Button {
                    Layout.fillWidth: true
                    text: "New Playlist"
                    onClicked: root.createDialogOpen = true
                }
            }
        }
    }

    Rectangle {
        id: lockedPanel
        visible: root.panelState === "locked"
        x: 48
        width: 220
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        color: "#1b1f2f"
        border.width: 1
        border.color: "#2f344b"

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: 52
                Layout.leftMargin: 8
                Layout.rightMargin: 8
                Label {
                    text: "Playlists"
                    color: "#c0caf5"
                    font.bold: true
                    Layout.fillWidth: true
                }
                Button {
                    text: "📍"
                    width: 28
                    height: 28
                    onClicked: root.panelState = "minimized"
                }
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Column {
                    width: parent.width
                    spacing: 4

                    Button {
                        width: parent.width
                        text: "All Wallpapers"
                        highlighted: root.activePlaylistId.length === 0
                        onClicked: root.activePlaylistCleared()
                    }

                    Repeater {
                        model: root.playlists
                        delegate: Button {
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
                Layout.preferredHeight: 48
                Layout.leftMargin: 8
                Layout.rightMargin: 8
                Button {
                    Layout.fillWidth: true
                    text: "New Playlist"
                    onClicked: root.createDialogOpen = true
                }
            }
        }
    }

    Dialog {
        id: createDialog
        visible: root.createDialogOpen
        modal: true
        title: "Create Playlist"
        standardButtons: Dialog.Ok | Dialog.Cancel

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
            spacing: 8
            TextField {
                id: nameInput
                placeholderText: "Playlist name"
                selectByMouse: true
            }
        }
    }
}
