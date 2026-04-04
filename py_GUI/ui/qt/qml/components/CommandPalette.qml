import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: root

    property var backend
    modal: true
    focus: true
    width: 760
    height: 520
    anchors.centerIn: Overlay.overlay
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    background: Rectangle {
        radius: 12
        color: "#1a1b26"
        border.width: 1
        border.color: "#2f344b"
    }

    property string query: ""

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        TextField {
            id: searchField
            Layout.fillWidth: true
            placeholderText: "Search wallpapers and commands..."
            text: root.query
            onTextEdited: root.query = text
            Component.onCompleted: forceActiveFocus()
        }

        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            model: {
                var out = []
                out.push({ kind: "action", label: "Random Wallpaper" })
                out.push({ kind: "action", label: "Stop All" })
                out.push({ kind: "action", label: "Refresh Library" })

                if (root.backend && root.backend.wallpapers) {
                    var q = (root.query || "").toLowerCase()
                    for (var i = 0; i < root.backend.wallpapers.length; i++) {
                        var w = root.backend.wallpapers[i]
                        var title = String(w.title || "")
                        var id = String(w.id || "")
                        if (!q || title.toLowerCase().indexOf(q) >= 0 || id.toLowerCase().indexOf(q) >= 0) {
                            out.push({ kind: "wallpaper", id: id, label: title || id })
                        }
                        if (out.length > 40) break
                    }
                }
                return out
            }

            delegate: ItemDelegate {
                required property var modelData
                width: ListView.view.width
                text: modelData.label
                onClicked: {
                    if (!root.backend) return
                    if (modelData.kind === "action") {
                        if (modelData.label === "Random Wallpaper") root.backend.applyRandomWallpaper()
                        else if (modelData.label === "Stop All") root.backend.stopWallpaper()
                        else if (modelData.label === "Refresh Library") root.backend.refresh()
                    } else if (modelData.kind === "wallpaper") {
                        root.backend.selectWallpaper(modelData.id)
                        root.backend.applyWallpaper(modelData.id)
                    }
                    root.close()
                }
            }
        }
    }
}
