import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Dialog {
    id: root

    property var backend
    property var rows: []
    property var themeBridge
    property var tb: themeBridge || null
    modal: true
    title: "Nickname Manager"
    width: 560
    height: 440

    background: Rectangle {
        radius: Theme.radiusXl
        color: tb ? tb.cElevated : Theme.elevated
        border.width: 1
        border.color: tb ? tb.cBorder : Theme.border
    }

    function rebuildRows() {
        var arr = []
        if (!root.backend) {
            root.rows = arr
            return
        }
        var source = root.backend.wallpapers || []
        for (var i = 0; i < source.length; i++) {
            arr.push({
                wallpaperId: source[i].id,
                title: source[i].title || source[i].id,
                nickname: source[i].title || "",
                selected: false
            })
        }
        arr.sort(function(a, b) { return String(a.title).localeCompare(String(b.title)) })
        root.rows = arr
    }

    onOpened: rebuildRows()

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceSm

        RowLayout {
            Layout.fillWidth: true
            Ctrl.GButton {
                text: "Select All"
                onClicked: {
                    var arr = root.rows.slice()
                    for (var i = 0; i < arr.length; i++) arr[i].selected = true
                    root.rows = arr
                }
            }
            Ctrl.GButton {
                text: "Deselect All"
                onClicked: {
                    var arr = root.rows.slice()
                    for (var i = 0; i < arr.length; i++) arr[i].selected = false
                    root.rows = arr
                }
            }
            Item { Layout.fillWidth: true }
            Ctrl.GButton {
                text: "Clear Selected"
                onClicked: {
                    var arr = root.rows.slice()
                    for (var i = 0; i < arr.length; i++) {
                        if (arr[i].selected) arr[i].nickname = ""
                    }
                    root.rows = arr
                }
            }
        }

        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            model: root.rows

            delegate: Rectangle {
                required property var modelData
                width: ListView.view.width
                height: 54
                color: modelData.selected ? (tb ? tb.cRowSelected : Theme.rowSelected) : (tb ? tb.cElevated : Theme.elevated)
                border.width: 1
                border.color: tb ? tb.cBorder : Theme.border
                radius: Theme.radiusMd

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: Theme.spaceSm
                    anchors.rightMargin: Theme.spaceSm
                    spacing: Theme.spaceSm

                    CheckBox {
                        checked: modelData.selected
                        onToggled: {
                            var arr = root.rows.slice()
                            arr[index].selected = checked
                            root.rows = arr
                        }
                    }

                    Label {
                        text: modelData.title
                        color: tb ? tb.cFg : Theme.fg
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }

                    Ctrl.GTextField {
                        Layout.preferredWidth: 300
                        text: modelData.nickname
                        onTextEdited: {
                            var arr = root.rows.slice()
                            arr[index].nickname = text
                            root.rows = arr
                        }
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Item { Layout.fillWidth: true }
            Ctrl.GButton { text: "Cancel"; onClicked: root.close() }
            Ctrl.GPillButton {
                text: "Save Changes"
                onClicked: {
                    if (root.backend) {
                        for (var i = 0; i < root.rows.length; i++) {
                            root.backend.setWallpaperNickname(root.rows[i].wallpaperId, root.rows[i].nickname)
                        }
                    }
                    root.close()
                }
            }
        }
    }
}