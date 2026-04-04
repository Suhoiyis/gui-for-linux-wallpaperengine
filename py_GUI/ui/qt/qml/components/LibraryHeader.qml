import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

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
    signal historyRequested()
    signal selectionModeToggled()

    radius: 12
    color: "#1f2335"
    border.width: 1
    border.color: "#2f344b"
    implicitHeight: 66

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 14
        anchors.rightMargin: 14
        spacing: 10

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 2

            Label {
                text: "CURRENTLY USING"
                color: "#7aa2f7"
                font.pixelSize: 10
                font.bold: true
            }

            Label {
                text: root.currentTitle && root.currentTitle.length > 0 ? root.currentTitle : "None"
                color: "#c0caf5"
                font.pixelSize: 12
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
        }

        Label {
            text: root.totalCount + " wallpapers"
            color: "#8a90b8"
            font.pixelSize: 11
        }

        ComboBox {
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

        TextField {
            id: searchField
            placeholderText: "Search wallpapers"
            text: root.searchText
            implicitWidth: 220

            onTextEdited: {
                root.searchChanged(text)
            }
        }

        Button {
            text: "Refresh"
            onClicked: root.refreshRequested()
        }

        Button {
            text: "Random"
            onClicked: root.randomRequested()
        }

        Button {
            text: "History"
            onClicked: root.historyRequested()
        }

        Button {
            text: root.selectionMode ? "Cancel Select" : "Select"
            highlighted: root.selectionMode
            onClicked: root.selectionModeToggled()
        }
    }
}
