import uuid
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID

from src.modelo.entidades.categoria import Categoria
from src.modelo.enums.estado_movimiento import EstadoMovimiento
from src.modelo.enums.tipo_movimiento import TipoMovimiento


@dataclass
class Movimiento:
    monto: Decimal
    tipo_movimiento: TipoMovimiento
    descripcion: str
    fecha_transaccion: date
    notas: str
    categoria: str | None = None
    id_relacionado: str | None = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    estado: EstadoMovimiento = EstadoMovimiento.COMPLETADO

    @property
    def monto_con_signo(self) -> Decimal:
        """Retorna el monto con signo según el tipo de id_presupuestomovimiento"""
        return self.monto if self.tipo_movimiento == TipoMovimiento.INGRESO else -self.monto

    def __str__(self):
        return f"""
id: {self.id}
descripcion: {self.descripcion}
monto: {str(self.monto)}
fecha transacción: {str(self.fecha_transaccion)}
categoria: {self.categoria}
estado: {self.estado}
notas: {self.notas}
"""