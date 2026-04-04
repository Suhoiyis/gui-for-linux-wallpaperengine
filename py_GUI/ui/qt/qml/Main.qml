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
        
        GridView {
            id: gridView
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.margins: 10
            
            model: Backend.wallpapers
            cellWidth: 200
            cellHeight: 220
            
            delegate: Comp.WallpaperCard {
                width: gridView.cellWidth - 10
                height: gridView.cellHeight - 10
                
                wp: model.modelData
                isSelected: Backend.selectedId === model.modelData.id
                
                onSelected: {
                    Backend.selectWallpaper(model.modelData.id)
                }
                onApplyRequested: {
                    Backend.applyWallpaper(model.modelData.id)
                }
                onFavoriteToggled: {
                    Backend.toggleFavorite(model.modelData.id)
                }
            }
            
            ScrollBar.vertical: ScrollBar {}
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
