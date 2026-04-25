import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../Theme.js" as Theme

Rectangle {
    id: root

    signal switchToNormal()

    color: Theme.panelBg
    border.width: 1
    border.color: Theme.panelBorder
    radius: Theme.radiusXl
    implicitHeight: Theme.navHeight

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: Theme.spaceMd
        anchors.rightMargin: Theme.spaceMd
        spacing: Theme.spaceSm

        Ctrl.GIconButton {
            text: "🗖"
            size: Theme.iconButtonMd
            onClicked: root.switchToNormal()
            ToolTip.visible: hovered
            ToolTip.text: "Switch to Normal Mode"
        }

        Item { Layout.fillWidth: true }
    }
}