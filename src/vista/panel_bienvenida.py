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
        self.setStyleSheet("""

            QLabel {
                color: #263238; /* Un gris oscuro para el texto */
                text-align: center;
            }

            QLabel#label { /* Estilo específico para el QLabel "Bienvenido/a" */
                font-size: 36px; /* Letra grande */
                font-weight: bold;
                color: #00796b; /* Un verde azulado fuerte */
                padding-bottom: 10px; /* Espacio inferior para separarlo del nombre de usuario */
            }

            QLabel#lbl_nombre_usuario { /* Estilo específico para el QLabel del nombre de usuario */
                font-size: 30px; /* Un poco más pequeño que el principal pero aún grande */
                font-weight: bold;
                color: #004d40; /* Un verde azulado más oscuro */
                margin-top: 10px; /* Espacio superior para separarlo del texto "Bienvenido/a" */
            }
        """)




