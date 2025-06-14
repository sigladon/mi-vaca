from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLineEdit, QWidget, QPushButton

from src.vista.ui.registrarse_ui import Ui_VentanaRegistrarse


class Registrarse(QWidget):
    solicitar_mostrar_login = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.ui = Ui_VentanaRegistrarse()
        self.ui.setupUi(self)
        self.ui.btn_mostrar_contrasenia.setIcon(QIcon("./assets/iconos/visible.svg"))
        self.ui.btn_mostrar_repetir_contrasenia.setIcon(QIcon("./assets/iconos/visible.svg"))

        self.ui.btn_mostrar_contrasenia.clicked.connect(
            lambda: self._mostrar_ocultar_contrasenia(self.ui.txt_contrasenia)
        )
        self.ui.btn_mostrar_repetir_contrasenia.clicked.connect(
            lambda: self._mostrar_ocultar_contrasenia(self.ui.txt_repetir_contrasenia)
        )

    def _mostrar_ocultar_contrasenia(self, componente_txt):
        componente_btn: QPushButton = self.sender()
        if componente_txt.echoMode() == QLineEdit.EchoMode.Password:
            componente_txt.setEchoMode(QLineEdit.EchoMode.Normal)
            componente_btn.setIcon(QIcon("./assets/iconos/oculto.svg"))
            componente_btn.setText("Ocultar")
        else:
            componente_txt.setEchoMode(QLineEdit.EchoMode.Password)
            componente_btn.setIcon(QIcon("./assets/iconos/visible.svg"))
            componente_btn.setText("Mostrar")

    def emitir_solicitar_mostrar_login(self):
        self.solicitar_mostrar_login.emit()