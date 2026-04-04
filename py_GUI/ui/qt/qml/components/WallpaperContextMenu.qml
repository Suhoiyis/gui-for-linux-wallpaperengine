import QtQuick
import QtQuick.Controls
import QtQml

Menu {
    id: root

    property string wallpaperId: ""
    property var playlists: []

    signal applyRequested()
    signal stopRequested()
    signal openFolderRequested()
    signal deleteRequested()
    signal editNicknameRequested()
    signal addToPlaylistRequested(string playlistId)
    signal copyIdRequested()
    signal workshopRequested()

    MenuItem {
        text: "▶ Apply Wallpaper"
        onTriggered: root.applyRequested()
    }
    MenuItem {
        text: "⏹ Stop Wallpaper"
        onTriggered: root.stopRequested()
    }
    MenuSeparator {}
    MenuItem {
        text: "📁 Open Folder"
        onTriggered: root.openFolderRequested()
    }
    MenuItem {
        text: "🌐 Workshop"
        onTriggered: root.workshopRequested()
    }
    MenuItem {
        text: "📋 Copy ID"
        onTriggered: root.copyIdRequested()
    }
    MenuSeparator {}
    MenuItem {
        text: "✏ Edit Nickname"
        onTriggered: root.editNicknameRequested()
    }
    Menu {
        id: addToPlaylistMenu
        title: "➕ Add to Playlist"
        Instantiator {
            model: root.playlists
            onObjectAdded: function(index, object) {
                addToPlaylistMenu.insertItem(index, object)
            }
            onObjectRemoved: function(index, object) {
                addToPlaylistMenu.removeItem(object)
            }
            delegate: MenuItem {
                text: modelData.name
                onTriggered: root.addToPlaylistRequested(modelData.id)
            }
        }
    }
    MenuSeparator {}
    MenuItem {
        text: "🗑 Delete Wallpaper"
        // color: "#f7768e" // QtQuick Controls Menu doesn't support color directly on MenuItem easily without custom delegate, but we can use rich text or just text
        onTriggered: root.deleteRequested()
    }
}
