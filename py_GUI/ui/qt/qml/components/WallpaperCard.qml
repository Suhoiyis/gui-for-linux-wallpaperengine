import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

Item {
    id: root

    property var wp: ({})
    property bool isSelected: false
    property bool isFavorite: Backend.isFavorite(wp.id)
    property bool showTitle: true
    property bool showIcons: true
    property bool selectionMode: false
    property bool selectionChecked: false

    signal selected()
    signal applyRequested()
    signal favoriteToggled()
    signal contextMenuRequested(var mousePos)
    signal selectionToggled()

    layer.enabled: true
    layer.smooth: true

    Rectangle {
        id: cardContainer
        anchors.fill: parent
        radius: Theme.radius3xl

        color: Theme.cardBg

        border.width: Theme.cardBorderWidth
        border.color: root.isSelected ? Theme.cardBorderActive : (mouseArea.containsMouse ? Theme.cardBorderHover : Theme.cardBorder)

        scale: mouseArea.containsMouse ? 1.01 : 1.0
        y: mouseArea.containsMouse ? -2 : 0

        Behavior on border.color {
            ColorAnimation { duration: Theme.animNormal }
        }
        Behavior on scale {
            NumberAnimation { duration: Theme.animNormal; easing.type: Easing.OutCubic }
        }
        Behavior on y {
            NumberAnimation { duration: Theme.animNormal; easing.type: Easing.OutCubic }
        }

        MouseArea {
            id: mouseArea
            anchors.fill: parent
            hoverEnabled: true
            acceptedButtons: Qt.LeftButton | Qt.RightButton

            onClicked: function(mouse) {
                if (mouse.button === Qt.RightButton) {
                    var mapped = mouseArea.mapToItem(null, mouse.x, mouse.y)
                    root.contextMenuRequested(mapped)
                } else {
                    if (root.selectionMode) {
                        root.selectionToggled()
                    } else {
                        root.selected()
                    }
                }
            }
            onDoubleClicked: function(mouse) {
                if (mouse.button === Qt.LeftButton) {
                    root.applyRequested()
                }
            }

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
                        color: Theme.errorBg
                        visible: previewImage.status === Image.Error || !previewImage.source
                        Text {
                            anchors.centerIn: parent
                            text: "No Preview"
                            color: Theme.errorText
                            font.pixelSize: Theme.fontSizeMd
                        }
                    }

                    Behavior on scale {
                        NumberAnimation { duration: Theme.animSlow; easing.type: Easing.OutCubic }
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
            visible: root.selectionMode
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.margins: Theme.spaceSm
            width: 22
            height: 22
            radius: 11
            color: root.selectionChecked ? Theme.accent : Theme.windowBg
            border.width: 1
            border.color: Theme.cardBorderHover

            Label {
                anchors.centerIn: parent
                text: root.selectionChecked ? "✓" : ""
                color: Theme.windowBg
                font.bold: true
                font.pixelSize: Theme.fontSizeMd
            }
        }

        Rectangle {
            visible: root.selectionMode && root.selectionChecked
            anchors.fill: parent
            radius: Theme.radius3xl
            color: Theme.selectionOverlay
            border.width: 1
            border.color: Theme.accent
        }

        Rectangle {
            id: favoriteButton
            visible: root.showIcons && !root.selectionMode
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.margins: Theme.spaceSm
            width: Theme.iconButtonSm
            height: Theme.iconButtonSm
            radius: Theme.radius2xl

            color: root.isFavorite ? Theme.favoriteGoldBg : Theme.windowBg
            border.width: 1
            border.color: root.isFavorite ? Theme.favoriteGold : Theme.inputBorder
            opacity: mouseArea.containsMouse || root.isFavorite ? 1 : 0

            Behavior on opacity {
                NumberAnimation { duration: Theme.animFast }
            }

            Text {
                anchors.centerIn: parent
                text: root.isFavorite ? "★" : "☆"
                color: root.isFavorite ? Theme.favoriteGold : Theme.textPrimary
                font.pixelSize: Theme.fontSizeLg
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
            anchors.margins: Theme.spaceSm
            width: typeLabel.implicitWidth + Theme.spaceMd
            height: Theme.spaceXl
            radius: Theme.radiusSm

            color: Theme.inputBg
            border.width: 1
            border.color: Theme.inputBorder
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
                font.pixelSize: Theme.fontSizeMd
            }
        }

        Rectangle {
            id: titleBar
            visible: root.showTitle
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            height: 52
            radius: Theme.radius3xl

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
                anchors.margins: Theme.spaceSm
                text: root.wp.title || "Unknown"
                color: Theme.textPrimary
                font.pixelSize: Theme.fontSizeMd
                font.bold: true
                elide: Text.ElideRight
            }
        }

        Rectangle {
            anchors.fill: parent
            radius: Theme.radius3xl
            color: "transparent"
            border.width: root.isSelected ? 3 : 0
            border.color: Theme.accent

            Rectangle {
                anchors.fill: parent
                radius: Theme.radius3xl
                color: "transparent"
                border.width: root.isSelected ? 1 : 0
                border.color: "#4da6ff66"
            }

            Behavior on border.width {
                NumberAnimation { duration: Theme.animFast }
            }
        }

        Rectangle {
            anchors.fill: parent
            radius: Theme.radius3xl
            color: "transparent"
            border.width: 1
            border.color: "#ffffff10"
            visible: mouseArea.containsMouse && !root.isSelected
        }
    }
}