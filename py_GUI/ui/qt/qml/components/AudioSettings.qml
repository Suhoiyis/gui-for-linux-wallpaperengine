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
            color: Theme.textSection
            font.pixelSize: Theme.fontSizeMd
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Mute Audio"; color: Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                id: muteSwitch
                checked: root.backend ? root.backend.silence : true
                onToggled: if (root.backend) root.backend.setSilence(checked)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            visible: !muteSwitch.checked
            Label { text: "Master Volume"; color: Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
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
                color: Theme.fgMuted
                Layout.preferredWidth: Theme.spaceXl * 2.3
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Disable Auto Mute"; color: Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                checked: root.backend ? root.backend.noAutomute : false
                onToggled: if (root.backend) root.backend.setNoAutomute(checked)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "No Audio Processing"; color: Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8.5 }
            Ctrl.GSwitch {
                checked: root.backend ? root.backend.noAudioProcessing : false
                onToggled: if (root.backend) root.backend.setNoAudioProcessing(checked)
            }
        }
    }
}