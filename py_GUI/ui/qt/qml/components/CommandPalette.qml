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

    function _matches(text, q) {
        var t = String(text || "").toLowerCase()
        var qq = String(q || "").toLowerCase().trim()
        return qq.length === 0 || t.indexOf(qq) >= 0
    }

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
                var q = (root.query || "").toLowerCase().trim()

                var quick = [
                    { kind: "action", label: "Random Wallpaper", tab: "library" },
                    { kind: "action", label: "Stop All", tab: "library" },
                    { kind: "action", label: "Refresh Library", tab: "library" }
                ]
                for (var qi = 0; qi < quick.length; qi++) {
                    if (root._matches(quick[qi].label, q)) out.push(quick[qi])
                }

                var nav = [
                    { kind: "navigate", label: "Open Library", page: "library" },
                    { kind: "navigate", label: "Open Performance", page: "performance" },
                    { kind: "navigate", label: "Open Settings", page: "settings" },
                    { kind: "navigate", label: "Open Compact Mode", page: "compact" }
                ]
                for (var ni = 0; ni < nav.length; ni++) {
                    if (root._matches(nav[ni].label, q)) out.push(nav[ni])
                }

                if (root.backend && root.backend.wallpapers) {
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
                    } else if (modelData.kind === "navigate") {
                        if (root.parent && root.parent.pageChangedByPalette) {
                            root.parent.pageChangedByPalette(modelData.page)
                        }
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
