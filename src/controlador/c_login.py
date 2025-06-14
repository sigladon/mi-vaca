from PyQt6.QtCore import QObject, pyqtSlot
import re

from PyQt6.QtWidgets import QLineEdit

from src.modelo.entidades.autenticacion import Autenticacion
from src.utils.manejador_archivos import ManejadorArchivos


class CLogin(QObject):
    def __init__(self, modelo):
        super().__init__()
        self._modelo = modelo
        self._p = re.compile(r'^[\w.%+-]+@[\w.-]+(\.[a-zA-Z]{2,})+$')

    @pyqtSlot(str, QLineEdit)
    def verificar_correo(self, correo, correo_line_edit):
        if not self._p.match(correo):
            print("Correo inválido (desde controlador)") # Para depuración
            # Mostrar QToolTip
            correo_line_edit.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            return False
        else:
            print(f"Correo '{correo}' es válido. (desde controlador)") # Para depuración
            # Si era inválido y ahora es válido, ocultar cualquier tooltip anterior
            correo_line_edit.setStyleSheet("")
            return True

    @pyqtSlot(str, str, QLineEdit)
    def verificar_credenciales(self, correo_ingresado, contrasenia_ingresada, contrasenia_line_edit):
        usuarios = ManejadorArchivos.cargar_archivo("usuarios", dict())

        registro_usuario = usuarios.get(correo_ingresado)
        contrasenia_usuario = registro_usuario.get("contrasenia")

        if registro_usuario is None:
            print("No existe ningún usuario registrado con ese correo")
            return False

        if contrasenia_usuario == contrasenia_ingresada:
            contrasenia_line_edit.setStyleSheet("")
            print("Ingresó el usuario")
            token = Autenticacion(registro_usuario.get("uuid"))
            ManejadorArchivos.guardar_archivo("token", token)
            return True
        else:
            contrasenia_line_edit.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            return False