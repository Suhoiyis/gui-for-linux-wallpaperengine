import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: root

    property var backend
    property bool requiredMode: false
    property int step: 0

    modal: true
    width: 620
    height: 500
    title: "Welcome"

    onOpened: step = 0
    closePolicy: requiredMode ? Popup.NoAutoClose : (Popup.CloseOnEscape | Popup.CloseOnPressOutside)

    ColumnLayout {
        anchors.fill: parent
        spacing: 12

        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            Repeater {
                model: 5
                delegate: Rectangle {
                    required property int index
                    width: 8
                    height: 8
                    radius: 4
                    color: root.step === index ? "#7aa2f7" : "#4a506b"
                }
            }
        }

        Label {
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
            color: "#c0caf5"
            font.pixelSize: 18
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
            radius: 10
            color: "#1f2335"
            border.width: 1
            border.color: "#2f344b"

            Label {
                anchors.centerIn: parent
                color: "#a9b1d6"
                width: parent.width - 40
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
            Button {
                text: "Back"
                enabled: root.step > 0
                onClicked: root.step = Math.max(0, root.step - 1)
            }
            Item { Layout.fillWidth: true }
            Button {
                visible: root.step < 4
                text: root.step === 0 ? "Get Started" : "Continue"
                onClicked: root.step = Math.min(4, root.step + 1)
            }
            Button {
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
