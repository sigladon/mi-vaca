from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLineEdit, QWidget

from src.vista.ui.registrarse_ui import Ui_VentanaRegistrarse


class Registrarse(QWidget):
    solicitar_mostrar_login = pyqtSignal()
    def __init__(self, controlador):
        super().__init__()

        self._controlador = controlador
        self._ui = Ui_VentanaRegistrarse()
        self._ui.setupUi(self)
        self._ui.btn_mostrar_contrasenia.setIcon(QIcon("./assets/iconos/visible.svg"))
        self._ui.btn_mostrar_repetir_contrasenia.setIcon(QIcon("./assets/iconos/visible.svg"))

        self._correo_valido = False
        self._contrasenias_coinciden = False

        self._ui.txt_correo.editingFinished.connect(self.verificar_correo)
        self._ui.btn_mostrar_contrasenia.clicked.connect(
            lambda: self.mostrar_ocultar_contrasenia(self._ui.btn_mostrar_contrasenia, self._ui.txt_contrasenia)
        )
        self._ui.btn_mostrar_repetir_contrasenia.clicked.connect(
            lambda: self.mostrar_ocultar_contrasenia(self._ui.btn_mostrar_repetir_contrasenia, self._ui.txt_repetir_contrasenia)
        )
        self._ui.btn_registrarse.clicked.connect(self.registrarse)
        self._ui.txt_repetir_contrasenia.editingFinished.connect(self.verificar_contrasenias)
        self._ui.txt_contrasenia.editingFinished.connect(self.verificar_contrasenias)
        self._ui.btn_volver.clicked.connect(self.emitir_solicitar_mostrar_login)

    def verificar_correo(self):
        correo_ingresado = self._ui.txt_correo.text()
        self._correo_valido = self._controlador.verificar_correo(correo_ingresado, self._ui.txt_correo)

    def verificar_contrasenias(self):
        contrasenia = self._ui.txt_contrasenia.text()
        contrasenia_confirmada = self._ui.txt_repetir_contrasenia.text()
        self._contrasenias_coinciden = self._controlador.verificar_contrasenias(contrasenia, contrasenia_confirmada, self._ui.txt_contrasenia, self._ui.txt_repetir_contrasenia)

    def mostrar_ocultar_contrasenia(self, componente_btn, componente_txt):
        if componente_txt.echoMode() == QLineEdit.EchoMode.Password:
            componente_txt.setEchoMode(QLineEdit.EchoMode.Normal)
            componente_btn.setIcon(QIcon("./assets/iconos/oculto.svg"))
            componente_btn.setText("Ocultar")
        else:
            componente_txt.setEchoMode(QLineEdit.EchoMode.Password)
            componente_btn.setIcon(QIcon("./assets/iconos/visible.svg"))
            componente_btn.setText("Mostrar")

    def registrarse(self):
        if not self._correo_valido:
            print("Debe ingresar un correo válido")
            return

        correo = self._ui.txt_correo.text()

        if not self._contrasenias_coinciden:
            print("Las contraseñas no coinciden")
            return

        contrasenia = self._ui.txt_contrasenia.text()

        nombre = self._ui.txt_nombre.text()
        self._controlador.registrar_usuario(correo, contrasenia, nombre)
        self.emitir_solicitar_mostrar_login()

    def emitir_solicitar_mostrar_login(self):
        self.solicitar_mostrar_login.emit()

