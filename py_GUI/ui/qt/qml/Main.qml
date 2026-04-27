// Main.qml - 主窗口
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components" as Comp
import "controls" as Ctrl
import "Theme.js" as Theme

ApplicationWindow {
    id: window
    visible: true
    width: 1200
    height: 800
    title: "LWG Qt Quick PoC"

    color: Theme.bg

    property string sortBy: "name"
    property string searchText: ""
    property bool playlistFloatingOpen: false
    property string currentPage: "library"
    property var backendRef: Backend
    property string layoutMode: window.width < Theme.breakpointCompact ? "compact"
                               : window.width < Theme.breakpointNormal ? "normal"
                               : "wide"
    property bool showAboutDialog: false
    property bool showUpdateDialog: false
    property bool showWelcomeDialog: false
    property bool showHistoryDialog: false
    property bool showQuitConfirm: false

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        Comp.NavBar {
            Layout.fillWidth: true
            Layout.margins: Theme.spaceSm

            screens: window.backendRef ? window.backendRef.screens : []
            selectedScreen: window.backendRef ? window.backendRef.selectedScreen : ""
            linkedMode: window.backendRef ? window.backendRef.linkedMode : false
            currentPage: window.currentPage
            backend: window.backendRef

            onSelectedScreenChangedByUser: function(screen) {
                if (window.backendRef) window.backendRef.setSelectedScreen(screen)
            }
            onLinkedModeChangedByUser: function(linked) {
                if (window.backendRef) window.backendRef.setLinkedMode(linked)
            }
            onPageChanged: function(page) {
                window.currentPage = page
            }
            onCommandPaletteRequested: commandPalette.open()
            onAppMenuHistoryRequested: window.showHistoryDialog = true
            onAppMenuAboutRequested: window.showAboutDialog = true
            onAppMenuUpdateRequested: {
                if (window.backendRef) {
                    var info = window.backendRef.checkForUpdates()
                    if (info && info.hasUpdate) {
                        updateDialog.latestVersion = info.latestVersion || window.backendRef.appVersion
                        updateDialog.downloadUrl = info.downloadUrl || "https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases"
                    } else {
                        updateDialog.latestVersion = window.backendRef.appVersion
                        updateDialog.downloadUrl = "https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases"
                    }
                }
                window.showUpdateDialog = true
            }
            onAppMenuWelcomeRequested: window.showWelcomeDialog = true
            onAppMenuQuitRequested: window.showQuitConfirm = true
        }

        StackLayout {
            id: pageStack
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: {
                if (window.currentPage === "performance") return 1
                if (window.currentPage === "settings") return 2
                if (window.currentPage === "compact") return 3
                return 0
            }

            Comp.LibraryPage {
                id: libraryPage
                backend: window.backendRef
                sortBy: window.sortBy
                searchText: window.searchText
                playlistFloatingOpen: window.playlistFloatingOpen

                opacity: pageStack.currentIndex === 0 ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: Theme.pageTransitionMs; easing.type: Easing.OutCubic } }

                onSortSelected: function(value) {
                    window.sortBy = value
                }
                onSearchQueryChanged: function(value) {
                    window.searchText = value
                }
                onRefreshRequested: {
                    if (window.backendRef) window.backendRef.refresh()
                }
                onPlaylistFloatingStateChanged: function(opened) {
                    window.playlistFloatingOpen = opened
                }
            }

            Comp.PerformancePage {
                id: performancePage
                backend: window.backendRef

                opacity: pageStack.currentIndex === 1 ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: Theme.pageTransitionMs; easing.type: Easing.OutCubic } }
            }

            Comp.SettingsPage {
                id: settingsPage
                backend: window.backendRef

                opacity: pageStack.currentIndex === 2 ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: Theme.pageTransitionMs; easing.type: Easing.OutCubic } }
            }

            Comp.CompactPage {
                id: compactPage
                backend: window.backendRef

                opacity: pageStack.currentIndex === 3 ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: Theme.pageTransitionMs; easing.type: Easing.OutCubic } }

                onSwitchToNormal: function() {
                    window.currentPage = "library"
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            height: 40
            color: Theme.statusBarBg

            Label {
                anchors.centerIn: parent
                text: (window.backendRef && window.backendRef.statusMessage.length > 0)
                    ? window.backendRef.statusMessage
                    : (window.backendRef && window.backendRef.selectedId
                       ? "Selected: " + window.backendRef.selectedId
                       : "Click a wallpaper to select")
                color: Theme.fgMuted
            }
        }
    }

    Comp.ToastManager {
        id: toastManager
        anchors.fill: parent
        z: 1000
    }

    Connections {
        target: window.backendRef
        function onStatusMessageChanged() {
            if (window.backendRef && window.backendRef.statusMessage && window.backendRef.statusMessage.length > 0) {
                toastManager.show(window.backendRef.statusMessage)
            }
        }
    }

    Shortcut {
        sequences: ["Ctrl+K", "Meta+K"]
        onActivated: commandPalette.open()
    }

    Comp.AboutDialog {
        backend: window.backendRef
        visible: window.showAboutDialog
        onClosed: window.showAboutDialog = false
    }

    Comp.UpdateDialog {
        id: updateDialog
        backend: window.backendRef
        currentVersion: window.backendRef ? window.backendRef.appVersion : "unknown"
        latestVersion: window.backendRef ? window.backendRef.appVersion : "unknown"
        downloadUrl: "https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases"
        visible: window.showUpdateDialog
        onClosed: window.showUpdateDialog = false
    }

    Comp.WelcomeDialog {
        backend: window.backendRef
        requiredMode: window.backendRef ? !window.backendRef.onboardingCompleted : false
        visible: window.showWelcomeDialog || (window.backendRef ? !window.backendRef.onboardingCompleted : false)
        onClosed: window.showWelcomeDialog = false
    }

    Comp.HistoryDialog {
        backend: window.backendRef
        visible: window.showHistoryDialog
        onClosed: window.showHistoryDialog = false
    }

    Comp.CommandPalette {
        id: commandPalette
        backend: window.backendRef
        function pageChangedByPalette(page) {
            window.currentPage = page
        }
    }

    Dialog {
        id: quitConfirm
        visible: window.showQuitConfirm
        modal: true
        title: "Quit Application?"
        width: 400
        standardButtons: Dialog.Ok | Dialog.Cancel
        onAccepted: Qt.quit()
        onRejected: window.showQuitConfirm = false
        onClosed: window.showQuitConfirm = false
        background: Rectangle {
            radius: Theme.radiusXl
            color: Theme.elevated
            border.width: 1
            border.color: Theme.border
        }
        contentItem: Label {
            text: "This will stop wallpapers and close the app."
            color: Theme.fg
            wrapMode: Text.WordWrap
        }
    }
}