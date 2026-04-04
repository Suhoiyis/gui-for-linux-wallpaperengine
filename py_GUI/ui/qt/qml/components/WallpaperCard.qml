import QtQuick
import QtQuick.Controls

Item {
    id: root
    
    property var wp: ({})
    property bool isSelected: false
    property bool isFavorite: Backend.isFavorite(wp.id)
    property bool showTitle: true
    property bool showIcons: true
    
    signal selected()
    signal applyRequested()
    signal favoriteToggled()

    layer.enabled: true
    layer.smooth: true
    
    Rectangle {
        id: cardContainer
        anchors.fill: parent
        radius: 16

        color: "#1f2335"

        border.width: 2
        border.color: root.isSelected ? "#7aa2f7" : (mouseArea.containsMouse ? "#4f5f8f" : "#2b2f42")

        scale: mouseArea.containsMouse ? 1.01 : 1.0

        Behavior on border.color {
            ColorAnimation { duration: 180 }
        }
        Behavior on scale {
            NumberAnimation { duration: 180; easing.type: Easing.OutCubic }
        }

        MouseArea {
            id: mouseArea
            anchors.fill: parent
            hoverEnabled: true

            onClicked: root.selected()
            onDoubleClicked: root.applyRequested()

            Rectangle {
                anchors.fill: parent
                color: "transparent"

                Image {
                    id: previewImage
                    anchors.fill: parent
                    source: root.wp.preview || ""
                    fillMode: Image.PreserveAspectCrop
                    asynchronous: true

                    sourceSize.width: 320
                    sourceSize.height: 320

                    BusyIndicator {
                        anchors.centerIn: parent
                        running: previewImage.status === Image.Loading
                    }

                    Rectangle {
                        anchors.fill: parent
                        color: "#374151"
                        visible: previewImage.status === Image.Error || !previewImage.source
                        Text {
                            anchors.centerIn: parent
                            text: "No Preview"
                            color: "#9ca3af"
                            font.pixelSize: 12
                        }
                    }

                    Behavior on scale {
                        NumberAnimation { duration: 420; easing.type: Easing.OutCubic }
                    }
                }

                states: [
                    State {
                        name: "hovered"
                        when: mouseArea.containsMouse
                        PropertyChanges {
                            target: previewImage
                            scale: 1.08
                        }
                    }
                ]
            }
        }

        Rectangle {
            id: favoriteButton
            visible: root.showIcons
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.margins: 8
            width: 28
            height: 28
            radius: 14

            color: root.isFavorite ? "#665216" : "#1a1b26"
            border.width: 1
            border.color: root.isFavorite ? "#e0af68" : "#3b4261"
            opacity: mouseArea.containsMouse || root.isFavorite ? 1 : 0

            Behavior on opacity {
                NumberAnimation { duration: 160 }
            }

            Text {
                anchors.centerIn: parent
                text: root.isFavorite ? "★" : "☆"
                color: root.isFavorite ? "#e0af68" : "#c0caf5"
                font.pixelSize: 14
            }

            MouseArea {
                anchors.fill: parent
                onClicked: function(e) {
                    e.accepted = true
                    root.favoriteToggled()
                }
            }
        }

        Rectangle {
            id: typeBadge
            visible: root.showIcons
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.margins: 8
            width: typeLabel.implicitWidth + 12
            height: 24
            radius: 6

            color: "#161926"
            border.width: 1
            border.color: "#3b4261"
            opacity: 0.92

            Text {
                id: typeLabel
                anchors.centerIn: parent
                text: {
                    var t = (root.wp.type || "").toLowerCase()
                    if (t === "video") return "🎬"
                    if (t === "web") return "🌐"
                    if (t === "scene") return "🖥️"
                    return "🖼️"
                }
                font.pixelSize: 12
            }
        }

        Rectangle {
            id: titleBar
            visible: root.showTitle
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            height: 52
            radius: 16

            gradient: Gradient {
                orientation: Gradient.Vertical
                GradientStop { position: 0.0; color: "transparent" }
                GradientStop { position: 0.25; color: "#55000000" }
                GradientStop { position: 1.0; color: "#d9000000" }
            }

            clip: true

            Text {
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 10
                text: root.wp.title || "Unknown"
                color: "#c0caf5"
                font.pixelSize: 12
                font.bold: true
                elide: Text.ElideRight
            }
        }

        Rectangle {
            anchors.fill: parent
            radius: 16
            color: "transparent"
            border.width: root.isSelected ? 3 : 0
            border.color: "#7aa2f7"

            Rectangle {
                anchors.fill: parent
                radius: 16
                color: "transparent"
                border.width: root.isSelected ? 1 : 0
                border.color: "#4da6ff66"
            }

            Behavior on border.width {
                NumberAnimation { duration: 120 }
            }
        }

        Rectangle {
            anchors.fill: parent
            radius: 16
            color: "transparent"
            border.width: 1
            border.color: "#ffffff10"
            visible: mouseArea.containsMouse && !root.isSelected
        }
    }
}
