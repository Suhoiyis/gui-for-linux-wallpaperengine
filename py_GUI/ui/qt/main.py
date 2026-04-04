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
from PySide6.QtCore import QUrl

from py_GUI.ui.qt.backend import Backend


def main():
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
