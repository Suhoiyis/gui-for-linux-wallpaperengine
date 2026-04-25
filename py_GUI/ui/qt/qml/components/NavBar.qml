import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls" as Ctrl
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
    radius: Theme.radiusXl
    implicitHeight: Theme.navHeight

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: Theme.spaceMd
        anchors.rightMargin: Theme.spaceMd
        spacing: Theme.spaceSm

        RowLayout {
            spacing: Theme.spaceSm

            Ctrl.GIconButton {
                visible: root.screens.length > 1
                text: root.linkedMode ? "🔗" : "⛓"
                size: Theme.iconButtonMd
                onClicked: root.linkedModeChangedByUser(!root.linkedMode)
            }

            Label {
                text: "🖥"
                color: Theme.textSecondary
                font.pixelSize: Theme.fontSizeMd
            }

            Ctrl.GComboBox {
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
            spacing: Theme.spaceXs

            AppMenu {
                backend: root.backend
                onShowHistoryRequested: root.appMenuHistoryRequested()
                onShowAboutRequested: root.appMenuAboutRequested()
                onShowUpdateRequested: root.appMenuUpdateRequested()
                onShowWelcomeRequested: root.appMenuWelcomeRequested()
                onRequestQuitConfirm: root.appMenuQuitRequested()
            }

            Ctrl.GIconButton {
                text: "🏠"
                size: Theme.navButtonSize
                highlighted: root.currentPage === "library"
                onClicked: root.pageChanged("library")
            }

            Ctrl.GIconButton {
                text: "📈"
                size: Theme.navButtonSize
                highlighted: root.currentPage === "performance"
                onClicked: root.pageChanged("performance")
            }

            Ctrl.GIconButton {
                text: "⚙"
                size: Theme.navButtonSize
                highlighted: root.currentPage === "settings"
                onClicked: root.pageChanged("settings")
            }

            Ctrl.GIconButton {
                text: "🪟"
                size: Theme.navButtonSize
                highlighted: root.currentPage === "compact"
                onClicked: root.pageChanged("compact")
            }
        }
    }
}