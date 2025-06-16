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
        self.ui.btn_olvide_contrasenia.hide()
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5; /* Un gris claro para el fondo */
            }

            QLabel {
                font-size: 14px;
                color: #333333;
                margin-bottom: 5px;
            }

            QLineEdit {
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-size: 14px;
                background-color: #ffffff;
                color: #333333;
            }

            QLineEdit:focus {
                border: 1px solid #007bff; /* Color azul para el enfoque */
            }

            QPushButton {
                background-color: #007bff; /* Azul vibrante para botones primarios */
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #0056b3; /* Azul más oscuro al pasar el ratón */
            }

            QPushButton#btn_registrarse, QPushButton#btn_olvide_contrasenia {
                background-color: transparent;
                color: #007bff;
                border: none;
                font-weight: normal;
                text-align: right; /* Alinea el texto a la derecha */
            }

            QPushButton#btn_registrarse:hover, QPushButton#btn_olvide_contrasenia:hover {
                text-decoration: underline;
            }
            
            QPushButton#btn_mostrar_ocultar_contrasenia {
                background-color: #6c757d; /* Gris para el botón de mostrar/ocultar */
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
            }
            
            QPushButton#btn_mostrar_ocultar_contrasenia:hover {
                background-color: #5a6268;
            }
        """)


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