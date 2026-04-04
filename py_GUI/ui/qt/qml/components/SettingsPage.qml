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
                    text: "Settings"
                    color: "#c0caf5"
                    font.pixelSize: 20
                    font.bold: true
                }

                Frame {
                    Layout.fillWidth: true
                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 10

                        Label {
                            text: "Playback"
                            color: "#9aa5ce"
                            font.pixelSize: 12
                            font.bold: true
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            Label {
                                text: "FPS"
                                color: "#c0caf5"
                                Layout.preferredWidth: 140
                            }
                            Slider {
                                id: fpsSlider
                                Layout.fillWidth: true
                                from: 1
                                to: 144
                                stepSize: 1
                                value: root.backend ? root.backend.fps : 30
                                onMoved: {
                                    if (root.backend) root.backend.setFps(Math.round(value))
                                }
                            }
                            Label {
                                text: String(Math.round(fpsSlider.value))
                                color: "#8a90b8"
                                Layout.preferredWidth: 42
                            }
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            Label {
                                text: "Scaling"
                                color: "#c0caf5"
                                Layout.preferredWidth: 140
                            }
                            ComboBox {
                                id: scalingCombo
                                Layout.fillWidth: true
                                model: ["default", "fit", "fill", "stretch"]
                                Component.onCompleted: {
                                    if (!root.backend) return
                                    var idx = model.indexOf(root.backend.scaling)
                                    currentIndex = idx >= 0 ? idx : 0
                                }
                                onActivated: {
                                    if (root.backend) root.backend.setScaling(currentText)
                                }
                            }
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            Label {
                                text: "Clamping"
                                color: "#c0caf5"
                                Layout.preferredWidth: 140
                            }
                            ComboBox {
                                id: clampingCombo
                                Layout.fillWidth: true
                                model: ["clamp", "repeat", "border", "mirror"]
                                Component.onCompleted: {
                                    if (!root.backend) return
                                    var idx = model.indexOf(root.backend.clamping)
                                    currentIndex = idx >= 0 ? idx : 0
                                }
                                onActivated: {
                                    if (root.backend) root.backend.setClamping(currentText)
                                }
                            }
                        }
                    }
                }

                Frame {
                    Layout.fillWidth: true
                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 10

                        Label {
                            text: "Audio"
                            color: "#9aa5ce"
                            font.pixelSize: 12
                            font.bold: true
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            Label {
                                text: "Volume"
                                color: "#c0caf5"
                                Layout.preferredWidth: 140
                            }
                            Slider {
                                id: volumeSlider
                                Layout.fillWidth: true
                                from: 0
                                to: 100
                                stepSize: 1
                                value: root.backend ? root.backend.volume : 0
                                onMoved: {
                                    if (root.backend) root.backend.setVolume(Math.round(value))
                                }
                            }
                            Label {
                                text: String(Math.round(volumeSlider.value))
                                color: "#8a90b8"
                                Layout.preferredWidth: 42
                            }
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            Label {
                                text: "Silence"
                                color: "#c0caf5"
                                Layout.preferredWidth: 140
                            }
                            Switch {
                                id: silenceSwitch
                                checked: root.backend ? root.backend.silence : true
                                onToggled: {
                                    if (root.backend) root.backend.setSilence(checked)
                                }
                            }
                        }
                    }
                }

                Frame {
                    Layout.fillWidth: true
                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 10

                        Label {
                            text: "Library"
                            color: "#9aa5ce"
                            font.pixelSize: 12
                            font.bold: true
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            Label {
                                text: "Workshop Path"
                                color: "#c0caf5"
                                Layout.preferredWidth: 140
                            }
                            TextField {
                                id: workshopPathField
                                Layout.fillWidth: true
                                text: root.backend ? root.backend.workshopPath : ""
                                selectByMouse: true
                            }
                            Button {
                                text: "Save"
                                onClicked: {
                                    if (root.backend) root.backend.setWorkshopPath(workshopPathField.text)
                                }
                            }
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            Label {
                                text: "Apply Mode"
                                color: "#c0caf5"
                                Layout.preferredWidth: 140
                            }
                            Switch {
                                checked: root.backend ? root.backend.linkedMode : false
                                text: checked ? "same" : "diff"
                                onToggled: {
                                    if (root.backend) root.backend.setLinkedMode(checked)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
