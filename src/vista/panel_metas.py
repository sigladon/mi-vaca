from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from src.vista.overlay_meta import OverlayMeta
from src.vista.ui.panel_metas_ui import Ui_PanelMetas


class PanelMetas(QWidget):
    solicitar_mostrar_login = pyqtSignal()
    def __init__(self, usuario):
        super().__init__()

        self._usuario = usuario
        self._ui = Ui_PanelMetas()
        self._ui.setupUi(self)
        self._ui.btn_nueva_meta.clicked.connect(self.mostrar_modal)


    def mostrar_modal(self):
        self.overlay = OverlayMeta(self)
        self.overlay.show()

    def ocultar_modal(self):
        self.overlay.hide()


