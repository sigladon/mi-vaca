import uuid
from PyQt6.QtCore import QObject, pyqtSlot
import re

from PyQt6.QtWidgets import QToolTip, QLineEdit

from src.modelo.usuario import Usuario
from src.utils.manejador_archivos import ManejadorArchivos


class CPresupuestos(QObject):
    def __init__(self):
        super().__init__()
        self._correo_regex = re.compile(r'^[\w.%+-]+@[\w.-]+(\.[a-zA-Z]{2,})+$')

    @pyqtSlot(str, QLineEdit)
    def verificar_nombre_presupuesto(self, nombre, txt_nombre):
        if not self._correo_regex.match(nombre):
            print("Correo inválido (desde controlador)") # Para depuración
            # Mostrar QToolTip
            txt_nombre.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            return False
        else:
            print(f"Correo '{txt_nombre}' es válido. (desde controlador)") # Para depuración
            # Si era inválido y ahora es válido, ocultar cualquier tooltip anterior
            txt_nombre.setStyleSheet("")
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

