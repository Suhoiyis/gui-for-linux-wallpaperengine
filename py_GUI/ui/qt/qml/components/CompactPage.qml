import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme

Item {
    id: root

    property var backend

    signal switchToNormal()

    Rectangle {
        anchors.fill: parent
        color: Theme.windowBg

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            CompactNavbar {
                Layout.fillWidth: true
                Layout.margins: Theme.spaceSm
                onSwitchToNormal: root.switchToNormal()
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                contentWidth: availableWidth

                ColumnLayout {
                    width: parent.width
                    spacing: Theme.spaceXl

                    Item {
                        Layout.fillWidth: true
                        Layout.preferredHeight: Theme.spaceXl
                    }

                    CompactPreview {
                        Layout.alignment: Qt.AlignHCenter
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
                        onApplyRequested: function() {
                            if (root.backend && root.backend.selectedId) {
                                root.backend.applyWallpaper(root.backend.selectedId)
                            }
                        }
                        onCopyIdRequested: function() {
                            if (root.backend && root.backend.selectedId) {
                                root.backend.copyTextToClipboard(root.backend.selectedId)
                            }
                        }
                    }
                }
            }

            CompactCarousel {
                Layout.fillWidth: true
                Layout.preferredHeight: 120
                wallpapers: root.backend ? root.backend.wallpapers : []
                selectedId: root.backend ? root.backend.selectedId : ""
                onSelectRequested: function(wallpaperId) {
                    if (root.backend) root.backend.selectWallpaper(wallpaperId)
                }
            }
        }
    }
}