import uuid
from PyQt6.QtCore import QObject, pyqtSlot
import re

from PyQt6.QtWidgets import QToolTip, QLineEdit

from src.modelo.usuario import Usuario
from src.utils.manejador_archivos import ManejadorArchivos


class CPresupuestos(QObject):
    def __init__(self):
        super().__init__()
        self._nombre_regex = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{1,25}$')
        self._descripcion_regex = re.compile(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s.,;:!?-_\']{1,250}$')

    @pyqtSlot(str, QLineEdit)
    def verificar_nombre_presupuesto(self, nombre, txt_nombre):
        if not self._nombre_regex.match(nombre):
            print("Nombre no válido para el presupuesto") # Para depuración
            txt_nombre.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            return False
        else:
            txt_nombre.setStyleSheet("")
            return True

    @pyqtSlot(str, QLineEdit)
    def verificar_nombre_presupuesto(self, desc, txt_desc):
        if not self._descripcion_regex.match(desc):
            print("Descripción no válida. Ingresó caracteres no permitidos") # Para depuración
            txt_desc.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            return False
        else:
            txt_desc.setStyleSheet("")
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

