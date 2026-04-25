import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme
import "../controls" as Ctrl

Item {
    id: root

    property string message: ""
    property bool visibleToast: false
    property int durationMs: Theme.toastDuration

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
        anchors.bottomMargin: Theme.spaceXl
        radius: Theme.radiusLg
        color: "#2f344bdd"
        border.width: 1
        border.color: Theme.textMuted
        visible: root.visibleToast
        opacity: root.visibleToast ? 1 : 0
        Behavior on opacity { NumberAnimation { duration: Theme.animToast } }

        implicitWidth: Math.max(180, toastText.implicitWidth + Theme.space2xl)
        implicitHeight: toastText.implicitHeight + Theme.spaceMd

        RowLayout {
            anchors.centerIn: parent
            spacing: Theme.spaceSm

            Label {
                id: toastText
                Layout.fillWidth: true
                text: root.message
                color: Theme.textPrimary
                font.pixelSize: Theme.fontSizeMd
            }

            Ctrl.GIconButton {
                text: "×"
                size: Theme.iconButtonSm
                onClicked: root.visibleToast = false
            }
        }
    }
}