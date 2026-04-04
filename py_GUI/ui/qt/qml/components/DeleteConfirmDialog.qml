import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: root

    property string wallpaperId: ""
    property string wallpaperTitle: ""
    property string wallpaperPath: ""

    signal confirmDelete(string wallpaperId, string wallpaperPath)

    modal: true
    title: "Delete this wallpaper?"
    width: 520
    height: 180
    standardButtons: Dialog.Ok | Dialog.Cancel

    onAccepted: {
        root.confirmDelete(root.wallpaperId, root.wallpaperPath)
    }

    contentItem: ColumnLayout {
        spacing: 10
        Label {
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            text: "This action cannot be undone. This will permanently delete \"" + (root.wallpaperTitle || root.wallpaperId) + "\" from disk."
            color: "#c0caf5"
        }
    }
}
