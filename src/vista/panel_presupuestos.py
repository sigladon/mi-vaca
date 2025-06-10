from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from src.controlador.c_transacciones import CTransacciones
from src.vista.overlay_presupuesto import OverlayPresupuesto
from src.vista.ui.panel_presupuestos_ui import Ui_PanelPresupuestos


class PanelPresupuesto(QWidget):
    solicitar_mostrar_login = pyqtSignal()
    def __init__(self, usuario):
        super().__init__()

        self.overlay = None
        self._usuario = usuario
        self._controlador = CTransacciones(self._usuario)
        self._ui = Ui_PanelPresupuestos()
        self._ui.setupUi(self)
        self._ui.btn_agregar_presupuesto.clicked.connect(self.mostrar_modal)


    def mostrar_modal(self):
        self.overlay = OverlayPresupuesto(self._controlador, self)
        self.overlay.show()

    def ocultar_modal(self):
        self.overlay.hide()


