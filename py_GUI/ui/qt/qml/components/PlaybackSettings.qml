import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../Theme.js" as Theme

Frame {
    id: root

    property var backend

    background: Rectangle {
        color: Theme.elevated
        radius: Theme.radiusXl
        border.width: 1
        border.color: Theme.border
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
            color: Theme.textSection
            font.pixelSize: Theme.fontSizeMd
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "Target FPS"
                color: Theme.fg
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
                color: Theme.fgMuted
                Layout.preferredWidth: Theme.spaceXl * 1.8
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "Scaling"
                color: Theme.fg
                Layout.preferredWidth: Theme.spaceXl * 8.5
            }
            Ctrl.GComboBox {
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
                color: Theme.fg
                Layout.preferredWidth: Theme.spaceXl * 8.5
            }
            Ctrl.GComboBox {
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
            Label { text: "Disable Parallax"; color: Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                checked: root.backend ? root.backend.disableParallax : false
                onToggled: if (root.backend) root.backend.setDisableParallax(checked)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Disable Particles"; color: Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                checked: root.backend ? root.backend.disableParticles : false
                onToggled: if (root.backend) root.backend.setDisableParticles(checked)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "No Fullscreen Pause"; color: Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                checked: root.backend ? root.backend.noFullscreenPause : false
                onToggled: if (root.backend) root.backend.setNoFullscreenPause(checked)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Disable Mouse Interaction"; color: Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                checked: root.backend ? root.backend.disableMouse : false
                onToggled: if (root.backend) root.backend.setDisableMouse(checked)
            }
        }
    }
}