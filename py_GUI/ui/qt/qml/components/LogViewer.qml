import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Frame {
    id: root

    property var backend
    property string filterSource: "All"

    ColumnLayout {
        anchors.fill: parent
        spacing: 8

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "Logs"
                color: "#9aa5ce"
                font.pixelSize: 12
                font.bold: true
            }
            Item { Layout.fillWidth: true }
            ComboBox {
                id: sourceFilter
                model: ["All", "GUI", "Core", "Engine", "Controller"]
                currentIndex: 0
                onActivated: root.filterSource = currentText
            }
            Button {
                text: "Clear"
                onClicked: if (root.backend) root.backend.clearLogs()
            }
        }

        ListView {
            Layout.fillWidth: true
            Layout.preferredHeight: 220
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
                height: 28
                color: index % 2 === 0 ? "#1f2335" : "#1b1f2f"

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 8
                    anchors.rightMargin: 8
                    spacing: 8

                    Label { text: modelData.timestamp || ""; color: "#8a90b8"; Layout.preferredWidth: 130; elide: Text.ElideRight }
                    Label { text: modelData.level || ""; color: "#c0caf5"; Layout.preferredWidth: 70 }
                    Label { text: modelData.source || ""; color: "#7aa2f7"; Layout.preferredWidth: 90 }
                    Label { text: modelData.message || ""; color: "#a9b1d6"; Layout.fillWidth: true; elide: Text.ElideRight }
                }
            }
        }
    }
}
