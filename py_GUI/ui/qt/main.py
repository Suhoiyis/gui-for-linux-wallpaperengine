#!/usr/bin/env python3
"""Qt Quick PoC 入口"""

import sys
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.insert(0, PROJECT_ROOT)

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QtMsgType, qInstallMessageHandler

from py_GUI.ui.qt.backend import Backend


def _qt_message_handler(mode, context, message):
    if mode in (QtMsgType.QtWarningMsg, QtMsgType.QtCriticalMsg, QtMsgType.QtFatalMsg):
        print(f"[Qt] {message}")


def main():
    qInstallMessageHandler(_qt_message_handler)
    app = QGuiApplication(sys.argv)
    app.setApplicationName("LWG Qt Quick PoC")

    engine = QQmlApplicationEngine()
    backend = Backend()
    engine.rootContext().setContextProperty("Backend", backend)

    qml_file = os.path.join(os.path.dirname(__file__), "qml", "Main.qml")
    engine.load(QUrl.fromLocalFile(qml_file))

    if not engine.rootObjects():
        print("Error: Failed to load QML file")
        return -1

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
