import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme

import "." as Comp

Item {
    id: root

    property var backend
    property string sortBy: "name"
    property string searchText: ""
    property bool playlistFloatingOpen: false
    property bool selectionMode: false
    property var selectedForPlaylist: []
    property int currentPage: 1
    property int itemsPerPage: 24
    property bool historyDialogOpen: false
    property bool deleteDialogOpen: false
    property string deleteWallpaperId: ""
    property string deleteWallpaperTitle: ""
    property string deleteWallpaperPath: ""

    function toggleSelection(wallpaperId) {
        var idx = selectedForPlaylist.indexOf(wallpaperId)
        if (idx >= 0) {
            selectedForPlaylist.splice(idx, 1)
        } else {
            selectedForPlaylist.push(wallpaperId)
        }
        selectedForPlaylist = selectedForPlaylist
    }

    function currentGridWallpapers() {
        var arr = root.backend ? root.backend.wallpapers : []
        var start = (root.currentPage - 1) * root.itemsPerPage
        var end = start + root.itemsPerPage
        return arr.slice(start, end)
    }

    function totalPages() {
        var total = root.backend ? root.backend.wallpapers.length : 0
        return Math.max(1, Math.ceil(total / root.itemsPerPage))
    }

    onSortByChanged: {
        root.currentPage = 1
    }

    onSearchTextChanged: {
        root.currentPage = 1
    }

    signal sortSelected(string value)
    signal searchQueryChanged(string value)
    signal refreshRequested()
    signal playlistFloatingStateChanged(bool opened)

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        Comp.LibraryHeader {
            Layout.fillWidth: true
            Layout.leftMargin: Theme.spaceSm
            Layout.rightMargin: Theme.spaceSm
            Layout.bottomMargin: Theme.spaceSm

            currentTitle: root.backend && root.backend.selectedId.length > 0
                ? root.backend.selectedId
                : "None"
            totalCount: root.backend ? root.backend.wallpapers.length : 0
            sortBy: root.sortBy
            searchText: root.searchText
            selectionMode: root.selectionMode

            onSortSelected: function(value) {
                root.sortSelected(value)
            }
            onSearchChanged: function(value) {
                root.searchQueryChanged(value)
            }
            onSelectionModeToggled: {
                root.selectionMode = !root.selectionMode
                if (!root.selectionMode) {
                    root.selectedForPlaylist = []
                }
            }
        }

        Comp.SelectionModeBar {
            visible: root.selectionMode
            Layout.fillWidth: true
            Layout.leftMargin: Theme.spaceSm
            Layout.rightMargin: Theme.spaceSm
            Layout.bottomMargin: Theme.spaceSm

            selectedCount: root.selectedForPlaylist.length
            totalCount: root.backend ? root.backend.wallpapers.length : 0
            playlists: root.backend ? root.backend.playlists : []

            onSelectAllRequested: {
                var pageItems = root.currentGridWallpapers()
                var ids = []
                for (var i = 0; i < pageItems.length; i++) ids.push(pageItems[i].id)
                root.selectedForPlaylist = ids
            }
            onDeselectRequested: {
                root.selectedForPlaylist = []
            }
            onCancelRequested: {
                root.selectionMode = false
                root.selectedForPlaylist = []
            }
            onAddToPlaylistRequested: function(playlistId) {
                if (!root.backend) return
                for (var i = 0; i < root.selectedForPlaylist.length; i++) {
                    root.backend.addToPlaylist(playlistId, root.selectedForPlaylist[i])
                }
                root.selectionMode = false
                root.selectedForPlaylist = []
            }
            onCreatePlaylistFromSelectionRequested: {
                if (!root.backend || root.selectedForPlaylist.length === 0) return
                var name = "Playlist " + (root.backend.playlists.length + 1)
                root.backend.createPlaylist(name)
                var playlists = root.backend.playlists
                var newId = ""
                for (var i = 0; i < playlists.length; i++) {
                    if (playlists[i].name === name) {
                        newId = playlists[i].id
                        break
                    }
                }
                if (newId.length > 0) {
                    for (var j = 0; j < root.selectedForPlaylist.length; j++) {
                        root.backend.addToPlaylist(newId, root.selectedForPlaylist[j])
                    }
                }
                root.selectionMode = false
                root.selectedForPlaylist = []
            }
        }

        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Theme.divider
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.margins: Theme.spaceSm

            SplitView {
                anchors.fill: parent
                orientation: Qt.Horizontal

                Comp.PlaylistPanel {
                    id: playlistPanel
                    SplitView.preferredWidth: panelState === "locked" ? 268 : 48
                    SplitView.minimumWidth: panelState === "locked" ? 260 : 48
                    SplitView.maximumWidth: panelState === "locked" ? 280 : 48

                    playlists: root.backend ? root.backend.playlists : []
                    activePlaylistId: root.backend ? root.backend.activePlaylistId : ""
                    favoriteIds: root.backend ? root.backend.favoriteIds : []

                    onActivePlaylistChanged: function(playlistId) {
                        if (root.backend) root.backend.setActivePlaylist(playlistId)
                    }
                    onActivePlaylistCleared: {
                        if (root.backend) root.backend.clearActivePlaylist()
                    }
                    onCreatePlaylistRequested: function(name) {
                        if (root.backend) root.backend.createPlaylist(name)
                    }
                    onRenamePlaylistRequested: function(playlistId, playlistName) {
                        if (root.backend) root.backend.renamePlaylist(playlistId, playlistName)
                    }
                    onDeletePlaylistRequested: function(playlistId) {
                        if (root.backend) root.backend.deletePlaylist(playlistId)
                    }

                    onPanelStateChanged: {
                        root.playlistFloatingStateChanged(panelState === "floating")
                    }
                }

                Comp.WallpaperGrid {
                    SplitView.fillWidth: true
                    SplitView.minimumWidth: 520

                    wallpapers: root.currentGridWallpapers()
                    playlists: root.backend ? root.backend.playlists : []
                    activePlaylistId: root.backend ? root.backend.activePlaylistId : ""
                    selectedId: root.backend ? root.backend.selectedId : ""
                    columns: width >= 1400 ? 6 : (width >= 1100 ? 5 : (width >= 800 ? 4 : 3))
                    searchText: root.searchText
                    sortBy: root.sortBy
                    selectionMode: root.selectionMode
                    selectedForPlaylist: root.selectedForPlaylist

                    onSelectRequested: function(wallpaperId) {
                        if (root.backend) root.backend.selectWallpaper(wallpaperId)
                    }
                    onApplyRequested: function(wallpaperId) {
                        if (root.backend) root.backend.applyWallpaper(wallpaperId)
                    }
                    onFavoriteToggled: function(wallpaperId) {
                        if (root.backend) root.backend.toggleFavorite(wallpaperId)
                    }
                    onStopRequested: function(wallpaperId) {
                        if (root.backend) root.backend.stopWallpaper()
                    }
                    onOpenFolderRequested: function(wallpaperId) {
                        if (!root.backend) return
                        var targetPath = ""
                        for (var i = 0; i < root.backend.wallpapers.length; i++) {
                            if (root.backend.wallpapers[i].id === wallpaperId) {
                                targetPath = root.backend.wallpapers[i].path || ""
                                break
                            }
                        }
                        root.backend.openFolder(targetPath)
                    }
                    onDeleteRequested: function(wallpaperId) {
                        if (!root.backend) return
                        var targetPath = ""
                        var targetTitle = wallpaperId
                        for (var i = 0; i < root.backend.wallpapers.length; i++) {
                            if (root.backend.wallpapers[i].id === wallpaperId) {
                                targetPath = root.backend.wallpapers[i].path || ""
                                targetTitle = root.backend.wallpapers[i].title || wallpaperId
                                break
                            }
                        }
                        root.deleteWallpaperId = wallpaperId
                        root.deleteWallpaperTitle = targetTitle
                        root.deleteWallpaperPath = targetPath
                        root.deleteDialogOpen = true
                    }
                    onEditNicknameRequested: function(wallpaperId, nickname) {
                        if (root.backend) root.backend.setWallpaperNickname(wallpaperId, nickname)
                    }
                    onAddToPlaylistRequested: function(wallpaperId, playlistId) {
                        if (root.backend) root.backend.addToPlaylist(playlistId, wallpaperId)
                    }
                    onCopyIdRequested: function(wallpaperId) {
                        if (root.backend) root.backend.copyTextToClipboard(wallpaperId)
                    }
                    onWorkshopRequested: function(wallpaperId) {
                        if (root.backend) root.backend.openWorkshopForWallpaper(wallpaperId)
                    }
                    onSelectionToggled: function(wallpaperId) {
                        root.toggleSelection(wallpaperId)
                    }
                    onConfigurePathRequested: {
                        window.currentPage = "settings"
                    }
                    onBrowseAllRequested: {
                        if (root.backend) root.backend.clearActivePlaylist()
                    }
                }

                Comp.WallpaperSidebar {
                    SplitView.preferredWidth: Theme.sidebarWidth
                    SplitView.minimumWidth: 300
                    SplitView.maximumWidth: 520

                    backend: root.backend
                    wallpaper: root.backend ? root.backend.selectedWallpaper : ({})
                    originalTitle: root.backend ? root.backend.selectedOriginalTitle : ""

                    onApplyRequested: function(wallpaperId) {
                        if (root.backend) root.backend.applyWallpaper(wallpaperId)
                    }
                    onFavoriteToggled: function(wallpaperId) {
                        if (root.backend) root.backend.toggleFavorite(wallpaperId)
                    }
                    onNicknameEditRequested: function(wallpaperId, nickname) {
                        if (root.backend) root.backend.setWallpaperNickname(wallpaperId, nickname)
                    }
                }
            }

            Rectangle {
                anchors.fill: parent
                visible: root.playlistFloatingOpen
                color: Theme.overlayDim
                z: 15

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        if (playlistPanel.panelState === "floating") {
                            playlistPanel.panelState = "minimized"
                        }
                    }
                }
            }

            Comp.LibraryPagination {
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.bottomMargin: Theme.spaceSm
                width: 360

                currentPage: root.currentPage
                totalPages: root.totalPages()

                onPageChangedByUser: function(page) {
                    root.currentPage = page
                }
            }
        }
    }

    Comp.HistoryDialog {
        id: historyDialog
        backend: root.backend
        visible: root.historyDialogOpen
        onVisibleChanged: if (!visible) root.historyDialogOpen = false
        onClosed: root.historyDialogOpen = false
        onRejected: root.historyDialogOpen = false
        onAccepted: root.historyDialogOpen = false
    }

    Comp.DeleteConfirmDialog {
        id: deleteDialog
        visible: root.deleteDialogOpen
        wallpaperId: root.deleteWallpaperId
        wallpaperTitle: root.deleteWallpaperTitle
        wallpaperPath: root.deleteWallpaperPath
        onConfirmDelete: function(wallpaperId, wallpaperPath) {
            if (root.backend) root.backend.removeWallpaper(wallpaperId, wallpaperPath)
            root.deleteDialogOpen = false
        }
        onClosed: root.deleteDialogOpen = false
        onRejected: root.deleteDialogOpen = false
        onAccepted: root.deleteDialogOpen = false
    }
}