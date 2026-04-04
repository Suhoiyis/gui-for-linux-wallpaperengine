import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "." as Comp

Item {
    id: root

    property var backend
    property string sortBy: "name"
    property string searchText: ""
    property bool playlistFloatingOpen: false

    signal sortSelected(string value)
    signal searchQueryChanged(string value)
    signal refreshRequested()
    signal playlistFloatingStateChanged(bool opened)

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        Comp.LibraryHeader {
            Layout.fillWidth: true
            Layout.leftMargin: 10
            Layout.rightMargin: 10
            Layout.bottomMargin: 10

            currentTitle: root.backend && root.backend.selectedId.length > 0
                ? root.backend.selectedId
                : "None"
            totalCount: root.backend ? root.backend.wallpapers.length : 0
            sortBy: root.sortBy
            searchText: root.searchText

            onSortSelected: function(value) {
                root.sortSelected(value)
            }
            onSearchChanged: function(value) {
                root.searchQueryChanged(value)
            }
            onRefreshRequested: {
                root.refreshRequested()
            }
        }

        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: "#292e42"
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.margins: 10

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

                    wallpapers: root.backend ? root.backend.wallpapers : []
                    playlists: root.backend ? root.backend.playlists : []
                    activePlaylistId: root.backend ? root.backend.activePlaylistId : ""
                    selectedId: root.backend ? root.backend.selectedId : ""
                    columns: width >= 1400 ? 6 : (width >= 1100 ? 5 : (width >= 800 ? 4 : 3))
                    searchText: root.searchText
                    sortBy: root.sortBy

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
                        for (var i = 0; i < root.backend.wallpapers.length; i++) {
                            if (root.backend.wallpapers[i].id === wallpaperId) {
                                targetPath = root.backend.wallpapers[i].path || ""
                                break
                            }
                        }
                        root.backend.removeWallpaper(wallpaperId, targetPath)
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
                }

                Comp.WallpaperSidebar {
                    SplitView.preferredWidth: 360
                    SplitView.minimumWidth: 300
                    SplitView.maximumWidth: 520

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
                color: "#0000000f"
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
        }
    }
}
