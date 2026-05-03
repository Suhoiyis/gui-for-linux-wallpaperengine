import QtQuick
import QtQuick.Controls
import "../controls" as Ctrl
import "../effects" as Effects
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
    property var themeBridge
    property var tb: themeBridge || null

    signal selected()
    signal applyRequested()
    signal favoriteToggled()
    signal contextMenuRequested(var mousePos)
    signal selectionToggled()

    layer.enabled: true
    layer.smooth: true

    // Drop shadow as sibling before card (so it renders behind)
    Effects.GDropShadow {
        visible: root.isSelected
        shadowWidth: cardContainer.width
        shadowHeight: cardContainer.height
        radius: cardContainer.radius
        color: tb ? tb.cBrand20 : Theme.brand20
        spread: 6
        verticalOffset: 2
        x: cardContainer.x
        y: cardContainer.y + (mouseArea.containsMouse ? -2 : 0)
    }

    Rectangle {
        id: cardContainer
        anchors.fill: parent
        radius: Theme.radiusLg
        y: mouseArea.containsMouse ? -3 : 0

        Behavior on y {
            NumberAnimation { duration: Theme.animNormal; easing.type: Easing.OutCubic }
        }

        color: tb ? tb.cSurface : Theme.surface

        border.width: root.isSelected ? 2 : 0
        border.color: root.isSelected ? (tb ? tb.cBrand : Theme.brand) : "transparent"

        Behavior on border.color {
            ColorAnimation { duration: Theme.animNormal }
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
                    anchors.margins: root.isSelected ? 2 : 1
                    source: root.wp.preview || ""
                    fillMode: Image.PreserveAspectCrop
                    asynchronous: true

                    sourceSize.width: 320
                    sourceSize.height: 320

                    Effects.GShimmer {
                        anchors.fill: parent
                        active: previewImage.status === Image.Loading
                        visible: previewImage.status === Image.Loading
                        radius: 0
                    }

                    Rectangle {
                        anchors.fill: parent
                        color: tb ? tb.cElevated : Theme.elevated
                        visible: previewImage.status === Image.Error || !previewImage.source
                        Text {
                            anchors.centerIn: parent
                            text: "No Preview"
                            color: tb ? tb.cFgSubtle : Theme.fgSubtle
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
                            scale: 1.05
                        }
                    }
                ]
            }
        }

        // Selection checkbox
        Rectangle {
            visible: root.selectionMode
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.margins: Theme.spaceSm
            width: 22
            height: 22
            radius: 11
            color: root.selectionChecked ? (tb ? tb.cBrand : Theme.brand) : (tb ? tb.cSurface : Theme.surface)
            border.width: root.selectionChecked ? 0 : 1
            border.color: root.selectionChecked ? (tb ? tb.cBrand : Theme.brand) : (tb ? tb.cBorderHover : Theme.borderHover)

            Ctrl.GIcon {
                visible: root.selectionChecked
                name: "check"
                size: 12
                color: tb ? tb.cBrandFg : Theme.brandFg
                anchors.centerIn: parent
            }
        }

        // Selection overlay
        Rectangle {
            visible: root.selectionMode && root.selectionChecked
            anchors.fill: parent
            radius: Theme.radiusLg
            color: tb ? tb.cSelectionOverlay : Theme.selectionOverlay
            border.width: 0
        }

        // Favorite button
        Rectangle {
            id: favoriteButton
            visible: root.showIcons && !root.selectionMode
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.margins: Theme.spaceSm
            width: Theme.iconButtonSm
            height: Theme.iconButtonSm
            radius: Theme.radius2xl

            color: root.isFavorite ? (tb ? tb.cFavoriteGoldBg : Theme.favoriteGoldBg) : Theme.withAlpha("#000000", 0.40)
            border.width: 0
            opacity: mouseArea.containsMouse || root.isFavorite ? 1 : 0

            Behavior on opacity {
                NumberAnimation { duration: Theme.animFast }
            }

            Ctrl.GIcon {
                name: "star"
                size: 14
                color: root.isFavorite ? (tb ? tb.cFavoriteGold : Theme.favoriteGold) : (tb ? tb.cFg : Theme.fg)
                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                onClicked: function(e) {
                    e.accepted = true
                    root.favoriteToggled()
                }
            }
        }

        // Type badge
        Rectangle {
            id: typeBadge
            visible: root.showIcons
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.margins: Theme.spaceSm
            width: typeIcon.size + Theme.spaceSm * 2
            height: typeIcon.size + Theme.spaceSm * 2
            radius: Theme.radiusSm

            color: Theme.withAlpha("#000000", 0.40)
            opacity: 0.92

            Ctrl.GIcon {
                id: typeIcon
                name: {
                    var t = (root.wp.type || "").toLowerCase()
                    if (t === "video") return "video"
                    if (t === "web") return "globe"
                    if (t === "scene") return "monitor"
                    return "image"
                }
                size: Theme.fontSizeMd
                color: tb ? tb.cFg : Theme.fg
                anchors.centerIn: parent
            }
        }

        // Title gradient overlay
        Rectangle {
            id: titleBar
            visible: root.showTitle
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            height: 52
            radius: Theme.radiusLg

            gradient: Gradient {
                orientation: Gradient.Vertical
                GradientStop { position: 0.0; color: "transparent" }
                GradientStop { position: 0.25; color: Theme.withAlpha("#000000", 0.33) }
                GradientStop { position: 1.0; color: Theme.withAlpha("#000000", 0.85) }
            }

            clip: true

            Text {
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: Theme.spaceSm
                text: root.wp.title || "Unknown"
                color: tb ? tb.cFg : Theme.fg
                font.pixelSize: Theme.fontSizeMd
                font.bold: true
                elide: Text.ElideRight
            }
        }

        // Hover outline - removed, using lift animation instead
        // Rectangle {
        //     anchors.fill: parent
        //     radius: Theme.radiusLg
        //     color: "transparent"
        //     border.width: 1
        //     border.color: Theme.withAlpha("#ffffff", 0.06)
        //     visible: mouseArea.containsMouse && !root.isSelected
        // }
    }
}
