import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "." as Comp
import "../controls" as Ctrl
import "../Theme.js" as Theme

Item {
    id: root

    property var backend
    property int settingsTabIndex: 0
    property bool showNicknameManager: false
    property bool showFavoriteManager: false

    Rectangle {
        anchors.fill: parent
        color: Theme.windowBg

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: Theme.spaceMd
            spacing: Theme.spaceMd

            Label {
                text: "Settings"
                color: Theme.textPrimary
                font.pixelSize: Theme.fontSize3xl
                font.bold: true
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: Theme.spaceSm

                Repeater {
                    model: ["Playback", "Audio", "Wayland", "System"]
                    delegate: Ctrl.GButton {
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
                        spacing: Theme.spaceSm
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
                        spacing: Theme.spaceSm
                        Comp.SystemSettings {
                            Layout.fillWidth: true
                            backend: root.backend
                        }
                        Comp.LogViewer {
                            Layout.fillWidth: true
                            backend: root.backend
                        }
                        RowLayout {
                            Layout.fillWidth: true
                            Item { Layout.fillWidth: true }
                            Ctrl.GButton {
                                text: "Manage Nicknames"
                                onClicked: root.showNicknameManager = true
                            }
                            Ctrl.GButton {
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