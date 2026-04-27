import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Dialog {
    id: root

    property var backend
    modal: true
    title: "About"
    width: 460
    height: 360

    background: Rectangle {
        radius: Theme.radiusXl
        color: Theme.elevated
        border.width: 1
        border.color: Theme.border
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceMd

        Label {
            text: "LINUX WALLPAPER ENGINE GUI"
            color: Theme.fg
            font.pixelSize: Theme.fontSize3xl
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Qt Quick Edition"
            color: Theme.fgMuted
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
            text: "A modern wallpaper manager for linux-wallpaperengine, migrated to Qt Quick."
            color: Theme.fg
        }

        Item { Layout.fillHeight: true }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            Ctrl.GButton {
                text: "GitHub"
                onClicked: {
                    if (root.backend) {
                        root.backend.openExternalUrl("https://github.com/Suhoiyis/gui-for-linux-wallpaperengine")
                    }
                }
            }
            Ctrl.GButton {
                text: "Close"
                onClicked: root.close()
            }
        }
    }
}