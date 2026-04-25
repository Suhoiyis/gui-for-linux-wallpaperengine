import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Dialog {
    id: root

    property var backend
    property bool requiredMode: false
    property int step: 0

    modal: true
    width: 620
    height: 500
    title: "Welcome"

    background: Rectangle {
        radius: Theme.radiusXl
        color: Theme.panelBg
        border.width: 1
        border.color: Theme.panelBorder
    }

    onOpened: step = 0
    closePolicy: requiredMode ? Popup.NoAutoClose : (Popup.CloseOnEscape | Popup.CloseOnPressOutside)

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceMd

        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            Repeater {
                model: 5
                delegate: Rectangle {
                    required property int index
                    width: 8
                    height: 8
                    radius: 4
                    color: root.step === index ? Theme.accent : Theme.inputBorder
                }
            }
        }

        Label {
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
            color: Theme.textPrimary
            font.pixelSize: Theme.fontSize2xl
            font.bold: true
            text: {
                if (root.step === 0) return "Welcome"
                if (root.step === 1) return "Requirements Check"
                if (root.step === 2) return "Directories"
                if (root.step === 3) return "Quick Settings"
                return "All Set!"
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: Theme.radiusLg
            color: Theme.panelBg
            border.width: 1
            border.color: Theme.panelBorder

            Label {
                anchors.centerIn: parent
                color: Theme.textBody
                width: parent.width - Theme.spaceXl * 2
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                text: {
                    if (root.step === 0) return "Welcome to Linux Wallpaper Engine GUI (Qt).\nThis setup helps you finish first-run configuration quickly."
                    if (root.step === 1) return "Requirements:\n1) linux-wallpaperengine installed\n2) Steam Workshop content available"
                    if (root.step === 2) return "Directories:\nSet Workshop Path and optional Assets Path in Settings > System."
                    if (root.step === 3) return "Quick Settings:\nTune FPS, audio, and cycle settings for your machine."
                    return "All set. You can now browse wallpapers and apply them to your screens."
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Ctrl.GButton {
                text: "Back"
                enabled: root.step > 0
                onClicked: root.step = Math.max(0, root.step - 1)
            }
            Item { Layout.fillWidth: true }
            Ctrl.GPillButton {
                visible: root.step < 4
                text: root.step === 0 ? "Get Started" : "Continue"
                onClicked: root.step = Math.min(4, root.step + 1)
            }
            Ctrl.GPillButton {
                visible: root.step === 4
                text: "Start Using App"
                onClicked: {
                    if (root.backend) root.backend.completeOnboarding()
                    root.close()
                }
            }
        }
    }
}