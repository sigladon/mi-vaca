from enum import Enum

from src.modelo.transaccion.tipo_transaccion import TipoTransaccion


class TiposTransaccion(Enum):
    INGRESO = TipoTransaccion(1, "Ingreso", "Transacción de dinero que aumenta el saldo.")
    EGRESO = TipoTransaccion(2, "Egreso", "Transacción de dinero que disminuye el saldo.")