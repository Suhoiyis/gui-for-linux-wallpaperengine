import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root

    property int currentPage: 1
    property int totalPages: 1

    signal pageChangedByUser(int page)

    implicitHeight: root.totalPages > 1 ? 44 : 0

    RowLayout {
        anchors.centerIn: parent
        spacing: 8
        visible: root.totalPages > 1

        Button {
            text: "◀"
            enabled: root.currentPage > 1
            onClicked: root.pageChangedByUser(root.currentPage - 1)
        }

        Label {
            text: "Page " + root.currentPage + " / " + root.totalPages
            color: "#8a90b8"
        }

        TextField {
            id: jumpInput
            placeholderText: String(root.currentPage)
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

        Button {
            text: "▶"
            enabled: root.currentPage < root.totalPages
            onClicked: root.pageChangedByUser(root.currentPage + 1)
        }
    }
}
