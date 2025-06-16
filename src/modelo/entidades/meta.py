import uuid
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from functools import reduce
from typing import Set, List

from src.modelo.entidades.movimiento import Movimiento
from src.modelo.enums.estado_movimiento import EstadoMovimiento


@dataclass
class Meta:
    nombre: str
    monto_objetivo: Decimal
    fecha_limite: date
    descripcion: str
    fecha_inicio: date = date.today()
    monto_base: Decimal = Decimal('0.00')
    monto_actual: Decimal = Decimal('0.00')
    esta_activo: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    movimientos: Set[str] = field(default_factory=set)

    def agregar_egreso(self, id_egreso: str):
        """Agrega un egreso a la meta"""
        self.movimientos.add(id_egreso)

    def obtener_monto_reunido(self, movimientos: List['Movimiento']) -> Decimal:
        """Calcula el monto gastado en el presupuesto"""
        self.monto_actual = self.monto_base + reduce(
            lambda total, mov: total + mov.monto,
            filter(lambda m: m.id in self.movimientos, movimientos),
            Decimal('0')
        )
        return self.monto_actual

    def obtener_cantidad_restante(self) -> Decimal:
        """Calcula el monto restante del presupuesto"""
        return self.monto_objetivo - self.monto_actual

    def obtener_porcentaje(self):
        return self.monto_actual / self.monto_objetivo * 100

    def esta_dentro_periodo(self, fecha_a_evaluar: date) -> bool:
        """Verifica si una fecha está dentro del período del presupuesto"""
        return self.fecha_inicio <= fecha_a_evaluar <= self.fecha_limite