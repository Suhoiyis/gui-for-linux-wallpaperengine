import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Theme.js" as Theme

Rectangle {
    id: root

    property var screens: []
    property var backend
    property string selectedScreen: ""
    property bool linkedMode: false
    property string currentPage: "library" // library | performance | settings

    signal selectedScreenChangedByUser(string screen)
    signal linkedModeChangedByUser(bool linked)
    signal pageChanged(string page)
    signal appMenuHistoryRequested()
    signal appMenuAboutRequested()
    signal appMenuUpdateRequested()
    signal appMenuWelcomeRequested()
    signal appMenuQuitRequested()

    color: Theme.panelBg
    border.width: 1
    border.color: Theme.panelBorder
    radius: 12
    implicitHeight: 50

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
        spacing: 8

        RowLayout {
            spacing: 8

            Button {
                visible: root.screens.length > 1
                text: root.linkedMode ? "🔗" : "⛓"
                width: 34
                height: 34
                onClicked: root.linkedModeChangedByUser(!root.linkedMode)
            }

            Label {
                text: "🖥"
                color: "#8a90b8"
                font.pixelSize: 12
            }

            ComboBox {
                id: screenCombo
                model: root.screens
                implicitWidth: 180

                Component.onCompleted: {
                    var idx = root.screens.indexOf(root.selectedScreen)
                    currentIndex = idx >= 0 ? idx : 0
                }

                onActivated: {
                    if (currentIndex >= 0 && currentIndex < root.screens.length) {
                        root.selectedScreenChangedByUser(root.screens[currentIndex])
                    }
                }

                Connections {
                    target: root
                    function onSelectedScreenChanged() {
                        var idx = root.screens.indexOf(root.selectedScreen)
                        if (idx >= 0) {
                            screenCombo.currentIndex = idx
                        }
                    }
                }
            }
        }

        Item { Layout.fillWidth: true }

        RowLayout {
            spacing: 6

            AppMenu {
                backend: root.backend
                onShowHistoryRequested: root.appMenuHistoryRequested()
                onShowAboutRequested: root.appMenuAboutRequested()
                onShowUpdateRequested: root.appMenuUpdateRequested()
                onShowWelcomeRequested: root.appMenuWelcomeRequested()
                onRequestQuitConfirm: root.appMenuQuitRequested()
            }

            Button {
                text: "🏠"
                width: 36
                height: 36
                highlighted: root.currentPage === "library"
                onClicked: root.pageChanged("library")
            }

            Button {
                text: "📈"
                width: 36
                height: 36
                highlighted: root.currentPage === "performance"
                onClicked: root.pageChanged("performance")
            }

            Button {
                text: "⚙"
                width: 36
                height: 36
                highlighted: root.currentPage === "settings"
                onClicked: root.pageChanged("settings")
            }

            Button {
                text: "🪟"
                width: 36
                height: 36
                highlighted: root.currentPage === "compact"
                onClicked: root.pageChanged("compact")
            }
        }
    }
}
