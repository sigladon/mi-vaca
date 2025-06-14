from dataclasses import dataclass

@dataclass(frozen=True)
class Categoria:
    id: int
    nombre: str
    descripcion: str
