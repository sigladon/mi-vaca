from enum import Enum


class EstadoMovimiento(Enum):
    PENDIENTE = "Pendiente"
    COMPLETADO = "Completado"
    CANCELADO = "Cancelado"