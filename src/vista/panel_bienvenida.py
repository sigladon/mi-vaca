from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from src.vista.ui.panel_bienvenida_ui import Ui_PanelBienvenida


class PanelBienvenida(QWidget):
    solicitar_mostrar_login = pyqtSignal()
    def __init__(self, modelo):
        super().__init__()

        self._modelo = modelo
        self._ui = Ui_PanelBienvenida()
        self._ui.setupUi(self)
        self._ui.lbl_nombre_usuario.setText(self._modelo.nombre)




