import QtQuick
import QtQuick.Controls

Item {
    id: root

    property var wallpapers: []
    property string selectedId: ""
    property int columns: 5
    property int cellGap: 12
    property bool showTitle: true
    property bool showIcons: true

    signal selectRequested(string wallpaperId)
    signal applyRequested(string wallpaperId)
    signal favoriteToggled(string wallpaperId)

    GridView {
        id: gridView
        anchors.fill: parent

        model: root.wallpapers
        clip: true

        cellWidth: Math.max(220, Math.floor((width - ((root.columns - 1) * root.cellGap)) / root.columns))
        cellHeight: Math.floor(cellWidth * 0.86)

        delegate: WallpaperCard {
            width: gridView.cellWidth - root.cellGap
            height: gridView.cellHeight - root.cellGap

            wp: modelData
            showTitle: root.showTitle
            showIcons: root.showIcons
            isSelected: root.selectedId === modelData.id

            onSelected: root.selectRequested(modelData.id)
            onApplyRequested: root.applyRequested(modelData.id)
            onFavoriteToggled: root.favoriteToggled(modelData.id)
        }

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AsNeeded
        }
    }

    Label {
        anchors.centerIn: parent
        visible: !gridView.count
        text: "No wallpapers found"
        color: "#8a90b8"
    }
}
