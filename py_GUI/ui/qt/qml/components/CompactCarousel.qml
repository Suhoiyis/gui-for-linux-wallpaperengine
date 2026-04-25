import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme

Rectangle {
    id: root

    property var wallpapers: []
    property string selectedId: ""

    signal selectRequested(string wallpaperId)

    color: Theme.statusBarBg
    border.width: 1
    border.color: Theme.panelBorder

    ListView {
        id: listView
        anchors.fill: parent
        anchors.margins: Theme.spaceSm
        orientation: ListView.Horizontal
        spacing: Theme.spaceSm
        clip: true

        model: root.wallpapers

        delegate: Rectangle {
            width: 100
            height: 100
            radius: Theme.radiusMd
            color: Theme.cardBg
            border.width: root.selectedId === modelData.id ? Theme.cardBorderWidth : 0
            border.color: Theme.cardBorderActive
            clip: true

            Image {
                anchors.fill: parent
                anchors.margins: root.selectedId === modelData.id ? Theme.cardBorderWidth : 0
                source: modelData.preview || ""
                fillMode: Image.PreserveAspectCrop
                asynchronous: true
                sourceSize.width: 100
                sourceSize.height: 100
            }

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    root.selectRequested(modelData.id)
                    listView.positionViewAtIndex(index, ListView.Contain)
                }
            }
        }

        onModelChanged: {
            for (var i = 0; i < root.wallpapers.length; i++) {
                if (root.wallpapers[i].id === root.selectedId) {
                    listView.positionViewAtIndex(i, ListView.Contain)
                    break
                }
            }
        }
    }
}