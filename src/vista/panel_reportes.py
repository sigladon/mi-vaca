from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from src.vista.ui.panel_bienvenida_ui import Ui_PanelBienvenida
from src.vista.ui.panel_reportes_ui import Ui_PanelReportes


class PanelReportes(QWidget):
    solicitar_mostrar_login = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.ui = Ui_PanelReportes()
        self.ui.setupUi(self)




