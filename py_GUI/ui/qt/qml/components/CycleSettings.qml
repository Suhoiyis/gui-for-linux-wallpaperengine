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
            text: "Automation"
            color: "#9aa5ce"
            font.pixelSize: 12
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "Enable Cycle"
                color: "#c0caf5"
                Layout.preferredWidth: 140
            }
            Switch {
                id: cycleSwitch
                checked: root.backend ? root.backend.cycleEnabled : false
                onToggled: {
                    if (root.backend) root.backend.setCycleEnabled(checked)
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
                color: "#c0caf5"
                Layout.preferredWidth: 140
            }
            SpinBox {
                id: intervalSpin
                from: 1
                to: 1440
                value: root.backend ? root.backend.cycleInterval : 15
                editable: true
                onValueModified: {
                    if (root.backend) root.backend.setCycleInterval(value)
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
                color: "#c0caf5"
                Layout.preferredWidth: 140
            }
            ComboBox {
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
                color: "#c0caf5"
                Layout.preferredWidth: 140
            }
            ComboBox {
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
