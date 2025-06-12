from src.modelo.transaccion import Transaccion


class Presupuesto:
    def __init__(self, categoria, monto, periodo, fecha_inicio, recibir_notificaciones, repeticiones_restantes = -1, descripcion = "",
                 gastos=None, gasto_total = 0):

        if gastos is None:
            gastos = list()
        self.categoria = categoria
        self.monto = monto
        self.fecha_inicio = fecha_inicio
        self.periodo = periodo
        self.repeticiones_restantes = repeticiones_restantes
        self.gastos = gastos
        self.descripcion = descripcion
        self.recibir_notificaciones = recibir_notificaciones
        self.gasto_total = gasto_total

    def agregar_gasto_categoria(self, gasto: Transaccion):
        self.gastos.append(gasto)
        self.gasto_total += gasto.monto
