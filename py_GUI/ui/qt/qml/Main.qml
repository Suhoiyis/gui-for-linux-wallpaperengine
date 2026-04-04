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
    property bool showAboutDialog: false
    property bool showUpdateDialog: false
    property bool showWelcomeDialog: false
    property bool showHistoryDialog: false

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
            onAppMenuHistoryRequested: window.showHistoryDialog = true
            onAppMenuAboutRequested: window.showAboutDialog = true
            onAppMenuUpdateRequested: window.showUpdateDialog = true
            onAppMenuWelcomeRequested: window.showWelcomeDialog = true
        }

        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: {
                if (window.currentPage === "performance") return 1
                if (window.currentPage === "settings") return 2
                if (window.currentPage === "compact") return 3
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

            Comp.PerformancePage {
                backend: Backend
            }

            Comp.SettingsPage {
                backend: Backend
            }

            Comp.CompactPage {
                backend: Backend
                onSwitchToNormal: function() {
                    window.currentPage = "library"
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

    Shortcut {
        sequences: ["Ctrl+K", "Meta+K"]
        onActivated: commandPalette.open()
    }

    Comp.AboutDialog {
        backend: Backend
        visible: window.showAboutDialog
        onClosed: window.showAboutDialog = false
    }

    Comp.UpdateDialog {
        backend: Backend
        currentVersion: Backend.appVersion
        latestVersion: Backend.appVersion
        downloadUrl: "https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases"
        visible: window.showUpdateDialog
        onClosed: window.showUpdateDialog = false
    }

    Comp.WelcomeDialog {
        backend: Backend
        requiredMode: !Backend.onboardingCompleted
        visible: window.showWelcomeDialog || !Backend.onboardingCompleted
        onClosed: window.showWelcomeDialog = false
    }

    Comp.HistoryDialog {
        backend: Backend
        visible: window.showHistoryDialog
        onClosed: window.showHistoryDialog = false
    }

    Comp.CommandPalette {
        id: commandPalette
        backend: Backend
    }
}
