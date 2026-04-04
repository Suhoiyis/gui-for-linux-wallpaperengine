import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Frame {
    id: root

    property var backend

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        Label {
            text: "Playback & Performance"
            color: "#9aa5ce"
            font.pixelSize: 12
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "Target FPS"
                color: "#c0caf5"
                Layout.preferredWidth: 170
            }
            Slider {
                id: fpsSlider
                Layout.fillWidth: true
                from: 10
                to: 144
                stepSize: 1
                value: root.backend ? root.backend.fps : 30
                onMoved: if (root.backend) root.backend.setFps(Math.round(value))
            }
            Label {
                text: String(Math.round(fpsSlider.value))
                color: "#8a90b8"
                Layout.preferredWidth: 36
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "Scaling"
                color: "#c0caf5"
                Layout.preferredWidth: 170
            }
            ComboBox {
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
                color: "#c0caf5"
                Layout.preferredWidth: 170
            }
            ComboBox {
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
            Label { text: "Disable Parallax"; color: "#c0caf5"; Layout.preferredWidth: 170 }
            Switch {
                checked: root.backend ? root.backend.disableParallax : false
                onToggled: if (root.backend) root.backend.setDisableParallax(checked)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Disable Particles"; color: "#c0caf5"; Layout.preferredWidth: 170 }
            Switch {
                checked: root.backend ? root.backend.disableParticles : false
                onToggled: if (root.backend) root.backend.setDisableParticles(checked)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "No Fullscreen Pause"; color: "#c0caf5"; Layout.preferredWidth: 170 }
            Switch {
                checked: root.backend ? root.backend.noFullscreenPause : false
                onToggled: if (root.backend) root.backend.setNoFullscreenPause(checked)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Disable Mouse Interaction"; color: "#c0caf5"; Layout.preferredWidth: 170 }
            Switch {
                checked: root.backend ? root.backend.disableMouse : false
                onToggled: if (root.backend) root.backend.setDisableMouse(checked)
            }
        }
    }
}
