import QtQuick
import QtQuick.Controls
import "../Theme.js" as Theme
import "../controls" as Ctrl

Ctrl.GButton {
    id: root

    property string idleText: text
    property string loadingText: "Loading..."
    property string successText: "Done"
    property int stateMode: 0 // 0 idle, 1 loading, 2 success

    text: {
        if (stateMode === 1) return loadingText
        if (stateMode === 2) return successText
        return idleText
    }

    enabled: stateMode !== 1

    Timer {
        id: successReset
        interval: 1200
        repeat: false
        onTriggered: root.stateMode = 0
    }

    function beginLoading() {
        stateMode = 1
    }

    function finishSuccess() {
        stateMode = 2
        successReset.restart()
    }

    function resetIdle() {
        stateMode = 0
    }
}