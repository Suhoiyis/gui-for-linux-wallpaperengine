import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../Theme.js" as Theme

Item {
    id: root

    property int currentPage: 1
    property int totalPages: 1

    signal pageChangedByUser(int page)

    implicitHeight: root.totalPages > 1 ? 44 : 0

    RowLayout {
        anchors.centerIn: parent
        spacing: Theme.spaceSm
        visible: root.totalPages > 1

        Ctrl.GIconButton {
            iconName: "chevronRight"
            size: Theme.iconButtonSm
            enabled: root.currentPage > 1
            onClicked: root.pageChangedByUser(root.currentPage - 1)
        }

        Label {
            text: "Page " + root.currentPage + " / " + root.totalPages
            color: Theme.fgMuted
        }

        Ctrl.GTextField {
            id: jumpInput
            placeholderText: "Page..."
            implicitWidth: 60
            horizontalAlignment: Text.AlignHCenter
            inputMethodHints: Qt.ImhDigitsOnly
            onAccepted: {
                var target = parseInt(text)
                if (!isNaN(target) && target >= 1 && target <= root.totalPages) {
                    root.pageChangedByUser(target)
                }
                text = ""
            }
        }

        Ctrl.GIconButton {
            iconName: "chevronDown"
            size: Theme.iconButtonSm
            enabled: root.currentPage < root.totalPages
            onClicked: root.pageChangedByUser(root.currentPage + 1)
        }
    }
}