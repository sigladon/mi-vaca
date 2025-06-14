import uuid

from PyQt6.QtCore import QObject, pyqtSlot
import re

from PyQt6.QtWidgets import QLineEdit

from src.modelo.entidades.usuario import Usuario
from src.utils.manejador_archivos import ManejadorArchivos


class CRegistro(QObject):
    def __init__(self):
        super().__init__()
        self._correo_regex = re.compile(r'^[\w.%+-]+@[\w.-]+(\.[a-zA-Z]{2,})+$')
        self._contrasenia_regex = re.compile(r'[\w.]{8,}$')

    @pyqtSlot(str, QLineEdit)
    def verificar_correo(self, correo, correo_line_edit):
        if not self._correo_regex.match(correo):
            print("Correo inválido (desde controlador)") # Para depuración
            # Mostrar QToolTip
            correo_line_edit.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            return False
        else:
            print(f"Correo '{correo}' es válido. (desde controlador)") # Para depuración
            # Si era inválido y ahora es válido, ocultar cualquier tooltip anterior
            correo_line_edit.setStyleSheet("")
            return True

    @pyqtSlot(str, str, QLineEdit, QLineEdit)
    def verificar_contrasenias(self, contrasenia, contrasenia_repetida, contrasenia_line_edit, repetir_contrasenia_line_edit):
        if not self._contrasenia_regex.match(contrasenia):
            print("La contraseña no cumple con los requisitos")
            contrasenia_line_edit.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            return False

        if contrasenia != contrasenia_repetida:
            print("Las contraseñas no coinciden")
            repetir_contrasenia_line_edit.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            return False


        contrasenia_line_edit.setStyleSheet("")
        repetir_contrasenia_line_edit.setStyleSheet("")
        return True

    @pyqtSlot(str, str, QLineEdit)
    def registrar_usuario(self, correo, contrasenia, nombre):
        usuarios = ManejadorArchivos.cargar_archivo("usuarios", dict())

        id_nuevo_usuario = str(uuid.uuid1())
        nuevo_usuario = Usuario(
            id_nuevo_usuario,
            correo,
            contrasenia,
            nombre
        )

        usuarios[correo] = {
            "contrasenia": contrasenia,
            "uuid": id_nuevo_usuario
        }
        ManejadorArchivos.guardar_archivo(id_nuevo_usuario, nuevo_usuario)
        ManejadorArchivos.guardar_archivo("usuarios", usuarios)

