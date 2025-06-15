from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame

from src.vista.ui.overlay_meta_ui import Ui_OverlayMeta
from src.vista.ui.overlay_presupuesto_ui import Ui_OverlayPresupuesto
from src.vista.ui.overlay_transacciones_ui import Ui_OverlayTransaccion


class Overlay(QWidget):
    def __init__(self, ui: Ui_OverlayTransaccion | Ui_OverlayPresupuesto | Ui_OverlayMeta, parent=None):
        super().__init__(parent)
        self.ui = ui

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        if parent:
            self.setGeometry(parent.rect())

        self.fondo = QFrame(self)
        self.fondo.setStyleSheet("background-color: rgba(0,0,0,168);")
        self.fondo.setGeometry(0,0,self.width(), self.height())

        self.modal = QFrame(self)
        self.modal.setObjectName("modal")
        self.modal.setFixedSize(500,550)
        self.modal.setStyleSheet("""
            QFrame {
                background-color: #f1f1f1;
                border-radius: 10px;
            }
        """)

        self.ui.setupUi(self.modal)

        self._centrar_modal()
        self.ui.btn_cerrar_modal.clicked.connect(
            lambda: parent.ocultar_modal(True)
        )

        QTimer.singleShot(0, self.ajustar_a_padre)

        self.hide()

    def _centrar_modal(self):
        overlay_rect = self.rect()
        modal_rect = self.modal.rect()

        x = (overlay_rect.width() - modal_rect.width()) // 2
        y = (overlay_rect.height() - modal_rect.height()) // 2

        self.modal.move(x, y)

    def ajustar_a_padre(self):
        if self.parent():
            parent_rect = self.parent().rect()
            self.setGeometry(parent_rect)
            self.fondo.setGeometry(0, 0, parent_rect.width(), parent_rect.height())
            self._centrar_modal()
            self.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fondo.setGeometry(0,0,self.width(),self.height())
        self._centrar_modal()

    def showEvent(self, event):
        super().showEvent(event)
        self.ajustar_a_padre()

    def show(self):
        super().show()
        QTimer.singleShot(10, self.ajustar_a_padre)