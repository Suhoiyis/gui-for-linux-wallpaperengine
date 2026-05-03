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
    property var themeBridge
    property int settingsTabIndex: 0
    property bool showNicknameManager: false
    property bool showFavoriteManager: false
    property string highlightField: ""

    // Local color alias — uses themeBridge when available, falls back to dark Theme
    property var tb: themeBridge || null

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
        color: tb ? tb.cBg : Theme.bg
        radius: Theme.radiusXl
        border.width: 0

        RowLayout {
            anchors.fill: parent
            spacing: 0

            // === LEFT SIDEBAR ===
            Rectangle {
                Layout.preferredWidth: 256
                color: tb ? tb.cSurface : Theme.surface
                border.width: 0
                border.color: tb ? tb.cBorder : Theme.border

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
                            color: tb ? tb.cFg : Theme.fg
                        }

                        Text {
                            text: "Settings"
                            color: tb ? tb.cFg : Theme.fg
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
                                color: root.settingsTabIndex === modelData.tab ? (tb ? tb.cElevated : Theme.elevated) : "transparent"
                                border.width: 0

                                // Active indicator bar
                                Rectangle {
                                    visible: root.settingsTabIndex === modelData.tab
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    width: 3
                                    height: parent.height * 0.4
                                    radius: 1.5
                                    color: tb ? tb.cBrand : Theme.brand
                                }

                                RowLayout {
                                    anchors.fill: parent
                                    anchors.leftMargin: Theme.spaceMd
                                    anchors.rightMargin: Theme.spaceSm
                                    spacing: Theme.spaceSm

                                    Rectangle {
                                        radius: Theme.radiusSm
                                        color: root.settingsTabIndex === modelData.tab ? (tb ? tb.cBrand : Theme.brand) : (tb ? tb.cOverlay : Theme.overlay)
                                        width: 32
                                        height: 32

                                        Ctrl.GIcon {
                                            name: modelData.icon
                                            size: Theme.fontSizeSm
                                            color: root.settingsTabIndex === modelData.tab ? (tb ? tb.cBrandFg : Theme.brandFg) : (tb ? tb.cFgMuted : Theme.fgMuted)
                                            anchors.centerIn: parent
                                        }
                                    }

                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        spacing: 0

                                        Text {
                                            text: modelData.label
                                            color: root.settingsTabIndex === modelData.tab ? (tb ? tb.cFg : Theme.fg) : (tb ? tb.cFgMuted : Theme.fgMuted)
                                            font.pixelSize: Theme.fontSizeSm
                                            font.weight: root.settingsTabIndex === modelData.tab ? Theme.fontWeightMedium : Theme.fontWeightNormal
                                        }

                                        Text {
                                            text: modelData.desc
                                            color: tb ? tb.cFgSubtle : Theme.fgSubtle
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
                        color: tb ? Theme.withAlpha(tb.cBg, 0.5) : Theme.withAlpha(Theme.bg, 0.5)
                        border.width: 0

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: Theme.spaceMd
                            spacing: Theme.spaceSm

                            Ctrl.GButton {
                                themeBridge: root.themeBridge
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
                                    themeBridge: root.themeBridge
                                    Layout.fillWidth: true
                                    text: "Reload"
                                    iconName: "edit3"
                                    variant: "outline"
                                    onClicked: {
                                        if (root.backend) root.backend.restartWallpapers()
                                    }
                                }

                                Ctrl.GButton {
                                    themeBridge: root.themeBridge
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
                color: tb ? tb.cBg : Theme.bg

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
                                themeBridge: root.themeBridge
                            }
                            Comp.CycleSettings {
                                Layout.fillWidth: true
                                backend: root.backend
                                themeBridge: root.themeBridge
                            }
                        }
                    }

                    ScrollView {
                        clip: true
                        contentWidth: availableWidth
                        Comp.AudioSettings {
                            width: parent.width
                            backend: root.backend
                            themeBridge: root.themeBridge
                        }
                    }

                    ScrollView {
                        clip: true
                        contentWidth: availableWidth
                        Comp.WaylandSettings {
                            width: parent.width
                            backend: root.backend
                            themeBridge: root.themeBridge
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
                                themeBridge: root.themeBridge
                            }
                            Comp.LogViewer {
                                Layout.fillWidth: true
                                backend: root.backend
                                themeBridge: root.themeBridge
                            }
                            RowLayout {
                                Layout.fillWidth: true
                                Item { Layout.fillWidth: true }
                                Ctrl.GButton {
                                    themeBridge: root.themeBridge
                                    text: "Manage Nicknames"
                                    iconName: "edit3"
                                    variant: "outline"
                                    onClicked: root.showNicknameManager = true
                                }
                                Ctrl.GButton {
                                    themeBridge: root.themeBridge
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
        themeBridge: root.themeBridge
        visible: root.showNicknameManager
        onClosed: root.showNicknameManager = false
    }

    Comp.FavoriteManagerDialog {
        backend: root.backend
        themeBridge: root.themeBridge
        visible: root.showFavoriteManager
        onClosed: root.showFavoriteManager = false
    }
}