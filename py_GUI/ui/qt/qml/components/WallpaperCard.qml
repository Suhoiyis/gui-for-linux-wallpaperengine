// WallpaperCard.qml - 翻译自 WallpaperCard.tsx
import QtQuick
import QtQuick.Controls

Item {
    id: root
    
    property var wp: ({})
    property bool isSelected: false
    property bool isFavorite: Backend.isFavorite(wp.id)
    
    signal selected()
    signal applyRequested()
    signal favoriteToggled()
    
    Rectangle {
        id: cardContainer
        anchors.fill: parent
        radius: 16
        
        color: "#24283b"
        
        border.width: 2
        border.color: root.isSelected ? "#7aa2f7" : "#292e42"
        
        Behavior on border.color {
            ColorAnimation { duration: 150 }
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
                    
                    BusyIndicator {
                        anchors.centerIn: parent
                        running: previewImage.status === Image.Loading
                    }
                    
                    Behavior on scale {
                        NumberAnimation { duration: 300; easing.type: Easing.OutCubic }
                    }
                }
                
                states: [
                    State {
                        name: "hovered"
                        when: mouseArea.containsMouse
                        PropertyChanges {
                            target: previewImage
                            scale: 1.1
                        }
                    }
                ]
            }
        }
        
        Rectangle {
            id: favoriteButton
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.margins: 8
            width: 28
            height: 28
            radius: 14
            
            color: root.isFavorite ? "#3d59a1" : "#1a1b26"
            opacity: mouseArea.containsMouse || root.isFavorite ? 1 : 0
            
            Behavior on opacity {
                NumberAnimation { duration: 150 }
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
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.margins: 8
            width: typeLabel.implicitWidth + 12
            height: 24
            radius: 6
            
            color: "#1a1b26"
            opacity: 0.8
            
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
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            height: 40
            radius: 16
            
            gradient: Gradient {
                orientation: Gradient.Vertical
                GradientStop { position: 0.0; color: "transparent" }
                GradientStop { position: 0.3; color: "#80000000" }
                GradientStop { position: 1.0; color: "#cc000000" }
            }
            
            clip: true
            
            Text {
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 8
                text: root.wp.title || "Unknown"
                color: "#c0caf5"
                font.pixelSize: 11
                font.bold: true
                elide: Text.ElideRight
            }
        }
        
        Rectangle {
            anchors.fill: parent
            radius: 16
            color: "transparent"
            border.width: 3
            border.color: "#7aa2f7"
            visible: root.isSelected
            
            Behavior on visible {
                NumberAnimation { target: borderOpacity; property: "value"; duration: 150 }
            }
        }
    }
}
