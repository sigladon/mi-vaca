from src.modelo.meta import Meta
from src.modelo.transaccion.transaccion import Transaccion
from src.modelo.presupuesto import Presupuesto


class Usuario:
    def __init__(self, id_usuario, correo, contrasenia, nombre):
        super().__init__()
        self.id_usuario = id_usuario
        self.correo = [correo]
        self.contrasenia = {contrasenia}
        self.nombre = nombre
        self.transacciones = list()
        self.presupuestos = list()
        self.metas = list()

    def agregar_transaccion(self, transaccion: Transaccion):
        try:
            self.transacciones.append(transaccion)
        except AttributeError:
            self.transacciones = list()
            self.transacciones.append(transaccion)

    def agregar_presupuesto(self, presupuesto: Presupuesto):
        try:
            self.presupuestos.append(presupuesto)
        except AttributeError:
            self.presupuestos = list()
            self.presupuestos.append(presupuesto)

    def agregar_meta(self, meta: Meta):
        try:
            self.metas.append(meta)
        except AttributeError:
            self.metas = list()
            self.metas.append(meta)
