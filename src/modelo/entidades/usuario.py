import hashlib
import uuid
from dataclasses import dataclass, field

from src.modelo.entidades.categoria import Categoria
from src.modelo.entidades.meta import Meta
from src.modelo.entidades.movimiento import Movimiento
from src.modelo.entidades.presupuesto import Presupuesto

@dataclass
class Usuario:
    username: str
    contrasenia: str
    nombre: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correo: list[str] = field(default_factory=list)
    movimientos: list[Movimiento] = field(default_factory=list)
    presupuestos: list[Presupuesto] = field(default_factory=list)
    metas: list[Meta] = field(default_factory=list)
    categorias: list[Categoria] = field(default_factory=list)

    def agregar_movimiento(self, movimiento: Movimiento):
        self.movimientos.append(movimiento)

    def agregar_presupuesto(self, presupuesto: Presupuesto):
        self.presupuestos.append(presupuesto)

    def agregar_meta(self, meta: Meta):
        self.metas.append(meta)

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        """Verifica si la contraseña proporcionada es correcta"""
        return self.contrasenia == self.hashear_contrasenia(contrasenia)

    def establecer_contrasenia(self, contrasenia: str):
        """Establece una nueva contraseñá"""
        self.contrasenia = self.hashear_contrasenia(contrasenia)

    @staticmethod
    def hashear_contrasenia(contrasenia: str) -> str:
        """Hashea una contraseña usando SHA-256"""
        return hashlib.sha256(contrasenia.encode()).hexdigest()