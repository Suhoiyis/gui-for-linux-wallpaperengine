import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "." as Comp
import "../controls" as Ctrl
import "../effects" as Effects
import "../Theme.js" as Theme

Item {
    id: root

    property var backend
    property int settingsTabIndex: 0
    property bool showNicknameManager: false
    property bool showFavoriteManager: false
    property string highlightField: ""

    // Auto-clear highlight after 3s
    Timer {
        id: highlightTimer
        interval: 3000
        repeat: false
        onTriggered: root.highlightField = ""
    }

    onHighlightFieldChanged: {
        if (highlightField.length > 0) {
            highlightTimer.restart()
            // Navigate to correct tab based on field name
            if (highlightField === "fps" || highlightField === "scaling" || highlightField === "clamping"
                || highlightField === "cycleEnabled" || highlightField === "cycleInterval"
                || highlightField === "disableParallax" || highlightField === "disableMouse"
                || highlightField === "noFullscreenPause" || highlightField === "disableParticles") {
                root.settingsTabIndex = 0
            } else if (highlightField === "volume" || highlightField === "silence"
                       || highlightField === "noAutomute" || highlightField === "noAudioProcessing") {
                root.settingsTabIndex = 1
            } else if (highlightField === "waylandOnlyActive" || highlightField === "waylandIgnoreAppids") {
                root.settingsTabIndex = 2
            } else {
                // workshopPath, assetsPath, screenshotDelay, screenshotRes, preferXvfb,
                // startHidden, autoRestore, etc. → System & Tools tab
                root.settingsTabIndex = 3
            }
        }
    }

    Rectangle {
        anchors.fill: parent
        color: Theme.bg
        radius: Theme.radiusXl
        border.width: 1
        border.color: Theme.border

        RowLayout {
            anchors.fill: parent
            spacing: 0

            // === LEFT SIDEBAR ===
            Rectangle {
                Layout.preferredWidth: 256
                color: Theme.surface
                border.width: 0
                border.color: Theme.border

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 0

                    // Title
                    RowLayout {
                        Layout.topMargin: Theme.spaceXl
                        Layout.leftMargin: Theme.spaceMd
                        Layout.rightMargin: Theme.spaceMd
                        Layout.bottomMargin: Theme.spaceMd
                        spacing: Theme.spaceSm

                        Ctrl.GIcon {
                            name: "settings"
                            size: Theme.fontSize2xl
                            color: Theme.fg
                        }

                        Text {
                            text: "Settings"
                            color: Theme.fg
                            font.pixelSize: Theme.fontSize2xl
                            font.weight: Theme.fontWeightBold
                        }
                    }

                    // Nav buttons
                    ColumnLayout {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        Layout.leftMargin: Theme.spaceSm
                        Layout.rightMargin: Theme.spaceSm
                        spacing: Theme.spaceXs

                        Repeater {
                            model: [
                                { label: "Playback & Perf", desc: "FPS, Cycling, Interaction", icon: "play", tab: 0 },
                                { label: "Audio & Display", desc: "Monitor, Theme, Volume", icon: "volume2", tab: 1 },
                                { label: "System & Tools", desc: "Paths, Root, Autostart", icon: "zap", tab: 2 },
                                { label: "Log Monitor", desc: "Debug & Filters", icon: "list", tab: 3 }
                            ]
                            delegate: Rectangle {
                                required property var modelData
                                Layout.fillWidth: true
                                height: 56
                                radius: Theme.radiusMd
                                color: root.settingsTabIndex === modelData.tab ? Theme.elevated : "transparent"
                                border.width: 0

                                // Active indicator bar
                                Rectangle {
                                    visible: root.settingsTabIndex === modelData.tab
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    width: 3
                                    height: parent.height * 0.4
                                    radius: 1.5
                                    color: Theme.brand
                                }

                                RowLayout {
                                    anchors.fill: parent
                                    anchors.leftMargin: Theme.spaceMd
                                    anchors.rightMargin: Theme.spaceSm
                                    spacing: Theme.spaceSm

                                    Rectangle {
                                        radius: Theme.radiusSm
                                        color: root.settingsTabIndex === modelData.tab ? Theme.brand : Theme.overlay
                                        width: 32
                                        height: 32

                                        Ctrl.GIcon {
                                            name: modelData.icon
                                            size: Theme.fontSizeSm
                                            color: root.settingsTabIndex === modelData.tab ? Theme.brandFg : Theme.fgMuted
                                            anchors.centerIn: parent
                                        }
                                    }

                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        spacing: 0

                                        Text {
                                            text: modelData.label
                                            color: root.settingsTabIndex === modelData.tab ? Theme.fg : Theme.fgMuted
                                            font.pixelSize: Theme.fontSizeSm
                                            font.weight: root.settingsTabIndex === modelData.tab ? Theme.fontWeightMedium : Theme.fontWeightNormal
                                        }

                                        Text {
                                            text: modelData.desc
                                            color: Theme.fgSubtle
                                            font.pixelSize: Theme.fontSizeXs
                                        }
                                    }
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: root.settingsTabIndex = modelData.tab
                                }
                            }
                        }
                    }

                    // Bottom action buttons
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 120
                        color: Theme.withAlpha(Theme.bg, 0.5)
                        border.width: 1
                        border.color: Theme.border

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: Theme.spaceMd
                            spacing: Theme.spaceSm

                            Ctrl.GButton {
                                Layout.fillWidth: true
                                text: "Save Changes"
                                iconName: "check"
                                onClicked: {
                                    if (root.backend) root.backend.saveSettings()
                                }
                            }

                            RowLayout {
                                Layout.fillWidth: true
                                spacing: Theme.spaceSm

                                Ctrl.GButton {
                                    Layout.fillWidth: true
                                    text: "Reload"
                                    iconName: "edit3"
                                    variant: "outline"
                                    onClicked: {
                                        if (root.backend) root.backend.restartWallpapers()
                                    }
                                }

                                Ctrl.GButton {
                                    Layout.fillWidth: true
                                    text: "Stop"
                                    iconName: "square"
                                    variant: "destructive"
                                    onClicked: {
                                        if (root.backend) root.backend.stopWallpaper()
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // === RIGHT CONTENT AREA ===
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: Theme.bg

                StackLayout {
                    anchors.fill: parent
                    anchors.margins: Theme.spaceXl
                    currentIndex: root.settingsTabIndex

                    ScrollView {
                        clip: true
                        contentWidth: availableWidth
                        ColumnLayout {
                            width: parent.width
                            spacing: Theme.spaceSm
                            Comp.PlaybackSettings {
                                Layout.fillWidth: true
                                backend: root.backend
                            }
                            Comp.CycleSettings {
                                Layout.fillWidth: true
                                backend: root.backend
                            }
                        }
                    }

                    ScrollView {
                        clip: true
                        contentWidth: availableWidth
                        Comp.AudioSettings {
                            width: parent.width
                            backend: root.backend
                        }
                    }

                    ScrollView {
                        clip: true
                        contentWidth: availableWidth
                        Comp.WaylandSettings {
                            width: parent.width
                            backend: root.backend
                        }
                    }

                    ScrollView {
                        clip: true
                        contentWidth: availableWidth
                        ColumnLayout {
                            width: parent.width
                            spacing: Theme.spaceSm
                            Comp.SystemSettings {
                                Layout.fillWidth: true
                                backend: root.backend
                            }
                            Comp.LogViewer {
                                Layout.fillWidth: true
                                backend: root.backend
                            }
                            RowLayout {
                                Layout.fillWidth: true
                                Item { Layout.fillWidth: true }
                                Ctrl.GButton {
                                    text: "Manage Nicknames"
                                    iconName: "edit3"
                                    variant: "outline"
                                    onClicked: root.showNicknameManager = true
                                }
                                Ctrl.GButton {
                                    text: "Manage Favorites"
                                    iconName: "star"
                                    variant: "outline"
                                    onClicked: root.showFavoriteManager = true
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    Comp.NicknameManagerDialog {
        backend: root.backend
        visible: root.showNicknameManager
        onClosed: root.showNicknameManager = false
    }

    Comp.FavoriteManagerDialog {
        backend: root.backend
        visible: root.showFavoriteManager
        onClosed: root.showFavoriteManager = false
    }
}
