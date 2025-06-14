from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from functools import reduce
from typing import Dict, List
from uuid import UUID

from src.modelo.enums.estado_movimiento import EstadoMovimiento
from src.modelo.enums.tipo_movimiento import TipoMovimiento
from src.modelo.entidades.movimiento import Movimiento


@dataclass
class Presupuesto:
    id: UUID
    nombre: str
    limite: Decimal
    inicio_periodo: date
    fin_periodo: date
    periodo_en_dias: int
    esta_activo: bool = True
    descripcion: str = ""
    categorias: Dict[str, float] = field(default_factory=dict)

    def obtener_monto_gastado(self, movimientos: List['Movimiento']) -> Decimal:
        """Calcula el monto gastado en el presupuesto"""
        return reduce(
            lambda total, mov: total + (mov.monto if mov.tipo_movimiento == TipoMovimiento.EGRESO else -mov.monto),
            filter(lambda m: m.id_presupuesto == self.id and m.estado == EstadoMovimiento.COMPLETADO, movimientos),
            Decimal('0')
        )

    def obtener_cantidad_restante(self, movimientos: List['Movimiento']) -> Decimal:
        """Calcula el monto restante del presupuesto"""
        return self.limite - self.obtener_monto_gastado(movimientos)

    def esta_dentro_periodo(self, fecha_a_evaluar: date) -> bool:
        """Verifica si una fecha está dentro del período del presupuesto"""
        return self.inicio_periodo <= fecha_a_evaluar <= self.fin_periodo
