import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Item {
    id: root

    property var backend
    property var themeBridge
    property var tb: themeBridge || null

    signal switchToNormal()

    Rectangle {
        anchors.fill: parent
        color: tb ? tb.cBg : Theme.bg

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            CompactNavbar {
                Layout.fillWidth: true
                Layout.margins: Theme.spaceSm
                themeBridge: root.themeBridge
                onSwitchToNormal: root.switchToNormal()
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                contentWidth: availableWidth
                clip: true

                ColumnLayout {
                    width: parent.width
                    spacing: Theme.spaceMd

                    Item {
                        Layout.fillWidth: true
                        Layout.preferredHeight: Theme.spaceMd
                    }

                    CompactPreview {
                        Layout.alignment: Qt.AlignHCenter
                        themeBridge: root.themeBridge
                        wallpaper: root.backend ? root.backend.selectedWallpaper : ({})
                        totalCount: root.backend ? root.backend.wallpapers.length : 0
                        currentIndex: {
                            if (!root.backend || !root.backend.selectedId) return 0
                            for (var i = 0; i < root.backend.wallpapers.length; i++) {
                                if (root.backend.wallpapers[i].id === root.backend.selectedId) {
                                    return i + 1
                                }
                            }
                            return 0
                        }
                        onNavigate: function(direction) {
                            if (!root.backend || root.backend.wallpapers.length === 0) return
                            var currentIdx = -1
                            for (var i = 0; i < root.backend.wallpapers.length; i++) {
                                if (root.backend.wallpapers[i].id === root.backend.selectedId) {
                                    currentIdx = i
                                    break
                                }
                            }
                            if (currentIdx === -1) return
                            var newIdx = currentIdx + direction
                            if (newIdx < 0) newIdx = root.backend.wallpapers.length - 1
                            if (newIdx >= root.backend.wallpapers.length) newIdx = 0
                            root.backend.selectWallpaper(root.backend.wallpapers[newIdx].id)
                        }
                        onJumpTo: function(index) {
                            if (!root.backend || index < 0 || index >= root.backend.wallpapers.length) return
                            root.backend.selectWallpaper(root.backend.wallpapers[index].id)
                        }
                        onCopyIdRequested: function() {
                            if (root.backend && root.backend.selectedId) {
                                root.backend.copyTextToClipboard(root.backend.selectedId)
                            }
                        }
                    }

                    // Apply Button - styled like Tauri
                    Ctrl.GButton {
                        themeBridge: root.themeBridge
                        Layout.alignment: Qt.AlignHCenter
                        Layout.preferredWidth: 280
                        text: "Apply Wallpaper"
                        iconName: "play"
                        enabled: root.backend && root.backend.selectedId
                        onClicked: {
                            if (root.backend && root.backend.selectedId) {
                                root.backend.applyWallpaper(root.backend.selectedId)
                            }
                        }
                    }

                    Item {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                }
            }

            CompactCarousel {
                Layout.fillWidth: true
                Layout.preferredHeight: 100
                themeBridge: root.themeBridge
                wallpapers: root.backend ? root.backend.wallpapers : []
                selectedId: root.backend ? root.backend.selectedId : ""
                onSelectRequested: function(wallpaperId) {
                    if (root.backend) root.backend.selectWallpaper(wallpaperId)
                }
            }
        }
    }
}