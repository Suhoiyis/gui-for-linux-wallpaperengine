import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../Theme.js" as Theme

Frame {
    id: root

    property var backend
    property var themeBridge

    background: Rectangle {
        color: root.themeBridge ? root.themeBridge.cElevated : Theme.elevated
        radius: Theme.radiusXl
        border.width: 1
        border.color: root.themeBridge ? root.themeBridge.cBorder : Theme.border
    }
    padding: Theme.spaceMd

    Timer {
        id: volumeDebounce
        interval: 500
        repeat: false
        onTriggered: if (root.backend) root.backend.setVolume(Math.round(volumeSlider.value))
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceSm

        Label {
            text: "Audio & Display"
            color: root.themeBridge ? root.themeBridge.cTextSection : Theme.textSection
            font.pixelSize: Theme.fontSizeMd
            font.bold: true
        }

        // ── Theme toggle ──
        RowLayout {
            Layout.fillWidth: true
            spacing: Theme.spaceSm

            Ctrl.GIcon {
                name: root.themeBridge && root.themeBridge.resolvedMode === "light" ? "sun" : "moon"
                size: Theme.fontSizeLg
                color: root.themeBridge ? root.themeBridge.cFg : Theme.fg
            }

            ColumnLayout {
                Layout.fillWidth: true
                spacing: 0

                Label {
                    text: "Interface Theme"
                    color: root.themeBridge ? root.themeBridge.cFg : Theme.fg
                    font.pixelSize: Theme.fontSizeSm
                    font.weight: Theme.fontWeightMedium
                }
                Label {
                    text: "Light or Dark mode"
                    color: root.themeBridge ? root.themeBridge.cFgSubtle : Theme.fgSubtle
                    font.pixelSize: Theme.fontSizeXs
                }
            }

            // Three-way animated toggle
            Rectangle {
                id: themeToggle
                Layout.preferredWidth: 260
                Layout.preferredHeight: 36
                radius: Theme.radiusLg
                color: root.themeBridge ? Theme.withAlpha(root.themeBridge.cSurface, 0.80) : Theme.surface80
                border.width: 1
                border.color: root.themeBridge ? Theme.withAlpha(root.themeBridge.cBorder, 0.50) : Theme.withAlpha(Theme.border, 0.50)

                property string currentMode: root.backend ? root.backend.themeMode : "dark"

                // Sliding highlight
                Rectangle {
                    id: toggleHighlight
                    width: (themeToggle.width - 8) / 3
                    height: themeToggle.height - 8
                    radius: Theme.radiusMd
                    color: root.themeBridge ? root.themeBridge.cElevated : Theme.elevated
                    border.width: 1
                    border.color: root.themeBridge ? Theme.withAlpha(root.themeBridge.cBorder, 0.50) : Theme.withAlpha(Theme.border, 0.50)
                    anchors.verticalCenter: parent.verticalCenter
                    y: 4

                    Behavior on x {
                        NumberAnimation { duration: Theme.animNormal; easing.type: Easing.OutCubic }
                    }

                    x: {
                        if (themeToggle.currentMode === "system") return 4
                        if (themeToggle.currentMode === "dark") return 4 + (themeToggle.width - 8) / 3
                        return 4 + 2 * (themeToggle.width - 8) / 3
                    }
                }

                // Three option buttons
                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 4
                    spacing: 0

                    Repeater {
                        model: [
                            { key: "system", icon: "monitor", label: "System" },
                            { key: "dark", icon: "moon", label: "Dark" },
                            { key: "light", icon: "sun", label: "Light" }
                        ]
                        delegate: Item {
                            required property var modelData
                            Layout.fillWidth: true
                            Layout.fillHeight: true

                            RowLayout {
                                anchors.centerIn: parent
                                spacing: Theme.spaceXs

                                Ctrl.GIcon {
                                    name: modelData.icon
                                    size: Theme.fontSizeXs
                                    color: themeToggle.currentMode === modelData.key
                                        ? (root.themeBridge ? root.themeBridge.cFg : Theme.fg)
                                        : (root.themeBridge ? root.themeBridge.cFgSubtle : Theme.fgSubtle)
                                }

                                Label {
                                    text: modelData.label
                                    font.pixelSize: Theme.fontSizeXs
                                    font.weight: themeToggle.currentMode === modelData.key ? Theme.fontWeightMedium : Theme.fontWeightNormal
                                    color: themeToggle.currentMode === modelData.key
                                        ? (root.themeBridge ? root.themeBridge.cFg : Theme.fg)
                                        : (root.themeBridge ? root.themeBridge.cFgSubtle : Theme.fgSubtle)
                                }
                            }

                            MouseArea {
                                anchors.fill: parent
                                onClicked: if (root.backend) root.backend.setThemeMode(modelData.key)
                            }
                        }
                    }
                }
            }
        }

        // ── Separator ──
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 1
            color: root.themeBridge ? root.themeBridge.cDivider : Theme.divider
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Mute Audio"; color: root.themeBridge ? root.themeBridge.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                id: muteSwitch
                checked: root.backend ? root.backend.silence : true
                onToggled: {
                    if (root.backend) root.backend.setSilence(checked)
                    if (root.backend) root.backend.saveSettings()
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            visible: !muteSwitch.checked
            Label { text: "Master Volume"; color: root.themeBridge ? root.themeBridge.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSlider {
                id: volumeSlider
                Layout.fillWidth: true
                from: 0
                to: 100
                stepSize: 1
                value: root.backend ? root.backend.volume : 0
                onMoved: volumeDebounce.restart()
            }
            Label {
                text: String(Math.round(volumeSlider.value)) + "%"
                color: root.themeBridge ? root.themeBridge.cFgMuted : Theme.fgMuted
                Layout.preferredWidth: Theme.spaceXl * 2.3
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Disable Auto Mute"; color: root.themeBridge ? root.themeBridge.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                checked: root.backend ? root.backend.noAutomute : false
                onToggled: {
                    if (root.backend) root.backend.setNoAutomute(checked)
                    if (root.backend) root.backend.saveSettings()
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "No Audio Processing"; color: root.themeBridge ? root.themeBridge.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                checked: root.backend ? root.backend.noAudioProcessing : false
                onToggled: {
                    if (root.backend) root.backend.setNoAudioProcessing(checked)
                    if (root.backend) root.backend.saveSettings()
                }
            }
        }
    }
}