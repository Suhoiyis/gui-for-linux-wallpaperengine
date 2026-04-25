import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme
import "../controls" as Ctrl

Item {
    id: root

    property var backend
    signal showAboutRequested()
    signal showUpdateRequested()
    signal showHistoryRequested()
    signal showWelcomeRequested()
    signal requestQuitConfirm()

    width: Theme.navButtonSize
    height: Theme.navButtonSize

    Ctrl.GIconButton {
        anchors.fill: parent
        text: "☰"
        size: Theme.navButtonSize
        onClicked: menu.popup()
    }

    Menu {
        id: menu
        MenuItem {
            text: "Refresh Library"
            onTriggered: if (root.backend) root.backend.refresh()
        }
        MenuItem {
            text: "Play History"
            onTriggered: root.showHistoryRequested()
        }
        MenuItem {
            text: "Get Started"
            onTriggered: root.showWelcomeRequested()
        }
        MenuSeparator {}
        MenuItem {
            text: "Check for Update"
            onTriggered: root.showUpdateRequested()
        }
        MenuItem {
            text: "About"
            onTriggered: root.showAboutRequested()
        }
        MenuSeparator {}
        MenuItem {
            text: "Restart"
            onTriggered: if (root.backend) root.backend.restartApp()
        }
        MenuItem {
            text: "Quit"
            onTriggered: root.requestQuitConfirm()
        }
    }
}