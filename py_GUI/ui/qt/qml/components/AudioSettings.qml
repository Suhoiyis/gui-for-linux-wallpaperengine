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
            text: "Audio & Display"
            color: "#9aa5ce"
            font.pixelSize: 12
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Mute Audio"; color: "#c0caf5"; Layout.preferredWidth: 170 }
            Switch {
                id: muteSwitch
                checked: root.backend ? root.backend.silence : true
                onToggled: if (root.backend) root.backend.setSilence(checked)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            visible: !muteSwitch.checked
            Label { text: "Master Volume"; color: "#c0caf5"; Layout.preferredWidth: 170 }
            Slider {
                id: volumeSlider
                Layout.fillWidth: true
                from: 0
                to: 100
                stepSize: 1
                value: root.backend ? root.backend.volume : 0
                onMoved: if (root.backend) root.backend.setVolume(Math.round(value))
            }
            Label {
                text: String(Math.round(volumeSlider.value)) + "%"
                color: "#8a90b8"
                Layout.preferredWidth: 46
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Disable Auto Mute"; color: "#c0caf5"; Layout.preferredWidth: 170 }
            Switch {
                checked: root.backend ? root.backend.noAutomute : false
                onToggled: if (root.backend) root.backend.setNoAutomute(checked)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "No Audio Processing"; color: "#c0caf5"; Layout.preferredWidth: 170 }
            Switch {
                checked: root.backend ? root.backend.noAudioProcessing : false
                onToggled: if (root.backend) root.backend.setNoAudioProcessing(checked)
            }
        }
    }
}
