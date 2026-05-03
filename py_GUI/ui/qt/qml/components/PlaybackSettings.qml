import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../Theme.js" as Theme

Frame {
    id: root

    property var backend
    property var themeBridge
    property var tb: themeBridge || null

    background: Rectangle {
        color: tb ? tb.cElevated : Theme.elevated
        radius: Theme.radiusXl
        border.width: 0
    }
    padding: Theme.spaceMd

    Timer {
        id: fpsDebounce
        interval: 500
        repeat: false
        onTriggered: if (root.backend) root.backend.setFps(Math.round(fpsSlider.value))
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceSm

        Label {
            text: "Playback & Performance"
            color: tb ? tb.cTextSection : Theme.textSection
            font.pixelSize: Theme.fontSizeMd
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "Target FPS"
                color: tb ? tb.cFg : Theme.fg
                Layout.preferredWidth: Theme.spaceXl * 8.5
            }
            Ctrl.GSlider {
                id: fpsSlider
                Layout.fillWidth: true
                from: 10
                to: 144
                stepSize: 1
                value: root.backend ? root.backend.fps : 30
                onMoved: fpsDebounce.restart()
            }
            Label {
                text: String(Math.round(fpsSlider.value))
                color: tb ? tb.cFgMuted : Theme.fgMuted
                Layout.preferredWidth: Theme.spaceXl * 1.8
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "Scaling"
                color: tb ? tb.cFg : Theme.fg
                Layout.preferredWidth: Theme.spaceXl * 8.5
            }
            Ctrl.GComboBox {
                themeBridge: root.themeBridge
                id: scalingCombo
                Layout.fillWidth: true
                model: ["default", "stretch", "fit", "fill"]
                Component.onCompleted: {
                    if (!root.backend) return
                    var idx = model.indexOf(root.backend.scaling)
                    currentIndex = idx >= 0 ? idx : 0
                }
                onActivated: if (root.backend) root.backend.setScaling(currentText)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "Clamping"
                color: tb ? tb.cFg : Theme.fg
                Layout.preferredWidth: Theme.spaceXl * 8.5
            }
            Ctrl.GComboBox {
                themeBridge: root.themeBridge
                id: clampingCombo
                Layout.fillWidth: true
                model: ["clamp", "border", "repeat"]
                Component.onCompleted: {
                    if (!root.backend) return
                    var idx = model.indexOf(root.backend.clamping)
                    currentIndex = idx >= 0 ? idx : 0
                }
                onActivated: if (root.backend) root.backend.setClamping(currentText)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Disable Parallax"; color: tb ? tb.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                themeBridge: root.themeBridge
                checked: root.backend ? root.backend.disableParallax : false
                onToggled: {
                    if (root.backend) root.backend.setDisableParallax(checked)
                    if (root.backend) root.backend.saveSettings()
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Disable Particles"; color: tb ? tb.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                themeBridge: root.themeBridge
                checked: root.backend ? root.backend.disableParticles : false
                onToggled: {
                    if (root.backend) root.backend.setDisableParticles(checked)
                    if (root.backend) root.backend.saveSettings()
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "No Fullscreen Pause"; color: tb ? tb.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                themeBridge: root.themeBridge
                checked: root.backend ? root.backend.noFullscreenPause : false
                onToggled: {
                    if (root.backend) root.backend.setNoFullscreenPause(checked)
                    if (root.backend) root.backend.saveSettings()
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Disable Mouse Interaction"; color: tb ? tb.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                themeBridge: root.themeBridge
                checked: root.backend ? root.backend.disableMouse : false
                onToggled: {
                    if (root.backend) root.backend.setDisableMouse(checked)
                    if (root.backend) root.backend.saveSettings()
                }
            }
        }
    }
}