import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../Theme.js" as Theme

Rectangle {
    id: root

    signal switchToNormal()
    property var themeBridge
    property var tb: themeBridge || null

    color: tb ? tb.cSurface : Theme.surface
    border.width: 0
    radius: Theme.radiusXl
    implicitHeight: Theme.navHeight

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: Theme.spaceMd
        anchors.rightMargin: Theme.spaceMd
        spacing: Theme.spaceSm

        Ctrl.GIconButton {
            themeBridge: root.themeBridge
            iconName: "maximize2"
            size: Theme.iconButtonMd
            tooltip: "Switch to Normal Mode"
            onClicked: root.switchToNormal()
        }

        Item { Layout.fillWidth: true }
    }
}
