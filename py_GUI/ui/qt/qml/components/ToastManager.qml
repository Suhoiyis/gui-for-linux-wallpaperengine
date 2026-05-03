import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../effects" as Effects
import "../Theme.js" as Theme

Item {
    id: root

    property string message: ""
    property bool visibleToast: false
    property int durationMs: Theme.toastDuration
    property var themeBridge
    property var tb: themeBridge || null

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

    Effects.GBackdropBlur {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: Theme.spaceXl
        radius: Theme.radiusLg
        tintColor: tb ? tb.cOverlay : Theme.overlay
        tintOpacity: 0.95
        border.width: 0
        visible: root.visibleToast
        opacity: root.visibleToast ? 1 : 0
        Behavior on opacity { NumberAnimation { duration: Theme.animToast } }

        implicitWidth: Math.max(180, toastText.implicitWidth + Theme.space2xl)
        implicitHeight: toastText.implicitHeight + Theme.spaceMd

        y: root.visibleToast ? 0 : 8
        Behavior on y { NumberAnimation { duration: Theme.animToast; easing.type: Easing.OutCubic } }

        // Shadow for toast
        Effects.GDropShadow {
            shadowWidth: parent.width
            shadowHeight: parent.height
            radius: Theme.radiusLg
            color: Theme.withAlpha("#000000", 0.15)
            spread: 4
            verticalOffset: 2
        }

        RowLayout {
            anchors.centerIn: parent
            spacing: Theme.spaceSm

            Text {
                id: toastText
                Layout.fillWidth: true
                text: root.message
                color: tb ? tb.cFg : Theme.fg
                font.pixelSize: Theme.fontSizeMd
            }

            Ctrl.GIconButton {
                themeBridge: root.themeBridge
                iconName: "x"
                size: Theme.iconButtonSm
                onClicked: root.visibleToast = false
            }
        }
    }
}
