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

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceSm

        Label {
            text: "System & Tools"
            color: tb ? tb.cTextSection : Theme.textSection
            font.pixelSize: Theme.fontSizeMd
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Workshop Path"; color: tb ? tb.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8 }
            Ctrl.GTextField {
                id: workshopField
                Layout.fillWidth: true
                text: root.backend ? root.backend.workshopPath : ""
                selectByMouse: true
            }
            Ctrl.GPillButton {
                text: "Save"
                onClicked: {
                    if (root.backend) {
                        root.backend.setWorkshopPath(workshopField.text)
                        root.backend.saveSettings()
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Assets Directory"; color: tb ? tb.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8 }
            Ctrl.GTextField {
                id: assetsField
                Layout.fillWidth: true
                text: root.backend ? root.backend.assetsPath : ""
            }
            Ctrl.GPillButton {
                text: "Save"
                onClicked: {
                    if (root.backend) {
                        root.backend.setAssetsPath(assetsField.text)
                        root.backend.saveSettings()
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Target Resolution"; color: tb ? tb.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8 }
            Ctrl.GComboBox {
                themeBridge: root.themeBridge
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
            Label { text: "Screenshot Delay (s)"; color: tb ? tb.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8 }
            Ctrl.GSpinBox {
                from: 0
                to: 300
                value: root.backend ? root.backend.screenshotDelay : 20
                editable: true
                onValueModified: if (root.backend) root.backend.setScreenshotDelay(value)
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Prefer Xvfb"; color: tb ? tb.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8 }
            Ctrl.GSwitch {
                themeBridge: root.themeBridge
                checked: root.backend ? root.backend.preferXvfb : true
                onToggled: {
                    if (root.backend) root.backend.setPreferXvfb(checked)
                    if (root.backend) root.backend.saveSettings()
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Start Hidden"; color: tb ? tb.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8 }
            Ctrl.GSwitch {
                themeBridge: root.themeBridge
                checked: root.backend ? root.backend.startHidden : false
                onToggled: {
                    if (root.backend) root.backend.setStartHidden(checked)
                    if (root.backend) root.backend.saveSettings()
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Auto Restore"; color: tb ? tb.cFg : Theme.fg; Layout.preferredWidth: Theme.spaceXl * 8 }
            Ctrl.GSwitch {
                themeBridge: root.themeBridge
                checked: root.backend ? root.backend.autoRestore : false
                onToggled: {
                    if (root.backend) root.backend.setAutoRestore(checked)
                    if (root.backend) root.backend.saveSettings()
                }
            }
        }
    }
}