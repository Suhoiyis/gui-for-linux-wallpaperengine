import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: root

    property var backend
    modal: true
    title: "About"
    width: 460
    height: 360

    ColumnLayout {
        anchors.fill: parent
        spacing: 12

        Label {
            text: "LINUX WALLPAPER ENGINE GUI"
            color: "#c0caf5"
            font.pixelSize: 20
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Qt Quick Edition"
            color: "#8a90b8"
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
            text: "A modern wallpaper manager for linux-wallpaperengine, migrated to Qt Quick."
            color: "#a9b1d6"
        }

        Item { Layout.fillHeight: true }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            Button {
                text: "GitHub"
                onClicked: {
                    if (root.backend) {
                        root.backend.openExternalUrl("https://github.com/Suhoiyis/gui-for-linux-wallpaperengine")
                    }
                }
            }
            Button {
                text: "Close"
                onClicked: root.close()
            }
        }
    }
}
