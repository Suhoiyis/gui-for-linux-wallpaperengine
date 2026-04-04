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
            text: "System & Tools"
            color: "#9aa5ce"
            font.pixelSize: 12
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Workshop Path"; color: "#c0caf5"; Layout.preferredWidth: 160 }
            TextField {
                id: workshopField
                Layout.fillWidth: true
                text: root.backend ? root.backend.workshopPath : ""
                selectByMouse: true
            }
            Button {
                text: "Save"
                onClicked: if (root.backend) root.backend.setWorkshopPath(workshopField.text)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Assets Directory"; color: "#c0caf5"; Layout.preferredWidth: 160 }
            TextField {
                id: assetsField
                Layout.fillWidth: true
                text: root.backend ? root.backend.assetsPath : ""
            }
            Button {
                text: "Save"
                onClicked: if (root.backend) root.backend.setAssetsPath(assetsField.text)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Target Resolution"; color: "#c0caf5"; Layout.preferredWidth: 160 }
            ComboBox {
                id: resolutionCombo
                Layout.fillWidth: true
                editable: true
                model: ["3840x2160", "2560x1440", "1920x1080", "1366x768", "1280x720"]
                Component.onCompleted: {
                    if (!root.backend) return
                    var idx = model.indexOf(root.backend.screenshotRes)
                    if (idx >= 0) {
                        currentIndex = idx
                    } else {
                        editText = root.backend.screenshotRes
                    }
                }
                onActivated: if (root.backend) root.backend.setScreenshotRes(currentText)
                onEditTextChanged: if (root.backend) root.backend.setScreenshotRes(editText)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Screenshot Delay (s)"; color: "#c0caf5"; Layout.preferredWidth: 160 }
            SpinBox {
                from: 0
                to: 300
                value: root.backend ? root.backend.screenshotDelay : 20
                editable: true
                onValueModified: if (root.backend) root.backend.setScreenshotDelay(value)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Prefer Xvfb"; color: "#c0caf5"; Layout.preferredWidth: 160 }
            Switch {
                checked: root.backend ? root.backend.preferXvfb : true
                onToggled: if (root.backend) root.backend.setPreferXvfb(checked)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Start Hidden"; color: "#c0caf5"; Layout.preferredWidth: 160 }
            Switch {
                checked: root.backend ? root.backend.startHidden : false
                onToggled: if (root.backend) root.backend.setStartHidden(checked)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Auto Restore"; color: "#c0caf5"; Layout.preferredWidth: 160 }
            Switch {
                checked: root.backend ? root.backend.autoRestore : false
                onToggled: if (root.backend) root.backend.setAutoRestore(checked)
            }
        }
    }
}
