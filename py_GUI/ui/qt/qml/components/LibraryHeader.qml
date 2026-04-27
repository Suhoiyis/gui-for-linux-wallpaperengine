import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../effects" as Effects
import "../Theme.js" as Theme

Rectangle {
    id: root

    property string currentTitle: "None"
    property int totalCount: 0
    property string sortBy: "name"
    property string searchText: ""
    property bool selectionMode: false

    signal searchChanged(string value)
    signal sortSelected(string value)
    signal selectionModeToggled()

    radius: Theme.radiusXl
    color: Theme.elevated
    border.width: 1
    border.color: Theme.border
    implicitHeight: Theme.navHeight

    Effects.GDropShadow {
        shadowWidth: root.width
        shadowHeight: root.height
        radius: root.radius
        color: Theme.withAlpha("#000000", 0.08)
        spread: 2
        verticalOffset: 1
    }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: Theme.spaceMd
        anchors.rightMargin: Theme.spaceMd
        spacing: Theme.spaceSm

        ColumnLayout {
            Layout.fillWidth: true
            spacing: Theme.spaceXs

            Text {
                text: "CURRENTLY USING"
                color: Theme.brand
                font.pixelSize: Theme.fontSizeXs
                font.weight: Theme.fontWeightMedium
                font.letterSpacing: Theme.trackingWider
            }

            Text {
                text: root.currentTitle && root.currentTitle.length > 0 ? root.currentTitle : "None"
                color: Theme.fg
                font.pixelSize: Theme.fontSizeMd
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
        }

        Text {
            text: root.totalCount + " wallpapers"
            color: Theme.fgSubtle
            font.pixelSize: Theme.fontSizeSm
        }

        Ctrl.GComboBox {
            id: sortBox
            model: ["name", "id", "size"]
            currentIndex: {
                if (root.sortBy === "id") return 1
                if (root.sortBy === "size") return 2
                return 0
            }

            onActivated: {
                root.sortSelected(currentText)
            }
        }

        Ctrl.GButton {
            text: root.selectionMode ? "Cancel Select" : "Select"
            iconName: root.selectionMode ? "x" : "check"
            variant: root.selectionMode ? "destructive" : "outline"
            sizeVariant: "sm"
            onClicked: root.selectionModeToggled()
        }
    }
}
