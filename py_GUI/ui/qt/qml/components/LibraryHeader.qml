import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../Theme.js" as Theme

Rectangle {
    id: root

    property string currentTitle: "None"
    property int totalCount: 0
    property string sortBy: "name"
    property string searchText: ""
    property bool selectionMode: false

    signal searchChanged(string value)
    signal sortSelected(string value)
    signal refreshRequested()
    signal randomRequested()
    signal screenshotRequested()
    signal historyRequested()
    signal selectionModeToggled()

    radius: Theme.radiusXl
    color: Theme.panelBg
    border.width: 1
    border.color: Theme.panelBorder
    implicitHeight: 66

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: Theme.spaceMd
        anchors.rightMargin: Theme.spaceMd
        spacing: Theme.spaceSm

        ColumnLayout {
            Layout.fillWidth: true
            spacing: Theme.spaceXs

            Label {
                text: "CURRENTLY USING"
                color: Theme.accent
                font.pixelSize: Theme.fontSizeXs
                font.bold: true
            }

            Label {
                text: root.currentTitle && root.currentTitle.length > 0 ? root.currentTitle : "None"
                color: Theme.textPrimary
                font.pixelSize: Theme.fontSizeMd
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
        }

        Label {
            text: root.totalCount + " wallpapers"
            color: Theme.textSecondary
            font.pixelSize: Theme.fontSizeSm
        }

        Ctrl.GComboBox {
            id: sortBox
            model: ["name", "id", "size"]
            currentIndex: {
                if (root.sortBy === "id") return 1
                if (root.sortBy === "size") return 2
                return 0
            }

            onActivated: {
                root.sortSelected(currentText)
            }
        }

        Ctrl.GTextField {
            id: searchField
            placeholderText: "Search wallpapers"
            text: root.searchText
            implicitWidth: 220

            onTextEdited: {
                root.searchChanged(text)
            }
        }

        StatefulButton {
            text: "Refresh"
            onClicked: root.refreshRequested()
        }

        Ctrl.GButton {
            text: "Random"
            onClicked: root.randomRequested()
        }

        Ctrl.GButton {
            text: "Screenshot"
            onClicked: root.screenshotRequested()
        }

        Ctrl.GButton {
            text: "History"
            onClicked: root.historyRequested()
        }

        Ctrl.GButton {
            text: root.selectionMode ? "Cancel Select" : "Select"
            highlighted: root.selectionMode
            onClicked: root.selectionModeToggled()
        }
    }
}