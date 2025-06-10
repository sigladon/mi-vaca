from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLineEdit, QWidget

from src.vista.ui.login_ui import Ui_VentanaIniciarSesion


class Login(QWidget):

    solicitar_mostrar_registro = pyqtSignal()
    solicitar_mostrar_bienvenida = pyqtSignal()

    def __init__(self, modelo, controlador):
        super().__init__()

        self._modelo = modelo
        self._controlador = controlador
        self._ui = Ui_VentanaIniciarSesion()
        self._ui.setupUi(self)
        self._ui.btn_mostrar_ocultar_contrasenia.setIcon(QIcon("./assets/iconos/visible.svg"))
        self._correo_valido = False

        self._ui.txt_correo.editingFinished.connect(self.verificar_correo)
        self._ui.btn_mostrar_ocultar_contrasenia.clicked.connect(self.mostrar_ocultar_contrasenia)
        self._ui.btn_iniciar_sesion.clicked.connect(self.iniciar_sesion)
        self._ui.btn_registrarse.clicked.connect(self.emitir_solicitar_mostrar_registro)

    def verificar_correo(self):
        correo_ingresado = self._ui.txt_correo.text()
        self._correo_valido = self._controlador.verificar_correo(correo_ingresado, self._ui.txt_correo)

    def mostrar_ocultar_contrasenia(self):
        if self._ui.txt_contrasenia.echoMode() == QLineEdit.EchoMode.Password:
            self._ui.txt_contrasenia.setEchoMode(QLineEdit.EchoMode.Normal)
            self._ui.btn_mostrar_ocultar_contrasenia.setIcon(QIcon("./assets/iconos/oculto.svg"))
            self._ui.btn_mostrar_ocultar_contrasenia.setText("Ocultar")
        else:
            self._ui.txt_contrasenia.setEchoMode(QLineEdit.EchoMode.Password)
            self._ui.btn_mostrar_ocultar_contrasenia.setIcon(QIcon("./assets/iconos/visible.svg"))
            self._ui.btn_mostrar_ocultar_contrasenia.setText("Mostrar")

    def iniciar_sesion(self):
        if self._correo_valido:
            correo = self._ui.txt_correo.text()
            contrasenia = self._ui.txt_contrasenia.text()
            if self._controlador.verificar_credenciales(correo,contrasenia,self._ui.txt_contrasenia):
                self.emitir_solicitar_mostrar_bienvenida()
                print(f"Correo: {correo}\nContraseña: {contrasenia}")
        else:
            print("Debe ingresar un correo válido")

    def emitir_solicitar_mostrar_registro(self):
        self.solicitar_mostrar_registro.emit()

    def emitir_solicitar_mostrar_bienvenida(self):
        self.solicitar_mostrar_bienvenida.emit()