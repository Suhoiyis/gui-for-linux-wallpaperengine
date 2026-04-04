import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "." as Comp

Item {
    id: root

    property var backend
    property int settingsTabIndex: 0

    Rectangle {
        anchors.fill: parent
        color: "#1a1b26"

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 12
            spacing: 12

            Label {
                text: "Settings"
                color: "#c0caf5"
                font.pixelSize: 20
                font.bold: true
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 8

                Repeater {
                    model: ["Playback", "Audio", "Wayland", "System"]
                    delegate: Button {
                        required property var modelData
                        required property int index
                        text: modelData
                        highlighted: root.settingsTabIndex === index
                        onClicked: root.settingsTabIndex = index
                    }
                }
            }

            StackLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                currentIndex: root.settingsTabIndex

                ScrollView {
                    clip: true
                    contentWidth: availableWidth
                    ColumnLayout {
                        width: parent.width
                        spacing: 10
                        Comp.PlaybackSettings {
                            Layout.fillWidth: true
                            backend: root.backend
                        }
                        Comp.CycleSettings {
                            Layout.fillWidth: true
                            backend: root.backend
                        }
                    }
                }

                ScrollView {
                    clip: true
                    contentWidth: availableWidth
                    Comp.AudioSettings {
                        width: parent.width
                        backend: root.backend
                    }
                }

                ScrollView {
                    clip: true
                    contentWidth: availableWidth
                    Comp.WaylandSettings {
                        width: parent.width
                        backend: root.backend
                    }
                }

                ScrollView {
                    clip: true
                    contentWidth: availableWidth
                    Comp.SystemSettings {
                        width: parent.width
                        backend: root.backend
                    }
                }
            }
        }
    }
}
