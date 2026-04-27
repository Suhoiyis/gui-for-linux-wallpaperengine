import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Rectangle {
    id: root

    property var wallpapers: []
    property string selectedId: ""

    signal selectRequested(string wallpaperId)

    color: Theme.surface
    border.width: 1
    border.color: Theme.border

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Previous button
        Rectangle {
            Layout.preferredWidth: 32
            Layout.fillHeight: true
            color: prevMouse.containsMouse ? Theme.elevated : "transparent"

            Behavior on color { ColorAnimation { duration: Theme.animFast } }

            Ctrl.GIcon {
                anchors.centerIn: parent
                name: "chevronRight"
                size: Theme.fontSizeMd
                color: Theme.fgMuted
                rotation: 180
            }

            MouseArea {
                id: prevMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    var currentIdx = -1
                    for (var i = 0; i < root.wallpapers.length; i++) {
                        if (root.wallpapers[i].id === root.selectedId) {
                            currentIdx = i
                            break
                        }
                    }
                    if (currentIdx > 0) {
                        root.selectRequested(root.wallpapers[currentIdx - 1].id)
                    }
                }
            }
        }

        // Carousel ListView
        ListView {
            id: listView
            Layout.fillWidth: true
            Layout.fillHeight: true
            orientation: ListView.Horizontal
            spacing: Theme.spaceSm
            clip: true
            model: root.wallpapers

            delegate: Rectangle {
                required property var modelData
                required property int index
                width: 80
                height: listView.height
                color: "transparent"

                Rectangle {
                    anchors.centerIn: parent
                    width: 72
                    height: 72
                    radius: Theme.radiusMd
                    color: Theme.elevated
                    border.width: root.selectedId === modelData.id ? 2 : 0
                    border.color: Theme.brand
                    opacity: root.selectedId === modelData.id ? 1.0 : 0.7

                    Behavior on opacity { NumberAnimation { duration: Theme.animFast } }
                    Behavior on border.width { NumberAnimation { duration: Theme.animFast } }

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

        // Next button
        Rectangle {
            Layout.preferredWidth: 32
            Layout.fillHeight: true
            color: nextMouse.containsMouse ? Theme.elevated : "transparent"

            Behavior on color { ColorAnimation { duration: Theme.animFast } }

            Ctrl.GIcon {
                anchors.centerIn: parent
                name: "chevronDown"
                size: Theme.fontSizeMd
                color: Theme.fgMuted
                rotation: -90
            }

            MouseArea {
                id: nextMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    var currentIdx = -1
                    for (var i = 0; i < root.wallpapers.length; i++) {
                        if (root.wallpapers[i].id === root.selectedId) {
                            currentIdx = i
                            break
                        }
                    }
                    if (currentIdx >= 0 && currentIdx < root.wallpapers.length - 1) {
                        root.selectRequested(root.wallpapers[currentIdx + 1].id)
                    }
                }
            }
        }
    }
}