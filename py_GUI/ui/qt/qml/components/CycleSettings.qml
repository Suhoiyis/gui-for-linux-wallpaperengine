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
        border.width: 1
        border.color: tb ? tb.cBorder : Theme.border
    }
    padding: Theme.spaceMd

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceSm

        Label {
            text: "Automation"
            color: tb ? tb.cTextSection : Theme.textSection
            font.pixelSize: Theme.fontSizeMd
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "Enable Cycle"
                color: tb ? tb.cFg : Theme.fg
                Layout.preferredWidth: Theme.spaceXl * 7
            }
            Ctrl.GSwitch {
                id: cycleSwitch
                checked: root.backend ? root.backend.cycleEnabled : false
                onToggled: {
                    if (root.backend) root.backend.setCycleEnabled(checked)
                    if (root.backend) root.backend.saveSettings()
                }
                Connections {
                    target: root.backend
                    function onSettingsChanged() {
                        if (!root.backend) return
                        cycleSwitch.checked = root.backend.cycleEnabled
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            enabled: cycleSwitch.checked
            opacity: enabled ? 1.0 : 0.5
            Label {
                text: "Interval (minutes)"
                color: tb ? tb.cFg : Theme.fg
                Layout.preferredWidth: Theme.spaceXl * 7
            }
            Ctrl.GSpinBox {
                id: intervalSpin
                from: 1
                to: 1440
                value: root.backend ? root.backend.cycleInterval : 15
                editable: true
                onValueModified: {
                    if (root.backend) root.backend.setCycleInterval(value)
                    if (root.backend) root.backend.saveSettings()
                }
                Connections {
                    target: root.backend
                    function onSettingsChanged() {
                        if (!root.backend) return
                        intervalSpin.value = root.backend.cycleInterval
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            enabled: cycleSwitch.checked
            opacity: enabled ? 1.0 : 0.5
            Label {
                text: "Order"
                color: tb ? tb.cFg : Theme.fg
                Layout.preferredWidth: Theme.spaceXl * 7
            }
            Ctrl.GComboBox {
                id: orderCombo
                Layout.fillWidth: true
                model: ["random", "title", "size", "type", "id"]
                Component.onCompleted: {
                    if (!root.backend) return
                    var idx = model.indexOf(root.backend.cycleOrder)
                    currentIndex = idx >= 0 ? idx : 0
                }
                onActivated: {
                    if (root.backend) root.backend.setCycleOrder(currentText)
                    if (root.backend) root.backend.saveSettings()
                }
                Connections {
                    target: root.backend
                    function onSettingsChanged() {
                        if (!root.backend) return
                        var idx = orderCombo.model.indexOf(root.backend.cycleOrder)
                        orderCombo.currentIndex = idx >= 0 ? idx : 0
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            enabled: cycleSwitch.checked
            opacity: enabled ? 1.0 : 0.5
            Label {
                text: "Playlist"
                color: tb ? tb.cFg : Theme.fg
                Layout.preferredWidth: Theme.spaceXl * 7
            }
            Ctrl.GComboBox {
                id: playlistCombo
                Layout.fillWidth: true
                textRole: "name"
                valueRole: "id"
                model: {
                    var arr = [{name: "All Wallpapers", id: ""}]
                    if (root.backend && root.backend.playlists) {
                        for (var i = 0; i < root.backend.playlists.length; i++) {
                            arr.push(root.backend.playlists[i])
                        }
                    }
                    return arr
                }
                Component.onCompleted: {
                    if (!root.backend) return
                    var currentId = root.backend.cyclePlaylistId || ""
                    for (var i = 0; i < count; i++) {
                        if (model[i].id === currentId) {
                            currentIndex = i
                            break
                        }
                    }
                }
                onActivated: {
                    if (root.backend) {
                        var selectedId = model[currentIndex].id
                        root.backend.setCyclePlaylistId(selectedId)
                        root.backend.saveSettings()
                    }
                }
                Connections {
                    target: root.backend
                    function onSettingsChanged() {
                        if (!root.backend) return
                        var currentId = root.backend.cyclePlaylistId || ""
                        for (var i = 0; i < playlistCombo.count; i++) {
                            if (playlistCombo.model[i].id === currentId) {
                                playlistCombo.currentIndex = i
                                break
                            }
                        }
                    }
                }
            }
        }
    }
}