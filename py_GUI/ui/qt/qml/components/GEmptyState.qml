import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

ColumnLayout {
    id: root

    property string iconName: "search"
    property string title: "Empty"
    property string description: ""
    property string actionText: ""
    signal actionTriggered()

    spacing: Theme.spaceMd
    Layout.alignment: Qt.AlignHCenter

    Ctrl.GIcon {
        name: root.iconName
        size: Theme.fontSize2xl
        color: Theme.fgSubtle
        Layout.alignment: Qt.AlignHCenter
    }

    Text {
        text: root.title
        color: Theme.fgMuted
        font.pixelSize: Theme.fontSizeMd
        font.weight: Theme.fontWeightBold
        Layout.alignment: Qt.AlignHCenter
    }

    Text {
        text: root.description
        color: Theme.fgSubtle
        font.pixelSize: Theme.fontSizeSm
        Layout.alignment: Qt.AlignHCenter
        wrapMode: Text.WordWrap
        Layout.maximumWidth: 320
        horizontalAlignment: Text.AlignHCenter
    }

    Ctrl.GButton {
        text: root.actionText
        visible: root.actionText.length > 0
        onClicked: root.actionTriggered()
        Layout.alignment: Qt.AlignHCenter
    }
}