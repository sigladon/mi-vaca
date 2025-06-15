import uuid
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from functools import reduce
from typing import Dict, List, Set
from uuid import UUID

from src.modelo.enums.estado_movimiento import EstadoMovimiento
from src.modelo.enums.tipo_movimiento import TipoMovimiento
from src.modelo.entidades.movimiento import Movimiento


@dataclass
class Presupuesto:
    nombre: str
    limite: Decimal
    inicio_presupuesto: date
    fin_presupuesto: date
    notificar_usuario: bool
    categorias: Dict[str, bool]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    esta_activo: bool = True
    notas: str = ""
    movimientos: Set[str] = field(default_factory=set)

    def obtener_monto_gastado(self, movimientos: List['Movimiento']) -> Decimal:
        """Calcula el monto gastado en el presupuesto"""
        return reduce(
            lambda total, mov: total + (mov.monto if mov.tipo_movimiento == TipoMovimiento.EGRESO else -mov.monto),
            filter(lambda m: m.id_vinculado == self.id and m.estado == EstadoMovimiento.COMPLETADO, movimientos),
            Decimal('0')
        )

    def obtener_cantidad_restante(self) -> Decimal:
        """Calcula el monto restante del presupuesto"""
        return self.limite - self.obtener_monto_gastado()

    def obtener_porcentaje(self, movimientos: List['Movimiento']):
        return self.obtener_monto_gastado(movimientos) / self.limite * 100

    def esta_dentro_periodo(self, fecha_a_evaluar: date) -> bool:
        """Verifica si una fecha está dentro del período del presupuesto"""
        return self.inicio_presupuesto <= fecha_a_evaluar <= self.fin_presupuesto

    def agregar_egreso(self, id_egreso: str):
        """Agrega un egreso al presupuesto"""
        self.movimientos = id_egreso