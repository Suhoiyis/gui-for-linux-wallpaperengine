import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Dialog {
    id: root

    property string wallpaperId: ""
    property string wallpaperTitle: ""
    property string wallpaperPath: ""

    signal confirmDelete(string wallpaperId, string wallpaperPath)

    modal: true
    title: "Delete this wallpaper?"
    width: 480
    standardButtons: Dialog.Ok | Dialog.Cancel

    background: Rectangle {
        radius: Theme.radiusXl
        color: Theme.panelBg
        border.width: 1
        border.color: Theme.panelBorder
    }

    onAccepted: {
        root.confirmDelete(root.wallpaperId, root.wallpaperPath)
    }

    contentItem: ColumnLayout {
        spacing: Theme.spaceSm
        Label {
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            text: "This action cannot be undone. This will permanently delete \"" + (root.wallpaperTitle || root.wallpaperId) + "\" from disk."
            color: Theme.textPrimary
        }
    }
}