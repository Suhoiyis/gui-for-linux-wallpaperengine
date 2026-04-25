import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Dialog {
    id: root

    property var backend
    modal: true
    title: "Play History"
    standardButtons: Dialog.Close
    width: 560
    height: 500

    background: Rectangle {
        radius: Theme.radiusXl
        color: Theme.panelBg
        border.width: 1
        border.color: Theme.panelBorder
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spaceSm

        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            model: root.backend ? root.backend.history : []

            delegate: Rectangle {
                required property var modelData
                width: ListView.view.width
                height: 58
                color: model.index % 2 === 0 ? Theme.rowEven : Theme.rowOdd

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: Theme.spaceSm
                    anchors.rightMargin: Theme.spaceSm

                    Label {
                        text: modelData.title || "Unknown"
                        color: Theme.textPrimary
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }

                    Label {
                        text: modelData.id || ""
                        color: Theme.textSecondary
                        font.pixelSize: Theme.fontSizeSm
                        Layout.preferredWidth: 120
                        elide: Text.ElideRight
                    }

                    Ctrl.GButton {
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
            Ctrl.GButton {
                text: "Clear History"
                enabled: (root.backend ? root.backend.history.length : 0) > 0
                onClicked: {
                    if (root.backend) root.backend.clearHistory()
                }
            }
        }
    }
}