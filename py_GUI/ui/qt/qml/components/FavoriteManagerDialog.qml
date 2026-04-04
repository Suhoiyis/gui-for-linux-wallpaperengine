import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: root

    property var backend
    property var rows: []
    modal: true
    title: "Favorite Manager"
    width: 680
    height: 560

    function rebuildRows() {
        var arr = []
        if (!root.backend) {
            root.rows = arr
            return
        }
        var fav = root.backend.favoriteIds || []
        var all = root.backend.wallpapers || []
        for (var i = 0; i < fav.length; i++) {
            var id = fav[i]
            var title = id
            for (var j = 0; j < all.length; j++) {
                if (all[j].id === id) {
                    title = all[j].title || id
                    break
                }
            }
            arr.push({ wallpaperId: id, title: title, selected: false })
        }
        arr.sort(function(a, b) { return String(a.title).localeCompare(String(b.title)) })
        root.rows = arr
    }

    onOpened: rebuildRows()

    ColumnLayout {
        anchors.fill: parent
        spacing: 8

        RowLayout {
            Layout.fillWidth: true
            Button {
                text: "Select All"
                onClicked: {
                    var arr = root.rows.slice()
                    for (var i = 0; i < arr.length; i++) arr[i].selected = true
                    root.rows = arr
                }
            }
            Button {
                text: "Deselect All"
                onClicked: {
                    var arr = root.rows.slice()
                    for (var i = 0; i < arr.length; i++) arr[i].selected = false
                    root.rows = arr
                }
            }
            Item { Layout.fillWidth: true }
            Button {
                text: "Remove Selected"
                onClicked: {
                    if (root.backend) {
                        for (var i = 0; i < root.rows.length; i++) {
                            if (root.rows[i].selected) root.backend.toggleFavorite(root.rows[i].wallpaperId)
                        }
                    }
                    root.rebuildRows()
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
                height: 50
                color: modelData.selected ? "#393423" : "#1f2335"
                border.width: 1
                border.color: "#2f344b"
                radius: 8

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 8
                    anchors.rightMargin: 8
                    spacing: 8

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
                        color: "#a9b1d6"
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }

                    Label {
                        text: "★"
                        color: "#e0af68"
                        font.pixelSize: 18
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Item { Layout.fillWidth: true }
            Button { text: "Close"; onClicked: root.close() }
        }
    }
}
