import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl
import "." as Comp

Item {
    id: root

    property var wallpapers: []
    property string selectedId: ""
    property int columns: 5
    property int cellGap: Theme.spaceMd
    property bool showTitle: true
    property bool showIcons: true
    property string searchText: ""
    property string sortBy: "name"
    property string activePlaylistId: ""
    property var playlists: []
    property bool selectionMode: false
    property var selectedForPlaylist: []

    signal selectRequested(string wallpaperId)
    signal applyRequested(string wallpaperId)
    signal favoriteToggled(string wallpaperId)
    signal stopRequested(string wallpaperId)
    signal openFolderRequested(string wallpaperId)
    signal deleteRequested(string wallpaperId)
    signal editNicknameRequested(string wallpaperId, string nickname)
    signal addToPlaylistRequested(string wallpaperId, string playlistId)
    signal copyIdRequested(string wallpaperId)
    signal workshopRequested(string wallpaperId)
    signal selectionToggled(string wallpaperId)
    signal configurePathRequested()
    signal browseAllRequested()
    signal highlightSettingRequested(string fieldName)

    GridView {
        id: gridView
        anchors.fill: parent

        model: {
            var arr = []
            for (var i = 0; i < root.wallpapers.length; i++) {
                arr.push(root.wallpapers[i])
            }

            var q = (root.searchText || "").toLowerCase()
            if (q.length > 0) {
                arr = arr.filter(function(item) {
                    var title = (item.title || "").toLowerCase()
                    var wid = (item.id || "").toLowerCase()
                    return title.indexOf(q) >= 0 || wid.indexOf(q) >= 0
                })
            }

            if (root.activePlaylistId && root.activePlaylistId.length > 0) {
                var matched = null
                for (var p = 0; p < root.playlists.length; p++) {
                    var playlist = root.playlists[p]
                    if (playlist.id === root.activePlaylistId) {
                        matched = playlist
                        break
                    }
                }
                if (matched && matched.wallpaper_ids) {
                    arr = arr.filter(function(item) {
                        return matched.wallpaper_ids.indexOf(item.id) >= 0
                    })
                } else {
                    arr = []
                }
            }

            if (root.sortBy === "id") {
                arr.sort(function(a, b) {
                    return (a.id || "").localeCompare(b.id || "")
                })
            } else if (root.sortBy === "size") {
                arr.sort(function(a, b) {
                    var sa = parseFloat(String(a.size || "0").replace(" MB", ""))
                    var sb = parseFloat(String(b.size || "0").replace(" MB", ""))
                    return sb - sa
                })
            } else {
                arr.sort(function(a, b) {
                    return (a.title || "").localeCompare(b.title || "")
                })
            }

            return arr
        }
        clip: true

        cellWidth: Math.max(220, Math.floor((width - ((root.columns - 1) * root.cellGap)) / root.columns))
        cellHeight: Math.floor(cellWidth * 0.86)

        delegate: WallpaperCard {
            width: gridView.cellWidth - root.cellGap
            height: gridView.cellHeight - root.cellGap

            wp: modelData
            showTitle: root.showTitle
            showIcons: root.showIcons
            isSelected: root.selectedId === modelData.id
            selectionMode: root.selectionMode
            selectionChecked: root.selectedForPlaylist.indexOf(modelData.id) >= 0

            onSelected: root.selectRequested(modelData.id)
            onApplyRequested: root.applyRequested(modelData.id)
            onFavoriteToggled: root.favoriteToggled(modelData.id)
            onContextMenuRequested: function(mousePos) {
                contextMenu.wallpaperId = modelData.id
                contextMenu.popup(null, mousePos.x, mousePos.y)
            }
            onSelectionToggled: root.selectionToggled(modelData.id)
        }

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AsNeeded
        }
    }

    WallpaperContextMenu {
        id: contextMenu
        playlists: root.playlists
        onApplyRequested: root.applyRequested(wallpaperId)
        onStopRequested: root.stopRequested(wallpaperId)
        onOpenFolderRequested: root.openFolderRequested(wallpaperId)
        onDeleteRequested: root.deleteRequested(wallpaperId)
        onEditNicknameRequested: {
            nicknameDialog.wallpaperId = wallpaperId
            nicknameDialog.open()
        }
        onAddToPlaylistRequested: function(playlistId) {
            root.addToPlaylistRequested(wallpaperId, playlistId)
        }
        onCopyIdRequested: root.copyIdRequested(wallpaperId)
        onWorkshopRequested: root.workshopRequested(wallpaperId)
    }

    // Empty state: search no results
    Comp.GEmptyState {
        anchors.centerIn: parent
        visible: !gridView.count && root.searchText.length > 0
        iconName: "search"
        title: "No Results Found"
        description: "No wallpapers match \"" + root.searchText + "\".\nTry different keywords or check your spelling."
    }

    // Empty state: empty playlist / favorites
    Comp.GEmptyState {
        anchors.centerIn: parent
        visible: !gridView.count && root.searchText.length === 0 && root.wallpapers.length > 0 && root.activePlaylistId.length > 0
        iconName: root.activePlaylistId === "favorites" ? "star" : "list"
        title: root.activePlaylistId === "favorites" ? "No Favorites Yet" : "This Playlist is Empty"
        description: root.activePlaylistId === "favorites"
            ? "You haven't added any wallpapers to your favorites.\nClick the star icon on any wallpaper to add it."
            : "This playlist doesn't have any wallpapers yet."
        actionText: root.activePlaylistId === "favorites" ? "Browse Wallpapers" : "Browse & Add Wallpapers"
        onActionTriggered: root.browseAllRequested()
    }

    // Empty state: no wallpapers at all
    Comp.GEmptyState {
        anchors.centerIn: parent
        visible: !gridView.count && root.searchText.length === 0 && root.wallpapers.length === 0
        iconName: "search"
        title: "No Wallpapers Found"
        description: "The wallpaper library appears to be empty."
        actionText: "Configure Library Path"
        onActionTriggered: root.highlightSettingRequested("workshopPath")
    }

    Dialog {
        id: nicknameDialog
        property string wallpaperId: ""
        modal: true
        title: "Edit Nickname"
        standardButtons: Dialog.Ok | Dialog.Cancel

        background: Rectangle {
            radius: Theme.radiusXl
            color: Theme.elevated
            border.width: 1
            border.color: Theme.border
        }

        onOpened: {
            nicknameInput.text = ""
            for (var i = 0; i < root.wallpapers.length; i++) {
                if (root.wallpapers[i].id === wallpaperId) {
                    nicknameInput.text = root.wallpapers[i].title || ""
                    break
                }
            }
            nicknameInput.forceActiveFocus()
            nicknameInput.selectAll()
        }

        onAccepted: {
            if (wallpaperId.length > 0) {
                root.editNicknameRequested(wallpaperId, nicknameInput.text)
            }
        }

        contentItem: ColumnLayout {
            spacing: Theme.spaceSm
            Ctrl.GTextField {
                id: nicknameInput
                placeholderText: "Nickname"
                selectByMouse: true
                onAccepted: {
                    nicknameDialog.accept()
                }
            }
        }
    }
}