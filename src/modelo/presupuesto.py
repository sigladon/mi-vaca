class Presupuesto:
    def __init__(self, categoria, monto, periodo, recibir_notificaciones, descripcion = ""):
        self.categoria = categoria
        self.monto = monto
        self.periodo = periodo
        self.descripcion = descripcion
        self.recibir_notificaciones = recibir_notificaciones