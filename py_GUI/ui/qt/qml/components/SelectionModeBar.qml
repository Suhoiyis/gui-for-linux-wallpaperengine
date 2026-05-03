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
    property var themeBridge
    property var tb: themeBridge || null

    color: tb ? tb.cRowSelected : Theme.rowSelected
    border.width: 0
    radius: Theme.radiusLg
    implicitHeight: 48

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: Theme.spaceSm
        anchors.rightMargin: Theme.spaceSm
        spacing: Theme.spaceSm

        Label {
            text: root.selectedCount + " selected"
            color: tb ? tb.cFg : Theme.fg
            font.bold: true
        }

        Item { Layout.fillWidth: true }

        Ctrl.GButton {
            themeBridge: root.themeBridge
            text: "Select All"
            onClicked: root.selectAllRequested()
        }

        Ctrl.GButton {
            themeBridge: root.themeBridge
            text: "Deselect"
            onClicked: root.deselectRequested()
        }

        Ctrl.GComboBox {
            themeBridge: root.themeBridge
            id: playlistCombo
            model: root.playlists
            textRole: "name"
            valueRole: "id"
            Layout.preferredWidth: 180
        }

        Ctrl.GButton {
            themeBridge: root.themeBridge
            text: "Add to Playlist"
            enabled: root.selectedCount > 0 && playlistCombo.count > 0
            onClicked: {
                if (playlistCombo.currentIndex >= 0 && playlistCombo.currentIndex < playlistCombo.count) {
                    root.addToPlaylistRequested(playlistCombo.model[playlistCombo.currentIndex].id)
                }
            }
        }

        Ctrl.GButton {
            themeBridge: root.themeBridge
            text: "Create Playlist"
            variant: "brand"
            enabled: root.selectedCount > 0
            onClicked: root.createPlaylistFromSelectionRequested()
        }

        Ctrl.GButton {
            themeBridge: root.themeBridge
            text: "Cancel"
            onClicked: root.cancelRequested()
        }
    }
}