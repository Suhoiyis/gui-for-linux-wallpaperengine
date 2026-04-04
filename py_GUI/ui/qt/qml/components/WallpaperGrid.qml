import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root

    property var wallpapers: []
    property string selectedId: ""
    property int columns: 5
    property int cellGap: 12
    property bool showTitle: true
    property bool showIcons: true
    property string searchText: ""
    property string sortBy: "name"
    property string activePlaylistId: ""
    property var playlists: []

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

            onSelected: root.selectRequested(modelData.id)
            onApplyRequested: root.applyRequested(modelData.id)
            onFavoriteToggled: root.favoriteToggled(modelData.id)
            onContextMenuRequested: function(mousePos) {
                contextMenu.wallpaperId = modelData.id
                contextMenu.popup(null, mousePos.x, mousePos.y)
            }
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

    Label {
        anchors.centerIn: parent
        visible: !gridView.count
        text: "No wallpapers found"
        color: "#8a90b8"
    }

    Dialog {
        id: nicknameDialog
        property string wallpaperId: ""
        modal: true
        title: "Edit Nickname"
        standardButtons: Dialog.Ok | Dialog.Cancel

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
            spacing: 8
            TextField {
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
