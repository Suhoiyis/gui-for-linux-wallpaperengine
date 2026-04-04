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
    
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        
        Comp.LibraryHeader {
            Layout.fillWidth: true
            Layout.margins: 10

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
        
        SplitView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.margins: 10
            orientation: Qt.Horizontal

            Comp.WallpaperGrid {
                id: wallpaperGrid
                SplitView.fillWidth: true
                SplitView.minimumWidth: 520

                wallpapers: Backend.wallpapers
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
