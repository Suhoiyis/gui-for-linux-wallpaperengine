import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root

    property var wallpapers: []
    property string selectedId: ""

    signal selectRequested(string wallpaperId)

    color: "#16161e"
    border.width: 1
    border.color: "#2f344b"

    ListView {
        id: listView
        anchors.fill: parent
        anchors.margins: 10
        orientation: ListView.Horizontal
        spacing: 10
        clip: true

        model: root.wallpapers

        delegate: Rectangle {
            width: 100
            height: 100
            radius: 8
            color: "#1f2335"
            border.width: root.selectedId === modelData.id ? 2 : 0
            border.color: "#7aa2f7"
            clip: true

            Image {
                anchors.fill: parent
                anchors.margins: root.selectedId === modelData.id ? 2 : 0
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
