import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root

    property int selectedCount: 0
    property int totalCount: 0
    property var playlists: []

    signal selectAllRequested()
    signal deselectRequested()
    signal cancelRequested()
    signal addToPlaylistRequested(string playlistId)

    color: "#252a3f"
    border.width: 1
    border.color: "#3b4261"
    radius: 10
    implicitHeight: 48

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        spacing: 8

        Label {
            text: root.selectedCount + " selected"
            color: "#c0caf5"
            font.bold: true
        }

        Item { Layout.fillWidth: true }

        Button {
            text: "Select All"
            onClicked: root.selectAllRequested()
        }

        Button {
            text: "Deselect"
            onClicked: root.deselectRequested()
        }

        ComboBox {
            id: playlistCombo
            model: root.playlists
            textRole: "name"
            valueRole: "id"
            Layout.preferredWidth: 180
        }

        Button {
            text: "Add to Playlist"
            enabled: root.selectedCount > 0 && playlistCombo.count > 0
            onClicked: {
                if (playlistCombo.currentIndex >= 0 && playlistCombo.currentIndex < playlistCombo.count) {
                    root.addToPlaylistRequested(playlistCombo.model[playlistCombo.currentIndex].id)
                }
            }
        }

        Button {
            text: "Cancel"
            onClicked: root.cancelRequested()
        }
    }
}
