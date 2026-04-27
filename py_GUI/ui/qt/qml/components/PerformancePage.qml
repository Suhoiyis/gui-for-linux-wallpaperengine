import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
import "../effects" as Effects
import "../Theme.js" as Theme

Item {
    id: root

    property var backend

    Rectangle {
        anchors.fill: parent
        color: Theme.bg

        ScrollView {
            anchors.fill: parent
            anchors.margins: Theme.spaceMd
            contentWidth: availableWidth
            clip: true

            ColumnLayout {
                width: parent.width
                spacing: Theme.spaceLg

                // Header
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: Theme.spaceXs

                    Text {
                        text: "System Monitor"
                        color: Theme.fg
                        font.pixelSize: Theme.fontSize2xl
                        font.weight: Theme.fontWeightBold
                    }

                    Text {
                        text: "Real-time resource usage of wallpaper components."
                        color: Theme.fgMuted
                        font.pixelSize: Theme.fontSizeSm
                    }
                }

                // Stats cards row
                RowLayout {
                    Layout.fillWidth: true
                    spacing: Theme.spaceMd

                    // CPU card
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 180
                        radius: Theme.radiusLg
                        color: Theme.surface
                        border.width: 1
                        border.color: Theme.border

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: Theme.spaceMd
                            spacing: Theme.spaceSm

                            RowLayout {
                                Layout.fillWidth: true
                                spacing: Theme.spaceSm

                                Rectangle {
                                    radius: Theme.radiusSm
                                    color: Theme.withAlpha("#a855f7", 0.15)
                                    width: 32
                                    height: 32

                                    Ctrl.GIcon {
                                        name: "activity"
                                        size: Theme.fontSizeMd
                                        color: "#a855f7"
                                        anchors.centerIn: parent
                                    }
                                }

                                ColumnLayout {
                                    Layout.fillWidth: true
                                    spacing: 0

                                    Text {
                                        text: "Total CPU"
                                        color: Theme.fgMuted
                                        font.pixelSize: Theme.fontSizeSm
                                    }

                                    Text {
                                        text: root.backend ? String(root.backend.performanceTotal.cpu_fmt || "0%") : "0%"
                                        color: Theme.fg
                                        font.pixelSize: Theme.fontSizeXl
                                        font.weight: Theme.fontWeightBold
                                    }
                                }
                            }

                            Item { Layout.fillHeight: true }

                            SparklineChart {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 60
                                lineColor: "#a855f7"
                                fillColor: Theme.withAlpha("#a855f7", 0.10)
                                values: {
                                    var hist = root.backend && root.backend.performanceTotal ? root.backend.performanceTotal.history : null
                                    return hist && hist.cpu ? hist.cpu : []
                                }
                                maxValue: 100
                            }
                        }
                    }

                    // Memory card
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 180
                        radius: Theme.radiusLg
                        color: Theme.surface
                        border.width: 1
                        border.color: Theme.border

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: Theme.spaceMd
                            spacing: Theme.spaceSm

                            RowLayout {
                                Layout.fillWidth: true
                                spacing: Theme.spaceSm

                                Rectangle {
                                    radius: Theme.radiusSm
                                    color: Theme.withAlpha("#06b6d4", 0.15)
                                    width: 32
                                    height: 32

                                    Ctrl.GIcon {
                                        name: "zap"
                                        size: Theme.fontSizeMd
                                        color: "#06b6d4"
                                        anchors.centerIn: parent
                                    }
                                }

                                ColumnLayout {
                                    Layout.fillWidth: true
                                    spacing: 0

                                    Text {
                                        text: "Total Memory"
                                        color: Theme.fgMuted
                                        font.pixelSize: Theme.fontSizeSm
                                    }

                                    Text {
                                        text: root.backend ? String(root.backend.performanceTotal.memory_fmt || "0 MB") : "0 MB"
                                        color: Theme.fg
                                        font.pixelSize: Theme.fontSizeXl
                                        font.weight: Theme.fontWeightBold
                                    }
                                }
                            }

                            Item { Layout.fillHeight: true }

                            SparklineChart {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 60
                                lineColor: "#06b6d4"
                                fillColor: Theme.withAlpha("#06b6d4", 0.10)
                                values: {
                                    var hist = root.backend && root.backend.performanceTotal ? root.backend.performanceTotal.history : null
                                    return hist && hist.memory_mb ? hist.memory_mb : []
                                }
                                maxValue: {
                                    var total = root.backend && root.backend.performanceTotal ? root.backend.performanceTotal.memory_mb : 1
                                    return Math.max(1, Number(total) * 1.5)
                                }
                            }
                        }
                    }

                    // Threads card
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 180
                        radius: Theme.radiusLg
                        color: Theme.surface
                        border.width: 1
                        border.color: Theme.border

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: Theme.spaceMd
                            spacing: Theme.spaceSm

                            RowLayout {
                                Layout.fillWidth: true
                                spacing: Theme.spaceSm

                                Rectangle {
                                    radius: Theme.radiusSm
                                    color: Theme.withAlpha("#10b981", 0.15)
                                    width: 32
                                    height: 32

                                    Ctrl.GIcon {
                                        name: "maximize2"
                                        size: Theme.fontSizeMd
                                        color: "#10b981"
                                        anchors.centerIn: parent
                                    }
                                }

                                ColumnLayout {
                                    Layout.fillWidth: true
                                    spacing: 0

                                    Text {
                                        text: "Active Threads"
                                        color: Theme.fgMuted
                                        font.pixelSize: Theme.fontSizeSm
                                    }

                                    Text {
                                        text: root.backend ? String(root.backend.performanceTotal.threads || 0) : "0"
                                        color: Theme.fg
                                        font.pixelSize: Theme.fontSizeXl
                                        font.weight: Theme.fontWeightBold
                                    }
                                }
                            }

                            Item { Layout.fillHeight: true }

                            // Mini bar chart placeholder
                            RowLayout {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 60
                                spacing: 2

                                Repeater {
                                    model: [40, 60, 30, 80, 50, 90, 20, 60]
                                    delegate: Rectangle {
                                        required property var modelData
                                        Layout.fillWidth: true
                                        Layout.fillHeight: true
                                        color: Theme.withAlpha("#10b981", 0.3)
                                        radius: 2

                                        Rectangle {
                                            anchors.bottom: parent.bottom
                                            anchors.left: parent.left
                                            anchors.right: parent.right
                                            height: parent.height * (modelData / 100)
                                            color: "#10b981"
                                            radius: 2
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                // Separator
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: Theme.border
                }

                // Process details section
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: Theme.spaceMd

                    Text {
                        text: "Process Details"
                        color: Theme.fg
                        font.pixelSize: Theme.fontSizeLg
                        font.weight: Theme.fontWeightBold
                    }

                    Repeater {
                        model: root.backend ? root.backend.performanceProcesses : []
                        delegate: Rectangle {
                            required property var modelData
                            Layout.fillWidth: true
                            implicitHeight: processColumn.implicitHeight + Theme.spaceMd * 2
                            radius: Theme.radiusLg
                            color: Theme.surface
                            border.width: 1
                            border.color: Theme.border

                            ColumnLayout {
                                id: processColumn
                                anchors.fill: parent
                                anchors.margins: Theme.spaceMd
                                spacing: Theme.spaceMd

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: Theme.spaceMd

                                    // Icon
                                    Rectangle {
                                        width: 48
                                        height: 48
                                        radius: Theme.radiusMd
                                        color: Theme.elevated

                                        Ctrl.GIcon {
                                            anchors.centerIn: parent
                                            name: modelData.category === "backend" ? "zap" : "monitor"
                                            size: Theme.fontSizeLg
                                            color: modelData.category === "backend" ? "#eab308" : Theme.brand
                                        }
                                    }

                                    // Name and PID
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        spacing: 0

                                        RowLayout {
                                            spacing: Theme.spaceSm

                                            Text {
                                                text: modelData.name || "Process"
                                                color: Theme.fg
                                                font.pixelSize: Theme.fontSizeMd
                                                font.weight: Theme.fontWeightBold
                                            }

                                            Rectangle {
                                                height: 18
                                                radius: Theme.radiusSm
                                                color: Theme.input
                                                border.width: 1
                                                border.color: Theme.border

                                                Text {
                                                    anchors.centerIn: parent
                                                    anchors.leftMargin: Theme.spaceSm
                                                    anchors.rightMargin: Theme.spaceSm
                                                    text: "PID: " + String(modelData.pid || 0)
                                                    color: Theme.fgMuted
                                                    font.pixelSize: Theme.fontSizeXs
                                                    font.family: "monospace"
                                                }

                                                implicitWidth: pidText.implicitWidth + Theme.spaceSm * 2
                                                Text {
                                                    id: pidText
                                                    visible: false
                                                    text: "PID: " + String(modelData.pid || 0)
                                                    font.pixelSize: Theme.fontSizeXs
                                                    font.family: "monospace"
                                                }
                                            }
                                        }

                                        Text {
                                            text: modelData.cmd || ""
                                            color: Theme.fgSubtle
                                            font.pixelSize: Theme.fontSizeXs
                                            elide: Text.ElideRight
                                            Layout.fillWidth: true
                                        }
                                    }

                                    // Stats
                                    RowLayout {
                                        spacing: Theme.spaceLg

                                        ColumnLayout {
                                            spacing: 0
                                            Text {
                                                text: String(modelData.cpu_fmt || "0%")
                                                color: {
                                                    var cpu = parseFloat(modelData.cpu || 0)
                                                    if (cpu > 20) return Theme.warning
                                                    return Theme.success
                                                }
                                                font.pixelSize: Theme.fontSizeSm
                                                font.weight: Theme.fontWeightBold
                                                font.family: "monospace"
                                            }
                                            Text {
                                                text: "CPU"
                                                color: Theme.fgMuted
                                                font.pixelSize: Theme.fontSizeXs - 2
                                            }
                                        }

                                        ColumnLayout {
                                            spacing: 0
                                            Text {
                                                text: String(modelData.memory_fmt || "0 MB")
                                                color: Theme.accent
                                                font.pixelSize: Theme.fontSizeSm
                                                font.weight: Theme.fontWeightBold
                                                font.family: "monospace"
                                            }
                                            Text {
                                                text: "MEM"
                                                color: Theme.fgMuted
                                                font.pixelSize: Theme.fontSizeXs - 2
                                            }
                                        }

                                        ColumnLayout {
                                            spacing: 0
                                            Text {
                                                text: String(modelData.status || "-")
                                                color: Theme.fgMuted
                                                font.pixelSize: Theme.fontSizeSm
                                                font.family: "monospace"
                                            }
                                            Text {
                                                text: "STATUS"
                                                color: Theme.fgMuted
                                                font.pixelSize: Theme.fontSizeXs - 2
                                            }
                                        }
                                    }
                                }

                                // Mini charts row
                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: Theme.spaceMd
                                    visible: modelData.cpuHistory && modelData.cpuHistory.length > 0

                                    Rectangle {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: 50
                                        color: Theme.input
                                        radius: Theme.radiusMd

                                        SparklineChart {
                                            anchors.fill: parent
                                            anchors.margins: Theme.spaceSm
                                            lineColor: {
                                                var cpu = parseFloat(modelData.cpu || 0)
                                                if (cpu > 20) return Theme.warning
                                                return Theme.success
                                            }
                                            fillColor: "transparent"
                                            values: modelData.cpuHistory || []
                                            maxValue: 100
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // Empty state
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 100
                        visible: (root.backend ? root.backend.performanceProcesses.length : 0) === 0
                        color: Theme.surface
                        radius: Theme.radiusLg
                        border.width: 1
                        border.color: Theme.border

                        Text {
                            anchors.centerIn: parent
                            text: "No active monitored processes"
                            color: Theme.fgSubtle
                            font.pixelSize: Theme.fontSizeSm
                        }
                    }
                }
            }
        }
    }
}
