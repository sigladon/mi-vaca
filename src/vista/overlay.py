from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame


class Overlay(QWidget):
    def __init__(self, ui, parent=None):
        super().__init__(parent)
        if parent:
            self.setGeometry(parent.rect())
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.fondo = QFrame(self)
        self.fondo.setStyleSheet("background-color: rgba(0,0,0,128);")
        self.fondo.setGeometry(self.rect())
        self.fondo.lower()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0,0,0,0)

        self.modal = QFrame()
        self.modal.setObjectName("modal")
        self.modal.setFixedSize(500,400)
        self.modal.setStyleSheet("""
            QFrame {
                background-color: #f1f1f1;
                border-radius: 10px;
            }
        """)

        self._ui = ui
        self._ui.setupUi(self.modal)

        layout.addWidget(self.modal)
        self.modal.raise_()

        self._ui.btn_cerrar_modal.clicked.connect(parent.ocultar_modal)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.fondo.setGeometry(self.rect())