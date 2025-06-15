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
    id_vinculado: str
    categoria: Categoria
    descripcion: str
    fecha_transaccion: date
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    estado: EstadoMovimiento = EstadoMovimiento.COMPLETADO
    id_meta: Optional[UUID] = None
    id_transaccion_recurrente: Optional[UUID] = None

    @property
    def monto_con_signo(self) -> Decimal:
        """Retorna el monto con signo según el tipo de id_presupuestomovimiento"""
        return self.monto if self.tipo_movimiento == TipoMovimiento.INGRESO else -self.monto