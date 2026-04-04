import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: root

    property var backend
    modal: true
    title: "Play History"
    standardButtons: Dialog.Close
    width: 560
    height: 500

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            model: root.backend ? root.backend.history : []

            delegate: Rectangle {
                required property var modelData
                width: ListView.view.width
                height: 58
                color: model.index % 2 === 0 ? "#1f2335" : "#1b1f2f"

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 10
                    anchors.rightMargin: 10

                    Label {
                        text: modelData.title || "Unknown"
                        color: "#c0caf5"
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }

                    Label {
                        text: modelData.id || ""
                        color: "#8a90b8"
                        font.pixelSize: 11
                        Layout.preferredWidth: 120
                        elide: Text.ElideRight
                    }

                    Button {
                        text: "Reuse"
                        onClicked: {
                            if (root.backend) {
                                root.backend.selectWallpaper(modelData.id)
                                root.backend.applyWallpaper(modelData.id)
                            }
                            root.close()
                        }
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Item { Layout.fillWidth: true }
            Button {
                text: "Clear History"
                enabled: (root.backend ? root.backend.history.length : 0) > 0
                onClicked: {
                    if (root.backend) root.backend.clearHistory()
                }
            }
        }
    }
}
