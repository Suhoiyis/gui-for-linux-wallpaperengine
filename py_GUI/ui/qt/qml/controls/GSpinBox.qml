import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme

SpinBox {
    id: root

    font.pixelSize: Theme.fontSizeMd

    background: Rectangle {
        radius: Theme.radiusMd
        color: Theme.input
        border.width: 1
        border.color: root.activeFocus ? Theme.accent : Theme.border

        Behavior on border.color { ColorAnimation { duration: Theme.animNormal } }
    }

    contentItem: TextInput {
        text: root.value
        font.pixelSize: Theme.fontSizeMd
        color: Theme.fg
        horizontalAlignment: Qt.AlignHCenter
        verticalAlignment: Qt.AlignVCenter
        readOnly: !root.editable
        validator: root.validator
        inputMethodHints: Qt.ImhDigitsOnly
    }

    up.indicator: Rectangle {
        x: root.width - height
        height: root.height / 2
        width: height
        radius: Theme.radiusSm
        color: root.up.hovered ? Theme.borderHover : Theme.elevated
        border.width: 1
        border.color: Theme.border

        Text {
            text: "+"
            font.pixelSize: Theme.fontSizeMd
            color: Theme.fg
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    down.indicator: Rectangle {
        x: root.width - height
        y: root.height / 2
        height: root.height / 2
        width: height
        radius: Theme.radiusSm
        color: root.down.hovered ? Theme.borderHover : Theme.elevated
        border.width: 1
        border.color: Theme.border

        Text {
            text: "-"
            font.pixelSize: Theme.fontSizeMd
            color: Theme.fg
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
}