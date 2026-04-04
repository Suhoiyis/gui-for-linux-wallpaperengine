import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "." as Comp

Item {
    id: root

    property var backend
    property int settingsTabIndex: 0
    property bool showNicknameManager: false
    property bool showFavoriteManager: false

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
                    ColumnLayout {
                        width: parent.width
                        spacing: 10
                        Comp.SystemSettings {
                            Layout.fillWidth: true
                            backend: root.backend
                        }
                        RowLayout {
                            Layout.fillWidth: true
                            Item { Layout.fillWidth: true }
                            Button {
                                text: "Manage Nicknames"
                                onClicked: root.showNicknameManager = true
                            }
                            Button {
                                text: "Manage Favorites"
                                onClicked: root.showFavoriteManager = true
                            }
                        }
                    }
                }
            }
        }
    }

    Comp.NicknameManagerDialog {
        backend: root.backend
        visible: root.showNicknameManager
        onClosed: root.showNicknameManager = false
    }

    Comp.FavoriteManagerDialog {
        backend: root.backend
        visible: root.showFavoriteManager
        onClosed: root.showFavoriteManager = false
    }
}
