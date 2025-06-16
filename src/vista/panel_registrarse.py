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
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5; /* Un gris claro para el fondo */
            }

            QLabel {
                font-size: 14px;
                color: #333333;
                margin-bottom: 5px;
            }
            
            QLabel#lbl_titulo {
                font-size: 24px;
                font-weight: bold;
                color: #007bff; /* Color principal para el título */
                text-align: center;
                margin-bottom: 20px;
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
                margin-top: 10px; /* Espacio superior para botones */
            }

            QPushButton:hover {
                background-color: #0056b3; /* Azul más oscuro al pasar el ratón */
            }

            QPushButton#btn_volver {
                background-color: transparent;
                color: #6c757d; /* Gris para el botón de volver */
                border: 1px solid #6c757d; /* Borde sutil */
                font-weight: normal;
            }

            QPushButton#btn_volver:hover {
                background-color: #e2e6ea; /* Un poco de fondo al pasar el ratón */
                text-decoration: none;
            }
            
            QPushButton#btn_mostrar_contrasenia, QPushButton#btn_mostrar_repetir_contrasenia {
                background-color: #6c757d; /* Gris para el botón de mostrar/ocultar */
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
            }
            
            QPushButton#btn_mostrar_contrasenia:hover, QPushButton#btn_mostrar_repetir_contrasenia:hover {
                background-color: #5a6268;
            }
        """)


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