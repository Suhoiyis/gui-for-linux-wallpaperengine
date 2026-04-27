import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../effects" as Effects
import "../Theme.js" as Theme

Rectangle {
    id: root

    property var screens: []
    property var backend
    property string selectedScreen: ""
    property bool linkedMode: false
    property string currentPage: "library"

    signal selectedScreenChangedByUser(string screen)
    signal linkedModeChangedByUser(bool linked)
    signal pageChanged(string page)
    signal appMenuHistoryRequested()
    signal appMenuAboutRequested()
    signal appMenuUpdateRequested()
    signal appMenuWelcomeRequested()
    signal appMenuQuitRequested()
    signal commandPaletteRequested()

    color: Theme.surface
    border.width: 1
    border.color: Theme.border
    radius: Theme.radiusXl
    height: Theme.navHeight

    Effects.GDropShadow {
        shadowWidth: root.width
        shadowHeight: root.height
        radius: root.radius
        color: Theme.withAlpha("#000000", 0.10)
        spread: 3
        verticalOffset: 1
    }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: Theme.spaceMd
        anchors.rightMargin: Theme.spaceMd
        spacing: Theme.spaceSm

        // === LEFT SIDE ===

        // Compact mode button
        Ctrl.GIconButton {
            iconName: "minimize2"
            size: Theme.navHeight - Theme.spaceMd * 2
            tooltip: "Compact Mode"
            onClicked: root.pageChanged("compact")
        }

        // Tab group: Library / Monitor / Settings
        Rectangle {
            radius: Theme.radiusMd
            color: Theme.elevated
            border.width: 1
            border.color: Theme.border
            implicitHeight: Theme.navHeight - Theme.spaceMd * 2

            RowLayout {
                anchors.fill: parent
                anchors.margins: Theme.spaceXs
                spacing: Theme.spaceXs

                Ctrl.GButton {
                    text: "Library"
                    iconName: "image"
                    variant: root.currentPage === "library" ? "default" : "ghost"
                    sizeVariant: "sm"
                    onClicked: root.pageChanged("library")
                }
                Ctrl.GButton {
                    text: "Monitor"
                    iconName: "activity"
                    variant: root.currentPage === "performance" ? "default" : "ghost"
                    sizeVariant: "sm"
                    onClicked: root.pageChanged("performance")
                }
                Ctrl.GButton {
                    text: "Settings"
                    iconName: "settings"
                    variant: root.currentPage === "settings" ? "default" : "ghost"
                    sizeVariant: "sm"
                    onClicked: root.pageChanged("settings")
                }
            }
        }

        // Search box with Ctrl+K hint
        Rectangle {
            Layout.fillWidth: true
            Layout.minimumWidth: 200
            Layout.maximumWidth: 300
            radius: Theme.radiusMd
            color: Theme.input
            border.width: 1
            border.color: Theme.border
            implicitHeight: Theme.navHeight - Theme.spaceMd * 2

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: Theme.spaceSm
                anchors.rightMargin: Theme.spaceSm
                spacing: Theme.spaceSm

                Ctrl.GIcon {
                    name: "search"
                    size: Theme.fontSizeMd
                    color: Theme.fgSubtle
                }

                Text {
                    text: "Search..."
                    color: Theme.fgSubtle
                    font.pixelSize: Theme.fontSizeSm
                    Layout.fillWidth: true
                    verticalAlignment: Text.AlignVCenter
                }

                Rectangle {
                    radius: Theme.radiusSm
                    color: Theme.elevated
                    border.width: 1
                    border.color: Theme.border
                    implicitHeight: 18
                    implicitWidth: 40

                    Text {
                        anchors.centerIn: parent
                        text: "Ctrl+K"
                        color: Theme.fgSubtle
                        font.pixelSize: Theme.fontSizeXs - 2
                    }
                }
            }

            MouseArea {
                anchors.fill: parent
                onClicked: root.commandPaletteRequested()
            }
        }

        // === RIGHT SIDE: Action button group ===

        Rectangle {
            radius: Theme.radiusMd
            color: Theme.elevated
            border.width: 1
            border.color: Theme.border
            implicitHeight: Theme.navHeight - Theme.spaceMd * 2

            RowLayout {
                anchors.fill: parent
                anchors.margins: Theme.spaceXs
                spacing: Theme.spaceXs

                // Screen selector
                Ctrl.GComboBox {
                    id: screenCombo
                    model: root.screens
                    implicitWidth: 120

                    Component.onCompleted: {
                        var idx = root.screens.indexOf(root.selectedScreen)
                        currentIndex = idx >= 0 ? idx : 0
                    }

                    onActivated: {
                        if (currentIndex >= 0 && currentIndex < root.screens.length) {
                            root.selectedScreenChangedByUser(root.screens[currentIndex])
                        }
                    }

                    Connections {
                        target: root
                        function onSelectedScreenChanged() {
                            var idx = root.screens.indexOf(root.selectedScreen)
                            if (idx >= 0) screenCombo.currentIndex = idx
                        }
                    }
                }

                // Separator
                Rectangle {
                    width: 1
                    height: 16
                    color: Theme.border
                }

                // Stop button
                Ctrl.GIconButton {
                    iconName: "square"
                    variant: "destructive"
                    size: 28
                    tooltip: "Stop"
                    onClicked: if (root.backend) root.backend.stopWallpaper()
                }

                // Shuffle button
                Ctrl.GIconButton {
                    iconName: "shuffle"
                    size: 28
                    tooltip: "Shuffle"
                    onClicked: if (root.backend) root.backend.applyRandomWallpaper()
                }

                // Screenshot button
                Ctrl.GIconButton {
                    iconName: "camera"
                    size: 28
                    tooltip: "Screenshot"
                    onClicked: {
                        if (!root.backend) return
                        var targetId = root.backend.selectedId || ""
                        if (targetId.length > 0) root.backend.takeScreenshot(targetId)
                    }
                }

                // Separator
                Rectangle {
                    width: 1
                    height: 16
                    color: Theme.border
                }

                AppMenu {
                    backend: root.backend
                    onShowHistoryRequested: root.appMenuHistoryRequested()
                    onShowAboutRequested: root.appMenuAboutRequested()
                    onShowUpdateRequested: root.appMenuUpdateRequested()
                    onShowWelcomeRequested: root.appMenuWelcomeRequested()
                    onRequestQuitConfirm: root.appMenuQuitRequested()
                }
            }
        }
    }
}
