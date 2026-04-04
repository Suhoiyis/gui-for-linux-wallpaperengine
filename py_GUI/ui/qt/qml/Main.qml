// Main.qml - 主窗口
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components" as Comp

ApplicationWindow {
    id: window
    visible: true
    width: 1200
    height: 800
    title: "LWG Qt Quick PoC"
    
    color: "#1a1b26"

    property string sortBy: "name"
    property string searchText: ""
    property bool playlistFloatingOpen: false
    
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        
        Comp.NavBar {
            Layout.fillWidth: true
            Layout.margins: 10

            screens: Backend.screens
            selectedScreen: Backend.selectedScreen
            linkedMode: Backend.linkedMode
            currentPage: "library"

            onSelectedScreenChangedByUser: function(screen) {
                Backend.setSelectedScreen(screen)
            }
            onLinkedModeChangedByUser: function(linked) {
                Backend.setLinkedMode(linked)
            }
            onPageChanged: function(_page) {
                // Phase 2 scope: keep library page active.
            }
        }

        Comp.LibraryHeader {
            Layout.fillWidth: true
            Layout.leftMargin: 10
            Layout.rightMargin: 10
            Layout.bottomMargin: 10

            currentTitle: Backend.selectedId.length > 0 ? Backend.selectedId : "None"
            totalCount: Backend.wallpapers.length
            sortBy: window.sortBy
            searchText: window.searchText

            onSortSelected: function(value) {
                window.sortBy = value
            }
            onSearchChanged: function(value) {
                window.searchText = value
            }
            onRefreshRequested: {
                Backend.refresh()
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
                id: contentSplit
                anchors.fill: parent
                orientation: Qt.Horizontal

                Comp.PlaylistPanel {
                    id: playlistPanel
                    SplitView.preferredWidth: panelState === "locked" ? 268 : 48
                    SplitView.minimumWidth: panelState === "locked" ? 260 : 48
                    SplitView.maximumWidth: panelState === "locked" ? 280 : 48

                    playlists: Backend.playlists
                    activePlaylistId: Backend.activePlaylistId
                    favoriteIds: Backend.favoriteIds

                    onActivePlaylistChanged: function(playlistId) {
                        Backend.setActivePlaylist(playlistId)
                    }
                    onActivePlaylistCleared: {
                        Backend.clearActivePlaylist()
                    }
                    onCreatePlaylistRequested: function(name) {
                        Backend.createPlaylist(name)
                    }

                    onPanelStateChanged: {
                        window.playlistFloatingOpen = panelState === "floating"
                    }
                }

                Comp.WallpaperGrid {
                    id: wallpaperGrid
                    SplitView.fillWidth: true
                    SplitView.minimumWidth: 520

                    wallpapers: Backend.wallpapers
                    playlists: Backend.playlists
                    activePlaylistId: Backend.activePlaylistId
                    selectedId: Backend.selectedId
                    columns: width >= 1400 ? 6 : (width >= 1100 ? 5 : (width >= 800 ? 4 : 3))
                    searchText: window.searchText
                    sortBy: window.sortBy

                    onSelectRequested: function(wallpaperId) {
                        Backend.selectWallpaper(wallpaperId)
                    }
                    onApplyRequested: function(wallpaperId) {
                        Backend.applyWallpaper(wallpaperId)
                    }
                    onFavoriteToggled: function(wallpaperId) {
                        Backend.toggleFavorite(wallpaperId)
                    }
                }

                Comp.WallpaperSidebar {
                    id: wallpaperSidebar
                    SplitView.preferredWidth: 360
                    SplitView.minimumWidth: 300
                    SplitView.maximumWidth: 520

                    wallpaper: Backend.selectedWallpaper

                    onApplyRequested: function(wallpaperId) {
                        Backend.applyWallpaper(wallpaperId)
                    }
                    onFavoriteToggled: function(wallpaperId) {
                        Backend.toggleFavorite(wallpaperId)
                    }
                }
            }

            Rectangle {
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                visible: window.playlistFloatingOpen
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
        
        Rectangle {
            Layout.fillWidth: true
            height: 40
            color: "#16161e"
            
            Label {
                anchors.centerIn: parent
                text: Backend.statusMessage.length > 0
                    ? Backend.statusMessage
                    : (Backend.selectedId
                       ? "Selected: " + Backend.selectedId
                       : "Click a wallpaper to select")
                color: "#565f89"
            }
        }
    }
}
