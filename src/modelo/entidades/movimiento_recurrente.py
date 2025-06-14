from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID

from src.modelo.entidades.categoria import Categoria
from src.modelo.enums.tipo_movimiento import TipoMovimiento


@dataclass
class MovimientoRecurrente:
    id_presupuesto: UUID
    nombre: str
    monto: Decimal
    tipo_movimiento: TipoMovimiento
    categoria: Categoria
    frecuencia_en_dias: int
    proxima_fecha: date
    esta_activo: bool = True
    descripcion: str = ""

    def debe_ejecutarse(self, fecha_a_evaluar: date) -> bool:
        """Verifica si la transacción debe ejecutarse en la fecha dada"""
        return self.esta_activo and fecha_a_evaluar >= self.proxima_fecha

    def calcular_proxima_fecha(self, fecha_base: date) -> date:
        """Calcula la próxima fecha de ejecución"""
        return fecha_base + timedelta(days=self.frecuencia_en_dias)
