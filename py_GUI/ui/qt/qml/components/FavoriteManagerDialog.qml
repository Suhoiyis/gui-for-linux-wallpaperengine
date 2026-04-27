import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Dialog {
    id: root

    property var backend
    property var rows: []
    modal: true
    title: "Favorite Manager"
    width: 560
    height: 480

    background: Rectangle {
        radius: Theme.radiusXl
        color: Theme.elevated
        border.width: 1
        border.color: Theme.border
    }

    // Custom header
    header: Rectangle {
        height: 60
        color: "transparent"

        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: Theme.spaceLg
            anchors.rightMargin: Theme.spaceLg
            spacing: Theme.spaceSm

            Ctrl.GIcon {
                name: "star"
                size: Theme.fontSizeXl
                color: Theme.favoriteGold
            }

            ColumnLayout {
                Layout.fillWidth: true
                spacing: 0

                Label {
                    text: "Favorite Manager"
                    color: Theme.fg
                    font.pixelSize: Theme.fontSizeLg
                    font.bold: true
                }

                Label {
                    text: (root.rows.length) + " favorite" + (root.rows.length !== 1 ? "s" : "")
                    color: Theme.fgMuted
                    font.pixelSize: Theme.fontSizeXs
                }
            }
        }
    }

    function rebuildRows() {
        var arr = []
        if (!root.backend) {
            root.rows = arr
            return
        }
        var fav = root.backend.favoriteIds || []
        var all = root.backend.wallpapers || []
        for (var i = 0; i < fav.length; i++) {
            var id = fav[i]
            var title = id
            for (var j = 0; j < all.length; j++) {
                if (all[j].id === id) {
                    title = all[j].title || id
                    break
                }
            }
            arr.push({ wallpaperId: id, title: title, selected: false })
        }
        arr.sort(function(a, b) { return String(a.title).localeCompare(String(b.title)) })
        root.rows = arr
    }

    onOpened: rebuildRows()

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceMd

        // Toolbar
        RowLayout {
            Layout.fillWidth: true
            Ctrl.GButton {
                text: "Select All"
                variant: "ghost"
                sizeVariant: "sm"
                onClicked: {
                    var arr = root.rows.slice()
                    for (var i = 0; i < arr.length; i++) arr[i].selected = true
                    root.rows = arr
                }
            }
            Ctrl.GButton {
                text: "Deselect All"
                variant: "ghost"
                sizeVariant: "sm"
                onClicked: {
                    var arr = root.rows.slice()
                    for (var i = 0; i < arr.length; i++) arr[i].selected = false
                    root.rows = arr
                }
            }
            Item { Layout.fillWidth: true }
            Ctrl.GButton {
                text: "Remove Selected" + (selectedCount() > 0 ? " (" + selectedCount() + ")" : "")
                variant: "destructive"
                sizeVariant: "sm"
                enabled: selectedCount() > 0
                onClicked: {
                    if (root.backend) {
                        for (var i = 0; i < root.rows.length; i++) {
                            if (root.rows[i].selected) root.backend.toggleFavorite(root.rows[i].wallpaperId)
                        }
                    }
                    root.rebuildRows()
                }
            }
        }

        // List with rounded border
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: Theme.radiusLg
            color: Theme.surface
            border.width: 1
            border.color: Theme.border

            ListView {
                anchors.fill: parent
                anchors.margins: 1
                clip: true
                model: root.rows
                spacing: Theme.spaceXs

                delegate: Rectangle {
                    required property var modelData
                    required property int index
                    width: ListView.view.width - Theme.spaceMd * 2
                    x: Theme.spaceMd
                    height: 56
                    radius: Theme.radiusMd
                    color: modelData.selected ? Theme.withAlpha(Theme.favoriteGold, 0.1) : "transparent"
                    border.width: modelData.selected ? 1 : 0
                    border.color: Theme.withAlpha(Theme.favoriteGold, 0.5)

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: Theme.spaceSm
                        anchors.rightMargin: Theme.spaceSm
                        spacing: Theme.spaceSm

                        CheckBox {
                            checked: modelData.selected
                            onToggled: {
                                var arr = root.rows.slice()
                                arr[index].selected = checked
                                root.rows = arr
                            }
                        }

                        Rectangle {
                            width: 36
                            height: 36
                            radius: Theme.radiusSm
                            color: Theme.elevated

                            Ctrl.GIcon {
                                name: "image"
                                size: Theme.fontSizeMd
                                color: Theme.fgMuted
                                anchors.centerIn: parent
                            }
                        }

                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 0

                            Label {
                                text: modelData.title
                                color: Theme.fg
                                font.pixelSize: Theme.fontSizeSm
                                font.weight: Theme.fontWeightMedium
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                            }

                            Label {
                                text: "ID: " + modelData.wallpaperId
                                color: Theme.fgMuted
                                font.pixelSize: Theme.fontSizeXs
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                            }
                        }

                        Ctrl.GIcon {
                            name: "star"
                            size: Theme.fontSizeMd
                            color: Theme.favoriteGold
                        }
                    }
                }

                // Empty state
                Label {
                    anchors.centerIn: parent
                    visible: parent.count === 0
                    text: "No favorites yet"
                    color: Theme.fgMuted
                    font.pixelSize: Theme.fontSizeMd
                }
            }
        }

        // Footer
        RowLayout {
            Layout.fillWidth: true
            Item { Layout.fillWidth: true }
            Ctrl.GButton {
                text: "Close"
                variant: "outline"
                onClicked: root.close()
            }
        }
    }

    function selectedCount() {
        var count = 0
        for (var i = 0; i < root.rows.length; i++) {
            if (root.rows[i].selected) count++
        }
        return count
    }
}