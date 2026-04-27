import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../Theme.js" as Theme

Rectangle {
    id: root

    property int selectedCount: 0
    property int totalCount: 0
    property var playlists: []

    signal selectAllRequested()
    signal deselectRequested()
    signal cancelRequested()
    signal addToPlaylistRequested(string playlistId)
    signal createPlaylistFromSelectionRequested()

    color: Theme.rowSelected
    border.width: 1
    border.color: Theme.border
    radius: Theme.radiusLg
    implicitHeight: 48

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: Theme.spaceSm
        anchors.rightMargin: Theme.spaceSm
        spacing: Theme.spaceSm

        Label {
            text: root.selectedCount + " selected"
            color: Theme.fg
            font.bold: true
        }

        Item { Layout.fillWidth: true }

        Ctrl.GButton {
            text: "Select All"
            onClicked: root.selectAllRequested()
        }

        Ctrl.GButton {
            text: "Deselect"
            onClicked: root.deselectRequested()
        }

        Ctrl.GComboBox {
            id: playlistCombo
            model: root.playlists
            textRole: "name"
            valueRole: "id"
            Layout.preferredWidth: 180
        }

        Ctrl.GButton {
            text: "Add to Playlist"
            enabled: root.selectedCount > 0 && playlistCombo.count > 0
            onClicked: {
                if (playlistCombo.currentIndex >= 0 && playlistCombo.currentIndex < playlistCombo.count) {
                    root.addToPlaylistRequested(playlistCombo.model[playlistCombo.currentIndex].id)
                }
            }
        }

        Ctrl.GButton {
            text: "Create Playlist"
            variant: "brand"
            enabled: root.selectedCount > 0
            onClicked: root.createPlaylistFromSelectionRequested()
        }

        Ctrl.GButton {
            text: "Cancel"
            onClicked: root.cancelRequested()
        }
    }
}