import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: root

    property var backend
    property var rows: []
    modal: true
    title: "Nickname Manager"
    width: 680
    height: 560

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
                color: modelData.selected ? "#2c3148" : "#1f2335"
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

                    TextField {
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
            Button { text: "Cancel"; onClicked: root.close() }
            Button {
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
