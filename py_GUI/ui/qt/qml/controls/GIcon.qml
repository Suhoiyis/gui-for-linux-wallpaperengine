import QtQuick
import "../Theme.js" as Theme
import "../icons/Icons.js" as Icons

Item {
    id: root

    property string name: ""
    property int size: 16
    property color color: Theme.fg

    implicitWidth: size
    implicitHeight: size

    Canvas {
        id: canvas
        anchors.fill: parent
        onPaint: {
            var ctx = getContext("2d")
            ctx.clearRect(0, 0, width, height)

            var data = Icons.get(root.name)
            if (!data) return

            var scale = root.size / 24
            var sw = Math.max(1, scale * 2)

            ctx.save()
            ctx.scale(scale, scale)
            ctx.strokeStyle = root.color
            ctx.lineWidth = sw / scale
            ctx.lineCap = "round"
            ctx.lineJoin = "round"
            ctx.fillStyle = "transparent"

            // Draw paths
            if (data.paths) {
                for (var i = 0; i < data.paths.length; i++) {
                    ctx.beginPath()
                    ctx.stroke(data.paths[i])
                }
            }

            // Draw circles
            if (data.circles) {
                for (var j = 0; j < data.circles.length; j++) {
                    var c = data.circles[j]
                    ctx.beginPath()
                    ctx.arc(c.cx, c.cy, c.r, 0, Math.PI * 2)
                    ctx.stroke()
                }
            }

            // Draw rects
            if (data.rects) {
                for (var k = 0; k < data.rects.length; k++) {
                    var r = data.rects[k]
                    ctx.beginPath()
                    if (r.rx > 0) {
                        roundedRect(ctx, r.x, r.y, r.w, r.h, r.rx)
                    } else {
                        ctx.rect(r.x, r.y, r.w, r.h)
                    }
                    ctx.stroke()
                }
            }

            // Draw lines
            if (data.lines) {
                for (var l = 0; l < data.lines.length; l++) {
                    var ln = data.lines[l]
                    ctx.beginPath()
                    ctx.moveTo(ln.x1, ln.y1)
                    ctx.lineTo(ln.x2, ln.y2)
                    ctx.stroke()
                }
            }

            ctx.restore()
        }

        function roundedRect(ctx, x, y, w, h, r) {
            ctx.moveTo(x + r, y)
            ctx.lineTo(x + w - r, y)
            ctx.arcTo(x + w, y, x + w, y + r, r)
            ctx.lineTo(x + w, y + h - r)
            ctx.arcTo(x + w, y + h, x + w - r, y + h, r)
            ctx.lineTo(x + r, y + h)
            ctx.arcTo(x, y + h, x, y + h - r, r)
            ctx.lineTo(x, y + r)
            ctx.arcTo(x, y, x + r, y, r)
            ctx.closePath()
        }

        Connections {
            target: root
            function onNameChanged() { canvas.requestPaint() }
            function onSizeChanged() { canvas.requestPaint() }
            function onColorChanged() { canvas.requestPaint() }
        }
    }
}
