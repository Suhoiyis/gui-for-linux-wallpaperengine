import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root

    property var backend

    Rectangle {
        anchors.fill: parent
        color: "#1a1b26"

        ScrollView {
            anchors.fill: parent
            anchors.margins: 12
            contentWidth: availableWidth

            ColumnLayout {
                width: parent.width
                spacing: 12

                Label {
                    text: "System Monitor"
                    color: "#c0caf5"
                    font.pixelSize: 20
                    font.bold: true
                }

                Label {
                    text: "Real-time resource usage of wallpaper components."
                    color: "#8a90b8"
                    font.pixelSize: 12
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8

                    Frame {
                        Layout.fillWidth: true
                        ColumnLayout {
                            anchors.fill: parent
                            Label { text: "Total CPU"; color: "#8a90b8" }
                            Label {
                                text: root.backend ? String(root.backend.performanceTotal.cpu_fmt || "0%") : "0%"
                                color: "#c0caf5"
                                font.pixelSize: 18
                                font.bold: true
                            }
                        }
                    }

                    Frame {
                        Layout.fillWidth: true
                        ColumnLayout {
                            anchors.fill: parent
                            Label { text: "Total Memory"; color: "#8a90b8" }
                            Label {
                                text: root.backend ? String(root.backend.performanceTotal.memory_fmt || "0 MB") : "0 MB"
                                color: "#c0caf5"
                                font.pixelSize: 18
                                font.bold: true
                            }
                        }
                    }

                    Frame {
                        Layout.fillWidth: true
                        ColumnLayout {
                            anchors.fill: parent
                            Label { text: "Threads"; color: "#8a90b8" }
                            Label {
                                text: root.backend ? String(root.backend.performanceTotal.threads || 0) : "0"
                                color: "#c0caf5"
                                font.pixelSize: 18
                                font.bold: true
                            }
                        }
                    }
                }

                Frame {
                    Layout.fillWidth: true
                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 8

                        Label {
                            text: "Process Details"
                            color: "#9aa5ce"
                            font.pixelSize: 12
                            font.bold: true
                        }

                        Repeater {
                            model: root.backend ? root.backend.performanceProcesses : []
                            delegate: Frame {
                                required property var modelData
                                Layout.fillWidth: true

                                RowLayout {
                                    anchors.fill: parent
                                    spacing: 10

                                    Label {
                                        text: (modelData.category || "process") + " (" + String(modelData.pid || 0) + ")"
                                        color: "#c0caf5"
                                        font.bold: true
                                        Layout.fillWidth: true
                                    }
                                    Label {
                                        text: String(modelData.cpu_fmt || "0%")
                                        color: "#fda4af"
                                        Layout.preferredWidth: 80
                                    }
                                    Label {
                                        text: String(modelData.memory_fmt || "0 MB")
                                        color: "#93c5fd"
                                        Layout.preferredWidth: 100
                                    }
                                    Label {
                                        text: String(modelData.status || "")
                                        color: "#8a90b8"
                                        Layout.preferredWidth: 100
                                    }
                                }
                            }
                        }

                        Label {
                            visible: (root.backend ? root.backend.performanceProcesses.length : 0) === 0
                            text: "No active monitored processes"
                            color: "#8a90b8"
                        }
                    }
                }
            }
        }
    }
}
