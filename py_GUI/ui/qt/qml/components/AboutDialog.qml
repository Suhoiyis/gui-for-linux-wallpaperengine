import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Dialog {
    id: root

    property var backend
    property var themeBridge
    property var tb: themeBridge || null
    modal: true
    title: "About"
    width: 460
    height: 360

    background: Rectangle {
        radius: Theme.radiusXl
        color: tb ? tb.cElevated : Theme.elevated
        border.width: 0
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceMd

        Label {
            text: "LINUX WALLPAPER ENGINE GUI"
            color: tb ? tb.cFg : Theme.fg
            font.pixelSize: Theme.fontSize3xl
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Qt Quick Edition"
            color: tb ? tb.cFgMuted : Theme.fgMuted
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
            text: "A modern wallpaper manager for linux-wallpaperengine, migrated to Qt Quick."
            color: tb ? tb.cFg : Theme.fg
        }

        Item { Layout.fillHeight: true }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            Ctrl.GButton {
                themeBridge: root.themeBridge
                text: "GitHub"
                onClicked: {
                    if (root.backend) {
                        root.backend.openExternalUrl("https://github.com/Suhoiyis/gui-for-linux-wallpaperengine")
                    }
                }
            }
            Ctrl.GButton {
                themeBridge: root.themeBridge
                text: "Close"
                onClicked: root.close()
            }
        }
    }
}