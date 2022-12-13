from pathlib import Path

try:
    from PySide5 import QtGui, QtWidgets, QtCore
    from PySide5.QtCore import Signal, Slot


except ModuleNotFoundError:
    from PyQt5 import QtGui, QtWidgets, QtCore
    from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot


def project_root() -> Path:
    return Path(__file__).parent


def resource_dir() -> Path:
    return project_root() / "resource"
