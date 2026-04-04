import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root

    property string message: ""
    property bool visibleToast: false
    property int durationMs: 2200

    function show(msg) {
        if (!msg || msg.length === 0) return
        message = msg
        visibleToast = true
        hideTimer.restart()
    }

    Timer {
        id: hideTimer
        interval: root.durationMs
        repeat: false
        onTriggered: root.visibleToast = false
    }

    Rectangle {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20
        radius: 10
        color: "#2f344bdd"
        border.width: 1
        border.color: "#565f89"
        visible: root.visibleToast
        opacity: root.visibleToast ? 1 : 0
        Behavior on opacity { NumberAnimation { duration: 150 } }

        implicitWidth: Math.max(180, toastText.implicitWidth + 24)
        implicitHeight: toastText.implicitHeight + 14

        Label {
            id: toastText
            anchors.centerIn: parent
            text: root.message
            color: "#c0caf5"
            font.pixelSize: 12
        }
    }
}
