from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLineEdit, QWidget

from src.vista.ui.login_ui import Ui_VentanaIniciarSesion


class Login(QWidget):

    solicitar_mostrar_registro = pyqtSignal()
    solicitar_mostrar_bienvenida = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_VentanaIniciarSesion()
        self.ui.setupUi(self)
        self.ui.btn_mostrar_ocultar_contrasenia.setIcon(QIcon("./assets/iconos/visible.svg"))
        self.ui.btn_mostrar_ocultar_contrasenia.clicked.connect(self.mostrar_ocultar_contrasenia)

    def mostrar_ocultar_contrasenia(self):
        if self.ui.txt_contrasenia.echoMode() == QLineEdit.EchoMode.Password:
            self.ui.txt_contrasenia.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.btn_mostrar_ocultar_contrasenia.setIcon(QIcon("./assets/iconos/oculto.svg"))
            self.ui.btn_mostrar_ocultar_contrasenia.setText("Ocultar")
        else:
            self.ui.txt_contrasenia.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.btn_mostrar_ocultar_contrasenia.setIcon(QIcon("./assets/iconos/visible.svg"))
            self.ui.btn_mostrar_ocultar_contrasenia.setText("Mostrar")

    def emitir_solicitar_mostrar_registro(self):
        self.solicitar_mostrar_registro.emit()

    def emitir_solicitar_mostrar_bienvenida(self):
        self.solicitar_mostrar_bienvenida.emit()