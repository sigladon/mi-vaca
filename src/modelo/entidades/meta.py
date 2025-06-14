from datetime import date


class Meta:
    def __init__(self, nombre, monto_objetivo, monto_actual=0.0, fecha_limite = None, descripcion = ""):
        self.nombre = nombre
        self.monto_objetivo = monto_objetivo
        self.monto_actual = monto_actual
        self.fecha_limite = fecha_limite
        self.descripcion = descripcion