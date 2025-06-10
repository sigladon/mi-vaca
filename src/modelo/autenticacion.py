from PyQt6.QtCore import QObject

from src.utils.custom_error import CustomError
from src.utils.manejador_archivos import ManejadorArchivos


class Autenticacion():
    def __init__(self, uuid):
        super().__init__()
        self.uuid = uuid
