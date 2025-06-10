from dataclasses import dataclass

@dataclass(frozen=True)
class TipoTransaccion:
    id: int
    nombre: str
    descripcion: str

