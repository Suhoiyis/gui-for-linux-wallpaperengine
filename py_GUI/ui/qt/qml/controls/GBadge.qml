import QtQuick
import "../Theme.js" as Theme
import "." as Controls

Rectangle {
    id: root

    property string text: ""
    property string icon: ""
    property string colorScheme: "slate"

    readonly property var _colors: ({
        "slate":   { bg: Theme.overlay, fg: Theme.fgMuted },
        "amber":   { bg: Theme.withAlpha(Theme.idOrange, 0.15), fg: Theme.idOrange },
        "rose":    { bg: Theme.withAlpha(Theme.sizePink, 0.15), fg: Theme.sizePink },
        "sky":     { bg: Theme.withAlpha(Theme.typeBlue, 0.15), fg: Theme.typeBlue },
        "brand":   { bg: Theme.brand10, fg: Theme.brand },
        "success": { bg: Theme.withAlpha(Theme.success, 0.15), fg: Theme.success },
        "danger":  { bg: Theme.destructive10, fg: Theme.destructive }
    })
    readonly property var _scheme: _colors[colorScheme] || _colors["slate"]

    color: _scheme.bg
    radius: Theme.radiusPill
    implicitWidth: _row.implicitWidth + Theme.spaceSm * 2
    implicitHeight: 20

    Row {
        id: _row
        anchors.centerIn: parent
        spacing: Theme.spaceXs

        Controls.GIcon {
            visible: root.icon !== ""
            name: root.icon
            size: 12
            color: root._scheme.fg
            anchors.verticalCenter: parent.verticalCenter
        }

        Text {
            text: root.text
            font.pixelSize: Theme.fontSizeXs
            font.weight: Theme.fontWeightMedium
            color: root._scheme.fg
            verticalAlignment: Text.AlignVCenter
        }
    }
}
