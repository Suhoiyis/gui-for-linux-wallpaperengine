import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme

Item {
    id: root

    property var backend

    Rectangle {
        anchors.fill: parent
        color: Theme.windowBg

        ScrollView {
            anchors.fill: parent
            anchors.margins: Theme.spaceMd
            contentWidth: availableWidth

            ColumnLayout {
                width: parent.width
                spacing: Theme.spaceMd

                Label {
                    text: "System Monitor"
                    color: Theme.textPrimary
                    font.pixelSize: Theme.fontSize3xl
                    font.bold: true
                }

                Label {
                    text: "Real-time resource usage of wallpaper components."
                    color: Theme.textSecondary
                    font.pixelSize: Theme.fontSizeMd
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: Theme.spaceSm

                    Frame {
                        Layout.fillWidth: true
                        ColumnLayout {
                            anchors.fill: parent
                            Label { text: "Total CPU"; color: Theme.textSecondary }
                            Label {
                                text: root.backend ? String(root.backend.performanceTotal.cpu_fmt || "0%") : "0%"
                                color: Theme.textPrimary
                                font.pixelSize: Theme.fontSize2xl
                                font.bold: true
                            }
                            SparklineChart {
                                Layout.fillWidth: true
                                Layout.preferredHeight: Theme.spaceXl * 2.3
                                values: {
                                    var hist = root.backend && root.backend.performanceTotal ? root.backend.performanceTotal.history : null
                                    return hist && hist.cpu ? hist.cpu : []
                                }
                                maxValue: 100
                            }
                        }
                    }

                    Frame {
                        Layout.fillWidth: true
                        ColumnLayout {
                            anchors.fill: parent
                            Label { text: "Total Memory"; color: Theme.textSecondary }
                            Label {
                                text: root.backend ? String(root.backend.performanceTotal.memory_fmt || "0 MB") : "0 MB"
                                color: Theme.textPrimary
                                font.pixelSize: Theme.fontSize2xl
                                font.bold: true
                            }
                            SparklineChart {
                                Layout.fillWidth: true
                                Layout.preferredHeight: Theme.spaceXl * 2.3
                                lineColor: Theme.typeBlue
                                fillColor: "#93c5fd22"
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

                    Frame {
                        Layout.fillWidth: true
                        ColumnLayout {
                            anchors.fill: parent
                            Label { text: "Threads"; color: Theme.textSecondary }
                            Label {
                                text: root.backend ? String(root.backend.performanceTotal.threads || 0) : "0"
                                color: Theme.textPrimary
                                font.pixelSize: Theme.fontSize2xl
                                font.bold: true
                            }
                        }
                    }
                }

                Frame {
                    Layout.fillWidth: true
                    ColumnLayout {
                        anchors.fill: parent
                        spacing: Theme.spaceSm

                        Label {
                            text: "Process Details"
                            color: Theme.textSection
                            font.pixelSize: Theme.fontSizeMd
                            font.bold: true
                        }

                        Repeater {
                            model: root.backend ? root.backend.performanceProcesses : []
                            delegate: Frame {
                                required property var modelData
                                Layout.fillWidth: true

                                RowLayout {
                                    anchors.fill: parent
                                    spacing: Theme.spaceSm

                                    Label {
                                        text: (modelData.category || "process") + " (" + String(modelData.pid || 0) + ")"
                                        color: Theme.textPrimary
                                        font.bold: true
                                        Layout.fillWidth: true
                                    }
                                    Label {
                                        text: String(modelData.cpu_fmt || "0%")
                                        color: Theme.sizePink
                                        Layout.preferredWidth: Theme.spaceXl * 4
                                    }
                                    Label {
                                        text: String(modelData.memory_fmt || "0 MB")
                                        color: Theme.typeBlue
                                        Layout.preferredWidth: Theme.spaceXl * 5
                                    }
                                    Label {
                                        text: String(modelData.status || "")
                                        color: Theme.textSecondary
                                        Layout.preferredWidth: Theme.spaceXl * 5
                                    }
                                }
                            }
                        }

                        Label {
                            visible: (root.backend ? root.backend.performanceProcesses.length : 0) === 0
                            text: "No active monitored processes"
                            color: Theme.textSecondary
                        }
                    }
                }
            }
        }
    }
}