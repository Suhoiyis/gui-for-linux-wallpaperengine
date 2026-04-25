import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../Theme.js" as Theme

Frame {
    id: root

    property var backend
    property string filterSource: "All"

    background: Rectangle {
        color: Theme.panelBg
        radius: Theme.radiusXl
        border.width: 1
        border.color: Theme.panelBorder
    }
    padding: Theme.spaceMd

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceSm

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "Logs"
                color: Theme.textSection
                font.pixelSize: Theme.fontSizeMd
                font.bold: true
            }
            Item { Layout.fillWidth: true }
            Ctrl.GComboBox {
                id: sourceFilter
                model: ["All", "GUI", "Core", "Engine", "Controller"]
                currentIndex: 0
                onActivated: root.filterSource = currentText
            }
            Ctrl.GButton {
                text: "Clear"
                onClicked: if (root.backend) root.backend.clearLogs()
            }
        }

        ListView {
            Layout.fillWidth: true
            Layout.preferredHeight: Theme.spaceXl * 11
            clip: true
            model: {
                if (!root.backend || !root.backend.logs) return []
                if (root.filterSource === "All") return root.backend.logs
                var out = []
                for (var i = 0; i < root.backend.logs.length; i++) {
                    if (String(root.backend.logs[i].source || "") === root.filterSource) out.push(root.backend.logs[i])
                }
                return out
            }

            delegate: Rectangle {
                required property var modelData
                required property int index
                width: ListView.view.width
                height: 32
                color: index % 2 === 0 ? Theme.rowEven : Theme.rowOdd

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: Theme.spaceSm
                    anchors.rightMargin: Theme.spaceSm
                    spacing: Theme.spaceSm

                    Label { text: modelData.timestamp || ""; color: Theme.textSecondary; Layout.preferredWidth: Theme.spaceXl * 6.5; elide: Text.ElideRight }
                    Label { text: modelData.level || ""; color: Theme.textPrimary; Layout.preferredWidth: Theme.spaceXl * 3.5 }
                    Label { text: modelData.source || ""; color: Theme.accent; Layout.preferredWidth: Theme.spaceXl * 4.5 }
                    Label { text: modelData.message || ""; color: Theme.textBody; Layout.fillWidth: true; elide: Text.ElideRight }
                }
            }
        }
    }
}