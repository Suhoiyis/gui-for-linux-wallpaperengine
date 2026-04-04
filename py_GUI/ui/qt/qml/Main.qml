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
    
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        
        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            Layout.margins: 10
            
            Label {
                text: "LWG Qt Quick PoC"
                font.pixelSize: 20
                font.bold: true
                color: "#c0caf5"
            }
            
            Item { Layout.fillWidth: true }
            
            Label {
                text: Backend.wallpapers.length + " wallpapers"
                color: "#565f89"
            }
            
            Button {
                text: "Refresh"
                onClicked: Backend.refresh()
            }
        }
        
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: "#292e42"
        }
        
        Comp.WallpaperGrid {
            id: wallpaperGrid
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.margins: 10

            wallpapers: Backend.wallpapers
            selectedId: Backend.selectedId
            columns: width >= 1400 ? 6 : (width >= 1100 ? 5 : (width >= 800 ? 4 : 3))

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
