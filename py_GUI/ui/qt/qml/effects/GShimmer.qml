import QtQuick
import "../Theme.js" as Theme

Rectangle {
    id: root

    property bool active: true

    color: Theme.elevated
    radius: Theme.radiusMd
    clip: true

    Canvas {
        id: shimmerCanvas
        anchors.fill: parent
        visible: root.active

        property real offset: -0.5

        NumberAnimation on offset {
            from: -0.5
            to: 1.5
            duration: 1500
            loops: Animation.Infinite
            running: root.active
            easing.type: Easing.InOutCubic
        }

        onOffsetChanged: requestPaint()

        onPaint: {
            var ctx = getContext("2d")
            ctx.clearRect(0, 0, width, height)

            var grad = ctx.createLinearGradient(0, 0, width, 0)
            var highlightPos = offset

            grad.addColorStop(0, Theme.elevated)
            grad.addColorStop(Math.max(0, highlightPos - 0.15), Theme.elevated)
            grad.addColorStop(Math.max(0, highlightPos), Theme.overlay)
            grad.addColorStop(Math.min(1, highlightPos + 0.15), Theme.elevated)
            grad.addColorStop(1, Theme.elevated)

            ctx.fillStyle = grad
            ctx.fillRect(0, 0, width, height)
        }
    }
}
