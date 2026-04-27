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
    title: "Delete Wallpaper"
    width: 480
    standardButtons: Dialog.Ok | Dialog.Cancel

    enter: Transition {
        NumberAnimation { property: "scale"; from: 0.95; to: 1.0; duration: Theme.animNormal; easing.type: Easing.OutCubic }
        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: Theme.animNormal; easing.type: Easing.OutCubic }
    }

    exit: Transition {
        NumberAnimation { property: "scale"; from: 1.0; to: 0.95; duration: Theme.animNormal; easing.type: Easing.InCubic }
        NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; duration: Theme.animNormal; easing.type: Easing.InCubic }
    }

    background: Rectangle {
        radius: Theme.radiusXl
        color: Theme.elevated
        border.width: 1
        border.color: Theme.border

        Rectangle {
            width: parent.width
            height: 3
            color: Theme.destructive
            radius: Theme.radiusXl
        }
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
            color: Theme.fg
        }
    }
}