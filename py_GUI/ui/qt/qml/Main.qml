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
    property string currentPage: "library"
    
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        
        Comp.NavBar {
            Layout.fillWidth: true
            Layout.margins: 10

            screens: Backend.screens
            selectedScreen: Backend.selectedScreen
            linkedMode: Backend.linkedMode
            currentPage: window.currentPage

            onSelectedScreenChangedByUser: function(screen) {
                Backend.setSelectedScreen(screen)
            }
            onLinkedModeChangedByUser: function(linked) {
                Backend.setLinkedMode(linked)
            }
            onPageChanged: function(page) {
                window.currentPage = page
            }
        }

        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: {
                if (window.currentPage === "performance") return 1
                if (window.currentPage === "settings") return 2
                return 0
            }

            Comp.LibraryPage {
                backend: Backend
                sortBy: window.sortBy
                searchText: window.searchText
                playlistFloatingOpen: window.playlistFloatingOpen

                onSortSelected: function(value) {
                    window.sortBy = value
                }
                onSearchQueryChanged: function(value) {
                    window.searchText = value
                }
                onRefreshRequested: {
                    Backend.refresh()
                }
                onPlaylistFloatingStateChanged: function(opened) {
                    window.playlistFloatingOpen = opened
                }
            }

            Rectangle {
                color: "#1a1b26"
                Label {
                    anchors.centerIn: parent
                    text: "Performance page (WIP)"
                    color: "#8a90b8"
                }
            }

            Rectangle {
                color: "#1a1b26"
                Label {
                    anchors.centerIn: parent
                    text: "Settings page (WIP)"
                    color: "#8a90b8"
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
