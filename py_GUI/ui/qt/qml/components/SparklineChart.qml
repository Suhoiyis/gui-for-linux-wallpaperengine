import QtQuick
import "../Theme.js" as Theme

Item {
    id: root

    property var values: []
    property color lineColor: tb ? tb.cAccent : Theme.accent
    property color fillColor: "#7aa2f722"
    property real maxValue: 100
    property var themeBridge
    property var tb: themeBridge || null

    Canvas {
        id: chart
        anchors.fill: parent
        onPaint: {
            var ctx = getContext("2d")
            ctx.clearRect(0, 0, width, height)

            var vals = root.values || []
            if (vals.length < 2) return

            var maxV = root.maxValue
            if (maxV <= 0) maxV = 1

            ctx.beginPath()
            for (var i = 0; i < vals.length; i++) {
                var x = (i / (vals.length - 1)) * width
                var y = height - (Math.max(0, Math.min(vals[i], maxV)) / maxV) * height
                if (i === 0) ctx.moveTo(x, y)
                else ctx.lineTo(x, y)
            }
            ctx.strokeStyle = root.lineColor
            ctx.lineWidth = 1.5
            ctx.stroke()

            ctx.lineTo(width, height)
            ctx.lineTo(0, height)
            ctx.closePath()
            ctx.fillStyle = root.fillColor
            ctx.fill()
        }

        Connections {
            target: root
            function onValuesChanged() { chart.requestPaint() }
            function onLineColorChanged() { chart.requestPaint() }
            function onFillColorChanged() { chart.requestPaint() }
            function onMaxValueChanged() { chart.requestPaint() }
        }
    }
}