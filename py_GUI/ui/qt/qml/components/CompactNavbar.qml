import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root

    signal switchToNormal()

    color: "#1f2335"
    border.width: 1
    border.color: "#2f344b"
    radius: 12
    implicitHeight: 50

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
        spacing: 8

        Button {
            text: "🗖"
            width: 34
            height: 34
            onClicked: root.switchToNormal()
            ToolTip.visible: hovered
            ToolTip.text: "Switch to Normal Mode"
        }

        Item { Layout.fillWidth: true }
    }
}
